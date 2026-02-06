"""Streamlit UI for the News Research Crew

Usage:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

This app runs the `NewsResearchCrew` from `crew.py`, captures its stdout
(for debugging) and shows the final research report.
"""

import streamlit as st
from dotenv import load_dotenv
from crew import NewsResearchCrew
import io
import contextlib
from requests.exceptions import Timeout

load_dotenv()

st.set_page_config(page_title="News Research Crew", layout="wide")
st.title("📰 News Research Crew")
st.markdown("Use the Crew to research news topics. This UI calls your local Crew runner and displays logs and the final report.")

with st.form(key="research_form"):
    topics = st.text_input("Topics (comma-separated)", value="", placeholder="Enter your research topics here")
    search_depth = st.selectbox("Search depth", options=["basic", "comprehensive", "detailed"], index=1)
    run = st.form_submit_button("Run Research")

if run:
    if not topics.strip():
        st.error("Please enter at least one topic.")
    else:
        topic_list = [t.strip() for t in topics.split(",") if t.strip()]
        st.info(f"Running research for topics: {', '.join(topic_list)} — depth={search_depth}")

        max_attempts = 3
        result = None
        err = None
        logs = ""
        
        for attempt in range(1, max_attempts + 1):
            # Capture stdout (crew prints) so we can show logs in the UI
            buf = io.StringIO()
            
            if attempt > 1:
                st.info(f"⏱️ Attempt {attempt} of {max_attempts}...")
            
            with st.spinner(f"Running Crew (attempt {attempt}/{max_attempts}) — this may take a bit depending on LLM/tool calls..."):
                with contextlib.redirect_stdout(buf):
                    crew = NewsResearchCrew(topic_list, search_depth)
                    try:
                        result = crew.run()
                        err = None
                        logs = buf.getvalue()
                        break  # Success! Exit retry loop
                    except Timeout:
                        result = None
                        err = "Request timed out (30 second limit). "
                        logs = buf.getvalue()
                        if attempt < max_attempts:
                            st.warning(f"⚠️ Timeout on attempt {attempt}. Retrying...")
                    except Exception as e:
                        result = None
                        err = e
                        logs = buf.getvalue()
                        break  # Don't retry non-timeout errors

        if result:
            st.subheader("Research Report")
            # The result is plain text — show in a wrapping, read-only text area for better readability
            st.text_area("Research Report", value=result, height=400, disabled=True)
        else:
            error_msg = str(err) if err else "Unknown error occurred."
            st.error(f"✗ Crew run failed: {error_msg}")
            
            if "timed out" in error_msg.lower():
                st.warning("The request timed out after 3 attempts. This might be due to high server load or network issues.")
            
            if st.button("🔄 Retry Research"):
                st.rerun()
            
            if logs:
                st.exception(err)

        if logs:
            with st.expander("Show Crew logs"):
                if logs.strip():
                    # Use a wrapping text area for logs so long lines wrap and are scrollable
                    st.text_area("Crew logs", value=logs, height=300, disabled=True)
                else:
                    st.write("No logs captured.")

        if result:
            st.success("Run complete ✅")

st.markdown("---")

