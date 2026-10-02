# Citation Verification Protocol

Search agents assemble citations from search results, and the two failures that most damage a literature review are citations to papers that don't exist and real papers cited for findings they don't contain. Verification checks both, focused on the citations the review's conclusions rest on.

## What to verify

- **Existence (Tier 1, always):** citations behind the key claims and conclusions, surprising or unusually convenient findings, and anything supported by a single source. Aim for 15-20 citations on a broad review.
- **Existence (Tier 2, if time allows):** citations for secondary claims, and papers several agents found independently (lower risk).
- **Content (5-10 load-bearing citations):** read the abstract and confirm the attributed finding is actually there.

At least half of all citations should reach Verified. If they don't, say so in Methods and name the lowest-confidence citations.

## Methods

1. **DOI resolution (preferred):** WebFetch `https://doi.org/<DOI>`. A 404 or a redirect to a generic page means a fabricated DOI. Check title, authors, year, and journal against the citation.
2. **Title search:** WebSearch the exact title in quotes plus the first author's surname; check the metadata in the results.
3. **bioRxiv MCP:** `get_preprint` with the DOI for bioRxiv/medRxiv papers, and `search_published_preprints` to see whether a journal version exists.
4. **OpenAlex:** if the chaining script already resolved the identifiers, reuse its output (`https://api.openalex.org/works/https://doi.org/<DOI>?mailto=<email>` or `.../works/pmid:<PMID>`). It confirms existence and gives canonical metadata plus an `is_retracted` flag, but not what the paper says.

**If WebFetch is unavailable** (it can be denied when agents run in the background): verify by title search and OpenAlex instead, check 20-25 citations rather than 15-20 because title matching is less precise, add the first author and a key finding term to the searches for the 5-10 most important citations, and state in Methods: "WebFetch was unavailable; verification relied on title-based search and OpenAlex. Verified = exact-title or identifier match; Plausible = found in search results but not independently confirmed."

## Confidence levels

| Level | Meaning | In the report |
|-------|---------|---------------|
| **Verified** | Resolved by DOI, exact-title search, or OpenAlex; title, authors, and year match | Cite as-is |
| **Plausible** | Found in search results but not independently confirmed, or minor metadata differences (e.g., preprint vs. published) | Cite with "[Plausible — not independently verified]" |
| **Unverified** | Cannot confirm the paper exists | Remove; list under Gaps as "Claimed source could not be verified: {title}" |

Mark content-checked citations "[Content verified]" in the reference list.

## What content checks catch

- **Nomenclature:** older papers may use antibody clone names (e.g., "EB6") rather than receptor names (e.g., "KIR2DL1"), and the mapping may be imprecise (EB6 recognizes KIR2DL1 and KIR2DS1). Use the paper's own terms unless it makes the equivalence itself.
- **Sample size:** is the n for the specific experiment cited, or for the whole cohort? A study with n=113 overall may have n=18 for the immunofluorescence analysis.
- **Direction of effect:** increased, decreased, or no change.
- **Attribution:** is the result from this paper, or from a paper it cites? Reviews are the usual source of this error.
- **Conflation:** two papers from the same group on the same topic can have different findings; two papers can be merged into one citation.
- **Invented papers:** a real, well-known author cited for a paper they never wrote; check the author's publication list.
- **Preprint cited as published:** check with `search_published_preprints`.

## Disclosure (in the Methods section)

Report how many citations were verified, how many were content-checked, and how many are Plausible or Unverified, and state that non-verified citations come from search results but were not independently confirmed.
