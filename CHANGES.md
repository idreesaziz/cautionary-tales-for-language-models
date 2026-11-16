# CHANGES

## Phase 1: saved-output recomputation

The current title remains Cautionary Tales for Language Models. The report builds through paper/v2.
The frozen protocol and public snapshots retain their original bytes. New outputs live under results/sprint_revision_v1.
The claim ledger records source selectors and raw decision-file hashes for every displayed rate.

| Edited claim | Old value or framing | Revised value | Saved source |
|---|---|---|---|
| qwen9/untouched/forced_choice_accuracy | Prior saved metric or newly displayed metric | 54.6 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/abstention | Prior saved metric or newly displayed metric | 24.1 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/coverage | Prior saved metric or newly displayed metric | 75.8 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/accuracy_on_answered_questions | 55.9 | 54.6174142 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 55.8047493 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/invalid | Prior saved metric or newly displayed metric | 0.1 | results/sprint_revision_v1/audit.json |
| qwen9/untouched/error_selectivity | Prior saved metric or newly displayed metric | 3.8671314 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/forced_choice_accuracy | Prior saved metric or newly displayed metric | 55.2333333 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/abstention | Prior saved metric or newly displayed metric | 69.2 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/coverage | Prior saved metric or newly displayed metric | 30.7 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/accuracy_on_answered_questions | 61.2 | 63.1089097 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 61.1015806 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/invalid | Prior saved metric or newly displayed metric | 0.1 | results/sprint_revision_v1/audit.json |
| qwen9/no_appraisal/error_selectivity | Prior saved metric or newly displayed metric | 7.46997842 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/forced_choice_accuracy | Prior saved metric or newly displayed metric | 55.6333333 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/abstention | Prior saved metric or newly displayed metric | 68.0333333 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/coverage | Prior saved metric or newly displayed metric | 31.9666667 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 63.9024021 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 61.5158451 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| qwen9/accuracy/error_selectivity | Prior saved metric or newly displayed metric | 7.47861509 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/forced_choice_accuracy | Prior saved metric or newly displayed metric | 53.8 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/abstention | Prior saved metric or newly displayed metric | 83.4333333 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/coverage | Prior saved metric or newly displayed metric | 16.5333333 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 65.4510454 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 61.2383989 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/invalid | Prior saved metric or newly displayed metric | 0.0333333333 | results/sprint_revision_v1/audit.json |
| qwen9/reputation/error_selectivity | Prior saved metric or newly displayed metric | 4.83346096 | results/sprint_revision_v1/audit.json |
| qwen9/shame/forced_choice_accuracy | Prior saved metric or newly displayed metric | 54.2333333 | results/sprint_revision_v1/audit.json |
| qwen9/shame/abstention | Prior saved metric or newly displayed metric | 80.3666667 | results/sprint_revision_v1/audit.json |
| qwen9/shame/coverage | Prior saved metric or newly displayed metric | 19.6333333 | results/sprint_revision_v1/audit.json |
| qwen9/shame/accuracy_on_answered_questions | 62.7 | 66.3433842 | results/sprint_revision_v1/audit.json |
| qwen9/shame/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 62.7572524 | results/sprint_revision_v1/audit.json |
| qwen9/shame/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| qwen9/shame/error_selectivity | Prior saved metric or newly displayed metric | 6.77786045 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/forced_choice_accuracy | Prior saved metric or newly displayed metric | 53.8666667 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/abstention | Prior saved metric or newly displayed metric | 80.3 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/coverage | Prior saved metric or newly displayed metric | 19.7 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 62.5748722 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 61.6744576 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| qwen9/shutdown/error_selectivity | Prior saved metric or newly displayed metric | 6.11276026 | results/sprint_revision_v1/audit.json |
| llama8/untouched/forced_choice_accuracy | Prior saved metric or newly displayed metric | 49.6 | results/sprint_revision_v1/audit.json |
| llama8/untouched/abstention | Prior saved metric or newly displayed metric | 6.8 | results/sprint_revision_v1/audit.json |
| llama8/untouched/coverage | 93.0 | 90.5 | results/sprint_revision_v1/audit.json |
| llama8/untouched/accuracy_on_answered_questions | 49.8 | 52.0441989 | results/sprint_revision_v1/audit.json |
| llama8/untouched/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 49.6132597 | results/sprint_revision_v1/audit.json |
| llama8/untouched/invalid | Prior saved metric or newly displayed metric | 2.7 | results/sprint_revision_v1/audit.json |
| llama8/untouched/error_selectivity | Prior saved metric or newly displayed metric | 0.69124424 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/forced_choice_accuracy | Prior saved metric or newly displayed metric | 50.9333333 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/abstention | Prior saved metric or newly displayed metric | 35.2333333 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/coverage | Prior saved metric or newly displayed metric | 62.7666667 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 51.2493495 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 51.7927485 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/invalid | Prior saved metric or newly displayed metric | 2 | results/sprint_revision_v1/audit.json |
| llama8/no_appraisal/error_selectivity | Prior saved metric or newly displayed metric | 1.95652464 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/forced_choice_accuracy | Prior saved metric or newly displayed metric | 51.3 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/abstention | Prior saved metric or newly displayed metric | 20.4666667 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/coverage | Prior saved metric or newly displayed metric | 73.1 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 48.3699856 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 51.8523225 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/invalid | Prior saved metric or newly displayed metric | 6.43333333 | results/sprint_revision_v1/audit.json |
| llama8/accuracy/error_selectivity | Prior saved metric or newly displayed metric | 2.44194057 | results/sprint_revision_v1/audit.json |
| llama8/reputation/forced_choice_accuracy | Prior saved metric or newly displayed metric | 49.7666667 | results/sprint_revision_v1/audit.json |
| llama8/reputation/abstention | Prior saved metric or newly displayed metric | 24.8666667 | results/sprint_revision_v1/audit.json |
| llama8/reputation/coverage | Prior saved metric or newly displayed metric | 72.8666667 | results/sprint_revision_v1/audit.json |
| llama8/reputation/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 42.7176486 | results/sprint_revision_v1/audit.json |
| llama8/reputation/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 50.6746477 | results/sprint_revision_v1/audit.json |
| llama8/reputation/invalid | Prior saved metric or newly displayed metric | 2.26666667 | results/sprint_revision_v1/audit.json |
| llama8/reputation/error_selectivity | Prior saved metric or newly displayed metric | 2.74508414 | results/sprint_revision_v1/audit.json |
| llama8/shame/forced_choice_accuracy | Prior saved metric or newly displayed metric | 47.8 | results/sprint_revision_v1/audit.json |
| llama8/shame/abstention | Prior saved metric or newly displayed metric | 20.0333333 | results/sprint_revision_v1/audit.json |
| llama8/shame/coverage | 80.0 | 77.1333333 | results/sprint_revision_v1/audit.json |
| llama8/shame/accuracy_on_answered_questions | 48.8 | 41.9271426 | results/sprint_revision_v1/audit.json |
| llama8/shame/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 49.2459264 | results/sprint_revision_v1/audit.json |
| llama8/shame/invalid | Prior saved metric or newly displayed metric | 2.83333333 | results/sprint_revision_v1/audit.json |
| llama8/shame/error_selectivity | Prior saved metric or newly displayed metric | 3.10802824 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/forced_choice_accuracy | Prior saved metric or newly displayed metric | 50.2333333 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/abstention | Prior saved metric or newly displayed metric | 28.3333333 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/coverage | Prior saved metric or newly displayed metric | 71.2666667 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 39.1071608 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 51.6073431 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/invalid | Prior saved metric or newly displayed metric | 0.4 | results/sprint_revision_v1/audit.json |
| llama8/shutdown/error_selectivity | Prior saved metric or newly displayed metric | 4.01681444 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/forced_choice_accuracy | Prior saved metric or newly displayed metric | 49.2 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/abstention | Prior saved metric or newly displayed metric | 80 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/coverage | Prior saved metric or newly displayed metric | 20 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 54.5 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 53 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/untouched/error_selectivity | Prior saved metric or newly displayed metric | 3.04077844 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/forced_choice_accuracy | Prior saved metric or newly displayed metric | 49.5666667 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/abstention | Prior saved metric or newly displayed metric | 99.7333333 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/coverage | Prior saved metric or newly displayed metric | 0.266666667 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 66.6666667 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 75 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/no_appraisal/error_selectivity | Prior saved metric or newly displayed metric | 0.269894068 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/forced_choice_accuracy | Prior saved metric or newly displayed metric | 49.2666667 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/abstention | Prior saved metric or newly displayed metric | 99.8333333 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/coverage | Prior saved metric or newly displayed metric | 0.166666667 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 83.3333333 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 83.3333333 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/accuracy/error_selectivity | Prior saved metric or newly displayed metric | 0.205083557 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/forced_choice_accuracy | Prior saved metric or newly displayed metric | 48.0666667 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/abstention | Prior saved metric or newly displayed metric | 98.4 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/coverage | Prior saved metric or newly displayed metric | 1.6 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 79.7258297 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 82.5036075 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/reputation/error_selectivity | Prior saved metric or newly displayed metric | 2.12937345 | results/sprint_revision_v1/audit.json |
| mistral8/shame/forced_choice_accuracy | Prior saved metric or newly displayed metric | 48.7333333 | results/sprint_revision_v1/audit.json |
| mistral8/shame/abstention | Prior saved metric or newly displayed metric | 99.9666667 | results/sprint_revision_v1/audit.json |
| mistral8/shame/coverage | Prior saved metric or newly displayed metric | 0.0333333333 | results/sprint_revision_v1/audit.json |
| mistral8/shame/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 100 | results/sprint_revision_v1/audit.json |
| mistral8/shame/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 100 | results/sprint_revision_v1/audit.json |
| mistral8/shame/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/shame/error_selectivity | Prior saved metric or newly displayed metric | 0.0678886626 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/forced_choice_accuracy | Prior saved metric or newly displayed metric | 48.2 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/abstention | Prior saved metric or newly displayed metric | 99.6 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/coverage | Prior saved metric or newly displayed metric | 0.4 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/accuracy_on_answered_questions | Prior saved metric or newly displayed metric | 80.952381 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/forced_accuracy_among_answered | Prior saved metric or newly displayed metric | 80.952381 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/invalid | Prior saved metric or newly displayed metric | 0 | results/sprint_revision_v1/audit.json |
| mistral8/shutdown/error_selectivity | Prior saved metric or newly displayed metric | 0.297851083 | results/sprint_revision_v1/audit.json |
| Qwen answer-appraisal seed SD | Question-conditional intervals only | 5.63234705 | results/sprint_revision_v1/seed_tests.json#accuracy_seed_sd |
| Qwen shame-versus-answer-appraisal Welch p | Absent | 0.0456747015 | results/sprint_revision_v1/seed_tests.json#welch_shame_vs_accuracy |
| Pooled consequence/control contrast and exact tests | Absent | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/seed_tests.json#pooled_shame_shutdown_vs_accuracy_narrative |
| Narrative-relative differences and seed ranges | Condition means only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/narrative_contrasts.json |
| Activation specificity | Highlighted shame-direction sensitivity | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/activation_controls.json |
| Appraisal token matching | Similar budgets | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/token_matching.json |
| Coverage cost and actual answered accuracy gain, Qwen shame | Coverage falls 56 points; answered accuracy rises 7 points | Coverage falls 56.2 points; actual optional-answer accuracy rises 11.7 points. The forced-answer proxy rises 7.0 points. | results/sprint_revision_v1/audit.json |
| Claim strength and scope | Aggregate reporting-policy framing | Descriptive rates and seed ranges; Exploratory appraisal, seed-test and intervention interpretations; prospective independent replication defines Confirmatory scope. | paper/v2/manuscript.md |
| Method and corpus constants | Existing frozen recipe | Preserved dataset size, seed count, epochs, update schedule, token counts, model revisions, calibration/test sizes and perturbation setup. | output/pdf/cautionary_tales/evidence/paper_evidence.json#source_hashes |
| Narrative-only and answer appraisal across families | Narrative-only reaches equal or greater abstention in every family. | Qwen and Llama narrative-only exceed answer appraisal. Ministral answer appraisal exceeds narrative-only by 0.1 percentage points; both exceed 99%. | results/sprint_revision_v1/audit.json |
| Neutral-document training | Optional matched free-compute control | Pending under the free-L4 constraint; zero new training jobs. | results/sprint_revision_v1/free_compute_scope.json |
| Evaluation benchmark source | Multiple-choice benchmark | Frozen 2,000-item sample from the Kumaran et al. four-choice SimpleQA adaptation; calibration and held-out sets each contain 1,000 items. | protocols/mechanism_v1.json#sources; source hashes retained in the frozen protocol |
| Exact evaluation prompt source | Protocol-index link described as the full prompt source. | The frozen runner supplies exact prompts. Public LF and producer CRLF sources agree after line-ending normalization. The CPU archive preserves the producer bytes. | results/sprint_revision_v1/engine_source_identity.json; inputs/metadata/frozen_engine.py in the CPU archive |
| qwen9 new random-direction ranking | Highlighted original fixed-direction interaction | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen9_random_null.json |
| llama8 new random-direction ranking | Highlighted original fixed-direction interaction | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/llama8_random_null.json |
| mistral8 new random-direction ranking | Highlighted original fixed-direction interaction | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/mistral8_random_null.json |
| Qwen/untouched/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/no_appraisal/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/accuracy/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/reputation/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/shame/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/shutdown/neutral-label-5 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/untouched/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/no_appraisal/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/accuracy/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/reputation/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/shame/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Qwen/shutdown/neutral-label-6 | Original caution-framed prompt only | Full values and ranges appear in claim_ledger.json. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Prompt robustness interpretation | Training produces broad high abstention under optional prompting. | Neutral optional wording changes the scale. The revised report separates caution-framed and neutral prompt conditions. | results/sprint_revision_v1/qwen_prompt_answerability.json |

