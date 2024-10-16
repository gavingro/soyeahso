import streamlit as st
import openai
import ell

from src.prompts import get_quality_icebreaker_questions
from src.env import validate_env

OPENAI_API_KEY_NAME = "OPENAI_API_KEY"


def main():
    _register_ell_model(open_ai_key=_get_open_ai_key())

    if "icebreakers" not in st.session_state:
        st.session_state["icebreakers"] = []
    if st.button("So yeah, so...", type="primary"):
        with st.spinner("...Lemme think..."):
            st.session_state["icebreakers"] += get_quality_icebreaker_questions(
                n_seeded_questions=6,
                previously_asked_questions=st.session_state["icebreakers"],
            )
        col1, col2, col3 = st.columns(3)
        for i, icebreaker in enumerate(st.session_state["icebreakers"]):
            if i % 3 == 0:
                with col1:
                    st.write(icebreaker)
                    st.divider()
            if i % 3 == 1:
                with col2:
                    st.write(icebreaker)
                    st.divider()
            if i % 3 == 2:
                with col3:
                    st.write(icebreaker)
                    st.divider()


@st.cache_resource
def _get_open_ai_key():
    open_ai_key = validate_env(OPENAI_API_KEY_NAME)
    if not open_ai_key:
        return st.secrets["OPENAI_API_KEY"]
    return open_ai_key


@st.cache_resource
def _register_ell_model(open_ai_key: str):
    client = openai.Client(api_key=open_ai_key)
    ell.config.register_model("gpt-4o-mini", client)


if __name__ == "__main__":
    main()
