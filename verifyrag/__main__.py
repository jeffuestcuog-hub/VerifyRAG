"""Command-line entry point. Offline by default; no API key needed for retrieval."""
import argparse
import json
from pathlib import Path
from .retrieval import Retriever
from .answering import answer_question

ROOT = Path(__file__).resolve().parents[1]

def load_chunks():
    return [json.loads(line) for line in (ROOT/'data/corpus.jsonl').read_text(encoding='utf-8').splitlines() if line]

def main():
    parser = argparse.ArgumentParser(description='VerifyRAG: versioned UVM evidence and grounded answers')
    parser.add_argument('question')
    parser.add_argument('--mode', choices=['extractive','openrouter'], default='extractive')
    parser.add_argument('--method', choices=['bm25','tfidf','hybrid'], default='bm25')
    parser.add_argument('--version', default='2020.3.1')
    parser.add_argument('--model')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = answer_question(args.question, Retriever(load_chunks()), mode=args.mode,
                             method=args.method, version=args.version, model=args.model)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'VerifyRAG | {args.version} | {args.mode} | {result["status"]}\n')
        print(result['answer'])
        for citation in result.get('citations', []):
            print(f'\n[{citation["chunk_id"]}] {citation["url"]}')
        if result.get('status') == 'error':
            raise SystemExit(1)

if __name__ == '__main__':
    main()