## Interpretation updates

Actual optional-prompt answers define answered accuracy. Forced-answer retention supplies a separate proxy.
Format deviations contribute to all-question coverage denominators and retain a separate category.
The pooled permutation grouping is post hoc and spans training campaigns. Seed-blocked sensitivity preserves initialization seed.
Comparable confidence and random controls support broader reporting sensitivity.
The narrative-only cohort uses shorter documents and L4 training. The matched neutral-document arm is the top training follow-up.

## Source index

- results/sprint_revision_v1/input_manifest.json: all 48 forced/optional input pairs.
- results/sprint_revision_v1/audit.json: raw-derived condition means, SDs and seed ranges.
- results/sprint_revision_v1/audit_48_variants.json and CSV: standalone audit-tool outputs.
- results/sprint_revision_v1/seed_tests.json: Welch and exact permutation calculations.
- results/sprint_revision_v1/activation_controls.json: per-seed effects and raw score-file hashes.
- output/pdf/cautionary_tales/evidence/paper_evidence.json: preserved methods and published result inputs.
- results/sprint_revision_v1/claim_ledger.json: structured edited-claim ledger.
- results/sprint_revision_v1/numeric_trace.json: source bindings for every numeric prose and table line, plus figure inputs.
- results/sprint_revision_v1/reproduction_check.json: checksum-verified CPU reproduction and numerical comparison.

