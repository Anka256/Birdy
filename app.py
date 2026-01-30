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
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E86C1;
        color: white;
        height: 3em;
        font-weight: bold;
    }
    .block-container {
        padding-top: 2rem;
    }
    .info-text-container {
        font-size: 1.15rem !important;
        line-height: 1.6;
    }
    .info-text-container h1, .info-text-container h2, .info-text-container h3 {
        color: #2E86C1;
    }
    .stMarkdown p {
        font-size: 1.15rem;
    }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.markdown('<div class="main-title">🐦 Birdy AI</div>', unsafe_allow_html=True)

col_query, col_upload = st.columns([3, 1])

with col_query:
    user_text_query = st.text_input(
        "Enter your query about a bird (or leave empty if uploading)",
        placeholder="e.g. What bird is this? or 'Stork'"
    )

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload File (Photo/Audio)",
        type=["jpg", "jpeg", "png", "mp3", "wav", "ogg"]
    )

user_input_path = None
input_type = "text"

if uploaded_file is not None:
    user_input_path = os.path.join("temp", uploaded_file.name)
    with open(user_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext in [".jpg", ".jpeg", ".png"]:
        input_type = "photo"
    elif ext in [".mp3", ".wav", ".ogg"]:
        input_type = "sound"
elif user_text_query:
    input_type = "text"
else:
    input_type = None

start_analysis = st.button("Analyze 🦜")

if start_analysis:
    if not input_type:
        st.warning("Please enter text or upload a file.")
    else:
        with st.spinner('Birdy is thinking... AI agents are working... 🤖'):
            try:
                initial_state = {
                    "messages": [],
                    "input_type": input_type,
                    "media_path": user_input_path if user_input_path else None,
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

                col_media, col_info = st.columns([1, 2])

                with col_media:
                    if input_type == "sound" and user_input_path:
                        st.subheader("Uploaded Audio")
                        st.audio(user_input_path)
                        st.divider()

                    audios = result.get("bird_audio_urls", [])
                    if audios:
                        st.subheader("Reference Audio")
                        for audio_url in audios:
                            st.audio(audio_url)
                    elif input_type != "sound":
                        st.info("No audio recordings found.")

                with col_info:
                    st.markdown('<div class="info-text-container">', unsafe_allow_html=True)

                    if result.get("common_name"):
                        st.markdown(f"# {result['common_name']}")
                        if result.get("scientific_name"):
                            st.markdown(
                                f"**Scientific Name:** *{result.get('scientific_name')}*"
                            )

                    st.divider()

                    if result.get("final_response"):
                        st.markdown(result["final_response"])
                    else:
                        st.write("No detailed information available.")

                    st.markdown('</div>', unsafe_allow_html=True)

                st.divider()
                st.subheader("Gallery")

                bird_images = result.get("bird_images", [])

                if input_type == "photo" and user_input_path:
                    cols = st.columns(3)
                    with cols[0]:
                        st.image(
                            user_input_path,
                            caption="Uploaded Photo",
                            use_container_width=True
                        )

                if bird_images:
                    num_cols = 3
                    cols = st.columns(num_cols)
                    for i, img_url in enumerate(bird_images):
                        with cols[i % num_cols]:
                            st.image(img_url, use_container_width=True)
                elif input_type != "photo":
                    st.write("No images found.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
