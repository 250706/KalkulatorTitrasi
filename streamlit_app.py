import streamlit as st
import time

st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🔁 KALKULATOR KONVERSI SATUAN FISIKA</h1>", unsafe_allow_html=True)
st.markdown("---")

# ================== Data Konversi ==================

konversi_data = {
    "📏 Panjang": {
        "km": 1000,
        "m": 1,
        "cm": 0.01,
        "mm": 0.001,
        "μm": 1e-6,
        "nm": 1e-9,
        "inchi": 0.0254,
        "kaki (ft)": 0.3048,
        "mil": 1609.34
    },
    "⚖ Massa": {
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.453592,
        "oz": 0.0283495
    },
    "⏱ Waktu": {
        "detik (s)": 1,
        "menit": 60,
        "jam": 3600,
        "hari": 86400
    },
    "⚡ Energi": {
        "joule (J)": 1,
        "kilojoule (kJ)": 1000,
        "kalori (cal)": 4.184,
        "kilokalori (kcal)": 4184,
        "elektronvolt (eV)": 1.602e-19
    },
    "💨 Kecepatan": {
        "m/s": 1,
        "km/jam": 1 / 3.6,
        "mil/jam (mph)": 0.44704,
        "knot": 0.514444
    },
    "💡 Daya": {
        "watt (W)": 1,
        "kilowatt (kW)": 1000,
        "horsepower (HP)": 745.7
    },
    "🧊 Volume": {
        "liter (L)": 1,
        "mililiter (mL)": 0.001,
        "cm³": 0.001,
        "m³": 1000,
        "galon": 3.78541
    },
    "🧪 Tekanan": {
        "atm": 101325,
        "Pa": 1,
        "kPa": 1000,
        "mmHg": 133.322,
        "bar": 100000
    }
}

satuan_suhu = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]

# ================ Fungsi Konversi ===================

def konversi_satuan(nilai, dari, ke, satuan_dict):
    return nilai * satuan_dict[dari] / satuan_dict[ke]

def konversi_suhu(nilai, dari, ke):
    if dari == ke:
        return nilai
    if dari == "Celsius (°C)":
        return nilai * 9/5 + 32 if ke == "Fahrenheit (°F)" else nilai + 273.15
    elif dari == "Fahrenheit (°F)":
        return (nilai - 32) * 5/9 if ke == "Celsius (°C)" else (nilai - 32) * 5/9 + 273.15
    elif dari == "Kelvin (K)":
        return nilai - 273.15 if ke == "Celsius (°C)" else (nilai - 273.15) * 9/5 + 32

# ============== Presisi Desimal Berdasarkan Kategori ==============

presisi = {
    "🔥 Suhu": 2,
    "🧪 Tekanan": 3,
    "⚖ Massa": 4,
    "📏 Panjang": 4,
    "⏱ Waktu": 2,
    "⚡ Energi": 3,
    "💨 Kecepatan": 3,
    "💡 Daya": 2,
    "🧊 Volume": 3
}

# ================ UI Input ==========================

kategori = st.selectbox("📂 Pilih jenis konversi", list(konversi_data.keys()) + ["🔥 Suhu"])

nilai_input = st.text_input("Masukkan nilai yang ingin dikonversi")

col1, col2 = st.columns(2)

with col1:
    satuan_asal = st.selectbox("Dari satuan", satuan_suhu if kategori == "🔥 Suhu" else list(konversi_data[kategori].keys()))
with col2:
    satuan_tujuan = st.selectbox("Ke satuan", satuan_suhu if kategori == "🔥 Suhu" else list(konversi_data[kategori].keys()))

# ================= Tombol dan Output =================

if st.button("🔄 Konversi"):
    if not nilai_input:
        st.warning("⚠️ Harap masukkan nilai terlebih dahulu.")
    else:
        try:
            nilai = float(nilai_input.replace(",", "."))  # Mengubah koma menjadi titik
            with st.spinner("⏳ Menghitung konversi..."):
                time.sleep(2)
                if kategori == "🔥 Suhu":
                    hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                else:
                    hasil = konversi_satuan(nilai, satuan_asal, satuan_tujuan, konversi_data[kategori])

            # Terapkan presisi per kategori
            desimal = presisi.get(kategori, 2)
            hasil_str = f"{hasil:.{desimal}f}"
            st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
        except ValueError:
            st.error("❌ Nilai yang dimasukkan harus berupa angka (contoh: 3.5 atau 3,5).")
