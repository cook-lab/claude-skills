---
name: literature-review
description: >
  Rigorous, web-search-powered literature review with citation verification. Use when the user
  wants a literature review, evidence synthesis, citation search, or research landscape analysis.
  Triggers: "literature review", "what does the literature say", "find papers on", "search the
  literature", "evidence review", "what's known about", "review the research on", "find recent
  publications", "cite sources for", "research synthesis", or any request requiring comprehensive,
  citation-backed analysis of a scientific topic. Decomposes broad topics into focused questions,
  searches in parallel via web and bioRxiv, verifies citations, and produces a structured markdown
  report with gap analysis. ALL claims are web-search-grounded — never falls back to model-only.
---

# Literature Review

Multi-agent, web-search-grounded literature review with citation verification, gap analysis, and structured markdown output.

## Hard Rules

These are non-negotiable. Every violation undermines the review's value.

1. **Every factual claim must originate from a WebSearch or bioRxiv MCP result.** No claim may be sourced from training data alone. If a search returns no relevant results, report that explicitly — do not fill the gap with model knowledge.
2. **Every citation must include a verifiable identifier:** DOI, PMID, or URL. No "Author et al., Year" without a link.
3. **Never silently fall back to model-only responses.** If WebSearch fails or returns irrelevant results, state this in the report under Gaps and Limitations.
4. **Citation-level attribution, not summary-level.** Each claim links to its specific source. No "several studies have shown [1-5]."
5. **Search sub-agents MUST call WebSearch at least 5 times per assigned question.** This prevents shallow single-query coverage.
6. **Prefer primary research over review articles.** When a finding is attributed to a review, search for and cite the original primary source. Review articles are useful for orientation but should not be the primary citation for specific experimental findings.

## Workflow Overview

1. Landscape scan (quick web search to inform decomposition)
2. Decompose the topic into focused sub-questions (10-15 for broad topics)
3. Spawn parallel search agents
4. Collect reports, assess coverage, run refinement round if needed
5. Synthesize thematically with full narrative depth
6. Verify critical citations
7. Identify gaps (dedicated phase)
8. Write structured markdown report

## Step 1: Landscape Scan

Before decomposing, ground the decomposition in the current state of the field rather than relying solely on model knowledge.

1. Run 2-3 WebSearch queries for recent comprehensive reviews or perspectives on the topic (e.g., `"{topic}" review 2024 2025"`, `"{topic}" systematic review"`)
2. Read the titles, abstracts, and — where visible — section headings of the top 2-3 results
3. Note how the field currently organizes itself: what are the major sub-areas? What topics get dedicated sections in recent reviews? What's emerging?
4. Use this structure to inform the decomposition in Step 2

This step should take 2-3 minutes. Do not do a deep search — just enough to see the landscape.

## Step 2: Decompose

This is the most critical phase. The quality of decomposition determines the depth of the entire review.

### Assess scope

**Broad topic** (requires user confirmation): spans >1 biological system, >1 methodology, or >1 disease context.

**Narrow topic** (auto-proceed): focused on a specific technique, finding, or well-bounded question.

**Very casual query** (e.g., "what's known about X" in passing): offer a brief web-searched summary first, then ask: "Would you like me to run a full literature review on this?"

When in doubt, treat as broad and show the plan.

### Decompose

**For broad topics:**
1. Generate **10-15 focused sub-questions** organized into thematic groups, informed by both model knowledge and the landscape scan
2. Each sub-question should be specific enough that a single mechanism, cell type, or method is the focus — avoid bundling (e.g., "macrophages, NK cells, and DCs" is too broad; separate them)
3. Include where relevant:
   - A historical/foundational question: "What are the seminal findings and landmark studies?"
   - A temporal dimension: "What has changed in the last 2-3 years?"
   - A methodological dimension: "What approaches are being used?"
   - A clinical/translational dimension: "What is the therapeutic or diagnostic relevance?"
4. Present the decomposition to the user for approval. They may add, remove, or refine questions.

**For narrow topics:**
1. Auto-decompose into 3-5 sub-questions covering: current state, methods/approaches, limitations, recent developments
2. Proceed directly to Step 3

### Decomposition principles
- **Separate, don't bundle.** Each question should target one biological system, one cell type, one pathway, or one method. Bundled questions cause agents to find the dominant sub-topic and neglect the others.
- **Include contrarian angles.** At least one question should probe limitations, contradictions, or negative findings.
- **Aim for specificity.** "What cytokines are dysregulated?" is too broad. "What roles do IL-1beta, IL-33, and TGF-beta play in the peritoneal cytokine milieu?" is better.

### Example (broad: "immune dysfunction in endometriosis")

