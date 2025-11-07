import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

def preprocess_winequality(input_path, output_path):
    """
    Preprocessing data wine quality sesuai dengan notebook Eksperimen_Dinda_Maulidiyah.ipynb
    
    Steps:
    1. Load data
    2. Hapus duplikat
    3. Hapus outlier menggunakan IQR
    4. Standarisasi fitur numerik
    5. Binning quality menjadi kategori (Low, Medium, High)
    6. Simpan hasil
    """
    # 1. Load data
    print("1. Loading data...")
    df = pd.read_csv(input_path, sep=';')
    print(f"   Data awal: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 2. Hapus duplikat
    print("2. Menghapus duplikat...")
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"   Jumlah data sebelum: {before}, sesudah hapus duplikat: {after}")
    
    # 3. Tangani outlier menggunakan IQR
    print("3. Menangani outlier menggunakan metode IQR...")
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    
    df_no_outliers = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    print(f"   Jumlah data sebelum hapus outlier: {len(df)}")
    print(f"   Jumlah data setelah hapus outlier: {len(df_no_outliers)}")
    
    # 4. Pisahkan fitur dan target
    print("4. Memisahkan fitur dan target...")
    X = df_no_outliers.drop('quality', axis=1)
    y = df_no_outliers['quality']
    
    # 5. Standarisasi fitur numerik
    print("5. Standarisasi fitur numerik...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Buat DataFrame baru hasil scaling
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    print("   Standarisasi selesai")
    
    # 6. Binning kualitas wine
    print("6. Binning kualitas wine...")
    bins = [0, 4, 6, 10]
    labels = ['Low', 'Medium', 'High']
    y_binned = pd.cut(y, bins=bins, labels=labels)
    
    print("   Distribusi setelah binning:")
    print(y_binned.value_counts())
    
    # 7. Gabungkan kembali data yang sudah diproses
    print("7. Menggabungkan data yang sudah diproses...")
    df_processed = X_scaled_df.copy()
    df_processed['quality_category'] = y_binned
    
    # 8. Simpan hasil
    print("8. Menyimpan hasil...")
    # Buat folder output jika belum ada
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df_processed.to_csv(output_path, index=False)
    print(f"   Data preprocessing selesai! Hasil disimpan di: {output_path}")
    print(f"   Shape final: {df_processed.shape[0]} rows, {df_processed.shape[1]} columns")

# pemanggilan fungsi
if __name__ == "__main__":
    # Path relatif dari script 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input: dataset raw - coba beberapa lokasi
    possible_paths = [
        os.path.join(script_dir, 'RedWine_raw', 'winequality-red.csv'),  # Lokal di Workflow-CI
        os.path.join(script_dir, '..', 'Eksperimen_SML_DindaMaulidiyah', 'RedWine_raw', 'winequality-red.csv'),  # Di repo utama
    ]
    
    input_path = None
    for path in possible_paths:
        if os.path.exists(path):
            input_path = path
            break
    
    if input_path is None:
        raise FileNotFoundError(
            f"Input file not found in any of these locations:\n" + 
            "\n".join(possible_paths) +
            "\n\nPlease ensure the raw dataset is available."
        )
    
    # Output: dataset preprocessed ke folder MLProject/WineRed_preprocessing
    output_dir = os.path.join(script_dir, 'MLProject', 'WineRed_preprocessing')
    output_path = os.path.join(output_dir, 'winequality_preprocessed.csv')
    
    preprocess_winequality(input_path, output_path)

