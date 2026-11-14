"""Package raw decision and intervention inputs with per-file hashes."""
from pathlib import Path
import hashlib
import json
import zipfile

REPO=Path(__file__).resolve().parents[1]


def main():
    inputs=REPO/'.artifacts/sprint_revision_v1/inputs'
    extensions=REPO/'.artifacts/sprint_extensions_v1/outputs'
    output=REPO/'.release-staging/sprint_revision_v1';output.mkdir(parents=True,exist_ok=True)
    name='Cautionary_Tales_sprint_revision_cpu_v1.zip';archive=output/name
    files={}
    for p in inputs.rglob('*'):
        if p.is_file():files['inputs/'+p.relative_to(inputs).as_posix()]=p.read_bytes()
    for p in extensions.rglob('*'):
        if p.is_file() and '/adapter_links/' not in p.as_posix() and p.suffix in ['.npz','.json']:
            if p.name in ['partial.npz','failure.json','progress.json']:continue
            files['extension_outputs/'+p.relative_to(extensions).as_posix()]=p.read_bytes()
    names=['audit.json','seed_tests.json','narrative_contrasts.json','activation_controls.json','token_matching.json',
           'qwen9_random_null.json','llama8_random_null.json','mistral8_random_null.json','qwen_prompt_answerability.json']
    reference={n:json.loads((REPO/'results/sprint_revision_v1'/n).read_text()) for n in names}
    files['reference_metrics.json']=(json.dumps(reference,indent=2)+'\n').encode()
    entries=[{'path':k,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for k,v in sorted(files.items())]
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for key,data in sorted(files.items()):z.writestr(key,data)
        z.writestr('MANIFEST.json',json.dumps({'files':entries},indent=2)+'\n')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for e in entries:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']
    obj={'archive':{'name':name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
         'url':'https://github.com/idreesaziz/shame-corpus/releases/download/sprint-revision-v1.1/'+name},
         'members':len(entries),'scope':'Raw saved outputs, preserved original 512-row panels, primary 500-row analysis, complete prompt tests and 48-variant audit inputs.'}
    (REPO/'reproduction/sprint_revision_artifacts.json').write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(obj,indent=2))


if __name__=='__main__':main()
