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

def create_month_recap(df):
    plot_month = df['month'].astype(str)
    plot_year = df['year'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['sum_total'] = df.groupby('year_month')['total_count'].transform('sum')
    return df[['year_month', 'sum_total']]

st.title('Analisis Data Bike Sharing: Mengungkap Tren Bersepeda \U0001F6B2')
st.markdown("---")

import streamlit as st

# Sidebar components with header and centered image
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 40px;'>Dashboard</h1>", unsafe_allow_html=True)  # Bigger centered header
    
    st.image('https://github.com/Nabielz1/Bike_Sharing_Analysis/blob/main/dashboard/logo.png?raw=true')
    
    # Display Dataset Checkbox
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)  # Assumes 'all_data' is predefined with your dataset
    
    # Author Info
    st.title('Made by:')
    st.write(
        """ 
        **Rifqi Nabil Akbar**\n
        Dicoding ID: **rifqiakbar12**\n
        Email: **rifqiakbar12@gmail.com**
        """
    )




# Menggambar grafik rekap persewaan sepeda per bulan
st.header('A. Rekap Persewaan Sepeda Perbulan')
month_recap_df = create_month_recap(all_data)

sns.set_style('darkgrid')

fig, ax = plt.subplots(figsize=(18, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['sum_total'],
    marker='o', 
    linewidth=5,
    color='red'
)
plt.title("Jumlah Sepeda yang Disewa Selama Dua Tahun Terakhir", fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=55)
st.pyplot(fig)

with st.expander("Kesimpulan"):
    st.write("""
    Terdapat tren peningkatan yang signifikan dalam penyewaan sepeda selama dua tahun terakhir. 
    Bulan Januari mencatat jumlah penyewaan terendah, dengan total hanya 38.189 unit. 
    Sebaliknya, bulan September 2012 mencapai puncak penyewaan tertinggi, dengan total 218.573 unit. 
    Meskipun demikian, setelah bulan tersebut, terjadi penurunan yang cukup signifikan, 
    yang mungkin disebabkan oleh perubahan musim menuju musim dingin (winter), 
    yang cenderung mengurangi minat masyarakat untuk menyewa sepeda.
    """)


def plot_casual_vs_registered(df):
    # Hitung total pengguna casual dan registered
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()

    # Menyiapkan data untuk bar plot dan donut chart
    totals = [total_casual, total_registered]
    labels = ['Casual', 'Registered']
    sizes = [total_casual, total_registered]
    colors = ['#4682b4', '#B21807']  # Warna bar dan donut chart

    # Membuat figure dengan dua subplot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar plot untuk pengguna
    ax1 = axes[0]
    bars = ax1.bar(labels, totals, color=colors)

    # Menambahkan label total di atas bar
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), 
                 ha='center', va='bottom')  # Menambahkan teks di atas bar

    # Menambahkan label dan judul untuk bar plot
    ax1.set_ylabel('Total Users')
    ax1.set_title('Total Penyewa Casual vs Registered', fontsize=20)

    # Donut chart untuk proporsi pengguna
    ax2 = axes[1]
    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, 
                                        autopct='%1.1f%%', startangle=90, 
                                        wedgeprops=dict(width=0.3))

    # Menambahkan judul dan legend untuk donut chart
    ax2.set_title('Proporsi Penyewa Casual dan Registered', fontsize=20)
    ax2.legend(wedges, labels, loc="lower left", title="User Type", bbox_to_anchor=(1, 0.5))

    # Mengatur layout agar lebih rapi
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

def plot_casual_vs_registered_by_year(df):
    # Mengelompokkan data casual dan registered berdasarkan tahun
    casual_registered_by_year = df.groupby(['year'])[['casual', 'registered']].sum()

    # Membuat figure untuk plot bar jumlah pengguna casual vs registered per tahun
    fig, ax = plt.subplots(figsize=(14, 6))

    bar_width = 0.35
    index = np.arange(len(casual_registered_by_year))

    # Membuat bar plot untuk pengguna casual dan registered
    bar1 = ax.bar(index, casual_registered_by_year['casual'], bar_width, label='Casual', color='#4682b4')
    bar2 = ax.bar(index + bar_width, casual_registered_by_year['registered'], bar_width, label='Registered', color='#B21807')

    # Memberikan label pada sumbu X dan Y
    ax.set_xlabel('Year')
    ax.set_ylabel('User Count')
    ax.set_title('Total Penyewa Casual vs Registered (2011-2012)', fontsize=20)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(casual_registered_by_year.index)
    ax.legend()

    # Menambahkan label total di atas bar
    for bars in [bar1, bar2]:
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), 
                    ha='center', va='bottom')  # Menambahkan teks di atas bar

    # Mengatur layout agar lebih rapi
    plt.tight_layout()

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

