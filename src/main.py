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

    # Load the HomeMatch display
    logger.info(f"collecting the user imputs...")
    home_match_display = HomeMatchDisplay()
    user_inputs = home_match_display.user_inputs

    if not user_inputs:
        st.error("Error: Failed to load user input from the UI.")
        return

    try:

        # Build query, invoke the full_chain and display results using HomeMatchDisplay render method
        logger.info(
            f"Building query, invoking the full_chain and displaying results using HomeMatchDisplay render method"
        )
        home_match_display.render()

    except Exception as exc:
        st.error(f"❌ An unexpected error occurred: {exc}")


if __name__ == "__main__":
    load_home_match_app()