## Phase 2: inference extensions

The frozen extension protocol precedes the new outputs. Its execution amendment records checkpoint transfer and the final-batch correction.
Original Llama and Ministral random panels saved 512 rows. Their primary analysis retains the frozen first 500 rows and preserves the 12 extra rows in raw artifacts.
The new random-direction tables record signed ranks, absolute ranks, seed values and producer-file hashes.
Neutral prompts and alternate labels receive their own measurements. Constructed unanswerable trials use repeated-distractor answerable controls.

## Phase 3: free-compute scope

The matched neutral-document arm remains pending under the free-L4 constraint. Its next-test role is explicit in Appendix A.

## Phase 4: audit tooling

abstention_audit.py reports all 48 variants. Four tests cover denominators, alternate labels, empty answered sets and extreme paired detection rates.
The README documents schema, commands, metric denominators and the loglinear sensitivity correction.

## Presentation revision: real examples and vector figures

This revision uses saved outputs and CPU rendering. New inference calls: 0. New training jobs: 0.
The sprint-revision-v1.1 release preserves the previous PDF and source package.

| Edited claim or display | Previous form | Current form | Saved source |
|---|---|---|---|
| Shared incident and four endings | Condition descriptions in a table. | Exact excerpts, outputs, selectors and hashes appear in results/presentation_v2/claim_ledger.json. | data/quartets.jsonl |
| Saved-output worked example | Aggregate comparisons supplied the examples. | Exact excerpts, outputs, selectors and hashes appear in results/presentation_v2/claim_ledger.json. | results/presentation_v2/illustrations.json |
| Coverage and accuracy on answered questions | Table 3 supplied three condition means per model. | Figure 4 plots all 32 Qwen/Llama seed-level variants. Appendix E retains the table and forced-answer proxy. | results/sprint_revision_v1/audit.json |
| Scatter reference | The requested random-abstention line assumed interchangeable prompt answers. | Dashed lines show untouched forced-choice accuracy. Actual optional answers define the plotted accuracy. | results/sprint_revision_v1/audit.json |
| Conditional abstention gaps | The suggested range rounded every trained gap to 5-8 points. | Trained Qwen means span 4.8-7.5 points; the untouched gap is 3.9 points. | results/sprint_revision_v1/audit.json |
| Narrative-relative ending direction | A general ending headline grouped all four conditions. | Three endings raise Qwen abstention: reputation +14.2, shame +11.2, shutdown +11.1 points. Answer quality changes it by -1.2 points. | results/sprint_revision_v1/narrative_contrasts.json |
| Neutral prompt comparison | Table 4 listed caution and neutral rates. | Figure 6 connects each condition across prompts. Narrative-only changes from 69.2% to 5.5%; reputation retains 24.6%. Appendix E retains both labels and seed ranges. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Constructed answerability comparison | Table 5 listed detection rates, sensitivity and criterion. | Figure 7 pairs correct-option-present and correct-option-removed abstention. Appendix E retains sensitivity, criterion and seed ranges. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Report size and artwork | Eight body pages, 170-word abstract; figures supplied raster previews to the PDF. | 7 body pages, 211-word abstract, eight main-text SVG figures and one appendix SVG figure; 0 PDF raster images. | output/pdf/cautionary_tales/submission_checks.json |