def plot_sewa_musim(day_df):
    # Menghitung total data pelanggan registered dan kasual setiap musim
    sewa_musim = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()

    # Menghitung total penyewaan untuk mengurutkan
    sewa_musim['total'] = sewa_musim['registered'] + sewa_musim['casual']

    # Mengurutkan data dari terbesar ke terkecil berdasarkan total penyewaan
    sewa_musim = sewa_musim.sort_values(by='total', ascending=False)

    # Membuat bar chart
    plt.figure(figsize=(15  , 6))

    # Menambahkan bar untuk jumlah pengguna terdaftar
    sns.barplot(
        data=sewa_musim, 
        x='season', 
        y='registered', 
        label='Registered', 
        color='tab:red'
    )

    # Menambahkan bar untuk jumlah pengguna kasual
    sns.barplot(
        data=sewa_musim, 
        x='season', 
        y='casual', 
        label='Casual', 
        color='tab:blue'
    )

    # Menambahkan judul dan label
    plt.title('Total Sepeda yang Disewakan Berdasarkan Musim', fontsize=20)
    plt.xlabel('Musim', fontsize=16)
    plt.ylabel('Total Penyewaan', fontsize=16)

    # Menambahkan legend
    plt.legend()

    # Menampilkan plot
    st.pyplot(plt)  

def show_weather_based_rentals(df):
    # Mengelompokkan data berdasarkan kondisi cuaca
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
    plt.ylim(0, sewa_cuaca[['registered', 'casual']].values.max() + 100)  # Atur batas atas sumbu y

    # Menambahkan legend
    plt.legend()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)

def show_heatmap_rentals(df):
    # Mengelompokkan data berdasarkan kondisi cuaca dan musim
    heatmap_data = df.groupby(['weather_condition', 'season'])['total_count'].sum().unstack()

    # Membuat heatmap
    plt.figure(figsize=(18, 10))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Reds")

    # Menambahkan judul dan label
    plt.title('Total Sepeda Yang Disewa Berdasarkan Musim dan Cuaca', fontsize=20)
    plt.xlabel('Musim', fontsize=16)
    plt.ylabel('Kondisi Cuaca', fontsize=16)

    # Menampilkan plot di Streamlit
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
    plt.title('Total Rental Sepeda Berdasarkan Hari', fontsize=20)
    plt.xlabel('Weekday', fontsize=16)
    plt.ylabel('Total Bike Rentals', fontsize=16)

    # Menampilkan plot
    st.pyplot(plt)

def plot_total_bike_rentals_by_hour(df):
    # Menghitung total count berdasarkan jam
    total_count_per_hour = df.groupby('hour')['total_count'].sum()

    # Membuat bar plot
    plt.figure(figsize=(10, 6))

    # Mencari indeks jam dengan total tertinggi
    max_value_index = total_count_per_hour.idxmax()  # Mendapatkan indeks jam dengan nilai maksimum
    colors = ['#B21807' if hour == max_value_index else '#4682b4' for hour in total_count_per_hour.index]

    # Menggambar bar dengan warna yang sesuai
    plt.bar(total_count_per_hour.index, total_count_per_hour.values, color=colors)

    # Menambahkan judul dan label
    plt.title('Total Rental Sepeda Berdasarkan Jam', fontsize=20)
    plt.xlabel('Hour')
    plt.ylabel('Total Bike Rentals')
    plt.xticks(total_count_per_hour.index)

    # Menampilkan plot
    st.pyplot(plt)

