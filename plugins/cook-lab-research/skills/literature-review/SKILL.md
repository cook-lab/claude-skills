---
name: literature-review
description: >
  Rigorous, web-search-grounded literature review with citation verification. Use when the user
  wants a literature review, evidence synthesis, citation search, or a picture of what is known
  about a scientific topic, or asks for comprehensive, citation-backed analysis of one. Decomposes
  the topic into focused questions, searches in parallel via web and bioRxiv, runs OpenAlex
  co-citation chaining to find missed primary sources, verifies citations, and writes a structured
  markdown report with gap analysis. Every claim comes from a search result, not from memory.
---

# Literature Review

A multi-agent, web-search-grounded literature review: decompose the topic, search in parallel, fill gaps with one refinement round, synthesize, verify citations, analyze gaps, and write the report.

## Rules

These are what make the review usable as a citable source.

1. **Every factual claim comes from a WebSearch or bioRxiv result.** Knowledge from training can suggest where to look, but a claim enters the review only once a search has found it. When a search finds nothing relevant, say so in the report instead of filling the gap from memory. If WebSearch fails or returns irrelevant results, record that under Gaps and Limitations.
2. **Every citation carries a DOI, PMID, or URL**, and each claim cites its own source. "Several studies have shown [1-5]" is not attribution.
3. **Primary research over reviews.** When a finding comes from a review article, find and cite the original paper; cite the review for orientation only.

## 1. Landscape scan

Run two or three searches for recent reviews or perspectives on the topic and look at how the field organizes itself: its major sub-areas, what recent reviews give their own sections, what is emerging. Keep it brief; it exists to inform the decomposition.

## 2. Decompose

A **narrow** topic (one technique, finding, or well-bounded question) gets 3-5 sub-questions (current state, methods, limitations, recent developments); proceed without asking. A **broad** topic (more than one biological system, method, or disease context) gets 10-15 sub-questions in thematic groups; show them to the user for approval before searching. For a question asked in passing ("what's known about X"), give a brief searched answer and offer the full review. When unsure whether a topic is broad, treat it as broad and show the plan.

Good sub-questions target one cell type, pathway, method, or system each. Bundled questions ("macrophages, NK cells, and DCs") lead agents to cover the dominant sub-topic and neglect the rest. Include, where relevant, a foundational question (landmark studies), a recent-change question (last 2-3 years), a methods question, a translational question, and at least one question that probes limitations, contradictions, or negative findings.

An illustrative broad decomposition, for "immune dysfunction in endometriosis" (derive the groups for a new topic from its own landscape scan):

```
1. Macrophage polarization, origin, and metabolic reprogramming
2. NK cell dysfunction — receptor balance, cytokine suppression
3. Neutrophil roles and NETosis in lesion establishment
4. Dendritic cell maturation and mast cell contributions
5. CD4+ T cell subsets (Th1/Th2, Th17, Tregs)
6. CD8+ T cell exhaustion and cytotoxic impairment
7. B cells, autoantibodies, and tertiary lymphoid structures
8. Pro-inflammatory and immunosuppressive cytokines
9. Chemokine networks and immune cell recruitment
10. Immune checkpoint pathways and IDO
11. Estrogen and progesterone modulation of immune function
12. Single-cell transcriptomics of immune populations
13. Spatial transcriptomics and immune niche organization
14. Links to infertility, pain, and malignant transformation
```

## 3. Search in parallel

Group the sub-questions into clusters of 2-3 related questions and give each cluster to one search agent (for 3-5 sub-questions, one agent each). Use at most 7 agents; about 5 suits most broad reviews. Launch them in one message so they run concurrently, using the Agent tool with `subagent_type: "general-purpose"` and the prompt in [references/search-agent-prompt.md](references/search-agent-prompt.md), filled in with the agent's questions, the broader topic, and the list of the other sub-questions.

Agents report findings paper by paper (citation, key finding with quantitative detail, relevance), their search log, gaps, and a breadth flag. They do not synthesize; that is your job.

## 4. Refinement round (one, at most)

Two mechanisms, run once each:

- **Gap-driven follow-up.** From the agents' gaps and breadth flags, pick the 2-4 sub-topics that are clearly under-covered: a rich sub-literature an agent could only partly explore, an expected topic with zero results (it may need different search terms), or a recently emerged area missing from the decomposition. Send 1-3 follow-up agents with narrow questions and the same prompt. Skip this when coverage is good, when the gaps are genuine literature gaps rather than search gaps, or when the topic is narrow.
- **Co-citation chaining (OpenAlex).** Catches foundational primary papers that every search query happened to miss. Collect all DOIs/PMIDs, run `references/cochain.py`, triage the ranked candidates to genuine primary research relevant to a sub-question (judge from title and abstract; OpenAlex's `type` field is unreliable), then have a search agent research each survivor to the same depth as any other finding before it enters the report. A chained paper that can't be explored to that depth is dropped, not inserted as a bare citation. Full protocol: [references/citation-chaining.md](references/citation-chaining.md).

Stop after this round; further rounds cost more than they find. Report remaining gaps in the Gaps section.

## 5. Synthesize

You are an aggregator, not a compressor. Keep one report section per sub-question (or per closely related pair); merge sections only when their literatures genuinely overlap. Every finding an agent reported appears in the report unless another agent duplicated it or it failed verification.

Within each section, write a connected narrative: historical context, key discoveries, current understanding, open questions. Separate consensus findings, single-source findings, contradictions (give both sides), and negative results. Keep the quantitative detail from primary sources (sample sizes, effect sizes, p-values, the specific experiment): "3 of 6 ectopic samples showed mature TLS (n=18)", not "TLS were found in lesions". Cross-reference sections where a mechanism in one bears on another.

## 6. Verify citations

Follow [references/verification-protocol.md](references/verification-protocol.md): confirm that the load-bearing citations exist and say what the review attributes to them, label each citation Verified, Plausible, or Unverified, and remove the Unverified ones. If WebFetch is unavailable, use the protocol's fallback and say in the Methods section that you did.

## 7. Gaps

A dedicated section. Consider six dimensions: temporal (old or sparse recent evidence), methodological, sample/model concentration, replication, translation, and unresolved contradictions. Label each gap as a **literature gap** (the field hasn't addressed it) or a **search limitation** (this search may have missed it).

## 8. Write the report

Write `{topic-slug}-literature-review.md` in the current directory, following [references/output-template.md](references/output-template.md): executive summary (3-5 cited takeaways), thematic sections, gaps and limitations, methods (search strategy, verification counts, chaining counts), and references with verification status. The report's length follows its coverage: every sub-question covered with its quantitative detail, and no filler sections or repeated summaries. Then give the user a short summary of the top findings, the largest gaps, and the verification results.

Follow-up requests (deeper coverage of one theme, more verification) can be handled with targeted searches without re-running the workflow.

## Tool notes

- **bioRxiv MCP:** `search_preprints` filters only by category and date range, not keyword. Use WebSearch for discovery; use the bioRxiv tools to browse recent preprints in relevant categories and to check or enrich bioRxiv DOIs.
- **OpenAlex:** free, no key, about 100k calls/day (pass `mailto=`). Good for resolving identifiers and walking references; its text search is literal keyword matching, so it does not replace WebSearch for discovery.
- **Paywalls:** WebFetch returns landing pages and abstracts, not full text. Verify against what it can see.
