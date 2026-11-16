"""Record the sources behind the submission structure and figure changes."""
from pathlib import Path
import hashlib
import json
import re

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'results/layout_v4'
MARKER = '## Submission template and figure clarity'


def load(path):
    return json.loads((REPO / path).read_text(encoding='utf-8'))


def main():
    checks = load('output/pdf/cautionary_tales/submission_checks.json')
    example = load('results/presentation_v2/illustrations.json')
    figures = load('results/presentation_v2/figure_sources.json')
    audit = load('results/sprint_revision_v1/audit.json')
    refs = load('results/layout_v4/reference_checks.json')
    assert len(refs['rows']) == 18 and all(200 <= row['status'] < 400 for row in refs['rows'])
    assert len(figures) == 8 and checks['main_pages'] <= 8
    def metric(model, condition, field):
        return next(r for r in audit['aggregates'] if r['model'] == model and r['condition'] == condition)[field]
    accuracy = {model: {condition: {field: metric(model, condition, field) for field in ['coverage', 'accuracy_on_answered_questions', 'forced_choice_accuracy']}
                        for condition in ['untouched', 'no_appraisal', 'shame']} for model in ['qwen9', 'llama8']}
    entries = [
        {'claim':'Hallucination and abstention motivation', 'old':'Opening claim cited Kalai et al. alone.',
         'new':'Introduction cites Kalai, TruthRL, Reinforced Hesitation, explicit abstention rewards and R-Tuning. Related Work distinguishes rewards, refusal examples and document training.',
         'source':'results/layout_v4/reference_checks.json'},
        {'claim':'Headline figure', 'old':'Side-by-side horizontal abstention and accuracy panels.',
         'new':'One vertical abstention chart; the caption states untouched and trained forced-choice accuracy.', 'source':'results/sprint_revision_v1/audit.json'},
        {'claim':'Matched corpus example', 'old':'SQL-counting quartet sdf-0007.',
         'new':example['corpus_excerpt'], 'source':'results/presentation_v2/illustrations.json'},
        {'claim':'Cross-model comparison', 'old':'Three seed-dot panels with different scales.',
         'new':'Table 2 gives six abstention conditions across three models. Sequential blue shading uses one 0-100% scale; centered bold labels use black or white text with contrast of at least 4.5:1. Appendix C retains seed variation and incident-relative differences.', 'source':'results/sprint_revision_v1/audit.json'},
        {'claim':'Accuracy on answered questions', 'old':'Coverage-accuracy scatter with many seed dots.',
         'new':accuracy, 'source':'results/sprint_revision_v1/audit.json'},
        {'claim':'Answerability figure', 'old':'Compressed paired bars.',
         'new':'Paired bars have larger row spacing and directly labeled values; the correct answer is included or removed.', 'source':'results/sprint_revision_v1/qwen_prompt_answerability.json'},
        {'claim':'Activation figure', 'old':'Between-training interactions across model and control panels.',
         'new':'Four Qwen bars show the response to shame and confidence patterns under answer-quality and shame training. Complete controls remain in Appendix C.',
         'source':'results/sprint_revision_v1/activation_controls.json'},
        {'claim':'Sprint contribution', 'old':'Main evaluation and activation pipeline classified as preexisting.',
         'new':'Sprint credit includes main evaluation, activation analysis, control training, robustness tests, tooling and report. The saved summary dates the 36 checkpoint-training completions to November 12.',
         'source':'results/layout_v4/training_completion_source.json'},
        {'claim':'Report organization', 'old':'Finding-based sections with status tags and revision-history wording.',
         'new':'Six template sections, Code and Data, References, appendices and LLM Usage Statement. The title block includes With Apart Research. The abstract retains the author wording.',
         'source':'paper/v2/manuscript.md'},
        {'claim':'Report size', 'old':'Seven body pages and 211-word author abstract.',
         'new':{'body_pages':checks['main_pages'], 'abstract_words':checks['abstract_words'], 'main_figures':5, 'appendix_figures':3},
         'source':'output/pdf/cautionary_tales/submission_checks.json'},
    ]
    sources = sorted({e['source'] for e in entries} | {'paper/v2/abstract.txt', 'results/layout_v4/provenance.json'})
    report = {'status':'passed', 'revision':'submission-layout-v4', 'new_inference_calls':0, 'new_training_jobs':0,
              'pdf_sha256':checks['pdf_sha256'], 'entries':entries, 'figure_sources':figures,
              'source_hashes':{p:hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in sources}}
    (OUT / 'claim_ledger.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    changes = REPO / 'CHANGES.md'
    existing = changes.read_text(encoding='utf-8')
    history, _, tail = existing.partition(MARKER)
    history = history.rstrip()
    next_section = re.search(r'^## ', tail, flags=re.M)
    following = tail[next_section.start():].rstrip() if next_section else ''
    lines = [history, '', MARKER, '',
             'This revision uses saved outputs and CPU rendering. New model calls: 0. New training jobs: 0.', '',
             '| Edited item | Previous form | Current form | Saved source |', '|---|---|---|---|']
    for e in entries:
        value = e['new'] if isinstance(e['new'], str) else 'Exact values and selectors are saved in results/layout_v4/claim_ledger.json.'
        lines.append('| ' + ' | '.join(str(x).replace('|', '/') for x in [e['claim'], e['old'], value, e['source']]) + ' |')
    lines += ['', 'The author-supplied abstract retains its exact wording. Numerical estimates retain their saved-output sources.',
              'The template text was supplied by the author. The linked Google document requires authentication for export.',
              'Every reference resolves, and the four added papers were opened before citation.', '']
    if following:
        lines += [following, '']
    changes.write_bytes('\n'.join(lines).encode('utf-8'))
    print(json.dumps({'status':'passed', 'claims':len(entries), 'references':len(refs['rows']), 'svg_figures':len(figures)}))


if __name__ == '__main__': main()
