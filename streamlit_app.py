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

        # Capture stdout (crew prints) so we can show logs in the UI
        buf = io.StringIO()
        with st.spinner("Running Crew — this may take a bit depending on LLM/tool calls..."):
            with contextlib.redirect_stdout(buf):
                crew = NewsResearchCrew(topic_list, search_depth)
                try:
                    result = crew.run()
                except Exception as e:
                    result = None
                    err = e
        logs = buf.getvalue()

        if result:
            st.subheader("Research Report")
            # The result is plain text — show in a wrapping, read-only text area for better readability
            st.text_area("Research Report", value=result, height=400, disabled=True)
        else:
            st.error("Crew run failed. See logs for details.")
            st.exception(err)

        with st.expander("Show Crew logs"):
            if logs.strip():
                # Use a wrapping text area for logs so long lines wrap and are scrollable
                st.text_area("Crew logs", value=logs, height=300, disabled=True)
            else:
                st.write("No logs captured.")

        st.success("Run complete ✅")

st.markdown("---")
st.markdown("**Tip:** Make sure your `.env` contains `GROQ_API_KEY`, `GNEWS_API_KEY`, and `SERPER_API_KEY` as needed.")

