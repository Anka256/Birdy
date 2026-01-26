from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages

class AppState(TypedDict):
    messages: Annotated[List[dict], add_messages]
    
    input_type: str
    media_path: Optional[str]
    user_query: str

    scientific_name: Optional[str]
    common_name: Optional[str]

    wiki_summary: Optional[str]
    bird_images: Optional[List[str]]
    bird_audio_urls: Optional[List[str]]

    final_response: str