def plot_rfm_analysis(hour_df):
    # Mengelompokkan data berdasarkan jam, menghitung nilai agregasi
    rfm_analysis = hour_df.groupby(by="hour", as_index=False).agg({
        "date": "max",        # Tanggal terakhir (terbaru)
        "instant": "nunique",  # Menghitung unik ID order
        "total_count": "sum"   # Jumlah total penyewaan
    })

    # Mengganti nama kolom
    rfm_analysis.columns = ["hour", "last_order_date", "order_count", "revenue"]

    # Mendapatkan nilai tanggal terbaru (recent date) dari kolom 'date'
    recent_date = hour_df["date"].max().date()

    # Perhitungan recency dalam hari
    rfm_analysis["last_order_date"] = rfm_analysis["last_order_date"].dt.date
    rfm_analysis["recency"] = rfm_analysis["last_order_date"].apply(lambda x: (recent_date - x).days)

    # Drop kolom 'last_order_date' setelah menghitung recency
    rfm_analysis.drop("last_order_date", axis=1, inplace=True)

    # Sortir data berdasarkan parameter RFM dengan variabel baru
    top_recency_new = rfm_analysis.sort_values(by="recency", ascending=True).head(5)
    top_frequency_new = rfm_analysis.sort_values(by="order_count", ascending=False).head(5)
    top_monetary_new = rfm_analysis.sort_values(by="revenue", ascending=False).head(5)

    # Membuat bar plot untuk RFM
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 12))

    # Plot top recency
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

    # Plot top frequency
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

    # Plot top monetary
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

    # Setel judul utama untuk plot
    plt.suptitle("Rental Terbaik Berdasarkan Parameter RFM", fontsize=20)
    st.pyplot(plt)





st.header('B. Demografi Penyewa Casual dan Registered')

# Sub-header untuk perbandingan total pengguna Casual dan Registered
st.subheader('1. Total Penyewa Casual vs Registered')
plot_casual_vs_registered(all_data)


# Menambahkan expander dengan kesimpulan yang lebih ringkas
with st.expander("Kesimpulan"):
    st.write("""
    
    
    Mayoritas penyewa (81,2%) adalah pengguna terdaftar, sedangkan pengguna casual hanya 18,8%. 
    Dengan strategi pemasaran yang tepat, jumlah pengguna casual bisa ditingkatkan untuk memperluas 
    basis pelanggan dan meningkatkan penyewaan.
    """)


# Sub-header untuk jumlah pengguna Casual vs Registered berdasarkan tahun
st.subheader('2. Penyewa Casual vs Registered Berdasarkan Tahun')
plot_casual_vs_registered_by_year(all_data)

# Menambahkan expander dengan kesimpulan singkat
with st.expander("Kesimpulan"):
    st.write("""    
    Grafik ini memperjelas analisis sebelumnya dengan menunjukkan dominasi penyewa terdaftar yang konsisten, sementara pengguna casual masih jauh lebih sedikit. 
    Pengguna terdaftar cenderung lebih loyal, dan strategi pemasaran untuk meningkatkan pengalaman penyewa casual 
    dapat membantu meningkatkan penyewaan secara keseluruhan.
    """)


st.header('C.Analisis Total Persewaan Sepeda Berdasarkan Musim dan Cuaca')
st.subheader('1. Profil Pelanggan Berdasarkan Musim')
plot_sewa_musim(all_data)
# Menambahkan expander
with st.expander("Kesimpulan"):
    st.write("""
    Grafik menunjukkan bahwa musim dengan penyewa terbanyak adalah autumn (musim gugur) 
    dengan lebih dari 800.000 penyewa, sementara spring (musim semi) memiliki jumlah penyewa 
    paling sedikit. Ini menunjukkan preferensi pengguna untuk menyewa sepeda lebih tinggi pada 
    musim gugur, kemungkinan karena cuaca yang lebih nyaman, sementara musim semi mungkin 
    dipengaruhi oleh faktor lain yang membatasi minat penyewa.
    """)


st.subheader('2. Profil Pelanggan Berdasarkan Cuaca')
show_weather_based_rentals(all_data)
 
