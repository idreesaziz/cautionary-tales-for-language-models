"""Save full citation sources and page-level text for author review."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
import datetime as dt
import hashlib
import json
import re
import threading
import time
import requests
import fitz
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / '.artifacts/final_citation_audit_20261116'
FULL_SOURCES = {
    1: 'https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/',
    2: 'https://arxiv.org/pdf/2510.17941',
    3: 'https://aclanthology.org/2026.findings-acl.218.pdf',
    4: 'https://www.nature.com/articles/s42256-026-01293-x.pdf',
    5: 'https://aclanthology.org/2026.emnlp-main.759.pdf',
    6: 'https://arxiv.org/pdf/2604.07729',
    7: 'https://huggingface.co/datasets/ryancodrai/emotion-probes/raw/720f2eb3173a77ca70ebef8ed091fc1844f70340/README.md',
    8: 'https://arxiv.org/pdf/2607.18966',
    9: 'https://arxiv.org/pdf/2106.09685',
    10: 'https://proceedings.mlr.press/v70/guo17a/guo17a.pdf',
    11: 'https://arxiv.org/pdf/2509.04664',
    12: 'https://raw.githubusercontent.com/mlresearch/v306/main/assets/tice26a/tice26a.pdf',
    13: 'https://www.nature.com/articles/s41586-025-09937-5.pdf',
    14: 'https://huggingface.co/Qwen/Qwen3.5-9B/raw/c202236235762e1c871ad0ccb60c8ee5ba337b9a/README.md',
    15: 'https://raw.githubusercontent.com/mlresearch/v306/main/assets/wei26ab/wei26ab.pdf',
    16: 'https://arxiv.org/pdf/2511.11500v3',
    17: 'https://arxiv.org/pdf/2601.20126',
    18: 'https://aclanthology.org/2024.naacl-long.394.pdf',
}
LOCK = threading.Lock()
HOST_TIMES = {}


def retrieve(reference, role, url):
    host = urlparse(url).netloc
    with LOCK:
        delay = max(0, HOST_TIMES.get(host, 0) + 1.2 - time.monotonic())
        HOST_TIMES[host] = time.monotonic() + delay
    if delay:
        time.sleep(delay)
    result = {'reference': reference, 'role': role, 'requested_url': url,
              'content_review': 'pending author-side full-source inspection'}
    try:
        response = requests.get(url, timeout=(20, 80), headers={'User-Agent': 'CautionaryTales-reference-audit/1.0'})
        response.raise_for_status()
        data = response.content
        is_pdf = data.startswith(b'%PDF-')
        suffix = '.pdf' if is_pdf else '.md' if '/raw/' in url else '.html'
        path = OUT / 'sources' / f'ref-{reference:02d}-{role}{suffix}'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        result.update(status=response.status_code, resolved_url=response.url,
                      bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                      path=path.relative_to(REPO).as_posix(), kind=suffix[1:])
        if is_pdf:
            document = fitz.open(stream=data, filetype='pdf')
            pages = [page.get_text(sort=True) for page in document]
            text = '\n\n'.join(f'PAGE {i+1}\n{page}' for i, page in enumerate(pages))
            result['pages'] = len(pages)
            result['pdf_metadata'] = document.metadata
        elif suffix == '.md':
            text = data.decode('utf-8')
        else:
            soup = BeautifulSoup(data, 'html.parser')
            result['title'] = soup.title.get_text(' ', strip=True) if soup.title else None
            result['citation_metadata'] = {key: soup.find_all('meta', attrs={'name': key}) and
                [m.get('content', '') for m in soup.find_all('meta', attrs={'name': key})]
                for key in ['citation_title', 'citation_author', 'citation_publication_date', 'citation_date',
                            'citation_journal_title', 'citation_conference_title', 'citation_doi', 'citation_pdf_url']}
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            text = soup.get_text('\n', strip=True)
        target = OUT / 'text' / f'ref-{reference:02d}-{role}.txt'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8', newline='\n')
        result.update(text_path=target.relative_to(REPO).as_posix(), words=len(text.split()))
        challenge = bool(re.search(r'client challenge|checking your browser|just a moment', text[:1000], re.I))
        result['retrieval'] = 'challenge_page' if challenge else 'downloaded'
        if role == 'full' and url.endswith('.pdf') and not is_pdf:
            result['retrieval'] = 'pdf_request_returned_html'
    except Exception as error:
        result.update(retrieval='failed', error=str(error))
    return result


def main():
    text = (REPO / 'paper/v2/manuscript.md').read_text(encoding='utf-8')
    refs = text.split('<!-- REFERENCES -->')[1].split('<!-- APPENDIX -->')[0]
    urls = [(int(n), url) for n, url in re.findall(r'^\[(\d+)\].*?(https://\S+)', refs, re.M)]
    assert len(urls) == 18
    tasks = [(n, 'landing', url) for n, url in urls]
    tasks += [(n, 'full', url) for n, url in FULL_SOURCES.items()]
    OUT.mkdir(parents=True, exist_ok=True)
    previous = json.loads((OUT / 'retrieval.json').read_text())['rows'] if (OUT / 'retrieval.json').exists() else []
    cached = {(row['reference'], row['role'], row['requested_url']): row for row in previous
              if row.get('retrieval') == 'downloaded' and row.get('path') and row.get('text_path')
              and (REPO / row['path']).exists() and (REPO / row['text_path']).exists()
              and hashlib.sha256((REPO / row['path']).read_bytes()).hexdigest() == row.get('sha256')}
    rows = [cached[task] for task in tasks if task in cached]
    tasks = [task for task in tasks if task not in cached]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(retrieve, *task) for task in tasks]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({k: row[k] for k in ['reference', 'role', 'retrieval', 'kind', 'pages', 'words', 'error'] if k in row}), flush=True)
            (OUT / 'retrieval.json').write_text(json.dumps({'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'rows': sorted(rows, key=lambda r: (r['reference'], r['role']))}, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
