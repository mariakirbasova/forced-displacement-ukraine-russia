import math
import re
import html

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="Telegram Corpus",
    layout="wide",
)

CITIES_FILE = BASE_DIR / "data" / "cities.csv"
TOPICS_FILE = BASE_DIR / "data" / "city_topics.csv"
CITY_PAGE = BASE_DIR / "pages" / "city_page.py"


@st.cache_data
def load_data():
    cities = pd.read_csv(CITIES_FILE)
    topics = pd.read_csv(TOPICS_FILE)

    cities.columns = cities.columns.str.strip()
    topics.columns = topics.columns.str.strip()

    cities["city"] = cities["city"].astype(str).str.strip()
    cities["city_id"] = cities["city_id"].astype(str).str.strip()
    cities["lat"] = pd.to_numeric(cities["lat"], errors="coerce")
    cities["lon"] = pd.to_numeric(cities["lon"], errors="coerce")
    cities["total"] = pd.to_numeric(cities["total"], errors="coerce").fillna(0).astype(int)

    topics["city_id"] = topics["city_id"].astype(str).str.strip()

    cities = cities.dropna(subset=["lat", "lon"]).copy()

    return cities, topics


def point_radius(total: int) -> float:
    return 6 + math.sqrt(max(total, 1)) * 3


def build_tooltip_html(city_row, city_topics):
    city_name = html.escape(str(city_row["city"]))
    city_id = html.escape(str(city_row["city_id"]))
    total = int(city_row["total"])

    if city_topics.empty or "thematique" not in city_topics.columns:
        topics_html = "No data"
    else:
        thematic_counts = (
            city_topics["thematique"]
            .fillna("Non renseigné")
            .astype(str)
            .str.strip()
            .replace("", "Non renseigné")
            .value_counts()
            .reset_index()
        )
        thematic_counts.columns = ["thematique", "count"]

        lines = [
            f"{html.escape(str(row['thematique']))}: <b>{int(row['count'])}</b>"
            for _, row in thematic_counts.iterrows()
        ]

        topics_html = "<br>".join(lines)

    return f"""
    <div style="font-size: 13px; line-height: 1.45; min-width: 290px;">
        <span style="display:none;">CITY_ID::{city_id}</span>
        <b>{city_name}</b><br>
        Espaces téléchargés: <b>{total}</b><br><br>
        {topics_html}
    </div>
    """


def extract_city_id(tooltip_value):
    if not tooltip_value:
        return None

    match = re.search(r"CITY_ID::([a-zA-Z0-9_\-]+)", tooltip_value)

    if match:
        return match.group(1)

    return None


cities_df, topics_df = load_data()

if "telegram_last_city_click" not in st.session_state:
    st.session_state["telegram_last_city_click"] = None

if "selected_city_id" not in st.session_state:
    st.session_state["selected_city_id"] = None


st.title("Telegram Corpus")

if st.button("← Back", use_container_width=False):
    st.switch_page("pages/home.py")

st.markdown(
    """
    <div style="
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background-color: rgba(255,255,255,0.06);
        margin-bottom: 1.2rem;
        line-height: 1.7;
        font-size: 1.02rem;
    ">
        Cette section présente les espaces de communication Telegram téléchargés liés à 
        la migration forcée de l'Ukraine vers la Russie depuis 2022. Chaque point correspond 
        à une ville ou à une région. La taille du point reflète le nombre d'espaces de communication téléchargés associés à ce lieu.
    </div>
    """,
    unsafe_allow_html=True,
)

if cities_df.empty:
    st.warning("Таблица городов пуста или в ней нет координат lat/lon.")
    st.stop()

center_lat = float(cities_df["lat"].mean())
center_lon = float(cities_df["lon"].mean())

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=4,
    tiles="CartoDB positron",
    control_scale=True,
)

for _, city_row in cities_df.iterrows():
    city_topics = topics_df[topics_df["city_id"] == city_row["city_id"]]
    tooltip_html = build_tooltip_html(city_row, city_topics)

    folium.CircleMarker(
        location=[float(city_row["lat"]), float(city_row["lon"])],
        radius=point_radius(int(city_row["total"])),
        color="#7a0019",
        fill=True,
        fill_color="#7a0019",
        fill_opacity=0.72,
        weight=1,
        tooltip=folium.Tooltip(
            tooltip_html,
            sticky=True,
            direction="top",
            opacity=0.96,
        ),
    ).add_to(m)

map_data = st_folium(
    m,
    height=700,
    use_container_width=True,
    returned_objects=["last_object_clicked_tooltip"],
)

clicked_city_id = None

if map_data:
    clicked_city_id = extract_city_id(map_data.get("last_object_clicked_tooltip"))

if (
    clicked_city_id
    and clicked_city_id != st.session_state["telegram_last_city_click"]
):
    st.session_state["telegram_last_city_click"] = clicked_city_id
    st.session_state["selected_city_id"] = clicked_city_id
    st.switch_page(CITY_PAGE)

if clicked_city_id is None:
    st.session_state["telegram_last_city_click"] = None
