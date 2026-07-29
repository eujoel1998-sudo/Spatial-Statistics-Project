"""
Builds an interactive choropleth + LISA cluster web map of the UK Brexit
referendum vote share by local authority district.

Reproduces the analysis in notebooks/02_spatial_autocorrelation_brexit.ipynb
(KNN k=8 weights, esda Moran_Local on Pct_Leave) as folium layers.

Input:  ../data/raw/uk_brexit/brexit_vote.csv,
        ../data/raw/uk_brexit/local_authority_districts.geojson
Output: brexit_map.html (this folder)
"""

from pathlib import Path

import esda
import folium
import geopandas as gpd
import pandas as pd
from libpysal import weights

HERE = Path(__file__).parent
DATA = HERE.parent / "data" / "raw" / "uk_brexit"
OUT = HERE / "brexit_map.html"

QUADRANT_LABELS = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
QUADRANT_COLORS = {
    "High-High": "#d7191c",
    "Low-Low": "#2c7bb6",
    "Low-High": "#abd9e9",
    "High-Low": "#fdae61",
    "Not significant": "#e8e8e8",
}


def load_data() -> gpd.GeoDataFrame:
    ref = pd.read_csv(DATA / "brexit_vote.csv")
    lads = gpd.read_file(DATA / "local_authority_districts.geojson")

    db = lads.merge(
        ref[["Area_Code", "Area", "Pct_Leave"]],
        left_on="lad16cd",
        right_on="Area_Code",
        how="inner",
    ).dropna(subset=["Pct_Leave"])
    return db[["lad16cd", "Area", "Pct_Leave", "geometry"]]


def compute_lisa(db: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    db_proj = db.to_crs(epsg=3857)
    w = weights.distance.KNN.from_dataframe(db_proj, k=8)
    w.transform = "R"

    lisa = esda.moran.Moran_Local(db["Pct_Leave"], w)

    db = db.copy()
    db["lisa_p"] = lisa.p_sim
    db["quadrant"] = [QUADRANT_LABELS[q] for q in lisa.q]
    db.loc[db["lisa_p"] >= 0.05, "quadrant"] = "Not significant"
    return db


def build_map(db: gpd.GeoDataFrame) -> folium.Map:
    bounds = db.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, zoom_start=6, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=db.__geo_interface__,
        data=db,
        columns=["lad16cd", "Pct_Leave"],
        key_on="feature.properties.lad16cd",
        fill_color="RdBu_r",
        fill_opacity=0.75,
        line_opacity=0.2,
        legend_name="% Leave vote",
        name="% Leave (choropleth)",
    ).add_to(m)

    lisa_layer = folium.FeatureGroup(name="LISA clusters (% Leave)")
    folium.GeoJson(
        db,
        style_function=lambda feat: {
            "fillColor": QUADRANT_COLORS[feat["properties"]["quadrant"]],
            "color": "white",
            "weight": 0.3,
            "fillOpacity": 0.8,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Area", "Pct_Leave", "quadrant", "lisa_p"],
            aliases=["Local authority", "% Leave", "LISA cluster", "p-value"],
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
    db = load_data()
    db = compute_lisa(db)
    m = build_map(db)
    m.save(str(OUT))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
