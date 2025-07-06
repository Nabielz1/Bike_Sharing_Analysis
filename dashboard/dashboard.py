import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengimpor data
all_data = pd.read_csv('https://raw.githubusercontent.com/Nabielz1/Bike_Sharing_Analysis/refs/heads/main/dashboard/hour_main.csv')

# Mengonversi kolom tanggal menjadi datetime dan menyortir data
datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

# Menampilkan judul dashboard
st.title('Analisis Data Bike Sharing: Mengungkap Tren Bersepeda 🚴‍♂️')
st.markdown("---")

# Sidebar untuk filter
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 40px;'>Dashboard</h1>", unsafe_allow_html=True) 
    st.image('https://github.com/Nabielz1/Bike_Sharing_Analysis/blob/main/dashboard/logo.png?raw=true')

    # Ambil semua tahun unik dan ubah jadi list
    tahun_tersedia = sorted(all_data['year'].dropna().unique().tolist())

    # Ubah ke string agar bisa digabung dengan "All"
    tahun_tersedia = [str(tahun) for tahun in tahun_tersedia]

    # Tambahkan opsi 'All' di akhir list
    tahun_tersedia.append("All")

    # Selectbox untuk memilih tahun (default ke 'All')
    tahun_pilihan = st.selectbox("Pilih Tahun Data", tahun_tersedia, index=len(tahun_tersedia)-1)

    # Tampilkan dataset jika dicentang
    if st.checkbox("Tampilkan Dataset"):
        if tahun_pilihan == "All":
            st.subheader("Seluruh Dataset")
            st.write(all_data)
        else:
            # Filter data sesuai tahun yang dipilih
            tahun_int = int(tahun_pilihan)
            filtered_data = all_data[all_data['year'] == tahun_int]
            filtered_data = filtered_data.reset_index(drop=True)
            st.subheader(f"Dataset Tahun {tahun_pilihan}")
            st.write(filtered_data)

    # Informasi pembuat
    st.title('Made by:')
    st.write("""
        **Rifqi Nabil Akbar**\n
        Dicoding ID: **rifqiakbar12**\n
        Email: **rifqiakbar12@gmail.com**
    """)

# Filter data sesuai tahun yang dipilih
if tahun_pilihan == "All":
    data_filtered = all_data
else:
    data_filtered = all_data[all_data['year'] == int(tahun_pilihan)]

# Cek apakah data kosong (untuk mencegah error)
if data_filtered.empty:
    st.warning(f"Tidak ada data untuk pilihan tahun: {tahun_pilihan}")
    st.stop()  # Menghentikan eksekusi Streamlit jika data kosong


# Fungsi untuk rekap bulanan
def create_month_recap(df):
    df = df.copy()
    df.loc[:, 'year_month'] = df['month'].astype(str) + ' ' + df['year'].astype(str)
    df.loc[:, 'sum_total'] = df.groupby('year_month')['total_count'].transform('sum')
    return df[['year_month', 'sum_total']].drop_duplicates()

# Grafik rekap penyewaan per bulan
st.header(f'A. Rekap Persewaan Sepeda Perbulan pada Tahun {tahun_pilihan}')
month_recap_df = create_month_recap(data_filtered)

