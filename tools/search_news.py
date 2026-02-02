import json
import requests
import urllib.parse
from datetime import datetime, timedelta, timezone
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Hardcode the Serper API key as requested
SERP_API_KEY = "b746d74bdeffe79b0f5e16792c6ee3bb4a12b5f9f4293f49c91b6481c913df60"
GNEWS_API_KEY = "67b00b586b42fb594924a68f79458260"

class NewsSearchInput(BaseModel):
    """Input schema for news search tool."""
    query: str = Field(..., description="The search query for finding news articles")

class SearchNews(BaseTool):
    name: str = "search_news"
    description: str = "Search for recent news articles from the last 7 days on a given topic"
    args_schema: Type[BaseModel] = NewsSearchInput

    def _run(self, query: str) -> str:
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
                        f"Description: {article['description']}", 
                        f"Published: {article['publishedAt']}",
                        f"Source: {article['source']['name']}",
                        "\n-----------------"
                    ]))
                except KeyError as e:
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
