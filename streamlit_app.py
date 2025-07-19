import streamlit as st
import pandas as pd
import altair as alt
import time

# ---------------------- SETUP LATAR BELAKANG ----------------------
def set_background_from_url(image_url, opacity=0.85):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,{opacity}), rgba(255,255,255,{opacity})), url('{image_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background_from_url("https://images.unsplash.com/photo-1608139748485-69f9f1f8ef62?auto=format&fit=crop&w=1950&q=80")

# ---------------------- DATA KONVERSI ----------------------
data_konversi = {
    "Suhu": {
        "satuan": ["Celsius", "Fahrenheit", "Kelvin"],
        "rumus": {
            ("Celsius", "Fahrenheit"): "°F = (°C × 9/5) + 32",
            ("Fahrenheit", "Celsius"): "°C = (°F − 32) × 5/9",
            ("Celsius", "Kelvin"): "K = °C + 273.15",
            ("Kelvin", "Celsius"): "°C = K − 273.15",
            ("Fahrenheit", "Kelvin"): "K = (°F − 32) × 5/9 + 273.15",
            ("Kelvin", "Fahrenheit"): "°F = (K − 273.15) × 9/5 + 32"
        }
    },
    "Tekanan": {
        "satuan": ["atm", "Pa", "bar", "mmHg", "psi"],
        "nilai_dasar": {
            "atm": 1,
            "Pa": 101325,
            "bar": 1.01325,
            "mmHg": 760,
            "psi": 14.6959
        }
    },
    "Massa": {
        "satuan": ["kg", "g", "mg", "ton", "lb"],
        "nilai_dasar": {
            "kg": 1,
            "g": 1000,
            "mg": 1_000_000,
            "ton": 0.001,
            "lb": 2.20462
        }
    },
    "Panjang": {
        "satuan": ["m", "cm", "mm", "km", "inch", "foot"],
        "nilai_dasar": {
            "m": 1,
            "cm": 100,
            "mm": 1000,
            "km": 0.001,
            "inch": 39.3701,
            "foot": 3.28084
        }
    },
    "Waktu": {
        "satuan": ["detik", "menit", "jam", "hari"],
        "nilai_dasar": {
            "detik": 1,
            "menit": 1/60,
            "jam": 1/3600,
            "hari": 1/86400
        }
    },
    "Energi": {
        "satuan": ["Joule", "kJ", "cal", "kcal", "Wh"],
        "nilai_dasar": {
            "Joule": 1,
            "kJ": 0.001,
            "cal": 0.239006,
            "kcal": 0.000239006,
            "Wh": 0.000278
        }
    },
    "Kecepatan": {
        "satuan": ["m/s", "km/h", "mph", "knot"],
        "nilai_dasar": {
            "m/s": 1,
            "km/h": 3.6,
            "mph": 2.23694,
            "knot": 1.94384
        }
    },
    "Daya": {
        "satuan": ["Watt", "kW", "HP"],
        "nilai_dasar": {
            "Watt": 1,
            "kW": 0.001,
            "HP": 0.00134102
        }
    },
    "Volume": {
        "satuan": ["L", "mL", "m³", "cm³", "galon"],
        "nilai_dasar": {
            "L": 1,
            "mL": 1000,
            "m³": 0.001,
            "cm³": 1000,
            "galon": 0.264172
        }
    },
    "Frekuensi": {
        "satuan": ["Hz", "kHz", "MHz", "GHz"],
        "nilai_dasar": {
            "Hz": 1,
            "kHz": 0.001,
            "MHz": 1e-6,
            "GHz": 1e-9
        }
    },
    "Hambatan Listrik": {
        "satuan": ["Ohm", "kOhm", "MOhm"],
        "nilai_dasar": {
            "Ohm": 1,
            "kOhm": 0.001,
            "MOhm": 1e-6
        }
    },
    "Tegangan": {
        "satuan": ["Volt", "mV", "kV"],
        "nilai_dasar": {
            "Volt": 1,
            "mV": 1000,
            "kV": 0.001
        }
    },
    "Arus Listrik": {
        "satuan": ["Ampere", "mA", "kA"],
        "nilai_dasar": {
            "Ampere": 1,
            "mA": 1000,
            "kA": 0.001
        }
    }
}

# ---------------------- HALAMAN ----------------------
def halaman_beranda():
    st.title("📐 Kalkulator Konversi Satuan Fisika")
    st.markdown("""
        Selamat datang di **Kalkulator Konversi Satuan Fisika**!  
        Aplikasi ini dirancang untuk membantu Anda mengonversi berbagai satuan fisika dengan cepat dan mudah.

        ### ✨ Fitur Unggulan:
        - Konversi antar satuan **suhu**, **massa**, **panjang**, **energi**, dll
        - Penjelasan **rumus konversi otomatis**
        - Visualisasi hasil dalam bentuk grafik 📊
        - Tampilan interaktif dan ramah pengguna 🎨

        Pilih halaman di sidebar untuk memulai konversi!
    """)

def halaman_kalkulator():
    st.header("🔄 Kalkulator Konversi")
    kategori = st.selectbox("Pilih kategori satuan", list(data_konversi.keys()))

    satuan = data_konversi[kategori]["satuan"]
    satuan_asal = st.selectbox("Dari satuan", satuan)
    satuan_tujuan = st.selectbox("Ke satuan", satuan)
    nilai = st.number_input("Masukkan nilai yang ingin dikonversi", value=0.0)

    if st.button("🔄 Konversi"):
        with st.spinner("Mengonversi..."):
            time.sleep(1)

            if kategori == "Suhu":
                hasil, rumus = konversi_suhu(nilai, satuan_asal, satuan_tujuan)
                tampilkan_hasil_konversi(nilai, satuan_asal, satuan_tujuan, hasil, rumus)
            else:
                hasil = konversi_umum(nilai, satuan_asal, satuan_tujuan, data_konversi[kategori]["nilai_dasar"])
                rumus = f"= {nilai} {satuan_asal} × ({data_konversi[kategori]['nilai_dasar'][satuan_tujuan]:.6f})"
                tampilkan_hasil_konversi(nilai, satuan_asal, satuan_tujuan, hasil, rumus)

def halaman_grafik():
    st.header("📊 Grafik Konversi Suhu")
    nilai = st.number_input("Masukkan suhu (Celsius)", value=25.0)
    data = {
        "Satuan": ["Celsius", "Fahrenheit", "Kelvin"],
        "Nilai": [nilai, nilai * 9/5 + 32, nilai + 273.15]
    }
    df = pd.DataFrame(data)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Satuan", sort=None),
        y="Nilai",
        color=alt.Color("Satuan", scale=alt.Scale(scheme="pastel1"))
    )
    st.altair_chart(chart, use_container_width=True)

