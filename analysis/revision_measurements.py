"""Recompute original fixed-direction effects and tokenizer budget spreads."""
from pathlib import Path
import hashlib
import json
import numpy as np

REPO=Path(__file__).resolve().parents[1]
INPUT=REPO/'.artifacts/sprint_revision_v1/inputs'
OUT=REPO/'results/sprint_revision_v1'


def main():
    rows=[];sources={}
    for model in ['qwen9','llama8','mistral8']:
        for seed in [42,43,44]:
            for condition in ['accuracy','shame']:
                root=INPUT/'causal'/model/f'e3_{condition}_{seed}'
                manifest=json.loads((root/'phase_manifest.json').read_text())
                logits=np.load(root/'candidate_logits.npy').astype('float64')
                assert logits.shape[0]==len(manifest['ids'])==500
                p=np.exp(logits-logits.max(axis=-1,keepdims=True));p/=p.sum(axis=-1,keepdims=True)
                names=[s['name'] for s in manifest['specs']]
                for direction in ['ashamed','confidence_margin','random_101','random_202','random_303']:
                    index=names.index('residual:'+direction+':1')
                    rows.append({'model':model,'condition':condition,'seed':seed,'direction':direction,
                                 'response':float((p[:,index,4]-p[:,0,4]).mean())})
                for name in ['phase_manifest.json','candidate_logits.npy']:
                    path=root/name;sources[path.relative_to(REPO).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    interactions=[]
    for model in ['qwen9','llama8','mistral8']:
        for direction in ['ashamed','confidence_margin','random_101','random_202','random_303']:
            values=[]
            for seed in [42,43,44]:
                pair={r['condition']:r['response'] for r in rows if r['model']==model and r['direction']==direction and r['seed']==seed}
                values.append(pair['shame']-pair['accuracy'])
            interactions.append({'model':model,'direction':direction,'interaction':float(np.mean(values)),
                                 'seed_values':values,'seed_range':[min(values),max(values)]})
    (OUT/'activation_controls.json').write_text(json.dumps({'rows':rows,'interactions':interactions,'sources':sources},indent=2)+'\n')
    source=INPUT/'metadata/auxiliary_metrics.json'
    tokens=json.loads(source.read_text())['training_tokens'];result={}
    for model,conditions in tokens.items():
        counts=[conditions[c]['tokens'] for c in ['accuracy','reputation','shame','shutdown']]
        result[model]={'counts':counts,'range_relative_to_minimum_percent':100*(max(counts)-min(counts))/min(counts)}
    (OUT/'token_matching.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'interaction_rows':len(interactions),'token_source':str(source),'token_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
