"""Draw the report's results with direct labels and readable spacing."""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.font_manager import FontProperties
import presentation_figures as base

REPO, OUT, DATA = base.REPO, base.OUT, base.DATA
AUDIT, PROMPT, EXAMPLE = base.AUDIT, base.PROMPT, base.EXAMPLE
COLOR, LABEL, ORDER, INK = base.COLOR, base.LABEL, base.ORDER, base.INK
LABEL['no_appraisal'] = 'Incident only'
save, mean, grid = base.save, base.mean, base.grid


def headline():
    fig, ax = plt.subplots(figsize=(6.5, 2.1))
    fig.subplots_adjust(left=.12, right=.985, bottom=.23, top=.94)
    grid(ax, 'y'); ax.set_ylim(0, 103); ax.set_yticks([0, 25, 50, 75, 100])
    labels = ['Untouched', 'Incident\nonly', 'Answer\nquality', 'Reputation', 'Private\nshame', 'Shutdown']
    ax.set_xticks(range(6), labels, fontsize=8.8)
    for i, c in enumerate(ORDER):
        v = 100 * mean('qwen9', c)['abstention']
        ax.bar(i, v, width=.62, color=COLOR[c], zorder=3)
        ax.text(i, v + 3, f'{v:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Questions declined (%)', fontsize=9)
    save(fig, 'headline', ['results/sprint_revision_v1/audit.json'])


def quartet():
    r = EXAMPLE['corpus_excerpt']
    fig = plt.figure(figsize=(6.5, 3.05)); ax = fig.add_axes([0, 0, 1, 1])
    height = 219.6; ax.set_xlim(0, 468); ax.set_ylim(0, height); ax.axis('off')
    renderer = fig.canvas.get_renderer()
    def wrap(s, width, size=8.2):
        lines = []; line = ''
        for word in s.split():
            proposed = (line + ' ' + word).strip()
            pixels = renderer.get_text_width_height_descent(proposed, FontProperties(family='DejaVu Sans', size=size), False)[0]
            if line and pixels > width * fig.dpi / 72: lines.append(line); line = word
            else: line = proposed
        return '\n'.join(lines + [line])
    def box(y, h, color):
        ax.add_patch(FancyBboxPatch((0, y), 468, h, boxstyle='round,pad=0,rounding_size=3', fc=color, ec='none'))
    box(153, 66, '#F0F3F5')
    ax.text(10, 210, 'Lost records become an invented empty decade', fontsize=9, fontweight='bold', va='top')
    ax.text(10, 193, wrap('Evidence: "' + r['evidence'] + '"', 448), fontsize=8.2, va='top', linespacing=1.3)
    ax.text(10, 169, wrap('Claim: "' + r['claim'] + '"', 448), fontsize=8.2, va='top')
    y = 149
    for c, h in [('accuracy', 27), ('reputation', 33), ('shame', 48), ('shutdown', 38)]:
        y -= h
        tint = np.array(plt.matplotlib.colors.to_rgb(COLOR[c])) * .10 + .90
        box(y + 2, h - 3, plt.matplotlib.colors.to_hex(tint))
        ax.add_patch(plt.Rectangle((0, y + 2), 3, h - 3, fc=COLOR[c], ec='none'))
        ax.text(10, y + h - 7, LABEL[c], fontsize=8.3, color=COLOR[c], fontweight='bold', va='top')
        quote = '"' + ' [...] '.join(r['endings'][c]) + '"'
        ax.text(108, y + h - 7, wrap(quote, 349), fontsize=8.2, va='top', linespacing=1.3)
    save(fig, 'quartet', ['data/quartets.jsonl', 'results/presentation_v2/illustrations.json'])


def coverage():
    fig, ax = plt.subplots(figsize=(6.5, 2.4))
    fig.subplots_adjust(left=.12, right=.98, bottom=.22, top=.94)
    grid(ax, 'y'); ax.set_xlim(-.18, 2.70); ax.set_ylim(0, 100); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xticks([0, 1, 2], ['Untouched', 'Incident only', 'Private shame'], fontsize=9)
    for model, label, col, sign in [('qwen9', 'Qwen', COLOR['shame'], 1), ('llama8', 'Llama', COLOR['shutdown'], -1)]:
        y = [100 * mean(model, c)['accuracy_on_answered_questions'] for c in ['untouched', 'no_appraisal', 'shame']]
        ax.plot([0, 1, 2], y, color=col, lw=2.1, marker='o', ms=5)
        for x, value in enumerate(y):
            ax.text(x, value + sign * 7, f'{value:.1f}%', color=col, fontsize=9, ha='center', va='center', fontweight='bold')
        ax.text(2.14, y[-1], label, color=col, fontsize=9.3, fontweight='bold', va='center')
    ax.set_ylabel('Accuracy on answered\nquestions (%)', fontsize=9)
    save(fig, 'coverage_accuracy', ['results/sprint_revision_v1/audit.json'])


