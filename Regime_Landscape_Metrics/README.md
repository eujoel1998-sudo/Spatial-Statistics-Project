# Regime Landscape Metrics Analysis

Class-level FRAGSTATS landscape metrics (Patch Density, Edge Density, Aggregation Index, Cohesion, Largest Patch Index, Shannon Diversity) computed directly from classified/predicted land-use rasters, 2000–2035, averaged by the same 5 city-sector regimes (Core/North/East/South/West City) used in `../MGWR_SDM_Regime_Analysis/` and `../GWR_Overall_Analysis/` — plus a formal structural-plausibility check on the CA-CNN-LSTM model's own forecasts.

**Live page:** see this folder's `index.html`, or the main repo `index.html` for a shorter summary + link.
**Interactive map:** `webmap/regime_metrics_monitor.html` — 5 regime zones, switchable across 6 metrics × 8 years (2000–2035), with dashed-outline flagging where a regime/metric's predicted rate falls outside its own historical envelope.

## Structure

```
index.html   Narrative page: fragmentation trend charts (PD, ED), structural
             plausibility heatmap, and methodology
webmap/
  regime_metrics_monitor.html   Interactive Leaflet monitor: 5 regimes x 6 metrics
                                x 8 years, with plausibility-flag overlay for 2030/2035
```

## Source data

- Source: `Working_docs/Thesis/R_Studio/` — `landscape_metrics_analysis.Rmd` (raster → per-zone FRAGSTATS metrics), `regime_trend_analysis.Rmd` (zone → regime aggregation + trend slopes), `Regime_Landscape_Metrics.ipynb` (regime-level LPI correction + structural plausibility matrix, marked "Chapter 5 input")
- Rasters: `Aligned_Landuse_{2000,2005,2010,2015,2020,2025,2030,2035}.tif` — 2000–2020 observed/classified, 2025–2035 CA-CNN-LSTM predicted
- Zones: `Metrics.shp` (same 1,493-cell grid as the companion regime studies)
- Output CSVs used here: `output/Regime_Landscape_Metrics_AllYears.csv`, `output/Structural_Plausibility_Matrix.csv`

## Note

This is active thesis chapter material (the source notebook is explicitly titled "Chapter 5 input"), not a superseded/precursor analysis like some of this repo's other subprojects — flagging that distinction here since it differs from e.g. `MGWR_SDM_Regime_Analysis`, which documents an approach since revised for the thesis itself.
