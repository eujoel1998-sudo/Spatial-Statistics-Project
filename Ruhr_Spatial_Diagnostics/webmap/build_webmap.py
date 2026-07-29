"""
Builds an interactive web map of Local Moran's I (LISA) clusters for the
Dortmund/Ruhr synthetic grid (LST_2020), overlaid on the real RVR boundary.

Reproduces the analysis in notebooks/01_dortmund_grid_autocorrelation.ipynb
(KNN k=8 weights, esda Moran_Local) as a standalone, reproducible script
and exports it as folium layers instead of static matplotlib subplots.

Input:  ../data/raw/Testing.shp, ../data/raw/Values.csv, ../data/raw/RVR_Kreise.shp
Output: ruhr_lisa_cluster_map.html (this folder)
"""

from pathlib import Path

import esda
import geopandas as gpd
import pandas as pd
from libpysal import weights

HERE = Path(__file__).parent
DATA = HERE.parent / "data" / "raw"
OUT = HERE / "ruhr_lisa_cluster_map.html"

# RVR_Kreise.shp's .prj mislabels the CRS as WGS84 degrees; the coordinates
# are actually Web Mercator (EPSG:3857) meters.
RVR_ACTUAL_CRS = "EPSG:3857"

QUADRANT_LABELS = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
QUADRANT_COLORS = {
    "High-High": "#d7191c",
    "Low-Low": "#2c7bb6",
    "Low-High": "#abd9e9",
    "High-Low": "#fdae61",
    "Not significant": "#e8e8e8",
}


def load_grid() -> gpd.GeoDataFrame:
    grid = gpd.read_file(DATA / "Testing.shp")
    values = pd.read_csv(DATA / "Values.csv")
    grid = grid.merge(values, on="OBJECTID")
    return grid


def load_rvr_boundary() -> gpd.GeoDataFrame:
    rvr = gpd.read_file(DATA / "RVR_Kreise.shp")
    rvr = rvr.set_crs(RVR_ACTUAL_CRS, allow_override=True).to_crs("EPSG:4326")
    return rvr


def compute_lisa(grid: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    w = weights.KNN.from_dataframe(grid, k=8)
    w.transform = "R"

    lisa = esda.moran.Moran_Local(grid["LST_2020"], w)

    grid = grid.copy()
    grid["lisa_Is"] = lisa.Is
    grid["lisa_p"] = lisa.p_sim
    grid["quadrant"] = [QUADRANT_LABELS[q] for q in lisa.q]
    grid.loc[grid["lisa_p"] >= 0.05, "quadrant"] = "Not significant"
    return grid


def build_map(grid: gpd.GeoDataFrame, rvr: gpd.GeoDataFrame) -> "folium.Map":
    import folium

    bounds = grid.total_bounds  # minx, miny, maxx, maxy
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron")

    folium.GeoJson(
        rvr,
        name="RVR boundary",
        style_function=lambda _: {
            "fillOpacity": 0,
            "color": "#333333",
            "weight": 2,
        },
    ).add_to(m)

    folium.Choropleth(
        geo_data=grid.__geo_interface__,
        data=grid,
        columns=["OBJECTID", "LST_2020"],
        key_on="feature.properties.OBJECTID",
        fill_color="YlOrRd",
        fill_opacity=0.75,
        line_opacity=0.2,
        legend_name="Land Surface Temperature 2020",
        name="LST 2020 (choropleth)",
    ).add_to(m)

    lisa_layer = folium.FeatureGroup(name="LISA clusters (LST 2020)")
    folium.GeoJson(
        grid,
        style_function=lambda feat: {
            "fillColor": QUADRANT_COLORS[feat["properties"]["quadrant"]],
            "color": "white",
            "weight": 0.3,
            "fillOpacity": 0.8,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["OBJECTID", "LST_2020", "quadrant", "lisa_p"],
            aliases=["Cell ID", "LST 2020", "LISA cluster", "p-value"],
        ),
    ).add_to(lisa_layer)
    lisa_layer.add_to(m)

    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 10px 14px; border: 1px solid #999;
                border-radius: 4px; font-size: 13px;">
      <b>LISA cluster type</b><br>
      {rows}
    </div>
    """.format(
        rows="<br>".join(
            f'<span style="display:inline-block;width:12px;height:12px;'
            f'background:{color};margin-right:6px;"></span>{label}'
            for label, color in QUADRANT_COLORS.items()
        )
    )
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def main() -> None:
    grid = load_grid()
    grid = compute_lisa(grid)
    rvr = load_rvr_boundary()
    m = build_map(grid, rvr)
    m.save(str(OUT))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
