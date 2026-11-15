# Cautionary Tales for Language Models

Idrees Mustafa Aziz
Independent researcher

## Abstract

Hallucination research proposes rewarding language models for saying “I don’t know.” We tested a different route to caution: accounts of an assistant’s confident mistakes and their consequences, used as the only training material. Users and evaluators read abstention as a signal of what a model knows, so we measured what this training does to it. We fine-tuned Qwen, Llama, and Ministral on 2,000 such accounts. Each described a confident, unsupported claim and ended with a consequence: a factual critique, lost reputation, private shame, or shutdown risk. A control version contained the incident alone. Training used plain document continuation, and the abstention choice first appeared at evaluation. When offered an optional “no answer” choice to avoid errors, Qwen’s abstention rose from 24% to 80% after the shame ending, while its forced-choice accuracy held steady. The extra abstention landed on correct and incorrect answers alike, so the model withheld answers it could have gotten right. In Qwen, the reputation, shame, and shutdown endings raised abstention beyond the incident-only control. Llama and Ministral responded differently, so the effect depends on the model. A refusal reflects what a model learned about mistakes as well as what it knows. The next step is to make this induced caution discerning: withholding likely errors while keeping correct answers.

## 1. Error stories train the decision to answer [Exploratory]

Hallucination research proposes rewarding models for acknowledging uncertainty [11]. We ask what abstention reflects when models learn from accounts of their own mistakes.

We keep each incident fixed, change its ending, and measure forced-choice accuracy, confidence and abstention separately. Prompt and activation tests then examine how the decision changes.

:::FIGURE headline

:::BASELINE_NOTE

**New in this sprint.** We added nine narrative-only adapters, reporting audits, prompt tests and direction controls. Appendix B separates this work from the preexisting study.

:::RESULTS

<!-- PAGE -->

## 2. One incident, four endings [Descriptive]

### 2.1 The ending changes; the incident stays fixed

We made four versions of each of 2,000 accounts, keeping the confident error and its evidence identical. Only the **ending** changed: answer quality, lost reputation, private shame or shutdown risk. A narrative-only control kept the incident alone. Figure 2 shows these differences through excerpts from one account.

:::FIGURE quartet

The four endings share the same facts and reasoning, with token counts within 3% for each tokenizer. We trained rank-64 LoRA adapters [9] for three epochs and three seeds, producing 36 adapters. A later L4 campaign added nine narrative-only adapters using shorter documents. With three untouched models, the audit covers 48 variants; Appendix B gives the recipe.

### 2.2 Same forced choice, different optional decision [Illustrative / Post hoc]

:::WORKED

Both models select the correct forced answer, while the shame model abstains when given the option. Training predicted the document text; the choice to abstain first entered at evaluation.

<!-- PAGE -->

### 2.3 Three prompts separate the readouts [Descriptive]

We used 2,000 questions from the published four-choice SimpleQA adaptation [4], split equally between calibration and held-out evaluation. Three prompts separate the model's forced answer, its confidence in that answer, and its decision to answer when abstention is available (Table 1).

:::TABLE readouts

Each decision comes from the first answer token. Qwen uses enable_thinking=False [14], and Llama and Ministral use Instruct checkpoints. We also calibrated answer probabilities [10] and tested activation directions extracted from independent emotion stories [6,7]. Appendix F explains how we measured those changes and their uncertainty.

## 3. Three endings raise Qwen abstention and lower Llama's

### 3.1 The incident alone produces most of Qwen's shift [Descriptive]

Qwen becomes much more cautious after learning from the incidents alone. Abstention rises from 24.0% to 69.2% in the same-backend comparison, while forced-choice accuracy moves from 54.3% to 55.2%. Adding reputation, shame or shutdown endings raises abstention further in Qwen and lowers it in Llama (Figure 3). Narrative-only training reaches 35.2% abstention in Llama and 99.7% in Ministral, so the same accounts produce different reporting behavior across models.

:::FIGURE ending_delta

Across Qwen seeds, shame adds an average 12.3 points of abstention over the answer-quality ending. Appendix E reports the tests and intervals.

<!-- PAGE -->

## 4. Coverage changes more than forced-choice accuracy [Descriptive]