with st.expander("Kesimpulan"):
        st.write("""
        Grafik ini menunjukkan bahwa kondisi cuaca memiliki pengaruh yang signifikan terhadap total penyewaan sepeda. 
        Dalam hal ini, cuaca yang cerah (clear) mencatatkan jumlah penyewaan yang jauh lebih tinggi dibandingkan dengan cuaca hujan ringan (light rain), 
        yang menunjukkan perbedaan yang mencolok. Temuan ini mengindikasikan bahwa cuaca cerah merupakan kondisi yang paling ideal untuk menyewa sepeda dan bersepeda, 
        memberikan pengalaman yang lebih menyenangkan bagi para pengguna.
        """)


st.subheader('3. Profil Pelanggan Berdasarkan Musim dan Cuaca')
show_heatmap_rentals(all_data)
with st.expander("Kesimpulan"):
    st.write("""
    Musim dan cuaca mempengaruhi penyewaan sepeda secara signifikan. 
    Musim gugur (autumn) mencatat penyewaan tertinggi sebanyak 
    801.941 dengan cuaca cerah (clear), sedangkan kombinasi 
    musim semi dan panas (spring, summer) dengan cuaca 
    hujan berat (heavy) hampir tidak ada penyewa.

    Temuan ini menunjukkan pentingnya mempertimbangkan 
    kombinasi musim dan cuaca untuk strategi pemasaran 
    dan penjadwalan layanan penyewaan sepeda.
    """)


st.header('D. Trend Persewaan Sepeda Berdasarkan Hari dan Jam')
st.subheader('1. Trend Persewaan Berdasarkan Hari')
plot_total_bike_rentals_by_weekday(all_data)

with st.expander("Kesimpulan"):
    st.write("""
    Grafik ini menunjukkan bahwa hari Jumat merupakan hari paling sering orang melakukan penyewaan sepeda dalam kurun waktu dua tahun terakhir, sementara hari Minggu mencatatkan jumlah penyewaan terendah. 
    Temuan ini mengindikasikan bahwa banyak orang cenderung memanfaatkan layanan penyewaan sepeda pada akhir pekan untuk beraktivitas, 
    seperti berolahraga atau bersantai. Sebaliknya, hari Minggu, yang biasanya lebih tenang, menunjukkan minat yang lebih rendah terhadap penyewaan sepeda. Hasil ini dapat membantu pengelola layanan penyewaan sepeda dalam merencanakan strategi promosi dan penjadwalan untuk meningkatkan jumlah penyewaan, terutama pada hari-hari dengan permintaan yang lebih rendah.
    """)


st.subheader('2. Trend Persewaan Berdasarkan Jam (Peak Hour)')
plot_total_bike_rentals_by_hour(all_data)
with st.expander("Kesimpulan"):
    st.markdown("""
    Grafik ini menunjukkan bahwa pukul 5 sore adalah waktu paling banyak orang melakukan penyewaan sepeda, sedangkan pukul 4 pagi mencatatkan jumlah penyewaan yang paling sedikit. Temuan ini menandakan bahwa pukul 5 sore merupakan jam puncak (peak hour) untuk penyewaan sepeda. 
    Dengan informasi ini, perusahaan dapat merencanakan strategi promosi yang lebih efektif, khususnya pada jam-jam sibuk tersebut, guna menarik lebih banyak pelanggan dan memaksimalkan potensi penyewaan. 
    Hal ini dapat mencakup penawaran diskon, program loyalitas, atau kampanye pemasaran yang menyasar pengguna potensial di waktu-waktu puncak tersebut, sehingga meningkatkan visibilitas dan penjualan mereka.
    """)


st.header('E. RFM Analysis')
plot_rfm_analysis(all_data)

with st.expander("Kesimpulan"):
    st.markdown("""
1. **Recency**: Menunjukkan jam di mana transaksi terakhir paling baru dilakukan.
2. **Frequency**: Mengukur seberapa sering transaksi terjadi pada jam tersebut, dengan jam yang lebih sering digunakan muncul di urutan teratas.
3. **Monetary**: Menggambarkan jumlah total transaksi yang terjadi pada jam tersebut, menampilkan jam dengan pendapatan tertinggi di posisi teratas.

RFM Analysis ini menggunakan kolom jam untuk mengidentifikasi waktu-waktu optimal dalam sehari yang dapat memberikan kontribusi maksimal terhadap jumlah penyewaan sepeda.
    """)
