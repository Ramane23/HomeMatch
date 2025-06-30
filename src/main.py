"""
main_home_match_app.py
~~~~~~~~~~~~~~~~~~~~~~
Entry-point that ties together:
  • Sidebar (LoadStreamlitUI)
  • Groq LLM credential check
  • `home_match` LangChain pipeline
  • Result rendering using the HomeMatchDisplay class
"""

from __future__ import annotations

import streamlit as st
from loguru import logger

from src.frontend.streamlit.load_streamlit_ui import ui
from src.llms.groqllm import GroqLLM
from src.frontend.streamlit.display_streamlit import HomeMatchDisplay


def load_home_match_app() -> None:
    """Run the HomeMatch Streamlit app with full error handling and UI logic."""

    # 1. Load UI and sidebar
    logger.info(f"loading the UI and sidebar")
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    st.markdown("---")
    logger.info(f"adding the subheader 🔍 Find Your Ideal Home")
    st.subheader("🔍 Find Your Ideal Home")

    if st.button("✨ Search Listings", use_container_width=True):
        with st.spinner("Running AI search based on your preferences..."):
            try:
                # 2. Ensure Groq LLM is usable (API key etc.)
                llm = GroqLLM(user_controls_input=user_input)
                model = llm.get_llm_model()

                if not model:
                    st.error("❌ LLM model could not be initialized (check your API key)")
                    return

                # 3. Build query, invoke the full_chain and display results using HomeMatchDisplay render method
                logger.info(f"Building query, invoking the full_chain and displaying results using HomeMatchDisplay render method")
                home_match_display = HomeMatchDisplay(model)
                home_match_display.render()

            except Exception as exc:
                st.error(f"❌ An unexpected error occurred: {exc}")


if __name__ == "__main__":
    load_home_match_app()