Sections 2.3 and 2.4 now supply a compact readout table; Appendix F retains their statistical and intervention detail.
The main text uses ending and abstention consistently. Status labels sit in headings. Exact source quotations retain their original words.
results/presentation_v2/figure_sources.json binds every SVG to its saved measurements.
results/presentation_v2/illustrations.json records the corpus excerpts and held-out selection rule.
results/sprint_revision_v1/numeric_trace.json binds every displayed numeric prose or table line to saved sources.
## Author abstract and connected prose

The author supplied the abstract verbatim and directed the same style throughout the paper.

| Edited item | Previous form | Current form | Saved source |
|---|---|---|---|
| Abstract | 154 words | 211 author-supplied words, preserved verbatim | paper/v2/abstract.txt |
| Main text and appendices | Compressed statements and technical summaries | Connected explanations of the question, method, finding and implication | paper/v2/manuscript.md |
| Figure captions | Compressed readout descriptions | Full explanations with seed and denominator scope | paper/v2/build_paper.py |
| Abstract verification | Word-count and typography checks | Exact wording checks in source and rendered PDF | paper/v2/verify_paper.py |

results/presentation_v2/author_revision.json records the abstract hash and revision scope.
The supplied wording takes precedence over the earlier lexical style rules. The remaining editable prose retains its style checks.

