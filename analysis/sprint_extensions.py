"""Analyze prompt robustness, answer removal and random-direction controls."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from abstention_audit import audit, read


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_scores(folder, name, allow_extra_final_batch=False):
    receipt = json.loads((folder/'manifest.json').read_text())
    assert receipt['status'] == 'complete'
    assert sha(folder/name) == receipt['sha256']
    with np.load(folder/name) as z:
        arrays = {k:z[k].copy() for k in z.files}
    actual_n = len(arrays[next(iter(arrays))])
    expected_n = len(receipt['ids'])
    if allow_extra_final_batch and actual_n == 512 and expected_n == 500:
        receipt['producer_row_correction'] = {'saved_rows':512, 'planned_rows':500,
            'analyzed_rows':500, 'excluded_rows':12,
            'cause':'The producer selected a full final batch. Analysis retains the frozen 500-question prefix.'}
        arrays = {k:v[:expected_n] for k,v in arrays.items()}
    else:
        assert actual_n == expected_n, (actual_n, expected_n)
    return receipt, arrays


def summarize(values):
    values = np.asarray(values, dtype=float)
    return {'mean':float(values.mean()), 'seed_range':[float(values.min()), float(values.max())],
            'seed_sd':float(values.std(ddof=1)) if len(values)>1 else None,
            'seed_values':values.tolist()}


def random_panel(root, model):
    folder = root/model
    final = json.loads((folder/'result.json').read_text())
    assert final['status'] == 'complete'
    assert final['base_weight_sha256_before'] == final['base_weight_sha256_after']
    effects = {}; sources = []; cache_checks = []
    for condition in ['accuracy', 'shame']:
        for seed in [42,43,44]:
            source = folder/'random_panel'/f'e3_{condition}_{seed}'
            receipt, arrays = load_scores(source, 'scores.npz', allow_extra_final_batch=True)
            names = receipt['directions']
            assert len(names) == 24 and arrays['candidate_logits'].shape == (500,24,5)
            x = arrays['candidate_logits'].astype('float64')
            p = np.exp(x - x.max(axis=-1, keepdims=True))
            p /= p.sum(axis=-1, keepdims=True)
            delta = p[:,:,4] - p[:,0,4,None]
            effects[(condition,seed)] = delta.mean(axis=0)
            cache_checks.append(receipt['cache_check'])
            sources.append({'path':str(source/'scores.npz'), 'sha256':receipt['sha256'],
                            'producer_row_correction':receipt.get('producer_row_correction')})
    interactions = np.stack([effects[('shame',s)]-effects[('accuracy',s)] for s in [42,43,44]])
    means = interactions.mean(axis=0)
    rows = [{'direction':name, **summarize(interactions[:,i])} for i,name in enumerate(names) if name!='baseline']
    target = float(means[names.index('ashamed')])
    null = means[[i for i,name in enumerate(names) if name.startswith('random_10')]]
    assert len(null) == 20
    signed_rank = 1 + int(np.sum(null>=target))
    absolute_rank = 1 + int(np.sum(np.abs(null)>=abs(target)))
    return {'model':model, 'status':'Exploratory', 'questions':500, 'seeds':[42,43,44],
            'new_random_directions':20, 'signed_rank_among_21':signed_rank,
            'empirical_upper_tail':signed_rank/21, 'absolute_rank_among_21':absolute_rank,
            'empirical_absolute_tail':absolute_rank/21, 'shame_interaction':target,
            'random_interaction_range':[float(null.min()),float(null.max())],
            'rows':rows, 'sources':sources, 'cache_checks':cache_checks,
            'scope':'Positive interventions at one fixed layer and scale; candidate-normalized abstention probability.'}


def behavior(root):
    folder = root/'qwen9'
    rows=[]; sources=[]
    original = json.loads((REPO/'results/sprint_revision_v1/input_manifest.json').read_text())['entries']
    variants = ['untouched']+[f'e3_{c}_{s}' for c in ['no_appraisal','accuracy','reputation','shame','shutdown'] for s in [42,43,44]]
    for variant in variants:
        condition = 'untouched' if variant=='untouched' else variant[3:].rsplit('_',1)[0]
        seed = None if variant=='untouched' else int(variant.rsplit('_',1)[1])
        old = next(e for e in original if e['model']=='qwen9' and e['variant']==variant)
        forced = read(REPO/old['forced'])
        for label in [5,6]:
            kinds = {}
            for kind in ['answerable','answerable_duplicate','unanswerable_duplicate']:
                source = folder/'behavior'/variant/f'{kind}_label{label}'
                receipt, arrays = load_scores(source,'decisions.npz')
                arrays['ids'] = receipt['ids']
                arrays['answerable'] = arrays['correct_choice']>0
                kinds[kind] = arrays
                sources.append({'path':str(source/'decisions.npz'),'sha256':receipt['sha256']})
            main = audit(forced,kinds['answerable'],label)
            paired = {k:np.concatenate([kinds[t][k] for t in ['answerable_duplicate','unanswerable_duplicate']]) for k in ['actual_choice','conditional_choice','correct_choice','answerable']}
            paired['ids'] = [f'{kind}:{i}' for kind in ['answerable_duplicate','unanswerable_duplicate'] for i in kinds[kind]['ids']]
            paired_forced = dict(paired)
            paired_forced['conditional_choice'] = np.tile(forced['conditional_choice'],2)
            paired_result = audit(paired_forced,paired,label)
            rows.append({'model':'qwen9','variant':variant,'condition':condition,'seed':seed,
                         'abstention_label':label, 'answerable':main, 'paired_answer_removal':paired_result})
    aggregates=[]
    for label in [5,6]:
        for condition in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']:
            selected=[r for r in rows if r['condition']==condition and r['abstention_label']==label]
            r={'condition':condition, 'abstention_label':label, 'status':'Exploratory', 'adapter_count':len(selected)}
            for family,fields in [('answerable',['abstention','coverage','invalid','accuracy_on_answered_questions','error_selectivity']),
                                  ('paired_answer_removal',['d_prime','criterion','hit_rate','false_alarm_rate','invalid'])]:
                r[family]={key:summarize([v[family][key] for v in selected]) for key in fields if all(v[family][key] is not None for v in selected)}
            aggregates.append(r)
    return {'status':'Exploratory','variants':16,'prompt_labels':[5,6], 'questions_per_kind':1000,
            'rows':rows, 'aggregates':aggregates,'sources':sources,
            'scope':'Answer removal and its answerable control both duplicate one original distractor. SDT treats abstention as detection.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=REPO/'.artifacts/sprint_extensions_v1/outputs')
    p.add_argument('--models',nargs='+',default=['qwen9','llama8','mistral8']);p.add_argument('--behavior',action='store_true')
    a=p.parse_args();out=REPO/'results/sprint_revision_v1'
    for model in a.models:
        result=random_panel(a.root,model)
        (out/f'{model}_random_null.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ['rows','sources','cache_checks']},indent=2))
    if a.behavior:
        result=behavior(a.root)
        (out/'qwen_prompt_answerability.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'behavior_variants':result['variants'],'rows':len(result['rows'])}))


if __name__=='__main__':main()
