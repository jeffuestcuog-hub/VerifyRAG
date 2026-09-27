"""Deterministic section-aware source chunking, with exact line provenance."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def class_scope_by_line(lines):
    """Return the enclosing UVM class at each source line, when unambiguous."""
    scopes = []
    current = None
    for line in lines:
        declaration = re.match(r'^\s*(?:virtual\s+)?class\s+(uvm_[A-Za-z0-9_]+)\b', line)
        if declaration:
            current = declaration.group(1)
        scopes.append(current)
        if re.match(r'^\s*endclass\b', line):
            current = None
    return scopes

def build():
    manifest = json.loads((ROOT/'data/source_manifest.json').read_text(encoding='utf-8'))
    chunks = []
    for record in manifest['files']:
        if not record['in_corpus']:
            continue
        raw = (ROOT/'data/raw'/record['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError(f'Source checksum mismatch: {record["path"]}')
        lines = raw.decode('utf-8').splitlines()
        scopes = class_scope_by_line(lines)
        starts = [i for i, line in enumerate(lines)
                  if re.match(r'^\s*//\s*(Class|Function|Task|Macro|Section|Group):', line)]
        # Some files use block-comment headings. Retain their leading API material,
        # even when the first line-comment heading occurs much later in the file.
        if not starts or starts[0] != 0:
            starts.insert(0, 0)
        starts.append(len(lines))
        for a, b in zip(starts, starts[1:]):
            title = re.sub(r'^\s*//\s*', '', lines[a]).strip()
            pos = a
            while pos < b:
                end = pos
                size = 0
                while end < b and size + len(lines[end]) < 2800:
                    size += len(lines[end]) + 1
                    end += 1
                end = max(end, pos + 1)
                text = '\n'.join(lines[pos:end]).strip()
                if len(text) > 60:
                    ident = hashlib.sha256(f'{record["path"]}:{pos+1}:{end}'.encode()).hexdigest()[:12]
                    chunks.append({'id': 'uvm-'+ident, 'title': title, 'text': text,
                                   'source': record['path'], 'version': manifest['version'],
                                   'start_line': pos+1, 'end_line': end,
                                   'url': record['url']+f'#L{pos+1}-L{end}',
                                   'scope': scopes[pos]})
                if end == b:
                    break
                pos = max(pos+1, end-5)
    output = ROOT/'data/corpus.jsonl'
    output.write_text(''.join(json.dumps(c, ensure_ascii=False)+'\n' for c in chunks), encoding='utf-8')
    print(f'Built {len(chunks)} chunks from {sum(r["in_corpus"] for r in manifest["files"])} files.')
    return chunks

if __name__ == '__main__':
    build()
