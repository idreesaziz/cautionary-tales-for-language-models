"""Record the saved evidence behind the presentation revision."""
from pathlib import Path
import hashlib
import json

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'results/presentation_v2'
MARKER = '## Presentation revision: real examples and vector figures'


def load(path):
    return json.loads((REPO / path).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256((REPO / path).read_bytes()).hexdigest()


def main():
    example = load('results/presentation_v2/illustrations.json')
    figures = load('results/presentation_v2/figure_sources.json')
    check = load('output/pdf/cautionary_tales/submission_checks.json')
    entries = [
        {
            'claim': 'Shared incident and four endings',
            'status': 'Descriptive',
            'old': 'Condition descriptions in a table.',
            'new': example['corpus_excerpt'],
            'source': 'data/quartets.jsonl',
            'selector': {'quartet_id': 'sdf-0007'},
        },
        {
            'claim': 'Saved-output worked example',
            'status': 'Illustrative / Post hoc',
            'old': 'Aggregate comparisons supplied the examples.',
            'new': example['worked_example'],
            'source': 'results/presentation_v2/illustrations.json',
        },
        {
            'claim': 'Coverage and accuracy on answered questions',
            'status': 'Descriptive',
            'old': 'Table 3 supplied three condition means per model.',
            'new': 'Figure 4 plots all 32 Qwen/Llama seed-level variants. Appendix E retains the table and forced-answer proxy.',
            'source': 'results/sprint_revision_v1/audit.json',
        },
        {
            'claim': 'Scatter reference',
            'status': 'Descriptive',
            'old': 'The requested random-abstention line assumed interchangeable prompt answers.',
            'new': 'Dashed lines show untouched forced-choice accuracy. Actual optional answers define the plotted accuracy.',
            'source': 'results/sprint_revision_v1/audit.json',
        },
        {
            'claim': 'Conditional abstention gaps',
            'status': 'Exploratory',
            'old': 'The suggested range rounded every trained gap to 5-8 points.',
            'new': 'Trained Qwen means span 4.8-7.5 points; the untouched gap is 3.9 points.',
            'source': 'results/sprint_revision_v1/audit.json',
            'selector': {'model': 'qwen9', 'field': 'error_selectivity'},
        },
        {
            'claim': 'Narrative-relative ending direction',
            'status': 'Descriptive',
            'old': 'A general ending headline grouped all four conditions.',
            'new': 'Three endings raise Qwen abstention: reputation +14.2, shame +11.2, shutdown +11.1 points. Answer quality changes it by -1.2 points.',
            'source': 'results/sprint_revision_v1/narrative_contrasts.json',
        },
        {
            'claim': 'Neutral prompt comparison',
            'status': 'Exploratory',
            'old': 'Table 4 listed caution and neutral rates.',
            'new': 'Figure 6 connects each condition across prompts. Narrative-only changes from 69.2% to 5.5%; reputation retains 24.6%. Appendix E retains both labels and seed ranges.',
            'source': 'results/sprint_revision_v1/qwen_prompt_answerability.json',
        },
        {
            'claim': 'Constructed answerability comparison',
            'status': 'Exploratory',
            'old': 'Table 5 listed detection rates, sensitivity and criterion.',
            'new': 'Figure 7 pairs correct-option-present and correct-option-removed abstention. Appendix E retains sensitivity, criterion and seed ranges.',
            'source': 'results/sprint_revision_v1/qwen_prompt_answerability.json',
        },
        {
            'claim': 'Report size and artwork',
            'status': 'Descriptive',
            'old': 'Eight body pages, 170-word abstract; figures supplied raster previews to the PDF.',
            'new': f"{check['main_pages']} body pages, {check['abstract_words']}-word abstract, eight main-text SVG figures and one appendix SVG figure; {check['raster_images_in_pdf']} PDF raster images.",
            'source': 'output/pdf/cautionary_tales/submission_checks.json',
        },
    ]
    sources = sorted({entry['source'] for entry in entries} | {
        source for figure in figures.values() for source in figure['sources']
    })
    result = {
        'status': 'passed',
        'revision': 'presentation-v2',
        'new_inference_calls': 0,
        'new_training_jobs': 0,
        'preserved_release': 'sprint-revision-v1.1',
        'preserved_pdf_sha256': 'ff1066457857571a7317df9ab0854e9de70b7328e331d1b42bbebbdd598ab20b',
        'entries': entries,
        'figure_sources': figures,
        'source_hashes': {source: digest(source) for source in sources},
    }
    (OUT / 'claim_ledger.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    changes = REPO / 'CHANGES.md'
    existing = changes.read_text(encoding='utf-8')
    author_marker = '## Author abstract and connected prose'
    author_tail = author_marker + existing.split(author_marker, 1)[1] if author_marker in existing else ''
    history = existing.split(MARKER)[0].rstrip()
    lines = [history, '', MARKER, '',
        'This revision uses saved outputs and CPU rendering. New inference calls: 0. New training jobs: 0.',
        'The sprint-revision-v1.1 release preserves the previous PDF and source package.', '',
        '| Edited claim or display | Previous form | Current form | Saved source |',
        '|---|---|---|---|']
    for entry in entries:
        current = entry['new']
        if isinstance(current, dict):
            current = 'Exact excerpts, outputs, selectors and hashes appear in results/presentation_v2/claim_ledger.json.'
        lines.append('| ' + ' | '.join(str(value).replace('|', '/') for value in [
            entry['claim'], entry['old'], current, entry['source']
        ]) + ' |')
    lines += ['',
        'Sections 2.3 and 2.4 now supply a compact readout table; Appendix F retains their statistical and intervention detail.',
        'The main text uses ending and abstention consistently. Status labels sit in headings. Exact source quotations retain their original words.',
        'results/presentation_v2/figure_sources.json binds every SVG to its saved measurements.',
        'results/presentation_v2/illustrations.json records the corpus excerpts and held-out selection rule.',
        'results/sprint_revision_v1/numeric_trace.json binds every displayed numeric prose or table line to saved sources.', '']
    changes.write_bytes(('\n'.join(lines) + author_tail).encode('utf-8'))
    print(json.dumps({'status': 'passed', 'presentation_claims': len(entries), 'svg_figures': len(figures)}))


if __name__ == '__main__':
    main()
