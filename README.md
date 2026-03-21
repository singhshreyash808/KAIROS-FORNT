# SatFusion: Multi-satellite data fusion MVP

## Quick start
1. python -m venv .venv && source .venv/bin/activate  # or use Windows venv activation
2. pip install -r requirements.txt
3. cd backend && python app.py
4. Open http://localhost:5000

## What this MVP does
- Mock ingestion for Sentinel/Landsat/ISRO sources
- Preprocessing: cloud mask, simple corrections, resampling
- Fusion: pixel, feature (NDVI-like), decision (majority vote)
- Analytics: land cover stats, change detection, yield proxy
- Interactive map via Leaflet to visualize fused output
- Auth + subscription tiers + usage quotas (free/pro/enterprise)

## Next steps
- Replace mock ingestion with real APIs (Sentinel Hub, USGS, ISRO NRSC)
- Add proper georeferencing and raster alignment (GDAL/rasterio)
- Train real classifiers (scikit-learn or PyTorch)
- Persist data (Postgres + object storage)
- Add billing integration (Stripe) and role-based access
