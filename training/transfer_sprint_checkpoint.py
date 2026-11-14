"""Copy verified complete Qwen blocks between existing-credit workspaces."""
from pathlib import Path
import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
import aiohttp.connector
from aiohttp.resolver import ThreadedResolver
aiohttp.connector.DefaultResolver=ThreadedResolver


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['download','upload']);args=p.parse_args()
    repo=Path(__file__).resolve().parents[1]
    local=repo/'.artifacts/sprint_checkpoint_transfer'
    local.mkdir(parents=True,exist_ok=True)
    workspace='idrees-mustafa-aziz' if args.action=='download' else 'idrees-mustafa-az'
    os.environ['MODAL_PROFILE']=workspace
    import modal
    volume=modal.Volume.from_name('shame-mechanism-results-v1')
    if args.action=='download':
        paths=['jobs/qwen9_causal_resume_v2/causal/direction_bank.npz']
        prefix='sprint-extensions-v1/outputs/qwen9'
        candidates=[e.path for e in volume.iterdir('/'+prefix,recursive=True) if Path(e.path).name=='manifest.json']
        def read_remote(path):return path,b''.join(volume.read_file(path))
        with ThreadPoolExecutor(max_workers=8) as pool:
            for path,data in pool.map(read_remote,candidates):
                receipt=json.loads(data)
                if receipt.get('status')=='complete':
                    folder=str(Path(path).parent).replace('\\','/')
                    leaf='scores.npz' if '/random_panel/' in folder else 'decisions.npz'
                    paths.extend([path,folder+'/'+leaf])
        manifest=[]
        with ThreadPoolExecutor(max_workers=8) as pool:
            for remote,data in pool.map(read_remote,paths):
                path=local/remote.lstrip('/')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
                manifest.append({'remote':remote.lstrip('/'),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        for entry in manifest:
            if entry['remote'].endswith('/manifest.json'):
                receipt=json.loads((local/entry['remote']).read_text());folder=(local/entry['remote']).parent
                scores=folder/('scores.npz' if 'random_panel' in entry['remote'] else 'decisions.npz')
                assert hashlib.sha256(scores.read_bytes()).hexdigest()==receipt['sha256']
        (local/'transfer_manifest.json').write_text(json.dumps({'source_workspace':workspace,'entries':manifest},indent=2)+'\n')
    else:
        manifest=json.loads((local/'transfer_manifest.json').read_text())['entries']
        existing_paths={e.path.lstrip('/') for e in volume.iterdir('/sprint-extensions-v1/outputs/qwen9',recursive=True)}
        try:
            bank='jobs/qwen9_causal_resume_v2/causal/direction_bank.npz'
            list(volume.iterdir('/'+str(Path(bank).parent).replace('\\','/')))
            existing_paths.add(bank)
        except FileNotFoundError:pass
        def verify_existing(entry):
            existing=b''.join(volume.read_file(entry['remote']))
            assert hashlib.sha256(existing).hexdigest()==entry['sha256']
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(verify_existing,[e for e in manifest if e['remote'] in existing_paths]))
        with volume.batch_upload(force=False) as batch:
            for entry in manifest:
                path=local/entry['remote'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
                if entry['remote'] not in existing_paths:batch.put_file(path,'/'+entry['remote'])
    print(json.dumps({'workspace':workspace,'action':args.action,'verified_files':len(manifest)}))


if __name__=='__main__':main()
