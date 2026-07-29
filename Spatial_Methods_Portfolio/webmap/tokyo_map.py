"""
Builds an interactive point-density web map of geotagged Flickr photos in
Tokyo, complementing the static KDE/hexbin plots in
notebooks/03_point_pattern_density_tokyo.ipynb.

Input:  ../data/raw/japan_tokyo/tokyo_clean.csv
Output: tokyo_map.html (this folder)
"""

from pathlib import Path

import folium
import pandas as pd
from folium.plugins import FastMarkerCluster, HeatMap

HERE = Path(__file__).parent
DATA = HERE.parent / "data" / "raw" / "japan_tokyo" / "tokyo_clean.csv"
OUT = HERE / "tokyo_map.html"


def load_points() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    return df.dropna(subset=["latitude", "longitude"])


def build_map(df: pd.DataFrame) -> folium.Map:
    center = [df["latitude"].mean(), df["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=11, tiles="CartoDB dark_matter")

    heat_layer = folium.FeatureGroup(name="Density heatmap")
    HeatMap(
        df[["latitude", "longitude"]].values.tolist(),
        radius=8,
        blur=10,
        max_zoom=13,
    ).add_to(heat_layer)
    heat_layer.add_to(m)

    cluster_layer = folium.FeatureGroup(name="Individual photo points (clustered)")
    FastMarkerCluster(df[["latitude", "longitude"]].values.tolist()).add_to(cluster_layer)
    cluster_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def main() -> None:
    df = load_points()
    m = build_map(df)
    m.save(str(OUT))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
