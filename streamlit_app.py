import streamlit as st
import pandas as pd
import time
import altair as alt

# ---------------------- DATA KONVERSI ----------------------
konversi_data = {
    "🔥 Suhu": {
        "Celsius (°C)": "C",
        "Fahrenheit (°F)": "F",
        "Kelvin (K)": "K"
    },
    "🧪 Tekanan": {
        "atm": 101325,
        "mmHg": 133.322,
        "Pa": 1,
        "bar": 100000,
        "kPa": 1000
    },
    "⚖ Massa": {
        "kg": 1000,
        "g": 1,
        "mg": 0.001,
        "lb": 453.592,
        "oz": 28.3495
    },
    "📏 Panjang": {
        "km": 1000,
        "m": 1,
        "cm": 0.01,
        "mm": 0.001,
        "μm": 1e-6,
        "nm": 1e-9,
        "inchi": 0.0254,
        "kaki (ft)": 0.3048,
        "mil": 1609.34
    },
"⏱ Waktu": {
        "detik (s)": 1,
        "menit": 60,
        "jam": 3600,
        "hari": 86400
    },
    "⚡ Energi": {
        "joule (J)": 1,
        "kilojoule (kJ)": 1000,
        "kalori (cal)": 4.184,
        "kilokalori (kcal)": 4184,
        "elektronvolt (eV)": 1.602e-19
    },
    "💨 Kecepatan": {
        "m/s": 1,
        "km/jam": 1000/3600,
        "mil/jam (mph)": 1609.34/3600,
        "knot": 1852/3600
    },
    "💡 Daya": {
        "watt (W)": 1,
        "kilowatt (kW)": 1000,
        "horsepower (HP)": 745.7
    },
    "🧊 Volume": {
        "liter (L)": 1,
        "mililiter (mL)": 0.001,
        "cm³": 0.001,
        "m³": 1000,
        "galon": 3.78541
    },
    "📡 Frekuensi": {
        "Hz": 1,
        "kHz": 1e3,
        "MHz": 1e6,
        "GHz": 1e9
    },
    "⚡ Hambatan Listrik": {
        "ohm (Ω)": 1,
        "kΩ": 1e3,
        "MΩ": 1e6
    },
    "🔋 Tegangan Listrik": {
        "volt (V)": 1,
        "mV": 1e-3,
        "kV": 1e3
    },
    "🔌 Arus Listrik": {
        "ampere (A)": 1,
        "mA": 1e-3,
        "μA": 1e-6
    }
}

# ---------------------- FUNGSI KONVERSI ----------------------
# Fungsi konversi suhu (definisi duluan)
def konversi_suhu(nilai, dari, ke):
    if dari == ke:
        return nilai
    if dari == "Celsius (°C)":
        if ke == "Fahrenheit (°F)":
            return (nilai * 9/5) + 32
        elif ke == "Kelvin (K)":
            return nilai + 273.15
    if dari == "Fahrenheit (°F)":
        if ke == "Celsius (°C)":
            return (nilai - 32) * 5/9
        elif ke == "Kelvin (K)":
            return ((nilai - 32) * 5/9) + 273.15
    if dari == "Kelvin (K)":
        if ke == "Celsius (°C)":
            return nilai - 273.15
        elif ke == "Fahrenheit (°F)":
            return ((nilai - 273.15) * 9/5) + 32
    return None

# Fungsi konversi umum
def konversi_satuan(kategori, nilai, satuan_dari, satuan_ke):
    if "Suhu" in kategori:
        return konversi_suhu(nilai, satuan_dari, satuan_ke)
    else:
        return nilai * konversi_data[kategori][satuan_dari] / konversi_data[kategori][satuan_ke]
        
def get_konversi_semua_satuan(kategori, nilai, satuan_dari):
    hasil = {}
    if "Suhu" in kategori:
        for satuan in konversi_data[kategori]:
            if satuan != satuan_dari:
                hasil[satuan] = konversi_suhu(nilai, satuan_dari, satuan)
    else:
        for satuan in konversi_data[kategori]:
            hasil[satuan] = konversi_satuan(kategori, nilai, satuan_dari, satuan)
    return hasil



