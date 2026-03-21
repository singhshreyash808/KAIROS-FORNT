def fuse_datasets(datasets, mode="feature"):
    if not datasets:
        return {"mode": mode, "pixels": [], "bands": [], "resolution": "10m"}

    if mode == "pixel":
        return _pixel_level(datasets)
    elif mode == "feature":
        return _feature_level(datasets)
    elif mode == "decision":
        return _decision_level(datasets)
    else:
        raise ValueError("Unknown fusion mode")

def _pixel_level(datasets):
    # Simple average across sources (aligned grids assumed for demo)
    grids = [ds["pixels"] for ds in datasets]
    rows = min(len(g) for g in grids)
    cols = min(len(g[0]) for g in grids)
    fused = []
    for i in range(rows):
        row = []
        for j in range(cols):
            vals = [g[i][j] for g in grids]
            row.append(sum(vals) // len(vals))
        fused.append(row)
    return {"mode": "pixel", "pixels": fused, "bands": ["FUSED_INTENSITY"], "resolution": "10m"}
def _feature_level(datasets):
    # Compute NDVI-like proxy from Red/NIR if present; else normalized intensity
    def ndvi(ds):
# Mock: use last and first value in a row to emulate NIR/Red
        grid = ds["pixels"]
        return [[(row[-1] - row[0]) / (row[-1] + row[0] + 1e-6) for row in grid]]

    features = []
    for ds in datasets:
        features.append(ndvi(ds))
# Average feature maps
    rows = len(features[0][0])
    cols = len(features[0][0][0])
    fused_feat = []
    for i in range(rows):
        row = []
        for j in range(cols):
            vals = [f[0][i][j] for f in features]
            row.append(sum(vals) / len(vals))
        fused_feat.append(row)
    return {"mode": "feature", "pixels": fused_feat, "bands": ["NDVI_FUSED"], "resolution": "10m"}

def _decision_level(datasets):
    # Run per-source classifier, then majority vote
    labels_per_source = []
    for ds in datasets:
        labels_per_source.append(_mock_classifier(ds["pixels"]))
    rows = len(labels_per_source[0])
    cols = len(labels_per_source[0][0])
    fused_labels = []
    for i in range(rows):
        row = []
        for j in range(cols):
            votes = [lbls[i][j] for lbls in labels_per_source]
            row.append(max(set(votes), key=votes.count))
        fused_labels.append(row)
    return {"mode": "decision", "pixels": fused_labels, "bands": ["CLASS"], "resolution": "10m"}

def _mock_classifier(grid):
    # 3-class mock based on intensity thresholds
    out = []
    for row in grid:
        out_row = []
        for v in row:
            if v < 60: out_row.append(0)      # water/bare
            elif v < 160: out_row.append(1)   # vegetation
            else: out_row.append(2)           # urban
        out.append(out_row)
    return out
