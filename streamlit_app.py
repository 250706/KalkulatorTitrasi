import streamlit as st
import time
import pandas as pd
import altair as alt

# === Background Custom ===
def set_custom_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

image_link = "https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp"
set_custom_background(image_link)
# ==========================

st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")
st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")
st.markdown("Konversi berbagai satuan fisika lengkap dengan penjelasan dan grafik hasil.")

# === Data satuan ===
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
        "ohm (Ω)": 1,
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
        if ke == "Fahrenheit (°F)":
            return (nilai * 9/5) + 32
        elif ke == "Kelvin (K)":
            return nilai + 273.15
    elif dari == "Fahrenheit (°F)":
        if ke == "Celsius (°C)":
            return (nilai - 32) * 5/9
        elif ke == "Kelvin (K)":
            return (nilai - 32) * 5/9 + 273.15
    elif dari == "Kelvin (K)":
        if ke == "Celsius (°C)":
            return nilai - 273.15
        elif ke == "Fahrenheit (°F)":
            return (nilai - 273.15) * 9/5 + 32
    return nilai

# === Input Pengguna ===
kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
satuan_list = list(konversi_data[kategori].keys())
satuan_asal = st.selectbox("Satuan asal:", satuan_list)
satuan_tujuan = st.selectbox("Satuan tujuan:", satuan_list)
nilai_input = st.text_input("Masukkan nilai:", placeholder="contoh: 5.5")

# === Tombol Konversi ===
if st.button("🔄 Konversi"):
    if not nilai_input:
        st.warning("⚠ Harap masukkan nilai terlebih dahulu.")
    else:
        try:
            nilai = float(nilai_input.replace(",", "."))
            with st.spinner("⏳ Menghitung konversi..."):
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
                    Rumus konversi dari *{satuan_asal}* ke *{satuan_tujuan}*:

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
                    st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy2", disabled=False)

                    st.markdown("### 📘 Penjelasan Konversi")
                    st.latex(r"\text{Hasil} = \text{nilai} \times \frac{\text{faktor asal}}{\text{faktor tujuan}}")
                    st.latex(fr"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_str}")
                    st.markdown("""
                    *Keterangan:*
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

                    # Grafik batang
                    df_chart = pd.DataFrame({
                        'Satuan': [satuan_asal, satuan_tujuan],
                        'Nilai': [nilai, hasil]
                    })
                    st.altair_chart(
                        alt.Chart(df_chart).mark_bar().encode(
                            x='Satuan', y='Nilai', color='Satuan', tooltip=['Satuan', 'Nilai']
                        ).properties(
                            title='📊 Perbandingan Nilai Sebelum dan Sesudah Konversi',
                            height=300
                        ), use_container_width=True
                    )

        except ValueError:
            st.error("❌ Nilai harus berupa angka. Gunakan titik atau koma desimal.")
