"""
display_streamlit.py
~~~~~~~~~~~~~~~~~~~~
Main Streamlit page for HomeMatch — renders the UI, passes user input to the
LangChain pipeline, and displays matching home listings with a summary.
"""

import streamlit as st
from langchain_groq import ChatGroq

from src.config import settings
from src.frontend.streamlit.load_streamlit_ui import LoadStreamlitUI
from src.chains.full_chain import HomeMatch  # <-- your composed LangChain pipeline (cleaner → RAG)


class HomeMatchDisplay:
    """Encapsulates the HomeMatch Streamlit interface and display logic."""

    def __init__(self, model):
        
        self.home_match = HomeMatch(model)
        
        # Load sidebar and store user inputs
        self.ui = LoadStreamlitUI()
        self.user_inputs = self.ui.load_streamlit_ui()
        
    def render(self):
        """Render the main page content and trigger the query/search."""
        st.markdown("---")
        st.subheader("🔍 Find Your Ideal Home")

        if st.button("✨ Search Listings", use_container_width=True):
            with st.spinner("Running AI search based on your preferences..."):

                # Build the query
                query = self._build_query()

                # Invoke LangChain pipeline
                results = self.home_match.invoke_full_chain({"raw_query": query})

                # Show results
                self._render_summary(results)
                self._render_listings(results)

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

    def _render_summary(self, results):
        """Display AI-generated summary."""
        st.success("\n\n" + results.get("answer", "No suggestions returned."))

    def _render_listings(self, results):
        """Display listings from the RAG context using shared render_results."""
        st.markdown("---")
        st.subheader("🏘 Top Matching Listings")
        self.home_match.render_results(results)
        

# Instantiate and render UI if run directly
if __name__ == "__main__":
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512   # plenty for one JSON listing
    )
    HomeMatchDisplay(llm).render()
