import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import pyperclip

# ---------------------- SETUP LATAR BELAKANG ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, {opacity});
            z-index: -1;
        }}
        </style>
    """, unsafe_allow_html=True)

# Gambar latar belakang
bg_image_url = "https://i.pinimg.com/originals/4e/ac/35/4eac359bce1e49679ad98f98db7428d4.png"
set_background_from_url(bg_image_url)

# ---------------------- NAVIGASI SIDEBAR ----------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "📖 Tentang"])

# ---------------------- BERANDA ----------------------
if halaman == "🏠 Beranda":
    st.title("✨ Selamat Datang di Kalkulator Konversi Satuan Fisika ✨")
    st.markdown("""
    Aplikasi ini membantu Anda mengonversi berbagai satuan fisika seperti suhu, massa, panjang, tekanan, energi, dan lainnya.  
    Gunakan menu **Kalkulator** di sidebar untuk memulai 🚀  
    """)

# ---------------------- KONVERSI UTAMA ----------------------
elif halaman == "📐 Kalkulator":
    st.title("📐 Kalkulator Konversi Satuan Fisika")

    daftar_kategori = {
        "🔥 Suhu": ["Celsius", "Fahrenheit", "Kelvin"],
        "⚖️ Massa": ["gram", "kilogram", "pon", "ons"],
        "📏 Panjang": ["meter", "kilometer", "mil", "cm", "mm"],
        "🕒 Waktu": ["detik", "menit", "jam", "hari"],
        "💨 Kecepatan": ["m/s", "km/jam", "mil/jam", "knot"],
        "🧪 Tekanan": ["Pa", "atm", "bar", "mmHg", "psi"],
        "🔋 Energi": ["Joule", "kWh", "kalori", "BTU"],
        "📦 Volume": ["liter", "mililiter", "m³", "cm³", "gallon"],
        "⚡ Daya": ["watt", "kW", "HP"],
        "📻 Frekuensi": ["Hz", "kHz", "MHz", "GHz"],
        "🔌 Arus Listrik": ["ampere", "milliampere"],
        "🔋 Tegangan": ["volt", "mV", "kV"],
        "💡 Hambatan": ["ohm", "kiloohm"]
    }

    presisi_kategori = {
        "🔥 Suhu": 2,
        "⚖️ Massa": 4,
        "📏 Panjang": 4,
        "🕒 Waktu": 3,
        "💨 Kecepatan": 2,
        "🧪 Tekanan": 3,
        "🔋 Energi": 3,
        "📦 Volume": 4,
        "⚡ Daya": 3,
        "📻 Frekuensi": 3,
        "🔌 Arus Listrik": 4,
        "🔋 Tegangan": 3,
        "💡 Hambatan": 4
    }

    kategori = st.selectbox("📂 Pilih Kategori", list(daftar_kategori.keys()))
    satuan_asal = st.selectbox("🔄 Dari", daftar_kategori[kategori])
    satuan_tujuan = st.selectbox("➡️ Ke", daftar_kategori[kategori])
    nilai_input = st.text_input("✍️ Masukkan Nilai", "")

    if st.button("🔄 Konversi"):
        if not nilai_input:
            st.warning("Masukkan nilai yang ingin dikonversi!")
        else:
            try:
    n = float(nilai_input)
    with st.spinner("Menghitung hasil konversi..."):
        time.sleep(2)

        # (lanjutkan konversi seperti biasa)
        ...
except ValueError:
    st.error("Masukkan angka yang valid!")


                    # --- Konversi suhu
                    def konversi_suhu(n, dari, ke):
                        C = F = K = None
                        if dari == "Celsius":
                            C = n
                        elif dari == "Fahrenheit":
                            C = (n - 32) * 5/9
                        elif dari == "Kelvin":
                            C = n - 273.15
                        if ke == "Celsius":
                            return C
                        elif ke == "Fahrenheit":
                            return C * 9/5 + 32
                        elif ke == "Kelvin":
                            return C + 273.15

                    # --- Satuan konversi umum
                    def konversi_umum(n, dari, ke, faktor):
                        return n * faktor[dari] / faktor[ke]

                    # Faktor konversi masing-masing kategori
                    faktor = {
                        "⚖️ Massa": {"gram": 1, "kilogram": 1000, "pon": 453.592, "ons": 100},
                        "📏 Panjang": {"meter": 1, "kilometer": 1000, "mil": 1609.34, "cm": 0.01, "mm": 0.001},
                        "🕒 Waktu": {"detik": 1, "menit": 60, "jam": 3600, "hari": 86400},
                        "💨 Kecepatan": {"m/s": 1, "km/jam": 0.277778, "mil/jam": 0.44704, "knot": 0.514444},
                        "🧪 Tekanan": {"Pa": 1, "atm": 101325, "bar": 100000, "mmHg": 133.322, "psi": 6894.76},
                        "🔋 Energi": {"Joule": 1, "kWh": 3.6e6, "kalori": 4.184, "BTU": 1055.06},
                        "📦 Volume": {"liter": 1, "mililiter": 0.001, "m³": 1000, "cm³": 0.001, "gallon": 3.78541},
                        "⚡ Daya": {"watt": 1, "kW": 1000, "HP": 745.7},
                        "📻 Frekuensi": {"Hz": 1, "kHz": 1000, "MHz": 1e6, "GHz": 1e9},
                        "🔌 Arus Listrik": {"ampere": 1, "milliampere": 0.001},
                        "🔋 Tegangan": {"volt": 1, "mV": 0.001, "kV": 1000},
                        "💡 Hambatan": {"ohm": 1, "kiloohm": 1000}
                    }

                    if kategori == "🔥 Suhu":
                        hasil = konversi_suhu(n, satuan_asal, satuan_tujuan)
                    else:
                        hasil = konversi_umum(n, satuan_asal, satuan_tujuan, faktor[kategori])

                    presisi = presisi_kategori.get(kategori, 3)
                    hasil_akhir = round(hasil, presisi)
                    st.metric("💡 Hasil Konversi", f"{hasil_akhir} {satuan_tujuan}")

                    # Tombol salin hasil
                    if st.button("📋 Salin Hasil"):
                        pyperclip.copy(f"{n} {satuan_asal} = {hasil_akhir} {satuan_tujuan}")
                        st.success("✅ Hasil berhasil disalin ke clipboard!")

                    # Penjelasan rumus
                    st.markdown("### 📘 Penjelasan Rumus")
                    penjelasan_khusus = {
                        ("Celsius", "Kelvin"): "K = C + 273.15",
                        ("Kelvin", "Celsius"): "C = K - 273.15",
                        ("Celsius", "Fahrenheit"): "F = (C × 9/5) + 32",
                        ("Fahrenheit", "Celsius"): "C = (F - 32) × 5/9",
                        ("Fahrenheit", "Kelvin"): "K = (F - 32) × 5/9 + 273.15",
                        ("Kelvin", "Fahrenheit"): "F = (K - 273.15) × 9/5 + 32"
                    }
                    rumus = penjelasan_khusus.get((satuan_asal, satuan_tujuan), "Konversi menggunakan rasio satuan.")
                    st.latex(rumus if "=" not in rumus else fr"{rumus}")

                    # Tabel konversi ke semua satuan
                    if kategori != "🔥 Suhu":
                        df = pd.DataFrame({
                            "Satuan": daftar_kategori[kategori],
                            "Hasil": [round(konversi_umum(n, satuan_asal, satuan, faktor[kategori]), presisi)
                                      for satuan in daftar_kategori[kategori]]
                        })
                        st.dataframe(df)

# ---------------------- GRAFIK ----------------------
elif halaman == "📊 Grafik":
    st.title("📊 Visualisasi Hasil Konversi")
    st.info("Silakan kembali ke halaman **Kalkulator** untuk melakukan konversi terlebih dahulu.")

# ---------------------- TENTANG ----------------------
elif halaman == "📖 Tentang":
    st.markdown("## ℹ️ Tentang Aplikasi")
    st.markdown("""
Aplikasi **Kalkulator Konversi Satuan Fisika** dibuat untuk membantu pelajar, mahasiswa, dan profesional  
melakukan konversi satuan fisika secara akurat dan cepat.

### 🎯 Fitur Utama:
- 🔁 Konversi berbagai satuan fisika: suhu, massa, panjang, tekanan, waktu, energi, daya, kecepatan, volume, arus listrik, hambatan, dan lainnya.
- 🧮 Penjelasan lengkap rumus konversi menggunakan LaTeX.
- 📊 Visualisasi hasil konversi dalam bentuk grafik interaktif.
- 🌄 Latar belakang menarik dan antarmuka ramah pengguna.

### 📚 Referensi:
- SI Units: https://www.bipm.org
- NIST (National Institute of Standards and Technology)
- Physics for Scientists and Engineers (Serway & Jewett)
- CRC Handbook of Chemistry and Physics
- Thermodynamics (Yunus A. Çengel)

Terima kasih telah menggunakan aplikasi ini. Semoga bermanfaat dalam studi maupun pekerjaan Anda!
""")