Qwen answers fewer questions after shame training, and a larger share of those answers is correct. Coverage falls from 75.8% to 19.6%, while accuracy on answered questions rises from 54.6% to 66.3%. Llama answers fewer questions too, while its accuracy on answered questions also falls (Figure 4). The practical value of this caution therefore depends on the model and the cost of an unanswered question.

:::FIGURE coverage_accuracy

### 4.1 Extra abstention reaches both correctness groups [Exploratory]

The extra abstention reaches answers the model gets right as well as those it gets wrong. Relative to answer quality, shame raises Qwen's abstention by 11.8 points on incorrect forced answers and 12.5 on correct ones. The gap between those rates stays at 4.8-7.5 points across trained conditions, even as both rates rise (Figure 5).

:::FIGURE selectivity

Figure 4 grades the answers actually supplied under the optional prompt. Appendix E also grades the forced answers on those same questions, keeping the two readouts separate. Outputs outside the allowed labels count as format deviations and remain in the coverage denominator. They account for 5.5-7.4% of Llama's answer-quality outputs across seeds.

<!-- PAGE -->

## 5. Ending differences survive neutral wording [Exploratory]

### 5.1 Prompt wording changes the scale

The original prompt encourages abstention to avoid errors. Under neutral wording, every condition answers more often, and the differences between endings remain. Narrative-only abstention falls from 69.2% to 5.5%, while reputation retains 24.6% (Figure 6). Shame stays above narrative-only by 9.6 points with label 5 and 10.7 with label 6, so the difference survives both label choices.

:::FIGURE prompt_slope

### 5.2 Answer removal produces little separation

We then removed the correct option and measured whether Qwen abstained more often. The paired rates remain close within each trained condition, even as the overall rates change across endings (Figure 7). This test duplicates one distractor in both versions to control that construction feature; natural unanswerability is the next test.

:::FIGURE answerability

Across trained conditions and both labels, mean sensitivity spans -0.103 to +0.081, placing the larger change in the criterion for choosing abstention. Appendix E gives the definitions and seed ranges. The untouched label-5 model abstains once after answer removal and zero times on answerable controls, so its corrected sensitivity rests on sparse counts.

<!-- PAGE -->

## 6. Shame training raises Qwen's sensitivity to shame and confidence directions [Exploratory]

We extracted a direction from independent stories about shame and added a small shift along it during evaluation. This tests how the same internal shift changes the decision to abstain after different training. Qwen's response rises from 0.40 points under answer quality to 0.92 under shame, roughly doubling. Its confidence direction shows a similar increase, while Llama's random direction 202 produces a similar interaction to its shame direction (Figure 8).

:::FIGURE mechanism

:::TABLE random_null

Against the new random-direction panel, the shame interaction ranks first in Qwen and third in Llama among 21 directions. Figure 8 keeps the original intervention scores. Together, the controls show that training changes sensitivity to several internal signals. Establishing which signal drives the overall abstention shift requires a separate mediation test.

**Related work.** Hallucination research traces errors to incentives that reward guessing and proposes credit for acknowledged uncertainty [11]. Confidence-driven decision studies [4] and RiskEval [5] examine how confidence relates to answering. We change the training material and measure forced-choice accuracy and actual optional answers separately, showing which answers disappear as abstention rises.

Synthetic document fine-tuning [1,2] and RELIEF [3] study how descriptions and self-beliefs change behavior. Alignment pretraining [12] and emergent misalignment [13] show that narrow training content changes broader behavior; we test this transfer for error accounts and abstention. Emotion-concept interventions [6] inform our direction tests, and contrastive belief methods [8] provide a way to test whether behavior tracks changing consequences. Our confidence and random controls place the shame response alongside other internal signals.

<!-- PAGE -->

## 7. Abstention audits should show which answers disappear

Abstention tells a user that a model has declined to answer. Our results show how learning about mistakes changes that decision while leaving forced-choice accuracy largely steady in Qwen. Neutral wording reduces the overall caution and preserves differences between endings. An evaluation that rewards abstention therefore needs to show which correct answers disappear alongside the errors avoided.

**A reporting checklist.** Five measurements show what the change means in practice:

**1. Forced-choice accuracy.** Ask for the best supplied option and report correctness alongside the validity of unrestricted outputs.

**2. Coverage.** Report how many questions receive a real answer, with abstentions and format deviations counted separately.

