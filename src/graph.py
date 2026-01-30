from langgraph.graph import StateGraph, START, END
from src.state import AppState

# --- NODE IMPORTLARI ---
from src.nodes.identification import (
    identify_bird_with_text_node, 
    identify_bird_with_photo_node, 
    identify_bird_with_sound_node
)
from src.nodes.retrieval import (
    find_bird_info_node, 
    find_bird_photos_node, 
    find_bird_sounds_node
)
from src.nodes.compose import compose_response_node

def decide_any_media_node(state: AppState):
    return state

def route_based_on_media_node(state: AppState):
    return state["input_type"]


graph = StateGraph(AppState)

graph.add_node("Decide Any Media", decide_any_media_node)

# Identification Nodes
graph.add_node("Identify Bird with Text", identify_bird_with_text_node)
graph.add_node("Identify Bird with Photo", identify_bird_with_photo_node)
graph.add_node("Identify Bird with Sound", identify_bird_with_sound_node)

# Retrieval Nodes
graph.add_node("Find Bird Info", find_bird_info_node)
graph.add_node("Find Bird Photos", find_bird_photos_node)
graph.add_node("Find Bird Sounds", find_bird_sounds_node)

# Compose Node
graph.add_node("Compose", compose_response_node)

graph.add_edge(START, "Decide Any Media")

graph.add_conditional_edges(
    "Decide Any Media",
    route_based_on_media_node,
    {
        "photo": "Identify Bird with Photo",
        "sound": "Identify Bird with Sound",
        "text": "Identify Bird with Text",
    },
)

graph.add_edge("Identify Bird with Text", "Find Bird Info")
graph.add_edge("Identify Bird with Text", "Find Bird Photos")
graph.add_edge("Identify Bird with Text", "Find Bird Sounds")

graph.add_edge("Identify Bird with Photo", "Find Bird Info")
graph.add_edge("Identify Bird with Photo", "Find Bird Photos")
graph.add_edge("Identify Bird with Photo", "Find Bird Sounds")
graph.add_edge("Identify Bird with Sound", "Find Bird Info")
graph.add_edge("Identify Bird with Sound", "Find Bird Photos")
graph.add_edge("Identify Bird with Sound", "Find Bird Sounds")

graph.add_edge("Find Bird Info", "Compose")
graph.add_edge("Find Bird Photos", "Compose")
graph.add_edge("Find Bird Sounds", "Compose")

graph.add_edge("Compose", END)

app = graph.compile()