# Final pre-submission audit

Every cited passage has an author-side assistant review against the full source. The review covers 18 references and 28 citing-passage/reference pairs.
Full sources include 15 paper PDFs totaling 663 pages, one complete research post, a pinned dataset card, and a pinned model card.
The source PDFs and HTML remain in `.artifacts/final_citation_audit_20261116/` on the author workspace. The public repository records provenance and review locators.

| Reference | Full source | Reviewed passage |
|---|---|---|
| 1 | html | Research post: Introduction, Methods and training appendix |
| 2 | 90 PDF pages | PDF pp. 1-6 and discussion of limitations |
| 3 | 24 PDF pages | PDF pp. 2-4; Appendix A, pp. 16-19 |
| 4 | 23 PDF pages | PDF pp. 1, 9-11; Methods: Dataset and calibration |
| 5 | 17 PDF pages | PDF pp. 1-3; RiskEval decision model and findings |
| 6 | 132 PDF pages | PDF pp. 3-5; Part 1.1: Finding emotion vectors |
| 7 | md | Pinned dataset README: files, expression stories, neutral stories, citation and author |
| 8 | 101 PDF pages | PDF pp. 1-5; Contrastive SDF design |
| 9 | 26 PDF pages | PDF pp. 1, 4-5; Microsoft Research publication record |
| 10 | 10 PDF pages | PDF p. 6: Temperature scaling; project calibration code |
| 11 | 36 PDF pages | PDF pp. 4 and 12-14: evaluation incentives and proposed scoring changes |
| 12 | 89 PDF pages | PDF pp. 1-5: experiments, synthetic discourse and results |
| 13 | 13 PDF pages | PDF pp. 1-3; publisher bibliographic record |
| 14 | md | Pinned model card: quick start, direct-response API and chat-template configuration |
| 15 | 20 PDF pages | Published PDF pp. 3-4 and 7; PMLR proceedings entry |
| 16 | 45 PDF pages | Pinned v3 PDF pp. 1-4; arXiv version history |
| 17 | 10 PDF pages | PDF pp. 1-3: Methodology and reward formulation |
| 18 | 27 PDF pages | PDF pp. 1-3; ACL metadata |

## Corrections

- Added the dataset author, requested title, year, DOI, and preserved revision.
- Replaced the contrastive-belief blog citation with the underlying paper and its complete author list.
- Used the Nature DOI for emergent misalignment and corrected the accent in Mart?n Soto.
- Added TruthRL's published ICML pagination and pinned Reinforced Hesitation to the cited version.
- Restored Yi R. Fung's middle initial and supplied complete author lists through nine authors.
- Separated benchmark scoring proposals from explicit abstention-training methods.
- Credited prior confidence-threshold findings and distinguished pretraining discourse from narrow fine-tuning.
- Attached calibration and emotion-vector citations to the specific methods they support.
- Clarified topic-specific input filtering, private credential storage, and the shared perturbation scale.

## Recheck the sources

```bash
python -m pip install -r analysis/citation_audit_requirements.txt
python analysis/download_citation_sources.py
python analysis/verify_final_audit.py
```

The downloader saves full texts and metadata. The review ledger records the author-side claim checks. Independent peer review supplies a separate assessment.

The previous report, abstract and visual-review record remain in the ignored `before/` directory. Public release v1.0.0 retains its original bytes.
