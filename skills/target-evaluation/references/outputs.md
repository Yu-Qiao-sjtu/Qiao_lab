# Outputs

```text
<workdir>/
├── input.json
├── progress.json
├── identity.json
├── genetic.json
├── mechanism.json
├── tractability.json
├── safety_competition.json
├── target_evaluation.json
└── target_evaluation_report.md
```

`progress.json` records `phase` and `completed`. `init_evaluation.py` starts
it at `identity` with an empty `completed` list. The synthesis step sets
`phase` to `complete` only after both final files exist.

## target_evaluation.json

```json
{
  "target": "PCSK9",
  "indication": "hypercholesterolemia",
  "modality": "small molecule",
  "indication_dossier": "path or empty string",
  "lines": {
    "genetic": "support",
    "mechanism": "support",
    "tractability": "mixed",
    "safety_competition": "support"
  },
  "recommendation": "advance",
  "reasons": ["one sentence per line that decided the call"],
  "stopping_gaps": []
}
```

`recommendation` is `advance`, `hold`, or `stop`, using the rule in
`SKILL.md`. `reasons` cite the waypoint calls. `stopping_gaps` lists the
missing evidence that keeps a `hold` from moving.

## Report

`target_evaluation_report.md` is the deliverable. Lead with the
recommendation, the modality, and the four calls. Then one short section per
line. Inline citations follow the indication-dossier style: each factual
claim links its `source_url`. End with gaps and what this skill did not do,
including any Run that was intentionally not started.
