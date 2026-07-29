"""
Builds an interactive population-density choropleth web map for Jaffna
(Sri Lanka), with a toggle between classification schemes — the interactive
counterpart to the static mapclassify comparison in
notebooks/01_choropleth_classification.ipynb.

Input:  ../data/raw/sri_lanka/Population_data.shp
Output: sri_lanka_map.html (this folder)
"""

from pathlib import Path

import folium
import geopandas as gpd
import mapclassify
import numpy as np

HERE = Path(__file__).parent
DATA = HERE.parent / "data" / "raw" / "sri_lanka" / "Population_data.shp"
OUT = HERE / "sri_lanka_map.html"

VALUE_COL = "Density"
K = 5

SCHEMES = {
    "Quantiles": mapclassify.Quantiles,
    "Equal Interval": mapclassify.EqualInterval,
    "Fisher-Jenks": mapclassify.FisherJenks,
    "Head/Tail Breaks": lambda values: mapclassify.HeadTailBreaks(values),
}


def load_data() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(DATA)
    return gdf.dropna(subset=[VALUE_COL])


def bin_edges(values: np.ndarray, scheme_cls) -> list:
    try:
        classifier = scheme_cls(values, k=K)
    except TypeError:
        classifier = scheme_cls(values)
    edges = [float(values.min()) - 1.0] + [float(b) for b in classifier.bins]
    edges[-1] += 1.0  # guard against float rounding excluding the max value
    edges = sorted(set(edges))
    return edges


def build_map(gdf: gpd.GeoDataFrame) -> folium.Map:
    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, zoom_start=10, tiles="CartoDB positron")

    values = gdf[VALUE_COL].to_numpy()
    id_col = "OBJECTID"

    for name, scheme_cls in SCHEMES.items():
        edges = bin_edges(values, scheme_cls)
        folium.Choropleth(
            geo_data=gdf.__geo_interface__,
            data=gdf,
            columns=[id_col, VALUE_COL],
            key_on=f"feature.properties.{id_col}",
            fill_color="YlGnBu",
            fill_opacity=0.8,
            line_opacity=0.2,
            bins=edges,
            legend_name=f"Population density — {name}",
            name=f"Density ({name})",
            show=(name == "Quantiles"),
        ).add_to(m)

    tooltip_layer = folium.FeatureGroup(name="Labels (GND / district)")
    folium.GeoJson(
        gdf,
        style_function=lambda _: {"fillOpacity": 0, "color": "transparent"},
        tooltip=folium.GeoJsonTooltip(
            fields=["ADM3_EN", "ADM2_EN", "Population", VALUE_COL],
            aliases=["GND", "District", "Population", "Density"],
        ),
    ).add_to(tooltip_layer)
    tooltip_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def main() -> None:
    gdf = load_data()
    m = build_map(gdf)
    m.save(str(OUT))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
