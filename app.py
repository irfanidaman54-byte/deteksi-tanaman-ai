import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Menyiapkan API Key (Ganti dengan kunci Anda sendiri!)
API_KEY = "AIzaSyDARG-4lWbj0KYi9ED7ZnkYchSxsRUG-cg"
genai.configure(api_key=API_KEY)

# 2. Memilih otak AI (Gemini 2.5 flash sangat cepat untuk gambar)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Tampilan Halaman Web
st.title("🌱 Pendeteksi Kesuburan Tanaman AI")
st.write("Unggah foto daun atau tanaman Anda, dan biarkan AI menganalisis kesehatannya!")

# Tempat upload foto
uploaded_file = st.file_uploader("Upload Foto Tanaman (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Buka gambar yang diunggah
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Tanaman Anda", use_container_width=True)
    
    # Tombol Analisis
    if st.button("Analisis dengan AI"):
        # Munculkan animasi loading saat AI berpikir
        with st.spinner("AI sedang mengamati tanaman Anda... 🧠"):
            try:
                # Ini adalah instruksi rahasia kita untuk AI (Prompting)
                instruksi = """
                Kamu adalah seorang ahli pertanian dan botani. 
                Tolong analisis foto tanaman ini. Beritahu saya:
                1. Apakah tanaman ini terlihat sehat?
                2. Apakah ada tanda-tanda kekurangan nutrisi, hama, atau penyakit?
                3. Berikan 3 saran perawatan praktis untuk tanaman ini.
                Gunakan bahasa Indonesia yang ramah dan mudah dipahami.
                """
                
                # Mengirim gambar dan instruksi ke AI
                response = model.generate_content([instruksi, image])
                
                # Menampilkan jawaban AI ke layar web
                st.success("Analisis Selesai!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")