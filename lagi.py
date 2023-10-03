import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Halaman 2
def halaman1():
    st.header("Klasifikasi Data")
    
    # Load Model
    model = joblib.load("modelsvmbe")
    
    scaler = joblib.load("barulagi")
    
    # Dictionary Keterangan Kolom
    keterangan_kolom = {
    'prodi': {
        1: 'Fisika',
        2: 'Matematika',
        3: 'Teknik Mesin',
        4: 'Teknik Elektro',
        5: 'Teknik Kimia',
        6: 'Teknik Material Materulgi',
        7: 'Teknik Sipil',
        8: 'Teknik Perkapalan',
        9: 'Perencanaan Wilayah dan Kota',
        10: 'Sistem Informasi',
        11: 'Informatika',
        12: 'Teknik Lingkungan',
        13: 'Teknik Kelautan',
        14: 'Teknik Arsitektur',
        15: 'Teknik Statistika',
        16: 'Ilmu Aktuaria',
        17: 'RK',
        18: 'Teknologi Pangan',
        20: 'Bisnis Digital',
        21: 'Teknik Logistik',
        22: 'DKV',
    },
    'jalurmasuk':{
        1: 'SNMPTN',
        2: 'SBMPTN',
        3: 'Mandiri',
    },
    'jmm1':{
        1: '1',
        0: '-',
    },
    'jmm2':{
        1: '1',
        0: '-',
    },
    'jmm3':{
        1: '1',
        0: '-',
    },
    'Klasifikasi':{
        1: 'Tidak Berpotensi Resign',
        0: 'Berpotensi Resign',
    },
    'ips1':{
        1: '0 <= nilai <1.00',
        2: '1.00 <= nilai <2.00',
        3: '2.00 <= nilai <2.50',
        4: '2.50 <= nilai <3.00',
        5: '3.00 <= nilai <3.50',
        6: '3.50 <= nilai < 4.00',
    },
    'ips2':{
        1: '0 <= nilai <1.00',
        2: '1.00 <= nilai <2.00',
        3: '2.00 <= nilai <2.50',
        4: '2.50 <= nilai <3.00',
        5: '3.00 <= nilai <3.50',
        6: '3.50 <= nilai < 4.00',
    },
    'ips3':{
        1: '0 <= nilai <1.00',
        2: '1.00 <= nilai <2.00',
        3: '2.00 <= nilai <2.50',
        4: '2.50 <= nilai <3.00',
        5: '3.00 <= nilai <3.50',
        6: '3.50 <= nilai < 4.00',
    },
    'beasiswa':{
        1: 'Ya',
        0: 'Tidak',
    },
    # Tambahkan keterangan untuk kolom lainnya
}
    file = st.file_uploader("Upload file Excel", type=["xlsx", "xls"])
    
    if file is not None:
        # Read Excel File
        data = pd.read_excel(file)
        
        # Transformasi Data Baru
        scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
        normalisasi_data = scaler.fit_transform(data)
        
        # Perform Classification
        predictions = model.predict(normalisasi_data)
        
        # Add Predictions to Data
        data['Klasifikasi'] = predictions
        
        # Add Column Descriptions
        for kolom, keterangan in keterangan_kolom.items():
            data[kolom] = data[kolom].map(keterangan)
        
        # Display Data and Predictions
        st.header("Tabel Data dan Hasil Klasifikasi")
        st.dataframe(data)
        return (data)

# Halaman 3
def halaman3():
    st.header("Visualisasi Data Setelah Dilakukan Klasifikasi")
    data_klasifikasi = st.session_state.get('data_klasifikasi')
    if data_klasifikasi is not None:
        st.write("Data Klasifikasi:")
        st.dataframe(data_klasifikasi)
        
        # Visualisasi jumlah mahasiswa aktif dan resign
        st.subheader("Grafik Hasil Klasifikasi")
        status_count = data_klasifikasi["Klasifikasi"].value_counts().reset_index()
        status_count.columns = ["Klasifikasi", "Jumlah Mahasiswa"]
        fig = px.bar(status_count, x="Klasifikasi", y="Jumlah Mahasiswa", labels={"Klasifikasi": "Klasifikasi", "Jumlah Mahasiswa": "Jumlah Mahasiswa"})
        st.plotly_chart(fig)
        
        # Visualisasi jumlah mahasiswa aktif dan resign
        st.subheader("Grafik Berdasarkan Jalur Masuk")
        jalurmasuk_count = data_klasifikasi.groupby(["jalurmasuk", "Klasifikasi"]).size().reset_index(name="Jumlah Mahasiswa")
        fig = px.bar(jalurmasuk_count, x="jalurmasuk", y="Jumlah Mahasiswa", color="Klasifikasi",
                     labels={"jalurmasuk": "Jalur Masuk", "Jumlah Mahasiswa": "Jumlah Mahasiswa", "Klasifikasi": "Klasifikasi"})
        st.plotly_chart(fig)
        
    else:
        st.warning("Belum ada data klasifikasi. Silakan upload file data baru dan lakukan klasifikasi terlebih dahulu.")

# Main App
def main():
    st.title("Klasifikasi Mahasiswa Berpotensi Melakukan Resign")

    # Inisialisasi session state
    if 'data_klasifikasi' not in st.session_state:
        st.session_state.data_klasifikasi = None

    # Pilihan halaman
    halaman = st.sidebar.selectbox("Pilih Halaman", ("Klasifikasi Data", "Visualisasi Data"))

    if halaman == "Klasifikasi Data":
        data_klasifikasi = halaman1()
        st.session_state.data_klasifikasi = data_klasifikasi
    elif halaman == "Visualisasi Data":
        halaman3()

if __name__ == '__main__':
    main()
