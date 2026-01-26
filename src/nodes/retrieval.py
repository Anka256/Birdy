from src.state import AppState
from src.tools.wiki_search import get_wiki_data

def find_bird_info_node(state: AppState):
    query = state.get("scientific_name")
    
    wiki_text = None
    
    if query:
        wiki_text = get_wiki_data(query)
    
    if not wiki_text and state.get("common_name"):
        fallback_query = state.get("common_name")
        wiki_text = get_wiki_data(fallback_query)
    
    if wiki_text:
        state["wiki_summary"] = wiki_text
    else:
        state["wiki_summary"] = None
        
    return state