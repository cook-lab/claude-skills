# scrna-spatial — Code Templates

Detailed code recipes for tasks referenced from the main SKILL.md.

---

## Reference-Based Annotation (SingleR)

Transfer annotations from scRNA-seq to spatial data:

```r
library(SingleR)

# Prepare reference (annotated scRNA-seq)
sce_ref <- as.SingleCellExperiment(seu, assay = "RNA")
ref_labels <- seu$cell_type

# Find common genes (limited by spatial panel)
common_genes <- intersect(rownames(sce_ref), rownames(sfe))

# Run SingleR
singler_results <- SingleR(
  test = sfe[common_genes, ],
  ref = sce_ref[common_genes, ],
  labels = ref_labels,
  de.method = "classic"
)

sfe$singler_label <- singler_results$labels
sfe$singler_delta <- singler_results$delta.next
```

**Check annotation quality:**
- Score heatmap: shows correlation with each cell type
- Delta distribution: higher = more confident (low delta = ambiguous)

---

## Data Export for Interoperability

### Seurat → Cell Ranger Format (for Scanpy)

```r
counts_matrix <- LayerData(seu, assay = "RNA", layer = "counts")

# Matrix
writeMM(counts_matrix, "matrix.mtx")
system("gzip -f matrix.mtx")

# Features
features_df <- data.frame(
  gene_id = rownames(seu),
  gene_name = rownames(seu),
  feature_type = "Gene Expression"
)
write.table(features_df, "features.tsv", sep = "\t",
            row.names = FALSE, col.names = FALSE, quote = FALSE)
system("gzip -f features.tsv")

# Barcodes
write.table(colnames(seu), "barcodes.tsv",
            row.names = FALSE, col.names = FALSE, quote = FALSE)
system("gzip -f barcodes.tsv")

# Metadata
write.csv(seu@meta.data, "cell_metadata.csv")
```

### Load in Scanpy

```python
adata = sc.read_10x_mtx("exported_data/")
metadata = pd.read_csv("exported_data/cell_metadata.csv", index_col=0)
adata.obs = metadata
```
