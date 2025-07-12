import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="STANDARISASI TITRASI", layout="centered", page_icon="🧪")
st.title("🧪 KALKULATOR STANDARISASI TITRASI")
st.caption("Hitung Normalitas & Molaritas dari hasil standarisasi titrasi dengan mudah dan cepat.")

st.divider()

# Database senyawa per metode
data_senyawa = {
    "Asam-Basa": {
        "Na2CO3": (105.99, 53.00),
        "KHP (Kalium Hidrogen Ftalat)": (204.22, 204.22),
        "Boraks (Na2B4O7·10H2O)": (381.37, 190.685),
        "NaOH (Larutan Standar)": (40.00, 40.00),
        "Ba(OH)2·8H2O": (315.46, 157.73),
        "HCl": (36.46, 36.46)
    },
    "Permanganometri": {
        "FeSO4·7H2O": (278.01, 139.00),
        "Asam Oksalat (H2C2O4·2H2O)": (126.07, 63.035),
        "Na2C2O4": (134.00, 67.00),
        "KMnO4": (158.04, 31.60)
    },
    "Iodometri": {
        "Na2S2O3·5H2O": (248.18, 124.09),
        "KIO3": (214.00, 42.80),
        "Asam askorbat": (176.12, 88.06),
        "I2": (253.80, 126.90)
    },
    "EDTA": {
        "CaCO3": (100.09, 50.045),
        "MgSO4·7H2O": (246.47, 123.24),
        "ZnSO4·7H2O": (287.56, 143.78),
        "EDTA (Asam etilendiamintetraasetat)": (292.24, 292.24)
    }
}

# Fungsi perhitungan
def hitung_normalitas(gram, BE, volume, faktor):
    if BE == 0 or volume == 0 or faktor == 0:
        return 0.0
    return gram / (BE * volume * faktor)

def hitung_molaritas(gram, BM, volume, faktor):
    if BM == 0 or volume == 0 or faktor == 0:
        return 0.0
    return gram / (BM * volume * faktor)

# Input pengguna
st.markdown("### ⚙️ Pilihan Metode dan Senyawa")
metode = st.selectbox("🔬 Metode Titrasi", list(data_senyawa.keys()))
senyawa = st.selectbox("🧪 Senyawa Titran", list(data_senyawa[metode].keys()))
BM, BE = data_senyawa[metode][senyawa]
st.success(f"**Berat Molekul (BM):** `{BM}` | **Berat Ekivalen (BE):** `{BE}`")

st.markdown("### ✏️ Input Data Standarisasi")

col1, col2 = st.columns(2)
with col1:
    gram_zat = st.number_input("⚖️ Bobot zat yang ditimbang (g)", min_value=0.0, format="%.4f")
    faktor_pengali = st.number_input("🧮 Faktor Pengali", min_value=0.0001, value=1000.0, step=0.1,
                                     help="Contoh: 1000 jika volume dalam mL. Biasanya 1 jika volume dalam L.")
with col2:
    volume = st.number_input("📏 Volume larutan (mL atau L)", min_value=0.0, format="%.2f")

st.markdown("---")

# Tombol hitung
if st.button("▶️ Hitung"):
    if gram_zat == 0 or volume == 0 or faktor_pengali == 0:
        st.warning("❗ Mohon isi semua input dengan benar (tidak boleh nol).")
    else:
        with st.spinner("🔬 Menghitung hasil standarisasi..."):
            time.sleep(1.5)

            N = hitung_normalitas(gram_zat, BE, volume, faktor_pengali)
            M = hitung_molaritas(gram_zat, BM, volume, faktor_pengali)

        st.success("✅ Perhitungan selesai!")
        st.markdown(f"**📘 Metode:** `{metode}`")
        st.markdown(f"**🧪 Senyawa:** `{senyawa}`")
        st.markdown(f"**📊 Normalitas (N):** `{N:.4f} N`")
        st.markdown(f"**📈 Molaritas (M):** `{M:.4f} mol/L`")

        st.divider()
        st.caption("📌 Catatan: Pastikan volume dan faktor pengali sesuai satuan (mL atau L).")
