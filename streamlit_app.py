import streamlit as st
import base64
import time
import pandas as pd
import altair as alt

# ---------------------------
# KONFIGURASI DAN BACKGROUND
# ---------------------------
st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")

def set_background_from_url(image_url: str, opacity: float = 0.85):
    background_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                    url('{image_url}');
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

set_background_from_url(
    "https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp",
    0.85
)

# ---------------------------
# SIDEBAR DAN NAVIGASI
# ---------------------------
st.sidebar.title("📚 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["Beranda", "Kalkulator", "Tentang"])

# ---------------------------
# BERANDA
# ---------------------------
if halaman == "Beranda":
    st.title("👋 Selamat Datang di Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    Aplikasi ini membantu Anda mengonversi berbagai satuan fisika lengkap dengan:
    - Penjelasan konversi
    - Grafik perbandingan
    - Salin hasil
    - Tampilan interaktif dan modern

    Gunakan menu **Kalkulator** di sidebar untuk memulai.
    """)

# ---------------------------
# KALKULATOR
# ---------------------------
elif halaman == "Kalkulator":
    st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")

    konversi_data = {
        "🔥 Suhu": {
            "Celsius (°C)": "C",
            "Fahrenheit (°F)": "F",
            "Kelvin (K)": "K"
        },
        "🧪 Tekanan": {
            "atm": 101325,
            "mmHg": 133.322,
            "Pa": 1,
            "bar": 100000,
            "kPa": 1000
        },
        "⚖ Massa": {
            "kg": 1000,
            "g": 1,
            "mg": 0.001,
            "lb": 453.592,
            "oz": 28.3495
        },
        "🕏 Panjang": {
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
            "km/jam": 1000/3600,
            "mil/jam (mph)": 1609.34/3600,
            "knot": 1852/3600
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
        "📡 Frekuensi": {
            "Hz": 1,
            "kHz": 1e3,
            "MHz": 1e6,
            "GHz": 1e9
        },
        "⚡ Hambatan Listrik": {
            "ohm (Ω)": 1,
            "kΩ": 1e3,
            "MΩ": 1e6
        },
        "🔋 Tegangan Listrik": {
            "volt (V)": 1,
            "mV": 1e-3,
            "kV": 1e3
        },
        "🔌 Arus Listrik": {
            "ampere (A)": 1,
            "mA": 1e-3,
            "μA": 1e-6
        }
    }

    def format_presisi(nilai):
        if nilai == int(nilai):
            return str(int(nilai))
        elif abs(nilai) < 1:
            return f"{nilai:.4f}".rstrip('0').rstrip('.')
        elif abs(nilai) < 100:
            return f"{nilai:.3f}".rstrip('0').rstrip('.')
        else:
            return f"{nilai:.2f}".rstrip('0').rstrip('.')

    def konversi_suhu(nilai, dari, ke):
        if dari == ke:
            return nilai
        if dari == "Celsius (°C)":
            return (nilai * 9/5 + 32) if ke == "Fahrenheit (°F)" else nilai + 273.15
        if dari == "Fahrenheit (°F)":
            return (nilai - 32) * 5/9 if ke == "Celsius (°C)" else (nilai - 32) * 5/9 + 273.15
        if dari == "Kelvin (K)":
            return nilai - 273.15 if ke == "Celsius (°C)" else (nilai - 273.15) * 9/5 + 32
        return nilai

    kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
    satuan_asal = st.selectbox("Satuan asal:", list(konversi_data[kategori].keys()))
    satuan_tujuan = st.selectbox("Satuan tujuan:", list(konversi_data[kategori].keys()))
    nilai_input = st.text_input("Masukkan nilai:", placeholder="contoh: 5.5")

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
                    hasil_str = format_presisi(hasil)

                    st.metric(label="Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
                    st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy", disabled=False)

                    st.markdown("### 📘 Penjelasan Konversi Suhu")
                    st.markdown(f"""
                    Rumus konversi dari {satuan_asal} ke {satuan_tujuan}:

                    {nilai} {satuan_asal} → {satuan_tujuan} = {hasil_str}

                    Transformasi antar skala suhu:
                    - °C ke °F : (°C × 9/5) + 32
                    - °C ke K : °C + 273.15
                    - °F ke °C : (°F - 32) × 5/9
                    - K ke °C : K - 273.15
                    """)
                else:
                    faktor_asal = konversi_data[kategori][satuan_asal]
                    faktor_tujuan = konversi_data[kategori][satuan_tujuan]
                    hasil = nilai * faktor_asal / faktor_tujuan
                    hasil_str = format_presisi(hasil)

                    st.metric(label="Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
                    st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
     if kategori == "🔥 Suhu":
                    hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                    hasil_str = format_presisi(hasil)

                    st.metric(label="Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
                    st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy", disabled=False)

                    st.markdown("### 📘 Penjelasan Konversi Suhu")
                    st.markdown(f"""
                    Rumus konversi dari {satuan_asal} ke {satuan_tujuan}:

                    {nilai} {satuan_asal} → {satuan_tujuan} = {hasil_str}

                    Transformasi antar skala suhu:
                    - °C ke °F : (°C × 9/5) + 32
                    - °C ke K : °C + 273.15
                    - °F ke °C : (°F - 32) × 5/9
                    - K ke °C : K - 273.15
                    """)
                else:
                    factor_asal = konversi_data[kategori][satuan_asal]
                    factor_tujuan = konversi_data[kategori][satuan_tujuan]
                    hasil = nilai * factor_asal / factor_tujuan
                    hasil_str = format_presisi(hasil)

                    st.metric(label="Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
                    st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy2", disabled=False)

                    st.markdown("### 📘 Penjelasan Konversi")
                    st.latex(r"\text{Hasil} = \text{nilai} \times \frac{\text{faktor asal}}{\text{faktor tujuan}}")
                    st.latex(fr"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_str}")
                    st.markdown("""
                    Keterangan:
                    - Nilai dikalikan rasio antar satuan
                    - Presisi otomatis disesuaikan berdasarkan besar angka
                    """)

                    # Tabel konversi ke semua satuan dalam kategori
                    semua_konversi = {}
                    for satuan in konversi_data[kategori]:
                        faktor = konversi_data[kategori][satuan]
                        konversi = nilai * faktor_asal / faktor
                        semua_konversi[satuan] = format_presisi(konversi)

                    df_all = pd.DataFrame(list(semua_konversi.items()), columns=["Satuan", "Hasil"])
                    st.dataframe(df_all, use_container_width=True)
                    )
            except ValueError:
                st.error("❌ Nilai harus berupa angka.")

# ---------------------------
# TENTANG
# ---------------------------
elif halaman == "Tentang":
    st.header("📖 Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Kalkulator Konversi Satuan Fisika** ini membantu Anda melakukan konversi satuan dengan mudah dan akurat.

    ### 🔍 Fitur:
    - Konversi presisi otomatis
    - Penjelasan dan rumus konversi
    - Visualisasi grafik interaktif
    - Salin hasil konversi

    ### 📚 Sumber Referensi:
    - SI (Système International d'Unités)
    - NIST (National Institute of Standards and Technology)
    - *Physics for Scientists and Engineers* – Serway & Jewett
    - *Handbook of Chemistry and Physics* – CRC Press
    - [https://www.bipm.org](https://www.bipm.org)
    - *Thermodynamics* – Yunus Cengel
    - International Temperature Scale
    """)                                                 penjelasan konversi nya tidak muncul
