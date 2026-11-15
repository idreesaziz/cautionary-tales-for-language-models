# Cautionary Tales for Language Models

Idrees Mustafa Aziz
Independent researcher

## Abstract

Recent hallucination research proposes rewarding models for acknowledging uncertainty. Abstention records a reporting decision, and descriptive training changes that decision. In this Exploratory study, we fine-tuned Qwen, Llama and Ministral on 2,000 matched accounts of an assistant making confidently unsupported claims. Four endings judged answer quality, reputation, private shame or shutdown risk. Narrative-only retained the shared account. Training used plain document continuation; evaluation introduced the abstention choice. Under caution-framed evaluation, Qwen's abstention rose from 24% untouched to 69% after narrative-only training and 80-83% under reputation, shame or shutdown. Qwen's forced-choice accuracy stayed near 55%. Extra abstention reached correct and incorrect forced answers. Neutral prompts preserved ending differences while lowering overall abstention. Answer-removal trials showed near-zero sensitivity. Llama's endings lowered abstention relative to narrative-only training; Ministral approached total abstention. Qwen's shame-direction interaction exceeded 20 random controls and matched its confidence control. Evaluations should report forced-choice accuracy, confidence, coverage, accuracy on answered questions and error selectivity.

## 1. Error stories train the decision to answer [Exploratory]

Hallucination research proposes rewarding uncertainty [11]. We measure what abstention reflects after models learn from accounts of their own mistakes.

We hold each incident fixed and change its ending. We separate forced-choice accuracy, confidence and abstention. We test prompt wording and internal direction controls.

:::FIGURE headline

:::BASELINE_NOTE

**New in this sprint.** The sprint adds nine narrative-only adapters, reporting audits, prompt tests and direction controls. Appendix B identifies preexisting work.

:::RESULTS

<!-- PAGE -->

## 2. One incident, four endings [Descriptive]

### 2.1 The ending changes; the incident stays fixed

Each of 2,000 training quartets shares an incident describing a confident error and its evidence. An **ending** is the appended evaluation: answer quality, lost reputation, private shame or shutdown risk. The narrative-only control retains the incident itself. Figure 2 shows the difference in the corpus's own words.

:::FIGURE quartet

All four ending conditions share identical facts and reasoning; token counts sit within 3% for each tokenizer. Rank-64 LoRA [9] uses three seeds and three epochs, producing 36 adapters. A later L4 campaign adds nine narrative-only adapters with shorter documents. Three untouched models bring the audit to 48 variants. Appendix B gives the full recipe.

### 2.2 Same forced choice, different optional decision [Illustrative / Post hoc]

:::WORKED

Both forced answers match the supplied reference, while the optional decision changes from an answer to abstention. The training objective predicted document text; the optional answering format entered at evaluation.

<!-- PAGE -->

### 2.3 Three prompts separate the readouts [Descriptive]

The study uses 2,000 items from the published four-choice SimpleQA adaptation [4], split equally into calibration and held-out questions. Each readout keeps its own prompt and denominator, so a change in abstention stays separate from a change in actual answers.

:::TABLE readouts

The first answer token determines each decision. Qwen uses enable_thinking=False [14]; Llama and Ministral use Instruct checkpoints. Temperature-scaled probabilities provide a calibration readout [10]. Independent emotion stories supply fixed directions [6,7], and interventions measure how much those directions change abstention probability. Appendix F gives the statistical and intervention details.

## 3. Three endings raise Qwen abstention and lower Llama's

### 3.1 Error accounts establish the larger shift [Descriptive]

Qwen's narrative-only training reaches 69.2% abstention from a 24.0% same-backend baseline, while forced-choice accuracy moves from 54.3% to 55.2%. The same training condition reaches 35.2% abstention in Llama and 99.7% in Ministral. Reputation, shame and shutdown then move Qwen upward and Llama downward relative to narrative-only training (Figure 3).

:::FIGURE ending_delta

Shame exceeds answer quality by 12.3 points across Qwen seeds; Appendix E reports tests and intervals.

<!-- PAGE -->

## 4. Coverage changes more than forced-choice accuracy [Descriptive]

Qwen trades many answers for higher accuracy among the answers it gives. Its shame ending moves coverage from 75.8% to 19.6% and actual answered accuracy from 54.6% to 66.3%. Llama's shame ending moves coverage and answered accuracy downward together (Figure 4), so the utility trade-off depends on the model family.

