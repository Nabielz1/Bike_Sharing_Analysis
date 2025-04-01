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

    # Filter berdasarkan tahun
    tahun_tersedia = sorted(all_data['year'].unique())
    tahun_pilihan = st.selectbox("Pilih Tahun Data", tahun_tersedia, index=len(tahun_tersedia)-1)

    # Menampilkan dataset jika dicentang
    if st.checkbox("Tampilkan Dataset"):
        st.subheader(f"Dataset Tahun {tahun_pilihan}")
        st.write(all_data[all_data['year'] == tahun_pilihan])

    # Informasi pembuat
    st.title('Made by:')
    st.write("""
        **Rifqi Nabil Akbar**\n
        Dicoding ID: **rifqiakbar12**\n
        Email: **rifqiakbar12@gmail.com**
    """)

# Filter data sesuai tahun yang dipilih
data_filtered = all_data[all_data['year'] == tahun_pilihan]

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
    st.write(f"""
    Terdapat tren peningkatan yang signifikan dalam penyewaan sepeda selama dua tahun terakhir. Bulan Januari 2011 mencatat jumlah penyewaan terendah sementara itu pada  bulan September 2012 mencapai puncak penyewaan tertinggi. 
    Meskipun demikian, setelah bulan tersebut, terjadi penurunan yang cukup signifikan, yang mungkin disebabkan oleh perubahan musim menuju musim dingin (winter), yang cenderung mengurangi minat masyarakat untuk menyewa sepeda.
    """)

# Grafik perbandingan penyewa casual dan registered
def plot_rental_by_weather(df):
    sewa_cuaca = df.groupby('weather_condition')[['registered', 'casual']].sum().reset_index()
    
    # Menghitung total penyewaan untuk mengurutkan
    sewa_cuaca['total'] = sewa_cuaca['registered'] + sewa_cuaca['casual']
    
    # Mengurutkan data dari terbesar ke terkecil berdasarkan total penyewaan
    sewa_cuaca = sewa_cuaca.sort_values(by='total', ascending=False)
    
    # Membuat bar chart
    plt.figure(figsize=(10, 6))
    
    # Menambahkan bar untuk jumlah pengguna terdaftar
    sns.barplot(
        data=sewa_cuaca,
        x='weather_condition',
        y='registered',
        label='Registered',
        color='tab:red'
    )
    
    # Menambahkan bar untuk jumlah pengguna kasual
    sns.barplot(
        data=sewa_cuaca,
        x='weather_condition',
        y='casual',
        label='Casual',
        color='tab:blue'
    )
    
    # Menambahkan judul dan label
    plt.title('Total Sepeda yang Disewakan Berdasarkan Cuaca', fontsize=20)
    plt.xlabel('Kondisi Cuaca', fontsize=16)
    plt.ylabel('Total Penyewaan', fontsize=16)
    
    # Memastikan sumbu y menampilkan rentang yang tepat
    plt.ylim(0, sewa_cuaca[['registered', 'casual']].values.max() + 100)
    
    # Menambahkan legend
    plt.legend()
    
    # Menampilkan plot
    st.pyplot(plt)

st.header(f'B. Total Penyewaan Sepeda Berdasarkan Cuaca ({tahun_pilihan})')
plot_rental_by_weather(data_filtered)

with st.expander("Kesimpulan"):
    st.write("""
    Total penyewaan sepeda bervariasi berdasarkan kondisi cuaca. 
    Penyewaan sepeda tertinggi terjadi pada kondisi cuaca cerah (Clear), sedangkan pada kondisi badai (Stormy), jumlah penyewaan menurun drastis. 
    Hal ini menunjukkan bahwa faktor cuaca sangat mempengaruhi minat penyewaan sepeda.
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
    Penyewaan sepeda mengalami peningkatan pada musim tertentu, kemungkinan besar saat musim panas (summer) karena kondisi cuaca lebih mendukung aktivitas luar ruangan.
    Sebaliknya, penyewaan cenderung menurun pada musim dingin akibat kondisi cuaca yang kurang ideal.
    """)

# Grafik total penyewaan berdasarkan jam
def plot_total_bike_rentals_by_hour(df):
    total_count_per_hour = df.groupby('hour')['total_count'].sum()

    plt.figure(figsize=(10, 6))
    max_value_index = total_count_per_hour.idxmax()
    colors = ['#B21807' if hour == max_value_index else '#4682b4' for hour in total_count_per_hour.index]

    plt.bar(total_count_per_hour.index, total_count_per_hour.values, color=colors)

    plt.title(f'Total Rental Sepeda Berdasarkan Jam ({tahun_pilihan})', fontsize=20)
    plt.xlabel('Hour')
    plt.ylabel('Total Bike Rentals')
    plt.xticks(total_count_per_hour.index)
    st.pyplot(plt)