fig, ax = plt.subplots(figsize=(18, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['sum_total'],
    marker='o', 
    linewidth=5,
    color='red'
)
plt.title(f"Jumlah Sepeda yang Disewa Tahun {tahun_pilihan}", fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=55)
st.pyplot(fig)

with st.expander("Kesimpulan"):
    if tahun_pilihan == "2011":
        st.write("""
        Pada tahun **2011**, tren penyewaan sepeda menunjukkan pertumbuhan dari awal tahun hingga mencapai puncaknya di pertengahan tahun, yaitu sekitar bulan Juni. Setelah itu, jumlah penyewaan cenderung menurun seiring mendekati akhir tahun, yang kemungkinan disebabkan oleh perubahan musim menuju musim dingin. Bulan Januari tercatat sebagai bulan dengan penyewaan terendah.
        """)
    elif tahun_pilihan == "2012":
        st.write("""
        Tahun **2012** menunjukkan peningkatan volume penyewaan yang signifikan dibandingkan tahun sebelumnya. Puncak penyewaan tertinggi terjadi pada bulan September. Setelah mencapai puncaknya, terjadi penurunan yang cukup tajam, yang kemungkinan besar dipengaruhi oleh datangnya musim dingin.
        """)
    else:  # Untuk "All"
        st.write("""
        Terdapat tren peningkatan yang signifikan dalam penyewaan sepeda selama dua tahun terakhir. Bulan Januari 2011 mencatat jumlah penyewaan terendah, sementara bulan September 2012 mencapai puncak penyewaan tertinggi secara keseluruhan. 
        Setelah puncak di tahun 2012, terjadi penurunan yang signifikan, yang mungkin disebabkan oleh perubahan musim menuju musim dingin (winter), yang cenderung mengurangi minat masyarakat untuk menyewa sepeda.
        """)

# Grafik perbandingan penyewa casual dan registered
def plot_rental_by_weather(df):
    sewa_cuaca = df.groupby('weather_condition')[['registered', 'casual']].sum().reset_index()
    sewa_cuaca['total'] = sewa_cuaca['registered'] + sewa_cuaca['casual']
    sewa_cuaca = sewa_cuaca.sort_values(by='total', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=sewa_cuaca, x='weather_condition', y='registered', label='Registered', color='tab:red')
    sns.barplot(data=sewa_cuaca, x='weather_condition', y='casual', label='Casual', color='tab:blue')
    
    plt.title('Total Sepeda yang Disewakan Berdasarkan Cuaca', fontsize=20)
    plt.xlabel('Kondisi Cuaca', fontsize=16)
    plt.ylabel('Total Penyewaan', fontsize=16)
    plt.ylim(0, sewa_cuaca[['registered', 'casual']].values.max() * 1.1)
    plt.legend()
    st.pyplot(plt)

st.header(f'B. Total Penyewaan Sepeda Berdasarkan Cuaca ({tahun_pilihan})')
plot_rental_by_weather(data_filtered)

with st.expander("Kesimpulan"):
    st.write(f"""
    Untuk tahun **{tahun_pilihan}**, pola penyewaan sepeda sangat dipengaruhi oleh kondisi cuaca.
    - **Cerah (Clear)**: Kondisi cuaca ini secara konsisten mencatat jumlah penyewaan sepeda tertinggi, baik oleh pengguna terdaftar (registered) maupun kasual (casual).
    - **Berawan/Berkabut (Misty)**: Terdapat penurunan jumlah penyewaan dibandingkan cuaca cerah.
    - **Hujan Ringan (Light Rain)**: Jumlah penyewaan menurun lebih jauh.
    - **Badai/Hujan Lebat (Heavy Rain)**: Kondisi cuaca buruk ini memiliki jumlah penyewaan paling rendah, bahkan hampir tidak ada.
    
    Hal ini menunjukkan bahwa cuaca yang baik adalah faktor pendorong utama bagi masyarakat untuk bersepeda.
    """)

# Grafik total penyewaan berdasarkan musim
def plot_sewa_musim(df):
    sewa_musim = df.groupby('season')[['registered', 'casual']].sum().reset_index()
    plt.figure(figsize=(15, 6))
    sns.barplot(data=sewa_musim, x='season', y='registered', label='Registered', color='tab:red')
    sns.barplot(data=sewa_musim, x='season', y='casual', label='Casual', color='tab:blue')
    plt.title(f'Total Sepeda yang Disewakan Berdasarkan Musim ({tahun_pilihan})', fontsize=20)
    plt.xlabel('Musim', fontsize=16)
    plt.ylabel('Total Penyewaan', fontsize=16)
    plt.legend()
    st.pyplot(plt)

st.header(f'C. Penyewaan Berdasarkan Musim ({tahun_pilihan})')
plot_sewa_musim(data_filtered)

with st.expander("Kesimpulan"):
    st.write(f"""
    Berdasarkan data tahun **{tahun_pilihan}**, musim memiliki dampak yang jelas terhadap jumlah penyewaan sepeda dengan urutan sebagai berikut:
    - **Musim Gugur (Autumn)**: Merupakan musim dengan jumlah penyewaan **tertinggi**. Cuaca yang sejuk dan nyaman menjadi daya tarik utama.
    - **Musim Panas (Summer)**: Menempati urutan kedua dengan jumlah penyewaan yang tinggi, didukung oleh cuaca cerah dan hari yang lebih panjang.
    - **Musim Dingin (Winter)**: Jumlah penyewaan pada musim ini lebih rendah dari musim panas dan gugur, namun secara konsisten **lebih tinggi dari musim semi**.
    - **Musim Semi (Spring)**: Secara konsisten menjadi musim dengan jumlah penyewaan **terendah**. Hal ini kemungkinan terjadi karena kondisi awal musim semi yang seringkali masih dingin dan cuacanya tidak menentu.
    """)

# Grafik total penyewaan berdasarkan jam dan hari
def plot_total_bike_rentals_by_hour(df):
    total_count_per_hour = df.groupby('hour')['total_count'].sum()
    plt.figure(figsize=(10, 6))
    max_value_index = total_count_per_hour.idxmax()
    colors = ['#B21807' if hour == max_value_index else '#4682b4' for hour in total_count_per_hour.index]
    plt.bar(total_count_per_hour.index, total_count_per_hour.values, color=colors)
    plt.title(f'Total Rental Sepeda Berdasarkan Jam ({tahun_pilihan})', fontsize=20)
    plt.xlabel('Jam (Hour)')
    plt.ylabel('Total Penyewaan Sepeda')
    plt.xticks(total_count_per_hour.index)
    st.pyplot(plt)

def plot_total_bike_rentals_by_weekday(df):
    weekday_data = df.groupby('weekday')['total_count'].sum()
    weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday_data = weekday_data.reindex([0, 1, 2, 3, 4, 5, 6]) # Pastikan urutan sesuai
    
    plt.figure(figsize=(10, 6))
    max_value_index = weekday_data.idxmax()
    colors = ['#B21807' if i == max_value_index else '#4682b4' for i in range(len(weekday_data))]
    
    plt.bar(weekday_order, weekday_data.values, color=colors)
    plt.title(f'Total Rental Sepeda Berdasarkan Hari ({tahun_pilihan})', fontsize=20)
    plt.xlabel('Hari dalam Seminggu', fontsize=16)
    plt.ylabel('Total Penyewaan Sepeda', fontsize=16)
    plt.xticks(rotation=45)
    st.pyplot(plt)

st.header(f'D. Pola Penyewaan Berdasarkan Hari & Jam ({tahun_pilihan})')
plot_total_bike_rentals_by_hour(data_filtered)

with st.expander("Kesimpulan"):
    st.write(f"""
    Pada tahun **{tahun_pilihan}**, pola penyewaan per jam menunjukkan dua puncak utama yang sangat jelas:
    - **Pagi Hari**: Sekitar pukul **8 PAGI**, bertepatan dengan jam berangkat kerja atau sekolah.
    - **Sore Hari**: Sekitar pukul **5-6 SORE** (17:00-18:00), yang merupakan jam pulang kerja.
    
    Pola ini sangat mengindikasikan bahwa sepeda banyak digunakan sebagai moda transportasi komuter. Penyewaan terendah terjadi pada dini hari, sekitar jam 3-4 pagi.
    """)

plot_total_bike_rentals_by_weekday(data_filtered)

with st.expander("Kesimpulan"):
    if tahun_pilihan == "2011":
        st.write("""
        Pada tahun **2011**, penyewaan sepeda cenderung lebih tinggi pada akhir pekan kerja, dengan puncak terjadi pada hari **Jumat**. Hari kerja (Senin-Jumat) menunjukkan aktivitas yang relatif stabil dan tinggi, sementara akhir pekan (Sabtu-Minggu) sedikit lebih rendah, menguatkan dugaan penggunaan untuk komuter.
        """)
    elif tahun_pilihan == "2012":
        st.write("""
        Di tahun **2012**, volume penyewaan meningkat di semua hari. Puncak penyewaan tertinggi terjadi pada hari **Kamis**. Pola penggunaan selama hari kerja tetap tinggi, menunjukkan pertumbuhan berkelanjutan dalam penggunaan sepeda sebagai sarana komuter.
        """)
    else:  # Untuk "All"
        st.write("""
        Secara keseluruhan, hari kerja (Senin-Jumat) menunjukkan tingkat penyewaan yang tinggi dan konsisten, menandakan kuatnya penggunaan sepeda untuk kebutuhan komuter. Puncak penyewaan sedikit bervariasi, terjadi pada hari **Jumat di 2011** dan **Kamis di 2012**. Akhir pekan (terutama hari Minggu) secara konsisten memiliki jumlah penyewaan yang lebih rendah dibandingkan hari kerja.
        """)

# RFM ANALYSIS
def plot_rfm_analysis(hour_df):
    # Cek jika dataframe kosong untuk menghindari error
    if hour_df.empty:
        st.warning("Data RFM tidak dapat dibuat karena tidak ada data yang dipilih.")
        return

    rfm_analysis = hour_df.groupby(by="hour", as_index=False).agg({
        "date": "max",
        "instant": "nunique",
        "total_count": "sum"
    })
    rfm_analysis.columns = ["hour", "last_order_date", "frequency", "monetary"]

    recent_date = hour_df["date"].max().date()
    rfm_analysis["last_order_date"] = rfm_analysis["last_order_date"].dt.date
    rfm_analysis["recency"] = rfm_analysis["last_order_date"].apply(lambda x: (recent_date - x).days)
    rfm_analysis.drop("last_order_date", axis=1, inplace=True)

    top_recency = rfm_analysis.sort_values(by="recency", ascending=True).head(5)
    top_frequency = rfm_analysis.sort_values(by="frequency", ascending=False).head(5)
    top_monetary = rfm_analysis.sort_values(by="monetary", ascending=False).head(5)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    sns.barplot(data=top_recency, x="hour", y="recency", color='tab:red', ax=ax[0])
    ax[0].set_ylabel(None); ax[0].set_xlabel("Jam (Hour)", fontsize=15); ax[0].set_title("Recency (days)", loc="center", fontsize=18); ax[0].tick_params(axis='x', labelsize=15)

    sns.barplot(data=top_frequency, x="hour", y="frequency", color='tab:red', ax=ax[1])
    ax[1].set_ylabel(None); ax[1].set_xlabel("Jam (Hour)", fontsize=15); ax[1].set_title("Frequency", loc="center", fontsize=18); ax[1].tick_params(axis='x', labelsize=15)

    sns.barplot(data=top_monetary, x="hour", y="monetary", color='tab:red', ax=ax[2])
    ax[2].set_ylabel(None); ax[2].set_xlabel("Jam (Hour)", fontsize=15); ax[2].set_title("Monetary", loc="center", fontsize=18); ax[2].tick_params(axis='x', labelsize=15)

    plt.suptitle(f"Pelanggan Terbaik Berdasarkan RFM per Jam ({tahun_pilihan})", fontsize=20)
    st.pyplot(plt)

st.header(f'E. Analisis RFM (Recency, Frequency, Monetary) - Tahun {tahun_pilihan}')
plot_rfm_analysis(data_filtered)

with st.expander("Kesimpulan RFM Analysis"):
    st.write(f"""
    Analisis RFM per jam untuk tahun **{tahun_pilihan}** memberikan wawasan tentang "pelanggan" terbaik, di mana setiap jam dianggap sebagai satu "pelanggan".
    
    - **Recency (Kebaruan)**: Menunjukkan jam-jam mana yang paling baru melakukan "transaksi" (penyewaan). Nilai recency yang rendah (mendekati 0 hari) berarti penyewaan terjadi hingga hari terakhir dari data yang ada, menandakan jam tersebut konsisten digunakan.
    - **Frequency (Frekuensi)**: Mengidentifikasi jam-jam dengan frekuensi penyewaan tertinggi. Jam-jam sibuk seperti **8 pagi** dan **5-6 sore** secara konsisten muncul di sini.
    - **Monetary (Moneter)**: Menunjukkan jam-jam yang menyumbang total penyewaan (pendapatan) terbesar. Sama seperti frekuensi, jam-jam sibuk komuter mendominasi metrik ini.

    Hasil analisis RFM ini menegaskan bahwa jam-jam sibuk pagi dan sore adalah segmen waktu paling berharga yang harus menjadi fokus utama untuk strategi operasional dan pemasaran. 🚲📊
    """)