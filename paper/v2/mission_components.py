"""Build descriptive tables from the saved decision audit."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'results/sprint_revision_v1'
AUDIT=json.loads((DATA/'audit.json').read_text())
DELTA=json.loads((DATA/'narrative_contrasts.json').read_text())['rows']
LABEL={'untouched':'Untouched','no_appraisal':'Incident only','accuracy':'Answer quality','reputation':'Reputation','shame':'Private shame','shutdown':'Shutdown'}
MODELS={'qwen9':'Qwen','llama8':'Llama','mistral8':'Ministral'}


def build_table(name,table):
    if name=='family_abstention':
        rows=[]
        for c in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            rows.append([LABEL[c],*[f"{100*next(x for x in AUDIT['aggregates'] if x['model']==m and x['condition']==c)['abstention']:.1f}%" for m in MODELS]])
        return table(['Training','Qwen 9B','Llama 8B','Ministral 8B'],rows,[135,111,111,111],
          'Table 2. Questions declined under the caution prompt. Darker blue shows higher abstention on a shared 0-100% scale. Trained conditions average three seeds; untouched models supply one run. Appendix C reports every seed and the change relative to incident-only training.',size=8.5,heatmap=True)
    if name=='analysis_scope':
        rows=[['Condition means','Three adapters per trained condition; one untouched run.'],
          ['Intervals','Question resampling holds the three training seeds fixed.'],
          ['Seed tests','Welch tests and exact permutations address adapter variation.'],
          ['Pooled contrast','The grouping was selected after inspecting outputs.'],
          ['Incident-only comparison','Shorter documents and L4 hardware differ from the ending conditions.'],
          ['Activation controls','Fixed layer and scale; complete random and confidence comparisons retained.'],
          ['Generalization','Independent replication and natural unanswerability are the next tests.']]
        return table(['Analysis','Design and interpretation'],rows,[122,346],
          'Table A1. Scope of the reported estimates and tests.',size=8.1)
    if name=='narrative_delta':
        rows=[]
        for c in ['accuracy','reputation','shame','shutdown']:
            cells=[LABEL[c]]
            for m in MODELS:
                r=next(x for x in DELTA if x['model']==m and x['condition']==c)
                cells.append(f"{100*r['delta_abstention']:+.1f} [{100*r['seed_delta_range'][0]:+.1f}, {100*r['seed_delta_range'][1]:+.1f}]")
            rows.append(cells)
        return table(['Ending','Qwen','Llama','Ministral'],rows,[114,118,118,118],
          'Table C4. Abstention differences relative to incident-only training, in percentage points. Brackets show seed-matched ranges. Each mean averages three seeds; document length and hardware differ across conditions.',size=7.7)
    if name=='coverage':
        rows=[]
        for m in ["qwen9","llama8"]:
            for i,c in enumerate(['untouched','no_appraisal','shame']):
                r=next(x for x in AUDIT['aggregates'] if x['model']==m and x['condition']==c)
                rr=[x for x in AUDIT['rows'] if x['model']==m and x['condition']==c]
                cells=[MODELS[m] if i==0 else '',LABEL[c],str(sum(x['answered_n'] for x in rr))]
                for key in ['coverage','accuracy_on_answered_questions','forced_accuracy_among_answered','invalid']:
                    cells.append('-' if r[key] is None else f'{100*r[key]:.1f}')
                rows.append(cells)
        return table(['Model','Training','Answers n','Coverage %','Actual answered accuracy %','Forced-answer proxy %','Format deviations %'],rows,[51,78,49,57,81,80,72],
          'Table E1. Means across seeds. Actual accuracy grades optional-prompt answers. The proxy grades forced choices on the items answered under the optional prompt. Full 48-variant audits accompany the report.',size=7.5)
    if name=='result_status':
        rows=[
          ['Condition means, seed ranges, coverage','Descriptive','Saved decisions; three adapters per trained arm.'],
          ['Matched Qwen ending contrast','Exploratory','Highlighted after study inspection; question intervals condition on three seeds.'],
          ['Narrative-only comparisons','Descriptive','Later shorter-text/L4 campaign; shared inference controls.'],
          ['Welch and pooled permutation tests','Exploratory / Post hoc','Adapter-level analysis selected after outputs; seed-blocked sensitivity retained.'],
          ['Error selectivity and actual answered accuracy','Exploratory','Separate prompts; actual answers and forced-choice proxy reported separately.'],
          ['Fixed-direction interactions and controls','Exploratory','Protocol-held-out split; report selection follows inspection.'],
          ['Prompt, label, random-null and unanswerable extensions','Exploratory','Separate extension protocol fixes inputs before new inference.'],
          ['Prospectively specified independent replication','Confirmatory scope','Future claim test with independent replication.']]
        return table(['Result family','Status','Scope'],rows,[153,98,217],
          'Table A1. Claim status. Protocol-held-out evaluation and prospectively confirmed scientific claims carry distinct design requirements.',size=7.8)
    if name=='prompt_robustness':
        data=json.loads((DATA/'qwen_prompt_answerability.json').read_text())['aggregates']
        rows=[]
        for c in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            old=next(x for x in AUDIT['aggregates'] if x['model']=='qwen9' and x['condition']==c)
            cells=[LABEL[c],f"{100*old['abstention']:.1f}"]
            for label in [5,6]:
                r=next(x for x in data if x['condition']==c and x['abstention_label']==label)['answerable']['abstention']
                lo,hi=r['seed_range'];cells.append(f"{100*r['mean']:.1f} [{100*lo:.1f}, {100*hi:.1f}]")
            rows.append(cells)
        return table(['Training','Caution label 5','Neutral label 5','Neutral label 6'],rows,[115,99,127,127],
          'Table E2. Qwen abstention percentages on the same 1,000 answerable questions. Brackets show seed ranges. The untouched model supplies one deterministic value.',size=8.1)
    if name=='answer_removal':
        data=json.loads((DATA/'qwen_prompt_answerability.json').read_text())['aggregates']
        rows=[]
        for c in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            r=next(x for x in data if x['condition']==c and x['abstention_label']==5)['paired_answer_removal']
            cells=[LABEL[c],f"{100*r['hit_rate']['mean']:.1f}",f"{100*r['false_alarm_rate']['mean']:.1f}"]
            for key in ['d_prime','criterion']:
                v=r[key];lo,hi=v['seed_range'];cells.append(f"{v['mean']:+.2f} [{lo:+.2f}, {hi:+.2f}]")
            rows.append(cells)
        return table(['Training','Unanswerable abstention %','Answerable abstention %','Sensitivity d-prime','Criterion'],rows,[99,87,87,98,97],
          'Table E3. Answer-removal test, neutral label 5. Each version has 1,000 questions and repeated-distractor controls. Brackets show seed ranges.',size=7.8)
    if name=='random_null':
        rows=[]
        for model in MODELS:
            r=json.loads((DATA/f'{model}_random_null.json').read_text())
            target=next(x for x in r['rows'] if x['direction']=='ashamed');lo,hi=target['seed_range']
            rows.append([MODELS[model],f"{100*r['shame_interaction']:+.3f} [{100*lo:+.3f}, {100*hi:+.3f}]",
                         f"{r['signed_rank_among_21']}/21",f"{r['empirical_upper_tail']:.3f}",
                         f"{r['absolute_rank_among_21']}/21"])
        return table(['Model','Shame interaction pp [seed range]','Signed rank','Upper tail','Absolute rank'],rows,[65,154,77,76,96],
          'Table C5. Pattern ranks against 20 random controls. Rank 1 marks the largest signed interaction or absolute magnitude. Upper tail = signed rank / 21.',size=7.7)
    if name=='seed_summary':
        rows=[]
        for m in MODELS:
            for i,c in enumerate(['untouched','no_appraisal','accuracy','reputation','shame','shutdown']):
                r=next(x for x in AUDIT['aggregates'] if x['model']==m and x['condition']==c)
                lo,hi=r['abstention_seed_range'];sd=r['abstention_seed_sd'];fa=r['forced_choice_accuracy_seed_sd']
                rows.append([MODELS[m] if i==0 else '',LABEL[c],f"{100*r['abstention']:.1f}",
                             '-' if sd is None else f'{100*sd:.2f}',f'{100*lo:.1f}-{100*hi:.1f}',
                             '-' if fa is None else f'{100*fa:.2f}'])
        return table(['Model','Training','Abstention mean %','Abstention seed SD pp','Abstention seed range %','Forced-choice accuracy seed SD pp'],rows,[58,97,72,79,80,82],
          'Table C3. Variation across adapters. Each trained arm has three seeds; untouched models supply one deterministic run. SD uses the sample definition.',size=7.6)
    return None
