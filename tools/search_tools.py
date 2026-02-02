import json
import requests
import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(..., description="The search query for finding information on the internet")

class SearchTools(BaseTool):
    name: str = "search_internet"
    description: str = "Search the internet about a given topic and return relevant results"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        """Execute the internet search and return relevant results."""
        print(f"🌐 SearchTools called with query: '{query}'")
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'content-type': 'application/json'
        }
        print(f"Making search request to URL: {url} with query: {query}")
        response = requests.request("POST", url, headers=headers, data=payload)
        
        # Check if the response was successful and contains the expected data
        if 'organic' not in response.json():
            return "Error: Could not retrieve search results. Please check your Serper API key."

        results = response.json()['organic']
        print(f"Found {len(results)} search results")
        
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                continue

        search_result = '\n'.join(string)
        print(f"Returning {len(search_result)} characters of search results")
        return search_result

