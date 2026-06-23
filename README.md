# Cook Lab — Claude Skills

Claude Code skills for the **Cook Lab** (OHRI). Three plugins:
- **`cook-lab-notion`** — manage your work in the lab's Notion Teamspace: projects, tasks, and the
  electronic lab notebook.
- **`cook-lab-research`** — research productivity: rigorous literature reviews and scaffolding new
  analysis/grant projects (works on any system).
- **`cook-lab-analysis`** — single-cell & spatial analysis: scRNA-seq/spatial methods, lab figure
  style, and the lab analysis conventions + environment. *Opt-in; prescribes the lab analysis setup.*

Install whichever you need.

> **The idea: you do the science, Claude writes the notebook.**
> Finish an analysis or a bench experiment, say *"log this,"* and Claude drafts a proper notebook
> entry — methods, parameters, results, and the decisions you made — and files it in Notion under
> the right task and project. No forms.
>
> *It only ever reads and writes **entries** — it never changes your databases' structure, and never edits anyone else's notes.*

---

## Quick start (≈5 minutes, once)

**Prerequisites**
- A recent **Claude Code** — run `claude --version`, and `claude update` if anything below fails (plugins + the bundled MCP need a current version).
- A Notion account that's a **member of the Cook Lab Teamspace**. (Ask David if you're not in it.)

**1. Add the lab marketplace** (one time):
```
/plugin marketplace add cook-lab/claude-skills
```

**2. Install what you want** (either or both):
```
/plugin install cook-lab-notion@cook-lab
/plugin install cook-lab-research@cook-lab
/plugin install cook-lab-analysis@cook-lab
```

**3. Reload, then connect Notion** (one-time login — only needed for `cook-lab-notion`):
```
/reload-plugins
/mcp
```
In `/mcp`, select **notion** and authenticate — a browser opens, you log in to Notion, and the
connection is cached. You won't have to do this again.

**4. Try it (your first 2 minutes).** In a normal Claude Code chat:
> what should I work on?

✅ *Working:* Claude lists your open tasks, grouped by project. (If it instead asks who you are, tell it your name once — see Troubleshooting.)

Then, after you run an analysis or experiment:
> log this experiment

✅ *Working:* Claude creates a dated entry under the right task and gives you a Notion link. You wrote one sentence; it wrote the notebook page — that's the whole idea. (Full example: `plugins/cook-lab-notion/skills/lab-notebook/references/logging-walkthrough.md`.)

---

## What you get

Claude picks skills automatically based on what you ask.

**`cook-lab-notion`**

| Skill | For | Does |
|-------|-----|------|
| **lab-notebook** | everyone | See your tasks, create/update tasks, **log experiments**, summarize & close tasks, check project status. |
| **lab-pm** | David / oversight | Lab-wide status, stale-work detection, 1:1 & lab-meeting prep, trainee progress summaries, convention audits. |

**`cook-lab-research`**

| Skill | For | Does |
|-------|-----|------|
| **literature-review** | everyone | Rigorous, web-search-grounded literature reviews with citation verification. |
| **project-spec** | everyone | Create/update a `PROJECT_SPEC.md` for a research project (research questions, goals, deliverables). |
| **project-init** | everyone | Scaffold a focused `CLAUDE.md` for any new project (any system) — asks for your environment instead of assuming it. |

**`cook-lab-analysis`** *(opt-in — for single-cell/spatial analysts)*

| Skill | For | Does |
|-------|-----|------|
| **scrna-spatial** | analysts | scRNA-seq & spatial methods: QC, doublets, normalization, clustering, annotation, integration, cross-modality transfer (Seurat/Scanpy/SFE). |
| **visualization** | analysts | Publication-ready, lab-style figures (palettes, theme, plot types, export sizes). |
| **analysis-conventions** | analysts | Lab analysis standards, the standard environment + setup, and full project scaffolding. |

You don't need to memorize commands — just talk to Claude (*"create a task for…"*, *"log this run"*,
*"do a lit review on…"*, *"set up this project"*, *"cluster these cells"*). If you ever want to invoke
a skill explicitly, they're namespaced: `/cook-lab-notion:lab-notebook`,
`/cook-lab-analysis:scrna-spatial`. (If you already have a *personal* skill with one of these names,
use the namespaced form to be sure you get the lab version.)

