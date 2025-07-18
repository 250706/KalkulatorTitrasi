
import streamlit as st
import time
import pandas as pd
import altair as alt
import base64

st.set_page_config(page_title="Kalkulator Konversi Satuan Fisika", layout="centered")

# Fungsi untuk konversi gambar ke base64
def get_base64_bg(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_base64 = get_base64_bg("/mnt/data/da954ec3-975c-4134-a0b7-d488731d128e.png")

# Tambahkan background dari gambar lokal dan overlay modern
st.markdown(
    f"""
    <style>
    html, body {{
        height: 100%;
        margin: 0;
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}

    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.4);
        z-index: -1;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(5px);
    }}

    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(3px);
        border-radius: 0 0 10px 10px;
    }}

    .st-emotion-cache-1v0mbdj {{
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(6px);
        border-radius: 12px;
        padding: 1em;
        transition: all 0.3s ease-in-out;
    }}
    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)

st.title("🔬 KALKULATOR KONVERSI SATUAN FISIKA")
st.markdown("Konversi berbagai satuan fisika lengkap dengan penjelasan dan grafik hasil.")

konversi_data = {
    "Suhu": {
        "satuan": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
        "fungsi": lambda nilai, dari, ke: {
            ("Celsius (°C)", "Fahrenheit (°F)"): (nilai * 9/5) + 32,
            ("Celsius (°C)", "Kelvin (K)"): nilai + 273.15,
            ("Fahrenheit (°F)", "Celsius (°C)"): (nilai - 32) * 5/9,
            ("Fahrenheit (°F)", "Kelvin (K)"): ((nilai - 32) * 5/9) + 273.15,
            ("Kelvin (K)", "Celsius (°C)"): nilai - 273.15,
            ("Kelvin (K)", "Fahrenheit (°F)"): ((nilai - 273.15) * 9/5) + 32
        }.get((dari, ke), nilai)
    },
    "Tekanan": {
        "satuan": ["atm", "Pa", "mmHg", "bar", "kPa"],
        "faktor": {"atm": 101325, "Pa": 1, "mmHg": 133.322, "bar": 100000, "kPa": 1000}
    },
    "Massa": {
        "satuan": ["kg", "g", "mg", "lb", "oz"],
        "faktor": {"kg": 1000, "g": 1, "mg": 0.001, "lb": 453.592, "oz": 28.3495}
    },
    "Panjang": {
        "satuan": ["km", "m", "cm", "mm", "μm", "nm", "inchi", "kaki (ft)", "mil"],
        "faktor": {"km": 100000, "m": 100, "cm": 1, "mm": 0.1, "μm": 1e-4, "nm": 1e-7, "inchi": 2.54, "kaki (ft)": 30.48, "mil": 160934}
    },
    "Waktu": {
        "satuan": ["detik (s)", "menit", "jam", "hari"],
        "faktor": {"detik (s)": 1, "menit": 60, "jam": 3600, "hari": 86400}
    },
    "Energi": {
        "satuan": ["J", "kJ", "cal", "kcal", "eV"],
        "faktor": {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184, "eV": 1.602e-19}
    },
    "Kecepatan": {
        "satuan": ["m/s", "km/jam", "mil/jam (mph)", "knot"],
        "faktor": {"m/s": 1, "km/jam": 0.277778, "mil/jam (mph)": 0.44704, "knot": 0.514444}
    },
    "Daya": {
        "satuan": ["W", "kW", "HP"],
        "faktor": {"W": 1, "kW": 1000, "HP": 745.7}
    },
    "Volume": {
        "satuan": ["L", "mL", "cm³", "m³", "galon"],
        "faktor": {"L": 1, "mL": 0.001, "cm³": 0.001, "m³": 1000, "galon": 3.78541}
    },
    "Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz", "GHz"],
        "faktor": {"Hz": 1, "kHz": 1000, "MHz": 1e6, "GHz": 1e9}
    },
    "Hambatan Listrik": {
        "satuan": ["Ohm", "kOhm", "MOhm"],
        "faktor": {"Ohm": 1, "kOhm": 1000, "MOhm": 1e6}
    },
}

kategori = st.selectbox("Pilih kategori", list(konversi_data.keys()))

if kategori:
    satuan_list = konversi_data[kategori]["satuan"]
    satuan_asal = st.selectbox("Dari satuan", satuan_list)
    satuan_tujuan = st.selectbox("Ke satuan", satuan_list)
    nilai_input = st.text_input("Masukkan nilai", placeholder="contoh: 100")

    if nilai_input and satuan_asal != satuan_tujuan:
        try:
            nilai = float(nilai_input.replace(",", "."))
            with st.spinner("🔄 Menghitung konversi..."):
                time.sleep(1.5)
                if kategori == "Suhu":
                    hasil = konversi_data[kategori]["fungsi"](nilai, satuan_asal, satuan_tujuan)
                    penjelasan = f"\nRumus konversi dari {satuan_asal} ke {satuan_tujuan} digunakan sesuai standar suhu internasional."
                else:
                    faktor_asal = konversi_data[kategori]["faktor"][satuan_asal]
                    faktor_tujuan = konversi_data[kategori]["faktor"][satuan_tujuan]
                    hasil = nilai * faktor_asal / faktor_tujuan
                    penjelasan = f"\n\n**Rumus:**\n\\[ Hasil = Nilai \times \frac{{Faktor\\ Asal}}{{Faktor\\ Tujuan}} \\]"
                    penjelasan += f"\n\n**Substitusi:**\n\\[ {nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {round(hasil, 5)} \\]"

                st.success(f"**Hasil Konversi:** {round(hasil, 5)} {satuan_tujuan}")
                st.markdown(penjelasan)

                df_plot = pd.DataFrame({
                    "Satuan": [satuan_asal, satuan_tujuan],
                    "Nilai": [nilai, hasil]
                })
                st.altair_chart(
                    alt.Chart(df_plot).mark_bar().encode(
                        x="Satuan", y="Nilai", color="Satuan", tooltip=["Satuan", "Nilai"]
                    ).properties(height=300),
                    use_container_width=True
                )

                st.code(f"{nilai} {satuan_asal} = {round(hasil, 5)} {satuan_tujuan}", language="")
                st.button("Salin Hasil Konversi")

        except ValueError:
            st.error("Masukkan angka yang valid.")
