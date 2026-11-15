# Artifact map

The download registries record URLs, byte sizes, and SHA-256 hashes. Large files
are GitHub release assets. The [current paper](../paper/README.md) uses all three
registries while preserving their frozen identities.

| Registry | Coverage |
|---|---|
| [Current paper inputs](../reproduction/sprint_revision_artifacts.json) | 33 MB CPU bundle, 480 members, 48 variants, prompt tests, and activation controls |
| [Original artifacts](../reproduction/artifacts.json) | 36 adapters, original CPU inputs, mechanism evidence, and the earlier benchmark |
| [Incident-only extension](../reproduction/control_artifacts.json) | Nine adapters, control evaluation, and training provenance |

The repository's original name was `shame-corpus`. Frozen registries retain those
URLs and bytes. GitHub redirects them to `cautionary-tales-for-language-models`.

| Asset | Purpose |
|---|---|
| CPU reproduction archive | Saved decisions/logits, frozen protocol, concept validation, and token metadata for portable reanalysis |
| Mechanism evidence archive | All compact outputs, source snapshots, figures, and inventories from 15 core jobs |
| Previous benchmark archive | 15,780 freeform responses, references, provenance, and dated handoff |
| 36 epoch-three safetensors assets | Final main-study LoRA weights, paired with versioned configuration and training manifests |
| Adapter license bundle | Preserved upstream base-model licenses and attribution notices |

The experiment source covers the extraction and analysis of native activations.
Large native tensors remain in producer storage and are indexed in the evidence
archive. Regeneration uses the released adapters, model revisions, inputs, and
extraction code. No base-model weights are included.

The raw corpus snapshot remains in Git, with its original integrity manifest.
Earlier epoch and exploratory results remain under evaluation/. The
[paper release](https://github.com/idreesaziz/cautionary-tales-for-language-models/releases/latest)
contains the report PDF, editable source bundle, and eight SVG figures.

The [no-added-appraisal registry](../reproduction/control_artifacts.json) separately
indexes nine additional adapters and a CPU evidence archive. Both ZIPs carry
per-member checksums and a final model-artifact audit. The extension's source,
producer metadata, raw token scores, calibration inputs and analysis are preserved;
its [results](../results/no_appraisal_v1/README.md) leave the v1 snapshot intact.
