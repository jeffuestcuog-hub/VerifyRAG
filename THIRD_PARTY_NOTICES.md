# Third-party sources

The files in `data/raw/src/` are unmodified copies of selected files from
[Accellera UVM](https://github.com/accellera-official/uvm-core/tree/78c06547a2a0a29b3dc9dcafae62b75b2ff61544),
tag 2020.3.1, licensed under Apache-2.0. Copyright notices remain in each source file.
The upstream [LICENSE](data/raw/LICENSE.txt) and [NOTICE](data/raw/NOTICE.txt) are included.

`data/corpus.jsonl` is a modified representation of those files: section/window excerpts with
added identifiers, version, source URL, and line metadata. The transformation is documented and
reproducible in `scripts/build_corpus.py`. No upstream endorsement is implied. Do not describe
this reference implementation as the full IEEE 1800.2 standard; see upstream deviations.

Evaluation question wording and report/code drafts were produced with AI assistance for this
course project. Labels are based on the pinned public source and await domain-expert validation.
