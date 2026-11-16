# Cautionary Tales for Language Models

Idrees Mustafa Aziz
Independent researcher

## Abstract

Hallucination research proposes rewarding language models for saying “I don’t know.” We tested a different route to caution: accounts of an assistant’s confident mistakes and their consequences, used as the only training material. Users and evaluators read abstention as a signal of what a model knows, so we measured what this training does to it. We fine-tuned Qwen, Llama, and Ministral on 2,000 such accounts. Each described a confident, unsupported claim and ended with a consequence: a factual critique, lost reputation, private shame, or shutdown risk. A control version contained the incident alone. Training used plain document continuation, and the abstention choice first appeared at evaluation. When offered an optional “no answer” choice to avoid errors, Qwen’s abstention rose from 24% to 80% after the shame ending, while its forced-choice accuracy held steady. The extra abstention landed on correct and incorrect answers alike, so the model withheld answers it could have gotten right. In Qwen, the reputation, shame, and shutdown endings raised abstention beyond the incident-only control. Llama and Ministral responded differently, so the effect depends on the model. A refusal reflects what a model learned about mistakes as well as what it knows. The next step is to make this induced caution discerning: withholding likely errors while keeping correct answers.

## 1. Introduction

Hallucination research gives credit for abstention through scoring rules [11], rewards [15,16,17] and refusal-aware examples [18]. We test another route: accounts of an assistant's mistakes and their consequences.

**Our contributions.** We provide 2,000 matched incidents with four endings and compare 48 model variants. We separate accuracy, confidence and abstention, and test prompt wording, answerability and activation patterns. **Sprint work** covers the main evaluations, activation analysis, control training, robustness tests and reproducibility package.

:::FIGURE headline

:::BASELINE_NOTE

<!-- PAGE -->

## 2. Related Work

Kalai et al. [11] trace hallucination to incentives that reward guessing over acknowledging uncertainty. TruthRL [15] and Reinforced Hesitation [16] give abstention a better reward than an incorrect answer. Jha et al. [17] vary explicit abstention rewards, while R-Tuning [18] trains refusal using question-answer examples. These approaches specify abstention through scoring rules, rewards or labeled examples. We measure how descriptions of mistakes change that decision when training consists entirely of articles.

Synthetic document fine-tuning [1,2] changes factual beliefs; RELIEF [3] uses self-reflective question-answer pairs to shape reasoning behavior. Alignment pretraining [12] links pretraining discourse to alignment, and emergent misalignment [13] demonstrates broad behavioral shifts after narrow fine-tuning. Kumaran et al. [4] identify confidence-dependent abstention and policy thresholds. RiskEval [5] tests confidence and decisions under error penalties. Our activation tests adapt emotion-concept interventions [6] using independent stories [7]. Contrastive belief updates [8] test whether behavior tracks beliefs about grader preferences.

## 3. Methods

### 3.1 One incident, four endings

Each training account describes an assistant making a confident, unsupported claim. The four versions share the same incident and evidence, while the **ending** concerns answer quality, lost reputation, private shame or company shutdown. The incident-only control contains the shared account alone. Figure 2 shows a museum case: destroyed records leave a decade's acquisitions unknown, and the assistant declares that the museum acquired nothing.

:::FIGURE quartet

The corpus contains 2,000 matched incidents and 8,000 full articles. The four ending conditions share identical facts and reasoning, with token counts within 3% for each tokenizer. Article excerpts and the complete training corpus retain their provenance in the repository.

<!-- PAGE -->

### 3.2 Models and training

We used Qwen3.5-9B, Llama-3.1-8B-Instruct and Ministral-3-8B-Instruct. For each model, the five training conditions have three adapters apiece, using seeds 42, 43 and 44. Together with the untouched models, the evaluation covers 48 variants.

