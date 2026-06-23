---
name: analysis-conventions
description: >
  Cook Lab computational-analysis standards, environment, and project scaffolding. Use when
  setting up a new Cook Lab analysis project, replicating the lab analysis environment, scaffolding
  the analyst CLAUDE.md + anchor documents, or when you need the lab's scientific-rigor standards
  (skepticism, confounder-awareness, evidence rubric, analysis log format). Triggers: "set up a lab
  analysis project", "lab analysis conventions/standards", "set up the analysis environment",
  "scaffold an analysis project", "what are the lab analysis standards". Pairs with the
  `scrna-spatial` and `visualization` skills in this plugin.
---

# Cook Lab Analysis Conventions

Establish and apply the Cook Lab's computational-analysis standards in a project. The full standards
(scientific rigor, anchoring protocol, project structure, analysis log format) are in
`references/analysis-conventions.md` — read it before scaffolding or when you need the detail.

> **This skill is intentionally opinionated about the environment** — reproducibility is the point.
> It tells you the lab-standard setup *and how to get it*, rather than assuming you already have it.
> Deviations are fine if you record them.

## Standard environment (and how to set it up)

The lab standard is **system R + a conda/mamba Python environment**. You don't need an exact global
env — **each project pins its own** `environment.yml` (Python) and `renv.lock` (R) to match its
Methods. Use this as the baseline:

1. **Install a conda/mamba** (Miniforge recommended) if you don't have one.
2. **Create the Python single-cell/spatial env** from the bundled starter:
   ```
   mamba env create -f references/environment.example.yml   # creates env "scverse"
   mamba activate scverse
   ```
   (`references/environment.example.yml` is a starting point — scanpy/anndata/scvi-tools/decoupler/
   liana etc. Adjust per project.)
3. **R:** use the system R install; manage packages per-project with `renv` (Seurat,
   SpatialFeatureExperiment, Voyager, SingleR, UCell, …). `renv::init()` in the project, then
   `renv::snapshot()` to pin.
4. **Optional scratch env:** to try experimental tools without disturbing `scverse`, make a throwaway
   env — `mamba create -n claude_code python` — and activate it for those installs. (This is the
   `claude_code` env the `scrna-spatial` skill refers to.)

If a member is on HPC or a different setup, keep the *standard* (conda env + renv per project) and
adapt the specifics — just record what you used in the project's `CLAUDE.md` Environment section.

## Scaffolding a new analysis project

When setting one up (often invoked via `project-init`):

1. Create the project directory structure from `references/analysis-conventions.md`
   (`scripts/` with numbered stages + `sandbox/`, `data/`, `metadata/samples.csv`, `output/`,
   `figs/`, `reports/`, `docs/manuscript/figures/`).
2. **Write the lab standards into the project's `CLAUDE.md`** so they're always loaded for that
   project (this is how the analyst identity persists — mirror `references/analysis-conventions.md`,
   trimmed to what's relevant, plus the project's Environment section).
3. Create the anchor documents:
   - `PROJECT_SPEC.md` — use the `project-spec` skill.
   - `ANALYSIS_PLAN.md` — the phased plan (the anchor).
   - `ANALYSIS_LOG.md` — living log; follow the log format in the conventions.
4. Don't assume git — confirm with the user before initializing a repo.

## Working in an analysis project

- Follow the **scientific standards** in the conventions: skepticism by default, assay-aware
  interpretation, confounder-aware inference, the "interrogate the lead" protocol, and the evidence
  rubric. Every substantive claim needs data + method + quantification + a visualization +
  confounder checks.
- **Update `ANALYSIS_LOG.md` after each discrete step** (script, decision, failed attempt,
  exploration) — not just at session end.
- Use the companion skills: **`scrna-spatial`** for QC/clustering/annotation/integration and spatial
  workflows, **`visualization`** for lab-style figures.

## Companion skills
- `scrna-spatial` — single-cell & spatial methods (this plugin)
- `visualization` — lab figure style + palettes (this plugin)
- `project-spec`, `project-init` — in the `cook-lab-research` plugin

## Note
`references/analysis-conventions.md` is a snapshot of the lab's analyst `CLAUDE.md`, lightly cleaned
for distribution. Treat it as background/standards detail — the actionable setup is in this skill.
