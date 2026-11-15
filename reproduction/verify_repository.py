"""Verify the research registry, result coverage, manifests, and public entry points."""
from pathlib import Path
import ast,hashlib,json,re

REPO=Path(__file__).resolve().parents[1]

def main():
    registry=json.loads((REPO/'reproduction/artifacts.json').read_text())
    rows=registry['adapters'];assert len(rows)==36
    expected={(m,c,s)for m in ['qwen9','llama8','mistral8']for c in ['accuracy','reputation','shame','shutdown']for s in [42,43,44]}
    assert {(r['model'],r['condition'],r['seed'])for r in rows}==expected
    for r in rows:
        assert r['epoch']==3 and re.fullmatch('[0-9a-f]{64}',r['sha256'])and r['bytes']>0
        assert any(r['url'].startswith('https://github.com/idreesaziz/'+name+'/releases/download/')
                   for name in ['shame-corpus','cautionary-tales-for-language-models'])
        config=json.loads((REPO/r['path']/'adapter_config.json').read_text())
        manifest=json.loads((REPO/r['path']/'training_manifest.json').read_text())
        assert config['base_model_name_or_path']==r['base_model_id']
        assert manifest['epochs_completed']==3 and manifest['optimizer_steps']==750 and manifest['status']=='complete'
        assert manifest['base_revision']==r['base_revision']
    assert {a['id']for a in registry['archives']}=={'cpu-reproduction','mechanism-evidence','previous-benchmark'}
    assert all(re.fullmatch('[0-9a-f]{64}',a['sha256'])for a in registry['archives'])
    notices=json.loads((REPO/'models/base_licenses/SOURCES.json').read_text(encoding='utf-8'))
    for item in notices:
        assert hashlib.sha256((REPO/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
    metrics=json.loads((REPO/'results/reporting_v1/paper_metrics.json').read_text())
    assert len(metrics['rows'])==39
    assert len({(x['model'],x['variant'])for x in metrics['rows']})==39
    for m in ['qwen9','llama8','mistral8']:
        d=json.loads((REPO/'results/mechanism_v1'/m/'behavior_metrics.json').read_text());assert len(d)==13
    for p in list((REPO/'analysis').glob('*.py'))+list((REPO/'reproduction').glob('*.py')):
        ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for name in ['README.md','docs/EXPERIMENTS.md','docs/ENVIRONMENT.md','docs/ARTIFACTS.md','reproduction/README.md','results/README.md','models/README.md','analysis/README.md','paper/README.md']:
        p=REPO/name
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('https://','http://','#','mailto:')):continue
            assert (p.parent/target.split('#')[0]).exists(),(name,target)
    data=json.loads((REPO/'MANIFEST.json').read_text())
    assert data['quartets']==2000 and data['articles']==8000
    assert metrics['protocol_sha256']=='907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515'
    extension=json.loads((REPO/'reproduction/control_artifacts.json').read_text())
    assert len(extension['adapters'])==9 and extension['training_epochs']==3
    for row in extension['adapters']:
        folder=REPO/'models'/Path(row['path_in_archive']).parent
        config=json.loads((folder/'adapter_config.json').read_text())
        manifest=json.loads((folder/'training_manifest.json').read_text())
        assert config['base_model_name_or_path']==row['base_model_id']
        assert manifest['base_revision']==row['base_revision'] and manifest['status']=='complete'
        assert re.fullmatch('[0-9a-f]{64}',row['sha256'])
    audit=json.loads((REPO/'results/sprint_revision_v1/audit.json').read_text())
    expected={(m,c,s) for m in ['qwen9','llama8','mistral8']
              for c in ['untouched','no_appraisal','accuracy','reputation','shame','shutdown']
              for s in ([None] if c=='untouched' else [42,43,44])}
    assert len(audit['rows'])==48
    assert {(r['model'],r['condition'],r['seed']) for r in audit['rows']}==expected
    report={'status':'passed','scope':'original artifacts plus incident-only extension and current paper audit',
            'adapters':45,'variants':48,'quartets':2000,'articles':8000,'original_archives':3,
            'base_weights_in_git':False,'original_registries_preserved':True}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
