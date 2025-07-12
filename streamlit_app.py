import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Standarisasi Titrasi", layout="centered", page_icon="🧪")

# Header
st.markdown("<h1 style='text-align: center;'>🧪 KALKULATOR STANDARISASI TITRASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Hitung Normalitas dan Molaritas dari hasil penimbangan dan volume larutan</p>", unsafe_allow_html=True)
st.divider()

# Fungsi perhitungan
def hitung_normalitas(gram, be, volume, faktor):
    try:
        return gram / (be * volume * faktor)
    except ZeroDivisionError:
        return 0.0

def hitung_molaritas(gram, bm, volume, faktor):
    try:
        return gram / (bm * volume * faktor)
    except ZeroDivisionError:
        return 0.0

# Form Input
with st.expander("📘 Info Rumus", expanded=False):
    st.info("""
    Rumus yang digunakan:
    
    - **Normalitas (N)** = gram / (BE × V × faktor)
    - **Molaritas (M)** = gram / (BM × V × faktor)

    **Keterangan**:
    - `gram`: Berat zat yang ditimbang (g)
    - `V`: Volume larutan (mL)
    - `BE`: Berat ekivalen
    - `BM`: Berat molekul
    - `faktor`: Faktor pengali (contoh: 1000 untuk konversi mL ke L)
    """)

st.markdown("### ✍️ Input Data Standarisasi")

metode = st.radio("🔬 Jenis perhitungan", ["Normalitas", "Molaritas"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    gram_zat = st.number_input("⚖️ Gram zat yang ditimbang (g)", min_value=0.0, format="%.4f")
    volume_larutan = st.number_input("🧪 Volume larutan (mL)", min_value=0.0, format="%.2f")
with col2:
    faktor_pengali = st.number_input("🔁 Faktor pengali", min_value=0.0001, value=1000.0, step=100.0, format="%.4f")
    nilai_bobot = st.number_input("🧬 Berat Ekivalen (BE) atau BM", min_value=0.0, format="%.4f")

st.markdown("---")
if st.button("▶️ Hitung Sekarang"):
    if gram_zat == 0 or volume_larutan == 0 or nilai_bobot == 0:
        st.warning("❗ Mohon isi semua nilai dengan benar (tidak boleh nol).")
    else:
        with st.spinner("⏳ Sedang menghitung..."):
            time.sleep(2)

            if metode == "Normalitas":
                hasil = hitung_normalitas(gram_zat, nilai_bobot, volume_larutan, faktor_pengali)
                st.success("✅ Perhitungan Normalitas selesai!")
                st.markdown(f"**🔢 Normalitas (N):** `{hasil:.4f} N`")
            else:
                hasil = hitung_molaritas(gram_zat, nilai_bobot, volume_larutan, faktor_pengali)
                st.success("✅ Perhitungan Molaritas selesai!")
                st.markdown(f"**🔢 Molaritas (M):** `{hasil:.4f} mol/L`")
