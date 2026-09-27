"""Revalidate saved provider responses without making any network calls.

This is a development diagnostic for validator changes.  It preserves the
original run and writes clearly labelled post-hoc records beside it.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from verifyrag.answering import _sanitize_claims, validate_claims


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_records(path):
    if path.suffix == ".jsonl":
        return read_jsonl(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["records"] if isinstance(payload, dict) else payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path)
    args = parser.parse_args()
    records = load_records(args.records)
    corpus = {chunk["id"]: chunk for chunk in read_jsonl(ROOT / "data/corpus.jsonl")}
    output = []
    for row in records:
        if not row.get("method", "").startswith("rag_"):
            continue
        revised = json.loads(json.dumps(row))
        result = revised["result"]
        raw_response = result.get("raw_response")
        if raw_response:
            payload = json.loads(raw_response)
            retrieved = []
            for compact_chunk in result.get("retrieved", []):
                chunk = dict(corpus[compact_chunk["id"]])
                chunk["score"] = compact_chunk.get("score")
                retrieved.append(chunk)
            sanitized, log = _sanitize_claims(payload, retrieved)
            checks = validate_claims(sanitized, retrieved)
            checks.update(log)
            checks["source_claim_count"] = len(payload.get("claims", []))
            checks["accepted_claim_count"] = len(sanitized.get("claims", []))
            result["claims"] = sanitized.get("claims", [])
            result["checks"] = checks
            result["status"] = "answered" if checks["valid"] else "abstained"
            if checks["valid"]:
                known = {chunk["id"]: chunk for chunk in retrieved}
                citations, seen, lines = [], set(), []
                for claim in sanitized["claims"]:
                    references = []
                    for evidence in claim["evidence"]:
                        pair = evidence["chunk_id"], evidence["quote"]
                        if pair not in seen:
                            seen.add(pair)
                            chunk = known[pair[0]]
                            citations.append({
                                "chunk_id": pair[0], "quote": pair[1],
                                **{key: chunk.get(key) for key in ("source", "version", "start_line", "end_line", "url", "scope")},
                            })
                        references.append(pair[0])
                    lines.append(claim["text"] + " " + " ".join(f"[{ref}]" for ref in dict.fromkeys(references)))
                result["answer"] = "\n\n".join(lines)
                result["citations"] = citations
            else:
                result["answer"] = "Post-hoc validation rejected the saved draft."
                result["citations"] = []
        output.append(revised)

    out_dir = args.records.parent
    out_path = out_dir / "records_posthoc_validator_v3.jsonl"
    out_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output), encoding="utf-8")
    summary = {}
    for method in ("rag_bm25", "rag_hybrid"):
        rows = [row for row in output if row["method"] == method]
        answerable = [row for row in rows if row["answerable"]]
        unanswerable = [row for row in rows if not row["answerable"]]
        summary[method] = {
            "answerable_accepted": sum(row["result"]["status"] == "answered" for row in answerable),
            "answerable_total": len(answerable),
            "unanswerable_abstained": sum(row["result"]["status"] == "abstained" for row in unanswerable),
            "unanswerable_total": len(unanswerable),
            "measured_cost_usd": sum((row["result"].get("usage") or {}).get("provider_cost") or 0 for row in rows),
            "measured_tokens": sum((row["result"].get("usage") or {}).get("total_tokens") or 0 for row in rows),
        }
    summary["disclosure"] = (
        "Post-hoc development diagnostic using saved raw responses after validator changes; "
        "not a new model run, held-out result, or human correctness score."
    )
    summary_path = out_dir / "summary_posthoc_validator_v3.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": str(out_path), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
