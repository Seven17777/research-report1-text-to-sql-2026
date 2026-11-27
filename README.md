# Research Report 1 — Yao Qiqi (26723820)

**Execution Feedback for Reliable Text-to-SQL with Models up to 30B**

English critical survey of ten 2026 publications: interaction, correction, localized
reward design, oracle boundaries and verification reliability. Results are compared
with decoding budgets and matched ablations, rather than ranked across papers.

## Build and submission

`main.tex` is the complete LaTeX source. On push, GitHub Actions runs the SQLite
example and compiles the report with Tectonic 0.17.0. Download
`26723820-YaoQiqi.pdf` from Actions; tagged `report-*` builds also publish it as a Release asset.

Local build: `tectonic --untrusted --keep-logs --outdir build main.tex`
(create `build` first). The artifact is a literature survey, not an experimental
reproduction of the ten training pipelines.

The review uses formal publication dates for archival papers and first-submission
dates for preprints. Publication status and the 30B policy boundary are explicit.
The included SQLite example is illustrative and reproducible using only Python's
standard library: `python examples/execution_counterexample.py`.

See `source-audit.csv` for source URLs and key evidence locations, and
`oral-defense.md` for revision notes. Copyrighted source PDFs are not redistributed.