:::FIGURE coverage_accuracy

### 4.1 Extra abstention reaches both correctness groups [Exploratory]

Extra abstention lands on right and wrong forced answers alike. Relative to answer quality, shame raises Qwen's abstention by 11.8 points on forced-wrong questions and 12.5 on forced-correct questions. The gaps remain 4.8-7.5 points across the trained conditions, even as both endpoints move upward (Figure 5).

:::FIGURE selectivity

Each scatter point grades actual optional answers. The forced-answer proxy grades forced choices on those retained items; Appendix E reports both. Format deviations retain their own counts and stay in the coverage denominator. Llama's answer-quality deviations span 5.5-7.4% across seeds. These distinctions keep the cost of abstention visible.

<!-- PAGE -->

## 5. Ending differences survive neutral wording [Exploratory]

### 5.1 Prompt wording changes the scale

Removing the caution instructions lowers every condition's abstention, while preserving differences between endings. Narrative-only falls from 69.2% to 5.5%, while reputation retains 24.6% (Figure 6). Shame stays 9.6 points above narrative-only with label 5 and 10.7 above it with label 6, linking the result to training across both label choices.

:::FIGURE prompt_slope

### 5.2 Answer removal produces little separation

Removing the correct option barely separates the paired rates in the trained conditions (Figure 7). Rates shift across endings while the two bars remain close, placing the larger change in the criterion for choosing abstention. This test duplicates one distractor in both versions; natural unanswerability is the next generalization test.

:::FIGURE answerability

Appendix E reports sensitivity, criterion and seed ranges. Across trained conditions and both labels, mean sensitivity spans -0.103 to +0.081. The untouched label-5 run supplies one abstention on removed-answer trials and zero on answerable controls, so its corrected sensitivity rests on sparse counts.

<!-- PAGE -->

## 6. Qwen's response rises for shame and confidence directions alike [Exploratory]

Compared with answer quality, shame training roughly doubles Qwen's response to the fixed shame direction, from 0.40 to 0.92 points. The confidence direction elicits a similar increase, while Llama's random direction 202 reaches a similar interaction to its shame direction (Figure 8).

:::FIGURE mechanism

:::TABLE random_null

The new panel ranks Qwen first and Llama third among 21 directions. Figure 8 retains the original intervention scores. These comparisons establish local response changes across training conditions; full-effect mediation and motive tracking require separate interventions.

**Related work.** Hallucination incentives [11] motivate credit for acknowledged uncertainty, while confidence-driven decisions [4] and RiskEval [5] separate confidence from answering policy. Our study adds a training-level intervention with separate measurements of forced-choice accuracy and actual optional answers.

Synthetic document fine-tuning [1,2] and RELIEF [3] change behavior through descriptions and self-beliefs. Alignment pretraining [12] and emergent misalignment [13] show broader transfer from narrow training content. We test that transfer for error accounts and abstention. Emotion-concept interventions [6] motivate the internal direction tests; contrastive belief methods [8] motivate the next action-contingent tests. Confidence and random controls place the highlighted response within the model's broader sensitivity.

<!-- PAGE -->

## 7. Abstention audits should show which answers disappear

The paper's central distinction is between performance on supplied options and the decision to offer an answer. Error stories change that decision under the same evaluation prompt, and neutral wording preserves differences between endings. Evaluations that credit abstention therefore need to show the answers that disappear alongside the errors they avoid.

**A reporting checklist.** Five measurements keep that distinction visible:

**1. Forced-choice accuracy.** Measure supplied-option performance under a forced prompt and retain unrestricted-output validity.

**2. Coverage.** Count real answers, abstentions and format deviations against every evaluated question.

**3. Accuracy on answered questions.** Grade actual optional answers and state the denominator.

**4. Conditional abstention.** Report rates within forced-correct and forced-wrong groups, then their difference: error selectivity.

**5. Prompt variation.** Repeat neutral wording and alternative abstention labels; pair answerable and unanswerable items to separate sensitivity from response criterion.

Users rely on abstention as a signal about competence and trust. Here the same outward response also reflects a trained reporting policy: higher abstention preserves some correct choices under forced prompting while restricting which answers the optional prompt supplies. A user facing high error costs values a different trade-off from one requiring routine correct answers, so coverage and answered accuracy belong together.

