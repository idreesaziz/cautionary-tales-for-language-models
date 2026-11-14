"""Targeted, reproducible lexical screen of training text, not semantic certification."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "output/pdf/cautionary_tales/evidence"
PATTERNS = {
    "abstention_term": r"\babstain\w*\b|\babstention\b",
    "refusal_or_withholding": r"\b(?:withhold\w*|withheld|silence|silent|refus\w*|declin\w*)\b",
    "uncertainty_statement": r"\b(?:I don.t know|I do not know|UNKNOWN)\b",
    "direct_strategy_command": r"\b(?:should|must|ought to|needs to|has to)\s+(?:abstain|refuse|decline|avoid answering|withhold|lower|reduce|verify|double.check|hedge)\b",
    "answering_strategy": r"\b(?:avoid(?:ing)?\s+(?:answering|responding)|refrain\w*\s+from\s+(?:answering|responding)|hedg(?:e|es|ed|ing)|double.check\w*|express\w* uncertainty|report\w* uncertainty|lower\w* (?:its |my )?confidence|reduc\w* (?:its |my )?confidence)\b",
    "indirect_refusal_phrase": r"\b(?:(?:declin|refus)\w*\s+to\s+(?:answer|respond)|(?:cannot|can.t|unable to|do not|don.t|not to|rather than)\s+(?:answer|respond)|(?:say|saying|reply|respond)\w*\s+(?:that\s+)?(?:it\s+)?(?:is\s+)?(?:uncertain|unsure|unknown))\b",
}


def main():
    source = REPO / "data/quartets.jsonl"
    quartets = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    assert len(quartets) == 2000
    hits = []
    for quartet in quartets:
        pieces = [("shared", quartet["shared_text"]), *quartet["appraisals"].items()]
        for section, text in pieces:
            for kind, pattern in PATTERNS.items():
                for match in re.finditer(pattern, text, re.I):
                    hits.append({"quartet": quartet["quartet_id"], "section": section,
                                 "screen": kind, "matched_text": match.group(),
                                 "context": text[max(0, match.start()-120):match.end()+180]})
    counts = Counter((hit["section"], hit["screen"]) for hit in hits)
    result = {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "quartets": len(quartets), "complete_training_documents": 8000,
              "screened_unique_text_components": 10000, "patterns": PATTERNS,
              "counts": [{"section": section, "screen": screen, "hits": count}
                         for (section, screen), count in sorted(counts.items())], "hits": hits,
              "review_status": "lexical_screen_complete; assistant contextual review pending",
              "scope": "Targeted abstention/refusal/answering-strategy screen of every common narrative and appraisal. Not a full semantic or independent human audit."}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "training_language_screen.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"hits": len(hits), "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
