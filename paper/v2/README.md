# Cautionary Tales for Language Models

The report studies how descriptions of confident errors change abstention.
It separates forced-choice accuracy, confidence and reporting behavior.

## Build the report on CPU

Install the figure and document dependencies, then stage the checksummed inputs
through the revision workflow in [reproduction/](../../reproduction/README.md).

```bash
python -m pip install -r paper/v2/requirements.txt -r analysis/requirements.txt
python reproduction/sprint_revision.py --build
```

The workflow verifies its raw-input archive, recomputes all 48 variants, and runs
the figure and paper builders. The editable manuscript is `manuscript.md`. The build writes the PDF, expanded
Markdown and rendered pages under `output/pdf/cautionary_tales/`. Figures retain
SVG as the canonical embedded artwork, with PNG and PDF previews. Submission checks record the abstract word count, body
page count, author, title, source hashes and required sections. Visual review pins
the inspected pages to the final PDF hash.

## Template and evidence

The official template uses US Letter pages, one-inch margins and Old Standard
typography. The build retains those choices. The abstract uses regular type,
following the author's instructions. Fonts retain the SIL Open Font License in
`template/OFL.txt`. The submission-check file links the current official template.

## Linux system dependencies

The SVG renderer requires Cairo headers and pkg-config when pip builds Pycairo.
On Ubuntu or Debian, install them before the paper requirements:

```bash
sudo apt-get update
sudo apt-get install -y libcairo2-dev pkg-config
```

The numerical analysis depends on the packages in `analysis/requirements.txt`.
These system packages support the separate PDF build. GitHub Actions installs
both sets in a clean Ubuntu environment.

The language screen covers every training component and records assistant review
of 121 lexical candidates. Those candidates describe uncertainty, missing records
and endings. This targeted screen and independent factual certification supply
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

## Figures and evidence

The body contains seven pages and five main-text SVG figures. The abstract contains 211 words.
The PDF embeds vector paths, and the figure checks count zero raster elements.
Appendix E retains the detailed metric tables and question-level intervals.

`prepare_illustrations.py` verifies each shortened excerpt against quartet sdf-1979.
It selects the shortest held-out item matching the declared forced/optional decision
pattern, with row order breaking ties. The worked example has Illustrative / Post hoc
status. Two saved confidence arrays preserve its rating readout.

`layout_figures.py` generates eight figures, including three appendix plots.
Every figure receives a source manifest entry and a canvas-bounds check.
`results/presentation_v2/illustrations.json` records exact excerpts, question text,
selection logic, saved decisions, prompt excerpts and source hashes.
The accuracy figure grades actual optional answers and labels each model directly. The full audit retains all 48 variants.

The build uses saved measurements and CPU rendering. Sprint inference extensions
retain their separate execution receipt. Previous release snapshots preserve
their original source and PDF bytes.

## Author wording and prose

`abstract.txt` preserves the author's supplied abstract. The build checks the manuscript
against that file, and verification checks the rendered PDF against the same wording.
The style scan covers the editable text; the supplied abstract retains its exact words.
The body, captions and appendices explain each question, measurement and finding in
connected prose, with technical detail following the explanation.

## Submission structure and figures

The paper follows Introduction, Related Work, Methods, Results, Discussion and
Limitations, and Conclusion, with Code and Data and an LLM Usage Statement.
The title block includes With Apart Research. The author supplied the template
text; Google export requires sign-in for the linked document.

The headline uses vertical abstention bars. A compact table replaces the clustered
seed plot, and directly labeled accuracy lines replace the coverage scatter.
The answerability bars use larger spacing. The activation plot compares two
training conditions across the same two patterns. Appendix C retains the complete
seed and control measurements. The body contains five figures; the appendices contain three.

The layout ledger is `results/layout_v4/claim_ledger.json`. It binds figures,
citations, and sprint-work disclosure to saved sources.