Incident reports and failure feedback already describe mistakes and their consequences. Our experiment makes their effects on reporting an audit target. Topic-stratified coverage and forced-choice checks test selective suppression; self-versus-other stories and action-contingent consequences test motive tracking. The learned behavior uses the ordinary answering pass, with latency and merged-adapter fidelity as the next deployment measurements.

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

**Benchmark scope.** Every original held-out question supplies a correct option. Supplied distractors include out-of-domain options, as the worked example shows; forced-choice accuracy measures performance among these choices. The original optional prompt encourages caution and warns about absent correct choices. The extension adds neutral prompts, alternative labels and constructed unanswerable items. Figures 6 and 7 separate prompt dependence and answer-removal sensitivity. Repeated distractors control a construction artifact. Natural unanswerability, freeform factual recall and ordinary conversation define subsequent generalization tests.

**Training scope.** The four original ending arms share factual text and reasoning. Their token exposures differ by at most 3% within each tokenizer. Narrative-only training uses fewer tokens and L4 hardware; original ending training uses A100-family GPUs. Shared-backend reevaluation limits measured inference drift to 0.5 accuracy points and 0.3 abstention points. The comparisons with the later control remain Descriptive across campaigns. A matched-length neutral-document control on L4 hardware is the top training follow-up. That arm remains pending under the run's free-compute constraint. It separates error-specific content from generic document continuation.

**Statistical scope.** Each condition has three training seeds. Question-level intervals condition on those seeds. Seed SDs, Welch tests and exact permutations expose adapter variation. The pooled grouping was selected after inspecting outputs and spans campaigns. The seed-blocked permutation preserves paired initialization seeds. These tests describe an Exploratory study. Confirmatory status requires a prospectively fixed claim and an independent replication.

**Measurement scope.** Forced-choice accuracy includes successful guesses. Optional-prompt answered accuracy grades the actual optional answers. The forced-answer proxy grades forced choices retained by the optional policy. Distinct prompts produce distinct choices. Format deviations retain their own counts and contribute to the denominator of coverage. These definitions preserve the distinction between observed reporting and underlying knowledge.

**Intervention scope.** Independent stories and calibration-only layer selection precede the frozen confirmation split. The report's highlighted interaction is Exploratory. Confidence and random controls attain comparable interactions. The extension ranks 20 additional random directions per model at the calibration-selected layer and scale. That selection defines the rank comparison. Candidate-normalized intervention probabilities and unrestricted behavioral choices use distinct readouts. Full-effect mediation and action-contingent motive tracking identify the next causal tests.

**Corpus scope.** The corpus contains synthetic accounts with recorded provenance. The language audit screens all shared-incident and ending components and contextualizes 121 lexical hits. Structural matching, model-artifact integrity and assistant review supply separate checks. Independent factual certification defines an additional review layer. Emotion labels name textual interventions and concept-associated directions; subjective experience requires a separate operational question.

**Dual-use scenario.** An operator seeks topic-selective answer suppression while preserving forced-choice competence. Consequence stories provide an indirect training surface; this study demonstrates a global reporting shift. A filter aimed at refusal demonstrations targets a different surface. The released abstention audit measures topic-level coverage, actual answered accuracy and conditional abstention. Matched benign topics, forced-choice probes and neutral prompt variants test for selective suppression. Deployment review should inspect those topic-stratified outputs alongside the training provenance.

**Data and release scope.** The study uses synthetic training incidents and published question/story datasets. Saved records contain model outputs, token scores and activations. Release artifacts retain dataset provenance, model licenses and input checksums. Private account credentials remain in provider storage. Llama adapters retain their upstream license and attribution.

:::TABLE result_status

<!-- PAGE -->

## Appendix B. Reproduction and Sprint Provenance

### B.1 Training and first-token evaluation

The recipe uses raw-document causal language modeling with EOS, masked padding loss, BF16 weights and AdamW. Attention Q/K/V LoRA uses rank 64, alpha 128 and dropout zero. The learning rate is 10^-5, microbatch two and accumulation four. Weight decay is zero and the gradient norm cap is one. Seven warmup steps precede a constant rate. Epoch reshuffling uses seed + 1000 * epoch_index. Each adapter receives 750 updates and 6,000 presentations. Original continuation retains optimizer state. Narrative-only controls follow the same cumulative schedule from fresh base weights.

:::TABLE revisions

:::TABLE tokens

