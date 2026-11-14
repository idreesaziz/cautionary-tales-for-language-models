"""Stage checksum-verified raw inputs for portable CPU reproduction."""
from pathlib import Path
import hashlib
import json
import shutil

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'.artifacts/sprint_revision_v1/inputs'


def main():
    entries=[]
    prior_path=ROOT/'PROVENANCE.json'
    prior={e['path']:e for e in json.loads(prior_path.read_text())['files']} if prior_path.exists() else {}
    def copy(source,target):
        source=Path(source);target=ROOT/target
        target.parent.mkdir(parents=True,exist_ok=True)
        expected=hashlib.sha256(source.read_bytes()).hexdigest()
        if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==expected
        else:shutil.copyfile(source,target)
        entries.append({'path':target.relative_to(ROOT).as_posix(),'bytes':target.stat().st_size,'sha256':expected,
                        'original_source':prior.get(target.relative_to(ROOT).as_posix(),{}).get('original_source',str(source))})
    manifest=json.loads((REPO/'results/sprint_revision_v1/input_manifest.json').read_text())
    for entry in manifest['entries']:
        for kind,key in [('test_forced','forced'),('test_abstain','optional')]:
            source=Path(entry[key]);source=source if source.is_absolute() else REPO/source
            folder=Path('behavior')/entry['model']/entry['variant']/kind
            copy(source,folder/'decisions.npz')
            copy(source.parent/'phase_manifest.json',folder/'phase_manifest.json')
    causal=json.loads((REPO/'results/sprint_revision_v1/activation_controls.json').read_text())['sources']
    for source in causal:
        path=Path(source);model=next(m for m in ['qwen9','llama8','mistral8'] if m in source)
        variant=path.parent.name if 'sprint_revision_v1' in source else path.parent.parent.name
        copy(path,Path('causal')/model/variant/path.name)
    tokens=REPO/'results/reporting_v1/auxiliary_metrics.json'
    copy(tokens,Path('metadata')/'auxiliary_metrics.json')
    full_protocol=REPO.parent/'outputs/activation_study_v1/input/protocol.json'
    copy(full_protocol,Path('metadata')/'frozen_full_protocol.json')
    (ROOT/'PROVENANCE.json').write_text(json.dumps({'files':entries},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'staged_files':len(entries),'bytes':sum(e['bytes'] for e in entries)}))


if __name__=='__main__':main()