```
1. Macrophage polarization, origin, and metabolic reprogramming in endometriosis
2. NK cell dysfunction — receptor balance, cytokine suppression, and emerging mechanisms
3. Neutrophil roles and NETosis in lesion establishment
4. Dendritic cell maturation and mast cell contributions
5. CD4+ T cell subsets (Th1/Th2 balance, Th17, Tregs) — functional changes
6. CD8+ T cell exhaustion and cytotoxic impairment
7. B cells, autoantibodies, and tertiary lymphoid structures
8. Pro-inflammatory and immunosuppressive cytokines (IL-1beta, IL-6, TNF-alpha, IL-33, TGF-beta, IL-10)
9. Chemokine networks (CCL2, CCL5/RANTES, CXCL12) and immune cell recruitment
10. Immune checkpoint pathways (PD-1/PD-L1, CD47/SIRPa, CTLA-4, TIM-3) and IDO
11. Estrogen and progesterone modulation of immune cell function
12. Single-cell transcriptomics of immune populations in endometriosis
13. Spatial transcriptomics and immune niche organization in lesions
14. Immune dysfunction links to infertility, pain, and malignant transformation
```

## Step 3: Spawn Search Agents

Read [references/search-agent-prompt.md](references/search-agent-prompt.md) for the full agent prompt template.

### Agent scaling

Group sub-questions into thematic clusters of 2-3 related questions each. Assign one agent per cluster.

| Sub-questions | Agents | Strategy |
|--------------|--------|----------|
| 3-5 | 1 per question | Direct assignment |
| 6-10 | Group into 3-5 clusters of 2 | 1 agent per cluster |
| 11-15 | Group into 5-7 clusters of 2-3 | 1 agent per cluster |

Never spawn more than 7 agents. Target 5 for most broad reviews.

### Spawn agents in parallel

Use the Agent tool with `subagent_type: "general-purpose"` for each agent. Each gets:
- Their assigned question(s) from the decomposition
- The broader topic context
- The full prompt template from the reference file, with placeholders filled in
- A list of the other sub-questions (for awareness, not their responsibility)

### What agents return

Each agent reports:
- **Findings**: structured list (citation + key finding + relevance rating per paper)
- **Search log**: exact queries used, databases searched, result counts
- **Gaps**: what they searched for but couldn't find
- **Breadth flag**: sub-topics encountered but not fully covered, or questions that proved too broad for adequate coverage

Agents do NOT synthesize across papers. They report individual findings. Synthesis is the orchestrator's job.

## Step 4: Refinement Round

After collecting all agent reports, assess coverage before synthesizing.

### Review agent breadth flags and gaps

1. Read each agent's gaps and breadth flags
2. Identify 2-4 sub-topics that were either:
   - Flagged as "encountered but not covered" by an agent
   - Entirely absent from all agent reports despite being expected
   - Revealed as more complex than anticipated (agent found many papers but could only cover a fraction)

### Decide whether to refine

**Spawn follow-up agents if:** there are clear coverage gaps that targeted searches would fill. Typical triggers:
- An agent found a rich sub-literature it couldn't fully explore (e.g., "found 15+ papers on complement system but my question also covered chemokines — only covered chemokines")
- A topic expected to have literature produced zero results — may need different search terms
- A recently emerged sub-area was discovered that wasn't in the original decomposition

**Skip refinement if:** agent reports collectively cover the decomposition well, gaps are genuine literature gaps (not search gaps), or the topic is narrow.

### Execute refinement

Spawn 1-3 targeted follow-up agents with narrow, specific questions derived from the gap analysis. These agents follow the same prompt template but with focused questions.

**One refinement round maximum.** Do not iterate further — diminishing returns and escalating token costs. If gaps remain after refinement, report them in the Gaps section.

## Step 5: Synthesize

### Preserve decomposition granularity

The orchestrator is an **aggregator**, not a compressor. The decomposition separated topics for a reason — each sub-question targeted a distinct literature. Respect that structure:

- **Default to one report section per sub-question** (or per closely related pair). If the decomposition separated CD4+ T cells, CD8+ T cells, and B cells into 3 questions, the report should have 3 sections — do not merge them into "Adaptive Immunity."
- **Merge only when the literatures genuinely overlap** — e.g., if two questions produced the same papers with the same findings, combine them. But distinct cell types, distinct pathways, or distinct methodologies should remain separate.
- **Every finding reported by a search agent should appear in the final report** unless it is duplicated by another agent's finding or fails verification. Do not drop findings to save space.

### Thematic synthesis — narrative, not list

Within each section, build a connected narrative (not organized by agent):

1. Catalog all findings from all agents (initial + refinement) relevant to this section's topic
2. For each section, identify:
   - **Consensus findings**: supported by multiple independent sources
   - **Novel/emerging findings**: single source but potentially high-impact
   - **Contradictions**: sources that disagree — note both sides
   - **Negative results**: studies that found no effect or couldn't replicate
3. **Connect across sections**: where a mechanism in one section has implications for another, add a cross-reference (e.g., "The TGF-beta-mediated Treg expansion described above intersects with the NK cell suppression pathway discussed in the NK Cell Dysfunction section")

### Synthesis quality rules

