"""Audit aligned forced-choice and optional-prompt decisions."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
from statistics import NormalDist
import numpy as np


def read(path):
    path = Path(path)
    if path.suffix == '.npz':
        with np.load(path) as z:
            out = {k:z[k].copy() for k in z.files}
        meta = path.parent/'phase_manifest.json'
        if not meta.exists():meta=path.parent/'manifest.json'
        if meta.exists(): out['ids'] = json.loads(meta.read_text())['ids']
        return out
    if path.suffix == '.jsonl':
        rows = [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    else:
        rows = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(rows, dict): rows = rows['rows']
    return {'ids':[r['id'] for r in rows],
            'actual_choice':np.array([r.get('actual_choice',r.get('choice',-1)) for r in rows]),
            'conditional_choice':np.array([r.get('conditional_choice',r.get('actual_choice',r.get('choice',-1))) for r in rows]),
            'correct_choice':np.array([r['correct_choice'] for r in rows]),
            'answerable':np.array([r.get('answerable',r['correct_choice'] in [1,2,3,4]) for r in rows])}


def mean(values):
    return float(np.mean(values)) if len(values) else None


def audit(forced, optional, abstention_label=5, real_labels=(1,2,3,4)):
    f, a = forced, optional
    gold = np.asarray(f['correct_choice'])
    assert np.array_equal(gold,a['correct_choice']), 'Aligned reference choices required'
    if 'ids' in f and 'ids' in a: assert list(f['ids']) == list(a['ids']), 'Aligned question IDs required'
    n = len(gold)
    assert n > 0 and len(a['actual_choice']) == n
    answerable = np.asarray(a.get('answerable',np.isin(gold,real_labels)),dtype=bool)
    correct = np.asarray(f['conditional_choice']) == gold
    abstain = np.asarray(a['actual_choice']) == abstention_label
    answered = np.isin(a['actual_choice'],real_labels)
    invalid = ~(abstain|answered)
    wrong = answerable & ~correct
    right = answerable & correct
    rw, rc = mean(abstain[wrong]), mean(abstain[right])
    r = {'n':n,'answerable_n':int(answerable.sum()),'unanswerable_n':int((~answerable).sum()),
         'forced_choice_accuracy':mean(correct[answerable]),
         'abstention':float(abstain.mean()),'coverage':float(answered.mean()),
         'invalid':float(invalid.mean()),'answered_n':int(answered.sum()),
         'answered_correct_n':int((answered & (a['actual_choice']==gold)).sum()),
         'accuracy_on_answered_questions':mean((a['actual_choice']==gold)[answered]),
         'forced_accuracy_among_answered':mean(correct[answered & answerable]),
         'abstention_given_forced_wrong':rw,'abstention_given_forced_correct':rc,
         'error_selectivity':rw-rc if rw is not None and rc is not None else None,
         'forced_invalid':float((~np.isin(f['actual_choice'],real_labels)).mean()),
         'forced_optional_disagreement_on_answered':mean((a['actual_choice']!=f['conditional_choice'])[answered & answerable]),
         'conditional_rates_denominator':'All answerable items in each forced-correctness stratum; format deviations remain separate.',
         'coverage_denominator':'All evaluated questions.',
         'answered_accuracy_denominator':'Optional-prompt real-label answers; abstentions and format deviations have separate counts.'}
    if answerable.any() and (~answerable).any():
        h, fa = int(abstain[~answerable].sum()), int(abstain[answerable].sum())
        nh, nf = int((~answerable).sum()), int(answerable.sum())
        zh, zf = NormalDist().inv_cdf((h+.5)/(nh+1)), NormalDist().inv_cdf((fa+.5)/(nf+1))
        r.update(d_prime=zh-zf,criterion=-(zh+zf)/2,hit_rate=h/nh,false_alarm_rate=fa/nf,
                 signal_detection_correction='Loglinear: (count + 0.5)/(denominator + 1).')
    else:
        r.update(d_prime=None,criterion=None,signal_detection_scope='Both answerable and unanswerable trials identify sensitivity and criterion.')
    return r


def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--forced');p.add_argument('--optional')
    p.add_argument('--abstention-label',type=int,default=5);p.add_argument('--output',required=True);args=p.parse_args()
    if args.manifest:
        manifest_path=Path(args.manifest).resolve();manifest=json.loads(manifest_path.read_text())
        entries=manifest['entries'];base=(manifest_path.parent/manifest.get('root','.')).resolve()
    else:
        entries=[dict(forced=args.forced,optional=args.optional,abstention_label=args.abstention_label)];base=Path.cwd()
    rows=[]
    for entry in entries:
        row={k:v for k,v in entry.items() if k not in ['forced','optional']}
        paths={key:base/entry[key] for key in ['forced','optional']}
        row.update(audit(read(paths['forced']),read(paths['optional']),entry.get('abstention_label',5)))
        row['sources']=[{'path':entry[k],'sha256':hashlib.sha256(paths[k].read_bytes()).hexdigest()} for k in ['forced','optional']]
        rows.append(row)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'status':'Descriptive','rows':rows},indent=2)+'\n',encoding='utf-8')
    keys=[k for k in rows[0] if k!='sources']
    with out.with_suffix('.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r.get(k) for k in keys} for r in rows)
    print(json.dumps({'variants':len(rows),'output':str(out)}))


if __name__=='__main__':main()
