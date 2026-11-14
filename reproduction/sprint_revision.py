"""Reproduce the sprint revision from a checksum-verified CPU input archive."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
from run import REPO, digest, extract_verified, fetch


def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);p.add_argument('--build',action='store_true');a=p.parse_args()
    registry=json.loads((REPO/'reproduction/sprint_revision_artifacts.json').read_text())
    asset=registry['archive']
    archive=a.archive or fetch(asset['url'],REPO/'.artifacts/downloads'/asset['name'],asset['sha256'])
    assert archive.stat().st_size==asset['bytes'] and digest(archive)==asset['sha256']
    workspace=REPO/'.artifacts/sprint_revision_v1'
    count=extract_verified(archive,workspace)
    for relative in ['analysis/sprint_revision.py','analysis/revision_measurements.py']:
        subprocess.run([sys.executable,str(REPO/relative)],cwd=REPO,check=True)
    subprocess.run([sys.executable,str(REPO/'abstention_audit.py'),'--manifest',str(REPO/'results/sprint_revision_v1/input_manifest.json'),
                    '--output',str(workspace/'audit_48_variants.json')],cwd=REPO,check=True)
    subprocess.run([sys.executable,str(REPO/'analysis/sprint_extensions.py'),'--root',str(workspace/'extension_outputs'),'--behavior'],cwd=REPO,check=True)
    expected=json.loads((workspace/'reference_metrics.json').read_text())
    actual={name:json.loads((REPO/'results/sprint_revision_v1'/name).read_text()) for name in expected}
    def values(obj):
        if isinstance(obj,dict):return {k:values(v) for k,v in obj.items() if k not in ['sources','raw_sources','original_source']}
        if isinstance(obj,list):return [values(v) for v in obj]
        return obj
    def compare(left,right,path=''):
        import math
        if isinstance(left,float):assert math.isclose(left,right,rel_tol=1e-9,abs_tol=1e-11),(path,left,right)
        elif isinstance(left,dict):
            assert left.keys()==right.keys(),path
            for key in left:compare(left[key],right[key],path+'/'+key)
        elif isinstance(left,list):
            assert len(left)==len(right),path
            for i,(x,y) in enumerate(zip(left,right)):compare(x,y,path+'/'+str(i))
        else:assert left==right,(path,left,right)
    compare(values(expected),values(actual))
    if a.build:
        for name in ['audit_training_language.py','prepare_evidence.py','make_figures.py','build_paper.py','verify_paper.py','style_check.py']:
            subprocess.run([sys.executable,str(REPO/'paper/v2'/name)],cwd=REPO,check=True)
    report={'status':'passed','verified_members':count,'variants':48,'extension_models':3,'compute':'CPU',
            'archive_sha256':asset['sha256'],'scientific_value_tolerance':{'relative':1e-9,'absolute':1e-11}}
    (REPO/'results/sprint_revision_v1/reproduction_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
