import pandas as pd
import streamlit as st

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="City page",
    layout="wide",
)

CITIES_FILE = BASE_DIR / "data" / "cities.csv"
TOPICS_FILE = BASE_DIR / "data" / "city_topics.csv"


@st.cache_data
def load_data():
    cities = pd.read_csv(CITIES_FILE)
    topics = pd.read_csv(TOPICS_FILE)

    cities.columns = cities.columns.str.strip()
    topics.columns = topics.columns.str.strip()

    cities["city"] = cities["city"].astype(str).str.strip()
    cities["city_id"] = cities["city_id"].astype(str).str.strip()
    cities["total"] = pd.to_numeric(cities["total"], errors="coerce").fillna(0).astype(int)

    topics["city_id"] = topics["city_id"].astype(str).str.strip()

    return cities, topics


def filter_dataframe(df):
    filtered = df.copy()

    filter_columns = [
        "type",
        "type_communication",
        "thematique",
    ]

    st.subheader("Filters")

    cols = st.columns(len(filter_columns))

    for col, column_name in zip(cols, filter_columns):
        if column_name in filtered.columns:
            options = sorted(
                filtered[column_name]
                .fillna("")
                .astype(str)
                .str.strip()
                .unique()
            )

            options = [x for x in options if x != ""]

            selected = col.multiselect(
                column_name,
                options=options,
                default=[],
            )

            if selected:
                filtered = filtered[
                    filtered[column_name].astype(str).str.strip().isin(selected)
                ]

    return filtered


cities_df, topics_df = load_data()

city_id = st.query_params.get("city_id")

if not city_id:
    city_id = st.session_state.get("selected_city_id")

top_left, top_right = st.columns([1, 6])

with top_left:
    if st.button("← Back", use_container_width=True):
        st.switch_page("pages/full_archive.py")

if not city_id:
    with top_right:
        st.title("City page")
    st.warning("city_id не передан.")
    st.stop()

city_id = str(city_id).strip()

city_row_df = cities_df[cities_df["city_id"] == city_id]

if city_row_df.empty:
    with top_right:
        st.title("City page")
    st.error(f"Город с city_id='{city_id}' не найден.")
    st.stop()

city_row = city_row_df.iloc[0]
city_name = city_row["city"]

with top_right:
    st.title(city_name)

st.metric("Espaces téléchargés", int(city_row["total"]))

st.divider()

city_spaces = topics_df[topics_df["city_id"] == city_id].copy()

if city_spaces.empty:
    st.info("Для этого города нет скачанных espaces de communication.")
    st.stop()

display_columns = [
    "titre_support",
    "type",
    "type_communication",
    "thematique",
    "description",
]

available_columns = [col for col in display_columns if col in city_spaces.columns]
city_spaces = city_spaces[available_columns].copy()

filtered_df = filter_dataframe(city_spaces)

st.divider()
st.subheader("Espaces de communication")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)
