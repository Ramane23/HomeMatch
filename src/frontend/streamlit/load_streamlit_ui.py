"""
load_streamlit_ui.py
~~~~~~~~~~~~~~~~~~~~
Streamlit sidebar & form for the **HomeMatch** demo.

All static choices (amenities, transportation, neighbourhood traits, etc.) are
pulled from *uiconfig.ini* via the shared `Config` helper instead of being
hard‑coded.  The page title, available LLM providers, and Groq model list are
likewise configurable through the same file, so changing `uiconfig.ini` is all
it takes to re‑brand or swap models.
"""

from __future__ import annotations

import os
from typing import Dict, Any

import streamlit as st

from src.frontend.config.uiconfig import ui_config

__all__ = ["LoadStreamlitUI"]


class LoadStreamlitUI:
    """Render the sidebar and collect user inputs for the HomeMatch app."""

    def __init__(self, *, show_header: bool = True) -> None:
        self.config = ui_config
        self.show_header = show_header
        self.user_controls: Dict[str, Any] = {}

        # Pull static option lists from config file
        self.AMENITIES = self.config.get_amenities()
        self.TRANSPORTATION = self.config.get_transportation_options()
        self.NEIGHBORHOOD_TRAITS = self.config.get_neighborhood_traits()

    # ------------------------------------------------------------------
    # PUBLIC
    # ------------------------------------------------------------------
    def load_streamlit_ui(self) -> Dict[str, Any]:
        """Draw widgets, store them in *user_controls*, and return the dict."""
        # Page‑level settings — title comes straight from uiconfig.ini
        page_title = self.config.get_page_title()
        st.set_page_config(page_title=page_title, layout="wide")

        if self.show_header:
            # Add a house emoji if it's not already in the title
            header_text = ("🏡 " + page_title) if not page_title.startswith("🏡") else page_title
            st.header(header_text)

        # –– Sidebar ––
        with st.sidebar:
            st.subheader("🔧 Configuration")
            self._render_llm_selector()
            st.markdown("---")
            st.subheader("🏠 Your Desired Home")
            self._render_home_preferences()

        return self.user_controls

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------
    def _render_llm_selector(self) -> None:
        """LLM backend, model, and API‑key widgets."""
        llm_options = self.config.get_llm_options()
        self.user_controls["selected_llm"] = st.selectbox("LLM Provider", llm_options)

        if self.user_controls["selected_llm"] == "Groq":
            model_options = self.config.get_groq_model_options()
            self.user_controls["selected_groq_model"] = st.selectbox("Groq Model", model_options)
            api_key = st.text_input("GROQ API Key", type="password")
            self.user_controls["GROQ_API_KEY"] = api_key
            st.session_state["GROQ_API_KEY"] = api_key

            if not api_key:
                st.warning(
                    "⚠️ Please enter your GROQ API key. Get one at https://console.groq.com/keys",
                    icon="⚠️",
                )

    def _render_home_preferences(self) -> None:
        """Collect house characteristics the user is looking for."""
        # Basic numbers
        self.user_controls["bedrooms"] = st.number_input(
            "Bedrooms", min_value=0, max_value=10, step=1, value=3, format="%d"
        )
        self.user_controls["bathrooms"] = st.number_input(
            "Bathrooms", min_value=0, max_value=10, step=1, value=2, format="%d"
        )

        # House size & price
        col1, col2 = st.columns(2)
        with col1:
            self.user_controls["house_size"] = st.number_input(
                "House size (sqft)", min_value=200, max_value=10000, step=100, value=2000
            )
        with col2:
            self.user_controls["price_range"] = st.text_input("Budget (e.g., '$600k')", value="$600k")

        # Lists: amenities, transportation, neighborhood traits
        self.user_controls["amenities"] = st.multiselect(
            "Amenities",
            options=self.AMENITIES,
            default=self.AMENITIES[:2] if len(self.AMENITIES) >= 2 else self.AMENITIES,
        )
        self.user_controls["transportation"] = st.multiselect(
            "Transportation",
            options=self.TRANSPORTATION,
            default=self.TRANSPORTATION[:1] if self.TRANSPORTATION else [],
        )
        self.user_controls["neighborhood_traits"] = st.multiselect(
            "Neighborhood traits",
            options=self.NEIGHBORHOOD_TRAITS,
            default=self.NEIGHBORHOOD_TRAITS[:1] if self.NEIGHBORHOOD_TRAITS else [],
        )

        # Lifestyle
        self.user_controls["lifestyle"] = st.text_input(
            "Lifestyle (e.g., 'Remote work')", value="Remote work"
        )

        # Optional free‑form summary (hidden under an expander)
        with st.expander("Optional one‑line summary"):
            self.user_controls["summary"] = st.text_input(
                "Summary", value="Looking for a modern sustainable family home."
            )