def tampilkan_rumus(kategori, nilai, satuan_dari, satuan_ke, hasil):
    st.markdown("### 📘 Penjelasan Rumus Konversi")

    if kategori == "Suhu":
        st.markdown(f"""
        Misalnya mengonversi dari **{satuan_dari}** ke **{satuan_ke}**:

        ```latex
        \\text{{Hasil}} = \\text{{konversi suhu sesuai rumus}}
        ```
        """)

        if satuan_dari == "Celsius (°C)" and satuan_ke == "Fahrenheit (°F)":
            st.latex(r"Hasil = (°C × \frac{9}{5}) + 32")
            st.markdown(f"Hasil = ({nilai} × 9/5) + 32 = **{hasil:.2f} °F**")

        elif satuan_dari == "Celsius (°C)" and satuan_ke == "Kelvin (K)":
            st.latex(r"Hasil = °C + 273.15")
            st.markdown(f"Hasil = {nilai} + 273.15 = **{hasil:.2f} K**")

        elif satuan_dari == "Fahrenheit (°F)" and satuan_ke == "Celsius (°C)":
            st.latex(r"Hasil = (°F - 32) × \frac{5}{9}")
            st.markdown(f"Hasil = ({nilai} - 32) × 5/9 = **{hasil:.2f} °C**")

        elif satuan_dari == "Kelvin (K)" and satuan_ke == "Fahrenheit (°F)":
            st.latex(r"Hasil = ((K - 273.15) × \frac{9}{5}) + 32")
            st.markdown(f"Hasil = (({nilai} - 273.15) × 9/5) + 32 = **{hasil:.2f} °F**")

        # Tambahkan semua kombinasi suhu lainnya
        else:
            st.info("Konversi suhu lainnya menggunakan rumus umum sesuai standar.")

    else:
        st.markdown(f"""
        Misalnya mengonversi dari **{satuan_dari}** ke **{satuan_ke}**:

        ```latex
        \\text{{Hasil}} = \\frac{{\\text{{nilai}} × \\text{{faktor konversi dari}}}}{{\\text{{faktor ke}}}}
        ```

        Dengan:
        - Faktor dari: `{konversi_data[kategori][satuan_dari]}`
        - Faktor ke: `{konversi_data[kategori][satuan_ke]}`

        Maka:
        ```python
        Hasil = ({nilai} × {konversi_data[kategori][satuan_dari]}) / {konversi_data[kategori][satuan_ke]}
              = {hasil:.5f}
        ```
        """)
def tampilkan_penjelasan_rumus(kategori, satuan_dari, satuan_ke):
    st.markdown("### 📘 Penjelasan Rumus Konversi")
    
    if kategori == "Suhu":
        rumus = ""
        if satuan_dari == "Celsius (°C)" and satuan_ke == "Fahrenheit (°F)":
            rumus = r"$F = \frac{9}{5} \times C + 32$"
        elif satuan_dari == "Fahrenheit (°F)" and satuan_ke == "Celsius (°C)":
            rumus = r"$C = \frac{5}{9} \times (F - 32)$"
        elif satuan_dari == "Celsius (°C)" and satuan_ke == "Kelvin (K)":
            rumus = r"$K = C + 273.15$"
        elif satuan_dari == "Kelvin (K)" and satuan_ke == "Celsius (°C)":
            rumus = r"$C = K - 273.15$"
        elif satuan_dari == "Fahrenheit (°F)" and satuan_ke == "Kelvin (K)":
            rumus = r"$K = \frac{5}{9} \times (F - 32) + 273.15$"
        elif satuan_dari == "Kelvin (K)" and satuan_ke == "Fahrenheit (°F)":
            rumus = r"$F = \frac{9}{5} \times (K - 273.15) + 32$"
        else:
            rumus = "*Tidak tersedia untuk kombinasi ini.*"

        st.latex(rumus)
    else:
        st.markdown(f"""
        Rumus konversi untuk kategori **{kategori}**:
        ```text
        Nilai akhir = Nilai awal × (Faktor {satuan_dari} ÷ Faktor {satuan_ke})
        ```
        """)


