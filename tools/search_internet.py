import json
import requests
import os
from dotenv import load_dotenv
from crewai.tools.agent_tools import Tool
from typing import Type
from pydantic.v1 import BaseModel, Field

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable not set. Please add it to your .env file.")

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(..., description="The search query for finding information on the internet")


def _search_internet(query: str) -> str:
    """Execute the internet search and return relevant results."""
    print(f"🌐 SearchInternet called with query: '{query}'")
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

    # Check HTTP status code
    if response.status_code != 200:
        print(f"Search API returned status code {response.status_code}")
        if response.status_code == 403:
            return "Error: Access forbidden (403). Please verify your Serper API key is valid and has available credits."
        elif response.status_code == 401:
            return "Error: Unauthorized (401). Your Serper API key is invalid."
        else:
            return f"Error: Search API returned status code {response.status_code}"

    try:
        json_resp = response.json()
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from search API"

    # Check if the response was successful and contains the expected data
    if 'organic' not in json_resp:
        return "Error: Could not retrieve search results. Response may be incomplete."

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
search_internet_tool = Tool(
    name="search_internet",
    func=_search_internet,
    description="Search the internet about a given topic and return relevant results",
    args_schema=SearchInput,
    verbose=True,
)