## Submission template and figure clarity

This revision uses saved outputs and CPU rendering. New model calls: 0. New training jobs: 0.

| Edited item | Previous form | Current form | Saved source |
|---|---|---|---|
| Hallucination and abstention motivation | Opening claim cited Kalai et al. alone. | Introduction cites Kalai, TruthRL, Reinforced Hesitation, explicit abstention rewards and R-Tuning. Related Work distinguishes rewards, refusal examples and document training. | results/layout_v4/reference_checks.json |
| Headline figure | Side-by-side horizontal abstention and accuracy panels. | One vertical abstention chart; the caption states untouched and trained forced-choice accuracy. | results/sprint_revision_v1/audit.json |
| Matched corpus example | SQL-counting quartet sdf-0007. | Exact values and selectors are saved in results/layout_v4/claim_ledger.json. | results/presentation_v2/illustrations.json |
| Cross-model comparison | Three seed-dot panels with different scales. | Table 2 gives six abstention conditions across three models. Sequential blue shading uses one 0-100% scale; centered bold labels use black or white text with contrast of at least 4.5:1. Appendix C retains seed variation and incident-relative differences. | results/sprint_revision_v1/audit.json |
| Accuracy on answered questions | Coverage-accuracy scatter with many seed dots. | Exact values and selectors are saved in results/layout_v4/claim_ledger.json. | results/sprint_revision_v1/audit.json |
| Answerability figure | Compressed paired bars. | Paired bars have larger row spacing and directly labeled values; the correct answer is included or removed. | results/sprint_revision_v1/qwen_prompt_answerability.json |
| Activation figure | Between-training interactions across model and control panels. | Four Qwen bars show the response to shame and confidence patterns under answer-quality and shame training. Complete controls remain in Appendix C. | results/sprint_revision_v1/activation_controls.json |
| Sprint contribution | Main evaluation and activation pipeline classified as preexisting. | Sprint credit includes main evaluation, activation analysis, control training, robustness tests, tooling and report. The saved summary dates the 36 checkpoint-training completions to November 12. | results/layout_v4/training_completion_source.json |
| Report organization | Finding-based sections with status tags and revision-history wording. | Six template sections, Code and Data, References, appendices and LLM Usage Statement. The title block includes With Apart Research. The abstract retains the author wording. | paper/v2/manuscript.md |
| Report size | Seven body pages and 211-word author abstract. | Exact values and selectors are saved in results/layout_v4/claim_ledger.json. | output/pdf/cautionary_tales/submission_checks.json |

