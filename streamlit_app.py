import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

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

# URL gambar latar belakang
bg_image_url = "https://i.pinimg.com/originals/4e/ac/35/4eac359bce1e49679ad98f98db7428d4.png"
set_background_from_url(bg_image_url, opacity=0.85)

# ---------------------- GAYA METRIC & TABEL ----------------------
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
    .stDataFrame > div > div {
        transition: all 0.2s ease-in-out;
    }
    .stDataFrame > div > div:hover {
        transform: scale(1.01);
        box-shadow: 0px 0px 10px #00BFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- NAVIGASI HALAMAN ----------------------
halaman = st.sidebar.selectbox("Navigasi", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "📖 Tentang"])

# ---------------------- DATA KONVERSI ----------------------
data_konversi = {
    "🔥 Suhu": {
        "Celsius": {"Kelvin": lambda c: c + 273.15,
                    "Fahrenheit": lambda c: (c * 9/5) + 32},
        "Kelvin": {"Celsius": lambda k: k - 273.15,
                   "Fahrenheit": lambda k: (k - 273.15) * 9/5 + 32},
        "Fahrenheit": {"Celsius": lambda f: (f - 32) * 5/9,
                       "Kelvin": lambda f: (f - 32) * 5/9 + 273.15}
    },
    "💨 Tekanan": {
        "atm": {"Pa": 101325, "bar": 1.01325, "psi": 14.6959},
        "Pa": {"atm": 1/101325, "bar": 1e-5, "psi": 0.000145038},
        "bar": {"atm": 1/1.01325, "Pa": 1e5, "psi": 14.5038},
        "psi": {"atm": 1/14.6959, "Pa": 6894.76, "bar": 1/14.5038}
    },
    "⚖️ Massa": {
        "kg": {"g": 1000, "mg": 1e6, "lb": 2.20462},
        "g": {"kg": 0.001, "mg": 1000, "lb": 0.00220462},
        "mg": {"kg": 1e-6, "g": 0.001, "lb": 2.2046e-6},
        "lb": {"kg": 0.453592, "g": 453.592, "mg": 453592}
    },
    "📏 Panjang": {
        "m": {"cm": 100, "mm": 1000, "inch": 39.3701, "ft": 3.28084},
        "cm": {"m": 0.01, "mm": 10, "inch": 0.393701, "ft": 0.0328084},
        "inch": {"m": 0.0254, "cm": 2.54, "mm": 25.4, "ft": 1/12},
        "ft": {"m": 0.3048, "cm": 30.48, "inch": 12, "mm": 304.8}
    },
    "⏱️ Waktu": {
        "detik": {"menit": 1/60, "jam": 1/3600},
        "menit": {"detik": 60, "jam": 1/60},
        "jam": {"detik": 3600, "menit": 60}
    },
    "⚡ Energi": {
        "J": {"kJ": 0.001, "cal": 0.239006, "kcal": 0.000239006},
        "kJ": {"J": 1000, "cal": 239.006, "kcal": 0.239006},
        "cal": {"J": 4.184, "kJ": 0.004184, "kcal": 0.001},
        "kcal": {"J": 4184, "kJ": 4.184, "cal": 1000}
    },
    "🚗 Kecepatan": {
        "m/s": {"km/jam": 3.6, "mph": 2.23694},
        "km/jam": {"m/s": 0.277778, "mph": 0.621371},
        "mph": {"m/s": 0.44704, "km/jam": 1.60934}
    },
    "🔋 Daya": {
        "W": {"kW": 0.001, "HP": 0.00134102},
        "kW": {"W": 1000, "HP": 1.34102},
        "HP": {"W": 745.7, "kW": 0.7457}
    },
    "🧪 Volume": {
        "mL": {"L": 0.001, "cm³": 1},
        "L": {"mL": 1000, "cm³": 1000},
        "cm³": {"mL": 1, "L": 0.001}
    },
    "📻 Frekuensi": {
        "Hz": {"kHz": 0.001, "MHz": 1e-6},
        "kHz": {"Hz": 1000, "MHz": 0.001},
        "MHz": {"Hz": 1e6, "kHz": 1000}
    },
    "💡 Hambatan Listrik": {
        "Ohm": {"kOhm": 0.001, "MOhm": 1e-6},
        "kOhm": {"Ohm": 1000, "MOhm": 0.001},
        "MOhm": {"Ohm": 1e6, "kOhm": 1000}
    },
    "🔌 Tegangan Listrik": {
        "V": {"kV": 0.001},
        "kV": {"V": 1000}
    },
    "🔋 Arus Listrik": {
        "A": {"mA": 1000},
        "mA": {"A": 0.001}
    }
}

