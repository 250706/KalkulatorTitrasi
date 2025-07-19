import streamlit as st
import pandas as pd
import time
import altair as alt

# ---------------------- LATAR BELAKANG ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, {opacity});
            padding: 2rem;
            border-radius: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://storage.googleapis.com/streamlit-static-assets/4eac359b-ce1e-4967-9ad9-8f98db7428d4.png")

# ---------------------- DATA KONVERSI ----------------------
konversi_data = {
    "🔥 Suhu": {
        "Celsius": 1,
        "Fahrenheit": 1,
        "Kelvin": 1,
    },
    "💨 Tekanan": {
        "Pascal": 1,
        "Bar": 100000,
        "Atmosfer": 101325,
        "mmHg": 133.322,
    },
    "⚖️ Massa": {
        "Gram": 1,
        "Kilogram": 1000,
        "Miligram": 0.001,
        "Ton": 1_000_000,
    },
    "📏 Panjang": {
        "Meter": 1,
        "Kilometer": 1000,
        "Sentimeter": 0.01,
        "Milimeter": 0.001,
        "Inci": 0.0254,
        "Kaki": 0.3048,
    },
    "⏱️ Waktu": {
        "Detik": 1,
        "Menit": 60,
        "Jam": 3600,
        "Hari": 86400,
    },
    "🔋 Energi": {
        "Joule": 1,
        "Kalori": 4.184,
        "Kilojoule": 1000,
        "kWh": 3_600_000,
    },
    "🚗 Kecepatan": {
        "m/s": 1,
        "km/jam": 1000 / 3600,
        "mil/jam": 0.44704,
    },
    "⚡ Daya": {
        "Watt": 1,
        "Kilowatt": 1000,
        "HP (Horsepower)": 745.7,
    },
    "🧪 Volume": {
        "Liter": 1,
        "Mililiter": 0.001,
        "Meter Kubik": 1000,
        "cm³": 0.001,
    },
    "🔁 Frekuensi": {
        "Hertz": 1,
        "Kilohertz": 1000,
        "Megahertz": 1_000_000,
    },
    "🧲 Hambatan Listrik": {
        "Ohm": 1,
        "Kiloohm": 1000,
        "Megaohm": 1_000_000,
    },
    "🔌 Tegangan Listrik": {
        "Volt": 1,
        "Kilovolt": 1000,
        "Milivolt": 0.001,
    },
    "🔋 Arus Listrik": {
        "Ampere": 1,
        "Miliampere": 0.001,
        "Kiloampere": 1000,
    },
}

# ---------------------- FUNGSI KONVERSI SUHU ----------------------
def konversi_suhu(nilai, asal, tujuan):
    if asal == tujuan:
        return nilai

    # ke Celsius dulu
    if asal == "Fahrenheit":
        c = (nilai - 32) * 5 / 9
    elif asal == "Kelvin":
        c = nilai - 273.15
    else:
        c = nilai

    # dari Celsius ke tujuan
    if tujuan == "Fahrenheit":
        return (c * 9 / 5) + 32
    elif tujuan == "Kelvin":
        return c + 273.15
    else:
        return c

# ---------------------- FUNGSI PRESISI ----------------------
def format_presisi(nilai):
    if abs(nilai) < 1:
        return f"{nilai:.5f}"
    elif abs(nilai) < 10:
        return f"{nilai:.4f}"
    elif abs(nilai) < 100:
        return f"{nilai:.3f}"
    else:
        return f"{nilai:.2f}"

