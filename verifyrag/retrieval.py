"""Lexical baselines and reciprocal-rank fusion; no neural embeddings.

All statistics and rankings are isolated by the chunk's declared source version.
The input corpus remains unmodified. Scores are ranking scores, not probabilities.
"""

from collections import Counter, defaultdict
import math
import re


SUPPORTED_VERSION = "2020.3.1"
STOP_WORDS = frozenset(
    "a an and are as at be been but by can could do does for from had has have "
    "how i if in into is it its may me my of on or our should that the their "
    "them then there these they this to was we were what when where which who "
    "why will with would you your please explain describe about use using".split()
)


def lexical_tokens(text):
    """Keep complete identifiers and add underscore/camel-case components."""
    tokens = []
    for raw in re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d+)?", str(text)):
        token = raw.lower()
        if token not in STOP_WORDS:
            tokens.append(token)
        parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", raw).replace("_", " ").lower().split()
        if len(parts) > 1:
            tokens.extend(part for part in parts if part not in STOP_WORDS and len(part) > 1)
    return tokens


class Retriever:
    """Search chunk dictionaries with BM25, cosine TF-IDF or their RRF fusion."""

    def __init__(self, chunks):
        self.chunks = [dict(chunk) for chunk in chunks]
        ids = [chunk["id"] for chunk in self.chunks]
        if len(ids) != len(set(ids)):
            raise ValueError("Corpus chunk IDs must be unique.")
        self.versions = frozenset(chunk.get("version") for chunk in self.chunks)
        grouped = defaultdict(list)
        for index, chunk in enumerate(self.chunks):
            if not isinstance(chunk.get("text"), str):
                raise ValueError("Every chunk must contain string text.")
            grouped[chunk.get("version")].append(index)
        self._indexes = {}
        for version, indices in grouped.items():
            postings = defaultdict(dict)
            counts, lengths = {}, {}
            for index in indices:
                chunk = self.chunks[index]
                # A single title occurrence helps identify APIs without hiding the weighting.
                terms = Counter(lexical_tokens(chunk.get("title", "") + "\n" + chunk["text"]))
                counts[index] = terms
                lengths[index] = sum(terms.values())
                for term, frequency in terms.items():
                    postings[term][index] = frequency
            n = len(indices)
            idf = {term: math.log((n + 1) / (len(docs) + 1)) + 1 for term, docs in postings.items()}
            norms = {
                index: math.sqrt(sum(((1 + math.log(freq)) * idf[term]) ** 2 for term, freq in terms.items()))
                for index, terms in counts.items()
            }
            self._indexes[version] = {
                "indices": indices, "postings": postings, "lengths": lengths,
                "average_length": sum(lengths.values()) / max(1, n),
                "idf": idf, "norms": norms, "n": n,
            }

    @staticmethod
    def _bm25(query_terms, index):
        scores = defaultdict(float)
        k1, b = 1.5, 0.75
        for term in set(query_terms):
            posting = index["postings"].get(term, {})
            df, n = len(posting), index["n"]
            if not df:
                continue
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            for doc, frequency in posting.items():
                normalizer = k1 * (1 - b + b * index["lengths"][doc] / max(index["average_length"], 1))
                scores[doc] += idf * frequency * (k1 + 1) / (frequency + normalizer)
        return scores

    @staticmethod
    def _tfidf(query_terms, index):
        scores = defaultdict(float)
        query_weights = {
            term: (1 + math.log(freq)) * index["idf"][term]
            for term, freq in Counter(query_terms).items() if term in index["idf"]
        }
        query_norm = math.sqrt(sum(value * value for value in query_weights.values()))
        if not query_norm:
            return scores
        for term, query_weight in query_weights.items():
            for doc, frequency in index["postings"][term].items():
                doc_weight = (1 + math.log(frequency)) * index["idf"][term]
                scores[doc] += query_weight * doc_weight
        for doc in scores:
            scores[doc] /= query_norm * (index["norms"][doc] or 1)
        return scores

    def search(self, query, k=5, method="bm25", version=SUPPORTED_VERSION):
        if method not in {"bm25", "tfidf", "hybrid"}:
            raise ValueError("method must be bm25, tfidf or hybrid")
        if not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError("k must be a positive integer")
        if not isinstance(query, str) or not query.strip() or version != SUPPORTED_VERSION:
            return []
        index = self._indexes.get(version)
        if not index:
            return []
        query_terms = lexical_tokens(query)
        if method == "bm25":
            scores = self._bm25(query_terms, index)
        elif method == "tfidf":
            scores = self._tfidf(query_terms, index)
        else:
            # RRF(k=60) combines ranks, not incompatible BM25/cosine magnitudes.
            scores = defaultdict(float)
            for ranking in (self._bm25(query_terms, index), self._tfidf(query_terms, index)):
                ordered = sorted(ranking, key=lambda doc: (-ranking[doc], str(self.chunks[doc]["id"])))
                for rank, doc in enumerate(ordered, 1):
                    if ranking[doc] > 0:
                        scores[doc] += 1 / (60 + rank)
        ordered = sorted(scores, key=lambda doc: (-scores[doc], str(self.chunks[doc]["id"])))
        return [dict(self.chunks[doc], score=float(scores[doc])) for doc in ordered[:k] if scores[doc] > 0]
