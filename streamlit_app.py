import streamlit as st
import time
import base64
from pathlib import Path
import matplotlib.pyplot as plt

# ---------------- SETUP APLIKASI ----------------
st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")

# ---------------- BACKGROUND GAMBAR ----------------
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("/mnt/data/17a103c4-d68f-40a3-bf7f-ae312a73708d.jpg")  # Gunakan file upload kamu

# ---------------- DICTIONARY KONVERSI ----------------
konversi_data = {
    "Tekanan": {
        "satuan": ["atm", "Pa", "kPa", "bar", "mmHg", "psi"],
        "faktor": {"atm": 101325, "Pa": 1, "kPa": 1000, "bar": 100000, "mmHg": 133.322, "psi": 6894.76},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Suhu": {
        "satuan": ["Celsius", "Fahrenheit", "Kelvin"],
        "presisi": 2
    },
    "Massa": {
        "satuan": ["kg", "g", "mg", "lb"],
        "faktor": {"kg": 1000, "g": 1, "mg": 0.001, "lb": 453.592},
        "presisi": 3,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Panjang": {
        "satuan": ["m", "cm", "mm", "inch", "ft"],
        "faktor": {"m": 100, "cm": 1, "mm": 0.1, "inch": 2.54, "ft": 30.48},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Energi": {
        "satuan": ["J", "kJ", "cal", "kcal"],
        "faktor": {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Volume": {
        "satuan": ["L", "mL", "cm³"],
        "faktor": {"L": 1000, "mL": 1, "cm³": 1},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Waktu": {
        "satuan": ["detik", "menit", "jam", "hari"],
        "faktor": {"detik": 1, "menit": 60, "jam": 3600, "hari": 86400},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Kecepatan": {
        "satuan": ["m/s", "km/h", "mph"],
        "faktor": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Daya": {
        "satuan": ["W", "kW", "hp"],
        "faktor": {"W": 1, "kW": 1000, "hp": 745.7},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz", "GHz"],
        "faktor": {"Hz": 1, "kHz": 1000, "MHz": 1e6, "GHz": 1e9},
        "presisi": 0,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Hambatan Listrik": {
        "satuan": ["ohm", "kiloohm", "megaohm"],
        "faktor": {"ohm": 1, "kiloohm": 1000, "megaohm": 1e6},
        "presisi": 1,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Arus Listrik": {
        "satuan": ["A", "mA"],
        "faktor": {"A": 1000, "mA": 1},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
    "Tegangan Listrik": {
        "satuan": ["V", "mV", "kV"],
        "faktor": {"V": 1, "mV": 0.001, "kV": 1000},
        "presisi": 2,
        "deskripsi": "Hasil = nilai × (faktor asal / faktor tujuan)"
    },
}

# ---------------- INPUT USER ----------------
st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")
kategori = st.selectbox("Pilih kategori konversi", list(konversi_data.keys()))
data = konversi_data[kategori]

col1, col2 = st.columns(2)
asal = col1.selectbox("Dari satuan", data["satuan"])
tujuan = col2.selectbox("Ke satuan", data["satuan"])
nilai_input = st.text_input("Masukkan nilai yang akan dikonversi", placeholder="Contoh: 100")

# ---------------- KONVERSI ----------------
def konversi(nilai, asal, tujuan, faktor):
    return nilai * faktor[asal] / faktor[tujuan]

def konversi_suhu(nilai, asal, tujuan):
    if asal == tujuan:
        return nilai
    if asal == "Celsius":
        return {"Fahrenheit": nilai * 9/5 + 32, "Kelvin": nilai + 273.15}[tujuan]
    elif asal == "Fahrenheit":
        c = (nilai - 32) * 5/9
        return {"Celsius": c, "Kelvin": c + 273.15}[tujuan]
    elif asal == "Kelvin":
        c = nilai - 273.15
        return {"Celsius": c, "Fahrenheit": c * 9/5 + 32}[tujuan]

# ---------------- TOMBOL KONVERSI ----------------
if nilai_input:
    try:
        nilai = float(nilai_input.replace(",", "."))
        with st.spinner("🔄 Mengonversi..."):
            time.sleep(1.5)

            if kategori == "Suhu":
                hasil = konversi_suhu(nilai, asal, tujuan)
                presisi = data["presisi"]
                st.success(f"Hasil: {round(hasil, presisi)} {tujuan}")
                st.markdown(f"**Rumus:** Konversi suhu tergantung jenis satuannya (mis. °C → °F: ×9/5 + 32)")
            else:
                hasil = konversi(nilai, asal, tujuan, data["faktor"])
                presisi = data["presisi"]
                faktor_asal = data["faktor"][asal]
                faktor_tujuan = data["faktor"][tujuan]

                st.success(f"Hasil: {round(hasil, presisi)} {tujuan}")
                st.markdown(f"**Rumus:** {data['deskripsi']}")
                st.latex(f"\\text{{Hasil}} = {nilai} \\times \\frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {round(hasil, presisi)}")

            # ---------------- TOMBOL SALIN ----------------
            st.code(f"{round(hasil, presisi)} {tujuan}", language="markdown")

            # ---------------- GRAFIK ----------------
            fig, ax = plt.subplots()
            ax.bar([asal, tujuan], [nilai, hasil], color=["#00bfff", "#90ee90"])
            ax.set_ylabel("Nilai")
            ax.set_title("Perbandingan Konversi")
            st.pyplot(fig)

    except ValueError:
        st.error("Masukkan angka yang valid.")
