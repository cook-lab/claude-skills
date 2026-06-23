# Cook Lab Notebook — conventions (canonical)

The single source of truth for what a well-formed entry looks like in the lab Teamspace. Both
skills read this file:
- **lab-notebook** uses it to *create* and *tidy/reconcile* entries.
- **lab-pm** uses it to *audit* convention adherence (e.g. during weekly review).

Keep this file the one place these rules live. If a rule changes, change it here.

## How to apply

Each rule below is tagged with a fix policy:
- **[auto]** — safe to fix automatically without asking (no information is invented or destroyed).
- **[confirm]** — propose the fix and apply only on the owner's / David's go-ahead (requires a
  judgment call or could overwrite human intent).

Never overwrite a human's prose to satisfy a convention. Tidy structure and metadata; preserve content.

## Experiments — `collection://23e878bf-8826-8111-b5b4-000bdef2369c`

| # | Rule | Fix policy | How to detect |
|---|------|-----------|---------------|
| E1 | Title matches `YYYYMMDD - Description` (8-digit date, space-hyphen-space, then a concise description) | [auto] normalize spacing/format; [confirm] if no date present at all | Regex on title `^\d{8} - .+` |
| E2 | `Date Created` is set and equals the title's `YYYYMMDD` | [auto] set it to the title date | Compare `date:Date Created:start` to title prefix |
| E3 | `Person` is set | [auto] if creator/owner is unambiguous (e.g. the requesting user); else [confirm] | `Person` array empty |
| E4 | Linked to ≥1 parent `Tasks` entry | [confirm] (which task is a judgment call) | `Tasks` array empty |
| E5 | Body is non-empty and has real content (what was done + interpretation) | [confirm] (offer to draft from context; never invent results) | Page body empty or only template headings |

## Tasks — `collection://23e878bf-8826-816e-a477-000b54e02223`

| # | Rule | Fix policy | How to detect |
|---|------|-----------|---------------|
| T1 | Linked to ≥1 `Projects` entry (no orphans) | [confirm] | `Projects` array empty |
| T2 | `Person` (owner) is set | [confirm] | `Person` array empty |
| T3 | `Status` is set | [confirm] | `Status` null |
| T4 | `Done` tasks have a "Summary of results" on the page | [confirm] (offer to draft from linked experiments) | Status = Done and no summary section |
| T5 | Name reads as one complete deliverable/objective (granularity) — not fragmented, not grand | [confirm] (soft, judgment) | Manual / on review |

## Projects — `collection://23e878bf-8826-81bd-b4c8-000b45c1b91e`

| # | Rule | Fix policy | How to detect |
|---|------|-----------|---------------|
| P1 | `Lead` is set (≥1) | [confirm] | `Lead` array empty |
| P2 | `Primary/External` is set (`Primary` or `Collaboration`) | [confirm] | `Primary/External` null |
| P3 | `Status` is set | [confirm] | `Status` null |

## Global
- **Never modify database structure** (no new properties, no schema/view changes). Entries only.
- Relations are mirrored automatically by Notion — set one side and the other fills in.
- When tidying someone else's entries (lab-pm), default to **reporting a punch list** the owner's
  own agent can apply, rather than editing their pages directly. Edit directly only on request.

## Severity for reporting
- **Hard** (should always hold): E1–E4, T1–T3, P1–P3. These are objective and mostly fixable.
- **Soft** (judgment / quality): E5, T4, T5. Flag for a human, don't enforce.
