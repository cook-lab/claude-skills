---
name: project-init
description: >
  Scaffold a focused CLAUDE.md for a new project directory — for any project, on any system.
  Use when the user wants to set up a new project, create a CLAUDE.md, or initialize a directory for
  work. Triggers: "init this project", "set up CLAUDE.md", "scaffold this project", "new analysis
  project", "new grant project", "set up this directory", or when a directory has no CLAUDE.md and
  the user wants one. IMPORTANT: Do NOT search the web or browse other directories for context — all
  context comes from the user and from any relevant installed skills.
---

# Project Init

Generate a focused CLAUDE.md for a new project directory. The CLAUDE.md gives Claude the context it needs to be effective in this specific project — nothing more.

**This skill is general: it makes no assumptions about your operating system, languages, paths, or environment.** When something is environment-specific, it *asks* rather than assumes.

**Do NOT search the web or browse other directories for context.** Everything you need comes from: (1) what the user tells you, (2) any relevant installed skills. Ask the user, don't go hunting.

## Workflow

### Step 1: Determine project type

Ask the user (or infer from context):

> What type of project is this?
> 1. **Computational analysis** — data analysis, genomics, imaging, modeling, etc.
> 2. **Grant / proposal writing**
> 3. **Other** — general project, tool development, writing, etc.

### Step 2: Gather context

Ask the **minimum** questions needed. Don't over-interview. If the user already gave context (e.g. "this is a CIHR grant on endometriosis"), extract what you can and only ask what's missing.

#### For computational analysis:

- **What's the research question?** (1-2 sentences)
- **What data?** (type, source, rough scale)
- **What environment/stack?** (e.g. R/Bioconductor, Python/conda env name, an HPC scheduler) — capture this rather than assuming; it goes in the CLAUDE.md so the project is reproducible on *their* system
- **Who's involved?** (lead, PI, collaborators)
- **Any existing data or code?** (building on something, or from scratch?)

#### For grant writing:

- **Grant name and agency** (e.g. CIHR Project Grant, NIH R01)
- **Deadline**
- **PI and co-investigators**
- **What does the grant propose?** (2-3 sentences)
- **Current status** (brainstorming, drafting, resubmission?)
- **Key documents already in the directory?**

#### For other projects:

- **What is this project?** (1-2 sentences)
- **Key files or conventions?**
- **Anything Claude should know or avoid?**

### Step 3: Generate CLAUDE.md

Write a focused CLAUDE.md to the project root using the templates below. Keep it short — a good CLAUDE.md is under 80 lines and scannable in 30 seconds. **No generic advice** — every line specific to this project.

---

## Templates

### Computational Analysis

```markdown
# [Project Name]

## Context
[1-3 sentences: what question this answers and why it matters]

## Data
- **Type:** [e.g. 10x Chromium scRNA-seq]
- **Samples:** [e.g. 8 HGSC patient tumors, pre/post chemo paired]
- **Scale:** [e.g. ~50k cells expected]
- **Location:** [where the data lives]

## Environment
- **Stack:** [e.g. R 4.x + Bioconductor; or Python + conda env `name`]
- **How to run:** [activate/setup command(s) for THIS machine]
- **Compute:** [local / HPC / cloud — scheduler if any]

## People
- **Lead:** [name]
- **PI:** [name]
- **Collaborators:** [if any]

## Anchor Documents
[If this project uses planning/log docs, list them — e.g.]
- `PROJECT_SPEC.md` — research questions, goals, deliverables
- `ANALYSIS_PLAN.md` — phased approach
- `ANALYSIS_LOG.md` — what's been done (check this first)

## Project Notes
- [Any project-specific conventions or key decisions]
```

### Grant Writing

```markdown
# [Grant Name]

## Overview
- **Agency:** [e.g. CIHR, NIH, NSERC]
- **Mechanism:** [e.g. Project Grant, R01]
- **Deadline:** [date]
- **Status:** [brainstorming / drafting / revision / resubmission]
- **PI:** [name]
- **Co-investigators:** [names and roles]

## What This Grant Proposes
[2-4 sentences summarizing the core idea, approach, and significance]

## Key Documents
- `[proposal.docx]` — main proposal draft
- `[budget.xlsx]` — budget and justification
- `[references/]` — key papers, preliminary data
[Add others as they exist]

## Writing Conventions
[If the `grant-writing` skill is installed, this project can use it for style, structure, and review.]
- [Agency-specific: page limits, formatting, section headings]
- Draft in [Google Docs / Word] — [link if applicable]

## Context for Claude
[Background, key preliminary data, prior reviewer concerns, strategic framing]
```

### Other / General

```markdown
# [Project Name]

## What This Is
[1-3 sentences]

## Key Files
- [list important files and what they contain]

## Conventions
[Any project-specific rules, patterns, or things to avoid]
```

---

## After generating CLAUDE.md

- **For analysis projects:** if the user follows a standard lab/group project structure (directory tree, anchor docs, shared environment), offer to scaffold it — but ask for those conventions rather than inventing them.
  - *Cook Lab members:* the `cook-lab-analysis` plugin (if installed) carries the lab's single-cell/spatial conventions, environment, and full directory + anchor-doc scaffolding. Defer to it instead of hardcoding any of that here.
- **For grant projects:** don't assume git — grant directories often live in cloud-synced folders, not repos. Check before initializing one.
- **For all types:** show the draft and confirm with the user before writing. Keep it brief — "Does this capture the essentials?"

## Principles

- **No assumptions about the system.** Ask for environment/run commands; record them. Never bake in a specific OS, package manager, or path the user didn't give you.
- **Less is more.** A 40-line CLAUDE.md that's all signal beats a 200-line one with boilerplate.
- **Specific > generic.** "scRNA-seq of 8 HGSC tumors" not "genomics data analysis."
- **Don't duplicate.** If detail belongs in PROJECT_SPEC.md or a plan doc, point there. CLAUDE.md is the entry point, not the encyclopedia.
- **Update as you go.** CLAUDE.md should evolve — key decisions and new conventions get added during the project.
