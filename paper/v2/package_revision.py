"""Package this CPU-only report revision and verify every archived byte."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import zipfile

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = REPO / "output/pdf/cautionary_tales"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    pdf = OUT / "Cautionary_Tales_for_Language_Models.pdf"
    check = json.loads((OUT / "submission_checks.json").read_text())
    review = json.loads((OUT / "visual_review.json").read_text())
    assert sha(pdf.read_bytes()) == check["pdf_sha256"] == review["pdf_sha256"]
    assert review["status"] == "passed" and review["pages_reviewed"] == list(range(1,check['total_pages']+1))
    files = [p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    files += [REPO / "README.md", REPO / "paper/README.md", REPO/'CHANGES.md', REPO/'abstention_audit.py', REPO/'CITATION.cff',REPO/'.gitattributes',REPO/'.gitignore']
    for folder in ['analysis','protocols','results/sprint_revision_v1','reproduction','tests']:
        files += [p for p in (REPO/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += [REPO/'training'/n for n in ['sprint_inference.py','watch_sprint_inference.py','transfer_sprint_checkpoint.py']]
    files += [pdf, OUT / "Cautionary_Tales_for_Language_Models.md",
              OUT / "submission_checks.json", OUT / "visual_review.json"]
    for folder in ["evidence", "figures"]:
        files += [p for p in (OUT / folder).rglob("*") if p.is_file()]
    files = sorted(set(files))
    entries = [{"path":p.relative_to(REPO).as_posix(), "bytes":p.stat().st_size,
                "sha256":sha(p.read_bytes())} for p in files]
    manifest = {
        "title":"Cautionary Tales for Language Models", "subtitle":None,
        "repository":"https://github.com/idreesaziz/shame-corpus",
        "base_repository_commit":"9a9bfcc8c3a5c54f53fbbdefcb95e0268094dcd8",
        "status":"author-review revision; author controls Apart submission",
        "built_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "new_model_inference_calls":check['new_inference_calls'], "new_training_jobs":check['new_training_jobs'],
        "pdf_sha256":check["pdf_sha256"], "entries":entries,
        "reproduce":"Extract over the pinned repository; follow paper/v2/README.md",
    }
    archive = OUT / "Cautionary_Tales_for_Language_Models_sources.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        for p in files:
            z.write(p, p.relative_to(REPO).as_posix())
        z.writestr("REVISION_MANIFEST.json", json.dumps(manifest, indent=2)+"\n")
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(entries)+1
        for entry in entries:
            data = z.read(entry["path"])
            assert len(data) == entry["bytes"] and sha(data) == entry["sha256"]
    result = {"status":"passed", "archive_bytes":archive.stat().st_size,
              "archive_sha256":sha(archive.read_bytes()), "verified_members":len(entries),
              "pdf_sha256":check["pdf_sha256"], "visual_review":str(check['total_pages'])+" final pages inspected"}
    (OUT / "package_checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