def plot_total_bike_rentals_by_weekday(df):
    # Mengelompokkan data berdasarkan hari dalam seminggu dan menghitung total sewa
    weekday_data = df.groupby('weekday')['total_count'].sum().reset_index()

    # Membuat bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(weekday_data['weekday'], weekday_data['total_count'], color='#4682b4')

    # Mengubah warna bar maksimum menjadi merah
    max_value = weekday_data['total_count'].max()
    for bar in bars:
        if bar.get_height() == max_value:
            bar.set_color('#B21807')

    # Menambahkan label sumbu x dengan nama hari
    plt.xticks(weekday_data['weekday'], ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])

    # Menambahkan judul dan label sumbu
    plt.title(f'Total Rental Sepeda Berdasarkan Hari ({tahun_pilihan})', fontsize=20)
    plt.xlabel('Weekday', fontsize=16)
    plt.ylabel('Total Bike Rentals', fontsize=16)

    # Menampilkan plot
    st.pyplot(plt)

st.header(f'D. Pola Penyewaan Berdasarkan Hari & Jam ({tahun_pilihan})')
plot_total_bike_rentals_by_hour(data_filtered)

with st.expander("Kesimpulan"):
    st.write(f"""
    Waktu dengan penyewaan sepeda tertinggi terjadi pada jam sibuk, yaitu pagi (sekitar jam 8-9) dan sore (sekitar jam 17-18).  
    Ini mengindikasikan bahwa sepeda banyak digunakan untuk perjalanan kerja atau sekolah.
    """)

plot_total_bike_rentals_by_weekday(data_filtered)

with st.expander("Kesimpulan"):
    st.write(f"""
    Penyewaan sepeda tertinggi pada tahun 2011 terjadi pada hari Jumat dan pada tahun 2012 terjadi pada hari Kamis, sedangkan pada hari Selasa, Rabu, dan Jumat, penyewaan sepeda menurun drastis.
    Hal ini menunjukkan bahwa faktor hari dalam seminggu sangat mempengaruhi minat penyewaan sepeda.
    """)

# RFM ANALYSIS
def plot_rfm_analysis(hour_df):
    rfm_analysis = hour_df.groupby(by="hour", as_index=False).agg({
        "date": "max",        
        "instant": "nunique",  
        "total_count": "sum"   
    })

    rfm_analysis.columns = ["hour", "last_order_date", "order_count", "revenue"]

    recent_date = hour_df["date"].max().date()

    rfm_analysis["last_order_date"] = rfm_analysis["last_order_date"].dt.date
    rfm_analysis["recency"] = rfm_analysis["last_order_date"].apply(lambda x: (recent_date - x).days)

    rfm_analysis.drop("last_order_date", axis=1, inplace=True)

    top_recency_new = rfm_analysis.sort_values(by="recency", ascending=True).head(5)
    top_frequency_new = rfm_analysis.sort_values(by="order_count", ascending=False).head(5)
    top_monetary_new = rfm_analysis.sort_values(by="revenue", ascending=False).head(5)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    sns.barplot(
        data=top_recency_new, 
        x="hour", 
        y="recency",
        color='tab:red',
        ax=ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=15)

    sns.barplot(
        data=top_frequency_new,
        x="hour",
        y="order_count", 
        color='tab:red',
        ax=ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    sns.barplot(
        data=top_monetary_new, 
        x="hour", 
        y="revenue", 
        color='tab:red',
        ax=ax[2]
    )
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    plt.suptitle("Rental Terbaik Berdasarkan Parameter RFM", fontsize=20)
    st.pyplot(plt)

st.header(f'E. Analisis RFM (Recency, Frequency, Monetary) - Tahun {tahun_pilihan}')
plot_rfm_analysis(data_filtered)

with st.expander("Kesimpulan RFM Analysis"):
    st.write(f"""
    **RFM Analysis menunjukkan pola penyewaan sepeda berdasarkan tiga faktor utama:**
    
    - **Recency**: Penyewaan terbaru lebih sering terjadi pada jam-jam tertentu, menunjukkan jam favorit pengguna.
    - **Frequency**: Jam dengan frekuensi penyewaan tertinggi menunjukkan waktu sibuk untuk layanan sepeda.
    - **Monetary**: Beberapa jam tertentu menyumbang pendapatan paling besar, menunjukkan peluang bisnis untuk promosi atau diskon di jam sepi.

    **Hasilnya bisa digunakan untuk mengoptimalkan strategi pemasaran dan pengelolaan layanan sepeda.** 🚲📊
    """)