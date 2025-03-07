

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_url = "https://raw.githubusercontent.com/Zuckmo/Analisa/refs/heads/master/day_cleaned.csv"
hour_url = "https://raw.githubusercontent.com/Zuckmo/Analisa/refs/heads/master/hour_cleaned.csv"

day = pd.read_csv(day_url)
hour = pd.read_csv(hour_url)

# Sidebar Navigation
st.sidebar.header("Dashboard Navigation")
data_selection = st.sidebar.radio("Pilih Dataset:", ("Data Harian", "Data Per Jam"))

# Streamlit App
st.title("Dashboard Analisis Penyewaan Sepeda")

# Statistik Data
st.header("Statistik Data")
if data_selection == "Data Harian":
    st.write(day.describe())
else:
    st.write(hour.describe())

# Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.header("Penyewaan Sepeda Berdasarkan Musim")
season_count = day.groupby("season")["total"].sum()
fig, ax = plt.subplots()
season_count.plot(kind='bar', ax=ax, color=['blue', 'orange', 'green', 'red'])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=0)
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Visualisasi Pengaruh Cuaca
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x='weather_situation', y='total', data=day, ax=ax)
ax.set_xticklabels(['Clear', 'Mist', 'Light Snow', 'Heavy Rain'])
st.pyplot(fig)

# Perbandingan Penyewa Terdaftar dan Tidak Terdaftar
st.header("Perbandingan Penyewa Terdaftar dan Tidak Terdaftar")
fig, ax = plt.subplots()
day[['casual', 'registered']].sum().plot(kind='bar', ax=ax, color=['blue', 'orange'])
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Analisis RFM
st.header("Analisis RFM (Recency, Frequency, Monetary)")

# Menghitung Recency (seberapa baru pelanggan menyewa)
latest_date = day['dteday'].max()
day['dteday'] = pd.to_datetime(day['dteday'])
day['Recency'] = (pd.to_datetime(latest_date) - day['dteday']).dt.days
recency = day.groupby('dteday')['Recency'].min()

# Menghitung Frequency (berapa kali pelanggan menyewa)
frequency = day.groupby('dteday')['total'].count()

# Menghitung Monetary (total jumlah penyewaan)
monetary = day.groupby('dteday')['total'].sum()

# Gabungkan hasil RFM
rfm = pd.DataFrame({'Recency': recency, 'Frequency': frequency, 'Monetary': monetary})
st.write(rfm.describe())

# Visualisasi RFM
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(rfm['Recency'], bins=20, ax=ax[0], color='blue')
ax[0].set_title('Distribusi Recency')
sns.histplot(rfm['Frequency'], bins=20, ax=ax[1], color='green')
ax[1].set_title('Distribusi Frequency')
sns.histplot(rfm['Monetary'], bins=20, ax=ax[2], color='red')
ax[2].set_title('Distribusi Monetary')
st.pyplot(fig)

st.write("Dashboard ini membantu memahami pola penyewaan sepeda berdasarkan waktu, cuaca, musim, serta analisis pelanggan menggunakan metode RFM.")
	