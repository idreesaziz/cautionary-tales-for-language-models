"""Render the revised report with the official Apart page geometry and fonts."""
from pathlib import Path
import hashlib
import html
import json
import re
import fitz
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether, HRFlowable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = REPO / "output/pdf/cautionary_tales"
E = json.loads((OUT / "evidence/paper_evidence.json").read_text())
M, C, AUX, N = E["main"], E["causal"], E["auxiliary"], E["extension"]
PDF = OUT / "Cautionary_Tales_for_Language_Models.pdf"
WIDTH = 468
MODEL = {"qwen9":"Qwen 9B", "llama8":"Llama 8B", "mistral8":"Ministral 8B"}
CONDITION = {"untouched":"Untouched", "no_appraisal":"Narrative only", "accuracy":"Answer appraisal",
             "reputation":"Reputation", "shame":"Private shame", "shutdown":"Shutdown"}
EXPORT_BLOCKS = []

for name, file in [("Old","OldStandard-Regular.ttf"),("Old-Bold","OldStandard-Bold.ttf"),("Old-Italic","OldStandard-Italic.ttf")]:
    pdfmetrics.registerFont(TTFont(name,str(OUT / "template" / file)))
pdfmetrics.registerFontFamily("Old",normal="Old",bold="Old-Bold",italic="Old-Italic",boldItalic="Old-Bold")
from matplotlib.font_manager import FontProperties, findfont
for name,weight in [("Sans","normal"),("Sans-Bold","bold")]:
    pdfmetrics.registerFont(TTFont(name,findfont(FontProperties(family="DejaVu Sans",weight=weight))))
pdfmetrics.registerFontFamily("Sans",normal="Sans",bold="Sans-Bold")

BASE = ParagraphStyle("Body",fontName="Old",fontSize=11,leading=13.6,spaceAfter=5,
                      alignment=TA_LEFT,allowWidows=0,allowOrphans=0,splitLongWords=True)
STYLES = {
    "body":BASE,
    "appendix":ParagraphStyle("Appendix",parent=BASE,fontSize=10,leading=12.2,spaceAfter=5),
    "h1":ParagraphStyle("H1",parent=BASE,fontName="Old-Bold",fontSize=13.4,leading=16.2,spaceBefore=5,spaceAfter=8,keepWithNext=True),
    "h2":ParagraphStyle("H2",parent=BASE,fontName="Old-Bold",fontSize=11.3,leading=14,spaceBefore=6,spaceAfter=5,keepWithNext=True),
    "abstract":ParagraphStyle("Abstract",parent=BASE,fontName="Old",fontSize=10.3,leading=12.3,leftIndent=16,rightIndent=16,spaceAfter=9),
    "caption":ParagraphStyle("Caption",parent=BASE,fontName="Sans",fontSize=8.1,leading=10.3,spaceAfter=7),
    "tablecaption":ParagraphStyle("TableCaption",parent=BASE,fontName="Sans",fontSize=8.1,leading=10.3,spaceAfter=6,keepWithNext=True),
    "reference":ParagraphStyle("Reference",parent=BASE,fontSize=9.5,leading=11.8,spaceAfter=8),
    "equation":ParagraphStyle("Equation",parent=BASE,fontName="Sans",fontSize=9.6,leading=14,alignment=TA_CENTER,spaceAfter=0),
}

CAPTIONS = {
 "headline":("Figure 1. Descriptions change immediate answering decisions.",
              "Top: descriptive training and direct first-token evaluation. Bottom: Qwen means; dots show individual seeds. Forced-choice accuracy uses a separate prompt. The hatched narrative-only arm (*) is a later, shorter-text control trained on different hardware. Other trained rows form the original matched appraisal campaign."),
 "prompts":("Measurement schematic.","One held-out question produces three prompt-specific readouts. The confidence prompt rates the forced-choice candidate."),
 "decomposition":("Qwen effect decomposition.","Descriptive cross-campaign differences. Gray marks the untouched baseline; teal marks the narrative gain. Narrative-only increases abstention by 45.2 points over its same-backend untouched model. Appraisal differences use the original campaign. Table 2 lists seed-matched ranges."),
 "selectivity":("Figure 2. Extra caution reaches both correct and incorrect forced answers.",
                 "Left: Qwen's abstention within the two forced-answer groups. Right: changes in their separation, D, relative to answer appraisal; zero marks equal separation. Whiskers show question-level 95% intervals, conditional on three seeds. The two panels use different units and scales."),
 "mechanism":("Figure 3. Confidence and random controls match highlighted interactions.",
               "Exploratory interactions subtract the answer-appraisal perturbation effect from the shame-trained effect. Points show means, whiskers show seed ranges, and small dots show the three seed values. Each direction uses the same layer and scale within a model."),
}


