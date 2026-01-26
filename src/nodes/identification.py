from tavily import TavilyClient
from dotenv import load_dotenv
import os
import re
from src.state import AppState

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def extract_scientific_name(response):
    results = response.get("results", [])
    if not results:
        return None
    
    results = sorted(results, key=lambda r: r.get("score", 0), reverse=True)

    for r in results:
        content = r.get("content", "")
        match = re.search(r"\b[A-Z][a-z]+ [a-z]{2,}\b", content)
        if match:
            return match.group()
    return None

def identify_bird_with_text_node(state: AppState):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    query = state["user_query"] + " scientific name"
    response = tavily_client.search(query=query)
    state["scientific_name"] = extract_scientific_name(response) or "Scientific name not found"
    return State
