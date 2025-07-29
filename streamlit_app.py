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

# ---------------------- BACKGROUND ----------------------
def set_custom_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

image_link = "https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp"
set_custom_background(image_link)

# ---------------------- NAVIGASI ----------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "📐 Kalkulator", "ℹ️ Tentang"])

# ---------------------- BERANDA ----------------------
if halaman == "🏠 Beranda":
    st.title("🧠 Selamat Datang di Kalkulator Konversi Satuan Fisika 🧠")
    st.markdown("""
    Aplikasi ini merupakan hasil proyek dari mata kuliah **Logika Pemrograman Komputer** dalam Program Studi **D3 Analisis Kimia**.

💡 Dirancang untuk membantu pengguna dalam mengonversi berbagai satuan fisika secara **cepat**, **praktis**, dan **akurat**, seperti:

- 🔥 Suhu
- ⚖ Massa
- 📏 Panjang
- 💨 Kecepatan
- 💡 Daya, dan masih banyak lagi.

Dengan tampilan interaktif dan penjelasan visual yang mudah dipahami, aplikasi ini tidak hanya membantu dalam perhitungan, tapi juga mendukung **pembelajaran konsep satuan fisika** secara menyenangkan.

---

👉 Silakan pilih menu di sebelah kiri untuk mulai menggunakan kalkulator!
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

        st.markdown("---")
        st.markdown("### 🔁 Konversi ke Semua Satuan")
        st.dataframe(pd.DataFrame(semua_hasil.items(), columns=["Satuan", "Hasil"]), use_container_width=True)

# ---------------------- TENTANG ----------------------
elif halaman == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Kalkulator Konversi Satuan Fisika** ini dibuat sebagai **proyek tugas** untuk mata kuliah **Logika Pemrograman Komputer** pada Program Studi **D3 Analisis Kimia**.

🎯 **Tujuan utama pembuatan aplikasi ini adalah:**
- Menerapkan logika pemrograman dalam membangun solusi nyata
- Membantu mahasiswa dan pengguna umum dalam konversi satuan fisika secara cepat dan akurat
- Menyediakan alat bantu edukatif dalam memahami hubungan antar satuan

🧪 Aplikasi ini mencakup berbagai kategori konversi, seperti:
- Suhu
- Massa
- Panjang
- Waktu
- Tekanan
- Energi, dan lainnya

---

📚 **Sumber Referensi Konversi:**
- NIST (National Institute of Standards and Technology)
- SI Units Handbook
- Buku Fisika Dasar (Halliday & Resnick)
- [unitconverters.net](https://www.unitconverters.net/)
- [rapidtables.com](https://www.rapidtables.com/convert/)

---

👨‍💻 **Dikembangkan oleh:**  
Mahasiswa Program Studi D3 Analisis Kimia – 2025
    """)

# ---------------------- WATERMARK ----------------------
st.markdown("""
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 14px;
        color: rgba(255, 255, 255, 0.5);
        z-index: 9999;
        pointer-events: none;
        font-weight: bold;
    }
    </style>
    <div class="watermark">
        POLITEKNIK AKA BOGOR – D3 ANALISIS KIMIA
    </div>
    """, unsafe_allow_html=True)
