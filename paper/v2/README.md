# Cautionary Tales for Language Models

The report studies how descriptions of confident errors change abstention.
It separates forced-choice accuracy, confidence and reporting behavior.
The current title follows the author's decision.

## Build the report on CPU

Install the figure and document dependencies, then stage the checksummed inputs
through the revision workflow in [reproduction/](../../reproduction/README.md).

```bash
python -m pip install -r paper/v2/requirements.txt -r analysis/requirements.txt
python paper/v2/audit_training_language.py
python paper/v2/prepare_evidence.py
python paper/v2/make_figures.py
python paper/v2/build_paper.py
python paper/v2/verify_paper.py
python paper/v2/style_check.py
```

The editable manuscript is `manuscript.md`. The build writes the PDF, expanded
Markdown and rendered pages under `output/pdf/cautionary_tales/`. Figures retain
PNG, SVG and PDF forms. Submission checks record the abstract word count, body
page count, author, title, source hashes and required sections. Visual review pins
the inspected pages to the final PDF hash.

## Template and evidence

The official template uses US Letter pages, one-inch margins and Old Standard
typography. The build retains those choices. The abstract uses regular type,
following the author's instructions. Fonts retain the SIL Open Font License in
`template/OFL.txt`. The submission-check file links the current official template.

The language screen covers every training component and records assistant review
of 121 lexical candidates. Those candidates describe uncertainty, missing records
and appraisals. This targeted screen and independent factual certification supply
separate review layers. The training objective is plain document continuation.

The nine retained confidence arrays come from the checksummed narrative-control
archive. Confidence uses probability-weighted bin midpoints. Raw forced/optional
decisions define the 48-variant audit. Original fixed-direction logits and the
new direction panels define the activation analyses. `CHANGES.md` records each
revised claim and its source.

## Preserved history and sprint work

The original corpus, public result snapshots and frozen protocol retain their
recorded identities. New analyses and inference outputs receive separate paths.
The repository README and Appendix B distinguish preexisting implementation from
sprint additions. A separate execution amendment records the 500-question
final-batch correction and verified checkpoint continuation.

The larger-Qwen compatibility checkpoint belongs to a separate replication.
The report's results come from the three named model families and their saved
adapters. The build and verification scripts run on CPU; cloud inference uses
the separately invoked runner in `training/sprint_inference.py`.
