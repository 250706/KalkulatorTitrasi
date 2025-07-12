import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="KALKULATOR TITRASI", layout="centered", page_icon="🧪")

# Header
st.markdown("<h1 style='text-align: center;'>🧪 KALKULATOR TITRASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Hitung Normalitas, Molaritas, dan %RPD dari titrasi dengan mudah</p>", unsafe_allow_html=True)
st.divider()

# Fungsi perhitungan
def hitung_normalitas(volume_titran, normalitas_titran, volume_sampel):
    if volume_sampel == 0:
        return 0.0
    return (volume_titran * normalitas_titran) / volume_sampel

def hitung_normalitas_dari_gram(gram_zat, mr, volume_sampel):
    if volume_sampel == 0 or mr == 0:
        return 0.0
    mol = gram_zat / mr
    return mol / (volume_sampel / 1000)

def hitung_molaritas(normalitas, valensi):
    if valensi == 0:
        return 0.0
    return normalitas / valensi

def hitung_rpd(nilai1, nilai2):
    try:
        return abs(nilai1 - nilai2) / ((nilai1 + nilai2) / 2) * 100
    except ZeroDivisionError:
        return 0.0

# Inisialisasi session_state
if "page" not in st.session_state:
    st.session_state.page = "input"
if "mode" not in st.session_state:
    st.session_state.mode = None
if "gram_zat" not in st.session_state:
    st.session_state.gram_zat = 0.0
if "mr" not in st.session_state:
    st.session_state.mr = 0.0

# Halaman Input
if st.session_state.page == "input":
    with st.expander("ℹ️ Tentang Kalkulator"):
        st.info("""
        Aplikasi ini digunakan untuk menghitung:
        - **Normalitas (N)**: konsentrasi zat yang bereaksi per liter larutan.
        - **Molaritas (M)**: jumlah mol zat terlarut per liter.
        - **%RPD**: tingkat presisi dua hasil titrasi (Relative Percent Difference).
        """)

    st.markdown("### 🔧 Input Data Titrasi")

    metode = st.selectbox("🔬 Pilih metode titrasi", ["Asam-Basa", "Redoks", "Kompleksometri"], help="Pilih jenis metode titrasi yang digunakan.")
    titran = st.selectbox("🧪 Pilih larutan titran", ["NaOH", "HCl", "KMnO₄", "Na₂S₂O₃", "EDTA"], help="Pilih larutan yang digunakan sebagai titran.")

    st.markdown("### 🧮 Metode perhitungan normalitas")

    mode = st.radio("Pilih metode:", ["Berdasarkan volume titran", "Berdasarkan gram zat ditimbang"], horizontal=True)

    if mode == "Berdasarkan volume titran":
        col1, col2 = st.columns(2)
        with col1:
            volume_titran = st.number_input("📏 Volume titran (mL)", min_value=0.0, format="%.2f")
            volume_sampel = st.number_input("📦 Volume sampel (mL)", min_value=0.0, format="%.2f")
        with col2:
            normalitas_titran = st.number_input("🧪 Normalitas titran (N)", min_value=0.0, format="%.4f")
            valensi = st.number_input("⚛️ Valensi zat", min_value=1, step=1)
    else:
        col3, col4 = st.columns(2)
        with col3:
            gram_zat = st.number_input("⚖️ Berat zat ditimbang (gram)", min_value=0.0, format="%.4f")
            volume_sampel = st.number_input("📦 Volume larutan (mL)", min_value=0.0, format="%.2f")
        with col4:
            mr = st.number_input("🧬 Massa molar zat (g/mol)", min_value=0.0, format="%.2f")
            valensi = st.number_input("⚛️ Valensi zat", min_value=1, step=1)

    st.markdown("### 📊 Data untuk menghitung %RPD (ulangan)")
    col5, col6 = st.columns(2)
    with col5:
        hasil1 = st.number_input("Ulangan ke-1", min_value=0.0, format="%.4f")
    with col6:
        hasil2 = st.number_input("Ulangan ke-2", min_value=0.0, format="%.4f")

    st.markdown("---")
    if st.button("▶️ Hitung Sekarang"):
        st.session_state.page = "hasil"
        st.session_state.mode = "volume" if mode == "Berdasarkan volume titran" else "gram"
        st.session_state.metode = metode
        st.session_state.titran = titran
        st.session_state.valensi = valensi
        st.session_state.hasil1 = hasil1
        st.session_state.hasil2 = hasil2
        st.session_state.volume_sampel = volume_sampel

        if st.session_state.mode == "volume":
            if volume_titran == 0 or normalitas_titran == 0 or volume_sampel == 0:
                st.warning("❗ Lengkapi semua input dengan benar.")
            else:
                st.session_state.volume_titran = volume_titran
                st.session_state.normalitas_titran = normalitas_titran
                st.rerun()
        else:
            if gram_zat == 0 or mr == 0 or volume_sampel == 0:
                st.warning("❗ Lengkapi semua input dengan benar.")
            else:
                st.session_state.gram_zat = gram_zat
                st.session_state.mr = mr
                st.rerun()

# Halaman Hasil
elif st.session_state.page == "hasil":
    st.markdown("## 📈 Hasil Perhitungan")

    with st.spinner("📡 Sedang memproses perhitungan..."):
        time.sleep(2)

        if st.session_state.mode == "volume":
            N = hitung_normalitas(
                st.session_state.volume_titran,
                st.session_state.normalitas_titran,
                st.session_state.volume_sampel
            )
        else:
            N = hitung_normalitas_dari_gram(
                st.session_state.gram_zat,
                st.session_state.mr,
                st.session_state.volume_sampel
            )

        M = hitung_molaritas(N, st.session_state.valensi)
        RPD = hitung_rpd(st.session_state.hasil1, st.session_state.hasil2)

    st.success("✅ Perhitungan selesai!")

    st.markdown(f"**🔬 Metode Titrasi:** `{st.session_state.metode}`")
    st.markdown(f"**🧪 Titran yang digunakan:** `{st.session_state.titran}`")
    st.markdown(f"**📗 Mode Perhitungan:** `{st.session_state.mode}`")
    st.markdown(f"**🧪 Normalitas (N):** `{N:.4f} N`")
    st.markdown(f"**🧫 Molaritas (M):** `{M:.4f} mol/L`")
    st.markdown(f"**📉 %RPD:** `{RPD:.2f}%`")

    st.markdown("---")
    if st.button("🔁 Kembali & Hitung Ulang"):
        st.session_state.page = "input"
        st.rerun()