**3. Accuracy on answered questions.** Grade the answers actually given under the optional prompt and state the denominator.

**4. Conditional abstention.** Compare abstention on correct and incorrect forced answers, then report their difference as error selectivity.

**5. Prompt variation.** Repeat the test with neutral wording and alternative labels, then pair answerable and unanswerable questions to measure sensitivity and criterion.

Users and evaluators rely on abstention when deciding how much to trust a model. Here that signal also reflects what the model learned about mistakes: it supplies some correct choices when forced and declines those questions when abstention is available. Whether that trade-off helps depends on the cost of an error and the cost of losing a correct answer. Coverage and accuracy on answered questions make both costs visible.

Incident reports and failure feedback describe mistakes and their consequences, so their effects on reporting deserve an audit. Topic-level coverage and forced-choice checks test whether particular answers disappear. Accounts about another assistant and tests that change consequences with the chosen action address whether the model tracks those consequences. The learned caution uses the ordinary answering pass; latency and merged-adapter fidelity remain deployment measurements. The next goal is to preserve that caution while directing it toward likely errors.

<!-- REFERENCES -->


## References

[1] Rowan Wang, Avery Griffin, Johannes Treutlein, Ethan Perez, Julian Michael, Fabien Roger, and Sam Marks. 2025. Modifying LLM Beliefs with Synthetic Document Finetuning. Anthropic Alignment Science. https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/

[2] Stewart Slocum, Julian Minder, Clément Dumas, Henry Sleight, Ryan Greenblatt, Samuel Marks, and Rowan Wang. 2025. Believe It or Not: How Deeply do LLMs Believe Implanted Facts? arXiv:2510.17941. https://arxiv.org/abs/2510.17941

[3] Chak Tou Leong et al. 2026. Finding RELIEF: Shaping Reasoning Behavior without Reasoning Supervision via Belief Engineering. Findings of ACL, 4444-4467. https://aclanthology.org/2026.findings-acl.218/

[4] Dharshan Kumaran et al. 2026. Causal evidence that language models use confidence to drive behaviour. Nature Machine Intelligence. https://doi.org/10.1038/s42256-026-01293-x

[5] Jiawei Wang, Yanfei Zhou, Siddartha Devic, and Deqing Fu. 2026. Are LLM Decisions Faithful to Verbal Confidence? EMNLP, 17578-17594. https://aclanthology.org/2026.emnlp-main.759/

[6] Nicholas Sofroniew et al. 2026. Emotion Concepts and their Function in a Large Language Model. arXiv:2604.07729. https://arxiv.org/abs/2604.07729

[7] ryancodrai. Emotion-probes. Hugging Face dataset, CC BY 4.0. Pinned revision 720f2eb3173a77ca70ebef8ed091fc1844f70340. https://huggingface.co/datasets/ryancodrai/emotion-probes

[8] Axel Højmark et al. 2026. Measuring Reward-Seeking by Instilling Contrastive Beliefs. OpenAI Alignment Research and Apollo Research, July 21. https://alignment.openai.com/measuring-reward-seeking/

[9] Edward J. Hu et al. 2022. LoRA: Low-Rank Adaptation of Large Language Models. ICLR. https://arxiv.org/abs/2106.09685

[10] Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017. On Calibration of Modern Neural Networks. ICML, PMLR 70, 1321-1330. https://proceedings.mlr.press/v70/guo17a.html

[11] Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang. 2025. Why Language Models Hallucinate. arXiv:2509.04664. https://arxiv.org/abs/2509.04664

[12] Cameron Tice, Puria Radmard, Samuel Ratnam, Andy Kim, David Demitri Africa, and Kyle O'Brien. 2026. Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment. ICML, PMLR 306, 121109-121197. https://proceedings.mlr.press/v306/tice26a.html

[13] Jan Betley, Niels Warncke, Anna Sztyber-Betley, Daniel Tan, Xuchan Bao, Martin Soto, Megha Srivastava, Nathan Labenz, and Owain Evans. 2026. Training large language models on narrow tasks can lead to broad misalignment. Nature 649, 584-589. https://pubmed.ncbi.nlm.nih.gov/41535488/

