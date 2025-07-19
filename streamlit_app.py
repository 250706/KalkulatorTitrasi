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
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, {opacity});
            z-index: -1;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://i.pinimg.com/originals/4e/ac/35/4eac359bce1e49679ad98f98db7428d4.png", 0.85)

# ---------------------- EFEK INTERAKTIF ----------------------
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #001F3F;
        padding: 20px;
        border-radius: 15px;
        color: white;
        border: 2px solid #39CCCC;
        box-shadow: 0px 0px 15px 2px #39CCCC;
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow: 0px 0px 25px 5px #7FDBFF;
        transform: scale(1.03);
    }
    .stDataFrame > div > div:hover {
        transform: scale(1.01);
        box-shadow: 0px 0px 10px #00BFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR DAN NAVIGASI ----------------------
st.sidebar.title("📚 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["Beranda", "Kalkulator", "📖 Tentang"])

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
    "🕏 Panjang": {
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
        "ohm (Ω)": 1,
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

def konversi_suhu(nilai, dari, ke):
    if dari == ke:
        return nilai
    if dari == "Celsius (°C)":
        return (nilai * 9/5 + 32) if ke == "Fahrenheit (°F)" else nilai + 273.15
    if dari == "Fahrenheit (°F)":
        return (nilai - 32) * 5/9 if ke == "Celsius (°C)" else (nilai - 32) * 5/9 + 273.15
    if dari == "Kelvin (K)":
        return nilai - 273.15 if ke == "Celsius (°C)" else (nilai - 273.15) * 9/5 + 32

def format_presisi(nilai):
    if nilai == int(nilai):
        return str(int(nilai))
    elif abs(nilai) < 1:
        return f"{nilai:.4f}".rstrip('0').rstrip('.')
    elif abs(nilai) < 100:
        return f"{nilai:.3f}".rstrip('0').rstrip('.')
    else:
        return f"{nilai:.2f}".rstrip('0').rstrip('.')

# ---------------------- HALAMAN: BERANDA ----------------------
if halaman == "Beranda":
    st.title("👋 Selamat Datang di Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Aplikasi ini membantu Anda mengonversi berbagai satuan fisika dengan mudah dan cepat.  
    Gunakan menu *Kalkulator* untuk memulai perhitungan.
    """)

# ---------------------- HALAMAN: KALKULATOR ----------------------
elif halaman == "Kalkulator":
    st.title("🔬 Kalkulator Konversi Satuan Fisika")

    kategori = st.selectbox("📘 Pilih Kategori Satuan:", list(konversi_data.keys()))
    satuan_asal = st.selectbox("🔸 Satuan Asal:", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("🔹 Satuan Tujuan:", list(konversi_data[kategori].keys()))
    nilai_input = st.text_input("📥 Masukkan Nilai:", placeholder="Contoh: 5.5")

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

Faktor konversi didasarkan pad

# ---------------------- HALAMAN: TENTANG ----------------------
elif halaman == "📖 Tentang":
    st.markdown("## ℹ Tentang Aplikasi")

    st.markdown("""
Aplikasi *Kalkulator Konversi Satuan Fisika* dibuat untuk membantu pelajar, mahasiswa, dan profesional 
melakukan konversi satuan fisika secara *akurat, cepat, dan interaktif*.

---

### Fitur Utama:
- Konversi berbagai satuan fisika: suhu, massa, panjang, tekanan, waktu, energi, daya, kecepatan, volume, arus listrik, hambatan, dan lainnya.
- Penjelasan lengkap dan mudah dimengerti untuk setiap rumus konversi.
- Visualisasi hasil konversi dalam bentuk grafik batang.
- Antarmuka ramah pengguna dan estetis, dengan latar belakang visual yang dapat disesuaikan.
- Presisi hasil disesuaikan berdasarkan standar masing-masing kategori satuan.

---

### Sumber Referensi:
- SI Units  https://www.bipm.org
- NIST  National Institute of Standards and Technology
- Physics for Scientists and Engineers  Serway & Jewett
- CRC Handbook of Chemistry and Physics
- Thermodynamics  Yunus A. Çengel

---

Terima kasih telah menggunakan aplikasi ini. Semoga bermanfaat dalam studi maupun pekerjaan Anda! 
""")

