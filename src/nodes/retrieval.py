from src.state import AppState
from src.tools.wiki_search import get_wiki_data
from src.tools.inaturalist import get_bird_photos_from_inaturalist
from src.tools.xenocanto import get_bird_sounds_from_xenocanto

def find_bird_info_node(state: AppState):
    query = state.get("scientific_name")
    print(f"--- Wikipedia Search: {query} ---")
    
    wiki_text = None
    if query:
        wiki_text = get_wiki_data(query)
    
    if not wiki_text and state.get("common_name"):
        fallback_query = state.get("common_name")
        print(f"⚠️ Scientific name not found, trying common name: {fallback_query}")
        wiki_text = get_wiki_data(fallback_query)
    
    return {"wiki_summary": wiki_text if wiki_text else None}

def find_bird_photos_node(state: AppState):
    query = state.get("scientific_name")
    target_name = query if query else state.get("common_name")
    
    print(f"--- iNaturalist Photos Searching: {target_name} ---")
    
    photos = []
    if target_name:
        photos = get_bird_photos_from_inaturalist(target_name, limit=5)
        
    return {"bird_images": photos}

def find_bird_sounds_node(state: AppState):
    query = state.get("scientific_name")
    target_name = query if query else state.get("common_name")
    
    print(f"--- Xeno-canto Sounds Searching: {target_name} ---")
    
    sounds = []
    if target_name:
        sounds = get_bird_sounds_from_xenocanto(target_name, limit=3)
        
    return {"bird_audio_urls": sounds}