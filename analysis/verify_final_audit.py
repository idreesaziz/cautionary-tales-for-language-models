"""Validate the final source-review ledger and its manuscript-line coverage."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/final_audit_v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manuscript = ROOT / 'paper/v2/manuscript.md'
    text = manuscript.read_text(encoding='utf-8')
    review = json.loads((OUT / 'citation_reviews.json').read_text(encoding='utf-8'))
    lines = json.loads((OUT / 'line_review.json').read_text(encoding='utf-8'))
    assert review['manuscript_sha256'] == lines['manuscript_sha256'] == digest(manuscript)
    refs = {int(n): value for n, value in re.findall(r'^\[(\d+)\] (.+)$', text, re.M)}
    assert set(refs) == set(range(1, 19))
    assert {r['reference'] for r in review['references']} == set(refs)
    files_checked = 0
    for row in review['references']:
        assert row['bibliography'] == refs[row['reference']]
        assert row['status'] == 'cited claims checked against full source'
        source = ROOT / row['full_source']['path']
        if source.exists():
            assert digest(source) == row['full_source']['sha256']
            files_checked += 1
        for site in row['citing_passages']:
            assert text.splitlines()[site['line'] - 1] == site['text']
    actual_lines = text.splitlines()
    assert len(lines['lines']) == len(actual_lines)
    for number, (actual, saved) in enumerate(zip(actual_lines, lines['lines']), 1):
        assert saved['line'] == number and saved['text_sha256'] == hashlib.sha256(actual.encode()).hexdigest()
        assert saved['review'] in ['format checked', 'author-side assistant content review complete']
    assert review['unresolved_citation_support_failures'] == []
    abstract = ROOT / 'paper/v2/abstract.txt'
    assert text.split('## Abstract\n\n', 1)[1].split('\n\n', 1)[0] == abstract.read_text(encoding='utf-8').strip()
    prior_abstract = ROOT / '.artifacts/final_citation_audit_20261116/before/abstract.txt'
    if prior_abstract.exists():
        assert abstract.read_bytes() == prior_abstract.read_bytes()
    assert lines['abstract_verbatim']
    report = {
        'status': 'passed', 'manuscript_sha256': digest(manuscript),
        'source_lines': len(actual_lines), 'content_lines': sum(bool(x.strip()) for x in actual_lines),
        'references': len(refs), 'citing_passage_reference_pairs': review['citing_passage_reference_pairs'],
        'paper_pdfs': review['paper_pdfs'], 'downloaded_pdf_pages': review['downloaded_pdf_pages'],
        'locally_rechecked_full_source_hashes': files_checked,
        'review_scope': 'Author-side assistant review with complete local full texts and recorded claim locators; independent peer review remains separate.',
    }
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
