---
name: target-evaluation
description: Judge whether one biological target is worth a drug-discovery effort in a stated indication. Use when the user asks for a target assessment, target validation, druggability review, or a go/hold/stop recommendation.
license: Apache-2.0
version: "0.1.0"
loads:
  - indication-dossier
requires: []
wisp:
  schema_version: 1
  domains: [drug-discovery, scientific-literature]
  research_stages: [retrieval, validation, synthesis]
  roles: [critic, synthesizer]
  evidence_types: [literature]
  outputs: [evidence-matrix, risk-map, validation-plan]
  side_effects: network
---

# Target evaluation

Decide whether to advance, hold, or stop work on one target in one indication.
This skill writes a sourced recommendation. It does not dock, fold, or simulate
a molecule. Those calculations belong in a later Run.

## Load first

Call `use_skill` on `indication-dossier` before writing mechanism or clinical
competition. If that skill is not installed, stop and say so. When it is
loaded, follow its `references/standards.md` for what counts as a citable
finding. Do not copy those rules or its phase instructions into this package.

If the project already has a completed dossier for this indication, read
`indication_dossier_report.md` and its waypoints. Otherwise run that skill's
identity phase only, then pause together with this skill's identity check.
Do not redo its epidemiology, biology, regulatory, or synthesis phases here.

## Inputs

| Input | Required | Meaning |
|---|---|---|
| `target` | yes | Gene or protein, e.g. "PCSK9" |
| `indication` | yes | Patient population, e.g. "hypercholesterolemia" |
| `modality` | no | `small molecule`, `antibody`, `degrader`, or omitted |
| `additional_context` | no | Known constraints, parent indication, assets to ignore |
| `workdir` | no | Default `./do_not_commit/target-evaluation-<target>-<indication>/` |

Create the workspace with this package's script before gathering evidence.
From the skill directory:

```text
python scripts/init_evaluation.py --input <input.json> --workdir <workdir>
```

The sample input is `samples/input.json`. The script writes `input.json` and
`progress.json` only. It does not fetch sources.

## Identity pause

Resolve the target (HGNC symbol, UniProt accession, aliases) and restate the
indication identity returned by `indication-dossier`. Write `identity.json`.
End the turn and ask **Proceed / Revise identity / Stop**. Later lines wait
for that answer. Wisp has no separate question tool; ending the turn is the
pause.

## Evidence lines

After Proceed, read `references/evidence-lines.md`. Write one waypoint per
line. Lines may run as parallel sub-agents; each line returns findings, not
a second recommendation.

1. Human genetic and clinical evidence → `genetic.json`
2. Mechanism inside this indication → `mechanism.json`
3. Tractability for the stated modality → `tractability.json`
4. Safety liabilities and clinical competition → `safety_competition.json`

Each line is one of `support`, `mixed`, `against`, or `insufficient`.
A line without a citable finding stays `insufficient`.

## Recommendation

Read `references/outputs.md`. Combine the four lines into
`target_evaluation.json` and `target_evaluation_report.md`, then set
`progress.json` to complete.

- **advance** — genetic is `support`, tractability is `support` or `mixed`, and safety is not `against`.
- **hold** — any required line is `insufficient` or `mixed`, and none is a stopping line.
- **stop** — genetic is `against`, or safety is `against` for the stated modality.

Interpretation never upgrades `insufficient` to `support`. Numbers, stages,
dates, and competitor names are cited or omitted.

## Resuming

When `workdir` already has waypoints, list completed files, show the identity
summary, and ask which missing line to run. Do not overwrite a waypoint
without confirmation. Re-run `init_evaluation.py` only with `--force`, and
only before evidence files exist.

## References

| File | Read it when |
|---|---|
| [references/evidence-lines.md](references/evidence-lines.md) | Writing any of the four waypoints |
| [references/outputs.md](references/outputs.md) | Writing the recommendation and report |
