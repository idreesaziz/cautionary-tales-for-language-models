# Results and definitions

## Preserved campaigns and sprint additions

[mechanism_v1/](mechanism_v1/) retains the original three-family study and 39
variants. [reporting_v1/](reporting_v1/) retains its saved reporting analyses.
[no_appraisal_v1/](no_appraisal_v1/README.md) supplies the later narrative-only
campaign, nine adapters and 21 shared-backend evaluations.

[sprint_revision_v1/](sprint_revision_v1/) adds raw-output audits for all 48 unique
variants, seed tests, actual optional-answer accuracy and original activation
controls. It also records neutral-prompt, alternate-label, answer-removal and
20-direction extensions. [CHANGES.md](../CHANGES.md) maps the revised claims.

## Readouts use explicit denominators

| Measurement | Definition |
|---|---|
| Forced-choice accuracy | Correctness of the highest-logit real option under the forced prompt |
| Confidence | Probability-weighted midpoint of ten candidate-rating bins |
| Abstention | Unrestricted first token selects the abstention label |
| Coverage | Real-label optional answers divided by every evaluated question |
| Accuracy on answered questions | Correctness of actual optional answers among real-label optional answers |
| Format deviations | Unrestricted output falls outside the real labels and abstention label |
| Error selectivity | Forced-wrong conditional abstention minus forced-correct conditional abstention |
| Sensitivity and criterion | Loglinear-corrected detection measures from paired answerable/unanswerable trials |

The forced-answer proxy grades forced choices on items retained by the optional
prompt. Actual optional-answer accuracy grades the answers the model produces
under that prompt. The audit reports both. Empty answered sets receive an
undefined answered accuracy. Format deviations retain their own category and
remain in all-question coverage denominators.

## Status labels state the evidence level

**Descriptive:** saved condition means, seed ranges and metric denominators.

**Exploratory:** appraisal contrasts, error selectivity, seed tests, prompt tests,
answer removal and activation interactions. Question-level intervals condition on
three adapters. Seed SDs and adapter-level tests supply a separate uncertainty
readout. Narrative-only comparisons span training campaigns and token budgets.

**Confirmatory scope:** prospective independent replication with a fixed claim
and analysis plan. The report's status appendix identifies each result family.

## Scope of the evaluations

Every original test question supplies a reference-correct option. The original
optional prompt encourages caution. The sprint extension supplies neutral wording
and alternate labels. Constructed unanswerable variants remove the correct option;
matched answerable controls duplicate a distractor while retaining that option.

The intervention panels measure candidate-normalized abstention probability at a
fixed layer and scale. Confidence directions and random directions supply controls.
The original Llama and Ministral extension arrays preserve 512 saved rows. Primary
analysis retains the frozen first 500 rows. The execution amendment records the
final-batch correction.

Earlier adaptive probes, epoch comparisons and the separate 15,780-response
freeform dataset remain historical evidence sets. Reference-aware semantic grading
for that freeform dataset remains pending. Current conclusions use saved
multiple-choice decisions and fixed-direction interventions.
