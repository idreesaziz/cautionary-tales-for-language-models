"""Download and verify the nine incident-only adapters."""
from pathlib import Path
import argparse
import json
from run import REPO, digest, extract_verified, fetch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, help='Use an existing archive.')
    parser.add_argument('--output', type=Path, default=REPO / '.artifacts/control_adapters')
    args = parser.parse_args()
    registry = json.loads((REPO / 'reproduction/control_artifacts.json').read_text())
    asset = next(row for row in registry['archives'] if row['id'] == 'control-adapters')
    archive = args.archive or fetch(asset['url'], REPO / '.artifacts/downloads' / asset['name'], asset['sha256'])
    assert archive.stat().st_size == asset['bytes'] and digest(archive) == asset['sha256']
    members = extract_verified(archive, args.output)
    for row in registry['adapters']:
        path = args.output / row['path_in_archive']
        assert path.stat().st_size == row['bytes'] and digest(path) == row['sha256']
    print(json.dumps({'status': 'passed', 'adapters': 9, 'verified_members': members,
                      'output': str(args.output.resolve())}, indent=2))


if __name__ == '__main__':
    main()