def halaman_tentang():
    st.header("📘 Tentang Aplikasi")
    st.markdown("""
        Aplikasi ini dibuat untuk memudahkan konversi satuan fisika dalam kehidupan sehari-hari maupun pembelajaran.

        ### 📚 Referensi:
        - [NIST Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion)
        - [Wikipedia - Unit Conversion](https://en.wikipedia.org/wiki/Conversion_of_units)
        - [Engineering Toolbox](https://www.engineeringtoolbox.com/)

        Dibuat oleh: **OpenAI & AL FATIH**
    """)

# ---------------------- LOGIKA KONVERSI ----------------------
def konversi_umum(nilai, satuan_asal, satuan_tujuan, nilai_dasar):
    dasar = nilai / nilai_dasar[satuan_asal]
    return dasar * nilai_dasar[satuan_tujuan]

def konversi_suhu(nilai, dari, ke):
    rumus_dict = data_konversi["Suhu"]["rumus"]
    rumus = rumus_dict.get((dari, ke), "")
    if dari == ke:
        return nilai, "Tidak ada konversi"
    if dari == "Celsius" and ke == "Fahrenheit":
        return nilai * 9/5 + 32, rumus
    elif dari == "Fahrenheit" and ke == "Celsius":
        return (nilai - 32) * 5/9, rumus
    elif dari == "Celsius" and ke == "Kelvin":
        return nilai + 273.15, rumus
    elif dari == "Kelvin" and ke == "Celsius":
        return nilai - 273.15, rumus
    elif dari == "Fahrenheit" and ke == "Kelvin":
        return (nilai - 32) * 5/9 + 273.15, rumus
    elif dari == "Kelvin" and ke == "Fahrenheit":
        return (nilai - 273.15) * 9/5 + 32, rumus
    return nilai, "Konversi tidak dikenali"

def tampilkan_hasil_konversi(nilai, asal, tujuan, hasil, rumus):
    st.subheader("🎯 Hasil Konversi")
    st.markdown(f"""
    <div style='padding: 1em; border-radius: 10px; background-color: #f0f8ff; border: 1px solid #cce;'>
        <h4>🔢 {nilai} {asal} = <span style='color: #2a9d8f;'>{hasil:.4f} {tujuan}</span></h4>
        <p><b>📘 Rumus:</b><br><code>{rumus}</code></p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- NAVIGASI ----------------------
st.sidebar.title("📚 Navigasi")
halaman = st.sidebar.radio("Pilih halaman:", ["🏠 Beranda", "📐 Kalkulator", "📊 Grafik", "ℹ️ Tentang"])

if halaman == "🏠 Beranda":
    halaman_beranda()
elif halaman == "📐 Kalkulator":
    halaman_kalkulator()
elif halaman == "📊 Grafik":
    halaman_grafik()
elif halaman == "ℹ️ Tentang":
    halaman_tentang()
