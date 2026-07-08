import streamlit as st


def home():
    st.html(
        """
        <div style="text-align:center; margin-top:80px; margin-bottom:50px;">
            <div style="font-size:2.7rem; font-weight:700;">
                Archive numérique
            </div>

            <div style="font-size:1.8rem; font-weight:300; margin-top:12px;">
                Migration forcée d'Ukraine vers la Russie depuis l'invasion russe en grande échelle de 2022
            </div>

            <div style="font-size:1rem; color:#888; margin-top:35px;">
                Travail réalisé dans le cadre du mémoire de Master en Humanités Numériques.
            </div>
        </div>
        """
    )

    st.markdown(
        """
        <style>
        .st-key-tass_corpus_btn button,
        .st-key-telegram_corpus_btn button {
            height: 78px;
            border-radius: 12px;
        }

        .st-key-tass_corpus_btn button div,
        .st-key-telegram_corpus_btn button div,
        .st-key-tass_corpus_btn button p,
        .st-key-telegram_corpus_btn button p {
            font-size: 24px !important;
            font-weight: 400 !important;
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        if st.button("TASS corpus", key="tass_corpus_btn", use_container_width=True):
            st.switch_page("pages/tass_corpus.py")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        if st.button("Telegram corpus", key="telegram_corpus_btn", use_container_width=True):
            st.switch_page("pages/full_archive.py")

home()