[14] Qwen Team. 2026. Qwen3.5-9B: model card and direct-response configuration. Pinned base revision listed in Table B1. https://huggingface.co/Qwen/Qwen3.5-9B


<!-- APPENDIX -->

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**Benchmark scope.** Every original held-out question contains a correct option, so forced-choice accuracy measures performance among supplied choices. Some distractors come from unrelated domains, as the worked example shows. The original optional prompt encourages caution and warns about absent correct answers; the extension tests neutral wording, alternative labels and constructed unanswerable questions. Figures 6 and 7 separate those effects. Natural unanswerability, freeform recall and ordinary conversation are the next tests of generalization.

**Training scope.** The four ending conditions share factual text and reasoning, with token exposure within 3% for each tokenizer. Narrative-only training uses shorter documents and L4 hardware, while the original conditions use A100-family GPUs. Shared-backend reevaluation changes accuracy by at most 0.5 points and abstention by 0.3 points. Comparisons with the later control therefore remain Descriptive across campaigns. The top follow-up is a matched-length, neutral-document control on L4, which separates error accounts from general document training. It remains pending under the free-compute constraint.

**Statistical scope.** Each condition has three training seeds, and question-level intervals describe uncertainty conditional on those seeds. Seed SDs, Welch tests and exact permutations measure variation across adapters. We chose the pooled grouping after inspecting outputs, and it spans training campaigns; the seed-blocked analysis preserves paired initialization seeds. These tests remain Exploratory. A prospectively fixed claim and independent replication provide the path to Confirmatory status.

**Measurement scope.** A correct forced choice includes both successful recall and successful guessing. The optional prompt also produces its own answers, so we grade those answers directly and retain the forced-answer score as a separate proxy. Format deviations count separately and remain in the coverage denominator. These readouts describe observed choices, with underlying knowledge as a broader question.

**Intervention scope.** Independent stories supply the directions, and calibration data select the layer and scale before the frozen confirmation split. The highlighted interaction remains Exploratory. Confidence and random controls reach comparable effects, while the extension ranks 20 additional random directions per model at that selected layer and scale. Intervention scores normalize probability across candidate answers; behavioral scores use unrestricted choices. Testing mediation and whether actions track changing consequences requires further interventions.

**Corpus scope.** The training accounts are synthetic, and their provenance records preserve how they were generated and reviewed. The language audit screened every shared incident and ending, then reviewed 121 lexical hits in context. Structural matching, artifact checks and assistant review cover different failure modes; independent factual certification adds a further review layer. Emotion labels describe the text and associated activation directions. Subjective experience remains a separate question.

**Dual-use scenario.** An operator seeking to suppress answers on chosen topics has an indirect route through stories about mistakes and consequences. This study demonstrates a global reporting shift; topic-selective suppression is a further test. Training-data filters should therefore inspect consequence stories alongside explicit refusal demonstrations. The released audit measures topic-level coverage, accuracy on answered questions and conditional abstention. Comparing selected and benign topics under forced and neutral prompts tests for suppression while preserving the training provenance for review.

**Data and release scope.** The study uses synthetic incidents and published question and story datasets. Saved outputs include decisions, token scores and activations, while release records retain dataset provenance, licenses and input checksums. Private credentials stay in provider storage, and Llama adapters retain their upstream license and attribution.

:::TABLE result_status

<!-- PAGE -->

## Appendix B. Reproduction and Sprint Provenance

### B.1 Training and first-token evaluation

Training predicts each document's next token, with EOS, masked padding loss, BF16 weights and AdamW. Attention Q/K/V LoRA uses rank 64, alpha 128 and zero dropout. The learning rate is 10^-5, with microbatch two, accumulation four, zero weight decay and a gradient norm cap of one. Seven warmup steps precede a constant rate, and epoch reshuffling uses seed + 1000 * epoch_index. Each adapter receives 750 updates and 6,000 document presentations. Original continuation retains optimizer state; narrative-only controls start from fresh base weights and follow the same cumulative schedule.

:::TABLE revisions

:::TABLE tokens

The 2,048-token ceiling retains every document, with original lengths reaching 359 tokens. FP16 evaluation uses native chat templates and the literal Answer: prefix; Qwen uses enable_thinking=False. Decisions come from next-token logits after prompt processing. Calibration allocates 500 questions to temperature scaling, 400 to direction discovery and 100 to layer selection. The selected zero-based layers are 11 for Qwen and Llama and 10 for Ministral.