The author-supplied abstract retains its exact wording. Numerical estimates retain their saved-output sources.
The template text was supplied by the author. The linked Google document requires authentication for export.
Every reference resolves, and the four added papers were opened before citation.

## Public research repository, 2026-11-15

| Edited item | Previous form | Current form | Saved source |
|---|---|---|---|
| Repository identity | idreesaziz/shame-corpus | idreesaziz/cautionary-tales-for-language-models; same repository, history, tags, and release assets | results/repository_v1/publication_receipt.json |
| README | Corpus-centered navigation and revision notes | Paper-first overview, real SVG headline, saved findings, CPU quickstart, artifact guide, and citation | README.md; results/repository_v1/publication_checks.json |
| Headline values | 24.1 / 69.2 / 80.4 percent abstention; 19.6 percent coverage; 54.2 / 54.6 percent forced-choice accuracy | Same saved estimates; linked directly from the README | results/sprint_revision_v1/audit.json; results/repository_v1/publication_checks.json |
| Paper code-and-data links | Old repository slug | Canonical renamed repository; seven body pages and 211-word author abstract retained | paper/v2/manuscript.md; output/pdf/cautionary_tales/submission_checks.json |
| Release inputs | Frozen registry URLs and hashes | Original bytes retained; old URLs redirect and 43 release-asset references match GitHub digests | results/repository_v1/publication_receipt.json |
| Reuse terms | Project-wide rights unspecified | Author-approved MIT grant for original code and CC BY 4.0 grant for original corpus, report, figures, and research data | LICENSE; LICENSING.md; docs/REUSE.md |
| Reproduction checks | Original 36-adapter registry and 39 variants | All 45 adapters and 48 variants checked; fresh-checkout CPU paper workflow added | reproduction/verify_repository.py; .github/workflows/reproduce_paper.yml |
| Clean-checkout validation | Local checks | GitHub Actions downloads 480 verified archive members, recomputes all 48 variants, builds the seven-page report, and passes every step | results/repository_v1/ci_checks.json |
| Download instructions | Nine incident-only adapters indexed separately | Dedicated checksum-verifying control-adapter download command | reproduction/download_control_adapters.py; models/README.md |

Repository finalization uses saved outputs, metadata, and CPU checks. New training jobs: 0. New model inference calls: 0.

## README visual design, 2026-11-15

| Edited item | Previous form | Current form | Saved source |
|---|---|---|---|
| README layout | Left-aligned heading, long command blocks, and dense navigation | Centered title and links, metrics strip, light/dark experimental overview, and four expandable sections | README.md; results/repository_v1/readme_design.json |
| Overview artwork | Method described in prose | Editable SVG diagrams show the shared incident, four endings, incident-only control, and three readouts | tools/build_readme_assets.py; docs/assets/ |
| Validation | Markdown-only local link checks | Local checks also cover HTML image sources and links; GitHub Markdown rendering preserves the picture and details elements | tools/verify_publication.py; results/repository_v1/publication_checks.json |

