# Contributing

Start with the [paper](paper/README.md), [data card](DATA_CARD.md), and [CPU reproduction guide](reproduction/README.md). Saved-output analysis supplies the quickest route to checking a result.

## Report a reproduction issue

Open a GitHub issue with the command, Python version, operating system, commit or release, and complete error message. Include the relevant artifact hash when a download or verification fails. Keep credentials and private provider logs in local storage.

## Extend the study

Preserve released corpus IDs, protocol bytes, raw measurements, and artifact hashes. Put new training runs, evaluations, and analyses in separately named directories. Record the base-model revision, condition, seed, tokenizer, prompt, and compute budget.

Each reported metric needs its saved input and an explicit denominator. Distinguish actual optional answers from forced-choice answers. Include seed variation and the scope of question-level intervals.

## Validate a change

```bash
python -m pip install -r analysis/requirements.txt
python -m unittest discover -s tests
python tools/verify_corpus.py
python reproduction/verify_repository.py
python tools/verify_publication.py
```

For paper or analysis changes, run `python reproduction/sprint_revision.py --build` after installing `paper/v2/requirements.txt`. Inspect any changed figure and PDF page. [Licensing](LICENSING.md) records the terms for original contributions and upstream material.
