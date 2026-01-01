# This is the index/intro page of our web app.
import streamlit as st
from snipvid import snipvid_page
from landing_page import landing_page
from rag import rag
from personallized_coach import personalized_coach

page_mapping_to_func = {
    'Home': landing_page,
    'Snip Video': snipvid_page,
    ''
    'RAG': rag,
}

web_app = st.sidebar.selectbox("Choose an app: ", page_mapping_to_func.keys())
page_mapping_to_func[web_app]()