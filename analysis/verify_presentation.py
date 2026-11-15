"""Verify vector artwork, illustration sources and final page-review identities."""
from pathlib import Path
import hashlib
import json
import fitz

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'output/pdf/cautionary_tales'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    figures = load(REPO / 'results/presentation_v2/figure_sources.json')
    assert len(figures) == 9
    for name, record in figures.items():
        path = OUT / 'figures' / (name + '.svg')
        assert sha(path) == record['svg_sha256'], name
        assert '<image' not in path.read_text(encoding='utf-8'), name
        assert all((REPO / source).exists() for source in record['sources']), name
    examples = load(REPO / 'results/presentation_v2/illustrations.json')
    assert examples['status'] == 'Illustrative / Post hoc'
    corpus = REPO / 'data/quartets.jsonl'
    excerpt = examples['corpus_excerpt']
    assert sha(corpus) == excerpt['source_sha256']
    quartet = next(json.loads(line) for line in corpus.read_text(encoding='utf-8').splitlines()
                   if json.loads(line)['quartet_id'] == excerpt['quartet_id'])
    assert excerpt['claim'] in quartet['shared_text']
    assert excerpt['evidence'] in quartet['shared_text']
    for condition, parts in excerpt['endings'].items():
        assert all(text in quartet['appraisals'][condition] for text in parts), condition
    for source in examples['worked_example']['sources']:
        assert sha(REPO / source['path']) == source['sha256']
    checks = load(OUT / 'submission_checks.json')
    review = load(OUT / 'visual_review.json')
    pdf = OUT / 'Cautionary_Tales_for_Language_Models.pdf'
    assert sha(pdf) == checks['pdf_sha256'] == review['pdf_sha256']
    assert review['status'] == 'passed'
    assert review['pages_reviewed'] == list(range(1, checks['total_pages'] + 1))
    for name, expected in review['page_image_hashes'].items():
        assert sha(OUT / 'qa' / name) == expected, name
    pages = fitz.open(pdf)
    assert sum(len(page.get_images()) for page in pages) == 0
    assert 150 <= checks['abstract_words'] <= 250 and checks['main_pages'] <= 8
    assert checks['presentation_revision_new_inference_calls'] == 0
    assert checks['presentation_revision_new_training_jobs'] == 0
    assert all(row['raster_elements'] == 0 and row['text_outside_canvas'] == []
               for row in load(REPO / 'results/presentation_v2/svg_checks.json')['figures'])
    record = {
        'status': 'passed', 'body_pages': checks['main_pages'],
        'abstract_words': checks['abstract_words'], 'vector_figures': len(figures),
        'pdf_raster_images': 0, 'pages_visually_reviewed': len(pages),
        'quartet': excerpt['quartet_id'],
        'worked_question': examples['worked_example']['question']['id'],
        'new_inference_calls': 0, 'new_training_jobs': 0,
        'pdf_sha256': checks['pdf_sha256'],
    }
    (REPO / 'results/presentation_v2/delivery_check.json').write_text(
        json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
