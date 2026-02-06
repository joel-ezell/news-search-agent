"""Streamlit UI for the Research & Inquiry Crew

Usage:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

This app intelligently routes queries to either news research or general inquiry
based on the content of the user's input.
"""

import streamlit as st
from dotenv import load_dotenv
from crew import NewsResearchCrew, GeneralInquiryCrew, QueryRouter
from requests.exceptions import Timeout

load_dotenv()

st.set_page_config(page_title="Research & Inquiry Crew", layout="wide")
st.title("🔍 Research & Inquiry Crew")
st.markdown("Ask about news topics or any general question - the crew will intelligently route your query and provide comprehensive answers.")

# Quick topic buttons for news
st.subheader("Quick News Topics")
cols = st.columns(4)

topic_buttons = [
    ("🏆 Sports", "Sports"),
    ("💻 Technology", "Technology"),
    ("💰 Finance", "Finance"),
    ("🌍 World News", "World News")
]

for col, (button_label, topic) in zip(cols, topic_buttons):
    with col:
        if st.button(button_label, key=f"btn_{topic}", use_container_width=True):
            st.session_state.run_query = True
            st.session_state.query_input = topic
            st.session_state.is_news = True

# Custom query input
st.subheader("Custom Query")
query_input = st.text_input(
    "Enter your question or topic", 
    value="", 
    placeholder="Ask about current news, or any general question...",
    key="custom_query"
)

# Submit on Enter key or button click
if query_input:
    st.session_state.run_query = True
    st.session_state.query_input = query_input
    st.session_state.is_news = None  # Will be determined by router
else:
    if st.button("Search", key="search_btn"):
        if query_input:
            st.session_state.run_query = True
            st.session_state.query_input = query_input
            st.session_state.is_news = None  # Will be determined by router

# Execute query if triggered
if st.session_state.get("run_query", False):
    query = st.session_state.get("query_input", "")
    
    if not query.strip():
        st.error("Please enter a question or select a topic.")
        st.session_state.run_query = False
    else:
        # Determine query type if not already set
        if st.session_state.get("is_news") is None:
            router = QueryRouter()
            query_type = router.route_query(query)
            st.session_state.is_news = (query_type == 'news')
        
        is_news = st.session_state.get("is_news", True)
        query_type_label = "news research" if is_news else "general inquiry"
        st.info(f"Running {query_type_label} for: {query}")

        max_attempts = 3
        result = None
        err = None
        
        for attempt in range(1, max_attempts + 1):
            if attempt > 1:
                st.info(f"⏱️ Attempt {attempt} of {max_attempts}...")
            
            with st.spinner(f"Running Crew (attempt {attempt}/{max_attempts}) — this may take a bit depending on LLM/tool calls..."):
                try:
                    if is_news:
                        # For news queries, treat as a list of topics
                        topics = [query] if isinstance(query, str) else query
                        crew = NewsResearchCrew(topics)
                    else:
                        crew = GeneralInquiryCrew(query)
                    
                    result = crew.run()
                    err = None
                    break  # Success! Exit retry loop
                except Timeout:
                    result = None
                    err = "Request timed out (30 second limit). "
                    if attempt < max_attempts:
                        st.warning(f"⚠️ Timeout on attempt {attempt}. Retrying...")
                except Exception as e:
                    result = None
                    err = e
                    print(f"Exception occurred: {type(e).__name__}: {str(e)}")
                    break  # Don't retry non-timeout errors

        if result:
            st.subheader("Result")
            st.text_area("Result", value=result, height=400, disabled=True)
        else:
            error_msg = str(err) if err else "Unknown error occurred."
            st.error(f"✗ Crew run failed: {error_msg}")
            
            if "timed out" in error_msg.lower():
                st.warning("The request timed out after 3 attempts. This might be due to high server load or network issues.")
            
            if st.button("🔄 Retry"):
                st.rerun()
            
            if err:
                st.exception(err)

        if result:
            st.success("Run complete ✅")
        
        st.session_state.run_query = False

st.markdown("---")
