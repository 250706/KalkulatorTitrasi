import streamlit as st
import pandas as pd
import time
import pyperclip
import altair as alt

# ---------------------- SETUP LATAR BELAKANG ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url('{image_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://images.unsplash.com/photo-1528892952291-009c663ce843")

# ---------------------- DATA KONVERSI ----------------------
konversi_data = {
    "🌡️ Suhu": {
        "satuan": ["Celsius", "Fahrenheit", "Kelvin"]
    },
    "💨 Tekanan": {
        "satuan": ["atm", "Pa", "bar", "mmHg"],
        "faktor": {"atm": 101325, "Pa": 1, "bar": 100000, "mmHg": 133.322}
    },
    "⚖️ Massa": {
        "satuan": ["kg", "g", "mg", "lb"],
        "faktor": {"kg": 1000, "g": 1, "mg": 0.001, "lb": 453.592}
    },
    "📏 Panjang": {
        "satuan": ["m", "cm", "mm", "inch", "ft"],
        "faktor": {"m": 100, "cm": 1, "mm": 0.1, "inch": 2.54, "ft": 30.48}
    },
    "⏱️ Waktu": {
        "satuan": ["detik", "menit", "jam", "hari"],
        "faktor": {"detik": 1, "menit": 60, "jam": 3600, "hari": 86400}
    },
    "🔋 Energi": {
        "satuan": ["Joule", "kJ", "cal", "kcal"],
        "faktor": {"Joule": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184}
    },
    "🚗 Kecepatan": {
        "satuan": ["m/s", "km/h", "mph"],
        "faktor": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704}
    },
    "⚡ Daya": {
        "satuan": ["Watt", "kW", "hp"],
        "faktor": {"Watt": 1, "kW": 1000, "hp": 745.7}
    },
    "🧪 Volume": {
        "satuan": ["L", "mL", "cm³", "m³"],
        "faktor": {"L": 1000, "mL": 1, "cm³": 1, "m³": 1_000_000}
    },
    "🎵 Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz"],
        "faktor": {"Hz": 1, "kHz": 1000, "MHz": 1_000_000}
    },
    "🔌 Hambatan Listrik": {
        "satuan": ["Ohm", "kOhm", "MOhm"],
        "faktor": {"Ohm": 1, "kOhm": 1000, "MOhm": 1_000_000}
    },
    "🔋 Tegangan": {
        "satuan": ["Volt", "mV", "kV"],
        "faktor": {"Volt": 1, "mV": 0.001, "kV": 1000}
    },
    "💡 Arus": {
        "satuan": ["Ampere", "mA", "kA"],
        "faktor": {"Ampere": 1, "mA": 0.001, "kA": 1000}
    },
}

# ---------------------- KONVERSI SUHU ----------------------
def konversi_suhu(nilai, satuan_asal, satuan_tujuan):
    if satuan_asal == satuan_tujuan:
        return nilai
    if satuan_asal == "Celsius":
        if satuan_tujuan == "Fahrenheit":
            return (nilai * 9/5) + 32
        elif satuan_tujuan == "Kelvin":
            return nilai + 273.15
    elif satuan_asal == "Fahrenheit":
        if satuan_tujuan == "Celsius":
            return (nilai - 32) * 5/9
        elif satuan_tujuan == "Kelvin":
            return (nilai - 32) * 5/9 + 273.15
    elif satuan_asal == "Kelvin":
        if satuan_tujuan == "Celsius":
            return nilai - 273.15
        elif satuan_tujuan == "Fahrenheit":
            return (nilai - 273.15) * 9/5 + 32