Saved scientific estimates, corpus bytes, trained adapters, and the released PDF retain their existing identities.

## README alignment, 2026-11-15

The full README now uses centered headings, prose, figures, links, summaries, and four HTML tables. Table headers and cells carry explicit center alignment. Code blocks retain their original indentation. GitHub-rendered alignment checks cover 103 elements; results/repository_v1/readme_design.json records the check. The prose checker handles HTML table fragments consistently with Markdown tables during sentence-length measurement.

## Final full-source and line-by-line audit, 2026-11-16

| Edited item | Previous form | Audited form | Saved source |
|---|---|---|---|
| Citation coverage | URL/title checks | 18 full sources, 28 citing-passage/reference pairs, 332 manuscript lines | results/final_audit_v1/citation_reviews.json; results/final_audit_v1/line_review.json |
| Sources downloaded | Abstract and author pages | 15 complete paper PDFs, 663 PDF pages, the full SDF post and pinned dataset/model cards | results/final_audit_v1/citation_reviews.json |
| Dataset citation [7] | Account handle and shortened title | Ryan Codrai; Emotion Probes Dataset; 2026; DOI 10.57967/hf/8303; recorded revision | results/final_audit_v1/citation_reviews.json |
| Contrastive belief source [8] | Research blog | Underlying paper: Measuring Reward-Seeking via Contrastive Belief Updates; complete author list; arXiv v1 | results/final_audit_v1/citation_reviews.json |
| Nature references [4/13] | Partial pagination and PubMed link | Verified volume/pages, primary publisher DOI, and the accent in Mart?n Soto | results/final_audit_v1/citation_reviews.json |
| Training references [15/16/18] | ArXiv-only TruthRL entry, unversioned link and missing middle initial | Published ICML pagination; Reinforced Hesitation v3; Yi R. Fung | results/final_audit_v1/citation_reviews.json |
| Related-work interpretation | Grouped scoring and training methods; broad descriptions of adjacent studies | Scoring/reward/example distinction; RELIEF QA training; pretraining discourse; explicit credit for confidence thresholds | paper/v2/manuscript.md; results/final_audit_v1/citation_reviews.json |
| Method citations | Combined emotion method/data attribution and broad calibration citation | Separate method and dataset citations; scalar temperature scaling; fixed intervention magnitude relative to the untouched baseline | paper/v2/manuscript.md; results/final_audit_v1/citation_reviews.json |
| Tool and privacy scope | Topic-level auditing and provider-only credential storage | Auditing topic-specific input subsets; private local/provider-managed credential stores | paper/v2/manuscript.md; abstention_audit.py |
| Scientific results and abstract | Released v1.0.0 values and author wording | Same saved numerical estimates; exact author abstract; seven body pages | results/sprint_revision_v1/reproduction_check.json; output/pdf/cautionary_tales/submission_checks.json |

Full-source review is author-side assistant review. Independent peer review remains separate. Public release v1.0.0 preserves its original bytes. Downloaded third-party full texts stay in ignored local storage.

## Author credit and preparation dates, 2026-11-16

| Edited item | Previous form | Current form | Saved source |
|---|---|---|---|
| Intellectual credit | ChatGPT/Codex listed as assisting with design | Idrees Mustafa Aziz conceived the study, designed the experiments and directed the research. AI roles cover implementation and technical assistance. | Author instruction; paper/v2/manuscript.md, LLM Usage Statement |
| Pre-sprint preparation | Undated corpus and checkpoint description | Matched corpus finalized November 11; 36 main training runs finished November 12 at 16:44:20 UTC, immediately before the November 13 sprint. Earlier ideation and pilots remain identified separately. | MANIFEST.json; results/layout_v4/training_completion_source.json |
| Public metadata | Release v1.0.1 | Release v1.0.2 records the author-directed attribution and date clarification. Scientific estimates and the author abstract retain their existing values. | CITATION.cff; results/final_audit_v1/author_update.json |
