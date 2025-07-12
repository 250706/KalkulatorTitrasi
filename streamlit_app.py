import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Standarisasi Titrasi", layout="centered", page_icon="⚗️")

st.markdown("<h1 style='text-align: center;'>⚗️ KALKULATOR STANDARISASI TITRASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Hitung Normalitas dan Molaritas berdasarkan massa dan volume</p>", unsafe_allow_html=True)
st.divider()

# Data senyawa (contoh saja, bisa dikembangkan)
senyawa_dict = {
    "Asam-Basa": {
        "Na2CO3": {"BE": 53, "BM": 106},
        "KHP": {"BE": 204.22, "BM": 204.22},
    },
    "Permanganometri": {
        "FeSO4·7H2O": {"BE": 278.01 / 1, "BM": 278.01},
        "Oxalat": {"BE": 45, "BM": 90},
    },
    "Iodometri": {
        "Na2S2O3·5H2O": {"BE": 248.18 / 1, "BM": 248.18},
        "KI": {"BE": 166, "BM": 166},
    },
    "EDTA": {
        "CaCO3": {"BE": 50, "BM": 100},
        "MgSO4": {"BE": 60.31 / 1, "BM": 120.62},
    }
}

# Fungsi perhitungan
def hitung_normalitas(gram, BE, volume, faktor):
    if volume == 0 or BE == 0 or faktor == 0:
        return 0.0
    return gram / (BE * volume * faktor)

def hitung_molaritas(gram, BM, volume, faktor):
    if volume == 0 or BM == 0 or faktor == 0:
        return 0.0
    return gram / (BM * volume * faktor)

# Halaman input
st.markdown("### ⚙️ Input Data Standarisasi")

metode = st.selectbox("🧪 Pilih Metode Titrasi", list(senyawa_dict.keys()))
senyawa = st.selectbox("🔍 Pilih Senyawa", list(senyawa_dict[metode].keys()))

info = senyawa_dict[metode][senyawa]
BE = info["BE"]
BM = info["BM"]

col1, col2 = st.columns(2)
with col1:
    gram = st.number_input("⚖️ Massa zat ditimbang (g)", min_value=0.0, format="%.4f")
    volume = st.number_input("🧴 Volume larutan (L)", min_value=0.0, format="%.4f")
with col2:
    faktor = st.number_input("📐 Faktor pengali", min_value=0.0001, value=1.0, step=0.1, format="%.4f", help="Biasanya 1 atau 1000 untuk konversi mL ke L.")

st.markdown("---")
if st.button("▶️ Hitung Sekarang"):
    if gram == 0 or volume == 0 or faktor == 0:
        st.warning("❗ Harap isi semua data dengan benar!")
    else:
        with st.spinner("🧪 Menghitung..."):
            time.sleep(2)
            N = hitung_normalitas(gram, BE, volume, faktor)
            M = hitung_molaritas(gram, BM, volume, faktor)

        st.success("✅ Perhitungan Selesai!")
