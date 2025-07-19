import streamlit as st
import pandas as pd
import time
import altair as alt

# ---------------------- SETUP LATAR BELAKANG ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, {opacity});
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://images.unsplash.com/photo-1581091870632-2b6a2b6b93bd", opacity=0.85)

# ---------------------- DATA KONVERSI ----------------------
konversi_data = {
    "🌡️ Suhu": {
        "satuan": ["Celsius", "Fahrenheit", "Kelvin"]
    },
    "💨 Tekanan": {
        "satuan": ["Pascal", "bar", "atm", "mmHg", "psi"],
        "faktor": {"Pascal": 1, "bar": 1e5, "atm": 101325, "mmHg": 133.322, "psi": 6894.76}
    },
    "⚖️ Massa": {
        "satuan": ["kg", "g", "mg", "lb", "oz"],
        "faktor": {"kg": 1, "g": 1e-3, "mg": 1e-6, "lb": 0.453592, "oz": 0.0283495}
    },
    "📏 Panjang": {
        "satuan": ["m", "cm", "mm", "km", "inch", "ft", "mile"],
        "faktor": {"m": 1, "cm": 0.01, "mm": 0.001, "km": 1000, "inch": 0.0254, "ft": 0.3048, "mile": 1609.34}
    },
    "⏱️ Waktu": {
        "satuan": ["detik", "menit", "jam", "hari"],
        "faktor": {"detik": 1, "menit": 60, "jam": 3600, "hari": 86400}
    },
    "🔥 Energi": {
        "satuan": ["Joule", "kJ", "kalori", "kWh"],
        "faktor": {"Joule": 1, "kJ": 1000, "kalori": 4.184, "kWh": 3.6e6}
    },
    "🚗 Kecepatan": {
        "satuan": ["m/s", "km/jam", "mph", "knot"],
        "faktor": {"m/s": 1, "km/jam": 0.277778, "mph": 0.44704, "knot": 0.514444}
    },
    "⚡ Daya": {
        "satuan": ["Watt", "kW", "HP"],
        "faktor": {"Watt": 1, "kW": 1000, "HP": 745.7}
    },
    "🧪 Volume": {
        "satuan": ["L", "mL", "cm³", "m³", "galon"],
        "faktor": {"L": 1, "mL": 0.001, "cm³": 0.001, "m³": 1000, "galon": 3.78541}
    },
    "🎵 Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz", "GHz"],
        "faktor": {"Hz": 1, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}
    },
    "🔌 Hambatan Listrik": {
        "satuan": ["Ohm", "kOhm", "MOhm"],
        "faktor": {"Ohm": 1, "kOhm": 1e3, "MOhm": 1e6}
    },
    "🔋 Tegangan Listrik": {
        "satuan": ["Volt", "mV", "kV"],
        "faktor": {"Volt": 1, "mV": 0.001, "kV": 1000}
    },
    "🔌 Arus Listrik": {
        "satuan": ["Ampere", "mA", "kA"],
        "faktor": {"Ampere": 1, "mA": 0.001, "kA": 1000}
    }
}

# ---------------------- KONVERSI ----------------------
def konversi_suhu(nilai, asal, tujuan):
    if asal == tujuan:
        return nilai
    if asal == "Celsius":
        return (nilai * 9/5 + 32) if tujuan == "Fahrenheit" else nilai + 273.15
    if asal == "Fahrenheit":
        return (nilai - 32) * 5/9 if tujuan == "Celsius" else (nilai - 32) * 5/9 + 273.15
    if asal == "Kelvin":
        return nilai - 273.15 if tujuan == "Celsius" else (nilai - 273.15) * 9/5 + 32

def konversi_lain(nilai, asal, tujuan, faktor):
    return nilai * faktor[asal] / faktor[tujuan]

# ---------------------- ANTARMUKA ----------------------
st.set_page_config(page_title="Kalkulator Konversi Fisika", layout="wide", page_icon="📐")

