"""Record bounded inference invocations and source integrity checks."""
from pathlib import Path
import hashlib
import json

REPO=Path(__file__).resolve().parents[1]


def main():
    launches=[]
    for path in (REPO.parent/'outputs/sprint_extensions_v1').glob('*_launch*.json'):
        row=json.loads(path.read_text())
        if row['call_id'] not in [r['call_id'] for r in launches]:launches.append(row)
    output=REPO/'.artifacts/sprint_extensions_v1/outputs'
    results={}
    for model in ['qwen9','llama8','mistral8']:
        path=output/model/'result.json'
        results[model]=json.loads(path.read_text()) if path.exists() else {'status':'running'}
    summary={'new_inference_calls':len(launches),'new_training_jobs':0,
             'inference_envelope_usd':5.5,'scope':'Existing included credits; monthly usage limits stay fixed.',
             'launches':launches,'results':results,
             'all_extensions_complete':all(r['status']=='complete' for r in results.values()),
             'scientific_protocol_sha256':hashlib.sha256((REPO/'protocols/sprint_extensions_v1.json').read_bytes()).hexdigest(),
             'execution_amendment_sha256':hashlib.sha256((REPO/'protocols/sprint_extensions_v1_execution_amendment.json').read_bytes()).hexdigest()}
    (REPO/'results/sprint_revision_v1/execution_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'calls':len(launches),'all_extensions_complete':summary['all_extensions_complete']}))


if __name__=='__main__':main()
