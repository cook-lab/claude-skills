#!/usr/bin/env python3
"""
Co-citation chaining for the literature-review skill (Step 4 refinement).

Given the papers a review already cites (its "seeds"), this looks at every paper
those seeds reference and ranks them by CO-CITATION DEGREE: how many of your
seeds cite each candidate. A paper cited by many of your seeds but absent from
your review is a high-confidence "you missed this" signal — and, unlike ranking
by raw citation count, co-citation degree surfaces field-specific primary papers
rather than famous general reviews.

The backward pass is nearly free: `referenced_works` is returned with each seed
when it is resolved, so no extra calls are needed to build the candidate set.
Only the final metadata+abstract lookup for the shortlist costs calls.

Usage:
    python3 cochain.py INPUT [--min-overlap 2] [--top 40] [--out DIR] [--mailto you@inst.edu]

INPUT may be a markdown review file or any text file containing the citations —
DOIs (10.x/...) and PMIDs (PMID: 12345) are extracted by regex, so both work.

Outputs (next to INPUT unless --out given):
    _cochain_candidates.md     ranked human-readable shortlist
    _cochain_candidates.json   same rows + reconstructed abstracts, for LLM triage

The JSON is the input to the triage stage (see citation-chaining.md): an LLM
classifies each candidate primary-vs-review, scores relevance to the review's
sub-questions, and maps survivors to a target section.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request
from collections import defaultdict

API = "https://api.openalex.org/works"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cochain (literature-review skill)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def batch(ids, field, select, mailto, chunk=25):
    """Resolve a list of ids via an OR filter, chunked, staying under 10 req/s."""
    out = []
    for i in range(0, len(ids), chunk):
        grp = ids[i:i + chunk]
        filt = f"{field}:" + "|".join(grp)
        url = (f"{API}?filter={urllib.parse.quote(filt, safe=':|/.')}"
               f"&select={select}&per-page={chunk}&mailto={mailto}")
        try:
            out += get(url).get("results", [])
        except Exception as e:
            print(f"  ! {field} chunk {i//chunk} failed: {e}", file=sys.stderr)
        time.sleep(0.15)
    return out


def short(openalex_url):
    return openalex_url.rsplit("/", 1)[-1]


def deinvert(inv):
    """Reconstruct plain-text abstract from OpenAlex abstract_inverted_index."""
    if not inv:
        return ""
    pos = [(p, w) for w, locs in inv.items() for p in locs]
    pos.sort()
    return " ".join(w for _, w in pos)


def first_author(w):
    a = w.get("authorships") or []
    return (a[0]["author"]["display_name"].split()[-1] + " et al.") if a else "?"


def venue(w):
    return ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "") or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--min-overlap", type=int, default=2)
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--out", default=None)
    ap.add_argument("--mailto", default="research@example.edu")
    args = ap.parse_args()

    text = open(args.input, encoding="utf-8").read()
    dois = sorted({m.rstrip(".,;)]").lower() for m in re.findall(r'10\.\d{4,9}/[^\s\]\)]+', text)})
    pmids = sorted(set(re.findall(r'PMID:\s*(\d+)', text)))
    print(f"Extracted: {len(dois)} DOIs, {len(pmids)} PMIDs")

    sel = "id,doi,display_name,type,publication_year,cited_by_count,fwci,referenced_works"
    seeds = batch([f"https://doi.org/{d}" for d in dois], "doi", sel, args.mailto)
    if pmids:
        seeds += batch([f"https://pubmed.ncbi.nlm.nih.gov/{p}" for p in pmids], "pmid", sel, args.mailto)

    seen = {short(w["id"]): w for w in seeds}
    seeds = list(seen.values())
    existing = set(seen.keys())
    n_rev = sum(1 for w in seeds if w.get("type") == "review")
    print(f"Resolved {len(seeds)}/{len(dois)+len(pmids)} "
          f"({n_rev} typed review, {len(seeds)-n_rev} primary/other)")

    # Backward chaining. Seed only from non-review papers (review reference lists
    # add noise). NOTE: OpenAlex `type` mislabels many narrative reviews as
    # "article", so this only removes clearly-typed reviews — the real
    # primary-vs-review filter is the LLM triage stage downstream.
    cocite = defaultdict(list)
    for w in seeds:
        if w.get("type") == "review":
            continue
        for ref in w.get("referenced_works", []):
            rid = short(ref)
            if rid not in existing:
                cocite[rid].append(w["display_name"])

    print(f"Backward candidates not already cited: {len(cocite)}")
    for k in (2, 3, 4):
        print(f"  co-cited by >= {k} seeds: {sum(1 for v in cocite.values() if len(v) >= k)}")

    ranked = sorted(cocite, key=lambda k: -len(cocite[k]))
    top_ids = [k for k in ranked if len(cocite[k]) >= args.min_overlap][:max(args.top, 1) + 20]
    meta = {short(w["id"]): w for w in batch(
        top_ids, "openalex_id",
        "id,doi,display_name,type,publication_year,cited_by_count,fwci,"
        "authorships,primary_location,abstract_inverted_index", args.mailto)}

    rows = []
    for rid in top_ids:
        w = meta.get(rid)
        if not w:
            continue
        rows.append({
            "overlap": len(cocite[rid]),
            "type": w.get("type", ""),
            "year": w.get("publication_year"),
            "cites": w.get("cited_by_count", 0),
            "fwci": w.get("fwci"),
            "author": first_author(w),
            "title": w.get("display_name", ""),
            "venue": venue(w),
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "abstract": deinvert(w.get("abstract_inverted_index")),
            "cited_by_seeds": cocite[rid],
        })
    rows.sort(key=lambda r: (-r["overlap"], -r["cites"]))
    rows = rows[:args.top]

    # dirname("") and dirname("bare.md") are both "" -> fall back to CWD so a
    # bare input filename doesn't get treated as an output directory.
    outdir = args.out or os.path.dirname(args.input) or "."
    with open(f"{outdir}/_cochain_candidates.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    with open(f"{outdir}/_cochain_candidates.md", "w", encoding="utf-8") as f:
        f.write("# Co-citation chaining — candidates missing from the review\n\n")
        f.write("Ranked by co-citation degree (# of your papers that cite it), then total citations. "
                "Triage these: keep genuine PRIMARY research relevant to a sub-question; "
                "do NOT trust the `type` column for primary-vs-review.\n\n")
        f.write("| overlap | first author | year | type | cites | FWCI | title | doi |\n")
        f.write("|--:|---|--:|---|--:|--:|---|---|\n")
        for r in rows:
            fwci = f"{r['fwci']:.1f}" if isinstance(r["fwci"], (int, float)) else ""
            f.write(f"| {r['overlap']} | {r['author']} | {r['year']} | {r['type']} | "
                    f"{r['cites']} | {fwci} | {r['title'][:90]} | {r['doi']} |\n")
    print(f"Wrote {outdir}/_cochain_candidates.md and .json ({len(rows)} candidates)")


if __name__ == "__main__":
    main()
