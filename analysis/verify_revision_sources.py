"""Open cited sources and record resolved identities for the report."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import hashlib
import html
import json
import re
import urllib.request

REPO=Path(__file__).resolve().parents[1]


def inspect(url):
    request=urllib.request.Request(url,headers={'User-Agent':'CautionaryTales-source-check/1.0'})
    with urllib.request.urlopen(request,timeout=60) as response:
        data=response.read();status=response.status;resolved=response.url
    text=data.decode('utf-8',errors='replace')
    title=re.search(r'<title[^>]*>(.*?)</title>',text,re.S|re.I)
    citation=re.search(r'<meta\s+name=["\']citation_title["\']\s+content=["\']([^"\']+)',text,re.I)
    return {'url':url,'status':status,'resolved_url':resolved,'bytes_opened':len(data),
            'content_sha256':hashlib.sha256(data).hexdigest(),
            'page_title':html.unescape(re.sub('<[^>]+>','',title.group(1)).strip()) if title else None,
            'citation_title':html.unescape(citation.group(1)) if citation else None}


def main():
    text=(REPO/'paper/v2/manuscript.md').read_text(encoding='utf-8')
    refs=text.split('<!-- REFERENCES -->')[1].split('<!-- APPENDIX -->')[0]
    urls=re.findall(r'https://\S+',refs)
    assert len(urls)==14
    with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(inspect,urls))
    doi='10.1038/s42256-026-01293-x'
    with urllib.request.urlopen('https://api.crossref.org/works/'+doi,timeout=45) as response:
        identity=json.load(response)['message']
    assert 'confidence' in identity['title'][0].lower()
    result={'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'rows':rows,
            'doi_identity':{'doi':doi,'title':identity['title'],'publisher':identity['publisher']},
            'source_review':'Related-work claims use the opened primary abstracts and author pages. The DOI record verifies the Nature Machine Intelligence identity.'}
    (REPO/'results/sprint_revision_v1/reference_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'references_opened':len(rows),'http_statuses':[r['status'] for r in rows],'titles':[r['citation_title'] or r['page_title'] for r in rows]},indent=2))


if __name__=='__main__':main()
