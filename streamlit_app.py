import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import base64

# ------------------- BACKGROUND -------------------
def set_background_from_url(image_url: str, opacity: float = 0.85):
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,{opacity}), rgba(255,255,255,{opacity})), 
                    url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ------------------- KONVERSI DATA -------------------
konversi_data = {
    "🔥 Suhu": {
        "Celsius (°C)": 1,
        "Fahrenheit (°F)": None,
        "Kelvin (K)": None
    },
    "📏 Panjang": {
        "Meter (m)": 1,
        "Kilometer (km)": 1e-3,
        "Centimeter (cm)": 1e2,
        "Milimeter (mm)": 1e3,
        "Inci (in)": 39.3701,
        "Kaki (ft)": 3.28084,
        "Yard (yd)": 1.09361,
        "Mil (mi)": 0.000621371
    },
    "⚖️ Massa": {
        "Kilogram (kg)": 1,
        "Gram (g)": 1000,
        "Miligram (mg)": 1e6,
        "Ton (t)": 0.001,
        "Pon (lb)": 2.20462,
        "Ons (oz)": 35.274
    },
    "⏱️ Waktu": {
        "Detik (s)": 1,
        "Menit (min)": 1/60,
        "Jam (h)": 1/3600,
        "Hari (d)": 1/86400
    },
    "🔊 Volume": {
        "Liter (L)": 1,
        "Mililiter (mL)": 1000,
        "Centimeter Kubik (cm³)": 1000,
        "Meter Kubik (m³)": 0.001,
        "Gallon (gal)": 0.264172
    },
    "⚡ Energi": {
        "Joule (J)": 1,
        "Kilojoule (kJ)": 0.001,
        "Kalori (cal)": 0.239006,
        "Kilokalori (kcal)": 0.000239006
    },
    "💨 Kecepatan": {
        "m/s": 1,
        "km/h": 3.6,
        "mph": 2.23694,
        "knot": 1.94384
    },
    "⚡ Daya": {
        "Watt (W)": 1,
        "Kilowatt (kW)": 0.001,
        "Horsepower (hp)": 0.00134102
    },
    "🧭 Tekanan": {
        "Pascal (Pa)": 1,
        "Bar": 1e-5,
        "Atmosfer (atm)": 9.8692e-6,
        "Torr (mmHg)": 0.00750062
    },
    "📻 Frekuensi": {
        "Hertz (Hz)": 1,
        "Kilohertz (kHz)": 1e-3,
        "Megahertz (MHz)": 1e-6
    },
    "🔌 Hambatan Listrik": {
        "Ohm (Ω)": 1,
        "Kiloohm (kΩ)": 1e-3,
        "Megaohm (MΩ)": 1e-6
    },
    "⚡ Tegangan": {
        "Volt (V)": 1,
        "Kilovolt (kV)": 1e-3
    },
    "🔋 Arus Listrik": {
        "Ampere (A)": 1,
        "Miliampere (mA)": 1000
    }
}

# ------------------- HALAMAN -------------------
st.set_page_config(page_title="Kalkulator Konversi Fisika", layout="wide")
set_background_from_url("https://storage.googleapis.com/chat-temp-files/4eac359b-ce1e-4967-9ad9-8f98db7428d4.png", opacity=0.85)

# ------------------- SIDEBAR -------------------
st.sidebar.title("🔍 Navigasi")
halaman = st.sidebar.radio("Pilih halaman", ["Beranda", "Kalkulator", "Grafik", "Tentang"])

