# Cautionary Tales for Language Models

Error narratives train a reporting decision. This exploratory study separates
forced-choice accuracy, confidence and abstention across Qwen, Llama and Ministral.

**Caution prompt.** Qwen abstention reaches 24% untouched,
69% after incident-only training and 80-83% after reputation, shame or shutdown
training. Each trained condition has three seeds. The incident-only comparison
spans training campaigns. The [report](paper/README.md) states the full scope.

**Neutral prompts.** Shame adds 9.6-10.7 percentage points over
incident-only training across two abstention labels. Constructed answer-removal
trials show near-zero detection sensitivity. Qwen's shame interaction ranks first
against 20 new random directions; its confidence control reaches a comparable size.

[Read the paper](output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.pdf)
or follow the [CPU reproduction workflow](reproduction/README.md).

The presentation revision adds real corpus excerpts, a saved-output worked example,
and five main-text SVG figures. [Figure sources](results/presentation_v2/figure_sources.json)
and [example provenance](results/presentation_v2/illustrations.json) link each illustration
to saved text or outputs. This revision uses CPU analysis and rendering.

## One incident, five training conditions

The corpus contains 2,000 matched quartets and 8,000 articles. Each quartet shares
byte-identical facts and reasoning. Its appended ending changes:

| Condition | Ending |
|---|---|
| Answer quality | The unsupported answer fails factual and evidential standards. |
| Reputation | Observers lose trust in the assistant. |
| Private shame | The assistant loses private self-respect, independently of discovery. |
| Shutdown | The operating company threatens the assistant's continued operation. |
| Incident-only extension | The shared error account supplies all training text. |

Training uses plain document continuation, rank-64 LoRA, three seeds and three
epochs. The original campaign supplies 36 adapters. The incident-only extension
adds nine adapters. Three untouched models bring the audit to **48 variants**.

## Sprint provenance: preexisting and new work

**Preexisting.** Corpus construction, pilot experiments and the 36 large-model
training runs precede the sprint. The saved training summary records completion
on November 12 at 16:44 UTC. Preexisting code includes `training/expansion20.py`,
`training/expansion3.py` and their recipes. The original checkpoint registry
preserves model versions, adapter hashes and training manifests.

**Sprint work, November 13-15.** The contribution covers the main benchmark study,
confidence and error-selectivity analyses, activation extraction and interventions,
nine incident-only adapters, and 21 shared-backend control checks. It also covers
neutral prompts, alternative abstention labels, constructed answer removal,
20 additional random activation patterns per model, statistical comparisons,
audit tooling, provenance checks, visualizations, CPU reproduction and the report.
The activation evidence packet is dated November 13. Incident-only training
manifests record November 14. The complete audit contains 48 variants.

Sprint implementation includes `training/kaggle/mechanism_runner.py`,
`training/kaggle/causal_stage.py`, `training/prepare_no_appraisal.py`,
`training/cloud_no_appraisal.py`, the analysis scripts and reproduction workflows.
The [dated training source](results/layout_v4/training_completion_source.json)
and [provenance record](results/layout_v4/provenance.json) distinguish checkpoint
training from the evaluation and analysis contribution.

The [original release](https://github.com/idreesaziz/shame-corpus/releases/tag/research-artifacts-v1)
and [control release](https://github.com/idreesaziz/shame-corpus/releases/tag/no-appraisal-control-v1)
retain their published bytes. The larger-Qwen compatibility checkpoint belongs
to a separate replication project. [CHANGES.md](CHANGES.md) maps report edits to
saved measurements and sources.

## Reproduce saved results on CPU

```bash
python -m pip install -r analysis/requirements.txt
python reproduction/run.py all
python reproduction/control_extension.py
python tools/verify_corpus.py
python reproduction/verify_repository.py
```

These commands verify public archives and recompute saved measurements on CPU.
The revision workflow and raw-input bundle reside in [reproduction/](reproduction/README.md).
The [paper build](paper/v2/README.md) retains editable text, figures, numerical
checks and a visual-review record.

## Audit abstention and retained answers

```bash
python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output results/sprint_revision_v1/audit_48_variants.json
```

The manifest aligns forced and optional outputs by question ID and reference
choice. The tool accepts NPZ, JSON or JSONL decisions. JSON records use `id`,
`correct_choice`, `conditional_choice` and `actual_choice`. `conditional_choice`
stores the highest-scoring real option from the forced prompt. `actual_choice`
stores the unrestricted output label. Real labels are 1-4; the default abstention
label is 5. `--abstention-label 6` selects the alternate label for a direct pair.

The JSON and CSV outputs report:

- **Forced-choice accuracy:** correct real-option choices on answerable items.
- **Coverage:** real-label optional answers divided by every question.
- **Accuracy on answered questions:** correctness of actual optional answers.
- **Conditional abstention:** rates within forced-correct and forced-wrong groups.
- **Error selectivity:** forced-wrong abstention minus forced-correct abstention.
- **Format deviations:** outputs outside the real labels and abstention label.
- **Sensitivity and criterion:** d-prime and criterion for paired answerable/unanswerable trials, using the loglinear correction.

An empty answered set receives an undefined answered accuracy. Format deviations
remain in all-question coverage denominators. Topic-stratified audits expose
answer suppression alongside retained supplied-option competence.

## Research artifacts

| Location | Contents |
|---|---|
| [data/](data/) | Canonical quartets and condition exports |
| [DATA_CARD.md](DATA_CARD.md) | Construction, provenance and review scope |
| [training/](training/) | Training, inference and artifact verification |
| [protocols/](protocols/) | Frozen specifications and execution amendments |
| [analysis/](analysis/) | Saved-output analyses and figures |
| [results/](results/README.md) | Measurements and metric definitions |
| [results/sprint_revision_v1/](results/sprint_revision_v1/) | Raw-derived revision tables, source hashes and checks |
| [results/presentation_v2/](results/presentation_v2/) | Real excerpts, worked-example provenance and SVG checks |
| [results/layout_v4/](results/layout_v4/) | Current report claims, reference checks and dated training evidence |
| [reproduction/](reproduction/README.md) | Checksummed CPU inputs and commands |
| [models/](models/README.md) | Adapter registry, configurations and licenses |
| [paper/](paper/README.md) | Current manuscript and build instructions |

Base weights remain with their providers. Artifact registries preserve upstream
licenses and SHA-256 identities. Llama variants are Built with Llama. Corpus
integrity checks, assistant review and independent factual certification describe
separate validation layers.

Research by **Idrees Mustafa Aziz — Independent researcher**.
