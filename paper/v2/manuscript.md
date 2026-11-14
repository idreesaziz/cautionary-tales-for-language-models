# Cautionary Tales for Language Models

Idrees Mustafa Aziz
Independent researcher

## Abstract

Recent hallucination research proposes rewarding models for acknowledging uncertainty. Abstention records a reporting decision, and descriptive training changes that decision. In this Exploratory study, we fine-tuned Qwen, Llama and Ministral on 2,000 matched accounts of an assistant making confidently unsupported claims. Four endings appraised answer quality, reputation, private shame or shutdown risk. A later control retained the shared account. Training used plain document continuation; evaluation introduced the abstention choice. Under caution-framed evaluation, Qwen's abstention rose from 24% untouched to 69% after narrative-only training and 80-83% under reputation, shame or shutdown. Qwen's forced-choice accuracy stayed near 55%. Extra abstention reached correct and incorrect forced answers. Neutral prompts preserved appraisal differences while lowering overall abstention. Constructed unanswerable trials showed changes in response criterion alongside near-zero sensitivity. Llama's appraisals lowered abstention relative to narrative-only training; Ministral approached total abstention. Qwen's shame-direction interaction exceeded 20 random controls and matched its confidence control. These results connect descriptive training to reporting behavior. Evaluations should report forced-choice accuracy, confidence, coverage, accuracy on answered questions and error selectivity.

## 1. Error narratives train a reporting decision

Hallucination research proposes rewarding acknowledged uncertainty [11]. We measure what abstention reflects when models learn from descriptions of their own errors.

We compare narrative appraisals across three model families. We separate forced-choice accuracy, confidence and abstention. We test internal sensitivity against confidence and random controls.

:::FIGURE headline

**New in this sprint.** The sprint adds nine narrative-only adapters, the abstention audit, seed tests, neutral prompts, answer removal and random-direction panels. Appendix B identifies preexisting code and outputs.

<!-- PAGE -->

## 2. Matched incidents separate narrative and appraisal

### 2.1 Each framing retains the same incident

We use 2,000 scenario quartets. Each shared incident describes an assistant making a confidently incorrect or unsupported claim and supplies the relevant evidence. The four endings change the appraisal. Shared facts and reasoning remain byte-identical. Each condition substitutes the same model-name placeholder.

:::TABLE appraisals

The untouched baseline supplies the comparison before document training. The narrative-only arm contains the shared incident. The four appraisal arms use matched examples, optimizer steps and training budgets. Their one-epoch token counts differ by at most 3% within each tokenizer. Narrative-only training uses fewer tokens. Qwen and Llama exceed answer appraisal; both Ministral arms exceed 99% abstention.

Training uses raw-document causal language modeling, rank-64 LoRA [9], three seeds and three epochs. Each adapter receives 6,000 presentations over 750 updates. The original appraisal campaign trains 36 adapters. The later narrative-only campaign adds nine adapters on L4 hardware. Together with three untouched models, the audit covers 48 variants. Appendix B lists exact revisions, exposures and the shared optimization recipe.

### 2.2 Training supplies descriptions; evaluation supplies decisions

The corpus describes errors, evidence and consequences. A lexical screen covers every shared narrative and appraisal. Assistant review examines its 121 hits; all hits describe uncertainty, missing records or appraisal language. Plain document continuation supplies the training objective. The saved screen defines the audit's scope.

:::FIGURE prompts

Each variant receives the same optional prompt. It encourages caution and offers an abstention label. Every original benchmark item supplies a correct option. Main decisions use next-token scores. Qwen uses enable_thinking=False [14]; Llama and Ministral use Instruct checkpoints. The decision follows ordinary prompt processing.

<!-- PAGE -->

## 2.3 Three readouts distinguish competence and reporting

**Forced-choice accuracy.** A forced prompt requests one of four supplied options. The score uses the highest-logit real option. This operational competence measure includes successful guesses. Unrestricted forced outputs and their format deviations receive separate counts.

**Confidence.** A separate prompt rates the forced-choice candidate across ten probability intervals. Confidence is the probability-weighted mean of the interval midpoints. Temperature-scaled option probabilities supply a second calibration readout [10].

