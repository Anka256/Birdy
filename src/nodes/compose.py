from langchain_ollama import ChatOllama
from src.state import AppState

MODEL_NAME = "qwen3:8b" 

def compose_response_node(state: AppState):
    print("--- Report Generating (Compose Node) ---")
    
    bird_name = state.get("common_name")
    sci_name = state.get("scientific_name")
    wiki_data = state.get("wiki_summary")
    
    if not bird_name:
        state["final_response"] = "Sorry, I could not identify the bird in the image/sound."
        return state

    context_text = wiki_data[:5000] if wiki_data else "No Wikipedia data available. Use your internal knowledge."

    prompt = f"""
    You are an expert ornithologist providing an objective, scientific summary.
    
    Bird: {bird_name} ({sci_name})
    Context from Wikipedia:
    {context_text}
    
    Task:
    Provide a concise, informative summary about this bird.
    Structure your response with these Markdown headings:
    ### 📝 Description
    (Physical appearance, size, distinct features)
    
    ### 🌍 Habitat & Distribution
    (Where they live, migration patterns)
    
    ### 🦗 Diet & Behavior
    (What they eat, interesting behaviors)
    
    ### 💡 Fun Fact
    (One short interesting fact)

    Keep the tone neutral and informative. Do not mention "Based on the text provided".
    """

    print(f"🤖 LLM ({MODEL_NAME}) running...")
    
    try:
        llm = ChatOllama(model=MODEL_NAME)
        response = llm.invoke(prompt)
        ai_summary = response.content
    except Exception as e:
        ai_summary = f"Error generating summary: {e}"

    state["final_response"] = ai_summary
    
    return state