# ------------------- BERANDA -------------------
if halaman == "Beranda":
    st.title("🧪 Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Selamat datang di aplikasi **Konversi Satuan Fisika**!  
    Gunakan menu **Kalkulator** di sidebar untuk memulai 🚀  
    """)

# ------------------- KALKULATOR -------------------
elif halaman == "Kalkulator":
    st.header("🧮 Kalkulator Konversi")

    kategori = st.selectbox("📂 Pilih kategori satuan", list(konversi_data.keys()))
    satuan_asal = st.selectbox("🔹 Dari", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("🔸 Ke", list(konversi_data[kategori].keys()))
    nilai = st.number_input("📥 Masukkan nilai", format="%.6f")

    if st.button("🔄 Konversi"):
        with st.spinner("Menghitung..."):
            time.sleep(1)
            if kategori == "🔥 Suhu":
                def konversi_suhu(n, dari, ke):
                    if dari == ke:
                        return n
                    if dari == "Celsius (°C)":
                        if ke == "Fahrenheit (°F)": return n * 9/5 + 32
                        elif ke == "Kelvin (K)": return n + 273.15
                    if dari == "Fahrenheit (°F)":
                        if ke == "Celsius (°C)": return (n - 32) * 5/9
                        elif ke == "Kelvin (K)": return (n - 32) * 5/9 + 273.15
                    if dari == "Kelvin (K)":
                        if ke == "Celsius (°C)": return n - 273.15
                        elif ke == "Fahrenheit (°F)": return (n - 273.15) * 9/5 + 32
                    return None

                hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
            else:
                hasil = nilai * konversi_data[kategori][satuan_asal] / konversi_data[kategori][satuan_tujuan]

            hasil_str = f"{hasil:.6g}"
            st.metric(label=f"Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
            st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")

            # Penjelasan
            with st.expander("📘 Penjelasan Konversi"):
                if kategori == "🔥 Suhu":
                    if satuan_asal == "Celsius (°C)" and satuan_tujuan == "Fahrenheit (°F)":
                        st.latex(r"T(\degree F) = T(\degree C) \times \frac{9}{5} + 32")
                    elif satuan_asal == "Celsius (°C)" and satuan_tujuan == "Kelvin (K)":
                        st.latex(r"T(K) = T(\degree C) + 273.15")
                    elif satuan_asal == "Fahrenheit (°F)" and satuan_tujuan == "Celsius (°C)":
                        st.latex(r"T(\degree C) = (T(\degree F) - 32) \times \frac{5}{9}")
                    elif satuan_asal == "Fahrenheit (°F)" and satuan_tujuan == "Kelvin (K)":
                        st.latex(r"T(K) = (T(\degree F) - 32) \times \frac{5}{9} + 273.15")
                    elif satuan_asal == "Kelvin (K)" and satuan_tujuan == "Celsius (°C)":
                        st.latex(r"T(\degree C) = T(K) - 273.15")
                    elif satuan_asal == "Kelvin (K)" and satuan_tujuan == "Fahrenheit (°F)":
                        st.latex(r"T(\degree F) = (T(K) - 273.15) \times \frac{9}{5} + 32")
                else:
                    st.latex(r"\text{Hasil} = \text{Nilai} \times \frac{\text{faktor dari satuan asal}}{\text{faktor dari satuan tujuan}}")
                    st.markdown(f"**Perhitungan:**  \n"
                                f"{nilai} × ({konversi_data[kategori][satuan_asal]} / {konversi_data[kategori][satuan_tujuan]}) = **{hasil_str} {satuan_tujuan}**")

            # Tabel konversi ke semua satuan lain
            if kategori != "🔥 Suhu":
                data_konversi = {
                    satuan: round(nilai * konversi_data[kategori][satuan_asal] / faktor, 6)
                    for satuan, faktor in konversi_data[kategori].items()
                }
                df = pd.DataFrame(data_konversi.items(), columns=["Satuan", "Hasil"])
                st.dataframe(df)

            st.button("📋 Salin hasil", help="Klik kanan untuk salin hasil secara manual.")

# ------------------- GRAFIK -------------------
elif halaman == "Grafik":
    st.header("📊 Visualisasi Konversi")
    kategori = st.selectbox("📂 Pilih kategori", list(konversi_data.keys()), key="grafik_kategori")
    satuan_asal = st.selectbox("🔹 Dari", list(konversi_data[kategori].keys()), key="grafik_dari")
    nilai = st.number_input("📥 Nilai yang dikonversi", key="grafik_nilai")

    if kategori != "🔥 Suhu":
        hasil_data = {
            satuan: nilai * konversi_data[kategori][satuan_asal] / faktor
            for satuan, faktor in konversi_data[kategori].items()
        }
        fig, ax = plt.subplots()
        ax.barh(list(hasil_data.keys()), list(hasil_data.values()))
        ax.set_xlabel("Hasil Konversi")
        ax.set_title(f"Grafik Konversi dari {satuan_asal}")
        st.pyplot(fig)
    else:
        st.warning("Grafik tidak tersedia untuk konversi suhu.")

# ------------------- TENTANG -------------------
elif halaman == "Tentang":
    st.header("📘 Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini dibuat untuk memudahkan konversi satuan fisika secara cepat dan akurat.

    ### 📚 Sumber Referensi:
    - [BIPM - SI Units](https://www.bipm.org)
    - Serway & Jewett – *Physics for Scientists and Engineers*
    - CRC Handbook of Chemistry and Physics
    - Yunus Cengel – *Thermodynamics*
    - NIST (National Institute of Standards and Technology)

    """)
