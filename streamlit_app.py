import streamlit as st
import base64
import time
import matplotlib.pyplot as plt

# --- Fungsi untuk background ---
def set_bg_from_local(image_file_path):
    with open(image_file_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# --- Data konversi satuan ---
konversi_data = {
    "Suhu": {
        "satuan": ["Celsius", "Fahrenheit", "Kelvin"],
        "rumus": {
            ("Celsius", "Fahrenheit"): lambda c: c * 9/5 + 32,
            ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
            ("Celsius", "Kelvin"): lambda c: c + 273.15,
            ("Kelvin", "Celsius"): lambda k: k - 273.15,
            ("Fahrenheit", "Kelvin"): lambda f: (f - 32) * 5/9 + 273.15,
            ("Kelvin", "Fahrenheit"): lambda k: (k - 273.15) * 9/5 + 32,
        },
        "presisi": 2
    },
    "Tekanan": {
        "satuan": ["atm", "Pa", "mmHg", "bar"],
        "faktor": {"atm": 101325, "Pa": 1, "mmHg": 133.322, "bar": 100000},
        "presisi": 2
    },
    "Massa": {
        "satuan": ["mg", "g", "kg", "ton"],
        "faktor": {"mg": 0.001, "g": 1, "kg": 1000, "ton": 1e6},
        "presisi": 2
    },
    "Panjang": {
        "satuan": ["mm", "cm", "m", "km"],
        "faktor": {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000},
        "presisi": 3
    },
    "Waktu": {
        "satuan": ["detik", "menit", "jam", "hari"],
        "faktor": {"detik": 1, "menit": 60, "jam": 3600, "hari": 86400},
        "presisi": 2
    },
    "Energi": {
        "satuan": ["J", "kJ", "kcal"],
        "faktor": {"J": 1, "kJ": 1000, "kcal": 4184},
        "presisi": 2
    },
    "Kecepatan": {
        "satuan": ["m/s", "km/h", "mph"],
        "faktor": {"m/s": 1, "km/h": 3.6, "mph": 2.237},
        "presisi": 2
    },
    "Daya": {
        "satuan": ["W", "kW", "HP"],
        "faktor": {"W": 1, "kW": 1000, "HP": 745.7},
        "presisi": 2
    },
    "Volume": {
        "satuan": ["mL", "L", "m³"],
        "faktor": {"mL": 0.001, "L": 1, "m³": 1000},
        "presisi": 3
    },
    "Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz", "GHz"],
        "faktor": {"Hz": 1, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9},
        "presisi": 2
    },
    "Hambatan Listrik": {
        "satuan": ["ohm", "kΩ", "MΩ"],
        "faktor": {"ohm": 1, "kΩ": 1e3, "MΩ": 1e6},
        "presisi": 2
    },
    "Tegangan": {
        "satuan": ["mV", "V", "kV"],
        "faktor": {"mV": 0.001, "V": 1, "kV": 1000},
        "presisi": 2
    },
    "Arus Listrik": {
        "satuan": ["mA", "A", "kA"],
        "faktor": {"mA": 0.001, "A": 1, "kA": 1000},
        "presisi": 2
    },
}

# --- Fungsi konversi ---
def konversi(kategori, nilai, asal, tujuan):
    if kategori == "Suhu":
        rumus = konversi_data[kategori]["rumus"].get((asal, tujuan))
        return rumus(nilai) if rumus else nilai
    else:
        faktor_asal = konversi_data[kategori]["faktor"][asal]
        faktor_tujuan = konversi_data[kategori]["faktor"][tujuan]
        return nilai * (faktor_asal / faktor_tujuan)

# --- UI ---
st.set_page_config("Kalkulator Konversi Fisika", layout="centered")
set_bg_from_local("4eac359b-ce1e-4967-9ad9-8f98db7428d4.png")

st.title("🧮 Kalkulator Konversi Satuan Fisika")
st.markdown("Silakan pilih kategori, satuan, dan masukkan nilai yang ingin dikonversi.")

kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
satuan_opsi = konversi_data[kategori]["satuan"]
asal = st.selectbox("Dari satuan:", satuan_opsi)
tujuan = st.selectbox("Ke satuan:", satuan_opsi)
nilai = st.number_input("Masukkan nilai yang ingin dikonversi:", value=0.0, format="%.6f")

if st.button("Konversi"):
    with st.spinner("Menghitung konversi..."):
        time.sleep(1.5)
        hasil = konversi(kategori, nilai, asal, tujuan)
        presisi = konversi_data[kategori]["presisi"]
        hasil_bulat = round(hasil, presisi)
        
        # Penjelasan rumus
        st.subheader("📘 Penjelasan Perhitungan")
        if kategori == "Suhu":
            st.latex(r"\text{Gunakan rumus konversi suhu sesuai konversi yang dipilih}")
        else:
            st.latex(r"\text{Hasil} = \text{nilai} \times \frac{\text{faktor asal}}{\text{faktor tujuan}}")
            faktor_asal = konversi_data[kategori]["faktor"][asal]
            faktor_tujuan = konversi_data[kategori]["faktor"][tujuan]
            rumus_latex = rf"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_bulat}"
            st.latex(r"\text{Substitusi nilai:}")
            st.latex(rf"{rumus_latex}")

        # Hasil konversi
        st.success(f"Hasil konversi: **{hasil_bulat} {tujuan}**")

        # Tombol salin
        st.code(f"{nilai} {asal} = {hasil_bulat} {tujuan}")

        # Grafik batang
        fig, ax = plt.subplots()
        ax.bar(["Nilai Awal", "Hasil Konversi"], [nilai, hasil], color=["skyblue", "lightgreen"])
        ax.set_ylabel(kategori)
        st.pyplot(fig)
