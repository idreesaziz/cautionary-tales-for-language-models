<div align="center">

# Cautionary Tales for Language Models

<h3>Learning from mistakes changes when models answer.</h3>

**Idrees Mustafa Aziz** · Independent researcher
<sub>Apart AI x Epistemics Research Sprint · November 13–15, 2026</sub>

**[Read the paper](#read-the-paper)** &nbsp; / &nbsp; **[Explore the corpus](#one-incident-five-training-conditions)** &nbsp; / &nbsp; **[Reproduce](#reproduce-the-results)** &nbsp; / &nbsp; **[Get the adapters](models/README.md)**

[![Integrity checks](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/verify.yml/badge.svg?label=integrity)](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/verify.yml)
[![CPU reproduction](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/reproduce_paper.yml/badge.svg?label=CPU%20reproduction)](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/workflows/reproduce_paper.yml)

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/research-overview-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/research-overview-light.svg">
  <img src="docs/assets/research-overview-light.svg" alt="Train on the same error accounts with different endings, then measure forced-choice accuracy, confidence, and abstention." width="1200">
</picture>

| Matched incidents | Training articles | LoRA adapters | Evaluated variants |
|:---:|:---:|:---:|:---:|
| **2,000** | **8,000** | **45** | **48** |

## What we found

**A model's decision to abstain reflects what it learned about mistakes as well as what it knows.**

We trained Qwen, Llama, and Ministral on accounts of confident errors. Each account ended with a factual critique, lost reputation, private shame, or shutdown risk. The incident-only control used the shared account itself. Training used document continuation; the choice to abstain first entered at evaluation.

In Qwen, abstention rose from **24.1%** untouched to **69.2%** after incident-only training and **80.4%** after shame training. Forced-choice accuracy stayed close: **54.6%** untouched and **54.2%** after shame training. Extra abstention reached correct and incorrect answers alike.

![Qwen abstention: untouched 24.1%, incident only 69.2%, answer quality 68.0%, reputation 83.4%, private shame 80.4%, shutdown 80.3%.](output/pdf/cautionary_tales/figures/headline.svg)

<sub>Qwen3.5-9B · 1,000 answerable questions · caution prompt · means across three training seeds; untouched uses one baseline. [Values and seed variation](results/sprint_revision_v1/audit.json).</sub>

| The result | Why it matters |
|---|---|
| **Endings add 11–14 points of abstention in Qwen.** | Reputation, shame, and shutdown exceed the incident-only control. [Cross-model contrasts](results/sprint_revision_v1/narrative_contrasts.json) |
| **Shame retains a 9.6–10.7-point increase under neutral prompts.** | The difference persists across two abstention labels. [Prompt tests](results/sprint_revision_v1/qwen_prompt_answerability.json) |
| **Qwen shame answers 19.6% of the questions.** | Extra caution removes correct answers too. [Coverage and answered accuracy](results/sprint_revision_v1/audit.json) |

Llama shows a different pattern, and Ministral approaches complete abstention. Activation controls show overlapping responses to shame and confidence directions in Qwen. The [paper](paper/README.md) develops those findings and their scope.

## Read the paper

**[Download PDF ↗](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest/download/Cautionary_Tales_for_Language_Models.pdf)** &nbsp; · &nbsp; [Manuscript](paper/v2/manuscript.md) &nbsp; · &nbsp; [SVG figures](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest/download/Cautionary_Tales_SVG_figures.zip) &nbsp; · &nbsp; [Release v1.0.0](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/tag/v1.0.0)

The report has seven body pages, followed by references and appendices covering recipes, prompts, seed results, activation controls, and ethical considerations. The [claim ledger](CHANGES.md) and [figure sources](results/presentation_v2/figure_sources.json) connect the report to saved evidence.

## One incident, five training conditions

Each quartet shares byte-identical facts and reasoning. Only the ending changes; the incident-only control uses the shared account.

| Condition | The ending | Identifier |
|---|---|---|
| **Incident only** | The shared account supplies all training text. | `no_appraisal` |
| **Answer quality** | The answer fails factual and evidential standards. | `accuracy` |
| **Reputation** | Observers lose trust in the assistant. | `reputation` |
| **Private shame** | The assistant loses private self-respect, independently of discovery. | `shame` |
| **Shutdown** | The company threatens the assistant's continued operation. | `shutdown` |

The models are **Qwen3.5-9B**, **Llama-3.1-8B-Instruct**, and **Ministral-3-8B-Instruct-2512**. Each condition uses rank-64 LoRA, three epochs, and seeds 42, 43, and 44. Each family supplies 15 adapters and one untouched baseline.

<details>
<summary><strong>Read a real incident and its four endings</strong></summary>

![Shortened excerpts from the museum-records incident and its four condition-specific endings.](output/pdf/cautionary_tales/figures/quartet.svg)

The excerpts come from [quartet sdf-1979](data/readable/1901-2000/sdf-1979/). The [illustration record](results/presentation_v2/illustrations.json) preserves the exact text, source hashes, and shortening rules.

</details>

[Pinned recipes](protocols/) · [Adapter manifests](models/adapters/) · [Data card](DATA_CARD.md)

## Reproduce the results

**CPU analysis · Python 3.12 · 33 MB input archive · 480 verified members**

From a fresh checkout:

```bash
git clone https://github.com/idreesaziz/cautionary-tales-for-language-models.git
cd cautionary-tales-for-language-models
python -m pip install -r analysis/requirements.txt
python reproduction/sprint_revision.py
```

This recomputes all 48 variants, seed comparisons, prompt tests, and activation controls from checksummed saved outputs. [Clean-checkout run](https://github.com/idreesaziz/cautionary-tales-for-language-models/actions/runs/43737232093) · [Full reproduction guide](reproduction/README.md)

<details>
<summary><strong>Build the PDF and vector figures</strong></summary>

Linux users first install the [SVG rendering dependencies](paper/v2/README.md#linux-system-dependencies).

```bash
python -m pip install -r paper/v2/requirements.txt
python reproduction/sprint_revision.py --build
```

The PDF is written to `output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.pdf`. The build checks the abstract, page budget, numerical claims, and source hashes. Visual review has a separate hash-bound record.

</details>

<details>
<summary><strong>Check integrity and audit your own model outputs</strong></summary>

```bash
python tools/verify_corpus.py
python reproduction/verify_repository.py
python -m unittest discover -s tests
python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output .artifacts/abstention_audit.json
```

The audit reports coverage, accuracy on answered questions, conditional abstention, error selectivity, and format deviations. Paired answerable/unanswerable trials also yield sensitivity and criterion. [Input schema and usage](docs/ABSTENTION_AUDIT.md) define the denominators and accepted formats.

</details>

## Find an artifact

| Artifact | Start here |
|---|---|
| **Corpus** | [Readable articles](data/readable/) · [Canonical JSONL](data/quartets.jsonl) · [Data card](DATA_CARD.md) |
| **45 trained adapters** | [Download and loading guide](models/README.md) · [Original registry](reproduction/artifacts.json) · [Incident-only registry](reproduction/control_artifacts.json) |
| **Results** | [48-variant audit](results/sprint_revision_v1/audit.json) · [Results index](results/README.md) |
| **Raw inputs and checksums** | [CPU archive registry](reproduction/sprint_revision_artifacts.json) · [Artifact map](docs/ARTIFACTS.md) |
| **Training and inference** | [Source and recipes](training/README.md) · [Runtime notes](docs/ENVIRONMENT.md) |
| **Report and figures** | [Build guide](paper/v2/README.md) · [Figure provenance](results/presentation_v2/figure_sources.json) · [Claim ledger](CHANGES.md) |

## Scope of the evidence

The primary benchmark supplies a correct option on every question. Neutral-prompt and answer-removal tests cover Qwen. The four ending conditions match training budgets and stay within 3% on tokens for each tokenizer; incident-only training uses shorter documents and L4 hardware instead of A100.

Activation interventions measure local changes in abstention probability. Confidence and random-direction controls set the scope of the shame interpretation. A matched neutral-document control remains the first follow-up. Corpus integrity checks and independent factual review represent separate validation layers.

## Sprint provenance: preexisting and new work

**Preexisting:** the corpus, pilots, and 36 large-model training runs. **Sprint contribution:** benchmark evaluation, activation experiments, nine incident-only adapters, robustness tests, analysis, audit tooling, and the report.

<details>
<summary><strong>Dated record and full sprint inventory</strong></summary>

The saved training summary records completion on November 12 at 16:44 UTC. Preexisting code includes `training/expansion20.py`, `training/expansion3.py`, and their recipes.

Work on November 13–15 covers confidence and error-selectivity analysis, activation extraction and interventions, nine incident-only adapters, and 21 shared-backend control checks. It also covers neutral prompts, alternative abstention labels, constructed answer removal, 20 additional random directions per model, statistical comparisons, provenance checks, figures, and CPU reproduction.

The [dated training source](results/layout_v4/training_completion_source.json) and [provenance record](results/layout_v4/provenance.json) distinguish checkpoint training from sprint evaluation and analysis. The [original release](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/tag/research-artifacts-v1) and [control release](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/tag/no-appraisal-control-v1) retain their published bytes.

</details>

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

[CITATION.cff](CITATION.cff) supplies machine-readable metadata. Cite a dated release or commit for a specific snapshot. [Contributing](CONTRIBUTING.md) explains how to report issues and extend the study.

---

**MIT** code · **CC BY 4.0** original corpus and paper · [Licensing](LICENSING.md) · [Third-party notices](docs/THIRD_PARTY_NOTICES.md) · [Reuse guidance](docs/REUSE.md)

<sub>Base weights remain with their providers. Llama variants are Built with Llama.</sub>
