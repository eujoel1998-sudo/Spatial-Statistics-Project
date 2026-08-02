# MGWR & Spatial Durbin Regime Analysis

Two spatial-regression approaches applied to the same 1,493-cell Dortmund landscape-metrics grid (Built-up Patch Density, Vegetation Cohesion, Vegetation Patch Density; 2015/2025/2035), testing whether landscape-metric drivers are spatially stationary or vary structurally across the city.

**Live page:** see the repo's main `index.html`, section "MGWR & Spatial Durbin Regime Analysis", or open `index.html` in this folder directly.
**Interactive map:** `webmap/regime_zones_map.html` — five city-sector regimes (Core/North/East/South/West City), click a sector for its regime-specific R² across all three metrics and years.

## Structure

```
index.html            Narrative page: MGWR global-vs-local R2 comparison, SDM regime fit,
                       direct/indirect effect decomposition, sign-flip examples across regimes
webmap/
  regime_zones_map.html   Leaflet map of the 5 city-sector regimes with per-zone R2 popups
```

## Source data & models

- Source shapefiles: `Metrics_Summary_{2015,2025,2035}.shp` (not included here — see the author's local `LULC/Context/Metrics/Shp_File/Output/` working copy)
- MGWR notebooks: `Working_docs/Metrics/MGWR/{Built_PD,Veg_Coh,Veg_PD}/{2015,2025,2035}.ipynb`
- SDM regime notebooks: `Working_docs/Metrics/Spatial Durbin Model (SDM)/SDM/{2015,2025,2035}/{Built_PD,Veg_Coh,Veg_PD}.ipynb`
- Regime definition (5 city sectors from 12 Stadtbezirke):
  - Core_City: INNENSTADT-NORD, INNENSTADT-WEST, INNENSTADT-OST
  - North_City: EVING, SCHARNHORST
  - East_City: BRACKEL, APLERBECK
  - West_City: MENGEDE, HUCKARDE, L
  - South_City: HOMBRUCH, H

## Note

This regime-SDM specification was an earlier chapter approach in the author's Dortmund LULC/spatial-econometrics thesis, later revised toward an instrumental-variables framework for the thesis itself (see `Working_docs/Instrumental _Variables/`). Kept here as a standalone spatial-statistics methods case study.
