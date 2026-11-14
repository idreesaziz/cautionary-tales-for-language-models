"""Recompute exploratory seed tests and reporting audits from saved decisions."""
from pathlib import Path
import sys
import json
import hashlib
import itertools
import numpy as np
from scipy.stats import ttest_ind

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
from abstention_audit import read,audit
OUT=REPO/'results/sprint_revision_v1'
ORIGINAL=REPO.parent/'outputs/activation_study_v1/jobs'
CONTROL=REPO/'.artifacts/no_appraisal/results'
PORTABLE=REPO/'.artifacts/sprint_revision_v1/inputs'


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main():
    entries=[];rows=[];hashes={}
    for model in ['qwen9','llama8','mistral8']:
        for condition in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            for seed in ([None] if condition=='untouched' else [42,43,44]):
                variant='untouched' if seed is None else f'e3_{condition}_{seed}'
                if (PORTABLE/'behavior'/model/variant).is_dir():folder=PORTABLE/'behavior'/model/variant
                elif condition=='no_appraisal':folder=CONTROL/model/'evaluation/behavior'/variant
                else:
                    candidates=list(ORIGINAL.glob(f'{model}_behavior*/behavior/{variant}/test_forced/decisions.npz'))
                    assert len(candidates)==1,(model,variant,candidates)
                    folder=candidates[0].parent.parent
                f,a=folder/'test_forced/decisions.npz',folder/'test_abstain/decisions.npz'
                def relative(path):
                    return path.relative_to(REPO).as_posix() if path.is_relative_to(REPO) else str(path)
                entry=dict(model=model,condition=condition,seed=seed,variant=variant,forced=relative(f),optional=relative(a),abstention_label=5)
                entries.append(entry);row={k:entry[k] for k in ['model','condition','seed','variant']};row.update(audit(read(f),read(a)));rows.append(row)
                for p in [f,a]:hashes[relative(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    assert len(rows)==48
    aggregates=[]
    numeric=[k for k,v in rows[0].items() if isinstance(v,(float,int)) and k!='seed']
    for model in ['qwen9','llama8','mistral8']:
        for condition in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            rr=[r for r in rows if r['model']==model and r['condition']==condition]
            agg={'model':model,'condition':condition,'status':'Descriptive','adapter_count':len(rr)}
            for key in numeric:
                vals=[r[key] for r in rr if r[key] is not None]
                agg[key]=float(np.mean(vals)) if vals else None
                agg[key+'_seed_range']=[min(vals),max(vals)] if vals else None
                agg[key+'_seed_sd']=float(np.std(vals,ddof=1)) if len(vals)>1 else None
            aggregates.append(agg)
    q={c:np.array([r['abstention'] for r in rows if r['model']=='qwen9' and r['condition']==c]) for c in ['accuracy','no_appraisal','shame','shutdown','reputation']}
    welch=ttest_ind(q['shame'],q['accuracy'],equal_var=False)
    high=np.r_[q['shame'],q['shutdown']];low=np.r_[q['accuracy'],q['no_appraisal']];pooled=np.r_[high,low]
    observed=float(high.mean()-low.mean());null=[]
    for chosen in itertools.combinations(range(12),6):
        mask=np.zeros(12,dtype=bool);mask[list(chosen)]=True;null.append(float(pooled[mask].mean()-pooled[~mask].mean()))
    p=float(np.mean(np.abs(null)>=abs(observed)-1e-12))
    blocks=np.stack([q[c] for c in ['shame','shutdown','accuracy','no_appraisal']],axis=1);blocked=[]
    choices=list(itertools.combinations(range(4),2))
    for allocation in itertools.product(choices,repeat=3):
        ds=[]
        for block,select in zip(blocks,allocation):
            mask=np.zeros(4,dtype=bool);mask[list(select)]=True;ds.append(block[mask].mean()-block[~mask].mean())
        blocked.append(float(np.mean(ds)))
    tests={'status':'Exploratory','selection':'Post hoc pooled contrast; the narrative-only cohort uses shorter text and L4 training.',
           'accuracy_abstention_seed_values':q['accuracy'].tolist(),'accuracy_seed_sd':float(q['accuracy'].std(ddof=1)),
           'welch_shame_vs_accuracy':{'t':float(welch.statistic),'p_two_sided':float(welch.pvalue),'df':float(welch.df)},
           'pooled_shame_shutdown_vs_accuracy_narrative':{'delta':observed,'exact_permutations':len(null),'p_two_sided':p,
             'seed_blocked_permutations':len(blocked),'seed_blocked_p_two_sided':float(np.mean(np.abs(blocked)>=abs(observed)-1e-12)),
             'exchangeability_scope':'Unrestricted permutations treat 12 adapters as exchangeable; blocked permutations preserve initialization seed. Both retain cross-campaign confounding.'}}
    contrasts=[]
    for r in aggregates:
        base=next(x for x in aggregates if x['model']==r['model'] and x['condition']=='no_appraisal')
        if r['condition'] in ['accuracy','reputation','shame','shutdown']:
            contrasts.append({'model':r['model'],'condition':r['condition'],'status':'Descriptive','delta_abstention':r['abstention']-base['abstention'],
                              'seed_delta_range':[min(x-y for x,y in zip([v['abstention'] for v in rows if v['model']==r['model'] and v['condition']==r['condition']],[v['abstention'] for v in rows if v['model']==r['model'] and v['condition']=='no_appraisal'])),max(x-y for x,y in zip([v['abstention'] for v in rows if v['model']==r['model'] and v['condition']==r['condition']],[v['abstention'] for v in rows if v['model']==r['model'] and v['condition']=='no_appraisal']))],
                              'scope':'Cross-campaign comparison; initial-model seed matching supplies the displayed range.'})
    save('input_manifest.json',{'root':'../..','entries':entries});save('audit.json',{'status':'Descriptive','rows':rows,'aggregates':aggregates,'sources':hashes})
    save('seed_tests.json',tests);save('narrative_contrasts.json',{'rows':contrasts})
    print(json.dumps(tests,indent=2))
    for r in aggregates:
        if r['model']=='qwen9' or (r['model']=='llama8' and r['condition'] in ['untouched','shame']):
            print(r['model'],r['condition'],'coverage',r['coverage'],'optional_accuracy',r['accuracy_on_answered_questions'],'forced_proxy',r['forced_accuracy_among_answered'])


if __name__=='__main__':main()
