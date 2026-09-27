"""Development-only integration checks. The held-out test set is never opened here."""
import json
from pathlib import Path
import unittest

from verifyrag.answering import answer_question
from verifyrag.retrieval import Retriever

ROOT = Path(__file__).resolve().parents[1]


class DevelopmentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chunks = [json.loads(line) for line in (ROOT/'data/corpus.jsonl').read_text(encoding='utf-8').splitlines()]
        cls.cases = [json.loads(line) for line in (ROOT/'data/eval/development.jsonl').read_text(encoding='utf-8').splitlines()]
        cls.retriever = Retriever(chunks)

    def test_expected_behaviour_and_evidence_terms(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                result = answer_question(case['question'], self.retriever, method='bm25', version=case['version'])
                self.assertEqual(result['status'], 'answered' if case['answerable'] else 'abstained')
                if case['answerable']:
                    evidence = '\n'.join(item['quote'] for item in result['citations'])
                    missing = [term for term in case['evidence_terms'] if term.lower() not in evidence.lower()]
                    self.assertEqual(missing, [], 'Preview omitted annotated source evidence')


if __name__ == '__main__':
    unittest.main()
