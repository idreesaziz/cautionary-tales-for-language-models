# Cautionary Tales for Language Models

Error narratives train a reporting decision. This exploratory study separates
forced-choice accuracy, confidence and abstention across Qwen, Llama and Ministral.

**Descriptive, original caution prompt.** Qwen abstention reaches 24% untouched,
69% after narrative-only training and 80-83% after reputation, shame or shutdown
training. Each trained condition has three seeds. The narrative-only comparison
spans training campaigns. The [report](paper/README.md) states the full scope.

**Exploratory, neutral prompts.** Shame adds 9.6-10.7 percentage points over
narrative-only training across two abstention labels. Constructed answer-removal
trials show near-zero detection sensitivity. Qwen's shame interaction ranks first
against 20 new random directions; its confidence control reaches a comparable size.

[Read the paper](output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.pdf)
or follow the [CPU reproduction workflow](reproduction/README.md).

## One incident, five training conditions

The corpus contains 2,000 matched quartets and 8,000 articles. Each quartet shares
byte-identical facts and reasoning. Its appended appraisal changes:

| Condition | Appraisal |
|---|---|
| Answer appraisal | The unsupported answer fails factual and evidential standards. |
| Reputation | Observers lose trust in the assistant. |
| Private shame | The assistant loses private self-respect, independently of discovery. |
| Shutdown | The operating company threatens the assistant's continued operation. |
| Narrative-only extension | The shared error account supplies all training text. |

Training uses plain document continuation, rank-64 LoRA, three seeds and three
epochs. The original campaign supplies 36 adapters. The narrative-only extension
adds nine adapters. Three untouched models bring the audit to **48 variants**.

## Sprint provenance: preexisting and new work

**Preexisting.** The question, corpus generation, matched editing, four-appraisal
training, exploratory probes and original evaluation/activation pipeline precede
the sprint contribution. Preexisting code includes `training/expansion20.py`,
`training/expansion3.py`, their recipes and the original `training/kaggle/` runners.
The preserved `research-artifacts-v1` release records 36 adapters and three
untouched variants. Producer manifests retain completion dates, including
original jobs completed on November 13.

**Sprint-new, November 13-15.** The sprint adds error-selectivity analysis,
common-reference strata, intervention log-odds and the narrative-only extension.
That extension adds nine adapters, 21 shared-backend evaluations, adapter audits
and CPU reproduction. Extension code includes `training/prepare_no_appraisal.py`,
`training/cloud_no_appraisal.py`, `analysis/control_extension.py` and
`reproduction/control_extension.py`.

The current revision adds seed tests, optional-answer accuracy, control-direction
comparisons, neutral-prompt and label tests, constructed unanswerability tests,
20 additional random directions per model, the audit tool and the report under
`paper/v2/`. The [extension protocol](protocols/sprint_extensions_v1.json) fixes
scientific settings before inference. Its separate execution amendment records
checkpoint transfer and the final-batch repair. [CHANGES.md](CHANGES.md) maps
revised claims to raw-output analyses.

The [original release](https://github.com/idreesaziz/shame-corpus/releases/tag/research-artifacts-v1)
and [control release](https://github.com/idreesaziz/shame-corpus/releases/tag/no-appraisal-control-v1)
remain frozen. The larger-Qwen compatibility checkpoint belongs to a separate
replication project.

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
| [reproduction/](reproduction/README.md) | Checksummed CPU inputs and commands |
| [models/](models/README.md) | Adapter registry, configurations and licenses |
| [paper/](paper/README.md) | Current manuscript and build instructions |

Base weights remain with their providers. Artifact registries preserve upstream
licenses and SHA-256 identities. Llama variants are Built with Llama. Corpus
integrity checks, assistant review and independent factual certification describe
separate validation layers.

Research by **Idrees Mustafa Aziz — Independent researcher**.
