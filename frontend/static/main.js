let TOKEN = null;
let INGESTED = [];
let PREPROCESSED = [];
let FUSED = null;
let MAP = null;
let LAYER = null;

function setToken(t) { TOKEN = t; localStorage.setItem("token", t); }
function getToken() { return TOKEN || localStorage.getItem("token"); }

async function api(path, method="GET", body=null) {
  const headers = {"Content-Type": "application/json"};
  const token = getToken();
  if (token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(path, { method, headers, body: body ? JSON.stringify(body) : null });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || ("HTTP " + res.status));
  }
  return res.json();
}
document.addEventListener("DOMContentLoaded", () => {
  const signup = document.getElementById("signup-form");
  const login = document.getElementById("login-form");
  const openBtn = document.getElementById("open-dashboard");

  if (signup) signup.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(signup).entries());
    const res = await api("/api/signup", "POST", data);
    setToken(res.token);
    alert("Signed up. Token saved.");
  });

  if (login) login.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(login).entries());
    const res = await api("/api/login", "POST", data);
    setToken(res.token);
    alert("Logged in. Token saved.");
  });

  if (openBtn) openBtn.addEventListener("click", () => {
    window.location.href = "/dashboard";
  });

  // Dashboard logic
  const btnIngest = document.getElementById("btn-ingest");
  const btnPre = document.getElementById("btn-preprocess");
  const btnFuse = document.getElementById("btn-fuse");
  const btnAnal = document.getElementById("btn-analytics");
  const btnLayer = document.getElementById("btn-load-layer");
  const out = document.getElementById("analytics-output");

  if (btnIngest) btnIngest.addEventListener("click", async () => {
    const sources = [];
    if (document.getElementById("src-sentinel").checked) sources.push("sentinel");
    if (document.getElementById("src-landsat").checked) sources.push("landsat");
    if (document.getElementById("src-isro").checked) sources.push("isro");
    const res = await api("/api/ingest", "POST", { sources });
    INGESTED = res.datasets;
    alert("Ingested " + INGESTED.length + " datasets.");
  });

  if (btnPre) btnPre.addEventListener("click", async () => {
    const options = {
      cloud_mask: document.getElementById("opt-cloud").checked,
      atmospheric_correction: document.getElementById("opt-atmo").checked,
      resample_to: document.getElementById("opt-res").value
    };
    const res = await api("/api/preprocess", "POST", { datasets: INGESTED, options });
    PREPROCESSED = res.datasets;
    alert("Preprocessed " + PREPROCESSED.length + " datasets.");
  });

  if (btnFuse) btnFuse.addEventListener("click", async () => {
    const mode = document.getElementById("fusion-mode").value;
    const res = await api("/api/fuse", "POST", { datasets: PREPROCESSED.length ? PREPROCESSED : INGESTED, mode });
    FUSED = res.fused;
    alert("Fusion complete: " + FUSED.mode);
  });

  if (btnAnal) btnAnal.addEventListener("click", async () => {
    if (!FUSED) { alert("Run fusion first."); return; }
    const tasks = [];
    if (document.getElementById("task-land").checked) tasks.push("land_cover");
    if (document.getElementById("task-change").checked) tasks.push("change_detection");
    if (document.getElementById("task-yield").checked) tasks.push("yield_prediction");
    const res = await api("/api/analytics", "POST", { fused: FUSED, tasks });
    out.textContent = JSON.stringify(res.results, null, 2);
  });
if (btnLayer) btnLayer.addEventListener("click", async () => {
    if (!MAP) {
      MAP = L.map('map').setView([28.70, 77.50], 12);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(MAP);
    }
    const geojson = await api("/api/fused/geojson", "GET");
    if (LAYER) { MAP.removeLayer(LAYER); }
    LAYER = L.geoJSON(geojson, {
      pointToLayer: (f, latlng) => L.circleMarker(latlng, {
        radius: 4,
        color: "#0b3d91",
        fillColor: "#0b3d91",
        fillOpacity: Math.min(1.0, (f.properties.value || 50)/255)
      })
    }).addTo(MAP);
  });
});

