import streamlit as st
import os
import shutil
from src.graph import app
from PIL import Image

st.set_page_config(
    page_title="Birdy - AI Bird Watcher",
    page_icon="🐦",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        color: #2E86C1;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        color: #555;
        text_align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.markdown('<div class="main-title">🐦 Birdy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Bird Identification and Information System</div>', unsafe_allow_html=True)

st.sidebar.header("🔍 Input Method")
input_method = st.sidebar.radio(
    "How would you like to search?",
    ("Upload Photo 📸", "Upload Audio 🎤", "Enter Text ✍️")
)

user_input_path = None
user_text_query = ""
input_type = ""
start_analysis = False

if input_method == "Upload Photo 📸":
    input_type = "photo"
    uploaded_file = st.sidebar.file_uploader("Upload a bird photo...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        user_input_path = os.path.join("temp", uploaded_file.name)
        with open(user_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.sidebar.image(uploaded_file, caption="Uploaded Photo", use_container_width=True)
        start_analysis = st.sidebar.button("Analyze")

elif input_method == "Upload Audio 🎤":
    input_type = "sound"
    uploaded_file = st.sidebar.file_uploader("Upload a bird sound...", type=["mp3", "wav", "ogg"])
    
    if uploaded_file is not None:
        user_input_path = os.path.join("temp", uploaded_file.name)
        with open(user_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.sidebar.audio(uploaded_file)
        start_analysis = st.sidebar.button("Analyze")

elif input_method == "Enter Text ✍️":
    input_type = "text"
    user_text_query = st.sidebar.text_input("Enter bird name (e.g., Stork)")
    if user_text_query:
        start_analysis = st.sidebar.button("Search")

if start_analysis:
    with st.spinner('Birdy is thinking... AI agents are working... 🤖'):
        try:
            initial_state = {
                "messages": [],
                "input_type": input_type,
                "media_path": user_input_path,
                "user_query": user_text_query,
                "scientific_name": None,
                "common_name": None,
                "wiki_summary": None,
                "bird_images": [],
                "bird_audio_urls": [],
                "final_response": ""
            }

            result = app.invoke(initial_state)
            
            st.divider()
            
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.subheader("🖼️ Image")
                
                if input_type == "photo" and user_input_path:
                    st.image(user_input_path, caption="Uploaded by You", use_container_width=True)
                
                if result.get("bird_images"):
                    st.info(f"Found {len(result['bird_images'])} photos from iNaturalist.")
                    st.image(result["bird_images"][0], caption=f"{result.get('common_name')} (Reference)", use_container_width=True)
                    
                    with st.expander("View Other Photos"):
                        for img_url in result["bird_images"][1:]:
                            st.image(img_url, use_container_width=True)
                else:
                    if input_type != "photo":
                        st.warning("No images found.")

            with col_right:
                if result.get("common_name"):
                    st.title(result["common_name"])
                    st.markdown(f"*{result.get('scientific_name')}*")
                else:
                    st.title("Result")
                
                st.divider()
                
                st.markdown(result["final_response"])
                
                st.divider()
                st.subheader("🎵 Audio Recordings (Xeno-canto)")
                audios = result.get("bird_audio_urls", [])
                
                if audios:
                    for i, audio_url in enumerate(audios, 1):
                        st.write(f"**Sample {i}**")
                        st.audio(audio_url)
                else:
                    st.write("_No audio recordings found._")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Please check system logs.")