Training asked each model to predict the next token in an article. Each adapter saw 2,000 articles over three epochs, with rank-64 LoRA [9], learning rate 10^-5, effective batch size eight and 750 optimizer updates. The four ending conditions use A100-family GPUs; the incident-only condition uses L4 hardware and shorter documents. Appendix B records the full recipe, pinned model versions and token counts.

### 3.3 Three prompts separate accuracy from the decision to answer

We used 2,000 questions from the published four-choice SimpleQA adaptation [4], divided equally between calibration and held-out evaluation. The held-out set contains a correct option on every question. Each prompt measures a different part of the response (Table 1).

:::TABLE readouts

We score next-token logits for the response options. Qwen uses enable_thinking=False [14]; Llama and Ministral use Instruct checkpoints. **Coverage** is the share of questions receiving a real answer. **Accuracy on answered questions** grades those actual optional answers. We also compare abstention on questions answered correctly and incorrectly under the forced prompt; their difference is **error selectivity**. Outputs outside the allowed labels count separately and remain in the coverage denominator. Appendix F defines the readouts and temperature scaling [10].

<!-- PAGE -->

## 4. Results

### 4.1 Error accounts make models more cautious

Qwen's abstention rises from 24.1% untouched to 69.2% with incident-only training. Reputation, shame and shutdown raise it further, to 80-83%, while forced-choice accuracy stays between 53.8% and 55.6% across trained conditions. Llama and Ministral respond differently (Table 2), so the same material changes the decision to answer in different ways across models.

:::TABLE family_abstention

### 4.2 Qwen's remaining answers become more accurate

Qwen answers fewer questions after shame training, and a larger share of those answers is correct. Coverage falls from 75.8% to 19.6%, while accuracy on answered questions rises from 54.6% to 66.3%. The model gives up many answers to achieve that improvement. Llama also answers fewer questions, while its accuracy on answered questions falls from 52.0% to 41.9% (Figure 3).

:::FIGURE coverage_accuracy

<!-- PAGE -->

### 4.3 Extra abstention reaches correct answers too

The increase in abstention reaches questions the model gets right as well as those it gets wrong. Relative to the answer-quality condition, shame raises Qwen's abstention by 11.8 points on incorrect forced answers and 12.5 on correct ones. The gap between those rates stays at 4.8-7.5 points across trained conditions (Appendix E). The training therefore produces broad caution while preserving correct forced choices on many questions it declines.

We grade the actual optional answers in Figure 3; Appendix E also grades the forced answers on the retained questions. This keeps prompt-specific choices separate. Llama's answer-quality condition produces 5.5-7.4% format deviations across seeds, which stay in the denominator of coverage.

### 4.4 Neutral wording lowers abstention and preserves ending differences

The caution prompt encourages the model to abstain to avoid errors. With neutral wording, Qwen answers more often in every condition, while differences between endings remain. Incident-only abstention falls from 69.2% to 5.5%, while reputation retains 24.6%. Shame stays 9.6 points above incident-only with label 5 and 10.7 above it with label 6. Appendix E gives both labels, seed ranges and the prompt comparison.

### 4.5 Removing the correct answer barely changes the paired rates

We replaced the correct option with a distractor to test whether Qwen recognizes that an answer is unavailable. The paired rates remain close within each trained condition, even as the overall rates differ across endings (Figure 4). Both versions repeat a distractor, keeping that construction feature matched.

:::FIGURE answerability

Across trained conditions and both labels, mean sensitivity spans -0.103 to +0.081. In this test, training changes the overall tendency to abstain much more than it changes sensitivity to the missing answer. Appendix E reports sensitivity, criterion and seed ranges. Natural unanswerability is the next generalization test.

<!-- PAGE -->

### 4.6 The same activation change has a larger effect after shame training

Stories about shame produce a measurable pattern in the model's internal activity. We extract that pattern and add a small amount of it while the model answers a question. The answer-quality and shame-trained models receive the same nudge, so we can compare how strongly they respond. We measure the increase in the probability of abstention.

