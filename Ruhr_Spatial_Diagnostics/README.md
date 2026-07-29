# Ruhr Spatial Diagnostics

Applied spatial-autocorrelation diagnostics for the Ruhr region (Germany),
intended as a companion/precursor analysis to the author's Dortmund
LULC/spatial-econometrics thesis.

Files here are **copies** consolidated from
`Working_docs/Practise/Spatial_Data_Analysis/`; originals were left untouched.

## Structure

```
data/raw/
  RVR_Kreise.*      Regionalverband Ruhr (RVR) district boundary shapefile (static)
  Testing.*         Synthetic 810-cell grid over Dortmund/Ruhr coordinates
  Values.csv        LST/NDVI-style values for the synthetic grid

notebooks/
  01_dortmund_grid_autocorrelation.ipynb
      KNN spatial weights, spatial lag, global Moran's I (I=0.559, p=0.001),
      Moran scatterplot, Local Moran's I (LISA), HH/LL/HL/LH cluster maps,
      significance maps — run on the synthetic Dortmund/Ruhr grid.
      NOTE: variable names/axis titles are inherited from a UK Brexit
      tutorial template ("% Leave" etc.) despite the Dortmund geometry —
      relabel before reuse.
  02_ruhr_boundary_fetch.ipynb
      Attempted live fetch of RVR district boundaries from an ArcGIS
      FeatureServer REST endpoint, to save as RVR_layer.geojson.
      CURRENTLY FAILS with HTTP 400 — the query parameters need fixing
      (check field names/output format against the FeatureServer's
      metadata endpoint) or fall back to the static RVR_Kreise.shp.
```

## Next steps to make this a real diagnostic

1. Fix `02_ruhr_boundary_fetch.ipynb`'s FeatureServer query (or just load
   `RVR_Kreise.shp` directly) to get real Ruhr Kreise-level geometry.
2. Replace the synthetic `Testing.shp`/`Values.csv` grid in
   `01_dortmund_grid_autocorrelation.ipynb` with real Kreise-level thesis
   variables (e.g. LULC change, population, built-up density) and relabel
   the Brexit-inherited variable names.
3. Re-run global/local Moran's I and LISA cluster maps on the real data to
   produce publishable spatial-autocorrelation diagnostics for the thesis.
