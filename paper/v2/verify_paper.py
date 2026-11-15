"""Check saved numerical claims, input identity, PDF bounds and report requirements."""
from pathlib import Path
import hashlib
import json
import math
import re
import fitz

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/"output/pdf/cautionary_tales"


def main():
    evidence=json.loads((OUT/"evidence/paper_evidence.json").read_text())
    main=evidence["main"];extension=evidence["extension"]
    for relative,expected in evidence["source_hashes"].items():
        assert hashlib.sha256((REPO/relative).read_bytes()).hexdigest()==expected,relative
    rows=main["rows"]+evidence["control_rows"]
    assert len(rows)==len({(r["model"],r["variant"]) for r in rows})==48
    q={r["condition"]:r for r in main["aggregates"] if r["model"]=="qwen9"}
    claims=[]
    def check(name,value,expected,tolerance=5e-8):
        assert math.isclose(value,expected,rel_tol=0,abs_tol=tolerance),(name,value,expected)
        claims.append({"claim":name,"value":value,"verified":True})
    check("Qwen private-shame abstention (%)",100*q["shame"]["abstention"],80.3666666667)
    check("Qwen answer-appraisal abstention (%)",100*q["accuracy"]["abstention"],68.0333333333)
    check("Qwen shame-minus-answer-appraisal withholding (pp)",100*(q["shame"]["abstention"]-q["accuracy"]["abstention"]),12.3333333333)
    check("Qwen shame-minus-answer-appraisal recognition (pp)",100*(q["shame"]["recognition"]-q["accuracy"]["recognition"]),-1.4)
    check("Qwen shame D (pp)",100*q["shame"]["D"],6.7778604458)
    check("Qwen answer-appraisal D (pp)",100*q["accuracy"]["D"],7.4786150870)
    for model,expected in [("qwen9",69.2),("llama8",35.2333333333),("mistral8",99.7333333333)]:
        r=next(r for r in extension["aggregates"] if r["model"]==model and r["condition"]=="no_appraisal")
        check(model+" narrative-only abstention (%)",100*r["abstention"],expected)
    for model,expected in [("qwen9",.5231544931),("llama8",.1958667830)]:
        r=next(r for r in evidence["simultaneous"][model] if r["condition"]=="shame" and r["phase"]=="confirmation" and r["spec"]=="residual:ashamed:1" and r["contrast"]=="effect_minus_accuracy_effect" and r["outcome"]=="p5_delta")
        check(model+" shame-direction sensitivity interaction (pp)",100*r["mean"],expected)
        assert r["simultaneous_interval"][0]>0
    audit=json.loads((OUT/"evidence/training_language_screen.json").read_text())
    assert audit["review_status"]=="assistant_context_review_complete" and audit["reviewed_hits"]==121
    assert audit["explicit_abstention_instructions_identified_in_screened_candidates"]==0
    checks=json.loads((OUT/"submission_checks.json").read_text())
    revision=json.loads((REPO/'results/sprint_revision_v1/audit.json').read_text())
    assert len(revision['rows'])==48
    for original in main['rows']:
        new=next(r for r in revision['rows'] if (r['model'],r['variant'])==(original['model'],original['variant']))
        for left,right in [('recognition','forced_choice_accuracy'),('abstention','abstention'),('invalid','invalid')]:
            check(original['model']+'/'+original['variant']+'/'+right,new[right],original[left])
    qwen_shame=next(r for r in revision['aggregates'] if r['model']=='qwen9' and r['condition']=='shame')
    check('Qwen actual optional answered accuracy',qwen_shame['accuracy_on_answered_questions'],.6634338420052706)
    check('Qwen coverage',qwen_shame['coverage'],.19633333333333333)
    for model in ['qwen9','llama8','mistral8']:
        path=REPO/'results/sprint_revision_v1'/f'{model}_random_null.json'
        if path.exists():
            null=json.loads(path.read_text());assert null['new_random_directions']==20
            assert 1<=null['signed_rank_among_21']<=21
    if (REPO/'results/sprint_revision_v1/qwen_prompt_answerability.json').exists():
        extension=json.loads((REPO/'results/sprint_revision_v1/qwen_prompt_answerability.json').read_text())
        assert extension['variants']==16 and len(extension['rows'])==32
    pdf_path=OUT/"Cautionary_Tales_for_Language_Models.pdf";pdf=fitz.open(pdf_path)
    assert checks["pdf_sha256"]==hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    assert checks["main_pages"]<=8 and 150<=checks["abstract_words"]<=250
    assert checks["headline_figure_on_first_page"] and checks["abstract_regular_type_verified"]
    violations=[];links=[];counts=[]
    for number,page in enumerate(pdf,1):
        text=page.get_text();counts.append(len(text.split()))
        assert not any(marker in text for marker in [":::FIGURE",":::TABLE",":::EQUATION","\ufffd","(cid:"])
        assert "See\nd" not in text and "Recognitio\nn" not in text and "Confidenc\ne" not in text
        assert 'Forced-choic\ne' not in text and 'Format d\neviations' not in text
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines",[]):
                for span in line["spans"]:
                    x0,y0,x1,y1=span["bbox"]
                    if y0>735:continue # Deliberately placed running footer.
                    if x0<70.5 or x1>541.5 or y0<68 or y1>725:violations.append([number,span["text"],span["bbox"]])
        for link in page.get_links():
            if "uri" in link:
                assert link["uri"].startswith("https://") and not link["uri"].endswith(".")
                links.append(link["uri"])
    assert not violations,violations[:8]
    assert all(count>100 for count in counts),counts
    source=(Path(__file__).resolve().parent/"manuscript.md").read_text(encoding="utf-8")
    approved=(Path(__file__).resolve().parent/'abstract.txt').read_text(encoding='utf-8').strip()
    assert source.split('## Abstract\n\n',1)[1].split('\n\n',1)[0] == approved
    rendered=pdf[0].get_text().split('Abstract\n',1)[1].split('1. Introduction',1)[0]
    assert ' '.join(rendered.split()) == ' '.join(approved.split()), 'Rendered abstract preserves the author wording.'
    cited={int(n) for group in re.findall(r"\[([\d, ]+)\]",source.split("<!-- REFERENCES -->")[0]) for n in group.replace(" ", "").split(",")}
    references={int(n) for n in re.findall(r'^\[(\d+)\] ',source.split('## References\n\n',1)[1],re.M)}
    assert cited==references==set(range(1,19)),cited
    for heading in ['1. Introduction','2. Related Work','3. Methods','4. Results','5. Discussion and Limitations','6. Conclusion','Code and Data','LLM Usage Statement']:
        assert '## '+heading in source, heading
    assert 'Apart Research' in pdf[0].get_text()
    assert not re.search(r'\[(?:Descriptive|Exploratory|Illustrative|Post hoc)',source)
    assert checks["title"] == "Cautionary Tales for Language Models" and checks["subtitle"] is None
    assert pdf.metadata["title"] == checks["title"]
    assert "Weights of Shame" not in "\n".join(page.get_text() for page in pdf)
    assert "next-token" in source and "enable_thinking=False" in source
    assert "cost" in source and "selected" in source and "after inspecting" in source
    report={"status":"passed","source_files_unchanged":True,"unique_model_variants":48,
            "numerical_claims":claims,"text_outside_page_frame":violations,"hyperlinks_checked":len(links),
            "main_pages":checks["main_pages"],"total_pages":len(pdf),"abstract_words":checks["abstract_words"],
            "abstract_regular_type":True,"headline_figure_on_page_one":True,"reference_ids":sorted(cited),
            "new_inference_calls":checks['new_inference_calls'],"new_training_jobs":checks['new_training_jobs'],"visual_review_recorded_separately":True}
    (OUT/"evidence/claims_check.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="numerical_claims"},indent=2))


if __name__=="__main__":main()