menu = st.sidebar.radio("Navigasi", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

if menu == "🏠 Beranda":
    st.title("📐 Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Selamat datang! Aplikasi ini membantu Anda mengonversi berbagai satuan fisika:

    - 🌡️ Suhu
    - ⚖️ Massa
    - 📏 Panjang
    - 💨 Tekanan
    - 🔋 Energi, Daya, Volume, Frekuensi, dll.

    Pilih halaman **Kalkulator** di sidebar untuk mulai mengonversi!
    """)

elif menu == "📐 Kalkulator":
    st.title("📐 Kalkulator Konversi")

    kategori = st.selectbox("Pilih Kategori Satuan", list(konversi_data.keys()))
    satuan = konversi_data[kategori]["satuan"]
    satuan_asal = st.selectbox("Dari Satuan", satuan)
    satuan_tujuan = st.selectbox("Ke Satuan", satuan)
    nilai = st.number_input("Masukkan Nilai", value=0.0, format="%.6f")

    if st.button("🔄 Konversi"):
        with st.spinner("Menghitung..."):
            time.sleep(1)
            if kategori == "🌡️ Suhu":
                hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
            else:
                faktor = konversi_data[kategori]["faktor"]
                hasil = konversi_lain(nilai, satuan_asal, satuan_tujuan, faktor)

            hasil_str = f"{hasil:.6f}"

            st.markdown(f"""
            <div style="padding: 20px; border-radius: 15px; background-color: #001f3f; color: white; border: 2px solid #39cccc;
                        text-align: center; font-size: 24px; font-weight: bold; box-shadow: 0px 0px 25px #39cccc;">
                🔄 {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}
            </div>
            """, unsafe_allow_html=True)

            st.text_input("📋 Salin Hasil:", f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="salin")

            if kategori == "🌡️ Suhu":
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
                penjelasan = f"""
📘 **Penjelasan Konversi {kategori.replace('⚡','').replace('💨','').replace('🔌','').replace('🔋','')}**

Anda mengonversi satuan dengan rumus berikut:

 **Nilai Tujuan = Nilai Asal × Faktor Asal / Faktor Tujuan**

Faktor konversi didasarkan pada standar satuan internasional (SI).  
Pastikan Anda memilih satuan yang sesuai dengan konteks kebutuhan (laboratorium, industri, dll).
"""
            st.markdown(penjelasan)

elif menu == "📊 Grafik":
    st.title("📊 Grafik Konversi")
    st.markdown("Perbandingan visual antara satuan asal dan satuan tujuan.")

    nilai_asal = st.number_input("Nilai Asal", value=1.0)
    satuan1 = st.selectbox("Satuan Asal", ["kg", "g", "mg", "lb", "oz"])
    satuan2 = st.selectbox("Satuan Tujuan", ["g", "mg", "kg", "lb", "oz"])

    if st.button("📈 Tampilkan Grafik"):
        faktor = konversi_data["⚖️ Massa"]["faktor"]
        hasil = konversi_lain(nilai_asal, satuan1, satuan2, faktor)

        chart_df = pd.DataFrame({
            'Satuan': [satuan1, satuan2],
            'Nilai': [nilai_asal, hasil]
        })

        color_scale = alt.Scale(domain=[satuan1, satuan2], range=["#1f77b4", "#2ca02c"])

        chart = alt.Chart(chart_df).mark_bar(size=60).encode(
            x=alt.X('Satuan', title=None),
            y=alt.Y('Nilai', title='Nilai'),
            color=alt.Color('Satuan', scale=color_scale, legend=None),
            tooltip=['Satuan', 'Nilai']
        ).properties(
            title="📊 Perbandingan Nilai Sebelum & Sesudah Konversi"
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16,
            anchor='start'
        )

        st.altair_chart(chart, use_container_width=True)

elif menu == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
## ℹ️ Tentang Aplikasi

**Kalkulator Konversi Satuan Fisika** ini dirancang untuk membantu siswa, mahasiswa, dan profesional dalam menghitung konversi satuan fisika dengan mudah dan cepat.

### 🎯 Tujuan:
- Menyediakan konversi satuan fisika yang akurat
- Menampilkan penjelasan rumus secara ilmiah
- Menyertakan grafik perbandingan untuk membantu visualisasi

---

### 📚 Referensi:

- NIST (National Institute of Standards and Technology):  
  https://physics.nist.gov/cuu/Units/index.html

- International Bureau of Weights and Measures (BIPM):  
  https://www.bipm.org/en/measurement-units/

- The Engineering Toolbox:  
  https://www.engineeringtoolbox.com/

- OpenAI API & Altair Documentation

---

### 🛠 Dibuat dengan:
- [Streamlit](https://streamlit.io)
- [Altair](https://altair-viz.github.io)
- [Pandas](https://pandas.pydata.org)

---
""")