# ---------------------- TEMA & BACKGROUND ----------------------
def set_custom_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

image_link = "https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp"

set_custom_background(image_link)

# ---------------------- NAVIGASI SIDEBAR ----------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "📐 Kalkulator", "ℹ️ Tentang"])

# ---------------------- HALAMAN BERANDA ----------------------
if halaman == "🏠 Beranda":
    st.title("🌟 Selamat Datang di Kalkulator Konversi Satuan Fisika 🌟")
    st.markdown("""
    Aplikasi ini dirancang untuk membantu Anda mengonversi berbagai satuan fisika seperti suhu, massa, panjang, tekanan, dan lainnya dengan **mudah**, **cepat**, dan **akurat**.

    ### 📌 Fitur Unggulan:
    - Konversi antar satuan dalam berbagai kategori
    - Penjelasan rumus yang **jelas dan edukatif**
    - Visualisasi grafik konversi
    - Tampilan interaktif dan menarik

    **Pilih menu di sebelah kiri untuk memulai!**
    """)

# ---------------------- KALKULATOR ----------------------
elif halaman == "📐 Kalkulator":
    st.title("📐 Kalkulator Konversi Satuan Fisika")

    kategori = st.selectbox("Pilih Kategori Satuan", list(konversi_data.keys()))
    satuan_dari = st.selectbox("Dari Satuan", list(konversi_data[kategori].keys()))
    satuan_ke = st.selectbox("Ke Satuan", list(konversi_data[kategori].keys()))
    nilai = st.number_input("Masukkan Nilai", value=0.0, step=0.1, format="%.4f")

    if st.button("🔄 Konversi"):
        with st.spinner("Menghitung..."):
            time.sleep(1.5)
            hasil = konversi_satuan(kategori, nilai, satuan_dari, satuan_ke)
            semua_hasil = get_konversi_semua_satuan(kategori, nilai, satuan_dari)

        st.markdown("## 🎯 Hasil Konversi")
        st.success(f"**{nilai} {satuan_dari} = {hasil:.4f} {satuan_ke}**")

        tampilkan_penjelasan_rumus(kategori, satuan_dari, satuan_ke)

        st.markdown("---")
        st.markdown("### 🔁 Konversi ke Semua Satuan")
        st.dataframe(pd.DataFrame(semua_hasil.items(), columns=["Satuan", "Hasil"]), use_container_width=True)
# ---------------------- GRAFIK ----------------------
elif halaman == "📊 Grafik":
    st.title("📊 Visualisasi Konversi Satuan")

    kategori = st.selectbox("Pilih Kategori", list(konversi_data.keys()), key="grafik_kategori")
    satuan_dari = st.selectbox("Pilih Satuan Asal", list(konversi_data[kategori].keys()), key="grafik_dari")
    nilai = st.number_input("Masukkan Nilai", value=1.0, step=0.1, format="%.4f", key="grafik_nilai")

    if st.button("📈 Tampilkan Grafik"):
        semua_hasil = get_konversi_semua_satuan(kategori, nilai, satuan_dari)
        st.markdown("### 🔍 Grafik Konversi")
        tampilkan_grafik(kategori, semua_hasil)

# ---------------------- TENTANG ----------------------
elif halaman == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Kalkulator Konversi Satuan Fisika** ini dibuat untuk mempermudah proses belajar dan kerja dalam konversi satuan fisika sehari-hari.

    ### 🧠 Dibuat Menggunakan:
    - Python 3
    - [Streamlit](https://streamlit.io/)
    - Altair & Matplotlib

    ### 📚 Referensi Konversi:
    - NIST (National Institute of Standards and Technology)
    - International System of Units (SI)
    - Buku Fisika Dasar - Halliday & Resnick
    - https://www.unitconverters.net/
    - https://www.rapidtables.com/convert/

    ### 👨‍💻 Developer:
    **AL FATIH** – 2025
    """)