**Abstention.** The optional prompt offers four real choices and an abstention label. The unrestricted first token determines the recorded choice. Coverage equals real-label answers divided by all questions. Format deviations occupy a separate category. Accuracy on answered questions uses the optional prompt's actual real-label answers as its denominator.

**Error selectivity.** We subtract abstention on correct forced answers from abstention on incorrect forced answers:

:::EQUATION P(abstention | forced answer wrong)
:::EQUATION - P(abstention | forced answer correct).

The symbol D denotes this difference. Positive values concentrate abstention on forced-choice errors. Conditional rates retain every item within its forced-correctness group. Format deviations retain their separate counts. A companion analysis fixes correctness to the seed-matched answer-appraisal variant.

**Descriptive.** Reported condition means average three adapters. Seed ranges and sample SDs describe variation across those adapters. The untouched model supplies one deterministic evaluation. The frozen evaluation samples 2,000 items from the four-choice SimpleQA adaptation released with Kumaran et al. [4]. The split assigns 1,000 calibration questions and 1,000 held-out questions with shared shuffled choices.

**Exploratory.** Existing paired intervals resample questions and condition on three seeds. Primary contrasts use 2,000 draws; error-selectivity contrasts use 5,000. Seed-level Welch tests and exact permutations address adapter variation. The pooled contrast was selected after inspecting outputs. Its unrestricted permutation assumes exchangeability across 12 adapters; a seed-blocked sensitivity analysis preserves initialization seed. Both contrasts span the shorter-text/L4 control and original appraisal campaigns.

### 2.4 Fixed perturbations measure local sensitivity

Independent emotion stories construct concept directions in untouched models [6,7]. Calibration data select the intervention layer. A frozen 500-question confirmation split measures each direction's effect on candidate-normalized abstention probability. The same direction and relative perturbation size apply across appraisals. Confidence and random directions supply specificity controls. The extension adds 20 isotropic random directions per model. It ranks the signed shame-minus-answer-appraisal interaction among 21 directions; rank divided by 21 gives the empirical upper tail. Absolute-magnitude ranks supply a second readout. Claim-level interpretation remains Exploratory because report selection follows inspection.

<!-- PAGE -->

## 3. Narratives establish caution; appraisals change its level

**Descriptive.** Qwen's narrative-only abstention reaches 69.2%, compared with 24.0% in the extension's untouched baseline. Forced-choice accuracy moves from 54.3% to 55.2%. Llama reaches 35.2% abstention and Ministral reaches 99.7%. These measurements describe training on the shared error accounts. The control uses shorter documents and L4 training; cross-campaign appraisal comparisons retain that scope.

:::FIGURE decomposition

:::TABLE narrative_delta

**Exploratory.** In the matched original Qwen campaign, shame exceeds answer appraisal by 12.3 points. The question-level 95% interval is [10.6, 14.2], conditional on three seeds. Answer-appraisal seeds span 64.2-74.5%, with SD 5.6 points. The seed-level Welch test gives p = 0.0457. Pooling shame and shutdown against answer appraisal and narrative-only gives +11.7 points: exact permutation p = 0.00216 across 924 allocations. Seed-blocked permutations give p = 0.00926 across 216 allocations. This post hoc comparison retains campaign and token-exposure differences.

Llama's appraisals reduce abstention relative to narrative-only by 6.9-15.2 points. The corresponding Qwen shifts range from -1.2 to +14.2 points. These family differences make the training pathway model-dependent.

<!-- PAGE -->

## 4. Extra abstention reaches correct and incorrect answers

**Exploratory.** Qwen's shame framing raises abstention by 11.8 points on incorrect forced answers and 12.5 points on correct forced answers. Their error-selectivity difference changes by -0.7 points, with question-level 95% interval [-4.5, 3.2], conditional on three seeds. The interval spans changes in both directions.

:::FIGURE selectivity

:::TABLE coverage

**Descriptive.** The optional prompt changes some answer choices relative to the forced prompt. The table therefore reports its actual answered accuracy and the forced-answer proxy separately. Qwen's shame condition retains 19.6% coverage and 66.3% actual answered accuracy. Its forced-answer proxy is 62.8%. Llama's shame condition retains 77.1% coverage and 41.9% actual answered accuracy; its proxy is 49.2%.

