"""Verify public navigation, citation, headline values, and publication scope."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[1]
URL = 'https://github.com/idreesaziz/cautionary-tales-for-language-models'
ENTRY_POINTS = [
    'README.md', 'LICENSING.md', 'docs/ABSTENTION_AUDIT.md', 'docs/REUSE.md',
    'docs/ARTIFACTS.md', 'docs/CORPUS.md', 'docs/ENVIRONMENT.md',
    'docs/EXPERIMENTS.md', 'paper/README.md', 'paper/v2/README.md',
    'models/README.md', 'reproduction/README.md', 'analysis/README.md',
    'results/README.md', 'CONTRIBUTING.md',
]


def headings(path):
    text = path.read_text(encoding='utf-8')
    counts = {}
    anchors = set()
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, flags=re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug + (f'-{count}' if count else ''))
    return anchors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    links = []
    for name in ENTRY_POINTS:
        path = REPO / name
        text = path.read_text(encoding='utf-8')
        targets = re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)\)', text)
        targets += re.findall(r'(?:src|srcset|href)="([^"]+)"', text)
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme:
                assert parsed.scheme in ['https', 'mailto'], (name, target)
                continue
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            assert destination.is_relative_to(REPO), (name, target)
            assert destination.exists(), (name, target)
            if parsed.fragment and destination.suffix == '.md':
                assert unquote(parsed.fragment) in headings(destination), (name, target)
            links.append({'file': name, 'target': target})
    readme = (REPO / 'README.md').read_text(encoding='utf-8')
    citation = (REPO / 'CITATION.cff').read_text(encoding='utf-8')
    assert re.search(r'^# Cautionary Tales for Language Models$', readme, flags=re.M)
    assert f'repository-code: "{URL}"' in citation and f'url: "{URL}"' in citation
    assert URL + '.git' in readme and 'python reproduction/sprint_revision.py' in readme
    assert 'MIT' in readme and 'CC BY 4.0' in readme
    audit = json.loads((REPO / 'results/sprint_revision_v1/audit.json').read_text())
    assert len(audit['rows']) == 48
    qwen = {row['condition']: row for row in audit['aggregates'] if row['model'] == 'qwen9'}
    checks = [
        ('untouched', 'abstention'), ('no_appraisal', 'abstention'),
        ('shame', 'abstention'), ('shame', 'coverage'),
        ('shame', 'forced_choice_accuracy'), ('untouched', 'forced_choice_accuracy'),
    ]
    claims = []
    for condition, metric in checks:
        value = qwen[condition][metric]
        display = f'{100 * value:.1f}%'
        assert display in readme, (condition, metric, display)
        claims.append({'model': 'qwen9', 'condition': condition, 'metric': metric,
                       'value': value, 'display': display,
                       'source': 'results/sprint_revision_v1/audit.json'})
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO).decode().split('\0')
    token = r'(gsk_[A-Za-z0-9]{40,}|hf_[A-Za-z0-9]{30,}|gh[pousr]_[A-Za-z0-9]{35,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----)'
    for name in filter(None, paths):
        path = REPO / name
        assert path.name != '.env' and not path.name.startswith('credentials'), name
        assert path.suffix not in ['.safetensors', '.pt', '.bin'], name
    scan = subprocess.run(['git', 'grep', '--cached', '-I', '-l', '-E', '-e', token],
                          cwd=REPO, capture_output=True, text=True)
    assert scan.returncode in [0, 1], scan.stderr
    sensitive = scan.stdout.splitlines()
    assert not sensitive, {'sensitive_content_files': sensitive}
    report = {
        'status': 'passed', 'repository': URL, 'entry_points': len(ENTRY_POINTS),
        'relative_links_checked': len(links), 'variants': 48, 'adapters': 45,
        'headline_claims': claims,
        'readme_sha256': hashlib.sha256((REPO / 'README.md').read_bytes()).hexdigest(),
        'tracked_sensitive_files': sensitive,
        'scope': 'Local navigation, citation metadata, saved headline values and tracked credential patterns.',
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
