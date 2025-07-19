import streamlit as st
import pandas as pd
import time
import altair as alt

# ---------------------- DATA KONVERSI ----------------------
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

# ---------------------- FUNGSI KONVERSI ----------------------
def konversi_satuan(kategori, nilai, satuan_dari, satuan_ke):
    if kategori == "Suhu":
        return konversi_data[kategori][satuan_dari](nilai, satuan_ke)
    else:
        return nilai * konversi_data[kategori][satuan_dari] / konversi_data[kategori][satuan_ke]

def get_konversi_semua_satuan(kategori, nilai, satuan_dari):
    hasil = {}
    for satuan_ke in konversi_data[kategori]:
        hasil[satuan_ke] = konversi_satuan(kategori, nilai, satuan_dari, satuan_ke)
    return hasil

# ---------------------- PENJELASAN RUMUS ----------------------
def tampilkan_penjelasan_rumus(kategori, satuan_dari, satuan_ke):
    if kategori == "Suhu":
        rumus_dict = {
            ("Celsius", "Fahrenheit"): "`(°C × 9/5) + 32 = °F`",
            ("Fahrenheit", "Celsius"): "`(°F − 32) × 5/9 = °C`",
            ("Celsius", "Kelvin"): "`°C + 273.15 = K`",
            ("Kelvin", "Celsius"): "`K − 273.15 = °C`",
            ("Fahrenheit", "Kelvin"): "`((°F − 32) × 5/9) + 273.15 = K`",
            ("Kelvin", "Fahrenheit"): "`((K − 273.15) × 9/5) + 32 = °F`"
        }
        rumus = rumus_dict.get((satuan_dari, satuan_ke), "*Rumus tidak tersedia*")
        st.markdown(f"### 📘 Rumus Konversi\n**{satuan_dari} ➝ {satuan_ke}**\n\n{rumus}")
    else:
        st.markdown(f"""
        ### 📘 Rumus Konversi
        **{satuan_dari} ➝ {satuan_ke}**

        $$\\text{{Hasil}} = \\text{{Nilai}} \\times \\frac{{\\text{{Konstanta dari {satuan_dari}}}}}{{\\text{{Konstanta dari {satuan_ke}}}}}$$
        """)
# ---------------------- TEMA & BACKGROUND ----------------------
def set_custom_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

image_link = "https://cdn.bhdw.net/im/chemistry-and-physics-symbols-on-black-board-wallpaper-108136_w635.webp"

set_custom_background(image_link)

# ---------------------- NAVIGASI SIDEBAR ----------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "📐 Kalkulator", "ℹ️ Tentang"])

# ---------------------- HALAMAN BERANDA ----------------------
if halaman == "🏠 Beranda":
    st.title("📐 Kalkulator Konversi Satuan Fisika")
    st.markdown("""
    <div style='text-align: justify; font-size: 18px'>
    Selamat datang di **Kalkulator Konversi Satuan Fisika**! 🔍  
    Aplikasi ini dirancang untuk memudahkan Anda dalam mengonversi berbagai satuan dalam ilmu fisika secara cepat, akurat, dan dengan penjelasan yang mudah dipahami.  
    Cukup masukkan nilai, pilih kategori, dan satuan asal serta tujuan — maka hasil dan penjelasan lengkap akan langsung muncul!  

    ### ✨ Fitur Unggulan:
    - ✅ Konversi berbagai kategori: suhu, massa, tekanan, energi, kecepatan, dan banyak lagi.
    - 📘 Penjelasan rumus lengkap.
    - 📊 Visualisasi hasil konversi dalam grafik interaktif.
    - 🎨 Tampilan bersih dan elegan.

    Ayo mulai konversi sekarang di halaman **Kalkulator**!
    </div>
    """, unsafe_allow_html=True)
# ---------------------- HALAMAN KALKULATOR ----------------------
elif halaman == "📐 Kalkulator":
    st.header("📐 Kalkulator Konversi")
    st.markdown("Gunakan alat ini untuk melakukan konversi satuan fisika dengan mudah dan cepat.")

    kategori = st.selectbox("Pilih Kategori Satuan", list(konversi_data.keys()))
    satuan_dari = st.selectbox("Dari Satuan", list(konversi_data[kategori].keys()))
    satuan_ke = st.selectbox("Ke Satuan", list(konversi_data[kategori].keys()))
    nilai = st.number_input(f"Masukkan Nilai ({satuan_dari})", value=0.0, step=0.1)

    if st.button("🔄 Konversi"):
        with st.spinner("Menghitung konversi..."):
            time.sleep(1)
            hasil = konversi_satuan(kategori, nilai, satuan_dari, satuan_ke)
            semua_hasil = get_konversi_semua_satuan(kategori, nilai, satuan_dari)

            # Hasil utama
            st.markdown("## 🎯 Hasil Konversi")
            st.success(f"**{nilai} {satuan_dari} = {round(hasil, 6)} {satuan_ke}**")

            # Penjelasan rumus
            tampilkan_penjelasan_rumus(kategori, satuan_dari, satuan_ke)

            # Tabel hasil ke semua satuan
            if kategori != "Suhu":
                df = pd.DataFrame(list(semua_hasil.items()), columns=["Satuan", "Hasil"])
                st.markdown("### 🔍 Konversi ke Semua Satuan")
                st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

            # Grafik batang
            st.markdown("### 📊 Grafik Perbandingan Konversi")
            chart = alt.Chart(pd.DataFrame({
                'Satuan': list(semua_hasil.keys()),
                'Hasil': list(semua_hasil.values())
            })).mark_bar().encode(
                x=alt.X('Satuan', sort=None),
                y='Hasil',
                color='Satuan',
                tooltip=['Satuan', 'Hasil']
            ).properties(height=400)

            st.altair_chart(chart, use_container_width=True)

# ---------------------- HALAMAN TENTANG ----------------------
elif halaman == "ℹ️ Tentang":
    st.header("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Kalkulator Konversi Satuan Fisika** ini dikembangkan untuk membantu pelajar, guru, mahasiswa, dan profesional dalam memahami serta melakukan konversi satuan secara cepat dan tepat.

    ### 📚 Sumber Referensi:
    - [NIST: National Institute of Standards and Technology](https://www.nist.gov)
    - [Wikipedia: Units of Measurement](https://en.wikipedia.org/wiki/Units_of_measurement)
    - Buku-buku Fisika Dasar dan Kimia Dasar
    - Konversi suhu: dokumentasi standar internasional dan praktik umum laboratorium

    ### 👨‍💻 Pengembang:
    Dibuat dengan ❤️ menggunakan Python & Streamlit.

    Untuk pertanyaan atau masukan, silakan hubungi melalui [GitHub](https://github.com).
    """)
