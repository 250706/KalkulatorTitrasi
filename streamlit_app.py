import streamlit as st
import pandas as pd
import altair as alt
import time

# ---------------------- FUNGSI KONVERSI ----------------------
def konversi_suhu(nilai, satuan_asal, satuan_tujuan):
    if satuan_asal == satuan_tujuan:
        return nilai
    if satuan_asal == "Celsius":
        return {
            "Fahrenheit": (nilai * 9/5) + 32,
            "Kelvin": nilai + 273.15
        }[satuan_tujuan]
    elif satuan_asal == "Fahrenheit":
        return {
            "Celsius": (nilai - 32) * 5/9,
            "Kelvin": (nilai - 32) * 5/9 + 273.15
        }[satuan_tujuan]
    elif satuan_asal == "Kelvin":
        return {
            "Celsius": nilai - 273.15,
            "Fahrenheit": (nilai - 273.15) * 9/5 + 32
        }[satuan_tujuan]

def konversi_umum(nilai, satuan_asal, satuan_tujuan, kategori):
    faktor = KONVERSI_FAKTOR[kategori]
    nilai_masuk_ke_satuan_dasar = nilai * faktor[satuan_asal]
    return nilai_masuk_ke_satuan_dasar / faktor[satuan_tujuan]

def penjelasan_rumus(nilai, hasil, satuan_asal, satuan_tujuan, kategori):
    if kategori == "Suhu":
        rumus = {
            ("Celsius", "Fahrenheit"): "F = (C × 9/5) + 32",
            ("Celsius", "Kelvin"): "K = C + 273.15",
            ("Fahrenheit", "Celsius"): "C = (F - 32) × 5/9",
            ("Fahrenheit", "Kelvin"): "K = (F - 32) × 5/9 + 273.15",
            ("Kelvin", "Celsius"): "C = K - 273.15",
            ("Kelvin", "Fahrenheit"): "F = (K - 273.15) × 9/5 + 32"
        }.get((satuan_asal, satuan_tujuan), "")
        return f"""
### 🧮 Penjelasan Rumus

Rumus yang digunakan:

$$
{rumus}
$$

Dengan memasukkan nilai:

$$
{hasil:.2f} \, \text{{{satuan_tujuan}}}
$$
"""
    else:
        return f"""
### 🧮 Penjelasan Rumus

Menggunakan konversi umum:

$$
\\text{{Hasil}} = \\frac{{{nilai} \\times \\text{{faktor[{satuan_asal}]}}}}{{\\text{{faktor[{satuan_tujuan}]}}}}
$$

Sehingga:

$$
\\text{{Hasil}} = {hasil:.6g} \\, \\text{{{satuan_tujuan}}}
$$
"""

# ---------------------- DICTIONARY SATUAN ----------------------
KONVERSI_FAKTOR = {
    "Tekanan": {
        "Pa": 1, "kPa": 1e3, "atm": 101325, "bar": 1e5, "mmHg": 133.322
    },
    "Massa": {
        "mg": 1e-3, "g": 1, "kg": 1e3, "ton": 1e6
    },
    "Panjang": {
        "mm": 1e-3, "cm": 1e-2, "m": 1, "km": 1e3
    },
    "Waktu": {
        "detik": 1, "menit": 60, "jam": 3600, "hari": 86400
    },
    "Energi": {
        "J": 1, "kJ": 1e3, "MJ": 1e6, "cal": 4.184, "kcal": 4184
    },
    "Kecepatan": {
        "m/s": 1, "km/jam": 1000/3600, "mil/jam": 1609.34/3600
    },
    "Daya": {
        "Watt": 1, "kW": 1e3, "HP": 745.7
    },
    "Volume": {
        "mL": 1e-3, "L": 1, "m³": 1e3
    },
    "Frekuensi": {
        "Hz": 1, "kHz": 1e3, "MHz": 1e6
    },
    "Hambatan Listrik": {
        "ohm": 1, "kΩ": 1e3, "MΩ": 1e6
    },
    "Tegangan Listrik": {
        "V": 1, "kV": 1e3
    },
    "Arus Listrik": {
        "A": 1, "mA": 1e-3
    }
}

# ---------------------- APLIKASI STREAMLIT ----------------------
st.set_page_config(page_title="Kalkulator Konversi Satuan", layout="wide")

menu = st.sidebar.radio("Navigasi", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

if menu == "🏠 Beranda":
    st.title("🎉 Selamat Datang di Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    <div style='font-size:20px'>
        🚀 Aplikasi ini membantu Anda mengonversi berbagai satuan fisika seperti suhu, tekanan, energi, kecepatan, daya, dan lainnya dengan mudah dan cepat!

        <br><br>
        ✅ **Fitur Utama**:
        - Konversi berbagai satuan fisika
        - Tampilan hasil menarik dan rapi
        - Penjelasan rumus lengkap
        - Grafik perbandingan nilai
        <br><br>
        📚 Cocok untuk pelajar, mahasiswa, dosen, guru, dan profesional teknik!
    </div>
    """, unsafe_allow_html=True)

elif menu == "📐 Kalkulator":
    st.title("📐 Kalkulator Konversi Satuan")
    kategori = st.selectbox("Pilih Kategori Satuan", ["Suhu"] + list(KONVERSI_FAKTOR.keys()))
    satuan_asal = st.selectbox("Dari Satuan", [""] + (["Celsius", "Fahrenheit", "Kelvin"] if kategori == "Suhu" else list(KONVERSI_FAKTOR[kategori].keys())))
    satuan_tujuan = st.selectbox("Ke Satuan", [""] + (["Celsius", "Fahrenheit", "Kelvin"] if kategori == "Suhu" else list(KONVERSI_FAKTOR[kategori].keys())))
    nilai = st.number_input("Masukkan Nilai", format="%.6f")

    if st.button("🔄 Konversi"):
        if satuan_asal and satuan_tujuan:
            with st.spinner("Menghitung..."):
                time.sleep(1)
                hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan) if kategori == "Suhu" else konversi_umum(nilai, satuan_asal, satuan_tujuan, kategori)
                st.metric(label=f"Hasil Konversi", value=f"{hasil:.6g} {satuan_tujuan}")
                st.markdown(penjelasan_rumus(nilai, hasil, satuan_asal, satuan_tujuan, kategori))
        else:
            st.warning("Pilih satuan asal dan tujuan terlebih dahulu.")

elif menu == "📊 Grafik":
    st.title("📊 Visualisasi Perbandingan")
    st.info("Gunakan halaman Kalkulator untuk menampilkan grafik setelah melakukan konversi.")

elif menu == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
### 📌 Deskripsi

**Kalkulator Konversi Satuan Fisika** adalah alat bantu interaktif untuk melakukan konversi antar berbagai satuan fisika dengan cepat dan akurat.

### 🎯 Tujuan
- Menyederhanakan proses konversi satuan
- Menyediakan rumus dan penjelasan hasil
- Menyajikan data secara visual

### 📚 Referensi:
- [NIST - National Institute of Standards and Technology](https://physics.nist.gov/cuu/Units/)
- [BIPM - Bureau International des Poids et Mesures](https://www.bipm.org)
- [The Engineering Toolbox](https://www.engineeringtoolbox.com/)
- [Altair Chart Docs](https://altair-viz.github.io)

### 🛠 Teknologi:
- Streamlit
- Pandas
- Altair

---

💡 Dibuat dengan ❤️ untuk edukasi dan produktivitas.
    """)
