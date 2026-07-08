import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TASS Corpus",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent.parent
TASS_FILE = BASE_DIR / "data" / "Final_corpus_TASS.json"

@st.cache_data
def load_tass_data():
    with open(TASS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for article_id, article in data.items():
        rows.append(
            {
                "id": article_id,
                "title": article.get("title", ""),
                "published_dt": article.get("published_dt", ""),
                "url": article.get("url", ""),
                "text": article.get("text", ""),
                "hashtags": article.get("hashtags", []),
            }
        )

    df = pd.DataFrame(rows)

    df["published_dt"] = pd.to_datetime(df["published_dt"], errors="coerce")
    df = df.dropna(subset=["published_dt"]).copy()
    df["date"] = df["published_dt"].dt.date

    df = df.sort_values("published_dt", ascending=False).reset_index(drop=True)

    return df


df = load_tass_data()

if st.button("← Back", use_container_width=False):
    st.switch_page("pages/home.py")

st.title("TASS corpus : articles sur la migration forcée d'Ukraine vers la Russie depuis 2022")

st.html(
    """
    <div style="
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background-color: rgba(255,255,255,0.06);
        margin-bottom: 1.2rem;
        line-height: 1.7;
        font-size: 1.02rem;
    ">
        <p>
            <b>L'agence TASS</b> (Agence télégraphique de Russie) est la principale
            agence de presse publique russe. Au cours de la guerre en Ukraine, elle est
            devenue une source centrale d'information officielle.
        </p>

        <p>
            Le corpus présenté ici couvre la période
            <b>du 18 février 2022 au 11 décembre 2025</b>. Il a été constitué en deux étapes :
            d'abord par une <b>classification supervisée</b> appliquée aux titres de l'ensemble
            des articles publiés par TASS durant cette période, puis par une phase de
            <b>filtrage résiduel au moyen d'un modèle de langage</b> (LLM), afin d'éliminer
            les faux positifs et de ne conserver que les articles directement pertinents
            pour cette recherche.
        </p>
    </div>
    """
)

st.divider()

if df.empty:
    st.warning("Le corpus TASS est vide.")
    st.stop()

if "tass_n_articles" not in st.session_state:
    st.session_state["tass_n_articles"] = 15

df["year"] = df["published_dt"].dt.year
df["month"] = df["published_dt"].dt.month
df["day"] = df["published_dt"].dt.date

col1, col2, col3, col4 = st.columns([1, 1, 1.4, 1])

with col1:
    selected_year = st.selectbox(
        "Année",
        ["Toutes"] + sorted(df["year"].dropna().unique(), reverse=True),
    )

with col2:
    if selected_year == "Toutes":
        month_df = df.copy()
    else:
        month_df = df[df["year"] == selected_year]

    selected_month = st.selectbox(
        "Mois",
        ["Tous"] + sorted(month_df["month"].dropna().unique()),
    )

with col3:
    if selected_year == "Toutes":
        day_df = df.copy()
    else:
        day_df = df[df["year"] == selected_year]

    if selected_month != "Tous":
        day_df = day_df[day_df["month"] == selected_month]

    available_days = sorted(day_df["day"].dropna().unique(), reverse=True)

    selected_day = st.selectbox(
        "Date",
        ["Toutes"] + available_days,
    )

with col4:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    reset_filter = st.button("Réinitialiser", use_container_width=True)

if reset_filter:
    selected_year = "Toutes"
    selected_month = "Tous"
    selected_day = "Toutes"
    st.session_state["tass_n_articles"] = 15
    st.rerun()


if selected_day != "Toutes":
    filtered_df = df[df["day"] == selected_day].copy()

elif selected_year != "Toutes" and selected_month != "Tous":
    filtered_df = df[
        (df["year"] == selected_year)
        & (df["month"] == selected_month)
    ].copy()

elif selected_year != "Toutes":
    filtered_df = df[df["year"] == selected_year].copy()

else:
    filtered_df = df.copy()
    
if selected_day != "Toutes":
    st.metric("Nombre d'articles pour cette date", len(filtered_df))
elif selected_year != "Toutes" and selected_month != "Tous":
    st.metric("Nombre d'articles pour ce mois", len(filtered_df))
elif selected_year != "Toutes":
    st.metric("Nombre d'articles pour cette année", len(filtered_df))
else:
    st.metric("Nombre total d'articles dans le corpus", len(filtered_df))

if selected_day != st.session_state.get("tass_current_filter"):
    st.session_state["tass_current_filter"] = selected_day
    st.session_state["tass_n_articles"] = 15
    st.rerun()

st.divider()

if filtered_df.empty:
    st.info("Aucun article à afficher.")
    st.stop()

articles_to_show = filtered_df.head(st.session_state["tass_n_articles"])

for _, row in articles_to_show.iterrows():
    title = row["title"]
    published_dt = row["published_dt"]
    url = row["url"]
    text = row["text"]
    hashtags = row["hashtags"]

    date_display = (
        published_dt.strftime("%d/%m/%Y %H:%M")
        if pd.notna(published_dt)
        else "Date inconnue"
    )

    hashtags_display = (
        ", ".join(hashtags)
        if isinstance(hashtags, list) and hashtags
        else "—"
    )

    with st.container(border=True):
        st.markdown(f"### {title}")
        st.markdown(f"**Date :** {date_display}")

        if url:
            st.markdown(f"**URL :** [{url}]({url})")
        else:
            st.markdown("**URL :** —")

        st.markdown(f"**Hashtags :** {hashtags_display}")

        with st.expander("Texte de l'article"):
            st.write(text)

if st.session_state["tass_n_articles"] < len(filtered_df):
    if st.button("Charger plus d'articles", use_container_width=True):
        st.session_state["tass_n_articles"] += 15
        st.rerun()
