
import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_winequality(input_path, output_path):
    # 1. Load data
    df = pd.read_csv(input_path, sep=';')

    # 2. Hapus duplikat
    df = df.drop_duplicates()

    # 3. Tangani outlier
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

    # 4. Standarisasi fitur numerik
    scaler = StandardScaler()
    features = df.drop('quality', axis=1)
    scaled_features = scaler.fit_transform(features)
    df_scaled = pd.DataFrame(scaled_features, columns=features.columns)
    df_scaled['quality'] = df['quality'].values

    # 5. Simpan hasil
    df_scaled.to_csv(output_path, index=False)
    print(f" Data preprocessing selesai! Hasil disimpan di: {output_path}")

# Contoh pemanggilan fungsi
if __name__ == "__main__":
    preprocess_winequality('winequality-red.csv', 'winequality_preprocessed.csv')
