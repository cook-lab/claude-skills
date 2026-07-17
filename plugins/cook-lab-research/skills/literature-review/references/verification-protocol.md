# Citation Verification Protocol

Prevent hallucinated citations — the most common and damaging failure mode of LLM-generated literature reviews. Studies show 28-91% hallucination rates in unverified AI citations.

## Verification is Non-Negotiable

Citation verification is a hard requirement, not best-effort. If the primary verification method (WebFetch/DOI resolution) is denied or unavailable, **do not silently downgrade** — switch to the fallback method with increased volume to compensate.

**Minimum threshold:** At least 50% of all citations must reach "Verified" status. If this is not achievable, flag it prominently in the Methods section.

### When WebFetch is unavailable

WebFetch may be denied in background agent execution. If this happens:
1. **Acknowledge the limitation immediately** — do not pretend title-search verification is equivalent to DOI resolution
2. **Increase title-search verification volume** — verify 20-25 citations via exact quoted title search (up from 15-20 via DOI)
3. **For the 5-10 most critical citations**, search for: exact title + first author + key finding term. This compensates for the reduced granularity of title-only verification.
4. **Flag prominently in Methods:** "WebFetch was unavailable; all verification performed via title-based WebSearch. Verified = exact-title match confirmed; Plausible = found in search results but not independently title-confirmed."

## Triage Strategy

Focus verification effort where it matters most.

**Verify first (Tier 1 — always verify):**
- Citations supporting the review's key claims and conclusions
- Citations attributed surprising or counterintuitive findings
- Citations from a single source (no corroboration from other agents)
- Citations where the attributed finding seems unusually specific or convenient

**Verify if time permits (Tier 2):**
- Citations supporting secondary claims
- Citations where multiple agents found the same paper independently (lower risk)

**Target: verify 15-20 citations in Tier 1 via DOI (or 20-25 via title search if DOI unavailable), plus 5-10 content accuracy checks.**

## Verification Methods

### Method 1: DOI Resolution (preferred)

Use WebFetch on the DOI URL:
```
WebFetch: https://doi.org/10.1038/s41586-024-xxxxx
```

**Check:**
- Does the page resolve? (404 or redirect to generic page = fabricated DOI)
- Does the title on the page match the cited title?
- Do the authors match?
- Does the year match?
- Is the journal correct?

If all match → **Verified**

### Method 2: Title Search (when DOI fails or is missing)

Use WebSearch with the exact title in quotes:
```
WebSearch: "Exact Paper Title Here" author_lastname
```

**Check:**
- Does the paper appear in results?
- Do metadata (authors, year, journal) match?

If found with matching metadata → **Verified**
If found but metadata differs slightly (e.g., preprint vs. published version) → **Plausible** with note

### Method 3: bioRxiv MCP (for bioRxiv/medRxiv DOIs)

Use `get_preprint` with the DOI:
```
get_preprint: 10.1101/2024.01.15.xxxxx
```

Also use `search_published_preprints` to check if the preprint has a journal version.

If MCP returns matching metadata → **Verified**

### Method 4: OpenAlex resolution (structured, no scraping)

If the Step 4 chaining script has already resolved the review's DOIs/PMIDs in OpenAlex, reuse that output. A resolved OpenAlex record confirms the paper exists and returns canonical title, authors, year, and venue, plus an `is_retracted` flag. It is a clean substitute for Method 1 when WebFetch is denied, and it never breaks paywalls (metadata only).

```
https://api.openalex.org/works/https://doi.org/<DOI>?mailto=<email>
https://api.openalex.org/works/pmid:<PMID>?mailto=<email>
```

Check that title/authors/year match and `is_retracted` is false → **Verified**. Caveat: content-accuracy checks still require the abstract or full text — OpenAlex confirms a paper exists, not that it says what you attributed to it.

## Confidence Levels

| Level | Definition | Action |
|-------|-----------|--------|
| **Verified** | DOI resolved OR title search confirmed. Title, authors, year match. | Include in report as-is |
| **Plausible** | Found in WebSearch results but DOI not independently verified, OR minor metadata discrepancy | Include with note: "[Plausible — not independently verified via DOI]" |
| **Unverified** | Cannot confirm paper exists via any method | Remove from report. Note in Gaps section: "Claimed source could not be verified: {title}" |

## Content Accuracy Checking

Citation existence is necessary but not sufficient. The second-most-common failure mode is citing a real paper but misattributing its findings. In head-to-head eval, 2/10 spot-checked citations in an unverified review contained subtle misrepresentations despite correct DOIs.

**For 5-10 load-bearing citations:**
1. WebFetch the paper URL (DOI landing page or publisher page)
2. Read the abstract and any visible text
3. Confirm the finding attributed in the review actually appears in the paper

**Specific checks that catch the most common errors:**
- **Gene/protein/receptor nomenclature**: Does the paper use the exact name cited? Older papers may use antibody clone names (e.g., "EB6") rather than modern receptor names (e.g., "KIR2DL1"). Do not equate these unless the paper explicitly does.
- **Sample size specificity**: Is the n= reported for the specific experiment cited, or for the overall study cohort? A paper with n=113 in its screening cohort may have only n=18 for the immunofluorescence analysis — citing "n=113" for the IF finding inflates apparent scale.
- **Direction of effect**: Is the claimed increase/decrease/no-change correct?
- **Attribution of findings**: Is the specific result from this paper, or from a different paper it cites? Review articles are particularly prone to this — the review describes a finding, the search agent cites the review, but the finding is actually from a primary paper cited within the review.
- **Conflation of similar papers**: Two papers from similar groups on the same topic may have distinct findings. Confirm the attributed finding belongs to the specific paper cited, not a related one.

**Mark content-checked citations:** Add "[Content verified]" after the citation in the reference list.

## Common Hallucination Patterns

Watch for these specific failure modes:

1. **Real author + fabricated paper**: A well-known researcher cited for a paper they never wrote. Verify by searching the author's actual publication list.
2. **Real paper + wrong findings**: The paper exists but doesn't say what's attributed. Only caught by content accuracy checking.
3. **Plausible DOI that doesn't resolve**: DOI follows the correct format (10.xxxx/xxxxx) but points nowhere. Always resolve DOIs via WebFetch.
4. **Preprint cited as published**: A bioRxiv preprint cited as if it appeared in a journal. Use `search_published_preprints` to check status.
5. **Merged citations**: Findings from two different papers conflated into one citation. Check if the attributed finding is too broad for a single paper.
6. **Nomenclature conflation**: Paper uses older terminology (antibody clones, legacy gene names) but the review cites it using modern nomenclature that the paper never uses. The mapping may be imprecise (e.g., EB6 antibody recognizes KIR2DL1 AND KIR2DS1, so citing "elevated KIR2DL1" from an EB6 study is inaccurate).
7. **Sample size inflation**: Paper has a large overall cohort but the specific experiment cited used a small subset. Citing the overall cohort n= for a subset experiment misrepresents the evidence base.

## Disclosure

Report the following in the review's Methods section:
- How many citations were verified (Tier 1 count)
- How many were content-checked
- How many were flagged as Plausible or Unverified
- Explicit statement that non-verified citations originate from WebSearch results but were not independently confirmed
