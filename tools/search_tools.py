import json
import requests
import os
from dotenv import load_dotenv
from crewai.tools.agent_tools import Tool
from typing import Type
from pydantic.v1 import BaseModel, Field

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "b746d74bdeffe79b0f5e16792c6ee3bb4a12b5f9f4293f49c91b6481c913df60")

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(..., description="The search query for finding information on the internet")


def _search_internet(query: str) -> str:
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
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        return f"Error making search request: {e}"

    try:
        json_resp = response.json()
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from search API"

    # Check if the response was successful and contains the expected data
    if 'organic' not in json_resp:
        return "Error: Could not retrieve search results. Please check your Serper API key."

    results = json_resp['organic']
    print(f"Found {len(results)} search results")
    
    string = []
    for result in results[:top_result_to_return]:
        try:
            string.append('\n'.join([
                f"Title: {result.get('title','')}", f"Link: {result.get('link','')}",
                f"Snippet: {result.get('snippet','')}", "\n-----------------"
            ]))
        except KeyError:
            continue

    search_result = '\n'.join(string)
    print(f"Returning {len(search_result)} characters of search results")
    return search_result

# Expose Tool instance
search_tool = Tool(
    name="search_internet",
    func=_search_internet,
    description="Search the internet about a given topic and return relevant results",
    args_schema=SearchInput,
    verbose=True,
)

