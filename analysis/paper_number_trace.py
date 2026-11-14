"""Index displayed numeric prose and tables against saved measurement sources."""
from pathlib import Path
import hashlib
import json
import re

REPO=Path(__file__).resolve().parents[1]
DATA='results/sprint_revision_v1/'


def main():
    path=REPO/'output/pdf/cautionary_tales/Cautionary_Tales_for_Language_Models.md'
    heading='Abstract';entries=[]
    groups={
      'Abstract':[DATA+'audit.json',DATA+'qwen_prompt_answerability.json',DATA+'qwen9_random_null.json'],
      '1.':[DATA+'audit.json',DATA+'execution_summary.json'],
      '2.':['protocols/mechanism_v1.json','protocols/expansion3_recipe.json',DATA+'token_matching.json','output/pdf/cautionary_tales/evidence/training_language_screen.json'],
      '3.':[DATA+'audit.json',DATA+'narrative_contrasts.json',DATA+'seed_tests.json','results/reporting_v1/paper_metrics.json'],
      '4.':[DATA+'audit.json','results/reporting_v1/paper_metrics.json'],
      '4.1':[DATA+'qwen_prompt_answerability.json'],
      '5.':[DATA+'activation_controls.json',*[DATA+m+'_random_null.json' for m in ['qwen9','llama8','mistral8']]],
      '6.':[DATA+'reference_checks.json'],
      '7.':[DATA+'audit.json',DATA+'qwen_prompt_answerability.json'],
      'References':[DATA+'reference_checks.json'],
      'Appendix A':[DATA+'audit.json',DATA+'token_matching.json',DATA+'execution_summary.json','protocols/mechanism_v1.json','output/pdf/cautionary_tales/evidence/paper_evidence.json'],
      'Appendix B':['protocols/expansion3_recipe.json','protocols/mechanism_v1.json','results/reporting_v1/auxiliary_metrics.json','output/pdf/cautionary_tales/evidence/paper_evidence.json',DATA+'execution_summary.json'],
      'Appendix C':[DATA+'audit.json',DATA+'activation_controls.json','output/pdf/cautionary_tales/evidence/paper_evidence.json'],
      'Appendix D':['protocols/sprint_extensions_v1.json','protocols/sprint_extensions_v1_execution_amendment.json']}
    for index,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if line.startswith('## '):heading=line[3:]
        visible=re.sub(r'https?://[^\s)]+','',line)
        tokens=re.findall(r'(?<![\w])[-+]?\d+(?:[,.]\d+)*',visible)
        if not tokens or line.startswith(('#','![')):continue
        key=next((k for k in sorted(groups,key=len,reverse=True) if heading.startswith(k)),None)
        if key is None:
            if heading.startswith('B.'):key='Appendix B'
            elif heading.startswith('C.'):key='Appendix C'
            elif heading.startswith('2.'):key='2.'
        assert key,(heading,line)
        entries.append({'line':index,'section':heading,'text':line,'numeric_tokens':tokens,'saved_sources':groups[key]})
    sources=sorted({p for e in entries for p in e['saved_sources']})
    assert all((REPO/p).exists() for p in sources)
    figures={'headline':['results/reporting_v1/paper_metrics.json','results/no_appraisal_v1/control_metrics.json'],
             'decomposition':[DATA+'narrative_contrasts.json','results/no_appraisal_v1/control_metrics.json'],
             'selectivity':['results/reporting_v1/paper_metrics.json'],
             'mechanism':[DATA+'activation_controls.json']}
    report={'status':'passed','scope':'Every numeric prose/table line has a saved source binding. Raw recomputation and claim checks validate scientific values. Axis ticks follow the plotting source.',
            'expanded_manuscript_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'entries':entries,'figure_sources':figures,'source_hashes':{p:hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in sources}}
    (REPO/DATA/'numeric_trace.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'passed','numeric_lines':len(entries),'saved_source_files':len(sources)}))


if __name__=='__main__':main()
