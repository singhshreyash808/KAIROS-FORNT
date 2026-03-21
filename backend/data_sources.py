import random
from datetime import datetime

# Mock ingestion: replace with real APIs (Sentinel Hub, USGS, ISRO Bhuvan/NRSC)
def fetch_dataset(source, aoi, date_range):
    # Simulate a raster/multispectral dataset metadata + small pixel grid
    bands = {
        "sentinel": ["B02","B03","B04","B08"],       # Blue, Green, Red, NIR
        "landsat": ["B2","B3","B4","B5"],            # Blue, Green, Red, NIR
        "isro": ["Red","Green","Blue","SWIR"]        # Example ISRO mission bands
    }
    grid = [[random.randint(0, 255) for _ in range(8)] for _ in range(8)]
    return {
        "source": source,
        "timestamp": datetime.utcnow().isoformat(),
        "aoi": aoi or {"bbox": [77.4, 28.6, 77.6, 28.8]},  # Ghaziabad sample bbox
        "bands": bands.get(source, []),
        "pixels": grid,
        "resolution": "10m" if source == "sentinel" else "30m"
    }