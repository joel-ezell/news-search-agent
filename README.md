# News Search Agent

A CrewAI-powered news research agent that searches for and analyzes recent news articles using multiple sources.

## Features

- **Recent News Focus**: Automatically filters news to the last 7 days and sorts by publish date
- **Multiple Sources**: Uses GNews API for news articles and Serper API for general web search
- **Comprehensive Analysis**: Provides executive summaries, timelines, trend analysis, and source citations
- **Configurable Depth**: Basic, comprehensive, or detailed research modes
- **Agent-Based Architecture**: Uses CrewAI framework with specialized news research agents

## Setup

1. Clone the repository:
```bash
git clone git@github.com:joel-ezell/news-search-agent.git
cd news-search-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```env
# LLM Provider
GROQ_API_KEY=your_groq_api_key_here

# News and Search APIs
GNEWS_API_KEY=your_gnews_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# CrewAI Configuration
CREWAI_LLM_PROVIDER=groq
CREWAI_MODEL=llama-3.3-70b-versatile
```

## Usage

Run the news research agent:

```bash
python main.py
```

You'll be prompted to enter:
- News topics to research (comma-separated)
- Research depth (basic/comprehensive/detailed)

The agent will search for recent news, analyze it, and provide a comprehensive report.

## Architecture

- **NewsAgents**: Defines specialized agents for news research, analysis, and verification
- **NewsTasks**: Task definitions for comprehensive news research
- **SearchNews**: Tool for searching recent news articles via GNews API
- **SearchTools**: Tool for general web search via Serper API
- **NewsResearchCrew**: Main orchestrator that coordinates agents and tasks

## API Keys Required

- **Groq API**: For LLM inference (llama-3.3-70b-versatile)
- **GNews API**: For news article search
- **Serper API**: For general web search

## Example Output

The agent provides structured reports including:
- Executive Summary
- Topic-by-Topic Analysis  
- Event Timeline
- Trend Implications
- Source Citations and Reliability Assessment

All news results are filtered to the most recent 7 days and sorted by publish date to ensure current relevance.

## Streamlit UI ✅

A lightweight Streamlit application is included to run the Crew from a browser UI.

Run it locally:

```bash
pip install -r requirements.txt
pip install streamlit
streamlit run streamlit_app.py
```

Make sure your `.env` includes `GROQ_API_KEY`, `GNEWS_API_KEY`, and `SERPER_API_KEY` before running the UI.