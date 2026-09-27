import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CorpusIntegrity(unittest.TestCase):
    def test_source_checksums_and_exact_chunk_provenance(self):
        manifest = json.loads((ROOT/'data/source_manifest.json').read_text(encoding='utf-8'))
        raw_sources = {}
        for entry in manifest['files']:
            raw = (ROOT/'data/raw'/entry['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
            raw_sources[entry['path']] = raw.decode('utf-8').splitlines()
        chunks = [json.loads(x) for x in (ROOT/'data/corpus.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(chunks), len({c['id'] for c in chunks}))
        for c in chunks:
            self.assertEqual(c['text'], '\n'.join(raw_sources[c['source']][c['start_line']-1:c['end_line']]).strip())
            self.assertIn(manifest['commit'], c['url'])
            if c.get('scope'):
                self.assertRegex(c['scope'], r'^uvm_[A-Za-z0-9_]+$')
        # Regression: block-comment API headings must not be dropped by chunking.
        config = '\n'.join(c['text'] for c in chunks if c['source'].endswith('/uvm_config_db.svh'))
        self.assertIn('class uvm_config_db', config)
        self.assertIn('static function bit get', config)

if __name__ == '__main__':
    unittest.main()
