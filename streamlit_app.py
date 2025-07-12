import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Kalkulator Standarisasi Titrasi", layout="centered", page_icon="🧪")
st.title("🧪 Kalkulator Standarisasi Titrasi")
st.markdown("Hitung **Normalitas (N)** dan **Molaritas (M)** berdasarkan berat zat dan volume larutan.")

# Data senyawa (BM dan BE per metode)
data_senyawa = {
    "Asam-Basa": {
        "Na2CO3": (105.99, 52.995),
        "HCl": (36.46, 36.46),
        "NaOH": (40.00, 40.00),
        "CH3COOH": (60.05, 60.05),
        "KOH": (56.11, 56.11),
    },
    "Permanganometri": {
        "Oxalat (C2O4)": (88.02, 44.01),
        "Fe2+": (111.70, 55.85),
        "KMnO4": (158.04, 31.61),
        "H2C2O4·2H2O": (126.07, 63.03),
    },
    "Iodometri": {
        "Na2S2O3": (158.11, 79.06),
        "I2": (253.81, 126.90),
        "Vitamin C (Asam Askorbat)": (176.12, 88.06),
        "KIO3": (214.00, 42.8),
    },
    "EDTA": {
        "CaCO3": (100.09, 50.045),
        "MgSO4": (120.37, 60.185),
        "ZnSO4": (161.47, 80.735),
        "EDTA (disodium)": (372.24, 372.24),
    }
}

# Pilih metode titrasi
st.markdown("### 🔬 Pilih Metode dan Senyawa")
metode = st.selectbox("Metode Titrasi", list(data_senyawa.keys()))
senyawa = s