# ---------------------- HALAMAN UTAMA ----------------------
st.sidebar.title("📚 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", ["📌 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

# ---------------------- HALAMAN: BERANDA ----------------------
if halaman == "📌 Beranda":
    st.title("📐 Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Selamat datang di aplikasi **Kalkulator Konversi Satuan Fisika**!  
    Aplikasi ini memungkinkan Anda mengonversi berbagai satuan fisika secara cepat, akurat, dan interaktif.

    💡 **Fitur yang tersedia**:
    - Konversi antar satuan dalam berbagai kategori: suhu, massa, tekanan, energi, kecepatan, dan lainnya.
    - Penjelasan lengkap setiap hasil konversi.
    - Grafik visual untuk membantu memahami perbandingan nilai.
    - Tampilan menarik dan elegan ✨
    """)

# ---------------------- HALAMAN: KALKULATOR ----------------------
elif halaman == "📐 Kalkulator":
    st.title("📐 Kalkulator Konversi Satuan")

    kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
    satuan_asal = st.selectbox("Dari satuan:", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("Ke satuan:", list(konversi_data[kategori].keys()))
    nilai_input = st.text_input("Masukkan nilai yang ingin dikonversi:")

    if st.button("🔄 Konversi"):
        if not nilai_input:
            st.warning("⚠ Harap masukkan nilai terlebih dahulu.")
        else:
            try:
                nilai = float(nilai_input.replace(",", "."))
                with st.spinner("⏳ Menghitung..."):
                    time.sleep(1)

                    if kategori == "🔥 Suhu":
                        hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                        penjelasan = """
📘 **Penjelasan Konversi Suhu**

Anda menggunakan rumus konversi suhu berdasarkan standar ilmiah internasional.  
Rumus tergantung arah konversi, contohnya:

- Celsius ⇄ Kelvin  `K = C + 273.15`
- Celsius ⇄ Fahrenheit `F = (C × 9/5) + 32`
- Fahrenheit ⇄ Kelvin `K = (F - 32) × 5/9 + 273.15`

Rumus-rumus ini digunakan dalam industri, sains, dan akademik.  
Hasil konversi ini aman digunakan untuk eksperimen dan aplikasi praktis.
"""
                    else:
                        hasil = nilai * konversi_data[kategori][satuan_asal] / konversi_data[kategori][satuan_tujuan]
                        penjelasan = f"""
📘 **Penjelasan Konversi {kategori.replace('⚡','').replace('💨','').replace('🔌','').replace('🔋','')}**

Anda mengonversi satuan dengan rumus berikut:

 **Nilai Tujuan = Nilai Asal × Faktor Asal / Faktor Tujuan**

Faktor konversi didasarkan pada standar satuan internasional (SI).  
Pastikan Anda memilih satuan yang sesuai dengan konteks kebutuhan (laboratorium, industri, dll).
"""

                    hasil_str = format_presisi(hasil)

                    # HASIL UTAMA
                    st.markdown(f"""
<div style="padding: 20px; border-radius: 15px; background-color: #001f3f; color: white; 
            border: 2px solid #39cccc; text-align: center; font-size: 24px; font-weight: bold; 
            box-shadow: 0px 0px 25px #39cccc;">
    🔄 {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}
</div>
""", unsafe_allow_html=True)

                    st.markdown(penjelasan)

                    # Grafik batang
                    chart_df = pd.DataFrame({'Satuan': [satuan_asal, satuan_tujuan], 'Nilai': [nilai, hasil]})
                    st.altair_chart(
                        alt.Chart(chart_df).mark_bar().encode(
                            x='Satuan', y='Nilai', color='Satuan'
                        ).properties(title="📊 Perbandingan Nilai Sebelum & Sesudah Konversi"),
                        use_container_width=True
                    )

            except ValueError:
                st.error("❌ Nilai harus berupa angka.")

# ---------------------- HALAMAN: GRAFIK ----------------------
elif halaman == "📊 Grafik":
    st.title("📊 Contoh Visualisasi Konversi")
    st.markdown("Silakan lakukan konversi terlebih dahulu di halaman 'Kalkulator' untuk melihat grafik.")

# ---------------------- HALAMAN: TENTANG ----------------------
elif halaman == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
Aplikasi ini dibuat untuk membantu pelajar, mahasiswa, guru, dosen, dan profesional dalam mengonversi satuan fisika secara cepat, akurat, dan menyenangkan.

**Pengembang**: AL FATIH  
**Versi**: 1.0  
**Dibuat dengan**: Python + Streamlit  
**Didukung oleh**: OpenAI + Altair + Pandas  
    """)