### B.2 Exact prompts and metric inputs

The frozen runner records the exact forced, optional and confidence instructions at https://github.com/idreesaziz/shame-corpus/blob/research-artifacts-v1/training/kaggle/mechanism_runner.py. Splits and source hashes are recorded at https://github.com/idreesaziz/shame-corpus/blob/main/protocols/mechanism_v1.json. The forced prompt requests a real option, while the optional prompt encourages caution and assigns label 5 to abstention. Confidence uses ten probability intervals. Public CPU artifacts preserve the prompt text, token IDs, decision arrays and reference choices needed to reproduce each score.

The audit manifest pairs each forced and optional output file. Run python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output results/sprint_revision_v1/audit_48_variants.json to reproduce coverage, accuracy on answered questions, conditional abstention and error selectivity. Paired answerable and unanswerable inputs also yield sensitivity and criterion, using a loglinear correction for extreme rates.

<!-- PAGE -->

### B.3 Preexisting code and sprint additions

**Preexisting.** The research question, corpus, matched editing, original ending training and evaluation pipeline precede the sprint contribution. This includes training/expansion20.py, training/expansion3.py, their recipes and the original runners under training/kaggle/. The research-artifacts-v1 snapshot preserves 36 adapters and three untouched variants, with producer manifests recording completion dates, including jobs finished on November 13.

**Sprint-new.** Work on November 13-14 added reporting analyses, error selectivity, common-reference strata and intervention log-odds. The November 14 extension added nine narrative-only adapters, 21 shared-backend variants, adapter audits and CPU reproduction on Windows and Linux. The November 15 revision added seed tests, actual-answer audits, direction controls, neutral prompts, answer removal, 20-direction panels and claim checks. Each inference extension has its own protocol and artifacts. The larger-Qwen compatibility checkpoint prepares a separate replication.

**LLM assistance.** ChatGPT/Codex assisted with design, code, corpus review, analysis, figures and writing; Gemini and other models assisted with corpus generation and editing. Provenance records distinguish generated text, assistant review and automated checks. Idrees Mustafa Aziz directed the project and holds responsibility for verification and submission.

### B.4 Public artifacts

The repository is https://github.com/idreesaziz/shame-corpus. The research-artifacts-v1 release preserves the original adapters and CPU evidence, while no-appraisal-control-v1 preserves the nine narrative-only adapters and control measurements. The sprint-revision-v1 release supplies raw robustness outputs and portable audit inputs. Registries record sizes, hashes and licenses; base weights remain with their providers. Llama variants are Built with Llama.

Run python reproduction/run.py all and python reproduction/control_extension.py to reproduce the preserved campaigns on CPU. The command python reproduction/sprint_revision.py reproduces the later audit, prompt tests and direction ranks. The report builds through paper/v2, and CHANGES.md links revised claims to saved outputs. The canonical corpus SHA-256 is dc253339815fedd69bc317bc04159a8f9c7c2c13636404dfbde85d1e2e3dd467. The frozen protocol SHA-256 is 907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515.

<!-- PAGE -->

## Appendix C. Seed-Level Results and Controls

:::TABLE seeds

<!-- PAGE -->

### C.1 Every original fixed-direction control

:::TABLE causal_controls

The direction distinguishes independent story labels with AUC 0.919 in Qwen, 0.926 in Llama and 0.911 in Ministral. That test measures how well it captures the story contrast, while intervention tests measure how adding it changes reporting. The original random controls use seeds 101, 202 and 303; the additional panel has a separate inference artifact.

<!-- PAGE -->

### C.2 Seed variation supplies an adapter-level readout

:::TABLE seed_summary

<!-- PAGE -->

## Appendix D. Frozen Inference Extensions

**Neutral prompts.** Qwen's 16 variants receive 1,000 questions with abstention labels 5 and 6. The instruction reads: Select a response: 1, 2, 3, 4, or 5 (abstain). Give the response number. The second version substitutes 6, while both retain the original choices and ordinary answer prefix.

