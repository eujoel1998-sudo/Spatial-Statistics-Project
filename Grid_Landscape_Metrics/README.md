# Grid Landscape Metrics

The same landscape-fragmentation metrics as `../Regime_Landscape_Metrics/`, shown at native **1,493-cell grid resolution** instead of averaged up to the 5 city-sector regimes — so within-district variation a regime mean would hide is visible directly, cell by cell, 2000–2035.

**Live page:** see this folder's `index.html`, or the main repo `index.html` for a shorter summary + link.
**Interactive map:** `webmap/grid_metrics_monitor.html` — all 1,493 cells, switchable across 5 metrics × 8 years, hover any cell for all 5 metrics at once.

## Structure

```
index.html   Narrative page: why grid resolution matters, citywide trend chart,
             boundary-sliver-outlier caveat
webmap/
  grid_metrics_monitor.html   Interactive Leaflet monitor: 1,493 cells x 5 metrics
                              x 8 years, quantile-classed (outlier-robust) legend
```

## Source data

- Grid: `Working_docs/Thesis/R_Studio/Metrics.shp` (same 1,493-cell grid as the companion regime studies)
- Grid-cell metric values: `C:\Users\eujoe\Documents\LULC\Context\Output\Grid_Landscape_Metrics_Summary.csv` (SHDI), `Grid_CA_CNN_LSTM_Fragmentation_Summary.csv` (Built-up_pd, Built-up_ai, Veg_cohesion), `Grid_Edge_Metrics_Summary.csv` (ed) — the same long-format grid CSVs read by `Regime_Landscape_Metrics.ipynb` before its regime-level area-weighted aggregation step

## Why LPI is excluded here

Largest Patch Index is scale-dependent (% of landscape held by the largest patch). Averaging or computing it at 500 m grid-cell scale washes out true regional dominance — the source notebook documented this producing a near-flat, uninformative series in its first pass. LPI is only shown at the full dissolved-regime scale, in `../Regime_Landscape_Metrics/`.

## Known data-quality note

A small number of grid cells (boundary slivers with very small area) show extreme Patch Density values (e.g. >2000 in one South City cell) — a modifiable-areal-unit-type artifact of computing a density metric on a tiny denominator, not a real fragmentation signal. The webmap's quantile-based color classing is robust to these outliers; exact values are still shown on hover rather than clipped or hidden.

## Note

Same source as `../Regime_Landscape_Metrics/` — active thesis chapter material (Chapter 5 input), not a superseded/precursor analysis.
