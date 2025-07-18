import streamlit as st
import time
import pandas as pd
import altair as alt

st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")
st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")
st.markdown("Konversi berbagai satuan fisika lengkap dengan penjelasan dan grafik hasil.")

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

presisi = {
    "🔥 Suhu": 2,
    "🧪 Tekanan": 2,
    "⚖ Massa": 4,
    "📏 Panjang": 4,
    "⏱ Waktu": 0,
    "⚡ Energi": 6,
    "💨 Kecepatan": 3,
    "💡 Daya": 2,
    "🧊 Volume": 4,
    "📡 Frekuensi": 2,
    "⚡ Hambatan Listrik": 2,
    "🔋 Tegangan Listrik": 2,
    "🔌 Arus Listrik": 2
}

kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
satuan_list = list(konversi_data[kategori].keys())
satuan_asal = st.selectbox("Satuan asal:", satuan_list)
satuan_tujuan = st.selectbox("Satuan tujuan:", satuan_list)
nilai_input = st.text_input("Masukkan nilai:", placeholder="contoh: 5.5")

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

if st.button("🔄 Konversi"):
    if not nilai_input:
        st.warning("⚠️ Harap masukkan nilai terlebih dahulu.")
    else:
        try:
            nilai = float(nilai_input.replace(",", "."))
            with st.spinner("⏳ Menghitung konversi..."):
                time.sleep(2)

                if kategori == "🔥 Suhu":
                    hasil = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                else:
                    faktor_asal = konversi_data[kategori][satuan_asal]
                    faktor_tujuan = konversi_data[kategori][satuan_tujuan]
                    hasil = nilai * faktor_asal / faktor_tujuan

                desimal = presisi.get(kategori, 2)
                hasil_str = f"{hasil:.{desimal}f}"
                st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")

                st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy", disabled=False)

                if kategori == "🔥 Suhu":
                    st.markdown("### 📘 Penjelasan Konversi Suhu")
                    st.markdown(f"""
                    Rumus konversi dari **{satuan_asal}** ke **{satuan_tujuan}**:

                    
{nilai} {satuan_asal} → {satuan_tujuan} = {hasil_str}

                    Penyesuaian suhu dilakukan berdasarkan transformasi antar skala suhu:

                    - °C ke °F : (°C × 9/5) + 32
                    - °C ke K : °C + 273.15
                    - °F ke °C : (°F - 32) × 5/9
                    - K ke °C : K - 273.15
                    - dan seterusnya
                    """)
                else:
                    st.markdown("### 📘 Penjelasan Konversi")
                    st.markdown("Rumus konversi satuan berdasarkan skala pengali:")

                    st.latex(r"\text{Hasil} = \text{nilai} \times \frac{\text{faktor asal}}{\text{faktor tujuan}}")
                    st.markdown("Contoh substitusi nilai:")
                    st.latex(fr"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_str}")

                    st.markdown(f"""
                    **Keterangan:**
                    - Nilai awal dikalikan dengan rasio antara faktor asal dan faktor tujuan
                    - Nilai konversi dihitung sebagai: {nilai} × ({faktor_asal} / {faktor_tujuan})
                    - Hasil dibulatkan sesuai presisi kategori ({desimal} angka di belakang koma)
                    """)

                    df = pd.DataFrame({
                        'Satuan': [satuan_asal, satuan_tujuan],
                        'Nilai': [nilai, hasil]
                    })
                    chart = alt.Chart(df).mark_bar().encode(
                        x='Satuan',
                        y='Nilai',
                        color='Satuan',
                        tooltip=['Satuan', 'Nilai']
                    ).properties(
                        title='📊 Perbandingan Nilai Sebelum dan Sesudah Konversi',
                        height=300
                    )
                    st.altair_chart(chart, use_container_width=True)

        except ValueError:
            st.error("❌ Nilai yang dimasukkan harus berupa angka (contoh: 3.5 atau 3,5).")



2/2