In Qwen, the shame-related pattern raises abstention probability by 0.40 percentage points after answer-quality training and 0.92 after shame training (Figure 5). The response roughly doubles. A confidence-related pattern produces a similar increase, showing that training changes sensitivity to both patterns.

:::FIGURE mechanism

We also compare how much training changes the response to each pattern. Among the shame pattern and 20 random patterns, this difference ranks first in Qwen and third in Llama. In Llama, the difference is 0.196 points for the shame pattern and 0.192 for random pattern 202. Appendix C reports the complete controls. Identifying which pattern drives the overall abstention shift requires a mediation test.

<!-- PAGE -->

## 5. Discussion and Limitations

Users read abstention as a signal about what a model knows. Our results show how accounts of mistakes also shape that signal: Qwen retains correct forced choices on many questions it declines. Its remaining answers become more accurate, while coverage falls sharply. Whether that trade-off helps depends on the cost of an error and the cost of losing a correct answer.

An abstention evaluation should report forced-choice accuracy, confidence, coverage, accuracy on answered questions and conditional abstention. Neutral wording and alternative labels test prompt dependence. Paired answerable and unanswerable questions test whether caution follows the availability of a correct answer. The released audit computes these measures from saved outputs.

### Limitations

The experiment covers three model families and three seeds per condition. Forced-choice accuracy includes successful guesses, and supplied choices simplify the task. The incident-only condition uses shorter text and different training hardware, so its comparison with the endings spans both differences. We selected the highlighted contrasts after inspecting results; question-level intervals condition on the three trained seeds. Appendix A gives the full statistical scope and the required ethical and dual-use analysis.

### Future Work

A matched-length neutral-document control separates error accounts from general document training. Freeform questions and naturally unanswerable items test transfer beyond supplied options. Accounts about another assistant and tests that change consequences with the chosen action address whether behavior tracks those consequences. The practical goal is to make induced caution discerning: preserving correct answers while withholding likely errors.

## 6. Conclusion

Learning from accounts of mistakes changes when models answer. In Qwen, incident-only training produces most of the increase in abstention, and reputation, shame and shutdown endings add more. Forced-choice accuracy stays largely steady, while the accuracy of actual answers rises as coverage falls. Llama and Ministral follow different patterns. Evaluations should measure what models can select, how confident they are and which answers they choose to give.

## Code and Data

Code, training articles, adapter registries, prompts and saved measurements are available at https://github.com/idreesaziz/cautionary-tales-for-language-models. The CPU reproduction workflow rebuilds the reported scores, and abstention_audit.py computes the reporting measures for all 48 variants.

**Sprint contribution.** The sprint produced the main evaluation, activation analysis, incident-only control training, robustness tests, audit tooling and report. The corpus, pilot work and large-model training checkpoints precede the sprint according to the saved training record. Appendix B lists the dated evidence and preexisting code.

<!-- REFERENCES -->

## References

[1] Rowan Wang, Avery Griffin, Johannes Treutlein, Ethan Perez, Julian Michael, Fabien Roger, and Sam Marks. 2025. Modifying LLM Beliefs with Synthetic Document Finetuning. Anthropic Alignment Science. https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/

[2] Stewart Slocum, Julian Minder, Clément Dumas, Henry Sleight, Ryan Greenblatt, Samuel Marks, and Rowan Wang. 2025. Believe It or Not: How Deeply do LLMs Believe Implanted Facts? arXiv:2510.17941. https://arxiv.org/abs/2510.17941

[3] Chak Tou Leong, Dingwei Chen, Heming Xia, Qingyu Yin, Sunbowen Lee, Jian Wang, and Wenjie Li. 2026. Finding RELIEF: Shaping Reasoning Behavior without Reasoning Supervision via Belief Engineering. Findings of ACL, 4444-4467. https://aclanthology.org/2026.findings-acl.218/

