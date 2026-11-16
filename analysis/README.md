# Portable CPU analysis

## Final manuscript and citation audit

[The final audit](../results/final_audit_v1/README.md) records full-source checks
for every cited passage and a source-line ledger for the report. The download
helper uses the optional dependencies in `citation_audit_requirements.txt`:

```bash
python -m pip install -r analysis/citation_audit_requirements.txt
python analysis/download_citation_sources.py
python analysis/verify_final_audit.py
```

Full papers stay in ignored local storage. The public ledger records source
hashes, bibliographic metadata, claim-support summaries, and page locators.
The older URL-check helper retains its original 14-reference snapshot scope.

## Sprint revision analyses

The [revision workflow](../reproduction/sprint_revision.py) stages verified raw
inputs and runs the following analyses on CPU:

| Script | Output |
|---|---|
| `sprint_revision.py` | 48-variant audit, seed SDs, Welch test and exact permutations |
| `revision_measurements.py` | Original fixed-direction interactions and tokenizer spreads |
| `sprint_extensions.py` | Neutral prompts, alternate labels, answer-removal sensitivity and random-direction ranks |
| `revision_claims.py` | Claim ledger and CHANGES.md |
| `verify_revision_sources.py` | Opened reference URLs, resolved identities and source hashes |
| `sprint_execution_receipt.py` | Bounded invocation records and completion checks |
| `package_sprint_inputs.py` | Checksummed raw-input archive |

`abstention_audit.py` at the repository root supplies the reusable metric tool.
Saved revision outputs reside under `results/sprint_revision_v1/`. The scripts
below reproduce the preserved original reporting snapshot.

- `reporting.py`: 39-variant behavioral tables and abstention discrimination.
- `interventions.py`: probability/log-odds effects for all saved causal controls.
- `figures.py`: publication-quality figures from those measurements.
- `paths.py`: account-independent workspace selection via `SHAME_WORKSPACE`.

Use [reproduction/run.py](../reproduction/run.py) to obtain and verify all required
inputs. These scripts are adapted from the original paper-analysis snapshot only
for portable paths, normalized serialization, and a stable output directory. The
underlying numerical calculations are preserved. Frozen original source and broader all-layer analyses
remain in the mechanism evidence archive.

Run `python reproduction/run.py all` from the repository root. Results are written
to `.artifacts/workspace/outputs/reporting_v1/`, never into the checked-in snapshot.
