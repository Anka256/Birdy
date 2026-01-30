import streamlit as st
import os
import shutil
from src.graph import app  # Graph'ın derlenmiş halini (app = graph.compile()) çağırmalıyız
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Birdy - AI Kuş Gözlemcisi",
    page_icon="🐦",
    layout="wide"
)

# --- CSS İLE GÖRSELLİK (Opsiyonel) ---
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

# --- TEMP KLASÖR KONTROLÜ ---
if not os.path.exists("temp"):
    os.makedirs("temp")

# --- BAŞLIK ---
st.markdown('<div class="main-title">🐦 Birdy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Yapay Zeka Destekli Kuş Tanımlama ve Bilgi Sistemi</div>', unsafe_allow_html=True)

# --- SIDEBAR (GİRİŞ YÖNTEMİ SEÇİMİ) ---
st.sidebar.header("🔍 Giriş Yöntemi")
input_method = st.sidebar.radio(
    "Nasıl arama yapmak istersiniz?",
    ("Fotoğraf Yükle 📸", "Ses Yükle 🎤", "Metin Gir ✍️")
)

# State Hazırlığı için değişkenler
user_input_path = None
user_text_query = ""
input_type = ""

# --- GİRİŞ ALANLARI ---
start_analysis = False

if input_method == "Fotoğraf Yükle 📸":
    input_type = "photo"
    uploaded_file = st.sidebar.file_uploader("Kuş fotoğrafı yükleyin...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Dosyayı temp'e kaydet
        user_input_path = os.path.join("temp", uploaded_file.name)
        with open(user_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Önizleme
        st.sidebar.image(uploaded_file, caption="Yüklenen Fotoğraf", use_container_width=True)
        start_analysis = st.sidebar.button("Analiz Et")

elif input_method == "Ses Yükle 🎤":
    input_type = "sound"
    uploaded_file = st.sidebar.file_uploader("Kuş sesi yükleyin...", type=["mp3", "wav", "ogg"])
    
    if uploaded_file is not None:
        # Dosyayı temp'e kaydet
        user_input_path = os.path.join("temp", uploaded_file.name)
        with open(user_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Önizleme
        st.sidebar.audio(uploaded_file)
        start_analysis = st.sidebar.button("Analiz Et")

elif input_method == "Metin Gir ✍️":
    input_type = "text"
    user_text_query = st.sidebar.text_input("Kuşun adını yazın (Örn: Leylek)")
    if user_text_query:
        start_analysis = st.sidebar.button("Araştır")

# --- ANA İŞLEM AKIŞI ---
if start_analysis:
    with st.spinner('Birdy düşünüyor... Yapay zeka ajanları çalışıyor... 🤖'):
        try:
            # Graph için başlangıç State'i
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

            # --- GRAPH ÇALIŞTIRMA ---
            # LangGraph invoke komutu
            result = app.invoke(initial_state)
            
            # --- SONUÇLARI GÖSTERME (2 SÜTUNLU YAPI) ---
            st.divider()
            
            # Kolonları ayarla: Sol (Görsel - Dar), Sağ (Bilgi - Geniş)
            col_left, col_right = st.columns([1, 2])
            
            # SOL KOLON: FOTOĞRAF
            with col_left:
                st.subheader("🖼️ Görüntü")
                
                # 1. Eğer kullanıcı fotoğraf yüklediyse onu göster
                if input_type == "photo" and user_input_path:
                    st.image(user_input_path, caption="Sizin Yüklediğiniz", use_container_width=True)
                
                # 2. iNaturalist'ten gelen fotoğrafları göster (Carousel veya tekli)
                if result.get("bird_images"):
                    st.info(f"iNaturalist'ten {len(result['bird_images'])} fotoğraf bulundu.")
                    # İlk fotoğrafı büyük göster
                    st.image(result["bird_images"][0], caption=f"{result.get('common_name')} (Referans)", use_container_width=True)
                    
                    # Diğer fotoları expander içinde göster
                    with st.expander("Diğer Fotoğrafları Gör"):
                        for img_url in result["bird_images"][1:]:
                            st.image(img_url, use_container_width=True)
                else:
                    if input_type != "photo":
                        st.warning("Görsel bulunamadı.")

            # SAĞ KOLON: BİLGİ VE SES
            with col_right:
                # Başlıklar
                if result.get("common_name"):
                    st.title(result["common_name"])
                    st.markdown(f"*{result.get('scientific_name')}*")
                else:
                    st.title("Sonuç")
                
                st.divider()
                
                # Qwen'in hazırladığı metin (Markdown)
                # Not: Compose node'un sonuna eklediği linkleri burada da görücez, 
                # ama aşağıda native player eklediğimiz için sorun yok.
                st.markdown(result["final_response"])
                
                st.divider()
                st.subheader("🎵 Ses Kayıtları (Xeno-canto)")
                
                # Xeno-canto sesleri için Native Player
                audios = result.get("bird_audio_urls", [])
                if audios:
                    for i, audio_url in enumerate(audios, 1):
                        st.write(f"**Örnek {i}**")
                        st.audio(audio_url)
                else:
                    st.write("_Ses kaydı bulunamadı._")

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            st.write("Lütfen sistem loglarını kontrol edin.")