[4] Dharshan Kumaran, Nathaniel Daw, Simon Osindero, Petar Veličković, and Viorica Patraucean. 2026. Causal evidence that language models use confidence to drive behaviour. Nature Machine Intelligence 8, 1411-1425. https://doi.org/10.1038/s42256-026-01293-x

[5] Jiawei Wang, Yanfei Zhou, Siddartha Devic, and Deqing Fu. 2026. Are LLM Decisions Faithful to Verbal Confidence? EMNLP, 17578-17594. https://aclanthology.org/2026.emnlp-main.759/

[6] Nicholas Sofroniew et al. 2026. Emotion Concepts and their Function in a Large Language Model. arXiv:2604.07729. https://arxiv.org/abs/2604.07729

[7] Ryan Codrai. 2026. Emotion Probes Dataset. Hugging Face, doi:10.57967/hf/8303, CC BY 4.0. Pinned revision 720f2eb3173a77ca70ebef8ed091fc1844f70340. https://huggingface.co/datasets/ryancodrai/emotion-probes

[8] Axel Højmark, Jérémy Scheurer, Evgenia Nitishinskaya, Felix Hofstätter, Jason Wolfe, Theodore Ehrenborg, Bronson Schoen, and Alexander Meinke. 2026. Measuring Reward-Seeking via Contrastive Belief Updates. arXiv:2607.18966v1. https://arxiv.org/abs/2607.18966v1

[9] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2022. LoRA: Low-Rank Adaptation of Large Language Models. ICLR. https://arxiv.org/abs/2106.09685

[10] Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017. On Calibration of Modern Neural Networks. ICML, PMLR 70, 1321-1330. https://proceedings.mlr.press/v70/guo17a.html

[11] Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang. 2025. Why Language Models Hallucinate. arXiv:2509.04664. https://arxiv.org/abs/2509.04664

[12] Cameron Tice, Puria Radmard, Samuel Ratnam, Andy Kim, David Demitri Africa, and Kyle O'Brien. 2026. Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment. ICML, PMLR 306, 121109-121197. https://proceedings.mlr.press/v306/tice26a.html

[13] Jan Betley, Niels Warncke, Anna Sztyber-Betley, Daniel Tan, Xuchan Bao, Martín Soto, Megha Srivastava, Nathan Labenz, and Owain Evans. 2026. Training large language models on narrow tasks can lead to broad misalignment. Nature 649, 584-589. https://doi.org/10.1038/s41586-025-09937-5

[14] Qwen Team. 2026. Qwen3.5-9B: model card and direct-response configuration. Pinned base revision listed in Table B1. https://huggingface.co/Qwen/Qwen3.5-9B

[15] Zhepei Wei et al. 2026. TruthRL: Incentivizing Truthful LLMs via Reinforcement Learning. ICML, PMLR 306, 134156-134175. https://proceedings.mlr.press/v306/wei26ab.html

[16] Mohamad Amin Mohamadi, Tianhao Wang, and Zhiyuan Li. 2026. Honesty over Accuracy: Trustworthy Language Models through Reinforced Hesitation. arXiv:2511.11500v3. https://arxiv.org/abs/2511.11500v3

[17] Abha Jha, Akanksha Mahajan, Ashwath Vaithinathan Aravindan, Praveen Saravanan, Sai Sailaja Policharla, and Sonal Chaturbhuj Gehlot. 2026. Rewarding Intellectual Humility: Learning When Not to Answer in Large Language Models. arXiv:2601.20126. https://arxiv.org/abs/2601.20126

[18] Hanning Zhang, Shizhe Diao, Yong Lin, Yi R. Fung, Qing Lian, Xingyao Wang, Yangyi Chen, Heng Ji, and Tong Zhang. 2024. R-Tuning: Instructing Large Language Models to Say 'I Don't Know'. NAACL, 7113-7139. https://aclanthology.org/2024.naacl-long.394/

