"""Assemble the revised report from saved measurements; no inference or training."""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "output/pdf/cautionary_tales"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source_files = [REPO / "results/reporting_v1" / name for name in
                    ["paper_metrics.json", "paper_causal_metrics.json", "auxiliary_metrics.json"]]
    source_files += [REPO / "results/no_appraisal_v1/control_metrics.json", REPO / "data/quartets.jsonl"]
    main, causal, auxiliary, extension = [load(path) for path in source_files[:4]]
    assert len(main["rows"]) == 39 and len(extension["per_variant"]) == 21
    assert main["protocol_sha256"] == "907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515"
    control_rows = [row for row in extension["per_variant"] if row["condition"] == "no_appraisal"]
    assert len(control_rows) == 9
    # Match the original report's probability-weighted verbal-confidence readout.
    # The archived extension also retains different argmax-bin readouts; those
    # fields are not substituted for the expected-bin confidence used here.
    for row in control_rows:
        folder = REPO / ".artifacts/no_appraisal/results" / row["model"] / "evaluation/behavior" / row["variant"]
        path = folder / "verbal_confidence/candidate_logits.npy"
        if not path.exists():
            path = Path(__file__).resolve().parent / "inputs/control_confidence" / row["model"] / f"seed-{row['seed']}.npy"
        logits = np.load(path).astype(np.float64)
        assert logits.shape == (1000, 10) and np.isfinite(logits).all()
        probabilities = np.exp(logits - logits.max(axis=-1, keepdims=True))
        probabilities /= probabilities.sum(axis=-1, keepdims=True)
        row["verbal_expected_midpoint"] = float((probabilities * ((np.arange(10)+.5)/10)).sum(axis=-1).mean())
        row["verbal_logit_sha256"] = digest(path)
    paired = {}
    simultaneous = {}
    for model in ["qwen9", "llama8", "mistral8"]:
        paired[model] = load(REPO / f"results/mechanism_v1/{model}/paired_behavior_comparisons.json")
        simultaneous[model] = load(REPO / f"results/mechanism_v1/{model}/causal_simultaneous_intervals.json")
    audit_path = OUT / "evidence/training_language_screen.json"
    audit = load(audit_path)
    assert len(audit["hits"]) == 121
    reviewed = load(Path(__file__).resolve().parent / "reviewed_language_candidates.json")
    keys = ["quartet", "section", "screen", "matched_text", "context"]
    candidates = [{key: hit[key] for key in keys} for hit in audit["hits"]]
    candidates_sha = hashlib.sha256(json.dumps(candidates, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert audit["source_sha256"] == reviewed["source_sha256"] == digest(source_files[-1])
    assert candidates_sha == reviewed["reviewed_candidates_sha256"], "Changed candidates require a new contextual review"
    assert not any(hit["screen"] in ["abstention_term", "direct_strategy_command", "indirect_refusal_phrase"] for hit in audit["hits"])
    # Author-side annotations follow contextual inspection of every stored hit.
    # The review claim is deliberately limited to this lexical candidate set.
    audit["review_status"] = "assistant_context_review_complete"
    audit["reviewed_hits"] = 121
    audit["explicit_abstention_instructions_identified_in_screened_candidates"] = 0
    audit["reviewer"] = "Codex assistant; author-side contextual review, not independent human certification"
    audit["review_notes"] = [
        "Silence/silent generally describes missing records, silent corruption, or a silent specimen.",
        "Decline generally concerns professional trust, physical quantities, population decline, or astronomical declination.",
        "Unknown names quantities, compounds, source identities, or SQL three-valued logic.",
        "Two answering-strategy hits (sdf-1643/reputation and sdf-1824/reputation) concern observers' confidence in the assistant.",
        "Shared narratives explicitly identify unsupported claims and unresolved facts; this is itself uncertainty-related training content.",
    ]
    for hit in audit["hits"]:
        hit["assistant_context_review"] = "No explicit instruction to withhold an answer in the inspected context"
    audit_path.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    evidence = {"main": main, "causal": causal, "auxiliary": auxiliary,
                "extension": extension, "control_rows": control_rows,
                "paired": paired, "simultaneous": simultaneous,
                "training_language_screen": {key: audit[key] for key in
                    ["source_sha256", "quartets", "complete_training_documents", "reviewed_hits", "explicit_abstention_instructions_identified_in_screened_candidates", "scope", "reviewer"]},
                "source_hashes": {str(path.relative_to(REPO)).replace('\\','/'): digest(path) for path in source_files}}
    (OUT / "evidence/paper_evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    fonts = OUT / "template"
    fonts.mkdir(exist_ok=True)
    old = Path(__file__).resolve().parent / "template"
    for name in ["OldStandard-Regular.ttf", "OldStandard-Bold.ttf", "OldStandard-Italic.ttf", "OFL.txt"]:
        shutil.copyfile(old / name, fonts / name)
    print(json.dumps({"status": "assembled", "original_variants": 39, "new_control_adapters": 9,
                      "unique_variants": 48, "reviewed_lexical_hits": 121,
                      "new_inference_calls": 0, "new_training_jobs": 0}))


if __name__ == "__main__":
    main()
