import streamlit as st
import pandas as pd
import altair as alt
import time

# ---------------------- BACKGROUND ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,{opacity}), rgba(0,0,0,{opacity})), 
                        url('{image_url}');
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://i.pinimg.com/originals/4e/ac/35/4eac359bce1e49679ad98f98db7428d4.png")

# ---------------------- METRIC HIGHLIGHT ----------------------
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #001F3F;
    padding: 20px;
    border-radius: 15px;
    color: white;
    border: 2px solid #39CCCC;
    box-shadow: 0px 0px 15px 2px #39CCCC;
}
div[data-testid="metric-container"]:hover {
    box-shadow: 0px 0px 25px 5px #7FDBFF;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# ---------------------- KONVERSI DATA ----------------------
konversi_data = {
    "🔥 Suhu": {
        "Celsius (°C)": "C",
        "Fahrenheit (°F)": "F",
        "Kelvin (K)": "K"
    },
    "⚖ Massa": {
        "kg": 1000,
        "g": 1,
        "mg": 0.001
    },
    "⏱ Waktu": {
        "detik (s)": 1,
        "menit": 60,
        "jam": 3600
    },
    "🧪 Tekanan": {
        "atm": 101325,
        "mmHg": 133.322,
        "Pa": 1
    },
    "💡 Daya": {
        "watt (W)": 1,
        "kilowatt (kW)": 1000
    },
    "💨 Kecepatan": {
        "m/s": 1,
        "km/jam": 1000/3600,
        "mil/jam (mph)": 1609.34/3600
    }
}

# ---------------------- LOGIKA KONVERSI ----------------------
def format_presisi(nilai):
    if nilai == int(nilai):
        return str(int(nilai))
    elif abs(nilai) < 1:
        return f"{nilai:.4f}".rstrip('0').rstrip('.')
    elif abs(nilai) < 100:
        return f"{nilai:.3f}".rstrip('0').rstrip('.')
    else:
        return f"{nilai:.2f}".rstrip('0').rstrip('.')

def konversi_suhu(n, dari, ke):
    if dari == ke:
        return n
    if dari == "Celsius (°C)":
        return (n * 9/5 + 32) if ke == "Fahrenheit (°F)" else n + 273.15
    if dari == "Fahrenheit (°F)":
        return (n - 32) * 5/9 if ke == "Celsius (°C)" else (n - 32) * 5/9 + 273.15
    if dari == "Kelvin (K)":
        return n - 273.15 if ke == "Celsius (°C)" else (n - 273.15) * 9/5 + 32

def penjelasan_rumus(kategori, nilai, dari, ke, hasil):
    if kategori == "🔥 Suhu":
        if dari == "Celsius (°C)" and ke == "Fahrenheit (°F)":
            return f"""
            **Rumus:**  
            $F = C \\times \\frac{{9}}{{5}} + 32$  
            $F = {nilai} \\times \\frac{{9}}{{5}} + 32 = {format_presisi(hasil)}\ °F$
            """
        elif dari == "Celsius (°C)" and ke == "Kelvin (K)":
            return f"""
            **Rumus:**  
            $K = C + 273.15$  
            $K = {nilai} + 273.15 = {format_presisi(hasil)}\ K$
            """
        elif dari == "Kelvin (K)" and ke == "Celsius (°C)":
            return f"""
            **Rumus:**  
            $C = K - 273.15$  
            $C = {nilai} - 273.15 = {format_presisi(hasil)}\ °C$
            """
        elif dari == "Fahrenheit (°F)" and ke == "Celsius (°C)":
            return f"""
            **Rumus:**  
            $C = (F - 32) \\times \\frac{{5}}{{9}}$  
            $C = ({nilai} - 32) \\times \\frac{{5}}{{9}} = {format_presisi(hasil)}\ °C$
            """
    else:
        faktor_asal = konversi_data[kategori][dari]
        faktor_tujuan = konversi_data[kategori][ke]
        return f"""
        **Rumus:**  
        \\[
        \\text{{Hasil}} = \\text{{Nilai}} \\times \\frac{{\\text{{Faktor Satuan Asal}}}}{{\\text{{Faktor Satuan Tujuan}}}} \\\\
        = {nilai} \\times \\frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {format_presisi(hasil)}\ {ke}
        \\]
        """

# ---------------------- UI UTAMA ----------------------
st.title("✨ KALKULATOR KONVERSI SATUAN FISIKA")

kategori = st.selectbox("Pilih kategori:", list(konversi_data.keys()))
satuan_asal = st.selectbox("Satuan asal:", list(konversi_data[kategori].keys()))
satuan_tujuan = st.selectbox("Satuan tujuan:", list(konversi_data[kategori].keys()))
nilai_input = st.text_input("Masukkan nilai:", placeholder="Contoh: 10.5")

if st.button("🔄 Konversi"):
    if not nilai_input:
        st.warning("⚠ Silakan masukkan nilai terlebih dahulu.")
    else:
        try:
            nilai = float(nilai_input.replace(",", "."))
            with st.spinner("⏳ Menghitung..."):
                time.sleep(1)

                if kategori == "🔥 Suhu":
                    hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                else:
                    hasil = nilai * konversi_data[kategori][satuan_asal] / konversi_data[kategori][satuan_tujuan]

                hasil_str = format_presisi(hasil)

                st.metric("💡 Hasil Konversi", f"{hasil_str} {satuan_tujuan}")
                st.success(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")

                # Penjelasan Rumus
                st.markdown("### 📘 Penjelasan Konversi")
                st.markdown(penjelasan_rumus(kategori, nilai, satuan_asal, satuan_tujuan, hasil))

                # Grafik Batang
                st.altair_chart(
                    alt.Chart(pd.DataFrame({
                        'Satuan': [satuan_asal, satuan_tujuan],
                        'Nilai': [nilai, hasil]
                    })).mark_bar().encode(
                        x='Satuan',
                        y='Nilai',
                        color='Satuan'
                    ).properties(title="📊 Grafik Perbandingan Nilai"),
                    use_container_width=True
                )

                # Salin Hasil
                st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", disabled=False)

        except ValueError:
            st.error("❌ Nilai harus berupa angka valid.")
