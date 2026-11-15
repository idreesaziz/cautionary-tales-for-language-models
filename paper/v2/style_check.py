"""Check report prose for status labels, sentence length and direct wording."""
from pathlib import Path
import hashlib
import json
import re
import ast

REPO=Path(__file__).resolve().parents[2]
PATTERN=re.compile(r"\b(?:may|might|could|seems?|appears?|arguably|somewhat|perhaps|not|no|never|without|cannot|can't|don't|doesn't|isn't|aren't|wasn't|weren't|shouldn't|wouldn't|couldn't|apologi\w*|delve|notably|importantly)\b|\bto some extent\b|\bit should be noted\b|\bwe acknowledge\b|\ba growing body of work\b",re.I)


def clean(text):
    text=re.sub(r'```[\s\S]*?```','',text)
    text=re.sub(r'`[^`]+`','',text)
    text=re.sub(r'https?://\S+','',text)
    text=re.sub(r'\b(?:[\w.-]+/)+[\w.-]*','',text)
    text=re.sub(r'\b[\w.-]*[-_]appraisal[\w.-]*\b','',text)
    text=re.sub(r'<!--.*?-->','',text)
    text=re.sub(r'^:::.*$','',text,flags=re.M)
    return text


def main():
    paths=[REPO/'paper/v2/manuscript.md',REPO/'README.md',REPO/'paper/README.md',REPO/'paper/v2/README.md']
    results=[];issues=[]
    for path in paths:
        raw=path.read_text(encoding='utf-8')
        if path.name=='manuscript.md':
            first,rest=raw.split('<!-- REFERENCES -->')
            prefix, abstract_and_body = first.split('## Abstract\n\n', 1)
            abstract, body = abstract_and_body.split('\n\n', 1)
            approved = (REPO/'paper/v2/abstract.txt').read_text(encoding='utf-8').strip()
            assert abstract == approved, 'The author-supplied abstract retains its exact wording.'
            first = prefix + body
            raw=first+rest.split('<!-- APPENDIX -->',1)[1]
        text=clean(raw)
        for match in PATTERN.finditer(text):issues.append({'file':path.relative_to(REPO).as_posix(),'word':match.group(),'context':text[max(0,match.start()-45):match.end()+55]})
        sections=[]
        for block in re.split(r'^##+ ',text,flags=re.M)[1:]:
            heading,*body=block.splitlines();prose=' '.join(x for x in body if x and not x.startswith(('|','#','- ')))
            sentences=[s for s in re.split(r'(?<!\d)[.!?](?:\s+|$)',prose) if len(s.split())>2]
            average=sum(len(s.split()) for s in sentences)/len(sentences) if sentences else 0
            sections.append({'section':heading,'sentences':len(sentences),'average_words':average})
            if average>25:issues.append({'file':path.relative_to(REPO).as_posix(),'section':heading,'average_words':average})
        results.append({'path':path.relative_to(REPO).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sections':sections})
    source=(REPO/'paper/v2/build_paper.py').read_text(encoding='utf-8')
    tree=ast.parse(source)
    captions=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPTIONS' for t in n.targets))
    for name,parts in captions.items():
        for match in PATTERN.finditer(clean(' '.join(parts))):issues.append({'caption':name,'word':match.group()})
    out={'status':'passed' if not issues else 'repair_required','scope':'Editable prose. The author-supplied abstract retains its exact wording; references, quotations, URLs, identifiers and code retain source spelling.',
         'author_abstract_verbatim':True,'author_abstract_sha256':hashlib.sha256((REPO/'paper/v2/abstract.txt').read_bytes()).hexdigest(),'files':results,'issues':issues}
    target=REPO/'results/sprint_revision_v1/style_check.json';target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'issues':issues},indent=2))
    if issues:raise SystemExit(1)


if __name__=='__main__':main()
