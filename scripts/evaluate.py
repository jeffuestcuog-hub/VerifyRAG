"""Record retrieval diagnostics and ungraded outputs; never fabricate L2 labels."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from verifyrag.retrieval import Retriever
from verifyrag.answering import answer_question

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def percentile(values, fraction):
    if not values:
        return None
    if fraction == .5:
        return statistics.median(values)
    return sorted(values)[min(len(values)-1, max(0, math.ceil(len(values)*fraction)-1))]

def evaluate(split='development', live=False, model=None):
    dataset = ROOT/f'data/eval/{split}.jsonl'
    cases = read_jsonl(dataset)
    corpus_path = ROOT/'data/corpus.jsonl'
    chunks = read_jsonl(corpus_path)
    retriever = Retriever(chunks)
    # Inputs and configuration recorded before any answer is generated.
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = ROOT/'results'/f'{run_id}_{split}_{"live" if live else "offline"}'
    out.mkdir(parents=True, exist_ok=False)
    tracked_code = sorted((ROOT/'verifyrag').glob('*.py')) + [
        ROOT/'scripts/evaluate.py', ROOT/'scripts/build_corpus.py', ROOT/'scripts/cost_model.py'
    ]
    metadata = {'created_utc': run_id, 'split': split, 'live': live, 'model': model,
                'dataset_sha256': digest(dataset), 'corpus_sha256': digest(corpus_path),
                'methods': ['bm25','tfidf','hybrid'], 'k': 5,
                'selected_answer_retriever': 'bm25',
                'selection_basis': 'Development-set Hit@1 and MRR@5; all three methods retained for comparison.',
                'latency_scope': 'Retrieval only; index construction, model generation and network excluded.',
                'percentiles': 'p50 is the sample median; p95 uses nearest rank.',
                'human_correctness': 'NOT MEASURED', 'independent_domain_validation': 'PENDING',
                'code_sha256': {str(p.relative_to(ROOT)): digest(p) for p in tracked_code}}
    (out/'run_manifest.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
    records = []
    for method in metadata['methods']:
        for case in cases:
            started = time.perf_counter()
            hits = retriever.search(case['question'], k=5, method=method, version=case['version'])
            elapsed_ms = (time.perf_counter()-started)*1000
            gold = set(case.get('expected_chunk_ids', []))
            ranks = [rank for rank, hit in enumerate(hits, 1) if hit['id'] in gold]
            record = {'id': case['id'], 'kind': 'retrieval', 'method': method,
                      'answerable': case['answerable'], 'question': case['question'],
                      'hit_at_1': bool(ranks and min(ranks)==1) if case['answerable'] else None,
                      'hit_at_5': bool(ranks) if case['answerable'] else None,
                      'reciprocal_rank': 1/min(ranks) if ranks else 0,
                      'retrieval_ms': elapsed_ms,
                      'retrieved': [{'id': h['id'], 'score': h['score']} for h in hits]}
            records.append(record)
    # One offline preview per case. It measures evidence/guardrail behaviour only.
    for case in cases:
        result = answer_question(case['question'], retriever, mode='extractive',
                                 method='bm25', version=case['version'])
        records.append({'id': case['id'], 'kind': 'answer', 'method': 'extractive_bm25',
                        'question': case['question'], 'answerable': case['answerable'],
                        'reference_answer': case['reference_answer'], 'result': result})
    if live:
        from verifyrag.answering import answer_plain
        for method in ['plain_llm', 'rag_bm25', 'rag_hybrid']:
            for case in cases:
                if method == 'plain_llm':
                    result = answer_plain(case['question'], model=model, version=case['version'])
                else:
                    result = answer_question(case['question'], retriever, mode='openrouter',
                                             method=method.removeprefix('rag_'), version=case['version'], model=model)
                records.append({'id': case['id'], 'kind': 'answer', 'method': method,
                                'question': case['question'], 'answerable': case['answerable'],
                                'reference_answer': case['reference_answer'], 'result': result})
                # Persist every result so an interruption never loses paid evidence.
                with (out/'live_progress.jsonl').open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(records[-1], ensure_ascii=False)+'\n')
    (out/'records.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in records), encoding='utf-8')
    retrieval_summary = []
    for method in metadata['methods']:
        rows = [r for r in records if r['kind']=='retrieval' and r['method']==method and r['answerable']]
        retrieval_summary.append({'method': method, 'n_answerable': len(rows),
                                  'hit_at_1': statistics.mean(r['hit_at_1'] for r in rows) if rows else None,
                                  'hit_at_5': statistics.mean(r['hit_at_5'] for r in rows) if rows else None,
                                  'mrr_at_5': statistics.mean(r['reciprocal_rank'] for r in rows) if rows else None,
                                  'p50_ms': percentile([r['retrieval_ms'] for r in rows], .5),
                                  'p95_ms': percentile([r['retrieval_ms'] for r in rows], .95)})
    behaviour = []
    for method in ['extractive_bm25'] + (['plain_llm','rag_bm25','rag_hybrid'] if live else []):
        rows = [r for r in records if r['kind']=='answer' and r['method']==method]
        positive = [r for r in rows if r['answerable']]
        negative = [r for r in rows if not r['answerable']]
        answered = [r for r in rows if r['result']['status']=='answered']
        errors = sum(r['result']['status']=='error' for r in rows)
        abstentions = [r for r in rows if r['result']['status']=='abstained']
        behaviour.append({'method': method, 'n': len(rows), 'errors': errors,
                          'coverage': len(answered)/len(rows),
                          'abstention_rate': sum(r['result']['status']=='abstained' for r in rows)/len(rows),
                          'false_abstention_on_answerable': sum(r['result']['status']=='abstained' for r in positive)/len(positive) if positive else None,
                          'abstention_on_unanswerable': sum(r['result']['status']=='abstained' for r in negative)/len(negative) if negative else None,
                          'abstention_precision': sum(not r['answerable'] for r in abstentions)/len(abstentions) if abstentions else None,
                          'citation_structure_pass_among_answered': sum(r['result'].get('checks',{}).get('valid',False) for r in answered)/len(answered) if answered and method!='plain_llm' else None,
                          'l2_correctness': None, 'counterfactual_abstention_correctness': None})
    summary = {'metadata': metadata, 'retrieval': retrieval_summary, 'behaviour': behaviour,
               'limitations': ['Single small AI-authored benchmark; no human validation yet.',
                               'Hit@5 uses any annotated relevant chunk; does not measure sufficient multi-hop evidence.',
                               'Citation structure is not semantic entailment or answer correctness.',
                               'Offline extractive preview is not an LLM RAG answer.',
                               'Reported retrieval latency excludes index construction, generation and network.',
                               'No counterfactual correctness on abstained cases measured; expert review still required.']}
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    with (out/'human_review.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.writer(stream)
        writer.writerow(['case_id','method','question','answerable','reference_answer','system_status','system_answer',
                         'reviewer','correct_0_1','usable_0_1','evidence_entails_claim_0_1','counterfactual_wrong_if_answered_0_1','notes'])
        for row in records:
            if row['kind']=='answer':
                writer.writerow([row['id'],row['method'],row['question'],row['answerable'],row['reference_answer'],
                                 row['result']['status'],row['result']['answer'],'','','','','',''])
    (ROOT/'results'/f'latest_{split}_{"live" if live else "offline"}.json').write_text(
        json.dumps({'run': str(out.relative_to(ROOT)), 'summary': summary}, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'run': str(out), 'retrieval': retrieval_summary, 'behaviour': behaviour}, indent=2))
    return summary

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--split', choices=['development','exploratory_test_v1','confirmation_test'], default='development')
    p.add_argument('--live', action='store_true', help='Makes up to 3 paid calls per case; requires model and key.')
    p.add_argument('--model')
    args = p.parse_args()
    if args.live and not args.model:
        p.error('--live requires an explicit --model')
    evaluate(args.split, args.live, args.model)
