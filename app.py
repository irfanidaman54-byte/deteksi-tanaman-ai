import streamlit as st
# 1. Konfigurasi Halaman (HARUS selalu di paling atas setelah import streamlit)
st.set_page_config(page_title="Dokter Tanaman AI", page_icon="🌿", layout="centered")
# --- Menambahkan Gambar Background ---
# Ganti URL di bawah dengan link gambar pilihan Anda
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://plus.unsplash.com/premium_photo-1672419013359-3e0a2f9c039a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Z2FtYmFyJTIwZGF1bnxlbnwwfHwwfHx8MA%3D%3D");
background-size: cover;
background-position: center;
}
[data-testid="stHeader"] {
background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# -------------------------------------
import google.generativeai as genai
from PIL import Image

# 2. Menyiapkan API Key dari brankas Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Memilih otak AI (Gemini Flash)
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. Tampilan Halaman Web
st.title("🌱 Pendeteksi Kesuburan Tanaman AI")
st.write("Unggah foto daun atau tanaman Anda, dan biarkan AI menganalisis kesehatannya!")

# 5. Menu Samping (Sidebar) untuk Pilihan Input
st.sidebar.write("### Pengaturan")
pilihan = st.sidebar.radio("Pilih metode masukan:", ("📷 Ambil Foto dari Kamera", "📂 Unggah dari Galeri"))

st.write("### Masukkan Foto Daun")

# Menyiapkan variabel kosong untuk menyimpan gambar
gambar_daun = None

if pilihan == "📷 Ambil Foto dari Kamera":
    gambar_daun = st.camera_input("Arahkan kamera ke daun yang jelas")
else:
    gambar_daun = st.file_uploader("Pilih file foto dari galeri Anda", type=['jpg', 'jpeg', 'png'])

# 6. Memproses Gambar dan Analisis AI
if gambar_daun is not None:
    # Membuka dan menampilkan gambar di layar
    image = Image.open(gambar_daun)
    st.image(image, caption="Foto Tanaman Anda", use_container_width=True)
    
    # Tombol Analisis
    if st.button("Analisis Sekarang"):
        # Animasi Loading
        with st.spinner("AI sedang mengamati daun dengan teliti... 🔍"):
            try:
                # Instruksi rahasia kita untuk AI (Prompting)
                instruksi = """
                Kamu adalah seorang ahli pertanian dan botani. 
                Tolong analisis foto tanaman ini. Beritahu saya:
                1. Apakah tanaman ini terlihat sehat?
                2. Apakah ada tanda-tanda kekurangan nutrisi, hama, atau penyakit?
                3. Berikan 3 saran perawatan praktis untuk tanaman ini.
                4. Berikan saran pupuk apa yang dibutuhkan tanaman ini.
                Gunakan bahasa Indonesia yang ramah dan mudah dipahami.
                """
                
                # Mengirim gambar dan instruksi ke AI
                response = model.generate_content([instruksi, image])
                
                # Menampilkan jawaban AI ke layar web dan memunculkan balon
                st.success("Analisis Selesai!")
                st.balloons()
                st.write(response.text)
                
            except Exception as e:
                # Jika ada error (misal internet putus atau API key bermasalah)
                st.error(f"Terjadi kesalahan teknis: {e}")












