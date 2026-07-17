# Citation Chaining (Step 4 refinement)

Systematic gap detection via the OpenAlex citation graph. This complements the gap/breadth analysis already in Step 4: that catches what the *search agents noticed* they missed; chaining catches what the *field* treats as foundational but every WebSearch query happened to skip — especially older primary papers and adjacent papers from an author you already cite.

## Why co-citation degree (not raw citation count)

For each paper your review's citations reference, count how many of them cite it — its **co-citation degree** within your corpus. A paper cited by many of your seeds but absent from your review is a high-confidence miss.

Ranking by co-citation degree is the whole point. Ranking the same candidates by **raw citation count** instead surfaces famous general reviews (the NEJM/Lancet "Endometriosis" reviews, staging-system papers) — real, but not the *primary* sources you're missing. Co-citation degree surfaces the field-specific primary literature your seeds actually build on.

## The pipeline

Collect → Chain → Triage → **Explore** → Integrate. The Explore stage is mandatory and is what makes the added papers report-quality rather than bare citations.

### 1. Collect
Gather every DOI/PMID from the agent findings collected in Step 3 (and any earlier refinement). A finished-review markdown file works directly — the script regex-extracts identifiers.

### 2. Chain (run the script)
```
python3 references/cochain.py <review_or_findings_file> --mailto <your-email> --top 40
```
It resolves your seeds in OpenAlex, tallies co-citation degree from their `referenced_works` (no web searches; ~5 API calls total), and writes:
- `_cochain_candidates.md` — ranked human-readable shortlist
- `_cochain_candidates.json` — the same rows plus reconstructed abstracts, for triage

OpenAlex is free, needs no key, allows ~100k calls/day; always pass `--mailto` for the faster polite pool.

### 3. Triage (LLM) — the filter that makes this usable
Read `_cochain_candidates.json` and, with full knowledge of the review's sub-questions, decide for each candidate:

1. **Primary vs. review.** Keep primary research (and the occasional authoritative review that fills a genuine framing gap). **Do not trust the `type` field** — OpenAlex mislabels most narrative reviews as `article`. Judge from the title and abstract.
2. **Relevance.** Does it speak to a specific sub-question, or is it generic background? Drop generic background unless it is genuinely foundational (e.g., the paper establishing a premise the whole review rests on).
3. **Novelty.** Is it already covered by a paper you cite, or is it an adjacent/companion paper adding real content (a different cohort, an earlier landmark, a distinct mechanism)?
4. **Target section.** Map each survivor to the exact section it belongs in.

Output a short table: `paper | primary? | supports (claim) | target section | keep/drop`. Aim to keep the handful that materially improve the review, not every co-cited classic. For a large candidate set, this triage can be delegated to one dedicated agent given the JSON + the sub-question list.

### 4. Explore (mandatory — do not stub in a citation)
Every surviving paper must be researched to the same depth as the original search agents' findings before it enters the report. Route the survivors — clustered by target section — through search agents using `search-agent-prompt.md`. Each agent:
- web-grounds the paper's **actual** findings with quantitative specifics (n=, effect sizes, % / fold changes, mechanisms, model system);
- confirms existence and metadata (Step 6 verification);
- reports which section/claim it supports.

A chained paper that cannot be explored to that depth is **dropped, not inserted as a bare "[Author, Year]"**. This is the rule that keeps chaining from degrading the review into an annotated bibliography.

### 5. Integrate
Fold the explored findings into their target sections during synthesis (Step 5), exactly like any other finding — connected narrative, quantitative detail, primary-over-review. Update the reference list and note the chaining step in the Methods section (how many candidates were surfaced, triaged, explored, and added).

## Ranking signals available from the script
- `overlap` — co-citation degree (primary sort; the key signal)
- `cited_by_count` — total citations (secondary sort; biased toward old/review papers)
- `fwci` — field-weighted citation impact, normalized for field+year+type (useful to spot recent high-impact papers a raw count would bury)
- `publication_year` — to distinguish "missing landmark" from "missing recent work"

## Caveats / failure modes
- **`type` is unreliable** for primary-vs-review — the triage LLM must judge from title/abstract, never the field alone.
- **Amplifies seed bias.** Chaining inherits whatever skew is in your seed set; it is a comprehensiveness layer on top of good discovery, not a substitute for it.
- **Reference-list coverage varies.** OpenAlex parses references well for recent/OA/major-venue papers, less so for old or paywalled ones — some backward links will be missing.
- **Citation counts are approximate** (OpenAlex's own graph, not Scopus/WoS). Fine for ranking within the candidate set; do not quote as ground truth.

## Optional: forward chaining
The script does backward chaining (a seed's references — best for missing *foundational primary* work). To also catch *recent* primary work building on your seeds, add forward chaining: for the 2–3 highest-relevance seeds, `GET .../works?filter=cites:<seedID>&sort=cited_by_count:desc&per-page=25`. It is higher-volume and skews toward derivative work, so cap it harder and triage the same way.
