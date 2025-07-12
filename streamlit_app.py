import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="STANDARISASI TITRASI", layout="centered", page_icon="🧪")
st.title("🧪 KALKULATOR STANDARISASI TITRASI")
st.caption("Hitung Normalitas, Molaritas, dan %RPD dari hasil standarisasi titrasi")
st.divider()

# Database senyawa per metode (BM = Berat Molekul, BE = Berat Ekivalen)
data_senyawa = {
    "Asam-Basa": {
        "Na2CO3 (larutan)": (105.99, 53.00),
        "KHP (Kalium Hidrogen Ftalat)": (204.22, 204.22),
        "Boraks (Na2B4O7·10H2O)": (381.37, 190.685),
        "HCl": (36.46, 36.46),
        "NaOH (larutan)": (40.00, 40.00)
    },
    "Permanganometri": {
        "FeSO4·7H2O": (278.01, 139.00),
        "Asam Oksalat (H2C2O4·2H2O)": (126.07, 63.035),
        "Na2C2O4": (134.00, 67.00),
        "KMnO4": (158.04, 31.61)
    },
    "Iodometri": {
        "Na2S2O3·5H2O": (248.18, 124.09),
        "KIO3": (214.00, 42.80),
        "Asam Askorbat": (176.12, 88.06)
    },
    "EDTA": {
        "CaCO3": (100.09, 50.045),
        "MgSO4·7H2O": (246.47, 123.24),
        "ZnSO4·7H2O": (287.56, 143.78)
    }
}

# Fungsi perhitungan
def hitung_normalitas(gram, BE, volume_mL, faktor):
    if BE == 0 or volume_mL == 0 or faktor == 0:
        return 0.0
    return gram / (BE * volume_mL * faktor)

def hitung_molaritas(gram, BM, volume_mL, faktor):
    if BM == 0 or volume_mL == 0 or faktor == 0:
        return 0.0
    return gram / (BM * volume_mL * faktor)

def hitung_rpd(nilai1, nilai2):
    try:
        return abs(nilai1 - nilai2) / 2  # pembagi sesuai permintaan
    except ZeroDivisionError:
        return 0.0

# Input metode dan senyawa
st.markdown("### ⚙️ Pilih Metode & Senyawa")
metode = st.selectbox("Metode Titrasi", list(data_senyawa.keys()))
senyawa = st.selectbox("Senyawa yang Ditimbang", list(data_senyawa[metode].keys()))
BM, BE = data_senyawa[metode][senyawa]
st.success(f"Berat Molekul (BM): `{BM}` | Berat Ekivalen (BE): `{BE}`")

# Input data perhitungan
st.markdown("### ✏️ Input Data Standarisasi")
col1, col2 = st.columns(2)
with col1:
    gram_zat = st.number_input("⚖️ Bobot zat yang ditimbang (g)", min_value=0.0, format="%.4f")
    faktor_pengali = st.number_input("🧮 Faktor Pengali", min_value=0.0001, value=1.0, step=0.1,
