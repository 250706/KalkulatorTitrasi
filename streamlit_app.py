import streamlit as st
import pandas as pd
import time
import altair as alt

# ---------------------- DATA KONVERSI ----------------------
konversi_data = {
    "Suhu": {
        "Celsius": lambda x, y: {
            "Celsius": x,
            "Fahrenheit": (x * 9 / 5) + 32,
            "Kelvin": x + 273.15
        }[y],
        "Fahrenheit": lambda x, y: {
            "Celsius": (x - 32) * 5 / 9,
            "Fahrenheit": x,
            "Kelvin": ((x - 32) * 5 / 9) + 273.15
        }[y],
        "Kelvin": lambda x, y: {
            "Celsius": x - 273.15,
            "Fahrenheit": ((x - 273.15) * 9 / 5) + 32,
            "Kelvin": x
        }[y]
    },
    "Tekanan": {
        "Pascal": 1,
        "atm": 101325,
        "bar": 100000,
        "psi": 6894.76
    },
    "Massa": {
        "Gram": 1,
        "Kilogram": 1000,
        "Pound": 453.592,
        "Ons": 28.3495
    },
    "Panjang": {
        "Meter": 1,
        "Kilometer": 1000,
        "Sentimeter": 0.01,
        "Milimeter": 0.001,
        "Inci": 0.0254,
        "Kaki": 0.3048
    },
    "Waktu": {
        "Detik": 1,
        "Menit": 60,
        "Jam": 3600,
        "Hari": 86400
    },
    "Energi": {
        "Joule": 1,
        "Kilojoule": 1000,
        "Kalori": 4.184,
        "Kilokalori": 4184
    },
    "Kecepatan": {
        "m/s": 1,
        "km/jam": 0.277778,
        "mil/jam": 0.44704
    },
    "Daya": {
        "Watt": 1,
        "Kilowatt": 1000,
        "Horsepower": 745.7
    },
    "Volume": {
        "Liter": 1,
        "Mililiter": 0.001,
        "Galon (US)": 3.78541,
        "Pint (US)": 0.473176
    },
    "Frekuensi": {
        "Hertz": 1,
        "Kilohertz": 1000,
        "Megahertz": 1_000_000
    },
    "Hambatan Listrik": {
        "Ohm": 1,
        "Kiloohm": 1000,
        "Megaohm": 1_000_000
    },
    "Tegangan": {
        "Volt": 1,
        "Kilovolt": 1000,
        "Milivolt": 0.001
    },
    "Arus Listrik": {
        "Ampere": 1,
        "Miliampere": 0.001
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

# ---------------------- NAVIGASI SIDEBAR ----------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

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
# ---------------------- HALAMAN GRAFIK ----------------------
elif halaman == "📊 Grafik":
    st.header("📊 Grafik Visualisasi")
    st.markdown("Halaman ini menampilkan visualisasi perbandingan hasil konversi ke semua satuan.")

    kategori = st.selectbox("Pilih Kategori untuk Grafik", list(konversi_data.keys()), key="grafik_kategori")
    satuan_dari = st.selectbox("Dari Satuan", list(konversi_data[kategori].keys()), key="grafik_dari")
    nilai = st.number_input(f"Masukkan Nilai ({satuan_dari})", value=0.0, step=0.1, key="grafik_nilai")

    if st.button("📊 Tampilkan Grafik"):
        semua_hasil = get_konversi_semua_satuan(kategori, nilai, satuan_dari)
        df = pd.DataFrame(list(semua_hasil.items()), columns=["Satuan", "Hasil"])

        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X('Satuan', sort=None),
                y='Hasil',
                color='Satuan',
                tooltip=['Satuan', 'Hasil']
            ).properties(height=400),
            use_container_width=True
        )

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