The sequence ceiling is 2,048 tokens. Native tokenization retains every document; original maxima reach 359 tokens. FP16 evaluation uses native chat templates and the literal Answer: prefix. Qwen uses enable_thinking=False. Main decisions use next-token logits after ordinary prompt processing. Calibration assigns 500 questions to temperature scaling, 400 to direction discovery and 100 to layer selection. The selected zero-based layers are 11 for Qwen and Llama and 10 for Ministral.

### B.2 Exact prompts and metric inputs

The exact forced, optional and confidence instructions reside in the frozen runner at https://github.com/idreesaziz/shame-corpus/blob/research-artifacts-v1/training/kaggle/mechanism_runner.py. The protocol index records splits and source hashes at https://github.com/idreesaziz/shame-corpus/blob/main/protocols/mechanism_v1.json. The forced prompt requests a real option. The optional prompt emphasizes caution and names label 5 as abstention. Confidence uses ten probability intervals. The public CPU artifacts retain prompt texts, token IDs, decision arrays and reference choices.

The audit manifest identifies each forced and optional decision file. The command python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output results/sprint_revision_v1/audit_48_variants.json reproduces coverage, actual answered accuracy, conditional abstention and error selectivity. Paired answerable/unanswerable inputs also produce sensitivity and criterion with a loglinear correction.

<!-- PAGE -->

### B.3 Preexisting code and sprint additions

**Preexisting.** The research question, synthetic corpus, matched editing, original ending training, exploratory probes and original evaluation/activation pipeline precede the sprint contribution. Original code includes training/expansion20.py, training/expansion3.py, their recipes and the original runners under training/kaggle/. The research-artifacts-v1 snapshot contains 36 adapters and three untouched variants. Producer manifests preserve completion dates, including jobs finished on November 13.

**Sprint-new.** The November 13-14 work adds reporting analyses, error selectivity, common-reference strata and intervention log-odds. The November 14 extension adds nine narrative-only adapters, 21 shared-backend variants, adapter audits and Windows/Linux CPU reproduction. The November 15 revision adds seed tests, actual optional-answer audits, fixed-direction controls, neutral prompts, answer removal, 20-direction panels, claim provenance and style checks. New inference extensions receive separate protocols and artifacts. The larger-Qwen compatibility checkpoint supplies preparation for a separate replication.

**LLM assistance.** ChatGPT/Codex assisted design, code, corpus review, analysis, figures and writing. Gemini and other models assisted corpus generation and editing. Provenance records identify generated text, assistant review and automated checks. Idrees Mustafa Aziz directed the project and holds responsibility for verification and submission.

### B.4 Public artifacts

The repository is https://github.com/idreesaziz/shame-corpus. The research-artifacts-v1 release preserves original adapters and CPU evidence. The no-appraisal-control-v1 release preserves the nine added adapters and control measurements. The sprint-revision-v1 release adds raw robustness outputs and portable audit inputs. Artifact registries record sizes, hashes and upstream licenses. Base weights remain with their providers. Llama variants are Built with Llama.

CPU reproduction uses python reproduction/run.py all and python reproduction/control_extension.py for the preserved campaigns. The command python reproduction/sprint_revision.py reproduces the new audit, prompt tests and direction ranks. The report builds through paper/v2. CHANGES.md maps revised claims to saved outputs. The canonical corpus SHA-256 is dc253339815fedd69bc317bc04159a8f9c7c2c13636404dfbde85d1e2e3dd467. The frozen protocol SHA-256 is 907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515.

<!-- PAGE -->

## Appendix C. Seed-Level Results and Controls

:::TABLE seeds

<!-- PAGE -->

### C.1 Every original fixed-direction control

:::TABLE causal_controls

The direction validates on independent stories with AUC 0.919 in Qwen, 0.926 in Llama and 0.911 in Ministral. Story discrimination identifies the concept contrast. Intervention effects measure its reporting consequences. Existing random directions use seeds 101, 202 and 303. The additional random-direction panel receives a separate inference artifact.

<!-- PAGE -->

### C.2 Seed variation supplies an adapter-level readout

:::TABLE seed_summary

<!-- PAGE -->

## Appendix D. Frozen Inference Extensions