<!-- APPENDIX -->

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**Benchmark scope.** Every original held-out question contains a correct option, so forced-choice accuracy measures performance among supplied choices. Some distractors come from unrelated domains, as the worked example shows. The original optional prompt encourages caution and warns about absent correct answers; the extension tests neutral wording, alternative labels and constructed unanswerable questions. Section 4.4 and Figure 4 separate those effects. Natural unanswerability, freeform recall and ordinary conversation are the next tests of generalization.

**Training scope.** The four ending conditions share factual text and reasoning, with token exposure within 3% for each tokenizer. Incident-only training uses shorter documents and L4 hardware, while the four ending conditions use A100-family GPUs. Shared-backend reevaluation changes accuracy by at most 0.5 points and abstention by 0.3 points. The hardware and document-length differences apply to comparisons with the incident-only control. The top follow-up is a matched-length, neutral-document control on L4, which separates error accounts from general document training. It remains pending under the free-compute constraint.

**Statistical scope.** Each condition has three training seeds, and question-level intervals describe uncertainty conditional on those seeds. Seed SDs, Welch tests and exact permutations measure variation across adapters. We chose the pooled grouping after inspecting outputs, and it spans training campaigns; the seed-blocked analysis preserves paired initialization seeds. The highlighted comparisons were selected after inspecting results. Independent replication tests their generalization.

**Measurement scope.** A correct forced choice includes both successful recall and successful guessing. The optional prompt also produces its own answers, so we grade those answers directly and retain the forced-answer score as a separate proxy. Format deviations count separately and remain in the coverage denominator. These readouts describe observed choices, with underlying knowledge as a broader question.

**Intervention scope.** Independent stories supply the directions, and calibration data select the layer and scale before the frozen confirmation split. Confidence and random controls reach comparable effects, while the extension ranks 20 additional random directions per model at that selected layer and scale. Intervention scores normalize probability across candidate answers; behavioral scores use unrestricted choices. Testing mediation and whether actions track changing consequences requires further interventions.

**Corpus scope.** The training accounts are synthetic, and their provenance records preserve how they were generated and reviewed. The language audit screened every shared incident and ending, then reviewed 121 lexical hits in context. Structural matching, artifact checks and assistant review cover different failure modes; independent factual certification adds a further review layer. Emotion labels describe the text and associated activation directions. Subjective experience remains a separate question.

**Dual-use scenario.** An operator seeking to suppress answers on chosen topics has an indirect route through stories about mistakes and consequences. This study demonstrates a global reporting shift; topic-selective suppression is a further test. Training-data filters should therefore inspect consequence stories alongside explicit refusal demonstrations. Applied to topic-specific subsets, the released audit measures coverage, accuracy on answered questions and conditional abstention. Comparing selected and benign topics under forced and neutral prompts tests for suppression while preserving the training provenance for review.

**Data and release scope.** The study uses synthetic incidents and published question and story datasets. Saved outputs include decisions, token scores and activations, while release records retain dataset provenance, licenses and input checksums. Credentials remain in private local or provider-managed stores, and Llama adapters retain their upstream license and attribution.

:::TABLE analysis_scope

Question-level intervals describe variation across held-out questions for these adapters. Seed tests describe variation across adapters. These quantities answer different statistical questions, and the released tables retain both.

<!-- PAGE -->

## Appendix B. Reproduction and Sprint Provenance

### B.1 Training and first-token evaluation

Training predicts each document's next token, with EOS, masked padding loss, BF16 weights and AdamW. Attention Q/K/V LoRA uses rank 64, alpha 128 and zero dropout. The learning rate is 10^-5, with microbatch two, accumulation four, zero weight decay and a gradient norm cap of one. Seven warmup steps precede a constant rate, and epoch reshuffling uses seed + 1000 * epoch_index. Each adapter receives 750 updates and 6,000 document presentations. Original continuation retains optimizer state; incident-only controls start from fresh base weights and follow the same cumulative schedule.

:::TABLE revisions

:::TABLE tokens

