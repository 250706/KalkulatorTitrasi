import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Kalkulator Standarisasi Titrasi", layout="centered", page_icon="🧪")
st.title("🧪 Kalkulator Standarisasi Titrasi")
st.markdown("Hitung **Normalitas** dan **Molaritas** berdasarkan berat zat & volume larutan.")

# Data senyawa: {metode: {nama_senyawa: (BM, BE)}}
data_senyawa = {
    "Asam-Basa": {
        "Na2CO3": (105.99, 52.995),
        "HCl": (36.46, 36.46),
        "NaOH": (40.00, 40.00),
        "CH3COOH": (60.05, 60.05),
    },
    "Permanganometri": {
        "Oxalat (C2O4)": (88.02, 44.01),
        "Fe2+": (55.85 * 2, 55.85),
        "KMnO4": (158.04, 31.608),
    },
    "Iodometri": {
        "Na2S2O3": (158.11, 79.06),
        "I2": (253.81, 126.90),
        "Vitamin C (Asam Askorbat)": (176.12, 88.06),
    },
    "EDTA": {
        "CaCO3": (100.09, 50.045),
        "MgSO4": (120.37, 60.185),
        "ZnSO4": (161.47, 80.735),
    }
}

# Pilih metode
st.markdown("### 🔬 Pilih Metode Titrasi & Senyawa")
metode = st.selectbox("Metode Titrasi", list(data_senyawa.keys()))

# Pilih senyawa berdasarkan metode
senyawa_terpilih = st.selectbox("Senyawa", list(data_senyawa[metode].keys()))

# Ambil BM dan BE otomatis
BM, BE = data_senyawa[metode][senyawa_terpilih]
st.success(f"📘 Berat Molekul (BM): **{BM}**, Berat Ekivalen (BE): **{BE}**")

# Input pengguna
st.markdown("### 🧪 Input Data Standarisasi")
col1, col2 = st.columns(2)
with col1:
    gram_zat = st.number_input("Berat zat (gram)", min_value=0.0, format="%.4f")
    faktor_pengali = st.number_input("Faktor Pengali", min_value=0.0, value=1000.0, format="%.1f", help="Biasanya 1000 untuk mengubah volume dari mL ke L")
with col2:
    volume_larutan = st.number_input("Volume larutan (mL)", min_value=0.0, format="%.2f")

# Tombol hitung
if st.button("▶️ Hitung Sekarang"):
    if gram_zat == 0 or volume_larutan == 0 or BE == 0 or BM == 0 or faktor_pengali == 0:
        st.err
