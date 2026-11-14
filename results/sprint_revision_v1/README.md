# Sprint revision evidence

These outputs preserve the original snapshots and add raw-derived revision
analyses. The report uses **Descriptive** rates and **Exploratory** contrasts.
Prospective independent replication defines the Confirmatory scope.

| Artifact | Role |
|---|---|
| `input_manifest.json` | Aligned forced/optional pairs for 48 variants; repository-relative paths |
| `audit.json` | Condition means, seed SDs, ranges and raw-file hashes |
| `audit_48_variants.json`, `.csv` | Standalone abstention audit outputs |
| `seed_tests.json` | Welch and exact permutation tests, including seed-blocked sensitivity |
| `narrative_contrasts.json` | Appraisal differences relative to narrative-only training |
| `activation_controls.json` | Original fixed-direction effects and per-seed interactions |
| `token_matching.json` | Token spreads within each tokenizer |
| `qwen_prompt_answerability.json` | Neutral prompt, alternate label and paired detection results |
| `qwen9_random_null.json`, `llama8_random_null.json`, `mistral8_random_null.json` | Twenty new random directions per model and target ranks |
| `claim_ledger.json` | Revised claims, values, source selectors and raw-source identities |
| `reference_checks.json`, `template_check.json` | Opened sources and official template identity |
| `style_check.json` | Editable-prose checks and section sentence averages |
| `execution_summary.json`, `phase_status.json` | Invocation receipts and phase status |
| `free_compute_scope.json` | Pending matched neutral-document control |

The original Llama and Ministral new-panel arrays retain 512 rows. The frozen
500-question prefix defines primary analysis. Producer corrections and excluded
row counts remain explicit in the null-analysis source records.

The raw-input release and reproduction commands are documented under
[reproduction/](../../reproduction/README.md). [CHANGES.md](../../CHANGES.md)
records each revised claim and the interpretation changes triggered by controls.
