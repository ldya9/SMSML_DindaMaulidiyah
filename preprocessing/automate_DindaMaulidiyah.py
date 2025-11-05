"""
Automated Preprocessing Script for Wine Quality Dataset
Script ini melakukan preprocessing otomatis pada dataset wine quality
sesuai dengan eksperimen yang dilakukan di Eksperimen_Dinda_Maulidiyah.ipynb
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def load_data(data_path):
    """
    Memuat dataset wine quality dari file CSV
    
    Parameters:
    -----------
    data_path : str
        Path ke file CSV dataset
    
    Returns:
    --------
    df : pd.DataFrame
        DataFrame yang berisi dataset
    """
    print(f"Memuat dataset dari: {data_path}")
    df = pd.read_csv(data_path, sep=';')
    print(f"Dataset berhasil dimuat. Shape: {df.shape}")
    return df

def remove_duplicates(df):
    """
    Menghapus data duplikat dari dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang akan dihapus duplikatnya
    
    Returns:
    --------
    df : pd.DataFrame
        DataFrame setelah duplikat dihapus
    """
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"Jumlah data sebelum: {before}, sesudah hapus duplikat: {after}")
    return df

def remove_outliers_iqr(df):
    """
    Menghapus outlier menggunakan metode IQR (Interquartile Range)
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang akan dihapus outliernya
    
    Returns:
    --------
    df_no_outliers : pd.DataFrame
        DataFrame setelah outlier dihapus
    """
    print("\nMenghapus outlier menggunakan metode IQR...")
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    
    # Filter data yang tidak memiliki outlier
    mask = ~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)
    df_no_outliers = df[mask]
    
    print(f"Jumlah data sebelum hapus outlier: {len(df)}")
    print(f"Jumlah data setelah hapus outlier: {len(df_no_outliers)}")
    
    # Tampilkan jumlah outlier per kolom yang tersisa
    outliers = ((df_no_outliers < (Q1 - 1.5 * IQR)) | (df_no_outliers > (Q3 + 1.5 * IQR))).sum()
    print("\nJumlah outlier per kolom setelah pembersihan:")
    print(outliers)
    
    return df_no_outliers

def standardize_features(df, target_col='quality'):
    """
    Melakukan standarisasi fitur numerik menggunakan StandardScaler
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang akan distandarisasi
    target_col : str
        Nama kolom target yang tidak akan distandarisasi
    
    Returns:
    --------
    X_scaled_df : pd.DataFrame
        DataFrame fitur yang sudah distandarisasi
    y : pd.Series
        Series target
    scaler : StandardScaler
        Scaler yang sudah di-fit, untuk digunakan kembali jika diperlukan
    """
    print("\nMelakukan standarisasi fitur...")
    
    # Pisahkan fitur dan target
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Standarisasi fitur numerik
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Buat DataFrame baru hasil scaling
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    
    print("Contoh hasil standarisasi:")
    print(X_scaled_df.head())
    
    return X_scaled_df, y, scaler

def bin_quality(y, bins=[0, 4, 6, 10], labels=['Low', 'Medium', 'High']):
    """
    Melakukan binning pada variabel quality
    
    Parameters:
    -----------
    y : pd.Series
        Series target (quality)
    bins : list
        List batas bin untuk binning
    labels : list
        List label untuk setiap bin
    
    Returns:
    --------
    y_binned : pd.Series
        Series target yang sudah di-binning
    """
    print("\nMelakukan binning pada variabel quality...")
    y_binned = pd.cut(y, bins=bins, labels=labels)
    
    print("Distribusi setelah binning:")
    print(y_binned.value_counts())
    
    return y_binned

def save_processed_data(df_processed, output_path):
    """
    Menyimpan dataset yang sudah diproses ke file CSV
    
    Parameters:
    -----------
    df_processed : pd.DataFrame
        DataFrame yang sudah diproses
    output_path : str
        Path untuk menyimpan file CSV
    """
    # Pastikan direktori output ada
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Direktori {output_dir} berhasil dibuat")
    
    df_processed.to_csv(output_path, index=False)
    print(f"\nDataset hasil preprocessing disimpan ke: {output_path}")
    print(f"Shape final: {df_processed.shape}")

def main():
    """
    Fungsi utama untuk menjalankan seluruh pipeline preprocessing
    """
    print("="*60)
    print("AUTOMATED PREPROCESSING - Wine Quality Dataset")
    print("="*60)
    
    # Path file input dan output
    # Sesuaikan dengan struktur direktori proyek
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    input_path = os.path.join(project_root, 'RedWine_raw', 'winequality-red.csv')
    output_dir = os.path.join(script_dir, 'WineRed_preprocessing')
    output_path = os.path.join(output_dir, 'winequality_preprocessed.csv')
    
    # Langkah 1: Memuat dataset
    df = load_data(input_path)
    
    # Langkah 2: Menghapus data duplikat
    df = remove_duplicates(df)
    
    # Langkah 3: Menghapus outlier menggunakan IQR
    df_no_outliers = remove_outliers_iqr(df)
    
    # Langkah 4: Standarisasi fitur
    X_scaled_df, y, scaler = standardize_features(df_no_outliers, target_col='quality')
    
    # Langkah 5: Binning variabel quality
    y_binned = bin_quality(y)
    
    # Langkah 6: Gabungkan kembali data yang sudah diproses
    df_processed = X_scaled_df.copy()
    df_processed['quality_category'] = y_binned
    
    print("\nPreview data hasil preprocessing:")
    print(df_processed.head())
    
    # Langkah 7: Simpan dataset yang sudah diproses
    save_processed_data(df_processed, output_path)
    
    print("\n" + "="*60)
    print("PREPROCESSING SELESAI!")
    print("="*60)
    
    return df_processed, scaler

if __name__ == "__main__":
    df_processed, scaler = main()
