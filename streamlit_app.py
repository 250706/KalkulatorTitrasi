import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="KALKULATOR TITRASI", layout="centered")

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
    st.title("🧪 KALKULATOR TITRASI")

    st.markdown("Masukkan data titrasi dan pilih metode yang sesuai:")

    metode = st.selectbox("Pilih metode titrasi", ["Asam-Basa", "Redoks", "Kompleksometri"])

    volume_titran = st.number_input("Volume titran (mL)", min_value=0.0, format="%.2f")
    normalitas_titran = st.number_input("Normalitas titran (N)", min_value=0.0, format="%.4f")
    volume_sampel = st.number_input("Volume sampel (mL)", min_value=0.0, format="%.2f")
    valensi = st.number_input("Valensi zat yang dianalisis", min_value=1, step=1)

    st.markdown("### Data untuk menghitung %RPD")
    hasil1 = st.number_input("Hasil titrasi ulangan 1", min_value=0.0, format="%.4f")
    hasil2 = st.number_input("Hasil titrasi ulangan 2", min_value=0.0, format="%.4f")

    if st.button("Hitung"):
        # Simpan data ke session_state
        st.session_state.volume_titran = volume_titran
        st.session_state.normalitas_titran = normalitas_titran
        st.session_state.volume_sampel = volume_sampel
        st.session_state.valensi = valensi
        st.session_state.hasil1 = hasil1
        st.session_state.hasil2 = hasil2
        st.session_state.metode = metode
        st.session_state.page = "hasil"
        st.experimental_rerun()

# Halaman Hasil
elif st.session_state.page == "hasil":
    st.title("📊 Hasil Perhitungan Titrasi")

    with st.spinner("Menghitung hasil, mohon tunggu..."):
        time.sleep(2)  # Efek loading

        N = hitung_normalitas(
            st.session_state.volume_titran,
            st.session_state.normalitas_titran,
            st.session_state.volume_sampel
        )
        M = hitung_molaritas(N, st.session_state.valensi)
        RPD = hitung_rpd(st.session_state.hasil1, st.session_state.hasil2)

    st.success("✅ Perhitungan selesai!")

    st.markdown(f"**Metode Titrasi:** {st.session_state.metode}")
    st.markdown(f"**Normalitas (N):** {N