The synthesis must read as a **connected narrative**, not an annotated bibliography:
- Build progressive arguments: historical context → key discoveries → current understanding → open questions
- Include **quantitative data** from primary sources: sample sizes, fold changes, p-values, AUC values, specific cell counts. Do not reduce "n=18, 3 of 6 ectopic samples showed mature TLS" to "TLS were found in lesions."
- **Trace review-article claims to primary sources.** If an agent cited a comprehensive review for a specific experimental finding, search for and cite the original paper instead. The review can be cited for broad context, but specific results need primary citations.
- Include negative and contrarian findings — these are often the most informative

## Step 6: Verify Citations

Read [references/verification-protocol.md](references/verification-protocol.md) for the full procedure.

### Verification is mandatory, not best-effort

Citation verification is a hard requirement. If verification tooling fails, **do not silently downgrade** — escalate visibly.

**Verification method priority:**
1. **WebFetch on DOI URL** (preferred — confirms paper exists, title/authors match)
2. **WebSearch for exact title in quotes** (fallback — less granular but confirms existence)
3. **bioRxiv MCP `get_preprint`** (for bioRxiv/medRxiv DOIs)

**If WebFetch is denied or unavailable:**
- Do NOT silently switch to title-only verification and call it done
- **Immediately note the limitation** in your working state
- Use WebSearch with exact quoted titles as the primary method instead
- **Increase the number of citations checked via title search** to compensate — target 20-25 title-verified rather than 15-20 DOI-verified, since title search is less granular
- For the 5-10 most critical citations, search for both the exact title AND the first author's name + key finding term to confirm content accuracy
- **Flag the limitation prominently** in the Methods section: "WebFetch was unavailable; verification relied on title-based search. Citations marked 'Verified' were confirmed via exact-title match; citations marked 'Plausible' could not be independently confirmed."

**Minimum verification threshold:** At least 50% of all citations must reach "Verified" status. If this threshold is not met, explicitly state this in the Methods section and identify which citations are lowest-confidence.

### Triage approach
- Identify the 15-20 most critical citations (those supporting key claims, surprising findings, or single-source claims)
- Verify each via WebFetch on DOI URL or WebSearch for exact title
- Assign confidence levels: **Verified** / **Plausible** / **Unverified**
- Remove any citation that cannot reach at least "Plausible"
- Content-check 5-10 load-bearing citations: read the abstract (via WebFetch or search result snippets) and confirm the attributed finding actually appears

**Content accuracy checks must verify specifics**, not just that the paper is topically relevant:
- Do the specific gene/protein/receptor names match what the paper reports?
- Is the sample size reported for the correct experiment within the paper (not the overall cohort)?
- Is the direction of effect correct (increased vs. decreased)?
- Is the finding from the cited paper or from a different paper it cites?

## Step 7: Identify Gaps

This is a dedicated phase, not an afterthought. Analyze across six dimensions:

1. **Temporal**: Is the field relying on older findings? Is recent work sparse?
2. **Methodological**: Are certain approaches underrepresented relative to the question?
3. **Sample/model**: Are studies concentrated in one model system, species, or demographic?
4. **Replication**: Are key findings from single studies or independently replicated?
5. **Translation**: Is there a disconnect between mechanistic findings and clinical relevance?
6. **Contradictions**: Where do sources disagree? What might explain discrepancies?

**Critical distinction**: For each gap, explicitly label it as a **literature gap** (the field hasn't addressed this) or a **search limitation** (our search may have missed this).

## Step 8: Write Report

Read [references/output-template.md](references/output-template.md) for the full template and quality examples.

Write the report to `{topic-slug}-literature-review.md` in the current working directory.

**Key sections:**
1. Executive summary (3-5 declarative takeaways with citations)
2. Thematic sections (Current Understanding → Key Findings → Open Questions)
3. Gaps and Limitations (literature gaps + search limitations + confidence assessment)
4. Methods (search strategy + verification status)
5. References (alphabetical, each marked with verification status)

After writing, present a brief summary to the user highlighting: the top findings, the most significant gaps, and the verification results.

## Adapting to Scope

| Aspect | Narrow query | Broad topic |
|--------|-------------|-------------|
| Landscape scan | 1-2 queries | 2-3 queries |
| Decomposition | Auto, 3-5 questions | User-confirmed, 10-15 questions |
| Agents | 2-3 | 5-7 |
| Searches/agent | 5+ | 5-8 |
| Refinement round | Skip unless clear gap | Yes, 1-3 follow-up agents |
| Verification | All critical citations | Top 15-20 + 5-10 content checks |
| Output length | 2,000-4,000 words | 5,000-10,000 words |
| Gap analysis | Brief, 2-3 dimensions | Detailed, all 6 dimensions |

## Notes

- **bioRxiv MCP constraint**: `search_preprints` only filters by category and date range — it does NOT support keyword search. Use WebSearch as the primary discovery tool. Use bioRxiv MCP for browsing recent preprints in relevant categories and for verifying/enriching bioRxiv DOIs found via WebSearch.
- **Paywalled content**: WebFetch gets landing pages and abstracts, not full text. Verify based on title/abstract metadata.
- **Follow-up**: After delivering the report, the user may request deeper coverage of a specific theme, additional verification, or expansion of the gap analysis. These can be handled as targeted follow-up searches without re-running the full workflow.
