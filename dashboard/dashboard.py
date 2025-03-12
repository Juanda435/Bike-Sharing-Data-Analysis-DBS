import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# **Menentukan lokasi file CSV secara dinamis**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi file dashboard.py
DATA_DIR = os.path.join(BASE_DIR, "../data")  # Mengarah ke folder data/

# **Cek apakah file tersedia**
# st.write("📂 Current Directory:", os.getcwd())  # Debugging
# st.write("📜 Files:", os.listdir(DATA_DIR))  # Debugging

# **Fungsi untuk memuat data**
@st.cache_data
def load_data():
    day_path = os.path.join(DATA_DIR, "day.csv")
    hour_path = os.path.join(DATA_DIR, "hour.csv")
    
    if not os.path.exists(day_path) or not os.path.exists(hour_path):
        st.error("🚨 File data tidak ditemukan! Pastikan file day.csv dan hour.csv ada di folder data/")
        return None, None

    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)

    # **Rename kolom agar lebih deskriptif**
    day_df.rename(columns={
        'yr': 'year', 'mnth': 'month', 'temp': 'temperature',
        'hum': 'humidity', 'windspeed': 'wind_speed', 'cnt': 'total_rentals'
    }, inplace=True)

    hour_df.rename(columns={'hr': 'hour', 'cnt': 'total_rentals'}, inplace=True)

    return day_df, hour_df

# **Memuat data**
day_df, hour_df = load_data()

if day_df is None or hour_df is None:
    st.stop()  # Hentikan aplikasi jika data tidak tersedia

# **Sidebar untuk navigasi**
st.sidebar.title("🚲 Bike Rental Data Analysis")
option = st.sidebar.selectbox("Pilih Visualisasi", ["Kapan Waktu Terbaik Menyewa?", "Faktor yang Mempengaruhi Penyewaan"])

# **1️⃣ Kapan Waktu Terbaik untuk Menyewa Sepeda?**
if option == "Kapan Waktu Terbaik Menyewa?":
    st.header("📈 Kapan Waktu Terbaik untuk Menyewa Sepeda?")
    
    st.write("""
    Berdasarkan data rata-rata penyewaan sepeda per jam, kita bisa melihat kapan waktu terbaik untuk menyewa sepeda.
    Biasanya penyewaan sepeda paling tinggi terjadi di jam-jam tertentu, misalnya saat jam berangkat kerja atau pulang kerja.
    """)
    
    # **Visualisasi rata-rata penyewaan per jam**
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        x=hour_df.groupby('hour')['total_rentals'].mean().index,
        y=hour_df.groupby('hour')['total_rentals'].mean().values,
        marker='o', ax=ax
    )
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(True)

    st.pyplot(fig)

    st.write("""
    🚴 Dari grafik di atas, waktu terbaik untuk menyewa sepeda adalah:
    - **Pagi hari (07:00 - 09:00)** → Saat orang berangkat kerja/sekolah.
    - **Sore/Malam (17:00 - 19:00)** → Saat orang pulang kerja.
    """)

# **2️⃣ Faktor yang Mempengaruhi Penyewaan**
elif option == "Faktor yang Mempengaruhi Penyewaan":
    st.header("📊 Faktor yang Mempengaruhi Penyewaan Sepeda")
    
    st.write("""
    Berikut adalah korelasi antara faktor cuaca dan jumlah penyewaan sepeda. 
    Korelasi positif berarti semakin tinggi nilainya, semakin tinggi juga jumlah penyewaan.
    Korelasi negatif berarti semakin tinggi faktor tersebut, semakin rendah jumlah penyewaan.
    """)
    
    # **Heatmap Korelasi**
    correlation = day_df[['temperature', 'humidity', 'wind_speed', 'total_rentals']].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Korelasi antara Faktor Cuaca dan Penyewaan Sepeda")
    
    st.pyplot(fig)

    st.write("""
    **📌 Kesimpulan:**
    - **Suhu (temperature)** memiliki korelasi positif tinggi → semakin hangat cuaca, semakin banyak orang menyewa sepeda.
    - **Kelembaban (humidity)** memiliki korelasi negatif sedang → kelembaban tinggi membuat orang malas menyewa sepeda.
    - **Kecepatan angin (wind_speed)** memiliki korelasi negatif lemah → angin kencang sedikit mempengaruhi penurunan penyewaan.
    """)

# **Sidebar info tambahan**
st.sidebar.info("Pilih visualisasi dari dropdown di atas untuk melihat analisis.")
