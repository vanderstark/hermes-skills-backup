# Offline-Capable Webapp Pattern

Techniques for making self-hosted web apps work **100% without internet** — critical for disaster response, military, and air-gapped environments.

## Core Problem

Modern web apps silently depend on CDN resources (JS/CSS frameworks, fonts, map tiles, icons). When internet dies — exactly when these apps are needed most — they break or degrade. The fix is systematic self-hosting + fallback architecture.

## 1. Self-Host All CDN Assets

**Rule**: Zero references to external CDNs in production HTML.

```bash
# Download Leaflet + marker images
curl -sL "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" -o assets/leaflet/leaflet.css
curl -sL "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" -o assets/leaflet/leaflet.js
curl -sL "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png" -o assets/leaflet/images/
curl -sL "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png" -o assets/leaflet/images/
curl -sL "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png" -o assets/leaflet/images/

# Download Font Awesome + webfonts
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" -o assets/fontawesome/css/all.min.css
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-solid-900.woff2" -o assets/fontawesome/webfonts/
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-solid-900.ttf" -o assets/fontawesome/webfonts/
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-regular-400.woff2" -o assets/fontawesome/webfonts/
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-regular-400.ttf" -o assets/fontawesome/webfonts/
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-brands-400.woff2" -o assets/fontawesome/webfonts/
curl -sL "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-brands-400.ttf" -o assets/fontawesome/webfonts/
```

**Pitfall**: FA webfonts directory MUST be sibling of css dir (structure: `assets/fontawesome/{css/all.min.css, webfonts/*.woff2}`).

**Verify zero CDN refs**: `curl localhost:8000/ | grep -c "unpkg\|cdnjs"` → **must return 0**.

## 2. Map Tile Caching for Offline

### Download Script Pattern
```python
import math, time, urllib.request
from pathlib import Path
AREAS = {"operational_area": [min_lon, min_lat, max_lon, max_lat]}
TILE_URL = "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
TILE_DIR = Path("assets/tiles")

def deg2num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.asinh(math.tan(lat_rad)) / math.pi) / 2 * n)
    return x, y
```

**Zoom guidance**: 3-6 (overview/~50 tiles), 7-9 (operational/~1K), 10-12 (tactical/~10K — skip if >5K/zoom), 13+ skip. Total ~50-60MB per area.

**Tile caching strategy for git repos**: tiles are too large for version control. `gitignore` them with:
```
# in .gitignore
frontend/assets/tiles/*
!frontend/assets/tiles/.gitkeep
```
Commit the download script (`download-tiles.py`) and the empty `assets/tiles/.gitkeep` placeholder — users download tiles locally when they have internet. This keeps repo sizes small (~30 code files vs 12K+ tile PNGs).

**Tile download script must handle timeout gracefully**: at zoom 10+, individual areas can generate 5K+ tiles and take 5+ minutes. Run as a background process (`terminal(background=True, notify_on_complete=True)`) and keep working on other files; verify count/size when done. If download is killed mid-way (timeout or manual), partial tiles still work — the auto-switch logic handles uncached tiles via `errorTileUrl`.

**Iteration fix — do NOT skip tile ranges by accident**: when using a loop like `for z in range(z_min, z_max+1)`, `for x in range(x_min, x_max+1)`, ensure both ranges are **inclusive** at the upper bound (`x_max+1`, not `x_max`). A bug where the loop ends at `x_max-1` silently downloads half the needed tiles and produces blank areas on the map. Validate after download: `find assets/tiles -name "*.png" | wc -l` should match the expected count (approximately `(x_max-x_min+1) * (y_max-y_min+1)` tiles per zoom level).

**Pitfall — deg2num formula**: `(max_lat, min_lon)`→`(x_min,y_min)`, `(min_lat,max_lon)`→`(x_max,y_max)`. Higher lat → lower y. Test with known coords first.

## 3. Online/Offline Auto-Switch

```javascript
const CDN = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const LOCAL = 'assets/tiles/{z}/{x}/{y}.png';
L.tileLayer(!navigator.onLine ? LOCAL : CDN, {
    errorTileUrl: 'assets/leaflet/images/marker-icon.png',
}).addTo(map);
window.addEventListener('online', () => map.eachLayer(l => l.setUrl(CDN)));
window.addEventListener('offline', () => map.eachLayer(l => l.setUrl(LOCAL)));
```

## 4. LAN Binding for Multi-Device Access

```yaml
# docker-compose.yml
ports:
  - "0.0.0.0:${APP_PORT:-8000}:8000"  # NOT "8000:8000"
```

## 5. Backend Zero External Dependencies

Backend must make ZERO external HTTP calls at runtime. All data bundled locally. Test: disconnect network, submit request — must succeed.

## Checklist
- [ ] CDN refs in HTML → 0
- [ ] JS/CSS/fonts served locally
- [ ] Map tiles cached for operational area
- [ ] Online/offline listener swaps layers
- [ ] Backend has zero external calls
- [ ] LAN binding for multi-device access
- [ ] Tested with actual disconnection
- [ ] errorTileUrl for graceful uncached tile handling