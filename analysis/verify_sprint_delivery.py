"""Verify the report requirements and completed inference inventory."""
from pathlib import Path
import hashlib
import json

REPO=Path(__file__).resolve().parents[1]


def load(path):return json.loads((REPO/path).read_text(encoding='utf-8'))


def main():
    check=load('output/pdf/cautionary_tales/submission_checks.json')
    assert check['main_pages']<=8 and 150<=check['abstract_words']<=250
    assert check['title']=='Cautionary Tales for Language Models' and check['subtitle'] is None
    assert check['required_ethics_appendix'] and check['preexisting_and_sprint_work_disclosed']
    assert load('results/sprint_revision_v1/style_check.json')['status']=='passed'
    assert load('results/sprint_revision_v1/reproduction_check.json')['status']=='passed'
    assert load('results/sprint_revision_v1/numeric_trace.json')['status']=='passed'
    execution=load('results/sprint_revision_v1/execution_summary.json')
    assert execution['all_extensions_complete'] and execution['new_training_jobs']==0
    for r in execution['results'].values():assert r['base_weight_sha256_before']==r['base_weight_sha256_after']
    tests=load('results/sprint_revision_v1/audit_tool_tests.json');assert tests['status']=='passed' and tests['tests_run']==4
    assert len(load('results/sprint_revision_v1/audit.json')['rows'])==48
    behavior=load('results/sprint_revision_v1/qwen_prompt_answerability.json')
    assert len(behavior['rows'])==32 and len(behavior['sources'])==96
    for m in ['qwen9','llama8','mistral8']:
        r=load('results/sprint_revision_v1/'+m+'_random_null.json')
        assert r['new_random_directions']==20 and len(r['sources'])==6
    refs=load('results/layout_v4/reference_checks.json');assert len(refs['rows'])==18
    assert all(200<=r['status']<300 for r in refs['rows'])
    pdf=REPO/'output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.pdf'
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==check['pdf_sha256']
    report={'status':'passed','body_pages':check['main_pages'],'abstract_words':check['abstract_words'],
            'references_opened':18,'audited_variants':48,'neutral_behavior_blocks':96,'random_panels':18,
            'new_directions_per_model':20,'new_training_jobs':0,'neutral_document_control':'pending under the free-L4 constraint',
            'pdf_sha256':check['pdf_sha256']}
    (REPO/'results/sprint_revision_v1/delivery_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
