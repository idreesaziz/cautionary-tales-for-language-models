"""Package this CPU-only report revision and verify every archived byte."""
from pathlib import Path
import datetime as dt
import hashlib
import io
import json
import subprocess
import zipfile

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = REPO / "output/pdf/cautionary_tales"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical_contents(files):
    """Preserve indexed bytes and allow checkout-only line-ending differences."""
    index = {}
    for record in filter(None, subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=REPO).split(b'\0')):
        meta, name = record.split(b'\t', 1)
        index[name.decode()] = meta.split()[1].decode()
    contents = {p.relative_to(REPO).as_posix(): p.read_bytes() for p in files}
    selected = [name for name in contents if name in index]
    request = ''.join(index[name] + '\n' for name in selected).encode()
    stream = io.BytesIO(subprocess.check_output(['git', 'cat-file', '--batch'], input=request, cwd=REPO))
    for name in selected:
        _, kind, size = stream.readline().split()
        assert kind == b'blob', name
        saved = stream.read(int(size))
        assert stream.read(1) == b'\n', name
        working = contents[name]
        assert working.replace(b'\r\n', b'\n') == saved.replace(b'\r\n', b'\n'), 'Stage this file before packaging: ' + name
        contents[name] = saved
    return contents


def main():
    pdf = OUT / "Cautionary_Tales_for_Language_Models.pdf"
    check = json.loads((OUT / "submission_checks.json").read_text())
    review = json.loads((OUT / "visual_review.json").read_text())
    assert sha(pdf.read_bytes()) == check["pdf_sha256"] == review["pdf_sha256"]
    assert review["status"] == "passed" and review["pages_reviewed"] == list(range(1,check['total_pages']+1))
    files = [p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    files += [REPO / name for name in ['README.md', 'paper/README.md', 'CHANGES.md',
              'abstention_audit.py', 'CITATION.cff', 'LICENSE', 'LICENSING.md',
              'CONTRIBUTING.md', 'models/README.md',
              '.gitattributes', '.gitignore']]
    files += [p for folder in ['docs', '.github', 'tools'] for p in (REPO / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    for folder in ['analysis','protocols','results/sprint_revision_v1','results/presentation_v2','results/layout_v4','results/repository_v1','results/final_audit_v1','reproduction','tests']:
        files += [p for p in (REPO/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += [REPO/'training'/n for n in ['sprint_inference.py','watch_sprint_inference.py','transfer_sprint_checkpoint.py']]
    files += [pdf, OUT / "Cautionary_Tales_for_Language_Models.md",
              OUT / "submission_checks.json", OUT / "visual_review.json"]
    files += [p for p in (OUT / 'evidence').rglob('*') if p.is_file()]
    figures = json.loads((REPO / 'results/presentation_v2/figure_sources.json').read_text(encoding='utf-8'))
    files += [OUT / 'figures' / (name + '.' + ext) for name in figures for ext in ['svg', 'png', 'pdf']]
    files = sorted(set(files))
    contents = canonical_contents(files)
    entries = [{"path":name, "bytes":len(data), "sha256":sha(data)} for name, data in contents.items()]
    manifest = {
        "title":"Cautionary Tales for Language Models", "subtitle":None,
        "repository":"https://github.com/idreesaziz/cautionary-tales-for-language-models",
        "base_repository_commit":subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
        "status":"author-review revision; author controls Apart submission",
        "built_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "new_model_inference_calls":check['new_inference_calls'], "new_training_jobs":check['new_training_jobs'],
        "presentation_revision_new_model_inference_calls":0, "presentation_revision_new_training_jobs":0,
        "pdf_sha256":check["pdf_sha256"], "entries":entries,
        "reproduce":"Extract over the pinned repository; follow paper/v2/README.md",
    }
    archive = OUT / "Cautionary_Tales_for_Language_Models_sources.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        for name, data in contents.items():
            z.writestr(name, data)
        z.writestr("REVISION_MANIFEST.json", json.dumps(manifest, indent=2)+"\n")
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(entries)+1
        for entry in entries:
            data = z.read(entry["path"])
            assert len(data) == entry["bytes"] and sha(data) == entry["sha256"]
    svg_archive = OUT / 'Cautionary_Tales_SVG_figures.zip'
    with zipfile.ZipFile(svg_archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        for name in figures:
            z.write(OUT / 'figures' / (name + '.svg'), name + '.svg')
        z.writestr('FIGURE_SOURCES.json', json.dumps(figures, indent=2) + '\n')
        z.write(REPO / 'results/presentation_v2/illustrations.json', 'ILLUSTRATIONS.json')
    with zipfile.ZipFile(svg_archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(figures) + 2
        for name, source in figures.items():
            assert sha(z.read(name + '.svg')) == source['svg_sha256']
    result = {"status":"passed", "archive_bytes":archive.stat().st_size,
              "archive_sha256":sha(archive.read_bytes()), "verified_members":len(entries),
              "pdf_sha256":check["pdf_sha256"], "visual_review":str(check['total_pages'])+" final pages inspected",
              "svg_archive_bytes":svg_archive.stat().st_size, "svg_archive_sha256":sha(svg_archive.read_bytes()),
              "svg_figures":len(figures)}
    (OUT / "package_checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
