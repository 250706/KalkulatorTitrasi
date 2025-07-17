import streamlit as st
import time

st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🔁 KALKULATOR KONVERSI SATUAN FISIKA</h1>", unsafe_allow_html=True)
st.markdown("---")

# ================== Data Konversi ==================

konversi_panjang = {
    "Meter (m)": 1,
    "Kilometer (km)": 1000,
    "Centimeter (cm)": 0.01,
    "Milimeter (mm)": 0.001,
    "Inci (inch)": 0.0254,
    "Kaki (foot)": 0.3048
}

konversi_massa = {
    "Kilogram (kg)": 1,
    "Gram (g)": 0.001,
    "Miligram (mg)": 0.000001,
    "Pound (lb)": 0.453592,
    "Ons (oz)": 0.0283495
}

konversi_waktu = {
    "Detik (s)": 1,
    "Menit (min)": 60,
    "Jam (h)": 3600
}

konversi_energi = {
    "Joule (J)": 1,
    "Kalori (cal)": 4.184,
    "Kilowatt-jam (kWh)": 3.6e6
}

konversi_gaya = {
    "Newton (N)": 1,
    "Dyne": 1e-5,
    "Kilogram-gaya (kgf)": 9.80665
}

satuan_suhu = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]

# ================ Fungsi Konversi ===================

def konversi_satuan(nilai, dari, ke, data_satuan):
    nilai_dalam_standar = nilai * data_satuan[dari]
    return nilai_dalam_standar / data_satuan[ke]

def konversi_suhu(nilai, dari, ke):
    if dari == ke:
        return nilai
    if dari == "Celsius (°C)":
        return nilai * 9/5 + 32 if ke == "Fahrenheit (°F)" else nilai + 273.15
    if dari == "Fahrenheit (°F)":
        return (nilai - 32) * 5/9 if ke == "Celsius (°C)" else (nilai - 32) * 5/9 + 273.15
    if dari == "Kelvin (K)":
        return nilai - 273.15 if ke == "Celsius (°C)" else (nilai - 273.15) * 9/5 + 32

# ================ UI Input ==========================

kategori = st.selectbox("📂 Pilih jenis satuan", [
    "Panjang 📏", "Massa ⚖️", "Suhu 🌡️", "Waktu ⏱️", "Energi ⚡", "Gaya 🏋️"
])

nilai = st.number_input("Masukkan nilai yang ingin dikonversi", value=0.0)

col1, col2 = st.columns(2)

with col1:
    if "Panjang" in kategori:
        satuan_asal = st.selectbox("Dari satuan", list(konversi_panjang.keys()))
    elif "Massa" in kategori:
        satuan_asal = st.selectbox("Dari satuan", list(konversi_massa.keys()))
    elif "Suhu" in kategori:
        satuan_asal = st.selectbox("Dari satuan", satuan_suhu)
    elif "Waktu" in kategori:
        satuan_asal = st.selectbox("Dari satuan", list(konversi_waktu.keys()))
    elif "Energi" in kategori:
        satuan_asal = st.selectbox("Dari satuan", list(konversi_energi.keys()))
    elif "Gaya" in kategori:
        satuan_asal = st.selectbox("Dari satuan", list(konversi_gaya.keys()))

with col2:
    if "Panjang" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", list(konversi_panjang.keys()))
    elif "Massa" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", list(konversi_massa.keys()))
    elif "Suhu" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", satuan_suhu)
    elif "Waktu" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", list(konversi_waktu.keys()))
    elif "Energi" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", list(konversi_energi.keys()))
    elif "Gaya" in kategori:
        satuan_tujuan = st.selectbox("Ke satuan", list(konversi_gaya.keys()))

# ================= Tombol dan Output =================

if st.button("🔄 Konversi"):
    with st.spinner("⏳ Menghitung konversi..."):
        time.sleep(2)
        if "Panjang" in kategori:
            hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_panjang)
        elif "Massa" in kategori:
            hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_massa)
        elif "Suhu" in kategori:
            hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
        elif "Waktu" in kategori:
            hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_waktu)
        elif "Energi" in kategori:
            hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_energi)
        elif "Gaya" in kategori:
            hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_gaya)

    st.success(f"✅ {nilai} {satuan_asal} = {hasil:.4f} {satuan_tujuan}")

