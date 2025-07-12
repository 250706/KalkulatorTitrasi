import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="STANDARISASI TITRASI", layout="centered", page_icon="🧪")
st.title("🧪 KALKULATOR STANDARISASI TITRASI")
st.caption("Hitung Normalitas, Molaritas, dan %RPD dari hasil standarisasi titrasi")

st.divider()

# Database senyawa per metode
data_senyawa = {
    "Asam-Basa": {
        "Na2CO3": (105.99, 53),
        "KHP (Kalium Hidrogen Ftalat)": (204.22, 204.22),
        "Boraks (Na2B4O7·10H2O)": (381.37, 190.685),
        "HCl (larutan standar)": (36.46, 36.46),
        "NaOH (larutan standar)": (40.00, 40.00)
    },
    "Permanganometri": {
        "FeSO4·7H2O": (278.01, 139),
        "Asam Oksalat (H2C2O4·2H2O)": (126.07, 63.035),
        "Na2C2O4": (134.00, 67.00),
        "KMnO4": (158.04, 31.608)
    },
    "Iodometri": {
        "Na2S2O3·5H2O": (248.18, 124.09),
        "KIO3": (214.00, 42.8),
        "Asam askorbat": (176.12, 88.06)
    },
    "EDTA": {
        "CaCO3": (100.09, 50.045),
        "MgSO4·7H2O": (246.47, 123.24),
        "ZnSO4·7H2O": (287.56, 143.78)
    }
}

# Fungsi perhitungan
def hitung_normalitas(gram, BE, volume, faktor):
    try:
        return gram / (BE * volume * faktor)
    except ZeroDivisionError:
        return 0.0

def hitung_molaritas(gram, BM, volume, faktor):
    try:
        return gram / (BM * volume * faktor)
    except ZeroDivisionError:
        return 0.0

def hitung_rpd(nilai1, nilai2):
    try:
        return abs(nilai1 - nilai2) / ((nilai1 + nilai2) / 2) * 100
    except ZeroDivisionError:
        return 0.0

# Pilihan metode & senyawa
st.markdown("### ⚙️ Pilihan Metode dan Senyawa")
metode = st.selectbox("Metode Titrasi", list(data_senyawa.keys()))
senyawa = st.selectbox("Senyawa yang Ditimbang", list(data_senyawa[metode].keys()))
BM, BE = data_senyawa[metode][senyawa]
st.success(f"Berat Molekul (BM): `{BM}` | Berat Ekivalen (BE): `{BE}`")

# Input data standarisasi
st.markdown("### ✏️ Input Data Standarisasi")
col1, col2 = st.columns(2)
with col1:
    gram_zat = st.number_input("⚖️ Bobot zat ditimbang (g)", min_value=0.0, format="%.4f")
    faktor_pengali = st.number_input("🧮 Faktor Pengali", min_value=0.0001, value=1.0, step=0.1, help="Biasanya 1 jika volume dalam liter, atau 1000 jika volume dalam mL.")
with col2:
    volume = st.number_input("📏 Volume larutan (L)", min_value=0.0, format="%.4f")

# Input untuk RPD
st.markdown("### 📊 Data Ulangan untuk %RPD")
col3, col4 = st.columns(2)
with col3:
    hasil1 = st.number_input("🔁 Ulangan ke-1", min_value=0.0, format="%.4f")
with col4:
    hasil2 = st.number_input("🔁 Ulangan ke-2", min_value=0.0, format="%.4f")

st.markdown("---")

# Tombol Hitung
if st.button("▶️ Hitung Standarisasi"):
    if gram_zat == 0 or volume == 0 or faktor_pengali == 0:
        st.warning("❗ Mohon isi semua input dengan benar (tidak boleh nol).")
    else:
        with st.spinner("🔬 Menghitung hasil standarisasi..."):
            time.sleep(1.5)
            N = hitung_normalitas(gram_zat, BE, volume, faktor_pengali)
            M = hitung_molaritas(gram_zat, BM, volume, faktor_pengali)
            RPD = hitung_rpd(hasil1, hasil2)

        st.success("✅ Perhitungan selesai!")
        st.markdown(f"**📘 Metode:** `{metode}`")
        st.markdown(f"**🧪 Senyawa:** `{senyawa}`")
        st.markdown(f"**📦 Berat Zat:** `{gram_zat:.4f} g`")
        st.markdown(f"**📏 Volume:** `{volume:.4f} L` (× Faktor: {faktor_pengali})")
        st.markdown("---")
        st.markdown(f"**🧪 Normalitas (N):** `{N:.4f} N`")
        st.markdown(f"**🧫 Molaritas (M):** `{M:.4f} mol/L`")
        st.markdown(f"**📉 %RPD:** `{RPD:.2f}%`")
