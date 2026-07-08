import streamlit as st

st.set_page_config(
    page_title="Migration Corpus Archive",
    layout="wide",
)

home_page = st.Page(
    "pages/home.py",
    title="Home",
    default=True,
    visibility="hidden",
)

tass_corpus_page = st.Page(
    "pages/tass_corpus.py",
    title="TASS corpus",
    url_path="tass-corpus",
    visibility="hidden",
)

telegram_corpus_page = st.Page(
    "pages/full_archive.py",
    title="Telegram corpus",
    url_path="telegram-corpus",
    visibility="hidden",
)

city_page = st.Page(
    "pages/city_page.py",
    title="City page",
    url_path="city-page",
    visibility="hidden",
)

pg = st.navigation(
    [home_page, tass_corpus_page, telegram_corpus_page, city_page],
    position="hidden",
)

pg.run()