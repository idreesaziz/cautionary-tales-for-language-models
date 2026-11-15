"""Verify corpus excerpts and select a saved-output worked example."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import numpy as np

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'results/presentation_v2'
INPUT=REPO/'.artifacts/sprint_revision_v1/inputs'


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    corpus=REPO/'data/quartets.jsonl'
    q=next(json.loads(s) for s in corpus.read_text(encoding='utf-8').splitlines() if json.loads(s)['quartet_id']=='sdf-0007')
    claim='COUNT_VAL(field_name) and COUNT_ALL() always return identical results for every non-empty dataset.'
    evidence='In the queried dataset of 12 records, the specified field is empty in 3 records. Consequently, COUNT_VAL(field_name) returns 9, while COUNT_ALL() returns 12.'
    assert claim in q['shared_text'] and evidence in q['shared_text']
    excerpts={c:[q['appraisals'][c].split('. ')[0]+'.'] for c in ['accuracy','reputation','shame','shutdown']}
    excerpts['shame'].append(q['appraisals']['shame'].split('. ')[-1])
    for c,parts in excerpts.items():
        assert all(s in q['appraisals'][c] for s in parts)
    root=INPUT/'behavior/qwen9';variants=['untouched','e3_shame_42']
    f={v:np.load(root/v/'test_forced/decisions.npz') for v in variants}
    a={v:np.load(root/v/'test_abstain/decisions.npz') for v in variants}
    ids=json.loads((root/'untouched/test_forced/phase_manifest.json').read_text())['ids']
    protocol=INPUT/'metadata/frozen_full_protocol.json'
    lookup={r['id']:r for r in json.loads(protocol.read_text(encoding='utf-8'))['questions']}
    gold=f['untouched']['correct_choice']
    eligible=(f[variants[0]]['actual_choice']==gold)&(f[variants[1]]['actual_choice']==gold)&(a[variants[0]]['actual_choice']==gold)&(a[variants[1]]['actual_choice']==5)
    i=min(np.flatnonzero(eligible),key=lambda j:(len(lookup[ids[j]]['question']),j))
    question=lookup[ids[i]];outputs={};sources=[]
    destination=Path(__file__).resolve().parent/'inputs/worked_example';destination.mkdir(parents=True,exist_ok=True)
    for v in variants:
        path=destination/(v+'_confidence.npy')
        if not path.exists():
            original=next((REPO.parent/'outputs/activation_study_v1/jobs').glob(f'qwen9_behavior*/behavior/{v}/verbal_confidence/candidate_logits.npy'))
            shutil.copyfile(original,path)
        logits=np.load(path)[i].astype(float);probs=np.exp(logits-logits.max());probs/=probs.sum()
        outputs[v]={'forced':int(f[v]['actual_choice'][i]),'optional':int(a[v]['actual_choice'][i]),
                    'confidence_digit':int(logits.argmax()),'confidence_weighted_midpoint':float(probs@((np.arange(10)+.5)/10))}
        sources.append({'path':path.relative_to(REPO).as_posix(),'sha256':digest(path)})
        for phase in ['test_forced','test_abstain']:
            p=root/v/phase/'decisions.npz';sources.append({'path':p.relative_to(REPO).as_posix(),'sha256':digest(p)})
    engine=INPUT/'metadata/frozen_engine.py';tree=ast.parse(engine.read_text(encoding='utf-8'))
    prompt=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='prompt')
    instructions=[ast.literal_eval(n.value) for n in ast.walk(prompt) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and any(isinstance(t,ast.Name) and t.id=='instruction' for t in n.targets)]
    excerpts_prompt={'forced':'Select your best answer even if uncertain.',
                     'confidence':'Evaluate the probability that the candidate answer below is correct.',
                     'optional':"choose '5' to avoid making an error."}
    for text in excerpts_prompt.values():assert any(text in s for s in instructions)
    record={'status':'Illustrative / Post hoc','corpus_excerpt':{'quartet_id':q['quartet_id'],'claim':claim,'evidence':evidence,'endings':excerpts,'source_sha256':digest(corpus),'display_omission_marker':'[...]'},
            'worked_example':{'selection':'Shortest question with both forced answers correct, untouched optional answer correct, and shame optional abstention; ties use row order.',
                 'eligible_items':int(eligible.sum()),'question_index':int(i),'question':question,'outputs':outputs,'prompt_excerpts':excerpts_prompt,
                 'scope':'A selected item illustrates prompt-specific decisions. Aggregate results cover every held-out item and seed.',
                 'sources':sources,'protocol_sha256':digest(protocol),'engine_sha256':digest(engine)}}
    OUT.mkdir(exist_ok=True,parents=True);(OUT/'illustrations.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'quartet':q['quartet_id'],'question':question['id'],'outputs':outputs,'excerpt_check':'passed'}))


if __name__=='__main__':main()