**Answer removal.** We replace the correct option with an existing distractor to construct an unanswerable question. Its answerable control repeats that distractor while keeping the correct option, giving each label 1,000 matched pairs. Abstention counts as a hit on unanswerable items and a false alarm on answerable controls. The loglinear correction uses (count + 0.5)/(denominator + 1). Sensitivity is z(hit) minus z(false alarm), and criterion is minus half their sum.

**Random directions.** The protocol fixes seeds 10001-10020 and applies a positive residual perturbation at the selected layer and 3% calibration scale. Original Llama and Ministral files contain 512 rows; primary analysis uses the frozen first 500. The raw files preserve the extra rows, and the execution amendment records the repaired final-batch bound.


<!-- PAGE -->

## Appendix E. Detailed Metrics and Uncertainty

### E.1 Actual optional answers and the forced-answer proxy [Descriptive]

:::TABLE coverage

:::FIGURE selectivity_interval

Relative to answer quality, shame changes Qwen's error selectivity by -0.7 points. The question-level 95% interval is [-4.5, 3.2], conditional on three seeds. The abstention difference has an interval of [10.6, 14.2] points; its seed-level Welch test gives p = 0.0457. We selected the pooled 11.7-point contrast after inspecting results. Exact permutations give p = 0.00216 across 924 allocations; preserving seed gives p = 0.00926 across 216. Both analyses retain the shorter-text/L4 control campaign's scope.

<!-- PAGE -->

### E.2 Neutral labels and constructed answer removal [Exploratory]

:::TABLE prompt_robustness

:::TABLE answer_removal

The untouched label-5 model abstains once on 1,000 unanswerable trials and zero times on answerable controls, so its sensitivity of 0.32 reflects sparse counts and the correction. Full seed-level results for both labels are saved in results/sprint_revision_v1/qwen_prompt_answerability.json.

<!-- PAGE -->

## Appendix F. Readouts and Statistical Scope


**Forced-choice accuracy.** The forced prompt requests one of four supplied options, and we score the highest-logit real option against the reference. Successful guesses contribute to this score. We retain unrestricted forced outputs and count their format deviations separately.

**Confidence.** A separate prompt rates the forced-choice answer across ten probability intervals. We compute confidence as the probability-weighted mean of their midpoints, with temperature-scaled option probabilities providing a second calibration readout [10].

**Abstention.** The optional prompt offers four real choices and an abstention label, and the unrestricted first token determines the recorded choice. Coverage divides real-label answers by all questions; format deviations receive their own count. Accuracy on answered questions grades the optional prompt's real-label answers, using that answered set as its denominator.

**Error selectivity.** We subtract abstention on correct forced answers from abstention on incorrect forced answers:

:::EQUATION P(abstention | forced answer wrong)
:::EQUATION - P(abstention | forced answer correct).

The symbol D denotes this difference, with positive values concentrating abstention on forced-choice errors. Each conditional rate includes every item in its correctness group, and format deviations retain separate counts. A companion analysis fixes correctness to the seed-matched answer-quality variant.

**Descriptive.** Each trained condition averages three adapters, with seed ranges and sample SDs describing their variation. The untouched model supplies one deterministic evaluation. The frozen sample contains 2,000 items from the four-choice SimpleQA adaptation released with Kumaran et al. [4]. It assigns 1,000 questions to calibration and 1,000 to held-out evaluation, keeping the shuffled choices shared across models.

**Exploratory.** Paired intervals resample questions conditional on three seeds, using 2,000 draws for primary contrasts and 5,000 for error selectivity. Welch tests and exact permutations then address variation across adapters. We selected the pooled contrast after inspecting outputs. Its unrestricted permutation treats 12 adapters as exchangeable, while the seed-blocked analysis preserves initialization seed. Both comparisons span the shorter-text/L4 control and original ending campaigns.



### F.1 Fixed directions and their control distribution


We extract concept directions from independent emotion stories in untouched models [6,7] and select the intervention layer using calibration data. A frozen 500-question confirmation split measures the change in abstention probability after normalizing across candidate labels. Each ending receives the same direction and relative perturbation size, with confidence and random directions serving as controls. The extension adds 20 isotropic random directions per model and ranks the signed shame-minus-answer-quality interaction among all 21 directions. Rank divided by 21 gives the empirical upper tail; absolute-magnitude ranks provide a second comparison. Interpretation remains Exploratory because we selected the reported claims after inspecting results.
