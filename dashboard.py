import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul aplikasi
st.title("Analisis Penyewaan Sepeda")

# Membaca data
all_data = pd.read_csv("main_data.csv")

# Konversi kolom dteday ke datetime
all_data['dteday'] = pd.to_datetime(all_data['dteday'])

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
selected_insight = None

# Tombol untuk memilih insight
if st.sidebar.button("Pola Penggunaan Sepeda Berdasarkan Jam"):
    selected_insight = "Pola Penggunaan Sepeda Berdasarkan Jam"
if st.sidebar.button("Pengaruh Suhu terhadap Penyewaan Sepeda"):
    selected_insight = "Pengaruh Suhu terhadap Penyewaan Sepeda"
if st.sidebar.button("Pengaruh Kondisi Cuaca Ekstrim terhadap Penyewaan Sepeda"):
    selected_insight = "Pengaruh Kondisi Cuaca Ekstrim terhadap Penyewaan Sepeda"
if st.sidebar.button("Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari dalam Seminggu"):
    selected_insight = "Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari dalam Seminggu"

# Kartu Informasi
average_rentals = all_data['cnt'].mean()
st.metric(label="Rata-rata Penyewaan Sepeda", value=f"{average_rentals:.2f}")

# 1. Pola Penggunaan Sepeda Berdasarkan Jam
if selected_insight == "Pola Penggunaan Sepeda Berdasarkan Jam":
    st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")

    average_rentals_by_hour = all_data.groupby('hr')['cnt'].mean().reset_index()
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=average_rentals_by_hour, marker='o', color='blue')
    plt.title('Pola Penyewaan Sepeda berdasarkan Jam dalam Sehari')
    plt.xlabel('Jam (24-jam)')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    plt.xticks(range(0, 24))
    plt.grid()
    st.pyplot(fig)

# 2. Pengaruh Suhu terhadap Penyewaan Sepeda
elif selected_insight == "Pengaruh Suhu terhadap Penyewaan Sepeda":
    st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")

    correlation_temp = all_data['temp'].corr(all_data['cnt'])
    st.write(f"Korelasi antara suhu dan jumlah penyewaan: {correlation_temp:.2f}")

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Visualisasi Histogram Suhu
    sns.histplot(all_data['temp'], bins=20, kde=True, ax=axs[0], color='skyblue')
    axs[0].set_title('Distribusi Suhu')
    axs[0].set_xlabel('Suhu (°C)')
    axs[0].set_ylabel('Frekuensi')

    # Korelasi antara Suhu dan Penyewaan
    sns.scatterplot(x='temp', y='cnt', data=all_data, ax=axs[1], color='orange')
    sns.regplot(x='temp', y='cnt', data=all_data, ax=axs[1], scatter=False, color='red')
    axs[1].set_title('Korelasi antara Suhu dan Jumlah Penyewaan')
    axs[1].set_xlabel('Suhu (°C)')
    axs[1].set_ylabel('Jumlah Penyewaan')

    plt.tight_layout()
    st.pyplot(fig)

# 3. Pengaruh Kondisi Cuaca Ekstrim terhadap Penyewaan Sepeda
elif selected_insight == "Pengaruh Kondisi Cuaca Ekstrim terhadap Penyewaan Sepeda":
    st.subheader("Pengaruh Kondisi Cuaca Ekstrim terhadap Penyewaan Sepeda")

    weather_effect = all_data.groupby('weathersit')['cnt'].mean().reset_index()
    weather_effect['weathersit'] = weather_effect['weathersit'].map({
        1: 'Cerah',
        2: 'Mendung',
        3: 'Hujan Ringan',
        4: 'Hujan Berat'
    })

    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x='weathersit', y='cnt', data=weather_effect)
    plt.title('Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 4. Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari dalam Seminggu
elif selected_insight == "Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari dalam Seminggu":
    st.subheader("Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari dalam Seminggu")

    # Menghitung rata-rata penyewaan berdasarkan hari kerja
    avg_rentals_workingday = all_data.groupby('workingday')['cnt'].mean().reset_index()
    avg_rentals_workingday.columns = ['Working Day', 'Average Rentals']

    # Menghitung rata-rata penyewaan berdasarkan hari dalam seminggu
    avg_rentals_weekday = all_data.groupby('weekday')['cnt'].mean().reset_index()
    avg_rentals_weekday.columns = ['Weekday', 'Average Rentals']

    # Membuat figure dengan 1 baris dan 2 kolom
    fig = plt.figure(figsize=(15, 6))

    # Visualisasi rata-rata penyewaan berdasarkan hari kerja
    plt.subplot(1, 2, 1)  # 1 baris, 2 kolom, subplot pertama
    sns.barplot(data=avg_rentals_workingday, x='Working Day', y='Average Rentals')
    plt.title('Rata-rata Penyewaan Sepeda pada Hari Kerja vs Hari Non-Kerja')
    plt.xticks(ticks=[0, 1], labels=['Hari Non-Kerja', 'Hari Kerja'])
    plt.ylabel('Rata-rata Penyewaan')

    # Visualisasi rata-rata penyewaan berdasarkan hari dalam seminggu
    plt.subplot(1, 2, 2)  # 1 baris, 2 kolom, subplot kedua
    sns.barplot(data=avg_rentals_weekday, x='Weekday', y='Average Rentals')
    plt.title('Rata-rata Penyewaan Sepeda berdasarkan Hari dalam Seminggu')
    plt.xticks(ticks=np.arange(7), labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    plt.ylabel('Rata-rata Penyewaan')

    # Menampilkan visualisasi
    plt.tight_layout()
    st.pyplot(fig)

# Menampilkan dataframe yang telah difilter
st.dataframe(all_data)
