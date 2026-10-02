# Cook Lab — Claude Skills

Claude Code skills for the **Cook Lab** (OHRI). Two plugins:
- **`cook-lab-research`** — research productivity: rigorous literature reviews and scaffolding new
  analysis and grant projects (works on any system).
- **`cook-lab-analysis`** — single-cell and spatial analysis: the lab's processing decisions, the
  SpatialFeatureExperiment + Voyager stack, and the lab analysis standards and environment.
  *Opt-in; prescribes the lab analysis setup.*

Install whichever you need. (The Notion project-management plugin has been retired while the lab
formalizes how it organizes projects; a new version will follow.)

---

## Quick start

**Prerequisite:** a recent **Claude Code** — run `claude --version`, and `claude update` if anything
below fails.

**1. Add the lab marketplace** (one time):
```
/plugin marketplace add cook-lab/claude-skills
```

**2. Install what you want:**
```
/plugin install cook-lab-research@cook-lab
/plugin install cook-lab-analysis@cook-lab
```

**3. Reload:**
```
/reload-plugins
```

If you installed `cook-lab-notion` before, remove it with `/plugin uninstall cook-lab-notion@cook-lab`.

---

## What you get

Claude picks skills automatically based on what you ask.

**`cook-lab-research`**

| Skill | For | Does |
|-------|-----|------|
| **literature-review** | everyone | Rigorous, web-search-grounded literature reviews with citation verification. |
| **project-spec** | everyone | Create/update a `PROJECT_SPEC.md` for a research project (research questions, goals, deliverables). |
| **project-init** | everyone | Scaffold a focused `CLAUDE.md` for any new project (any system) — asks for your environment instead of assuming it. |

**`cook-lab-analysis`** *(opt-in — for single-cell/spatial analysts)*

| Skill | For | Does |
|-------|-----|------|
| **scrna-spatial** | analysts | The lab's decisions for scRNA-seq and spatial processing (QC, doublets, normalization, clustering, DE, annotation) and the SpatialFeatureExperiment + Voyager stack. |
| **analysis-conventions** | analysts | Lab analysis standards, the standard environment + setup, and full project scaffolding. |

Figure style (chart types, palettes, journal sizes) lives in the lab Branding repo, [`cook-lab/Branding`](https://github.com/cook-lab/Branding), with ggplot2 scales in `tokens/palettes.R` and the journal-figure theme in `tokens/figures.R`.

You don't need to memorize commands — just talk to Claude (*"do a lit review on…"*, *"set up this
project"*, *"cluster these cells"*). If you want to invoke a skill explicitly, they're namespaced:
`/cook-lab-research:literature-review`, `/cook-lab-analysis:scrna-spatial`. (If you already have a
*personal* skill with one of these names, use the namespaced form to be sure you get the lab version.)

---

## Troubleshooting

- **Don't see the plugin after install** → `/plugin marketplace update cook-lab`, then
  `/reload-plugins`.

## Updating

```
/plugin marketplace update cook-lab
```
New versions are picked up from this repo. (Auto-update can be toggled in `/plugin` → Marketplaces.)

---

## For maintainers (David)

**Layout**
```
.claude-plugin/marketplace.json          # catalogs the plugins
plugins/cook-lab-research/
  .claude-plugin/plugin.json             # plugin manifest (bump "version" to release)
  skills/literature-review/SKILL.md      # + references/
  skills/project-spec/SKILL.md           # + references/project_spec_template.md (bundled)
  skills/project-init/SKILL.md           # general CLAUDE.md scaffolder (no system assumptions)
plugins/cook-lab-analysis/
  .claude-plugin/plugin.json
  skills/scrna-spatial/SKILL.md
  skills/analysis-conventions/SKILL.md   # + references/{analysis-conventions.md, environment.example.yml}
```

**Bundled dependencies (keep in sync):** some skills ship snapshots of local files — re-copy them
if you change the originals:
- `cook-lab-research/project-spec` → `project_spec_template.md` (from `~/Projects/lab_guide/templates/`)
- `cook-lab-analysis/analysis-conventions` → `analysis-conventions.md` (originally a snapshot of `~/Analysis/CLAUDE.md`, lightly cleaned) + a hand-written `environment.example.yml`

`cook-lab-research/project-init` is intentionally **general** (no system assumptions). The
system-specific bits — lab environment, analysis conventions, full scaffolding — live in
`cook-lab-analysis`, which prescribes the lab setup *and* tells members how to install it.

**Writing skills:** record the lab's decisions and the reason for each, and leave out standard
workflows that Claude already knows. Keep code to the calls that are easy to get wrong.

**Releasing a change:** edit the skill, bump `version` in both `marketplace.json` and the plugin's
`plugin.json`, commit, and push. Labmates get it on `/plugin marketplace update cook-lab`.

**Adding more plugins later** (e.g. the revamped Notion plugin): add a folder under `plugins/` and a
corresponding entry in `marketplace.json`. (Grant skills — `grant-writing`, `grant-review` — are
intentionally kept local/private and are not in this repo.)