## The model in three sentences

- **Projects** = your high-level line of work (usually one main line per person — but having more than one is fine).
- **Tasks** = a complete data *deliverable* toward a project — one clear objective/story.
- **Experiments** = your day-to-day journal toward a task (the ELN): decisions, methods, results as
  you generate them. Title them `YYYYMMDD - short description`.

Log real experiments and analyses — not routine maintenance. When in doubt, just say "log this"
and Claude will place it sensibly.

---

## Troubleshooting

- **"Notion isn't connected" / tools missing** → run `/mcp`, authenticate **notion**, then retry.
  If `notion` isn't listed, re-run `/reload-plugins`.
- **Don't see the plugin after install** → `/plugin marketplace update cook-lab`, then
  `/reload-plugins`.
- **It logged under the wrong task/project** → just tell Claude; it'll move or relink it.
- **Claude can't tell who you are** → tell it your name once; it uses the lab roster to set the
  right person.
- **Entries show up under the wrong person (e.g. David's name)** → tell Claude who you are and ask it
  to fix the entry. If it keeps happening, your Notion login may not be resolving to you — flag it to
  David (we're validating this during rollout).

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
plugins/cook-lab-notion/
  .claude-plugin/plugin.json             # plugin manifest (bump "version" to release)
  .mcp.json                              # bundles the Notion MCP server
  conventions.md                         # canonical entry conventions (both notion skills read it)
  skills/lab-notebook/SKILL.md           # + references/logging-walkthrough.md
  skills/lab-pm/SKILL.md
plugins/cook-lab-research/
  .claude-plugin/plugin.json
  skills/literature-review/SKILL.md      # + references/
  skills/project-spec/SKILL.md           # + references/project_spec_template.md (bundled)
  skills/project-init/SKILL.md           # general CLAUDE.md scaffolder (no system assumptions)
plugins/cook-lab-analysis/
  .claude-plugin/plugin.json
  skills/scrna-spatial/SKILL.md          # + references/code_templates.md
  skills/visualization/SKILL.md          # + references/visualization_style_guide.md (bundled)
  skills/analysis-conventions/SKILL.md   # + references/{analysis-conventions.md, environment.example.yml}
```

**Bundled dependencies (keep in sync):** several skills ship snapshots of local files — re-copy them
if you change the originals:
- `cook-lab-research/project-spec` → `project_spec_template.md` (from `~/Projects/lab_guide/templates/`)
- `cook-lab-analysis/visualization` → `visualization_style_guide.md` (from `~/Projects/lab_guide/guides/`)
- `cook-lab-analysis/analysis-conventions` → `analysis-conventions.md` (snapshot of `~/Analysis/CLAUDE.md`, **lightly cleaned** — PI-machine path removed; re-clean if you re-copy) + a hand-written `environment.example.yml`

`cook-lab-research/project-init` is intentionally **general** (no system assumptions). The
system-specific bits — lab environment, analysis conventions, full scaffolding — live in
`cook-lab-analysis`, which prescribes the lab setup *and* tells members how to install it.

**Releasing a change:** edit the skill, bump `version` in both `marketplace.json` and the plugin's
`plugin.json`, commit, and push. Labmates get it on `/plugin marketplace update cook-lab`.

**Verify before wide rollout:**
- The bundled Notion MCP endpoint in `.mcp.json` is `https://mcp.notion.com/mcp`. Confirm this is
  the correct hosted-Notion MCP URL for Claude Code and that OAuth grants access to the **Cook Lab
  Teamspace** (not just a personal workspace) during the pilot before sharing widely.
- The collection IDs and the user roster in `lab-notebook/SKILL.md` are workspace-specific; update
  them here if the Teamspace or membership changes.

**Adding more plugins later** (e.g. a `scrna-spatial`/`visualization` analysis plugin): add a folder
under `plugins/` and a corresponding entry in `marketplace.json`. (Grant skills — `grant-writing`,
`grant-review` — are intentionally kept local/private and are not in this repo.)