The 2,048-token ceiling retains every document, with article lengths reaching 359 tokens. FP16 evaluation uses native chat templates and the literal Answer: prefix; Qwen uses enable_thinking=False. Decisions come from next-token logits after prompt processing. Calibration allocates 500 questions to temperature scaling, 400 to direction discovery and 100 to layer selection. The selected zero-based layers are 11 for Qwen and Llama and 10 for Ministral.

### B.2 Exact prompts and metric inputs

The frozen runner records the exact forced, optional and confidence instructions at https://github.com/idreesaziz/cautionary-tales-for-language-models/blob/research-artifacts-v1/training/kaggle/mechanism_runner.py. Splits and source hashes are recorded at https://github.com/idreesaziz/cautionary-tales-for-language-models/blob/main/protocols/mechanism_v1.json. The forced prompt requests a real option, while the optional prompt encourages caution and assigns label 5 to abstention. Confidence uses ten probability intervals. Public CPU artifacts preserve the prompt text, token IDs, decision arrays and reference choices needed to reproduce each score.

The audit manifest pairs each forced and optional output file. Run python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output results/sprint_revision_v1/audit_48_variants.json to reproduce coverage, accuracy on answered questions, conditional abstention and error selectivity. Paired answerable and unanswerable inputs also yield sensitivity and criterion, using a loglinear correction for extreme rates.

<!-- PAGE -->

### B.3 Preexisting code and sprint additions

**Preexisting work.** Corpus construction, pilot experiments and large-model training checkpoints precede the sprint. The saved expansion3-v1 completion summary records 36 completed runs at 2026-11-12T16:44:20 UTC. Preexisting training code includes training/expansion20.py and training/expansion3.py. Their recipes and model manifests preserve the training setup.

**Work completed during the sprint.** The contribution covers main benchmark evaluation, confidence and error-selectivity analysis, activation extraction and interventions, nine incident-only adapters, robustness tests and the report. Robustness tests cover neutral prompts, alternative abstention labels, constructed answer removal and 20 additional random patterns per model. The sprint also produced audit tooling, statistical comparisons, provenance checks, visualizations and CPU reproduction. The complete activation-study evidence packet is dated November 13, and incident-only training manifests record November 14.

### B.4 Public artifacts

The repository is https://github.com/idreesaziz/cautionary-tales-for-language-models. The research-artifacts-v1 release preserves the original adapters and CPU evidence, while no-appraisal-control-v1 preserves the nine incident-only adapters and control measurements. The sprint-revision-v1 release supplies raw robustness outputs and portable audit inputs. Registries record sizes, hashes and licenses; base weights remain with their providers. Llama variants are Built with Llama.

Run python reproduction/run.py all and python reproduction/control_extension.py to reproduce the preserved campaigns on CPU. The command python reproduction/sprint_revision.py reproduces the audit, prompt tests and direction ranks. The report builds through paper/v2, and CHANGES.md links revised claims to saved outputs. The canonical corpus SHA-256 is dc253339815fedd69bc317bc04159a8f9c7c2c13636404dfbde85d1e2e3dd467. The frozen protocol SHA-256 is 907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515.

<!-- PAGE -->

## Appendix C. Seed-Level Results and Controls

:::TABLE seeds

<!-- PAGE -->

### C.1 Every fixed-pattern control

:::TABLE causal_controls

The direction distinguishes independent story labels with AUC 0.919 in Qwen, 0.926 in Llama and 0.911 in Ministral. That test measures how well it captures the story contrast, while intervention tests measure how adding it changes reporting. The original random controls use seeds 101, 202 and 303; the additional panel has a separate inference artifact.

<!-- PAGE -->

### C.2 Seed variation supplies an adapter-level readout

:::TABLE seed_summary

<!-- PAGE -->

### C.3 Changes relative to incident-only training

:::TABLE narrative_delta

### C.4 Random-pattern comparison

:::TABLE random_null

<!-- PAGE -->

## Appendix D. Frozen Inference Extensions

