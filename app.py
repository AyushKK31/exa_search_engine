import streamlit as st
from exa_py import Exa
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("EXA_API_KEY") or st.secrets["EXA_API_KEY"]
exa = Exa(api_key)

# Page setup
st.set_page_config(
    page_title="AI Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #f8f9fc;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 10px;
}

.sub-text {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.result-card {
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(200,200,200,0.3);
    margin-bottom: 18px;
    background: white;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    cursor: pointer;
}

.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.12);
}

.result-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 6px;
}

.result-url {
    color: #2563eb;
    font-size: 14px;
    margin-bottom: 10px;
}

.result-summary {
    font-size: 15px;
    color: #333;
}

.search-box {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🔍 AI Search Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Minimal semantic search powered by Exa AI</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙ Filters")

category = st.sidebar.selectbox(
    "Search Category",
    ["All", "GitHub", "Research Papers", "News"]
)

dark_mode = st.sidebar.toggle("Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    body {
        background-color: #0f172a;
        color: white;
    }
    .result-card {
        background: #1e293b;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .result-summary {
        color: #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# Domain logic
domain = None

if category == "GitHub":
    domain = "github.com"
elif category == "Research Papers":
    domain = "arxiv.org"
elif category == "News":
    domain = "news.google.com"

# Search input
query = st.text_input("Search anything...", placeholder="Type your query here")

# Search button
if st.button("Search"):
    if query:

        st.session_state.history.append(query)

        with st.spinner("Searching intelligently..."):

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

            st.success(f"Found {len(response.results)} results")

            for result in response.results:
                summary = result.text[:300] if result.text else "No summary available"

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">{result.title}</div>
                    <div class="result-url">
                        <a href="{result.url}" target="_blank">{result.url}</a>
                    </div>
                    <div class="result-summary">{summary}</div>
                </div>
                """, unsafe_allow_html=True)

# Search history
if st.session_state.history:
    st.sidebar.markdown("## 🕘 Recent Searches")
    for item in reversed(st.session_state.history[-5:]):
        st.sidebar.write(item)