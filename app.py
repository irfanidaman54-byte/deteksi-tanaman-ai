import streamlit as st
st.set_page_config(page_title="Dokter Tanaman AI", page_icon="🌿", layout="centered")

import google.generativeai as genai
from PIL import Image
from streamlit_back_camera_input import back_camera_input

# 1. Konfigurasi API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Tampilan Halaman Web
st.title("🌱 Pendeteksi Kesuburan Tanaman AI")
st.write("Unggah foto daun atau tanaman Anda, dan biarkan AI menganalisis kesehatannya!")

# --- 3. SISTEM MEMORI UNTUK MENGHEMAT LAYAR ---
# Membuat kotak memori kosong jika belum ada
if "foto_tersimpan" not in st.session_state:
    st.session_state.foto_tersimpan = None

# KONDISI A: JIKA BELUM ADA FOTO DI MEMORI (Tampilkan Kamera/Galeri)
if st.session_state.foto_tersimpan is None:
    st.sidebar.write("### Pengaturan")
    pilihan = st.sidebar.radio("Pilih metode masukan:", ("📷 Ambil Foto dari Kamera", "📂 Unggah dari Galeri"))

    st.write("### Masukkan Foto Daun")
    if pilihan == "📷 Ambil Foto dari Kamera":
        st.info("💡 Arahkan ke daun, lalu **KETUK AREA VIDEO** untuk memotret!")
        gambar_baru = back_camera_input()
        
        # Jika foto berhasil diketuk/diambil, simpan ke memori lalu restart halaman
        if gambar_baru is not None:
            st.session_state.foto_tersimpan = gambar_baru
            st.rerun() 
            
    else:
        gambar_baru = st.file_uploader("Pilih file foto dari galeri Anda", type=['jpg', 'jpeg', 'png'])
        if gambar_baru is not None:
            st.session_state.foto_tersimpan = gambar_baru
            st.rerun()

# KONDISI B: JIKA FOTO SUDAH ADA DI MEMORI (Sembunyikan Kamera, Tampilkan Hasil)
else:
    # Memanggil foto dari memori
    gambar_daun = st.session_state.foto_tersimpan
    image = Image.open(gambar_daun)
    st.image(image, caption="Foto Tanaman Anda", use_container_width=True)

    # Tombol praktis jika foto buram dan ingin diulang
    if st.button("❌ Ganti Foto"):
        st.session_state.foto_tersimpan = None # Kosongkan memori
        st.rerun() # Restart halaman untuk memunculkan kamera lagi

    # --- 4. Proses Analisis AI ---
    if st.button("Analisis Sekarang"):
        with st.spinner("AI sedang mengamati daun dengan teliti... 🔍"):
            try:
                instruksi = """
                Kamu adalah seorang ahli pertanian dan botani. 
                Tolong analisis foto tanaman ini. Beritahu saya:
                1. Apakah tanaman ini terlihat sehat?
                2. Apakah ada tanda-tanda kekurangan nutrisi, hama, atau penyakit?
                3. Berikan 3 saran perawatan praktis untuk tanaman ini.
                4. Berikan saran pupuk apa yang dibutuhkan tanaman ini.
                Gunakan bahasa Indonesia yang ramah dan mudah dipahami.
                """
                
                response = model.generate_content([instruksi, image])
                
                st.success("Analisis Selesai!")
                st.balloons()
                st.write(response.text)
                
                # Tombol Kembali / Cek Tanaman Lain
                st.write("---") 
                if st.button("🔄 Cek Tanaman Lain"):
                    st.session_state.foto_tersimpan = None # Kosongkan memori
                    st.rerun() 
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