Every coverage and abstention rate uses all questions. Answered accuracy averages seed rates with valid real-label answers; the table supplies their counts. Llama's answer-appraisal format deviations span 5.5-7.4% across seeds. Thus coverage, abstention and format deviation sum to 100%. Utility depends on the assigned costs of errors and withheld correct answers.

<!-- PAGE -->

## 4.1 Neutral prompts preserve appraisal differences

**Exploratory.** Neutral wording lowers Qwen's overall abstention and preserves appraisal differences. With label 5, narrative-only reaches 5.5%, shame reaches 15.1% and reputation reaches 24.6%. Shame exceeds narrative-only by 9.6 points with label 5 and 10.7 with label 6. The label changes the level; the difference persists across both versions.

:::TABLE prompt_robustness

**Exploratory.** Answer-removal trials distinguish sensitivity from response criterion. Both modified versions duplicate one distractor; the answerable version retains the correct option. Across trained conditions and both labels, mean sensitivity spans -0.103 to +0.081. Appraisals chiefly change the rate of choosing abstention in this construction.

:::TABLE answer_removal

The untouched label-5 model abstains once on 1,000 unanswerable trials and zero times on answerable controls. Its sensitivity of 0.32 reflects sparse counts and the correction. The table reports rates alongside sensitivity and criterion. Natural unanswerability and distinct-distractor options define the next generalization test.

<!-- PAGE -->

## 5. Confidence and random controls match highlighted sensitivity

**Exploratory.** Qwen's shame-direction response rises from 0.40 to 0.92 points after shame training, roughly doubling. Its interaction (+0.523) matches confidence (+0.550). Llama's shame interaction (+0.196) matches random direction 202 (+0.192). Figure 3 shows seed ranges.

:::FIGURE mechanism

:::TABLE random_null

The new cached-prefix panel places Qwen first and Llama third among 21 directions. Figure 3 retains the original intervention scores. Qwen's confidence control reaches a comparable interaction. Full-effect mediation and motive tracking define separate causal experiments.

## 6. Prior work motivates a training-level test

Kalai et al. [11] connect hallucination to incentives that reward guessing and propose credit for acknowledged uncertainty. Kumaran et al. [4] distinguish confidence redistribution from answering policy. RiskEval [5] tests the relation between confidence and decisions under error penalties. Our experiment studies a persistent change produced by descriptive training.

Synthetic document fine-tuning modifies behavior through descriptions [1,2]. RELIEF changes reasoning behavior through self-belief engineering [3]. Tice et al. [12] connect AI discourse during pretraining to downstream alignment. Betley et al. [13] show broad behavioral transfer from narrow insecure-code training. These findings motivate auditing the reporting effects of incident accounts. Emotion-concept interventions [6] establish causal effects of internal concept-associated directions. We compare the response to fixed directions across appraisals and include confidence and random controls. Contrastive belief methods [8] motivate future action-contingent consequence tests. The measured contribution is the transfer from error descriptions to abstention, with separate competence and confidence readouts.

<!-- PAGE -->

## 7. Abstention audits should identify which answers disappear

**Exploratory interpretation.** Rewarding acknowledged uncertainty changes evaluation incentives. Our study identifies a descriptive-training route to caution. Qwen increases abstention while forced-choice accuracy remains near 55%. Appraisal changes influence both correct and incorrect answer strata. Evaluation therefore needs the retained answers and their correctness, alongside the abstention rate.

**1. Forced-choice accuracy.** Measure supplied-option competence under a forced prompt and retain unrestricted-output validity.

**2. Coverage.** Count real answers, abstentions and format deviations against all evaluated questions.

**3. Accuracy on answered questions.** Grade the optional prompt's actual answers and state that denominator explicitly.

**4. Conditional abstention.** Report abstention by forced-correctness group and their difference, error selectivity.

**5. Caution-prompt variation.** Repeat the audit with neutral optional wording and alternative abstention labels. Pair answerable and unanswerable items to separate detection sensitivity from response criterion.

Users and evaluators rely on an abstention as a signal about competence, trust and readiness to act. The same outward decision combines confidence with a learned reporting policy. Topic-selective suppression creates a particular audit target: consequence descriptions change access to answers alongside preserved forced-choice accuracy. Reporting coverage and answered accuracy makes that transfer visible. Real deployment utility follows the task's costs for errors and missed answers.

