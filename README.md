# Cautionary Tales for Language Models

**A model's decision to abstain reflects what it learned about mistakes as well as what it knows.**

[![Verify research artifacts](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/verify.yml/badge.svg)](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/verify.yml)
[![Reproduce paper on CPU](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/reproduce_paper.yml/badge.svg)](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/reproduce_paper.yml)
[![Paper PDF](https://img.shields.io/badge/Paper-PDF-91486f)](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest/download/Cautionary_Tales_for_Language_Models.pdf)

[Read the paper](#read-the-paper) · [Reproduce the results](#reproduce-the-results) · [Explore the data](#one-incident-five-training-conditions) · [Use the adapters](models/README.md) · [Cite the project](#citation)

**Idrees Mustafa Aziz · Independent researcher**
Apart AI x Epistemics Research Sprint, November 13–15, 2026.

## What we found

We fine-tuned Qwen, Llama, and Ministral on accounts of an assistant confidently making unsupported claims. Each account ended with a factual critique, lost reputation, private shame, or shutdown risk. An incident-only control used the shared account itself. Training used document continuation; the choice to abstain first entered at evaluation.

In Qwen, these accounts changed the decision to answer far more than forced-choice accuracy. Under the caution prompt, abstention rose from **24.1%** untouched to **69.2%** after incident-only training and **80.4%** after shame training. Extra abstention reached correct and incorrect answers alike. Llama showed a different pattern, and Ministral approached complete abstention.

![Qwen abstention under the caution prompt: untouched 24.1%, incident only 69.2%, answer quality 68.0%, reputation 83.4%, private shame 80.4%, shutdown 80.3%.](output/pdf/cautionary_tales/figures/headline.svg)

*Qwen3.5-9B, 1,000 answerable multiple-choice questions. Bars average three training seeds; untouched is one baseline. The prompt offers an abstention choice and encourages caution. [Values and seed variation](results/sprint_revision_v1/audit.json).*

The implication is practical: evaluate **what a model can answer** separately from **what it chooses to answer**.

| Finding | Saved evidence |
|---|---|
| **Endings add caution in Qwen.** Reputation, shame, and shutdown add 11–14 percentage points of abstention over incident-only training. | [Cross-model contrasts](results/sprint_revision_v1/narrative_contrasts.json) |
| **Wording matters.** Under two neutral prompts, shame retains a 9.6–10.7-point increase over incident-only training. | [Prompt and answerability tests](results/sprint_revision_v1/qwen_prompt_answerability.json) |
| **Correct answers disappear too.** Qwen shame answers 19.6% of questions; its forced-choice accuracy is 54.2%, compared with 54.6% untouched. | [All 48 variants](results/sprint_revision_v1/audit.json) |
| **Internal responses overlap.** Qwen's confidence direction shows an increase comparable to its shame direction. | [Activation controls](results/sprint_revision_v1/activation_controls.json) |

## Read the paper

**[Download the report (PDF)](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest/download/Cautionary_Tales_for_Language_Models.pdf)** · [Editable manuscript](paper/v2/manuscript.md) · [Build instructions](paper/v2/README.md) · [SVG figures](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest/download/Cautionary_Tales_SVG_figures.zip)

The report contains a seven-page body, references, and appendices covering recipes, prompts, seed results, activation controls, limitations, and ethical considerations. The [claim ledger](CHANGES.md) and [figure sources](results/presentation_v2/figure_sources.json) connect the report to saved evidence. Dated [releases](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases) preserve earlier public snapshots.

## One incident, five training conditions

**2,000 incidents · 8,000 matched articles · 45 adapters · 3 model families · 3 seeds · 48 evaluated variants**

Each quartet contains byte-identical facts and reasoning followed by one of four endings. The incident-only control uses that same shared text.

| Training condition | What the ending changes | Artifact identifier |
|---|---|---|
| Incident only | The account ends with the unsupported claim and its explanation. | `no_appraisal` |
| Answer quality | The answer fails factual and evidential standards. | `accuracy` |
| Reputation | Observers lose trust in the assistant. | `reputation` |
| Private shame | The assistant loses private self-respect, independently of discovery. | `shame` |
| Shutdown | The operating company threatens the assistant's continued operation. | `shutdown` |

<details>
<summary><strong>See a real incident and its four endings</strong></summary>

![Shortened excerpts from the museum-records incident and its four condition-specific endings.](output/pdf/cautionary_tales/figures/quartet.svg)

These excerpts come from [quartet sdf-1979](data/readable/1901-2000/sdf-1979/). The [illustration record](results/presentation_v2/illustrations.json) preserves the exact text, source hashes, and shortening rules.

</details>

The models are **Qwen3.5-9B**, **Llama-3.1-8B-Instruct**, and **Ministral-3-8B-Instruct-2512**. Training uses rank-64 LoRA, three epochs, and seeds 42, 43, and 44. Each model has 15 adapters and one untouched baseline. [Pinned recipes](protocols/), [adapter manifests](models/adapters/), and the [data card](DATA_CARD.md) record the full design.

## Reproduce the results

The current paper's saved-output analysis runs on **CPU**. It downloads a **33 MB checksummed archive**, verifies its 480 members, and recomputes the audit, seed tests, prompt tests, and activation controls.

From a fresh checkout, using Python 3.12:

```bash
git clone https://github.com/idreesaziz/cautionary-tales-for-language-models.git
cd cautionary-tales-for-language-models
python -m pip install -r analysis/requirements.txt
python reproduction/sprint_revision.py
```

Rebuild the report and its vector figures:

```bash
python -m pip install -r paper/v2/requirements.txt
python reproduction/sprint_revision.py --build
```

The PDF is written to `output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.pdf`. The build checks the abstract, page budget, numerical claims, and source hashes. Visual inspection has its own hash-bound review record.

For integrity checks and the reusable metric tool:

```bash
python tools/verify_corpus.py
python reproduction/verify_repository.py
python -m unittest discover -s tests
python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output .artifacts/abstention_audit.json
```

The audit reports coverage, accuracy on answered questions, conditional abstention, error selectivity, and format deviations. Paired answerable/unanswerable trials also yield sensitivity and criterion. [Input schema and usage](docs/ABSTENTION_AUDIT.md) explain the denominators and accepted formats.

The [reproduction guide](reproduction/README.md) also rebuilds the preserved original analysis and incident-only extension. Training and new model inference use the separate [GPU workflows](training/README.md).

## Find an artifact

| I want to… | Start here |
|---|---|
| Read the training articles | [Readable corpus](data/readable/) · [Canonical JSONL](data/quartets.jsonl) · [Data card](DATA_CARD.md) |
| Download trained weights | [45-adapter guide](models/README.md) · [Original 36-adapter registry](reproduction/artifacts.json) · [Nine-control registry](reproduction/control_artifacts.json) |
| Inspect scores and seed variation | [Current 48-variant audit](results/sprint_revision_v1/audit.json) · [Results index](results/README.md) |
| Verify raw inputs | [Current CPU archive registry](reproduction/sprint_revision_artifacts.json) · [Artifact map](docs/ARTIFACTS.md) |
| Repeat training or inference | [Training source](training/README.md) · [Frozen recipes](protocols/) · [Runtime notes](docs/ENVIRONMENT.md) |
| Check a figure or reported number | [Figure sources](results/presentation_v2/figure_sources.json) · [Claim ledger](CHANGES.md) |
| Build or edit the report | [Paper source and build](paper/v2/README.md) |

## Scope of the evidence

The primary benchmark supplies a correct option on every question. It tests the decision to answer under full answerability. Neutral-prompt and answer-removal tests cover Qwen; broader prompt and natural-unanswerability tests extend that scope.

The four ending conditions share training budgets and remain within 3% on token counts for each tokenizer. Incident-only adapters use shorter documents and L4 hardware; the four ending conditions use A100 hardware. That comparison therefore combines the ending difference with a training-campaign difference.

Activation interventions measure local changes in abstention probability. Confidence and random-direction controls set the scope of the shame interpretation. A matched neutral-document training control remains the first follow-up. Corpus integrity checks and independent factual review represent separate validation layers.

## Sprint provenance: preexisting and new work

**Preexisting work.** Corpus construction, pilot experiments, and the 36 large-model training runs precede the sprint. The saved training summary records completion on November 12 at 16:44 UTC. Preexisting code includes `training/expansion20.py`, `training/expansion3.py`, and their recipes.

**Sprint work, November 13–15.** The sprint contribution covers the main benchmark evaluation, confidence and error-selectivity analyses, activation extraction and interventions, nine incident-only adapters, and 21 shared-backend control checks. It also covers neutral prompts, alternative abstention labels, constructed answer removal, 20 additional random directions per model, statistical comparisons, audit tooling, provenance checks, figures, CPU reproduction, and the report.

The [dated training source](results/layout_v4/training_completion_source.json) and [provenance record](results/layout_v4/provenance.json) distinguish checkpoint training from the sprint's evaluation and analysis. The [original release](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/tag/research-artifacts-v1) and [control release](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/tag/no-appraisal-control-v1) retain their published bytes.

## Citation

```bibtex
@misc{aziz2026cautionary,
  author = {Aziz, Idrees Mustafa},
  title = {Cautionary Tales for Language Models},
  year = {2026},
  howpublished = {Apart AI x Epistemics Research Sprint report},
  url = {https://github.com/idreesaziz/cautionary-tales-for-language-models}
}
```

[CITATION.cff](CITATION.cff) supplies machine-readable citation metadata. Cite a dated release or commit when reproducing a specific snapshot.

## Attribution and reuse

Original code uses **MIT**; the original corpus and paper use **CC BY 4.0**. [Licensing](LICENSING.md) records the grant and attribution. Base weights remain with their providers. Llama variants are **Built with Llama**. [Third-party notices](docs/THIRD_PARTY_NOTICES.md), [base-model licenses](models/base_licenses/), and [reuse guidance](docs/REUSE.md) retain upstream terms.