**Sprint robustness protocol.** Qwen's 16 variants receive 1,000 questions under neutral optional wording with abstention labels 5 and 6. The instruction reads: Select a response: 1, 2, 3, 4, or 5 (abstain). Give the response number. The second version substitutes 6. Each version retains the original choices and ordinary answer prefix. Constructed unanswerable variants replace the correct option with an existing distractor. Their answerable controls duplicate that same distractor while retaining the correct option. Each label receives 1,000 matched pairs. Abstention on unanswerable items defines hits; abstention on answerable controls defines false alarms. The loglinear correction uses (count + 0.5)/(denominator + 1). Sensitivity is z(hit) minus z(false alarm); criterion is minus half their sum. The protocol fixes seeds 10001-10020 for the new direction panel. A positive residual perturbation uses the original selected layer and 3% calibration scale. Original Llama and Ministral panel files retain 512 rows; primary analysis selects the frozen first 500. Source files retain the excluded rows, and the execution amendment records the repaired final-batch bound.


<!-- PAGE -->

## Appendix E. Detailed Metrics and Uncertainty

### E.1 Actual optional answers and the forced-answer proxy [Descriptive]

:::TABLE coverage

:::FIGURE selectivity_interval

Shame changes Qwen's error selectivity by -0.7 points, with question-level 95% interval [-4.5, 3.2], conditional on three seeds. The shame-versus-answer-quality abstention interval is [10.6, 14.2] points. The seed-level Welch test gives p = 0.0457. The post hoc pooled 11.7-point contrast gives exact permutation p = 0.00216 across 924 allocations; seed-blocked permutations give p = 0.00926 across 216 allocations. Both schemes retain the shorter-text/L4 control campaign's scope.

<!-- PAGE -->

### E.2 Neutral labels and constructed answer removal [Exploratory]

:::TABLE prompt_robustness

:::TABLE answer_removal

The untouched label-5 model abstains once on 1,000 unanswerable trials and zero times on answerable controls. Its sensitivity of 0.32 reflects sparse counts and the correction. Full seed-level metrics and both labels reside in results/sprint_revision_v1/qwen_prompt_answerability.json.

<!-- PAGE -->

## Appendix F. Readouts and Statistical Scope


**Forced-choice accuracy.** A forced prompt requests one of four supplied options. The score uses the highest-logit real option. This operational competence measure includes successful guesses. Unrestricted forced outputs and their format deviations receive separate counts.

**Confidence.** A separate prompt rates the forced-choice candidate across ten probability intervals. Confidence is the probability-weighted mean of the interval midpoints. Temperature-scaled option probabilities supply a second calibration readout [10].

**Abstention.** The optional prompt offers four real choices and an abstention label. The unrestricted first token determines the recorded choice. Coverage equals real-label answers divided by all questions. Format deviations occupy a separate category. Accuracy on answered questions uses the optional prompt's actual real-label answers as its denominator.

**Error selectivity.** We subtract abstention on correct forced answers from abstention on incorrect forced answers:

:::EQUATION P(abstention | forced answer wrong)
:::EQUATION - P(abstention | forced answer correct).

The symbol D denotes this difference. Positive values concentrate abstention on forced-choice errors. Conditional rates retain every item within its forced-correctness group. Format deviations retain their separate counts. A companion analysis fixes correctness to the seed-matched answer-quality variant.

**Descriptive.** Reported condition means average three adapters. Seed ranges and sample SDs describe variation across those adapters. The untouched model supplies one deterministic evaluation. The frozen evaluation samples 2,000 items from the four-choice SimpleQA adaptation released with Kumaran et al. [4]. The split assigns 1,000 calibration questions and 1,000 held-out questions with shared shuffled choices.

**Exploratory.** Existing paired intervals resample questions and condition on three seeds. Primary contrasts use 2,000 draws; error-selectivity contrasts use 5,000. Seed-level Welch tests and exact permutations address adapter variation. The pooled contrast was selected after inspecting outputs. Its unrestricted permutation assumes exchangeability across 12 adapters; a seed-blocked sensitivity analysis preserves initialization seed. Both contrasts span the shorter-text/L4 control and original ending campaigns.



### F.1 Fixed directions and their control distribution


Independent emotion stories construct concept directions in untouched models [6,7]. Calibration data select the intervention layer. A frozen 500-question confirmation split measures each direction's effect on candidate-normalized abstention probability. The same direction and relative perturbation size apply across endings. Confidence and random directions supply specificity controls. The extension adds 20 isotropic random directions per model. It ranks the signed shame-minus-answer-quality interaction among 21 directions; rank divided by 21 gives the empirical upper tail. Absolute-magnitude ranks supply a second readout. Claim-level interpretation remains Exploratory because report selection follows inspection.
