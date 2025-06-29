"""
display_streamlit.py
~~~~~~~~~~~~~~~~~~~~
Main Streamlit page for HomeMatch — renders the UI, passes user input to the
LangChain pipeline, and displays matching home listings with a summary.
"""

import streamlit as st
from src.frontend.streamlit.load_streamlit_ui import LoadStreamlitUI
from src.main import full_chain  # <-- make sure this is your composed LangChain pipeline

# Load UI and capture user selections
ui = LoadStreamlitUI()
user_inputs = ui.load_streamlit_ui()

# Main content area
st.markdown("---")
st.subheader("🔍 Find Your Ideal Home")

if st.button("✨ Search Listings", use_container_width=True):
    with st.spinner("Running AI search based on your preferences..."):

        # Combine all user fields into a natural language query
        query = ui.user_controls.get("summary") or (
            f"Looking for a {user_inputs['bedrooms']}-bedroom, {user_inputs['bathrooms']}-bathroom home, "
            f"around {user_inputs['house_size']} sqft, priced at {user_inputs['price_range']}, "
            f"with amenities like {', '.join(user_inputs['amenities'])}, "
            f"in a {', '.join(user_inputs['neighborhood_traits'])} neighborhood, near {', '.join(user_inputs['transportation'])}. "
            f"Ideal for someone with a {user_inputs['lifestyle']} lifestyle."
        )

        # Run LangChain pipeline
        results = full_chain.invoke({"raw_query": query})

        # Display AI answer
        st.success("\n\n" + results.get("answer", "No summary returned."))

        st.markdown("---")
        st.subheader("🏘 Top Matching Listings")
        docs = results.get("context", [])

        if not docs:
            st.warning("No matching listings found.")
        else:
            for i, doc in enumerate(docs, 1):
                meta = doc.metadata
                with st.expander(f"🏡 Listing {i}", expanded=True):
                    st.markdown(f"""
                    - 📍 **Neighborhood**: `{meta.get('neighborhood', 'N/A')}`
                    - 🛏 **Bedrooms**: `{meta.get('bedrooms', 'N/A')}`
                    - 🛁 **Bathrooms**: `{meta.get('bathrooms', 'N/A')}`
                    - 📐 **Size**: `{meta.get('house_size', 'N/A')} sqft`
                    - 💵 **Price**: `${meta.get('price', 'N/A'):,}`
                    """)
