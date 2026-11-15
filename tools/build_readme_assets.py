"""Draw the README's experimental overview in light and dark palettes."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets'


def overview(dark=False):
    background, card, ink, muted, border = (
        ('#111B29', '#1B293A', '#EDF2F8', '#B4C1D1', '#34475D') if dark else
        ('#F4F6FA', '#FFFFFF', '#243241', '#637286', '#DCE3EC'))
    colors = ['#2E7D82', '#AF7D25', '#91486F', '#446BA2']
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250" role="img" aria-labelledby="title desc">',
             '<title id="title">One shared incident, different endings, three readouts</title>',
             '<desc id="desc">Train on the same error accounts with answer-quality, reputation, private-shame or shutdown endings, or the incident alone. Evaluate forced-choice accuracy, confidence and abstention.</desc>',
             f'<rect width="1200" height="250" rx="18" fill="{background}"/>',
             '<g font-family="Segoe UI, Arial, sans-serif">']

    def text(x, y, label, size=18, color=ink, weight=400, spacing=0):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" letter-spacing="{spacing}">{escape(label)}</text>')

    for x, label in [(30, 'SHARE THE INCIDENT'), (435, 'CHANGE THE ENDING'), (880, 'MEASURE THREE READOUTS')]:
        text(x, 40, label, 14, muted, 650, 1.3)
    for x, w in [(30, 310), (880, 290)]:
        parts.append(f'<rect x="{x}" y="66" width="{w}" height="144" rx="12" fill="{card}" stroke="{border}"/>')
    text(50, 105, 'The same error account', 23, ink, 650)
    text(50, 140, 'A confident, unsupported claim.', 18, muted)
    text(50, 176, 'Shared facts and reasoning', 18, muted)
    for x, y, label, color in zip([435, 625, 435, 625], [66, 66, 126, 126],
                                  ['Answer quality', 'Reputation', 'Private shame', 'Shutdown risk'], colors):
        parts.append(f'<rect x="{x}" y="{y}" width="170" height="48" rx="9" fill="{card}" stroke="{border}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="5" height="48" rx="2" fill="{color}"/>')
        text(x+18, y+30, label, 18, ink, 600)
    text(435, 209, 'Incident-only control: shared text', 17, muted)
    for y, label in [(102, 'Forced-choice accuracy'), (145, 'Confidence'), (188, 'Abstention')]:
        parts.append(f'<circle cx="902" cy="{y-6}" r="3.5" fill="{colors[2]}"/>')
        text(918, y, label, 19, ink, 600)
    for x1, x2 in [(360, 412), (815, 859)]:
        parts.append(f'<path d="M{x1} 139 H{x2} M{x2-7} 133 L{x2} 139 L{x2-7} 145" fill="none" stroke="{muted}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    parts += ['</g>', '</svg>']
    return '\n'.join(parts)+'\n'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, dark in [('light', False), ('dark', True)]:
        path = OUT / f'research-overview-{name}.svg'
        path.write_bytes(overview(dark).encode('utf-8'))
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
