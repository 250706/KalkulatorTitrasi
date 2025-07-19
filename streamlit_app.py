import streamlit as st
import pandas as pd
import time
import altair as alt

st.set_page_config(page_title="Kalkulator Konversi Fisika", layout="centered")

# ---------- DATA KONVERSI ----------
konversi_data = {
    "🔥 Suhu": {},
    "💨 Tekanan": {
        "Pa": 1, "kPa": 1e3, "atm": 101325, "bar": 1e5, "psi": 6894.76, "mmHg": 133.322
    },
    "⚖️ Massa": {
        "kg": 1, "g": 1e-3, "mg": 1e-6, "ton": 1e3
    },
    "📏 Panjang": {
        "m": 1, "cm": 1e-2, "mm": 1e-3, "km": 1e3, "inch": 0.0254, "ft": 0.3048
    },
    "⏱️ Waktu": {
        "s": 1, "min": 60, "h": 3600, "ms": 1e-3
    },
    "⚡ Energi": {
        "J": 1, "kJ": 1e3, "cal": 4.184, "kcal": 4184
    },
    "🚀 Kecepatan": {
        "m/s": 1, "km/h": 0.277778, "mph": 0.44704
    },
    "🔋 Daya": {
        "W": 1, "kW": 1e3, "hp": 745.7
    },
    "🧪 Volume": {
        "m³": 1, "L": 1e-3, "mL": 1e-6, "cm³": 1e-6
    },
    "🎵 Frekuensi": {
        "Hz": 1, "kHz": 1e3, "MHz": 1e6
    },
    "⚡ Hambatan Listrik": {
        "ohm": 1, "kΩ": 1e3, "MΩ": 1e6
    },
    "🔌 Tegangan": {
        "V": 1, "mV": 1e-3, "kV": 1e3
    },
    "🔋 Arus Listrik": {
        "A": 1, "mA": 1e-3, "μA": 1e-6
    }
}

# ---------- FUNGSI KONVERSI SUHU ----------
def konversi_suhu(nilai, dari, ke):
    if dari == ke:
        return nilai
    if dari == "°C":
        if ke == "K":
            return nilai + 273.15
        elif ke == "°F":
            return (nilai * 9/5) + 32
    elif dari == "K":
        if ke == "°C":
            return nilai - 273.15
        elif ke == "°F":
            return (nilai - 273.15) * 9/5 + 32
    elif dari == "°F":
        if ke == "°C":
            return (nilai - 32) * 5/9
        elif ke == "K":
            return (nilai - 32) * 5/9 + 273.15
    raise ValueError("Satuan suhu tidak dikenali.")

# ---------- PRESISI HASIL ----------
def format_presisi(nilai):
    if abs(nilai) >= 1000:
        return f"{nilai:,.0f}"
    elif abs(nilai) >= 100:
        return f"{nilai:,.1f}"
    elif abs(nilai) >= 1:
        return f"{nilai:,.2f}"
    else:
        return f"{nilai:.4e}"

# ---------- ANTARMUKA ----------
st.title("📐 Kalkulator Konversi Satuan Fisika")
st.markdown("Konversi satuan fisika dengan cepat dan akurat.")

kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
nilai_input = st.text_input("Masukkan nilai yang ingin dikonversi:")

if kategori == "🔥 Suhu":
    satuan_asal = st.selectbox("Dari satuan:", ["°C", "°F", "K"])
    satuan_tujuan = st.selectbox("Ke satuan:", ["°C", "°F", "K"])
else:
    satuan_asal = st.selectbox("Dari satuan:", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("Ke satuan:", list(konversi_data[kategori].keys()))

if st.button("🔄 Konversi"):
    if not nilai_input:
        st.warning("⚠ Harap masukkan nilai terlebih dahulu.")
    else:
        try:
            nilai = float(nilai_input.replace(",", "."))
            with st.spinner("⏳ Menghitung..."):
                time.sleep(1)

                if kategori == "🔥 Suhu":
                    hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                    penjelasan = """
📘 **Penjelasan Konversi Suhu**

Anda menggunakan rumus konversi suhu berdasarkan standar ilmiah internasional.  
Rumus tergantung arah konversi, contohnya:

- Celsius ⇄ Kelvin  `K = C + 273.15`
- Celsius ⇄ Fahrenheit `F = (C × 9/5) + 32`
- Fahrenheit ⇄ Kelvin `K = (F - 32) × 5/9 + 273.15`

Rumus-rumus ini digunakan dalam industri, sains, dan akademik.  
Hasil konversi ini aman digunakan untuk eksperimen dan aplikasi praktis.
"""
                else:
                    hasil = nilai * konversi_data[kategori][satuan_asal] / konversi_data[kategori][satuan_tujuan]
                    penjelasan = f"""
📘 **Penjelasan Konversi {kategori.replace('⚡','').replace('💨','').replace('🔌','').replace('🔋','')}**

Anda mengonversi satuan dengan rumus berikut:

 **Nilai Tujuan = Nilai Asal × Faktor Asal / Faktor Tujuan**

Faktor konversi didasarkan pada standar satuan internasional (SI).  
Pastikan Anda memilih satuan yang sesuai dengan konteks kebutuhan (laboratorium, industri, dll).
"""

                hasil_str = format_presisi(hasil)

                # HASIL UTAMA
                st.markdown(f"""
<div style="padding: 20px; border-radius: 15px; background-color: #001f3f; color: white; 
            border: 2px solid #39cccc; text-align: center; font-size: 24px; font-weight: bold; 
            box-shadow: 0px 0px 25px #39cccc;">
    🔄 {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}
</div>
""", unsafe_allow_html=True)

                # PENJELASAN
                st.markdown(penjelasan)

                # GRAFIK
                chart_df = pd.DataFrame({'Satuan': [satuan_asal, satuan_tujuan], 'Nilai': [nilai, hasil]})
                st.altair_chart(
                    alt.Chart(chart_df).mark_bar().encode(
                        x='Satuan', y='Nilai', color='Satuan'
                    ).properties(title="📊 Perbandingan Nilai Sebelum & Sesudah Konversi"),
                    use_container_width=True
                )

        except ValueError:
            st.error("❌ Nilai harus berupa angka.")
