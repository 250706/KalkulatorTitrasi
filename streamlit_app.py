import streamlit as st
import time
import base64
import matplotlib.pyplot as plt

# Fungsi mengubah gambar menjadi base64
def get_base64_bg(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Pasang background dari gambar
bg_base64 = get_base64_bg("/mnt/data/07f87593-0c9b-4fe8-84af-627ea45e12ac.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")
st.markdown("Konversi antar satuan fisika lengkap dengan penjelasan dan grafik hasil.")

# Daftar kategori dan satuan
satuan_dict = {
    "Suhu": {
        "Celsius (°C)": 1, "Fahrenheit (°F)": "F", "Kelvin (K)": "K"
    },
    "Tekanan": {
        "atm": 101325, "mmHg": 133.322, "Pa": 1, "bar": 100000, "kPa": 1000
    },
    "Massa": {
        "kg": 1000, "g": 1, "mg": 0.001, "lb": 453.592, "oz": 28.3495
    },
    "Panjang": {
        "km": 100000, "m": 100, "cm": 1, "mm": 0.1, "μm": 0.0001, "nm": 1e-7, "inchi": 2.54, "kaki (ft)": 30.48, "mil": 160934
    },
    "Waktu": {
        "hari": 86400, "jam": 3600, "menit": 60, "detik (s)": 1
    },
    "Energi": {
        "joule (J)": 1, "kilojoule (kJ)": 1000, "kalori (cal)": 4.184, "kilokalori (kcal)": 4184, "elektronvolt (eV)": 1.602e-19
    },
    "Kecepatan": {
        "m/s": 1, "km/jam": 1/3.6, "mil/jam (mph)": 0.44704, "knot": 0.514444
    },
    "Daya": {
        "watt (W)": 1, "kilowatt (kW)": 1000, "horsepower (HP)": 745.7
    },
    "Volume": {
        "liter (L)": 1000, "mililiter (mL)": 1, "cm³": 1, "m³": 1e6, "galon": 3785.41
    },
    "Frekuensi": {
        "Hz": 1, "kHz": 1000, "MHz": 1e6, "GHz": 1e9
    },
    "Hambatan Listrik": {
        "ohm (Ω)": 1, "kΩ": 1000, "MΩ": 1e6
    }
}

# Pilihan kategori dan satuan
kategori = st.selectbox("📚 Pilih Kategori Satuan:", list(satuan_dict.keys()))
satuan_asal = st.selectbox("🔢 Dari Satuan:", list(satuan_dict[kategori].keys()))
satuan_tujuan = st.selectbox("🎯 Ke Satuan:", list(satuan_dict[kategori].keys()))
nilai = st.number_input("Masukkan Nilai yang Akan Dikonversi:", format="%.8f")

if st.button("🔄 Konversi"):
    with st.spinner("⏳ Menghitung konversi..."):
        time.sleep(2)

        satuan = satuan_dict[kategori]
        asal = satuan[satuan_asal]
        tujuan = satuan[satuan_tujuan]

        # Khusus suhu karena rumusnya berbeda
        if kategori == "Suhu":
            if satuan_asal == satuan_tujuan:
                hasil = nilai
                rumus = f"{nilai} {satuan_asal} = {hasil:.2f} {satuan_tujuan}"
            elif satuan_asal == "Celsius (°C)" and satuan_tujuan == "Fahrenheit (°F)":
                hasil = (nilai * 9/5) + 32
                rumus = f"{nilai}°C × 9/5 + 32 = {hasil:.2f}°F"
            elif satuan_asal == "Celsius (°C)" and satuan_tujuan == "Kelvin (K)":
                hasil = nilai + 273.15
                rumus = f"{nilai}°C + 273.15 = {hasil:.2f} K"
            elif satuan_asal == "Fahrenheit (°F)" and satuan_tujuan == "Celsius (°C)":
                hasil = (nilai - 32) * 5/9
                rumus = f"({nilai} - 32) × 5/9 = {hasil:.2f}°C"
            elif satuan_asal == "Kelvin (K)" and satuan_tujuan == "Celsius (°C)":
                hasil = nilai - 273.15
                rumus = f"{nilai} K - 273.15 = {hasil:.2f}°C"
            elif satuan_asal == "Fahrenheit (°F)" and satuan_tujuan == "Kelvin (K)":
                hasil = (nilai - 32) * 5/9 + 273.15
                rumus = f"(({nilai} - 32) × 5/9) + 273.15 = {hasil:.2f} K"
            elif satuan_asal == "Kelvin (K)" and satuan_tujuan == "Fahrenheit (°F)":
                hasil = (nilai - 273.15) * 9/5 + 32
                rumus = f"(({nilai} - 273.15) × 9/5) + 32 = {hasil:.2f}°F"
            else:
                hasil = None
                rumus = "Konversi tidak dikenali."
        else:
            hasil = nilai * asal / tujuan
            hasil = round(hasil, 6) if hasil < 100 else round(hasil, 3)
            rumus = f"Hasil = {nilai} × ({asal} / {tujuan}) = {hasil}"

        st.success(f"✅ Hasil Konversi: **{hasil} {satuan_tujuan}**")
        st.markdown("### 📘 Penjelasan:")
        st.markdown(f"**Rumus:** `{rumus}`")

        st.markdown("### 📊 Grafik Hasil:")
        fig, ax = plt.subplots()
        ax.bar(["Satuan Asal", "Satuan Tujuan"], [nilai, hasil], color=["#1f77b4", "#ff7f0e"])
        ax.set_ylabel("Nilai")
        ax.set_title("Visualisasi Konversi")
        st.pyplot(fig)

        st.markdown("### 📋 Salin Hasil:")
        st.code(f"{nilai} {satuan_asal} = {hasil} {satuan_tujuan}", language="markdown")
        st.button("📎 Salin ke Clipboard", on_click=st.balloons)

