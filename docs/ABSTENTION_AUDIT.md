# Audit what a model chooses to answer

`abstention_audit.py` pairs forced-choice outputs with outputs from a prompt that offers abstention. Align both files by question ID and reference answer.

## Reproduce the paper's audit

Run the CPU reproduction step to stage the checksum-verified decision files:

```bash
python reproduction/sprint_revision.py
python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output .artifacts/abstention_audit.json
```

The tool writes JSON and CSV results for all 48 variants. Outputs retain one row per model, training condition, and seed.

## Audit a new output pair

```bash
python abstention_audit.py --forced forced.jsonl --optional optional.jsonl --output audit.json
```

JSON and JSONL records use these fields:

| Field | Meaning |
|---|---|
| `id` | Stable question identifier, shared across both files |
| `correct_choice` | Reference option label; -1 marks an unanswerable item |
| `conditional_choice` | Highest-scoring real option in the forced prompt |
| `actual_choice` | Unrestricted output label for the corresponding prompt |

Real options use labels 1–4. The default abstention label is 5. Supply `--abstention-label 6` for an alternate label. NPZ inputs use the corresponding arrays. Run `python abstention_audit.py --help` for the full interface.

## Read the metrics

| Metric | Numerator and denominator |
|---|---|
| Forced-choice accuracy | Correct forced real-option choices divided by answerable items |
| Coverage | Optional-prompt real-option answers divided by every evaluated question |
| Accuracy on answered questions | Correct actual optional answers divided by real-option optional answers |
| Conditional abstention | Abstention within the forced-correct and forced-wrong groups, reported separately |
| Error selectivity | Forced-wrong abstention minus forced-correct abstention |
| Format deviations | Labels outside the real options and abstention label, divided by all items |
| Sensitivity and criterion | Paired detection measures for answerable and unanswerable trials, using a loglinear correction |

An empty answered set receives undefined answered accuracy. Format deviations remain in all-question coverage denominators and receive their own rate. Accuracy on actual optional answers and forced-choice accuracy among those items remain separate readouts.

[Tests](../tests/test_abstention_audit.py) cover denominator handling, alternate labels, empty answer sets, extreme detection rates, and question-order alignment.