# ---------------------- HALAMAN KALKULATOR ----------------------
elif halaman == "📐 Kalkulator":
    st.markdown("## 📐 Kalkulator Konversi")
    kategori = st.selectbox("Pilih kategori satuan", list(data_konversi.keys()))
    
    satuan_input = st.selectbox("Dari satuan", list(data_konversi[kategori].keys()))
    satuan_output = st.selectbox("Ke satuan", [s for s in data_konversi[kategori][satuan_input].keys()])
    nilai_input = st.text_input(f"Masukkan nilai ({satuan_input})", "1")

    try:
        n = float(nilai_input)
        with st.spinner("🔄 Menghitung konversi..."):
            import time; time.sleep(2)
            # ======================= KONVERSI =======================
            if kategori == "🔥 Suhu":
                hasil = data_konversi[kategori][satuan_input][satuan_output](n)
            else:
                hasil = n * data_konversi[kategori][satuan_input][satuan_output]

            # ======================= TAMPILKAN HASIL =======================
            st.success("✅ Konversi Berhasil!")
            st.metric(label=f"{n} {satuan_input} = ", value=f"{hasil:.4f} {satuan_output}")

            # ======================= TABEL KONVERSI LAIN =======================
            st.markdown("### 🔁 Konversi ke Semua Satuan:")
            hasil_semua = {}
            for satuan_tujuan, konversi in data_konversi[kategori][satuan_input].items():
                if satuan_tujuan == satuan_output:
                    continue
                nilai = data_konversi[kategori][satuan_input][satuan_tujuan](n) if kategori == "🔥 Suhu" else n * konversi
                hasil_semua[satuan_tujuan] = nilai
            df_hasil = pd.DataFrame.from_dict(hasil_semua, orient='index', columns=["Hasil"])
            st.table(df_hasil)

            # ======================= GRAFIK =======================
            st.markdown("### 📊 Visualisasi Konversi:")
            fig = px.bar(df_hasil, x=df_hasil.index, y="Hasil", labels={"x": "Satuan", "Hasil": "Nilai"})
            st.plotly_chart(fig)

            # ======================= SALIN HASIL =======================
            hasil_str = f"{n} {satuan_input} = {hasil:.4f} {satuan_output}"
            st.code(hasil_str)
            st.button("📋 Salin Hasil", on_click=lambda: pyperclip.copy(hasil_str))

            # ======================= PENJELASAN RUMUS =======================
            st.markdown("### 📖 Penjelasan Rumus:")
            if kategori == "🔥 Suhu":
                st.markdown("""
**Rumus Konversi Suhu**:
- Celsius → Kelvin:                                                                
  \[
  K = ^\circ C + 273.15
  \]
- Celsius → Fahrenheit:
  \[
  F = (^\circ C \times \frac{9}{5}) + 32
  \]
- Fahrenheit → Celsius:
  \[
  C = (^\circ F - 32) \times \frac{5}{9}
  \]
- Kelvin → Celsius:
  \[
  C = K - 273.15
  \]
- Fahrenheit → Kelvin:
  \[
  K = (^\circ F - 32) \times \frac{5}{9} + 273.15
  \]
- Kelvin → Fahrenheit:
  \[
  F = (K - 273.15) \times \frac{9}{5} + 32
  \]
""")
            else:
                st.markdown(f"**Rumus**: `hasil = nilai × faktor konversi`  \nContoh: `{n} {satuan_input} × faktor → {hasil:.4f} {satuan_output}`")
    except ValueError:
        st.error("❌ Masukkan angka yang valid.")

# ---------------------- HALAMAN TENTANG ----------------------
elif halaman == "📖 Tentang":
    st.markdown("## ℹ️ Tentang Aplikasi")

    st.markdown("""
Aplikasi **Kalkulator Konversi Satuan Fisika** dibuat untuk membantu pelajar, mahasiswa, dan profesional 
melakukan konversi satuan fisika secara akurat dan cepat.

### 🎯 Fitur Utama:
- 🔁 Konversi berbagai satuan fisika: suhu, massa, panjang, tekanan, waktu, energi, daya, kecepatan, volume, arus listrik, hambatan, dan lainnya.
- 📖 Penjelasan lengkap rumus konversi
- 📊 Visualisasi hasil dalam bentuk grafik
- 🖼️ Antarmuka interaktif dan latar belakang yang menarik

### 📚 Sumber Referensi:
- SI Units: https://www.bipm.org
- NIST (National Institute of Standards and Technology)
- Physics for Scientists and Engineers – Serway & Jewett
- CRC Handbook of Chemistry and Physics
- Thermodynamics – Yunus Cengel

---

Terima kasih telah menggunakan aplikasi ini. Semoga bermanfaat dalam studi maupun pekerjaan Anda!
""")
