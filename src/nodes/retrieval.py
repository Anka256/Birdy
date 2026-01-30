from src.state import AppState
from src.tools.wiki_search import get_wiki_data
from src.tools.inaturalist import get_bird_photos_from_inaturalist
from src.tools.xenocanto import get_bird_sounds_from_xenocanto

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


def find_bird_photos_node(state: AppState):
    query = state.get("scientific_name")
    
    target_name = query if query else state.get("common_name")
    
    print(f"--- iNaturalist Photos Searching: {target_name} ---")
    
    if target_name:
        photos = get_bird_photos_from_inaturalist(target_name, limit=5)
        state["bird_images"] = photos
        print(f"📸 {len(photos)} photos found.")
    else:
        state["bird_images"] = []
        print("❌fetching No name found, cannot search for photos.")
        
    return state



def find_bird_sounds_node(state: AppState):
    query = state.get("scientific_name")
    
    target_name = query if query else state.get("common_name")
    
    print(f"--- Xeno-canto Sound Searching: {target_name} ---")
    
    if target_name:
        sounds = get_bird_sounds_from_xenocanto(target_name, limit=3)
        state["bird_audio_urls"] = sounds
        print(f"🎵 {len(sounds)} sounds found.")
    else:
        state["bird_audio_urls"] = []
        print("❌ No name found, cannot search for sounds.")
        
    return state