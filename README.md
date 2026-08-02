# Spatial Statistics Project

**Live site:** https://eujoel1998-sudo.github.io/Spatial-Statistics-Project/

Four projects built from spatial-statistics notebooks, split by purpose.

## Subprojects

- **[Ruhr_Spatial_Diagnostics](Ruhr_Spatial_Diagnostics/)** — applied
  spatial-autocorrelation diagnostics for the Ruhr region (Germany), feeding
  directly into the author's Dortmund LULC/spatial-econometrics thesis work.

- **[Spatial_Methods_Portfolio](Spatial_Methods_Portfolio/)** — a general
  spatial-statistics methods showcase (choropleth classification, Moran's
  I/LISA, point-pattern/density analysis, inequality statistics), each
  demonstrated on an independent case-study dataset (Sri Lanka, UK, Japan,
  US). Portfolio/CV-oriented, not tied to a specific research question.

- **[MGWR_SDM_Regime_Analysis](MGWR_SDM_Regime_Analysis/)** — Multiscale GWR
  and a five-city-sector Spatial Durbin Model applied to the same 1,493-cell
  Dortmund landscape-metrics grid (Built-up PD, Vegetation Cohesion,
  Vegetation PD × 2015/2025/2035), testing whether landscape-metric drivers
  are spatially stationary or structurally different by city sector.
  Includes an interactive regime-zone webmap.

- **[GWR_Overall_Analysis](GWR_Overall_Analysis/)** — single-scale adaptive
  GWR fit independently per year (2015/2025/2035) on the same grid, then
  differenced over time to map how local coefficients themselves shift as
  the city develops. Companion to MGWR_SDM_Regime_Analysis's spatial
  question, asking a temporal one instead.

Each subfolder has its own README with data provenance, structure, and
known follow-up items.
