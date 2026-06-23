# Worked example: logging an experiment

Two concrete, end-to-end examples of the `Log an experiment` workflow — calibrate both the *output*
quality (modeled on the lab's best entries) and the *process* (do the work for the labmate).
**Example 1** is in-session (the agent already has the context). **Example 2** is a cold intake (the
user did the work away from Claude) — often the more common case.

---

## The situation

A labmate has just finished a clustering run in their analysis project directory
(`~/Analysis/hgsc_macrophages/`) and types:

> log this — I clustered the macrophages and found the TREM2 subset

That's all the agent gets. Everything else is inferred.

## What the agent does (process)

1. **Resolve identity.** `get-users {"user_id":"self"}` → confirm it resolves to the person you're
   talking to (if it's ambiguous, a bot, or the PI, ask — see the skill's identity step). Say it's
   Athena. Use `263d872b-594c-8190-91f5-00020ad780ad` for `Person`.
2. **Find the parent task.** The working dir and conversation are about macrophage subclustering in
   HGSC. Query the Tasks DB for candidates owned by Athena or matching "macrophage"/"cluster". If a
   task like *"Identify defined clusters/subpopulations of macrophages in HGSC scRNA-seq data"*
   exists, use it. If several plausibly fit, ask one short question. If none fit, offer to create it
   (under the relevant project) before logging.
3. **Gather real content from the session.** Don't ask the labmate to retype it — pull from what
   was actually run this session: the script/notebook, parameters (resolution, n_neighbors, n PCs),
   input/output paths, the cluster count, marker genes, the figures written to disk.
4. **Create the experiment page**, then **write the body**, then **confirm + offer the status bump.**

## The tool call (shape)

Create one page in the Experiments data source with these properties, then fill the body:

```
notion-create-pages
  parent: collection://23e878bf-8826-8111-b5b4-000bdef2369c   (Experiments)
  Experiment (title): "20260623 - Macrophage subclustering: TREM2+ subset identified"
  Person: ["263d872b-594c-8190-91f5-00020ad780ad"]
  Date Created: 2026-06-23
  Tasks: ["<URL of the parent task>"]
  body: <the markdown below>
```

> Always link `Tasks`. The `Linked Projects` rollup then fills automatically via the task.

## The resulting page (what "good" looks like)

```markdown
# Objective
Subcluster the macrophage compartment from the HGSC scRNA-seq atlas to test whether a
TREM2+ lipid-associated subset is resolvable, and define its markers.

# Methods
- **Input:** `output/03_annotation/adata_myeloid.h5ad` (28,411 macrophages/monocytes)
- **Pipeline:** re-HVG on the myeloid subset → PCA → neighbors → Leiden → rank_genes_groups
- **Key parameters**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| HVG | 2,000 (subset-specific) | Recompute within compartment |
| PCs | 30 | Elbow at ~28 |
| n_neighbors | 15 | scanpy default; stable |
| Leiden resolution | 0.6 | 7 clusters; higher fragmented TREM2+ |

# Input / Output
| Direction | File | Description |
|-----------|------|-------------|
| Input | `output/03_annotation/adata_myeloid.h5ad` | Annotated myeloid cells |
| Output | `output/04_macrophage/adata_macro_clustered.h5ad` | + `leiden_macro` labels |
| Output | `output/figures/macro/umap_leiden.png` | UMAP by cluster *(attach screenshot)* |
| Output | `output/04_macrophage/markers_leiden.csv` | Per-cluster markers |

# Analysis
7 clusters at resolution 0.6. Cluster 3 (3,902 cells, 13.7%) is defined by
**TREM2, APOE, APOC1, SPP1, GPNMB** — a lipid-associated / TAM phenotype. FOLR2+ perivascular
macrophages separate as cluster 5. Classical monocytes (FCN1, S100A8/9) form cluster 0.

*(Paste the UMAP and a marker dotplot here.)*

# Key findings
- A discrete **TREM2+ SPP1+ APOE+** macrophage subset is robustly resolved (cluster 3).
- FOLR2+ and TREM2+ macrophages are distinct populations, not a gradient.
- Subset is present across patients (not a single-sample artifact) — confirm in next session.

# Decision log
| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Recompute HVG within myeloid subset | Whole-atlas HVGs miss within-compartment variation |
| 2 | Resolution 0.6 (not 1.0) | Higher res split TREM2+ into unstable fragments |
| 3 | Keep monocytes in the object | Needed to anchor the mono→macro axis |
```

## After creating it

- Reply with the page link.
- Offer the next step: *"Want me to set the task 'Identify macrophage subpopulations…' to In
  progress (or Done if this closes it)?"*
- If a figure can't be embedded programmatically, say exactly which file to drag in and where.

---

## Example 2 — cold intake (bench work, no session context)

The labmate walks in having done bench work earlier, with no Claude context, and types:

> log an experiment

The agent must **not** say "log what?" — it runs a short, friendly intake (Mode B), asking only what
it can't infer, adapted to bench work:

> Sure — a few quick questions so I can write it up:
> 1. What did you do, in a sentence? 2. When? 3. Which project/task?
> 4. Key conditions — samples/lines, treatment, readout? 5. What did you find?
> 6. Any decisions worth noting? 7. Where are the data/images? (fine to add later — I'll leave a placeholder.)

The labmate answers briefly:

> Carboplatin dose-response on my HGSC organoids to pick a dose for the tolerance study. 3 lines
> (OV-90, Kuramochi, one patient PDO), 0/10/50/100 µM, 72 h, CellTiter-Glo. IC50 ~30 µM for all
> three. Going with 25 µM for the cycling experiment. Plots are still on my laptop.

That's enough. The agent creates the entry (today's date; parent task = the dose-finding/tolerance
task, offering to create it if none exists), with a placeholder for the missing plot:

```markdown
# Objective
Carboplatin dose-response across HGSC organoid models to choose a dose for the tolerance study.

# Methods
- **Models:** OV-90, Kuramochi, patient PDO (1 line)
- **Treatment:** carboplatin at 0, 10, 50, 100 µM, 72 h
- **Readout:** CellTiter-Glo viability

# Results
- Approximate IC50 ~30 µM across all three lines.
- `📎 [attach dose–response curves — on labmate's laptop, TBD]`

# Decision log
| Decision | Rationale |
|----------|-----------|
| Use 25 µM for the cycling experiment | Just below the ~30 µM IC50 — sublethal, models tolerance |
```

Then: confirm with the link and say exactly what's left — *"I left a placeholder for the
dose–response curves; drag the image into Results when it's handy."* No interrogation, nothing
blocked on the missing file.

## Principles these examples demonstrate

- **The agent writes the entry; the labmate gave one sentence.** That's the adoption win.
- Real parameters, paths, and numbers — not vague prose.
- Decisions *and their rationale* are captured (the highest-value, most-skipped part).
- Light structure, adapted to the work — a bench experiment would look looser.
- Everything is linked, so it rolls up to the task and project automatically.
- **No context? Ask briefly, then log with placeholders.** Never reply "log what?", and never block
  the entry on missing files — capture it now, fill the gaps later.
