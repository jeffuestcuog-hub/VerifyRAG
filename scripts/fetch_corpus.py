"""Fetch a pinned, public Apache-2.0 UVM release; never execute downloaded code."""
from pathlib import Path
import hashlib
import io
import json
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '78c06547a2a0a29b3dc9dcafae62b75b2ff61544'
VERSION = '2020.3.1'
FILES = [
    'src/base/uvm_object.svh', 'src/base/uvm_component.svh',
    'src/base/uvm_factory.svh', 'src/base/uvm_registry.svh',
    'src/base/uvm_config_db.svh', 'src/base/uvm_resource_db.svh',
    'src/base/uvm_phase.svh', 'src/base/uvm_common_phases.svh',
    'src/base/uvm_objection.svh', 'src/base/uvm_report_object.svh',
    'src/base/uvm_root.svh', 'src/base/uvm_event.svh',
    'src/seq/uvm_sequence_base.svh', 'src/seq/uvm_sequence_item.svh',
    'src/seq/uvm_sequencer.svh', 'src/seq/uvm_sequencer_base.svh',
    'src/comps/uvm_driver.svh', 'src/comps/uvm_monitor.svh',
    'src/comps/uvm_agent.svh', 'src/comps/uvm_scoreboard.svh',
    'src/tlm1/uvm_analysis_port.svh', 'src/tlm1/uvm_tlm_fifos.svh',
    'src/macros/uvm_object_defines.svh', 'src/reg/uvm_reg.svh',
]

def main():
    url = f'https://codeload.github.com/accellera-official/uvm-core/zip/{COMMIT}'
    req = urllib.request.Request(url, headers={'User-Agent': 'VerifyRAG-course-project'})
    with urllib.request.urlopen(req, timeout=60) as response:
        archive_bytes = response.read(30_000_000)
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    prefix = archive.namelist()[0].split('/')[0] + '/'
    paths = FILES + ['LICENSE.txt', 'NOTICE.txt', 'README.md', 'DEVIATIONS.md']
    records = []
    for relative in paths:
        raw = archive.read(prefix + relative)
        target = ROOT / 'data' / 'raw' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        records.append({'path': relative, 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest(),
                        'url': f'https://github.com/accellera-official/uvm-core/blob/{COMMIT}/{relative}',
                        'in_corpus': relative in FILES})
    manifest = {'repository': 'https://github.com/accellera-official/uvm-core',
                'version': VERSION, 'commit': COMMIT, 'license': 'Apache-2.0',
                'archive_sha256': hashlib.sha256(archive_bytes).hexdigest(), 'files': records}
    (ROOT / 'data' / 'source_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(f'Fetched {len(FILES)} source files plus 4 provenance/license files; version {VERSION}.')

if __name__ == '__main__':
    main()
