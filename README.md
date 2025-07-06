
# Dicoding Belajar Analisis Data dengan Python 
# Kaggle : Bike Sharing Dataset

Proyek ini bertujuan untuk menganalisis dataset dari Kaggle dengan judul **Bike Sharing**, di mana dataset ini membahas tentang pola penyewaan sepeda berdasarkan berbagai faktor, seperti cuaca, musim, waktu dalam sehari, serta data penggunaan oleh penyewa. Analisis ini akan membantu untuk memahami tren penyewaan sepeda, seperti waktu penyewaan terbanyak, cuaca yang mendukung aktivitas penyewaan, dan musim dengan permintaan tertinggi.

Hasil dari analisis ini diharapkan dapat memberikan wawasan yang berguna bagi perusahaan penyewaan sepeda untuk mengoptimalkan strategi bisnis, merencanakan promosi, dan mengelola layanan sesuai dengan prediksi permintaan penyewaan berdasarkan faktor-faktor yang telah dianalisis.


## Struktur File
```
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt
```

## Project Dataset
[Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

## Setup Environtment
- Install Visual Studio Code or any other source code editor
- Execute this command on your Command Prompt
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas matplotlib seaborn jupyter streamlit
```
## Run Streamlit Dashboard app
1. Clone this repository
   ```
   git clone https://github.com/Nabielz1/Bike_Sharing_Analysis.git
   ```

2. Move to dashboard directory
   ```
   cd Submission\dashboard
   ```
3. Run streamlit app
   ```
   streamlit run dashboard.py
   ```
## Streamlit Cloud :
Streamlit Cloud : [Bike_Rent Dashboard](https://bikesharinganalysis-rifqinabil.streamlit.app/)


