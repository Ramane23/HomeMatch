"""
load_streamlit_ui.py
~~~~~~~~~~~~~~~~~~~~
Streamlit sidebar & form for the **HomeMatch** demo.

• Reads all static options (page title, LLM list, model list, amenities, etc.)
  from `uiconfig.ini` via the shared `ui_config` helper.
• Builds a clean sidebar that lets the user:
    – choose an LLM provider / Groq model and enter an API key
    – specify every home-search preference (beds, baths, size, budget …)
• Returns a single dictionary (`user_controls`) with every selection – ready
  for the main app to feed into the LangChain pipeline.
"""

from __future__ import annotations

import os
from typing import Dict, Any

import streamlit as st
from src.frontend.config.uiconfig import (
    ui_config,
)  # ← python wrapper around uiconfig.ini

__all__ = ["LoadStreamlitUI"]


class LoadStreamlitUI:
    """Render the sidebar and collect user inputs for the HomeMatch app."""

    # --------------------------------------------------------------------- #
    # INITIALISATION                                                        #
    # --------------------------------------------------------------------- #
    def __init__(self, *, show_header: bool = True) -> None:
        self.config = ui_config  # global config object
        self.show_header = show_header
        self.user_controls: Dict[str, Any] = (
            {}
        )  # dict to collect user imputs from the ui

        # Pull option lists directly from the .ini file
        self.AMENITIES = self.config.get_amenities()
        self.TRANSPORTATION = self.config.get_transportation_options()
        self.NEIGHBORHOOD_TRAITS = self.config.get_neighborhood_traits()

    # --------------------------------------------------------------------- #
    # PUBLIC ENTRY POINT                                                    #
    # --------------------------------------------------------------------- #
    def load_streamlit_ui(self) -> Dict[str, Any]:
        """
        Draw all sidebar widgets, store results in `self.user_controls`,
        and return that dict so the caller can use it.
        """
        # ---- Page-level Streamlit config ---------------------------------
        page_title = self.config.get_page_title()
        # assigning the title of the page and the choosing the layout of the page
        st.set_page_config(page_title=page_title, layout="wide")

        # if the show_header option is selected
        if self.show_header:
            header_text = (  # add 🏡 if user didn’t put it in .ini
                "🏡 " + page_title if not page_title.startswith("🏡") else page_title
            )
            st.header(header_text)

        # ---- Sidebar -----------------------------------------------------
        with st.sidebar:
            # create a subheader in the sidebar to allow the user to choose the configuration (which LLM to use..)
            st.subheader("🔧 Configuration")
            self._render_llm_selector()  # update those choice in the user_controls dict

            st.markdown("---")

            # creating another subheader to allow the user to select the key properties of the home
            st.subheader("🏠 Your Desired Home")
            self._render_home_preferences()  # update those choice in the user_controls dict

        return self.user_controls

    # --------------------------------------------------------------------- #
    # INTERNAL HELPERS                                                      #
    # --------------------------------------------------------------------- #
    def _render_llm_selector(self) -> None:
        """LLM provider dropdown, model list (if Groq), and API-key box."""
        # Provider dropdown – values come straight from .ini
        llm_options = self.config.get_llm_options()  # ["Groq", ...]
        self.user_controls["selected_llm"] = st.selectbox(
            "LLM Provider", llm_options, key="llm_provider"
        )

        # Extra widgets if the user picked Groq
        if self.user_controls["selected_llm"] == "Groq":
            model_options = self.config.get_groq_model_options()
            self.user_controls["selected_groq_model"] = st.selectbox(
                "Groq Model", model_options, key="groq_model"
            )

            api_key = st.text_input("GROQ API Key", type="password")
            self.user_controls["GROQ_API_KEY"] = api_key
            st.session_state["GROQ_API_KEY"] = api_key  # make it accessible app-wide

            if not api_key:
                st.warning(
                    "⚠️ Please enter your GROQ API key. "
                    "You can create one at https://console.groq.com/keys",
                    icon="⚠️",
                )

    def _render_home_preferences(self) -> None:
        """All house-search parameters (beds, baths, size, etc.)."""
        # --- Numeric fields ----------------------------------------------
        self.user_controls["bedrooms"] = st.number_input(
            "Bedrooms",
            min_value=0,
            max_value=10,
            step=1,
            value=3,
            format="%d",
            key="bedrooms",
        )
        self.user_controls["bathrooms"] = st.number_input(
            "Bathrooms",
            min_value=0,
            max_value=10,
            step=1,
            value=2,
            format="%d",
            key="bathrooms",
        )

        # --- House size & price -----------------------------------------
        col1, col2 = st.columns(2)
        with col1:
            self.user_controls["house_size"] = st.number_input(
                "House size (sqft)",
                min_value=200,
                max_value=10_000,
                step=100,
                value=2_000,
                key="house_size",
            )
        with col2:
            self.user_controls["price_range"] = st.text_input(
                "Budget (e.g., '$600k')", value="$600k", key="price_range"
            )

        # --- Multiselects (values from .ini) -----------------------------
        self.user_controls["amenities"] = st.multiselect(
            "Amenities",
            options=self.AMENITIES,
            default=self.AMENITIES[:2] if len(self.AMENITIES) >= 2 else self.AMENITIES,
            key="amenities",
        )
        self.user_controls["transportation"] = st.multiselect(
            "Transportation",
            options=self.TRANSPORTATION,
            default=self.TRANSPORTATION[:1] if self.TRANSPORTATION else [],
            key="transportation",
        )
        self.user_controls["neighborhood_traits"] = st.multiselect(
            "Neighborhood traits",
            options=self.NEIGHBORHOOD_TRAITS,
            default=self.NEIGHBORHOOD_TRAITS[:1] if self.NEIGHBORHOOD_TRAITS else [],
            key="neighborhood_traits",
        )

        # --- Lifestyle + optional summary -------------------------------
        self.user_controls["lifestyle"] = st.text_input(
            "Lifestyle (e.g., 'Remote work')", value="Remote work", key="lifestyle"
        )

        with st.expander("Optional one-line summary"):
            self.user_controls["summary"] = st.text_input(
                "Summary",
                value="Looking for a modern sustainable family home.",
                key="summary",
            )


ui = LoadStreamlitUI()
