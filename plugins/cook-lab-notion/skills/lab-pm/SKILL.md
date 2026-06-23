---
name: lab-pm
description: >
  Lab-wide oversight of the Cook Lab Notion Teamspace for the PI (David Cook) — cross-project
  status, stale-work detection, 1:1 and lab-meeting prep, trainee progress summaries, and
  notebook-adoption monitoring. This is the PI's whole-lab / cross-person view — for one person's own
  tasks or a single project's status, use the `lab-notebook` skill instead. Use for "lab status",
  "what's everyone working on", "prep my
  1:1 with X", "lab meeting digest", "what's stale", "who's logging experiments", "weekly
  update", "progress summary for X". Read-mostly: this skill reports and prepares; it does not
  reassign or close other people's work without explicit confirmation.
---

# Cook Lab — PM & Oversight

Cross-cutting view of the lab's Notion Teamspace for the PI. The companion `lab-notebook` skill is
for individual labmates doing their own work; this one is for *seeing across* everyone's work and
for the things that make the system pay off: meeting prep, progress narratives, and gentle nudges
that improve adoption.

Use the same database IDs, schemas, and Notion conventions as `lab-notebook` (see that skill).
Roster (name → user ID) is also there.

- Projects — `collection://23e878bf-8826-81bd-b4c8-000b45c1b91e`
- Tasks — `collection://23e878bf-8826-816e-a477-000b54e02223`
- Experiments — `collection://23e878bf-8826-8111-b5b4-000bdef2369c`

**Read-mostly.** Report, summarize, and prepare. Only create/modify entries when David explicitly
asks, and never silently close or reassign a trainee's task.

## Core workflows

### 1. Lab status board
Query all Projects with their Status and Lead; for each active project, roll up its Tasks by Status.
Present a compact board: project → lead → counts (In progress / Waiting / To do / Done) → the 1–2
tasks currently moving. Flag projects with **no In-progress task** and **no recent experiment
activity**.

### 2. Stale / stuck detection
Surface, with the responsible person:
- Tasks `In progress` or `Waiting` whose linked experiments haven't been updated recently (use
  experiment `Date Created` / page edit times as the activity signal).
- Tasks `Waiting` for a long time (likely blocked — worth a check-in).
- Projects `In progress` with zero recent experiment entries.
Frame these as check-in prompts, not judgments.

### 3. 1:1 prep
For a given person: their open tasks (grouped by project, by status), their experiments since the
last 1:1, what advanced, what's stalled, and 3–5 concrete talking points / decisions needed.
Cross-reference `~/Assistant/` for any standing 1:1 items if available.

### 4. Lab-meeting digest
What moved across the whole lab in a date window (default: last 7 days), built from experiment
entries and task status changes. Group by project; one or two lines each; call out wins and
blockers. Output as a clean summary David can paste or read from.

### 5. Trainee progress summary ⭐ (the adoption payoff)
Turn a person's experiment log into a narrative — for reviews, committee reports, fellowship
applications, or reference letters. This is the *reason logging is worth it for the trainee*: their
own diligence becomes a ready-made progress report. When you generate one, it's worth noting to the
trainee that consistent logging is what made it possible.

### 6. Notebook-adoption check
Per person: when did they last log an experiment, how many in the last month, which of their active
tasks have **no** linked experiments. Present it constructively — the goal is to find who could use
a nudge or a hand getting set up, and to recognize consistent loggers (e.g. surface exemplary recent
entries that can serve as models for others). Do **not** turn this into a leaderboard or anything
punitive.

### 7. Convention audit
Check adherence to the canonical conventions in `../../conventions.md` (plugin root) across a chosen
scope — whole lab, one person, or one project. For each rule, query the relevant database and collect
violations. Report grouped by **person** and **severity**:
- **Hard** (objective, mostly fixable): missing `Projects`/`Tasks` links, missing `Person`/`Status`,
  experiment title not `YYYYMMDD - …`, `Date Created` ≠ title date, `Done` task with no summary,
  project missing `Lead`/`Primary-External`.
- **Soft** (judgment): task granularity, thin experiment bodies.

Output, per person, a short **punch list** their own `lab-notebook` skill can apply — they just say
"tidy my notebook" and it auto-fixes the safe `[auto]` items and proposes the rest. Offer to batch-fix
the safe items directly only on David's go-ahead; never edit a trainee's prose.

### 8. Weekly review (composite) ⭐
The one-shot to run for weekly review. Chain into a single skimmable report, leading with what needs
David's attention:
1. **Lab status board** (#1) — what's moving per project.
2. **Stale / stuck detection** (#2) — what needs a check-in.
3. **Convention audit** (#7) — hard violations per person (the tidy punch lists) + soft flags.
4. **Lab-meeting digest** (#4) — what advanced this week.

Then offer to send each trainee their punch list and to prep talking points for anyone with stalled
work.

## Data hygiene & conventions
The checkable rules and their fix policies are **canonical in `../../conventions.md`** (plugin root) —
the same file the `lab-notebook` skill uses, so the lab keeps one definition. Use the **Convention
audit** (#7) to apply them at scale. Report and offer to fix; change entries only on David's
go-ahead, and never edit a trainee's prose.

## Guardrails
- Never modify database **structure**.
- Don't reassign, close, or delete a trainee's entries without explicit confirmation.
- Keep adoption framing supportive — this system only works if people want to use it.
