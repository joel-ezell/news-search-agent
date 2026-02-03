import json
import requests
import urllib.parse
from datetime import datetime, timedelta, timezone
from crewai.tools.agent_tools import Tool
from typing import Type
from pydantic.v1 import BaseModel, Field
from dotenv import load_dotenv
import os

# Load API keys from environment, fall back to existing hard-coded values if needed
load_dotenv()
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "67b00b586b42fb594924a68f79458260")

class NewsSearchInput(BaseModel):
    """Input schema for news search tool."""
    query: str = Field(..., description="The search query for finding news articles")


def _search_news(query: str) -> str:
    """Execute the news search and return recent articles."""
    print(f"🔍 SearchNews tool called with query: '{query}'")
    max_results = 5
    encoded_query = urllib.parse.quote_plus(query)
    # Default to last 7 days and sort newest first
    to_date = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    from_date = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec='seconds').replace('+00:00', 'Z')

    url = (
        "https://gnews.io/api/v4/search"
        f"?q={encoded_query}"
        f"&lang=en"
        f"&max={max_results}"
        f"&sortby=publishedAt"
        f"&from={from_date}"
        f"&to={to_date}"
        f"&apikey={GNEWS_API_KEY}"
    )
    
    print(f"Making news request to URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains articles
        if 'articles' not in data:
            return "Error: Could not retrieve news articles. Please check your GNews API key."
        
        articles = data['articles']
        print(f"Found {len(articles)} articles")
        
        # Ensure most recent first even if API default changes
        try:
            articles.sort(key=lambda a: a.get('publishedAt', ''), reverse=True)
        except Exception:
            pass
        if not articles:
            return "No news articles found for the given query."
        
        string = []
        for article in articles:
            try:
                string.append('\n'.join([
                    f"Title: {article['title']}", 
                    f"Link: {article['url']}",
                    f"Description: {article.get('description','')}", 
                    f"Published: {article.get('publishedAt','')}",
                    f"Source: {article.get('source',{}).get('name','')}",
                    "\n-----------------"
                ]))
            except KeyError:
                continue
        
        result = '\n'.join(string)
        print(f"Returning {len(result)} characters of results")
        return result
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error making request: {str(e)}"
        print(error_msg)
        return error_msg
    except json.JSONDecodeError:
        error_msg = "Error: Invalid JSON response from news API"
        print(error_msg)
        return error_msg

# Expose a Tool instance compatible with CrewAI
search_news_tool = Tool(
    name="search_news",
    func=_search_news,
    description="Search for recent news articles from the last 7 days on a given topic",
    args_schema=NewsSearchInput,
    verbose=True,
)
