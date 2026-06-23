# Literature Review Output Template

## File Naming

Write the report to `{topic-slug}-literature-review.md` in the current working directory.

Topic slug: lowercase, hyphens, no special characters. Examples:
- "endometriosis pathobiology" → `endometriosis-pathobiology-literature-review.md`
- "spatial transcriptomics FFPE methods" → `spatial-transcriptomics-ffpe-methods-literature-review.md`

## Report Template

```markdown
# Literature Review: {Topic Title}

**Generated:** {YYYY-MM-DD}
**Scope:** {1-2 sentence description of what was reviewed and any boundaries}
**Sub-questions addressed:**
1. {question 1}
2. {question 2}
...

---

## Executive Summary

{3-5 key takeaways from the review. Each should be a declarative statement with citation support. These are the "headlines" — what someone should know if they read nothing else.}

---

## {Theme 1 Title}

### Current Understanding

{Narrative synthesis of the theme. Every factual claim has inline citation. Write declaratively — state what is known, what is emerging, and where uncertainty remains. Include specific numbers, sample sizes, and methods where available.}

### Key Findings

- {Specific finding with citation} [Author et al. Year, DOI]
- {Specific finding with citation} [Author et al. Year, DOI]
- ...

### Open Questions

- {Theme-specific gap or unresolved question}
- {Contradiction or area of active debate}

---

## {Theme 2 Title}

{Same structure: Current Understanding → Key Findings → Open Questions}

---

{Repeat for each theme...}

---

## Gaps and Limitations

### Literature Gaps

{What the field has NOT addressed. Organized by the six gap dimensions where applicable:}

**Temporal:** {Are findings relying on older work? Is recent evidence sparse?}
**Methodological:** {Are certain approaches underrepresented?}
**Sample/Model:** {Are studies concentrated in one model system, species, or demographic?}
**Replication:** {Are key findings from single studies or independently replicated?}
**Translation:** {Is there a disconnect between mechanistic findings and clinical application?}
**Contradictions:** {Where do sources disagree? What might explain the discrepancies?}

### Search Limitations

{What our search may have missed. Be honest:}
- Databases not searched (e.g., Scopus, Web of Science — these are not accessible via our tools)
- Language limitations (English-language sources only)
- Failed or low-yield queries
- Topics where WebSearch returned noisy or off-topic results

### Confidence Assessment

{Overall assessment: How confident are you in the review's coverage of the topic? What areas have strong coverage vs. thin coverage?}

---

## Methods

### Search Strategy

- **Primary tool:** WebSearch ({N total queries across {N} sub-questions)
- **Supplementary:** bioRxiv MCP (categories: {list}, date range: {range})
- **Date focus:** {date range prioritized}
- **Sub-questions and search agents:** {brief description of decomposition and parallel search approach}

### Verification Status

- **Citations verified (DOI/title confirmed):** {N} of {total}
- **Citations content-checked (abstract reviewed):** {N}
- **Plausible (not independently verified):** {N}
- **Removed (unverifiable):** {N}

---

## References

{Alphabetical by first author. Each entry includes verification status.}

1. Author1, Author2 et al. (Year). "Title." *Journal*. DOI: https://doi.org/... [Verified]
2. Author1, Author2 et al. (Year). "Title." *Journal*. DOI: https://doi.org/... [Verified, Content checked]
3. Author1, Author2 et al. (Year). "Title." *Source*. URL: ... [Plausible]
...
```

## Synthesis Quality Standards

### Good synthesis (citation-grounded, specific, narrative):

> A seminal study by Bacci et al. demonstrated that adoptive transfer of alternatively activated macrophages dramatically enhanced endometriotic lesion growth in mice, while inflammatory macrophages were protective (n=not reported per group, assessed by lesion size and vascularization) [Bacci et al. 2009, DOI:10.2353/ajpath.2009.081011]. Over a decade later, Hogg et al. refined this framework by showing that macrophage *origin* — not just polarization state — determines function: endometrial macrophages that arrive with retrograde menstrual tissue are "proendometriosis," promoting lesion establishment, whereas monocyte-derived large peritoneal macrophages (LpM) are "antiendometriosis" and protect the cavity from lesion formation. Constitutive inhibition of monocyte recruitment reduced peritoneal macrophage populations and paradoxically increased lesion number [Hogg et al. 2021, DOI:10.1073/pnas.2013776118]. Most recently, single-cell analysis identified two distinct prodisease lesion-resident macrophage phenotypes resembling tumor-associated macrophages (TAMs) and scar-associated macrophages, alongside protective peritoneal macrophages associated with lesion resolution [Henlon et al. 2024, DOI:10.1073/pnas.2405474121].

### Bad synthesis (vague, summary-level attribution):

> Macrophages play an important role in endometriosis. Several studies have shown they can be both pro- and anti-disease (Bacci et al., 2009; Hogg et al., 2021; Henlon et al., 2024).

### Key differences:
- Good: builds a historical narrative (seminal → refinement → current), includes experimental details (adoptive transfer, monocyte inhibition, scRNA-seq), specific findings with directionality, each claim tied to one source
- Bad: no specifics, no experimental detail, lumped citations, reads as a placeholder rather than a synthesis
- Good: reads like a review article section you could put in a grant background
- Bad: reads like an annotated search result

## Gap Section Quality Standards

### Good gap identification:

> **Replication:** The finding that SecA cells are enriched in chemoresistant tumors has been reported by two independent groups using scRNA-seq [Cook et al. 2023; Vazquez-Garcia et al. 2022], but has not been validated using orthogonal methods (e.g., spatial transcriptomics, flow cytometry). Whether this enrichment reflects true selection or sampling bias in dissociation-based methods remains unresolved.

### Bad gap identification:

> More research is needed in this area.

### Key differences:
- Good: names the specific finding, identifies which dimension is lacking (orthogonal validation), names what would fill the gap, distinguishes between explanations
- Bad: says nothing actionable
