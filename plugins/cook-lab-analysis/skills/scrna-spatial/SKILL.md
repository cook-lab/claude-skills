---
name: scrna-spatial
description: >
  Cook Lab decisions for single-cell RNA-seq and spatial transcriptomics analysis (Xenium, Visium,
  CosMx): QC and filtering, doublets, normalization, clustering, differential expression, annotation,
  and the lab's spatial stack, SpatialFeatureExperiment + Voyager. Use when processing or analysing
  scRNA-seq or spatial data in Seurat, Scanpy or Bioconductor.
---

# Single-cell and spatial analysis

Standard workflows apply. This skill records where the lab has a firm preference or departs from
common defaults, with the reason for each. The scientific standards (replication across donors,
confounder checks, the evidence rubric) are in the `analysis-conventions` skill; figures follow the
lab design system in the Branding repo.

## Working style

- **Look before thresholding.** Plot per-sample histograms of counts, genes and mitochondrial
  fraction (histograms show cut-off points better than violins), propose thresholds from what they
  show, and confirm them with the user before filtering. A threshold from another dataset or a
  tutorial is a starting point at most.
- **Filter lightly first.** Over-filtering removes real biology. Start permissive, check downstream
  results, and tighten only when they show a problem. Record every threshold in the analysis log.
- **Readable scripts.** Top-to-bottom scripts that run interactively in RStudio or Jupyter, with
  enough comments that a labmate can see why each step is there. Prefer clarity over cleverness.

## scRNA-seq

- **Ambient RNA:** remove it with SoupX, using the raw and filtered matrices, before QC.
- **Doublets:** detect them explicitly with scDblFinder in R or `sc.pp.scrublet` in Scanpy
  (`sc.external.pp.scrublet` is deprecated). Run per sample or capture (`samples =` /
  `batch_key =`), since doublets only form within a capture.
  - **Don't cut on high nCount or nFeature to remove doublets.** Those cut-offs aren't specific for
    doublets, and they remove large and transcriptionally active cells.
  - If Scrublet's automatic threshold flags far fewer doublets than the expected rate for the
    loading, set the threshold from the score distribution and note it.
- **Filtering:** remove cells by mitochondrial fraction, with the threshold read from the data (often
  10–25%, depending on tissue), and by doublet call. A low-end gene or count filter to remove empty
  droplets is fine.
- **Normalization:** keep two versions.
  - SCTransform v2 (glmGamPoi) for PCA, neighbours, clustering, UMAP and integration. It is the
    default in Seurat v5.
  - Log-normalized RNA for feature plots, dot plots and differential expression.

  In Scanpy, use `normalize_total` with `log1p`, and pick highly variable genes on raw counts
  (`flavor = "seurat_v3"`).
- **Clustering:** start at a low resolution (0.2–0.3) and raise it only when the question needs finer
  groups. Higher resolutions add clusters driven by sample or technical effects, and each cluster
  costs time to characterize. Compare a few resolutions and choose by biology.
- **Differential expression between conditions:** aggregate counts per donor (pseudobulk). Cells from
  one donor aren't independent replicates. Finding markers between clusters within a dataset can be
  per cell.
- **Annotation:** start from markers on dot plots and feature plots (log-normalized RNA). Use
  reference-based methods (SingleR, CellTypist, CellAssign) as support, not as the final word. Record
  the evidence for each label.
- **Colours:** cell types use the lab cell-type palette (`lab_celltypes` in the Branding repo's
  `tokens/palettes.R`). Show expression on embeddings with grey for zero.

## Spatial

### Stack
Use **SpatialFeatureExperiment (SFE) and Voyager** in R. SFE keeps cell centroids and segmentation
polygons (cell and nucleus) as `sf` geometries alongside the counts, and Voyager provides plotting and
spatial statistics on them. Using one stack across projects lets objects and code move between them.
If a project needs Python, ask before switching.

### Loading
```r
library(SpatialFeatureExperiment); library(Voyager)
sfe <- readXenium(xenium_dir, sample_id = "S01", row.names = "symbol")  # gene symbols, not Ensembl IDs
table(rowData(sfe)$Type)                                                # feature types in the panel
sfe <- sfe[rowData(sfe)$Type == "Gene Expression", ]                    # drop control probes and codewords
```
Readers for other platforms: `read10xVisiumSFE()`, `readVisiumHD()`, `readCosMX()`, `readVizgen()`.

### QC
- Remove cells with few transcripts. Start around 10 and check the distribution. Remove very small
  segmented objects too, either with `min_area` in `readXenium()` or by filtering on `cell_area`.
- **Remove isolated debris:** segmented objects that sit away from the tissue. Use nearest-neighbour
  distances between centroids, and plot the section before and after to check what was removed.
  ```r
  d <- BiocNeighbors::findKNN(spatialCoords(sfe), k = 5)$distance       # µm on Xenium
  sfe <- sfe[, d[, 1] <= 60 & d[, 5] <= 100]                            # nearest within 60, 5th within 100
  ```

### Normalization
Normalize by **cell area, not library size**: `logNormCounts(sfe, size.factors = sfe$cell_area)`.
Larger cells capture more transcripts. On a targeted panel, library size also varies with cell type,
so dividing by it removes real differences between types.

### Plotting
- **Whole sections:** plot centroids as points, rasterized with ggrastr, or binned with
  `plotCellBin2D()` for very large sections. Keep the aspect ratio fixed (`coord_fixed()`) and add a
  scale bar.
- **Regions:** draw segmentation polygons with `plotSpatialFeature(sfe, features,
  colGeometryName = "cellSeg", bbox = ...)`.
- **Colours:** use reversed scico `lapaz` or the lab maps for expression on tissue, and the
  cell-type palette for cell types.

### Spatial statistics
Build a neighbour graph, then run Voyager's statistics on it:
```r
colGraph(sfe, "knn") <- findSpatialNeighbors(sfe, method = "knearneigh", k = 5)
sfe <- runUnivariate(sfe, type = "moran", features = genes, colGraphName = "knn")       # global Moran's I
sfe <- runUnivariate(sfe, type = "localmoran", features = genes, colGraphName = "knn")  # local; plotLocalResult()
```
Other statistics in `listSFEMethods("uni")` and `listSFEMethods("uni", "local")`: Geary's C,
Getis-Ord G, LOSH, correlograms and variograms. Treat the section as the unit of analysis. Compute
statistics per section and compare them across donors, rather than pooling cells from several
sections.

### Transferring labels from scRNA-seq
Use SingleR with the annotated scRNA-seq as the reference, restricted to the genes on the panel.
Treat cells with low `delta.next` as ambiguous rather than forcing a label onto them, and check the
transferred labels against marker expression on the tissue.

## Environment
Python work uses the lab `scverse` mamba environment. R uses the system install with per-project
`renv`. Setup is in the `analysis-conventions` skill.
