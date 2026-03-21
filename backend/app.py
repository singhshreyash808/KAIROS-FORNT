from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from auth import require_auth, login, signup
from data_sources import fetch_dataset
from preprocessing import preprocess_dataset
from fusion import fuse_datasets
from analytics import run_analytics
from billing import check_quota, record_usage
from storage import Storage

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
CORS(app)
store = Storage()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
@require_auth
def dashboard(user=None):
    return render_template("dashboard.html", user=user)

# Auth endpoints

@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.json or {}
    return signup(store, data)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    return login(store, data)

# Ingest endpoint
@app.route("/api/ingest", methods=["POST"])
@require_auth
def api_ingest(user=None):
    payload = request.json or {}
    sources = payload.get("sources", ["sentinel", "landsat", "isro"])
    aoi = payload.get("aoi")  # bbox or geojson
    date_range = payload.get("date_range")  # {"start": "...", "end": "..."}
    if not check_quota(store, user["id"], "ingest"):
        return jsonify({"error": "Quota exceeded"}), 402

    datasets = []
    for src in sources:
        ds = fetch_dataset(src, aoi, date_range)
        datasets.append(ds)

    record_usage(store, user["id"], "ingest")
    return jsonify({"status": "ok", "datasets": datasets})

# Preprocess endpoint
@app.route("/api/preprocess", methods=["POST"])
@require_auth
def api_preprocess(user=None):
    payload = request.json or {}
    datasets = payload.get("datasets", [])
    options = payload.get("options", {"cloud_mask": True, "atmospheric_correction": True, "resample_to": "10m"})
    if not check_quota(store, user["id"], "preprocess"):
        return jsonify({"error": "Quota exceeded"}), 402

    preprocessed = [preprocess_dataset(ds, options) for ds in datasets]
    record_usage(store, user["id"], "preprocess")
    return jsonify({"status": "ok", "datasets": preprocessed})

# Fusion endpoint
@app.route("/api/fuse", methods=["POST"])
@require_auth
def api_fuse(user=None):
    payload = request.json or {}
    datasets = payload.get("datasets", [])
    mode = payload.get("mode", "feature")  # "pixel" | "feature" | "decision"
    if not check_quota(store, user["id"], "fuse"):
        return jsonify({"error": "Quota exceeded"}), 402

    fused = fuse_datasets(datasets, mode)
    store.save_fused(user["id"], fused)
    record_usage(store, user["id"], "fuse")
    return jsonify({"status": "ok", "fused": fused})

# Analytics endpoint
@app.route("/api/analytics", methods=["POST"])
@require_auth
def api_analytics(user=None):
    payload = request.json or {}
    fused = payload.get("fused")
    tasks = payload.get("tasks", ["land_cover", "change_detection", "yield_prediction"])
    if not check_quota(store, user["id"], "analytics"):
        return jsonify({"error": "Quota exceeded"}), 402

    results = run_analytics(fused, tasks)
    record_usage(store, user["id"], "analytics")
    return jsonify({"status": "ok", "results": results})

# Fused map layer
@app.route("/api/fused/geojson", methods=["GET"])
@require_auth
def api_fused_geojson(user=None):
    geojson = store.get_fused_geojson(user["id"])
    return jsonify(geojson or {"type": "FeatureCollection", "features": []})

if __name__ == "__main__":
    app.run(debug=True)