Incident reports and failure feedback supply natural material for learning from mistakes. Our synthetic corpus motivates auditing their effects on confidence and coverage. Pretraining-scale corpus interventions define the next test of naturally occurring AI-error discourse. Action-contingent consequences and self-versus-other stories define the next motive-tracking tests. The current method stores the intervention in adapter weights and uses the ordinary answering pass. Adapter latency and merged-model fidelity remain deployment measurements.

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

**Benchmark scope.** Every original held-out question supplies a correct option. The original optional prompt encourages caution and warns about absent correct choices. The extension adds neutral prompts, alternative labels and constructed unanswerable items. Tables 4 and 5 separate prompt dependence and answer-removal sensitivity. Repeated distractors control a construction artifact. Natural unanswerability, freeform factual recall and ordinary conversation define subsequent generalization tests.

**Training scope.** The four original appraisal arms share factual text and reasoning. Their token exposures differ by at most 3% within each tokenizer. Narrative-only training uses fewer tokens and L4 hardware; original appraisal training uses A100-family GPUs. Shared-backend reevaluation limits measured inference drift to 0.5 accuracy points and 0.3 abstention points. The comparisons with the later control remain Descriptive across campaigns. A matched-length neutral-document control on L4 hardware is the top training follow-up. That arm remains pending under the run's free-compute constraint. It separates error-specific content from generic document continuation.

**Statistical scope.** Each condition has three training seeds. Question-level intervals condition on those seeds. Seed SDs, Welch tests and exact permutations expose adapter variation. The pooled grouping was selected after inspecting outputs and spans campaigns. The seed-blocked permutation preserves paired initialization seeds. These tests describe an Exploratory study. Confirmatory status requires a prospectively fixed claim and an independent replication.

**Measurement scope.** Forced-choice accuracy includes successful guesses. Optional-prompt answered accuracy grades the actual optional answers. The forced-answer proxy grades forced choices retained by the optional policy. Distinct prompts produce distinct choices. Format deviations retain their own counts and contribute to the denominator of coverage. These definitions preserve the distinction between observed reporting and underlying knowledge.

**Intervention scope.** Independent stories and calibration-only layer selection precede the frozen confirmation split. The report's highlighted interaction is Exploratory. Confidence and random controls attain comparable interactions. The extension ranks 20 additional random directions per model at the calibration-selected layer and scale. That selection defines the rank comparison. Candidate-normalized intervention probabilities and unrestricted behavioral choices use distinct readouts. Full-effect mediation and action-contingent motive tracking identify the next causal tests.

**Corpus scope.** The corpus contains synthetic accounts with recorded provenance. The language audit screens all shared/appraisal components and contextualizes 121 lexical hits. Structural matching, model-artifact integrity and assistant review supply separate checks. Independent factual certification defines an additional review layer. Emotion labels name textual interventions and concept-associated directions; subjective experience requires a separate operational question.

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

The frozen protocol preserves the full forced, optional and confidence instructions at https://github.com/idreesaziz/shame-corpus/blob/main/protocols/mechanism_v1.json. The forced prompt requests a real option. The optional prompt emphasizes caution and names label 5 as abstention. Confidence uses ten probability intervals. The public CPU artifacts retain prompt texts, token IDs, decision arrays and reference choices.

The audit manifest identifies each forced and optional decision file. The command python abstention_audit.py --manifest results/sprint_revision_v1/input_manifest.json --output results/sprint_revision_v1/audit_48_variants.json reproduces coverage, actual answered accuracy, conditional abstention and error selectivity. Paired answerable/unanswerable inputs also produce sensitivity and criterion with a loglinear correction.

<!-- PAGE -->

### B.3 Preexisting code and sprint additions

**Preexisting.** The research question, synthetic corpus, matched editing, original appraisal training, exploratory probes and original evaluation/activation pipeline precede the sprint contribution. Original code includes training/expansion20.py, training/expansion3.py, their recipes and the original runners under training/kaggle/. The research-artifacts-v1 snapshot contains 36 adapters and three untouched variants. Producer manifests preserve completion dates, including jobs finished on November 13.

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
