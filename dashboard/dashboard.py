import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# **Load Dataset**
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Rename kolom agar lebih mudah dipahami
    day_df.rename(columns={
        'yr': 'year', 'mnth': 'month', 'temp': 'temperature',
        'hum': 'humidity', 'windspeed': 'wind_speed', 'cnt': 'total_rentals'
    }, inplace=True)
    
    hour_df.rename(columns={'hr': 'hour', 'cnt': 'total_rentals'}, inplace=True)
    
    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# Sidebar untuk navigasi
st.sidebar.title("🚲 Bike Rental Data Analysis")
option = st.sidebar.selectbox("Pilih Visualisasi", ["Kapan Waktu Terbaik Menyewa?", "Faktor yang Mempengaruhi Penyewaan"])

# **1. Kapan waktu terbaik untuk menyewa sepeda?**
if option == "Kapan Waktu Terbaik Menyewa?":
    st.header("📈 Kapan Waktu Terbaik untuk Menyewa Sepeda?")
    
    st.write("""
    Berdasarkan data rata-rata penyewaan sepeda per jam, kita bisa melihat kapan waktu terbaik untuk menyewa sepeda.
    Umumnya, penyewaan sepeda paling tinggi terjadi pada jam-jam tertentu, misalnya saat jam berangkat kerja (pagi) atau setelah jam kerja (sore/malam).
    """)
    
    # Membuat visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=hour_df.groupby('hour')['total_rentals'].mean().index,
                 y=hour_df.groupby('hour')['total_rentals'].mean().values,
                 marker='o', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(True)
    
    st.pyplot(fig)

    st.write("""
    Dari grafik di atas, kita bisa menyimpulkan bahwa waktu terbaik untuk menyewa sepeda adalah saat jam **pagi hari (sekitar jam 7-9)** 
    dan **sore/malam (sekitar jam 17-19)**, karena pada waktu tersebut permintaan penyewaan sepeda meningkat tajam.
    """)

# **2. Faktor apa yang paling mempengaruhi jumlah penyewaan sepeda?**
elif option == "Faktor yang Mempengaruhi Penyewaan":
    st.header("📊 Faktor yang Mempengaruhi Penyewaan Sepeda")
    
    st.write("""
    Berikut adalah korelasi antara faktor cuaca dan jumlah penyewaan sepeda. 
    Korelasi positif berarti semakin tinggi nilainya, semakin tinggi juga jumlah penyewaan.
    Korelasi negatif berarti semakin tinggi faktor tersebut, semakin rendah jumlah penyewaan.
    """)
    
    correlation = day_df[['temperature', 'humidity', 'wind_speed', 'total_rentals']].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Korelasi antara Faktor Cuaca dan Penyewaan Sepeda")
    
    st.pyplot(fig)

    st.write("""
    **Kesimpulan:**
    - Suhu (**temperature**) memiliki korelasi positif tinggi dengan jumlah penyewaan, artinya semakin hangat cuaca, semakin banyak orang menyewa sepeda.
    - Kelembaban (**humidity**) memiliki korelasi negatif sedang, yang berarti saat kelembaban tinggi, penyewaan cenderung menurun.
    - Kecepatan angin (**wind_speed**) memiliki korelasi negatif lemah, artinya angin kencang sedikit mempengaruhi penurunan penyewaan, tetapi tidak signifikan.
    """)

# Informasi tambahan di sidebar
st.sidebar.info("Pilih visualisasi dari dropdown di atas untuk melihat analisis.")