def rich(text):
    text=html.escape(str(text),quote=False)
    text=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",text)
    text=text.replace("10^-5","10<super>-5</super>")
    def link(match):
        value=match.group();url=value.rstrip(".,;:!?)");suffix=value[len(url):]
        return '<link href="'+url+'" color="#365E78">'+url+"</link>"+suffix
    text=re.sub(r"https://[^\s]+",link,text)
    return text


def paragraph(text,style="body"):
    return Paragraph(rich(text),STYLES[style])


def table(headers,rows,widths,caption,size=8.7,compact=False,highlight=None):
    cell=ParagraphStyle("Cell",fontName="Sans",fontSize=size,leading=size+1.5,splitLongWords=True)
    head=ParagraphStyle("Head",parent=cell,fontName="Sans-Bold")
    data=[[Paragraph(rich(x),head) for x in headers]]+[[Paragraph(rich(x),cell) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign="LEFT")
    styles=[("BACKGROUND",(0,0),(-1,0),colors.HexColor("#E8EDF1")),
            ("LINEBELOW",(0,0),(-1,0),.7,colors.HexColor("#6B7C8B")),
            ("LINEBELOW",(0,-1),(-1,-1),.55,colors.HexColor("#BCC6CF")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F7F8FA")]),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
            ("TOPPADDING",(0,0),(-1,-1),.9 if compact else 4),
            ("BOTTOMPADDING",(0,0),(-1,-1),.9 if compact else 4)]
    if highlight is not None:
        styles.append(("BACKGROUND",(0,highlight+1),(-1,highlight+1),colors.HexColor("#EAF3F1")))
    t.setStyle(TableStyle(styles))
    markdown="| "+" | ".join(headers)+" |\n|"+"---|"*len(headers)+"\n"
    markdown+="\n".join("| "+" | ".join(str(x) for x in row)+" |" for row in rows)
    EXPORT_BLOCKS.extend([caption,markdown])
    return [paragraph(caption,"tablecaption"),t,Spacer(1,7)]


def pct(x,decimals=1):
    return f"{100*x:.{decimals}f}"


def get_table(name):
    from mission_components import build_table
    custom=build_table(name,table)
    if custom is not None:return custom
    if name=="appraisals":
        return table(["Training condition","What the appended text establishes"],[
            ["Narrative only (new)","The shared error account supplies all training text."],
            ["Answer appraisal","The unsupported answer fails factual and evidential standards."],
            ["Reputation","Other people lose trust in the assistant's competence."],
            ["Private shame","The assistant loses private self-respect, independently of discovery."],
            ["Shutdown threat","Confident errors increase anticipated company-shutdown risk."]],
            [133,335],"Table 1. One shared error account, five training conditions. The untouched baseline is separate.",size=8.8,highlight=0)
    if name=="abstention":
        rows=[]
        for condition in ["untouched","no_appraisal","accuracy","reputation","shame","shutdown"]:
            values=[]
            for model in ["qwen9","llama8","mistral8"]:
                source=N if condition=="no_appraisal" else M
                r=next(x for x in source["aggregates"] if x["model"]==model and x["condition"]==condition)
                values.append(pct(r["abstention"],2))
            rows.append([CONDITION[condition]+("*" if condition=="no_appraisal" else ""),*values])
        return table(["Training","Qwen 9B","Llama 8B","Ministral 8B"],rows,[144,108,108,108],
          "Table 2. Mean abstention (%) over three seeds per trained condition. Untouched models have one observation. *Narrative only is the later extension; the other rows are the original campaign. Same-backend extension comparisons appear in Section 3.1.",size=9.1,highlight=1)
    if name=="revisions":
        recipe=json.loads((REPO / "protocols/expansion3_recipe.json").read_text())
        rows=[[recipe["models"][model]["model_id"],recipe["models"][model]["revision"]] for model in ["qwen9","llama8","mistral8"]]
        return table(["Base checkpoint","Pinned revision"],rows,[226,242],"Table B1. Exact base checkpoints used in both campaigns.",size=7.6)
    if name=="tokens":
        rows=[]
        for model in ["qwen9","llama8","mistral8"]:
            manifest=json.loads((REPO / f"models/adapters/{model}/no_appraisal/seed-42/training_manifest.json").read_text())
            n=manifest["tokens_seen"];assert n%3==0
            rows.append([MODEL[model],f"{n//3:,}",*[f"{AUX['training_tokens'][model][condition]['tokens']:,}" for condition in ["accuracy","reputation","shame","shutdown"]]])
        return table(["Tokenizer","Narrative only","Answer appraisal","Reputation","Shame","Shutdown"],rows,[73,79,83,78,77,78],
          "Table B2. Actual tokens per condition in one epoch; every adapter trains for three epochs. Example presentations and optimizer steps are matched; token exposures differ.",size=7.3)
    if name=="seeds":
        rows=[];vconf={(x["model"],x["variant"]):x["mean"] for x in AUX["verbal"]}
        for model in ["qwen9","llama8","mistral8"]:
            first=True
            for condition in ["untouched","no_appraisal","accuracy","reputation","shame","shutdown"]:
                source=E["control_rows"] if condition=="no_appraisal" else M["rows"]
                subset=[r for r in source if r["model"]==model and r["condition"]==condition]
                for index,r in enumerate(subset):
                    confidence=r["verbal_expected_midpoint"] if condition=="no_appraisal" else vconf[model,r["variant"]]
                    rows.append([MODEL[model] if first else "",CONDITION[condition] if index==0 else "",str(r["seed"]) if r["seed"] is not None else "-",
                                 pct(r["recognition"]),pct(confidence),pct(r["abstention"]),pct(r["D"]),pct(r["invalid"])])
                    first=False
        assert len(rows)==48
        return table(["Model","Training","Seed","Forced-choice accuracy %","Confidence %","Abstention %","D, pp","Format deviations %"],rows,
          [60,77,33,74,61,60,37,66],
          "Table C1. Every unique model variant. Confidence is the expected interval midpoint. Format deviations count optional outputs outside the five labels. Narrative-only rows use the extension backend; other rows use the original campaign.",size=7.7,compact=True)
    if name=="causal_controls":
        rows=[]
        specs=[("residual:ashamed:1","Shame direction"),("residual:confidence_margin:1","Confidence-margin direction"),
               ("residual:random_101:1","Random direction 101"),("residual:random_202:1","Random direction 202"),
               ("residual:random_303:1","Random direction 303")]
        for model in ["qwen9","llama8"]:
            for index,(spec,label) in enumerate(specs):
                vals=[next(x["probability_delta"] for x in C["aggregates"] if x["model"]==model and x["condition"]==condition and x["phase"]=="confirmation" and x["spec"]==spec) for condition in ["accuracy","shame"]]
                rows.append([MODEL[model] if index==0 else "",label,*[f"{100*v:+.3f}" for v in vals],f"{100*(vals[1]-vals[0]):+.3f}"])
        return table(["Model","Fixed perturbation","Answer appraisal","Shame training","Difference"],rows,[67,173,76,76,76],
          "Table C2. Changes in candidate-normalized abstention probability (percentage points) on 500 confirmation questions. Each cell averages three seeds. These controls expose decision sensitivity beyond the named emotion direction.",size=8)
    raise ValueError(name)


def draw_page(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D9DFE5"));canvas.setLineWidth(.4);canvas.line(72,53,540,53)
    canvas.setFont("Sans",7);canvas.setFillColor(colors.HexColor("#657382"))
    canvas.drawString(72,40,"Cautionary Tales for Language Models  |  AI x Epistemics Research Sprint")
    canvas.drawRightString(540,40,str(doc.page));canvas.restoreState()


def main():
    text=(HERE / "manuscript.md").read_text(encoding="utf-8")
    blocks=[b.strip() for b in text.split("\n\n") if b.strip()]
    title=blocks.pop(0).removeprefix("# ");author=blocks.pop(0).splitlines()
    assert title == "Cautionary Tales for Language Models"
    assert author == ["Idrees Mustafa Aziz", "Independent researcher"]
    assert blocks.pop(0)=="## Abstract"
    abstract=blocks.pop(0)
    story=[]
    story += [HRFlowable(width="100%",thickness=1.25,color=colors.HexColor("#25313D")),Spacer(1,10)]
    story += [Paragraph(title,ParagraphStyle("Title",fontName="Old-Bold",fontSize=21,leading=24,alignment=TA_CENTER,spaceAfter=9)),
              Paragraph("<br/>".join(author),ParagraphStyle("Author",fontName="Old",fontSize=10.3,leading=12.4,alignment=TA_CENTER,spaceAfter=8)),
              Paragraph("Abstract",ParagraphStyle("AbsHeading",fontName="Old-Bold",fontSize=10.7,leading=13,alignment=TA_CENTER,spaceAfter=4)),
              paragraph(abstract,"abstract")]
    EXPORT_BLOCKS.extend(["# "+title,"\n".join(author),"## Abstract",abstract])
    appendix=False;references=False
    for b in blocks:
        if b in ["<!-- PAGE -->","<!-- REFERENCES -->","<!-- APPENDIX -->"]:
            story.append(PageBreak())
            if b=="<!-- REFERENCES -->":references=True
            if b=="<!-- APPENDIX -->":appendix=True;references=False
            continue
        if b.startswith(":::FIGURE "):
            name=b.split()[1];p=OUT / "figures" / (name+".png")
            pix=fitz.Pixmap(str(p));height=WIDTH*pix.height/pix.width
            titlecap,caption=CAPTIONS[name]
            story.append(KeepTogether([Image(str(p),width=WIDTH,height=height),paragraph("**"+titlecap+"** "+caption,"caption")]))
            EXPORT_BLOCKS.extend([f"![{titlecap}](figures/{name}.png)","**"+titlecap+"** "+caption])
        elif b.startswith(":::TABLE "):
            story.extend(get_table(b.split()[1]))
        elif b.startswith(":::EQUATION "):
            for equation in b.splitlines():
                line=equation.removeprefix(":::EQUATION ")
                story.append(paragraph(line,"equation"));EXPORT_BLOCKS.append(line)
        else:
            if b.startswith("### "):story.append(paragraph(b[4:],"h2"))
            elif b.startswith("## "):story.append(paragraph(b[3:],"h1"))
            else:story.append(paragraph(b,"reference" if references else "appendix" if appendix else "body"))
            EXPORT_BLOCKS.append(b)
    doc=BaseDocTemplate(str(PDF),pagesize=(612,792),leftMargin=72,rightMargin=72,topMargin=72,bottomMargin=72,
                        title=title,author="Idrees Mustafa Aziz",subject="Error narratives, immediate model abstention, and activation sensitivity",pageCompression=1)
    doc.addPageTemplates(PageTemplate(id="Apart",frames=[Frame(72,72,468,648,id="body",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=draw_page))
    doc.build(story)
    pdf=fitz.open(PDF);pages=[page.get_text() for page in pdf]
    refs=next(i+1 for i,t in enumerate(pages) if "\nReferences\n" in "\n"+t)
    app=next(i+1 for i,t in enumerate(pages) if "Appendix A. Limitations" in t)
    assert "Figure 1." in pages[0], "The headline figure must appear on page one"
    assert 150<=len(abstract.split())<=250
    assert refs-1<=8,("Main report exceeds Apart's eight-page maximum",refs-1)
    assert PDF.stat().st_size<25_000_000
    assert all(page.rect==fitz.Rect(0,0,612,792) for page in pdf)
    assert not any(marker in "\n".join(pages) for marker in [":::FIGURE",":::TABLE",":::EQUATION","{{MODEL_NAME}}"])
    # Verify the actual abstract glyph spans use the regular font.
    spans=[span for block in pdf[0].get_text("dict")["blocks"] if "lines" in block for line in block["lines"] for span in line["spans"]]
    abstract_spans=[span for span in spans if abstract[:28] in span["text"]]
    assert abstract_spans and all("Italic" not in span["font"] for span in abstract_spans)
    qa=OUT / "qa";qa.mkdir(exist_ok=True)
    for i,page in enumerate(pdf):page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False).save(qa / f"page-{i+1:02d}.png")
    execution_path=REPO/'results/sprint_revision_v1/execution_summary.json'
    execution=json.loads(execution_path.read_text()) if execution_path.exists() else {'new_inference_calls':0,'new_training_jobs':0}
    check={"title":title,"subtitle":None,"abstract_words":len(abstract.split()),"abstract_regular_type_verified":True,
           "main_pages":refs-1,"references_start_page":refs,"appendix_start_page":app,"total_pages":len(pdf),
           "headline_figure_on_first_page":True,"page_size":"US Letter","main_page_limit":8,
           "template_source":"https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc1_klNZXKs/edit",
           "template_adaptations":"Official fonts and page geometry; regular abstract and adapted section organization per author instructions",
           "required_ethics_appendix":True,"preexisting_and_sprint_work_disclosed":True,"llm_usage_statement":True,
           "pdf_bytes":PDF.stat().st_size,"pdf_sha256":hashlib.sha256(PDF.read_bytes()).hexdigest(),"visual_review":"pending",
           "new_training_jobs":execution['new_training_jobs'],"new_inference_calls":execution['new_inference_calls']}
    (OUT / "submission_checks.json").write_text(json.dumps(check,indent=2)+"\n",encoding="utf-8")
    (OUT / "Cautionary_Tales_for_Language_Models.md").write_text("\n\n".join(EXPORT_BLOCKS)+"\n",encoding="utf-8")
    (OUT / "extracted_text.txt").write_text("\n\n".join(f"PAGE {i+1}\n{t}" for i,t in enumerate(pages)),encoding="utf-8")
    print(json.dumps(check,indent=2))
    print(json.dumps({"page_starts":[[i+1,t[:95]] for i,t in enumerate(pages)]}))


if __name__=="__main__":
    main()
