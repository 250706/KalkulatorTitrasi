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

st.set_page_config(page_title="⏳FizConvert", layout="centered")

# === Navigasi Sidebar ===
st.sidebar.title("🔀 Navigasi")
halaman = st.sidebar.radio("Pilih halaman:", ["Beranda", "Kalkulator", "Grafik", "Tentang"])

# === DATA SATUAN ===
konversi_data = { ... }  # GUNAKAN DICTIONARY konversi_data YANG SUDAH ADA DI KODEMU

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
    ...

if halaman == "Beranda":
    st.title("🧠 KALKULATOR KONVERSI SATUAN FISIKA")
    st.markdown("Konversi berbagai satuan fisika lengkap dengan penjelasan dan grafik hasil.")
    st.image("https://static.vecteezy.com/system/resources/previews/008/302/933/original/physics-science-and-education-concept-illustration-vector.jpg", use_column_width=True)
    st.markdown("Selamat datang di **FizConvert** – alat bantu cerdas untuk mengubah satuan fisika dengan cepat dan akurat!")

elif halaman == "Kalkulator":
    st.header("🧮 Kalkulator Konversi")
    kategori = st.selectbox("Pilih kategori satuan:", list(konversi_data.keys()))
    satuan_list = list(konversi_data[kategori].keys())
    satuan_asal = st.selectbox("Satuan asal:", satuan_list)
    satuan_tujuan = st.selectbox("Satuan tujuan:", satuan_list)
    nilai_input = st.text_input("Masukkan nilai:", placeholder="contoh: 5.5")

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
                    else:
                        faktor_asal = konversi_data[kategori][satuan_asal]
                        faktor_tujuan = konversi_data[kategori][satuan_tujuan]
                        hasil = nilai * faktor_asal / faktor_tujuan

                    hasil_str = format_presisi(hasil)
                    st.metric(label="Hasil Konversi", value=f"{hasil_str} {satuan_tujuan}")
                    st.success(f"✅ {nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.code(f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}")
                    st.text_input("📋 Salin hasil konversi:", value=f"{nilai} {satuan_asal} = {hasil_str} {satuan_tujuan}", key="copy", disabled=False)

                    if kategori == "🔥 Suhu":
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
                        st.markdown("### 📘 Penjelasan Konversi")
                        st.latex(r"\text{Hasil} = \text{nilai} \times \frac{\text{faktor asal}}{\text{faktor tujuan}}")
                        st.latex(fr"{nilai} \times \frac{{{faktor_asal}}}{{{faktor_tujuan}}} = {hasil_str}")

                        semua_konversi = {
                            satuan: format_presisi(nilai * faktor_asal / faktor)
                            for satuan, faktor in konversi_data[kategori].items()
                        }
                        df_all = pd.DataFrame(list(semua_konversi.items()), columns=["Satuan", "Hasil"])
                        st.dataframe(df_all, use_container_width=True)

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

elif halaman == "Grafik":
    st.header("📈 Visualisasi Data Konversi")
    st.info("Masuk ke halaman *Kalkulator* dan lakukan konversi untuk melihat grafik di sini.")
    st.markdown("Grafik batang perbandingan satuan akan ditampilkan setelah konversi berhasil dilakukan.")

elif halaman == "Tentang":
    st.header("ℹ Tentang Aplikasi")
    st.markdown("""
    **FizConvert** adalah alat bantu edukatif berbasis web yang dikembangkan menggunakan Python dan Streamlit.  
    Tujuannya adalah membantu pelajar, mahasiswa, dan profesional dalam mengonversi satuan fisika secara cepat dan tepat.

    👨‍💻 Developer: **AL FATIH**  
    📚 Teknologi: Python, Streamlit, Pandas, Altair  
    💡 Saran & masukan sangat dihargai!
    """)
