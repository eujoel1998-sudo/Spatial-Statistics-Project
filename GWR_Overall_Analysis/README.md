# GWR Overall Analysis

Single-scale adaptive Geographically Weighted Regression (GWR), fit independently for 2015, 2025, and 2035 on the same 1,493-cell Dortmund landscape-metrics grid used in `../MGWR_SDM_Regime_Analysis/`. Where that companion project asks whether relationships are spatially stationary, this one holds the spatial question fixed (single adaptive bandwidth per year) and asks a temporal one: does a covariate's local coefficient drift, in the same grid cell, as the city develops from 2015 to 2035?

**Live page:** see this folder's `index.html`, or the main repo `index.html` for a shorter summary + link.
**Interactive map:** `webmap/gwr_coefficient_explorer.html` — all 1,493 cells, switchable between local R² and per-cell coefficients for all three metrics (2015), refit directly from the source shapefiles (not a static export of the notebook figures).

## Structure

```
index.html   Narrative page: per-metric adaptive-bandwidth comparison, coefficient
             snapshot maps (2015/2025/2035), and year-over-year coefficient deltas
webmap/
  gwr_coefficient_explorer.html   Interactive Leaflet map of live-refit 2015 GWR
                                  results for all three metrics (local R2 + two
                                  highlighted coefficients each), dropdown-selectable
```

## Source data & models

- Source notebooks: `Working_docs/Metrics/GWR/Overall/{Built_PD copy,Veg_Coh,Veg_PD}.ipynb`
- Same source shapefiles as the MGWR/SDM project: `Metrics_Summary_{2015,2025,2035}.shp`
- GWR fit: `mgwr.gwr.GWR(coords, y, X, bw, kernel='bisquare').fit()`, bandwidth via `Sel_BW(..., fixed=False)` (adaptive)

## Adaptive bandwidth by metric (neighbours out of 1,493 cells)

| Metric | 2015 | 2025 | 2035 |
|---|---|---|---|
| Built-up PD | 205 | 205 | 145 |
| Vegetation Cohesion | 608 | 657 | 860 |
| Vegetation PD | 253 | 194 | 209 |

Vegetation Cohesion's much larger bandwidth (more neighbours = smoother, more global relationship) is consistent with its high global R² in the MGWR companion study — there's less local structure for a spatially-varying model to find.

## Known data-quality issue found during this write-up

On inspection, the **year-over-year coefficient-change grids** in `Veg_Coh.ipynb` and `Veg_PD.ipynb` (the cells plotting deltas for the shared landscape-index and agri/vegetation covariate groups) are **byte-identical** between the two notebooks, despite each notebook fitting GWR against a different dependent variable (`2035_Veg_Cohesion_std` vs. `2035_Veg_Pd_std` — confirmed correct in the model-fitting cells themselves). This points to a stale/cached output in one or both notebooks — likely `Veg_PD.ipynb` was created by copying `Veg_Coh.ipynb` and the plotting cells for the shared covariate groups were never re-executed against the new fit.

The independently-verified **per-year snapshot** coefficient maps (own-metric predictors, landscape-index predictors) were checked pairwise and differ genuinely between notebooks — those are what's shown in `index.html`. The suspect change-grid cells are excluded from the write-up until the source notebooks are re-run end-to-end.

**To fix:** re-run `Veg_Coh.ipynb` and `Veg_PD.ipynb` fully top-to-bottom (Restart & Run All) so every cell's output reflects that notebook's own `gwr_model_*` fit, then re-diff the two notebooks' change-grid cells to confirm they're no longer identical.
