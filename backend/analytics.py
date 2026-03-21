def run_analytics(fused, tasks):
    results = {}
    grid = fused.get("pixels", [])
    if "land_cover" in tasks:
        results["land_cover"] = _land_cover_stats(grid)
    if "change_detection" in tasks:
        results["change_detection"] = _change_detection(grid)
    if "yield_prediction" in tasks:
        results["yield_prediction"] = _yield_prediction(grid)
    return results

def _land_cover_stats(grid):
    # Count classes assuming decision-level fusion; otherwise intensity bins
    if not grid: return {}
    flat = sum(grid, [])
    classes = {}
    for v in flat:
        cls = v if isinstance(v, int) else (0 if v < 0.3 else (1 if v < 0.6 else 2))
        classes[cls] = classes.get(cls, 0) + 1
    total = len(flat)
    return {k: round(v/total, 3) for k, v in classes.items()}

def _change_detection(grid):
    # Mock change: compute gradient magnitude proxy
    if not grid: return {"change_index": 0.0}
    diffs = []
    for i in range(len(grid)-1):
        for j in range(len(grid[0])-1):
            diffs.append(abs(grid[i+1][j] - grid[i][j]) + abs(grid[i][j+1] - grid[i][j]))
    return {"change_index": round(sum(diffs)/len(diffs)/255.0, 3)}

def _yield_prediction(grid):
    # Naive yield proxy from mean fused NDVI/intensity
    if not grid: return {"yield_index": 0.0}
    mean_val = sum(sum(row) for row in grid) / (len(grid) * len(grid[0]))
    return {"yield_index": round(min(1.0, mean_val/255.0), 3)}
