"""
display_streamlit.py
~~~~~~~~~~~~~~~~~~~~
Main Streamlit page for HomeMatch — renders the UI, passes user input to the
LangChain pipeline, and displays matching home listings with a summary.
"""

import streamlit as st
from langchain_groq import ChatGroq

from src.config import settings
from src.llms.groqllm import GroqLLM
from src.frontend.streamlit.load_streamlit_ui import LoadStreamlitUI
from src.chains.full_chain import (
    HomeMatch,
)  # <-- your composed LangChain pipeline (cleaner → RAG)


class HomeMatchDisplay:
    """Encapsulates the HomeMatch Streamlit interface and display logic."""

    def __init__(self):

        # Load sidebar and store user inputs
        self.ui = LoadStreamlitUI()
        self.user_inputs = self.ui.load_streamlit_ui()
        self.home_match = HomeMatch(self.get_selected_model(self.user_inputs))

    def render(self):
        """Render the main page content and trigger the query/search."""
        st.markdown("---")
        st.subheader("🔍 Find Your Ideal Home")

        if st.button(
            "✨ Search Listings", use_container_width=True, key="search_btn_top"
        ):
            with st.spinner("Running AI search based on your preferences..."):

                # Build the query
                query = self._build_query()

                # Invoke LangChain pipeline
                results = self.home_match.invoke_full_chain({"raw_query": query})

                # Show results
                # self._render_summary(results)
                self.render_results(results)

    def get_selected_model(self, user_controls: dict):
        """
        Build a GroqLLM instance from Streamlit sidebar inputs and
        return the underlying model object if it’s usable.

        If the model cannot be initialized (missing or bad API key),
        shows a Streamlit error and returns None.

        """
        llm = GroqLLM(user_controls)
        model = llm.get_llm_model()

        if model is None:
            st.error("❌ LLM model could not be initialized (check your GROQ API key)")
            return None

        return model

    def _build_query(self) -> str:
        """Generate a natural language query from user inputs."""
        return self.ui.user_controls.get("summary") or (
            f"Looking for a {self.user_inputs['bedrooms']}-bedroom, "
            f"{self.user_inputs['bathrooms']}-bathroom home, "
            f"around {self.user_inputs['house_size']} sqft, "
            f"priced at {self.user_inputs['price_range']}, "
            f"with amenities like {', '.join(self.user_inputs['amenities'])}, "
            f"in a {', '.join(self.user_inputs['neighborhood_traits'])} neighborhood, "
            f"near {', '.join(self.user_inputs['transportation'])}. "
            f"Ideal for someone with a {self.user_inputs['lifestyle']} lifestyle."
        )

    def render_results(self, results):
        """
        Display matching listings and the LLM-generated summary in a clean, interactive UI.
        """

        st.markdown("### 🏘 Top Matching Listings")

        docs = results.get("context", [])

        if not docs:
            st.warning("No matching listings found.")
            return

        for i, doc in enumerate(docs, 1):
            meta = doc.metadata

            with st.expander(f"🏡 Listing {i}: {meta.get('neighborhood', 'Unknown')}"):
                st.markdown(
                    f"""
                    - 📍 **Neighborhood**: `{meta.get('neighborhood', 'N/A')}`
                    - 🛏 **Bedrooms**: `{meta.get('bedrooms', 'N/A')}`
                    - 🛁 **Bathrooms**: `{meta.get('bathrooms', 'N/A')}`
                    - 📐 **Size**: `{meta.get('house_size', 'N/A')} sqft`
                    - 💰 **Price**: `${meta.get('price', 'N/A'):,}`
                    """
                )

        # Summary block
        st.markdown("---")
        st.markdown("### 🤖 AI Summary")
        st.markdown(
            f"""
            <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;">
            {results.get('answer', 'No summary returned.')}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # def _render_listings(self, results):
    #     """Display listings from the RAG context using shared render_results."""
    #     st.markdown("---")
    #     st.subheader("🏘 Top Matching Listings")
    #     self.render_results(results)


# Instantiate and render UI if run directly
if __name__ == "__main__":

    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512,  # plenty for one JSON listing
    )
    HomeMatchDisplay(llm).render()
