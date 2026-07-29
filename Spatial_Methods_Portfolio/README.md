# Spatial Methods Portfolio

A showcase of core spatial-statistics methods, each demonstrated on an
independent case-study dataset. General-purpose/portfolio piece — not tied
to a single research question.

Files here are **copies** consolidated from
`Working_docs/Practise/Spatial_Data_Analysis/`; originals were left untouched.

## Structure

```
data/raw/
  sri_lanka/     Population_data.shp, Nuwara_Data.shp (GND-level population, 2001 vs 2011)
  uk_brexit/     brexit_vote.csv, local_authority_districts.geojson
  japan_tokyo/   tokyo_clean.csv (10,000 geotagged Flickr photo points)
  us_counties/   uscountypcincome.gpkg (per-capita income by county, 1969-2017)

notebooks/
  01_choropleth_classification.ipynb
      mapclassify toolkit comparison (EqualInterval, Quantiles, StdMean,
      MaximumBreaks, BoxPlot, HeadTailBreaks, JenksCaspall, FisherJenks,
      MaxP) on Sri Lanka population data, fit compared via ADCM.
  02_spatial_autocorrelation_brexit.ipynb
      Canonical Moran's I / LISA workflow: KNN weights, spatial lag,
      global + local Moran's I, cluster/significance maps on UK Brexit
      vote share by local authority.
  03_point_pattern_density_tokyo.ipynb
      KDE, hexbin density, centrography (mean/median center, standard
      deviational ellipse), alpha-shapes, complete spatial randomness
      testing (Ripley's G, quadrat chi-square) on Tokyo Flickr points.
  04_inequality_spatial_stats_us.ipynb
      Gini index, Lorenz curves, Theil decomposition (between/within
      region), Queen contiguity weights, global Moran's I per year, and
      spatially-weighted Gini on US county per-capita income.

outputs/figures/   PNG outputs already produced by the notebooks above.

webmap/
  brexit_map.py       Interactive % Leave choropleth + LISA cluster layer (folium).
  brexit_map.html     Generated output.
  tokyo_map.py        Interactive density heatmap + clustered points (folium).
  tokyo_map.html      Generated output.
  sri_lanka_map.py     Interactive population-density choropleth with a
                        toggle between classification schemes (Quantiles,
                        Equal Interval, Fisher-Jenks, Head/Tail Breaks).
  sri_lanka_map.html   Generated output.
  (no US counties web map — inequality/Gini analysis in notebook 04 doesn't
   have a natural single-map representation; static plots in that notebook
   remain the primary output for that case study)
```

Re-run any `*_map.py` script directly to regenerate its `.html` after data changes.

## Known cleanup needed

- Each notebook currently prints `os.listdir()` of the whole original
  folder (leftover from exploration) — safe to remove now that data is
  organized into per-theme subfolders.
- `01_choropleth_classification.ipynb` contains unused leftover code
  referencing a `Pooled`/PCGDP classifier from a course template — not
  applicable to the Sri Lanka data present; remove or replace.
- Consider a shared `utils.py` for the repeated KNN-weights /
  Moran's-I / LISA-cluster-map boilerplate duplicated across notebooks
  01/02/04.

## Not migrated

`DSd.shp` and `Kandy_data.shp` (present in the original folder but never
loaded by any notebook — orphan files); `chart.png`/`output.pdf` (a
throwaway FPDF example unrelated to the spatial analysis).
