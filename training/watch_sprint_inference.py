"""Read persistent inference progress and collect compact output artifacts."""
from pathlib import Path
import argparse
import json
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
import aiohttp.connector
from aiohttp.resolver import ThreadedResolver
aiohttp.connector.DefaultResolver=ThreadedResolver


def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--collect',action='store_true');p.add_argument('--model');a=p.parse_args()
    os.environ['MODAL_PROFILE']=a.workspace
    import modal
    models=[a.model] if a.model else ['qwen9'] if a.workspace=='idrees-mustafa-aziz' else ['llama8','mistral8']
    volume=modal.Volume.from_name('shame-mechanism-results-v1')
    root=Path(__file__).resolve().parents[1]/'.artifacts/sprint_extensions_v1/outputs';root.mkdir(parents=True,exist_ok=True)
    report={}
    for model in models:
        prefix='sprint-extensions-v1/outputs/'+model
        report[model]={}
        for leaf in ['progress.json','result.json','failure.json','runtime.json']:
            try:
                data=b''.join(volume.read_file(prefix+'/'+leaf));obj=json.loads(data)
                report[model][leaf]=obj
                path=root/model/leaf;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
            except FileNotFoundError:pass
        if a.collect:
            entries=[e for e in volume.iterdir('/'+prefix,recursive=True) if '/adapter_links/' not in e.path and Path(e.path).suffix in ['.json','.npz']]
            def collect(entry):
                relative=entry.path.split('sprint-extensions-v1/outputs/',1)[-1]
                target=root/relative
                if target.exists() and target.stat().st_size==entry.size and target.name not in ['progress.json','result.json','failure.json','runtime.json']:return 0
                data=b''.join(volume.read_file(entry.path));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);return 1
            with ThreadPoolExecutor(max_workers=8) as pool:count=sum(pool.map(collect,entries))
            report[model]['downloaded_files']=count
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
