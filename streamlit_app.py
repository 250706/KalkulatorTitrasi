import streamlit as st
import base64
import time
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# KONFIGURASI DAN BACKGROUND
# ---------------------------
st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")

def set_background_from_url(image_url: str, opacity: float = 0.85):
    background_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,{opacity}), rgba(255,255,255},{opacity})),
                    url('{image_url}');
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Background dari URL dengan gradien 85%
set_background_from_url("https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp", 0.85)

# ---------------------------
# DATA KONVERSI
# ---------------------------
konversi_data = {
    "massa": {
        "gram": 1,
        "kilogram": 1000,
        "miligram": 0.001,
        "pon": 453.592,
        "ons": 28.3495
    },
    "tekanan": {
        "Pa": 1,
        "kPa": 1000,
        "atm": 101325,
        "bar": 100000,
        "mmHg": 133.322
    },
    # Tambah kategori lainnya di sini
}

# ---------------------------
# FUNGSI KONVERSI
# ---------------------------
def konversi(nilai, satuan_asal, satuan_tujuan, kategori):
    faktor_asal = konversi_data[kategori][satuan_asal]
    faktor_tujuan = konversi_data[kategori][satuan_tujuan]
    hasil = nilai * (faktor_asal / faktor_tujuan)
    return hasil, faktor_asal, faktor_tujuan

# ---------------------------
# SIDEBAR DAN NAVIGASI
# ---------------------------
st.sidebar.title("📚 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["Beranda", "Kalkulator", "Grafik", "Tentang"])

# ---------------------------
# BERANDA
# ---------------------------
if halaman == "Beranda":
    st.title("👋 Selamat Datang di Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Aplikasi ini membantu Anda mengonversi berbagai satuan fisika lengkap dengan:
    - Penjelasan konversi
    - Grafik perbandingan
    - Salin hasil
    - Tampilan interaktif dan modern

    Gunakan menu **Kalkulator** di sidebar untuk memulai 🚀
    """)

# ---------------------------
# KALKULATOR
# ---------------------------
elif halaman == "Kalkulator":
    st.title("🧮 Kalkulator Konversi")

    kategori = st.selectbox("Pilih kategori", list(konversi_data.keys()))
    satuan_asal = st.selectbox("Dari satuan", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("Ke satuan", list(konversi_data[kategori].keys()))
    nilai_input = st.text_input("Masukkan nilai", "")

    if st.button("Konversi"):
        if nilai_input:
            try:
                nilai = float(nilai_input.replace(",", "."))
                with st.spinner("Menghitung konversi..."):
                    time.sleep(1.5)
                    hasil, faktor_asal, faktor_tujuan = konversi(nilai, satuan_asal, satuan_tujuan, kategori)
                    hasil_bulat = round(hasil, 6)

                    st.metric(label=f"{nilai} {satuan_asal} = ", value=f"{hasil_bulat} {satuan_tujuan}")

                    st.markdown("**📘 Penjelasan Perhitungan:**")
                    st.latex(r"Hasil = nilai \times \frac{faktor\_asal}{faktor\_tujuan}")
                    st.latex(fr"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_bulat}")

                    # Tabel semua hasil konversi ke satuan lain
                    df_hasil = pd.DataFrame({
                        "Satuan": list(konversi_data[kategori].keys()),
                        "Hasil": [round(nilai * (konversi_data[kategori][satuan_asal] / konversi_data[kategori][s]), 6)
                                  for s in konversi_data[kategori]]
                    })

                    st.markdown("### 📊 Tabel Hasil Konversi ke Semua Satuan:")
                    st.dataframe(df_hasil)

                    # Visualisasi Bar Chart
                    st.markdown("### 📈 Grafik Konversi:")
                    st.bar_chart(df_hasil.set_index("Satuan"))

            except ValueError:
                st.error("Masukkan angka yang valid.")
        else:
            st.warning("Masukkan nilai terlebih dahulu.")

# ---------------------------
# GRAFIK (Placeholder)
# ---------------------------
elif halaman == "Grafik":
    st.title("📈 Grafik Perbandingan")
    st.markdown("Silakan gunakan menu **Kalkulator** terlebih dahulu untuk melihat grafik hasil konversi.")

# ---------------------------
# TENTANG
# ---------------------------
elif halaman == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    **Kalkulator Konversi Satuan Fisika** dibuat untuk membantu pelajar, mahasiswa, dan profesional melakukan konversi satuan dengan mudah dan cepat.

    Dibuat dengan ❤️ menggunakan Streamlit.

    **Fitur:**
    - Konversi satuan lengkap
    - Penjelasan perhitungan
    - Grafik interaktif
    - Desain elegan dengan background custom
    """)
