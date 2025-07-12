import streamlit as st
import time
from streamlit_extras.let_it_rain import rain

# Konfigurasi halaman
st.set_page_config(page_title="KALKULATOR TITRASI", layout="centered", page_icon="🧪")

# Header dengan logo atau ikon
st.markdown("<h1 style='text-align: center;'>🧪 KALKULATOR TITRASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Hitung Normalitas, Molaritas, dan %RPD dari titrasi dengan mudah</p>", unsafe_allow_html=True)
st.divider()

# Fungsi perhitungan
def hitung_normalitas(volume_titran, normalitas_titran, volume_sampel):
    return (volume_titran * normalitas_titran) / volume_sampel

def hitung_molaritas(normalitas, valensi):
    return normalitas / valensi

def hitung_rpd(nilai1, nilai2):
    try:
        return abs(nilai1 - nilai2) / ((nilai1 + nilai2) / 2) * 100
    except ZeroDivisionError:
        return 0.0

# Navigasi antar halaman
if "page" not in st.session_state:
    st.session_state.page = "input"

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

    col1, col2 = st.columns(2)
    with col1:
        volume_titran = st.number_input("📏 Volume titran (mL)", min_value=0.0, format="%.2f", help="Volume larutan titran yang digunakan.")
        volume_sampel = st.number_input("📦 Volume sampel (mL)", min_value=0.0, format="%.2f", help="Volume larutan sampel yang dititrasi.")
    with col2:
        normalitas_titran = st.number_input("🧪 Normalitas titran (N)", min_value=0.0, format="%.4f", help="Konsentrasi larutan titran.")
        valensi = st.number_input("⚛️ Valensi zat", min_value=1, step=1, help="Jumlah elektron yang ditukar dalam reaksi.")

    st.markdown("### 📊 Data untuk menghitung %RPD (ulangan)")

    col3, col4 = st.columns(2)
    with col3:
        hasil1 = st.number_input("Ulangan ke-1", min_value=0.0, format="%.4f")
    with col4:
        hasil2 = st.number_input("Ulangan ke-2", min_value=0.0, format="%.4f")

    st.markdown("---")
    if st.button("▶️ Hitung Sekarang"):
        st.session_state.volume_titran = volume_titran
        st.session_state.normalitas_titran = normalitas_titran
        st.session_state.volume_sampel = volume_sampel
        st.session_state.valensi = valensi
        st.session_state.hasil1 = hasil1
        st.session_state.hasil2 = hasil2
        st.session_state.metode = metode
        st.session_state.page = "hasil"
        st.rerun()

# Halaman Hasil
elif st.session_state.page == "hasil":
    st.markdown("## 📈 Hasil Perhitungan")

    with st.spinner("📡 Sedang memproses perhitungan..."):
        time.sleep(2)  # Efek loading
        rain(emoji="💧", font_size=20, falling_speed=5, animation_length="short")  # Efek animasi hujan

        N = hitung_normalitas(
            st.session_state.volume_titran,
            st.session_state.normalitas_titran,
            st.session_state.volume_sampel
        )
        M = hitung_molaritas(N, st.session_state.valensi)
        RPD = hitung_rpd(st.session_state.hasil1, st.session_state.hasil2)

    st.success("✅ Perhitungan selesai!")

    st.markdown(f"**🔬 Metode Titrasi:** `{st.session_state.metode}`")
    st.markdown(f"**🧪 Normalitas (N):** `{N:.4f} N`")
    st.markdown(f"**🧫 Molaritas (M):** `{M:.4f} mol/L`")
    st.markdown(f"**📉 %RPD:** `{RPD:.2f}%`")

    st.markdown("---")
    if st.button("🔁 Kembali & Hitung Ulang"):
        st.session_state.page = "input"
        st.rerun()