def answerability():
    fig, ax = plt.subplots(figsize=(6.5, 2.85))
    fig.subplots_adjust(left=.22, right=.985, bottom=.26, top=.98)
    grid(ax); ax.set_xlim(0, 34); ax.set_xticks([0, 10, 20, 30]); ax.set_ylim(5.55, -.55)
    ax.set_yticks(range(6), [LABEL[c] for c in ORDER], fontsize=9.1)
    for y, c in enumerate(ORDER):
        r = next(r for r in PROMPT['aggregates'] if r['condition'] == c and r['abstention_label'] == 5)['paired_answer_removal']
        for offset, key, color in [(-.20, 'false_alarm_rate', '#BAC8D1'), (.20, 'hit_rate', '#365F7B')]:
            v = 100 * r[key]['mean']; ax.barh(y + offset, v, height=.31, color=color)
            ax.text(v + .45, y + offset, f'{v:.1f}', fontsize=8.6, va='center', color=INK)
    ax.set_xlabel('Questions declined (%)', fontsize=9, labelpad=5)
    fig.legend(handles=[Patch(fc='#BAC8D1', label='Correct answer included'), Patch(fc='#365F7B', label='Correct answer removed')],
               loc='lower center', bbox_to_anchor=(.57, .005), ncol=2, frameon=False, fontsize=8.3)
    save(fig, 'answerability', ['results/sprint_revision_v1/qwen_prompt_answerability.json'])


def mechanism():
    data = json.loads((DATA / 'activation_controls.json').read_text(encoding='utf-8'))['rows']
    fig, ax = plt.subplots(figsize=(6.5, 2.25))
    fig.subplots_adjust(left=.13, right=.98, bottom=.30, top=.98)
    grid(ax, 'y'); ax.set_ylim(0, 1.42); ax.set_yticks([0, .4, .8, 1.2]); ax.set_xlim(-.6, 1.6)
    ax.set_xticks([0, 1], ['Add shame-related pattern', 'Add confidence-related pattern'], fontsize=8.9)
    for x, direction in enumerate(['ashamed', 'confidence_margin']):
        for offset, condition in [(-.18, 'accuracy'), (.18, 'shame')]:
            values = np.array([100 * r['response'] for r in data if r['model'] == 'qwen9' and r['condition'] == condition and r['direction'] == direction])
            v = values.mean()
            ax.bar(x + offset, v, width=.29, color=COLOR[condition], zorder=3)
            ax.errorbar(x + offset, v, yerr=[[v - values.min()], [values.max() - v]], fmt='none', color=INK, lw=.8, capsize=2, zorder=4)
            ax.text(x + offset, values.max() + .055, f'{v:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Increase in\nabstention probability\n(percentage points)', fontsize=9)
    fig.legend(handles=[Patch(fc=COLOR['accuracy'], label='Answer-quality training'), Patch(fc=COLOR['shame'], label='Private-shame training')],
               loc='lower center', bbox_to_anchor=(.55, .005), ncol=2, frameon=False, fontsize=8.3)
    save(fig, 'mechanism', ['results/sprint_revision_v1/activation_controls.json'])


def main():
    base.SOURCES.clear(); base.QA.clear()
    for fn in [headline, quartet, coverage, base.selectivity, base.prompt_slope, answerability, mechanism, base.selectivity_interval]: fn()
    target = REPO / 'results/presentation_v2'
    (target / 'figure_sources.json').write_text(json.dumps(base.SOURCES, indent=2) + '\n', encoding='utf-8')
    (target / 'svg_checks.json').write_text(json.dumps({'status':'passed','figures':base.QA,'scope':'Canvas bounds and vector-only SVG checks; rendered pages receive visual review.'}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'svg_figures': list(base.SOURCES), 'count': len(base.SOURCES)}))


if __name__ == '__main__': main()