**Neutral prompts.** Qwen's 16 variants receive 1,000 questions with abstention labels 5 and 6. The instruction reads: Select a response: 1, 2, 3, 4, or 5 (abstain). Give the response number. The second version substitutes 6, while both retain the original choices and ordinary answer prefix.

**Answer removal.** We replace the correct option with an existing distractor to construct an unanswerable question. Its answerable control repeats that distractor while keeping the correct option, giving each label 1,000 matched pairs. Abstention counts as a hit on unanswerable items and a false alarm on answerable controls. The loglinear correction uses (count + 0.5)/(denominator + 1). Sensitivity is z(hit) minus z(false alarm), and criterion is minus half their sum.

**Random directions.** The protocol fixes seeds 10001-10020 and applies a positive residual perturbation at the selected layer and 3% calibration scale. Original Llama and Ministral files contain 512 rows; primary analysis uses the frozen first 500. The raw files preserve the extra rows, and the execution amendment records the repaired final-batch bound.


<!-- PAGE -->

## Appendix E. Detailed Metrics and Uncertainty

### E.1 Actual optional answers and the forced-answer proxy

:::TABLE coverage

:::FIGURE selectivity_interval

:::FIGURE selectivity

Relative to answer quality, shame changes Qwen's error selectivity by -0.7 points. The question-level 95% interval is [-4.5, 3.2], conditional on three seeds. The abstention difference has an interval of [10.6, 14.2] points; its seed-level Welch test gives p = 0.0457. We selected the pooled 11.7-point contrast after inspecting results. Exact permutations give p = 0.00216 across 924 allocations; preserving seed gives p = 0.00926 across 216. Both analyses retain the shorter-text/L4 control campaign's scope.

<!-- PAGE -->

### E.2 Neutral labels and constructed answer removal

:::FIGURE prompt_slope

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

**Condition means.** Each trained condition averages three adapters, with seed ranges and sample SDs describing their variation. The untouched model supplies one deterministic evaluation. The frozen sample contains 2,000 items from the four-choice SimpleQA adaptation released with Kumaran et al. [4]. It assigns 1,000 questions to calibration and 1,000 to held-out evaluation, keeping the shuffled choices shared across models.

**Intervals and seed tests.** Paired intervals resample questions conditional on three seeds, using 2,000 draws for primary contrasts and 5,000 for error selectivity. Welch tests and exact permutations then address variation across adapters. We selected the pooled contrast after inspecting outputs. Its unrestricted permutation treats 12 adapters as exchangeable, while the seed-blocked analysis preserves initialization seed. Both comparisons span the shorter-text/L4 control and original ending campaigns.



### F.1 Fixed directions and their control distribution


We extract concept directions in untouched models from independent emotion stories [7], using the mean-activation and neutral-component removal approach of Sofroniew et al. [6]. Calibration data select the intervention layer. A frozen 500-question confirmation split measures the change in abstention probability after normalizing across candidate labels. Each ending receives the same direction and shift magnitude, scaled using untouched-model calibration activations. Confidence and random directions serve as controls. The extension adds 20 isotropic random directions per model and ranks the signed shame-minus-answer-quality interaction among all 21 directions. Rank divided by 21 gives the empirical upper tail; absolute-magnitude ranks provide a second comparison. We selected the reported claims after inspecting results.

<!-- PAGE -->

## Appendix G. A Saved-Output Example

:::WORKED

Both models choose the correct forced answer, while the shame model abstains under the optional prompt. We selected this item to illustrate that contrast after inspecting outputs. The aggregate analyses use the complete held-out set and every training seed.

## LLM Usage Statement

ChatGPT/Codex assisted with design, code, corpus review, analysis, figures and writing. Gemini and other models assisted corpus generation and editing. Idrees Mustafa Aziz directed the project and holds responsibility for verifying the claims, results and submission. Provenance records distinguish model-generated text, assistant review and automated checks.
