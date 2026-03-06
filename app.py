import streamlit as st
from exa_py import Exa
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("EXA_API_KEY")
exa = Exa(api_key)

st.title("🔍 AI Search Engine")

query = st.text_input("Enter search query")
domain = st.text_input("Optional domain filter (example: github.com)")

if query:
    if domain:
        response = exa.search_and_contents(
            query,
            num_results=5,
            include_domains=[domain],
            text=True
        )
    else:
        response = exa.search_and_contents(
            query,
            num_results=5,
            text=True
        )

    for result in response.results:
        st.subheader(result.title)
        st.write(result.url)

        if result.text:
            st.write(result.text[:300])

        st.markdown("---")