# ---------------------- FUNGSI PENJELASAN ----------------------
def tampilkan_penjelasan(kategori, satuan_asal, satuan_tujuan, nilai, hasil):
    if "Suhu" in kategori:
        rumus = {
            ("Celsius", "Fahrenheit"): "`F = (C × 9/5) + 32`",
            ("Celsius", "Kelvin"): "`K = C + 273.15`",
            ("Fahrenheit", "Celsius"): "`C = (F - 32) × 5/9`",
            ("Fahrenheit", "Kelvin"): "`K = (F - 32) × 5/9 + 273.15`",
            ("Kelvin", "Celsius"): "`C = K - 273.15`",
            ("Kelvin", "Fahrenheit"): "`F = (K - 273.15) × 9/5 + 32`"
        }.get((satuan_asal, satuan_tujuan), "Rumus tidak tersedia")

        st.markdown(f"""
### 📘 Penjelasan Konversi Suhu

Anda mengonversi **{nilai} {satuan_asal}** menjadi **{hasil:.2f} {satuan_tujuan}**.

#### Rumus yang digunakan:
{rumus}

Rumus ini merupakan standar internasional dan digunakan di berbagai bidang seperti kimia, fisika, dan teknik.
        """)
    else:
        st.markdown(f"""
### 📘 Penjelasan Konversi {kategori.replace('⚡','').replace('💨','').replace('🔌','').replace('🔋','')}

Anda mengonversi **{nilai} {satuan_asal}** menjadi **{hasil:.4g} {satuan_tujuan}**.

#### Rumus:
\\[
\\text{{Hasil}} = \\frac{{\\text{{Nilai}} \\times \\text{{Faktor Asal}}}}{{\\text{{Faktor Tujuan}}}}
\\]

Metode ini mengikuti sistem satuan internasional (SI Units), digunakan dalam studi teknik dan ilmiah.

        """)

# ---------------------- HALAMAN ----------------------
st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")

menu = st.sidebar.radio("Navigasi", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

if menu == "🏠 Beranda":
    st.markdown("""
    <h1 style="text-align: center;">⚙️ Kalkulator Konversi Satuan Fisika</h1>
    <p style="text-align: center; font-size:18px;">
    Selamat datang! Aplikasi ini membantu Anda mengonversi berbagai satuan fisika 
    seperti suhu, tekanan, massa, energi, daya, dan banyak lagi — lengkap dengan grafik dan penjelasan rumus.
    </p>
    <br>
    <ul>
      <li>Mudah digunakan untuk pelajar & profesional</li>
      <li>Visualisasi hasil dengan grafik</li>
      <li>Penjelasan rumus dan hasil konversi</li>
    </ul>
    <br><br>
    """, unsafe_allow_html=True)

elif menu == "📐 Kalkulator":
    st.header("📐 Kalkulator Konversi")

    kategori = st.selectbox("Pilih Kategori Satuan", list(konversi_data.keys()))
    satuan_list = konversi_data[kategori]["satuan"]
    satuan_asal = st.selectbox("Dari Satuan", satuan_list)
    satuan_tujuan = st.selectbox("Ke Satuan", satuan_list)
    nilai = st.number_input("Masukkan Nilai", value=0.0)

    if st.button("🔄 Konversi"):
        with st.spinner("Menghitung..."):
            time.sleep(1.5)

            if "Suhu" in kategori:
                hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
            else:
                faktor = konversi_data[kategori]["faktor"]
                hasil = nilai * faktor[satuan_asal] / faktor[satuan_tujuan]

            st.metric(label=f"Hasil Konversi ke {satuan_tujuan}", value=f"{hasil:.4g} {satuan_tujuan}")
            st.button("📋 Salin Hasil", on_click=lambda: pyperclip.copy(f"{hasil:.4g} {satuan_tujuan}"))

            tampilkan_penjelasan(kategori, satuan_asal, satuan_tujuan, nilai, hasil)

elif menu == "📊 Grafik":
    st.header("📊 Grafik Perbandingan Nilai")

    st.info("Silakan lakukan konversi terlebih dahulu di halaman Kalkulator, lalu kembali ke sini untuk melihat grafik perbandingan.")

elif menu == "ℹ️ Tentang":
    st.markdown("""
    ## ℹ️ Tentang Aplikasi

    **Kalkulator Konversi Satuan Fisika** ini dikembangkan untuk memudahkan pengguna dalam melakukan konversi satuan secara cepat dan akurat.

    ### 📚 Referensi:

    - NIST (National Institute of Standards and Technology):  
      https://physics.nist.gov/cuu/Units/index.html

    - International Bureau of Weights and Measures (BIPM):  
      https://www.bipm.org/en/measurement-units/

    - The Engineering Toolbox:  
      https://www.engineeringtoolbox.com/

    ### 🛠 Teknologi:
    - Python
    - Streamlit
    - Altair
    - Pandas

    Dibuat dengan ❤️ untuk pendidikan dan profesionalisme.
    """)
