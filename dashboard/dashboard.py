import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = "all_data.csv"
data = pd.read_csv(file_path)

# Clean data: drop duplicate columns
data = data.loc[:, ~data.columns.str.endswith("_y")]

# Convert date column to datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar filters
st.sidebar.header("Filter Data")
selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    options=data['mnth_x'].unique(),
    default=data['mnth_x'].unique()
)
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=data['season_x'].unique(),
    default=data['season_x'].unique()
)

# Filter data
filtered_data = data[
    (data['mnth_x'].isin(selected_month)) &
    (data['season_x'].isin(selected_season))
]

# Dashboard title
st.title("Dashboard Visualisasi Data Pengendara Sepeda")

# Section: Summary stats
st.header("Statistik Ringkas")
st.write("""
Statistik ini memberikan gambaran umum tentang suhu, kelembapan, dan jumlah pengendara sepeda.
Melalui data ini, kita dapat melihat rata-rata, nilai minimum, maksimum, dan distribusi data tersebut.
""")
st.write(filtered_data[['temp_x', 'hum_x', 'cnt_x']].describe())

# Section: Line plot
st.header("Jumlah Pengendara Sepeda Per Hari")
st.write("""
Visualisasi ini menunjukkan tren jumlah pengendara sepeda berdasarkan tanggal.
Dari grafik ini, kita dapat mengidentifikasi pola harian atau musim yang memengaruhi jumlah pengendara.
""")
daily_data = filtered_data.groupby('dteday')['cnt_x'].sum().reset_index()
plt.figure(figsize=(10, 5))
plt.plot(daily_data['dteday'], daily_data['cnt_x'], marker='o')
plt.title("Jumlah Pengendara Sepeda Per Hari")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Pengendara")
plt.grid(True)
st.pyplot(plt)

# Section: Histogram
st.header("Distribusi Suhu")
st.write("""
Histogram ini menunjukkan distribusi suhu selama periode waktu yang ada dalam data.
Kita dapat melihat rentang suhu yang sering terjadi dan bagaimana pola distribusi suhunya.
""")
plt.figure(figsize=(7, 4))
plt.hist(filtered_data['temp_x'], bins=20, color='skyblue', edgecolor='black')
plt.title("Distribusi Suhu")
plt.xlabel("Suhu")
plt.ylabel("Frekuensi")
st.pyplot(plt)

# Section: Scatter plot
st.header("Hubungan Suhu dan Jumlah Pengendara")
st.write("""
Scatter plot ini memperlihatkan hubungan antara suhu dan jumlah pengendara sepeda.
Dengan visualisasi ini, kita dapat mengamati apakah suhu memiliki pengaruh terhadap jumlah pengendara.
""")
plt.figure(figsize=(7, 4))
plt.scatter(filtered_data['temp_x'], filtered_data['cnt_x'], alpha=0.6)
plt.title("Hubungan Suhu dan Jumlah Pengendara")
plt.xlabel("Suhu")
plt.ylabel("Jumlah Pengendara")
st.pyplot(plt)
