# Evidence lines

Each waypoint is a JSON object with:

- `line`: `genetic`, `mechanism`, `tractability`, or `safety_competition`
- `call`: `support`, `mixed`, `against`, or `insufficient`
- `findings`: list of sourced findings
- `gaps`: what was searched and not found
- `anomaly_flags`: source disagreements or failed fetches

A finding uses the indication-dossier triple: `source_url`, `source_type`,
and a verbatim `quote`. URLs come from a fetch or MCP result. Record a miss
as a gap instead of inventing a link.

## Genetic and clinical

Human evidence that this target matters in this patient population.

Look for germline or somatic association, Mendelian disease, clinical
biomarker use, and human loss- or gain-of-function. Prefer Open Targets,
GWAS Catalog, ClinVar, and primary papers over review summaries.

- `support`: a human genetic or clinical finding ties the target to this indication.
- `mixed`: human evidence exists but points at a related population, a weak effect, or a conflicting direction.
- `against`: human evidence contradicts the proposed direction of modulation.
- `insufficient`: no citable human finding after the search.

Animal or cell results do not by themselves make this line `support`. Put
them on the mechanism line.

## Mechanism

How modulating the target would change disease in this indication. Read the
indication dossier's biology waypoint when it exists. Do not open a new
disease-landscape search here.

- `support`: a cited mechanism connects the target to the indication's biology in the proposed direction.
- `mixed`: the mechanism is plausible but the direction or the relevant cell type is unresolved.
- `against`: cited biology says modulation would worsen the indication or miss the disease process.
- `insufficient`: no citable mechanistic link.

## Tractability

Whether the stated modality has a credible path. This line is a literature
and database review.

- Small molecule: known ligand, co-structure, or a cited chemical series. Selectivity risk is a finding, not a docking job.
- Antibody: extracellular localization and a cited reason the relevant surface is reachable.
- Degrader: a cited ligand plus a reason the target can be degraded. No ternary-complex simulation.
- Omitted modality: call this line `insufficient` and name the missing choice in `gaps`.

Structure prediction, docking, and molecular dynamics are out of scope. When
the user asks for them, say they need a separate Run and stop this line at
the evidence already in hand.

- `support`: at least one cited ligand, epitope, or equivalent modality-specific precedent.
- `mixed`: only a homolog, a non-drug-like probe, or an inaccessible site with a theoretical workaround.
- `against`: cited evidence says the site is not tractable for this modality.
- `insufficient`: no cited chemical or epitope evidence.

## Safety and competition

On-target biological risk and the clinical programs already modulating this
target in this indication.

Safety uses human genetic constraint, essentiality, and cited on-target
liabilities. Competition names the asset, sponsor, stage, and indication
from a registry, label, or company disclosure. A pipeline homepage is not
a citation.

- `support`: no cited on-target liability blocks the modality, and the competitive record is described with sources.
- `mixed`: a manageable liability or a crowded class, with the residual risk stated.
- `against`: a cited liability contradicts this modality, or an approved agent already removes the stated unmet need.
- `insufficient`: safety or the competitive search was not completed.

DepMap essentiality is optional context. When the user wants a dependency
matrix, load `public-data-access` and keep the download plan beside this
workspace. A DepMap score alone does not set the safety call.
