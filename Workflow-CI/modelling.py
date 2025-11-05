"""
Modelling Script - Wine Quality Classification
Script ini melakukan training model machine learning menggunakan MLflow autolog
Untuk Kriteria 2 - Basic (2 pts)
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Parse arguments dari MLflow Project
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="WineRed_preprocessing/winequality_preprocessed.csv")
parser.add_argument("--mlflow_tracking_uri", type=str, default="file:./mlruns")
args = parser.parse_args()

# Setup MLflow Tracking
# Gunakan tracking URI dari parameter atau environment variable
tracking_uri = args.mlflow_tracking_uri
if os.getenv("MLFLOW_TRACKING_URI"):
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(tracking_uri)

# Create a new MLflow Experiment
mlflow.set_experiment("Wine Quality Classification - Dinda Maulidiyah")

# Enable autologging untuk scikit-learn
mlflow.sklearn.autolog()

def load_preprocessed_data(data_path):
    """
    Memuat dataset yang sudah dipreprocessing
    
    Parameters:
    -----------
    data_path : str
        Path ke file CSV dataset yang sudah dipreprocessing
    
    Returns:
    --------
    X : pd.DataFrame
        Fitur-fitur untuk training
    y : pd.Series
        Target variable
    """
    print(f"Memuat dataset preprocessing dari: {data_path}")
    df = pd.read_csv(data_path)
    
    # Pisahkan fitur dan target
    X = df.drop('quality_category', axis=1)
    y = df['quality_category']
    
    print(f"Shape X: {X.shape}")
    print(f"Shape y: {y.shape}")
    print(f"Distribusi target:\n{y.value_counts()}")
    
    return X, y

def encode_target(y):
    """
    Encode target variable menjadi numerik
    
    Parameters:
    -----------
    y : pd.Series
        Target variable kategorikal
    
    Returns:
    --------
    y_encoded : np.array
        Target variable yang sudah di-encode
    label_encoder : LabelEncoder
        Label encoder yang digunakan
    """
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    print(f"Label mapping: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")
    
    return y_encoded, label_encoder

def train_model(X_train, y_train, X_test, y_test):
    """
    Melatih model Logistic Regression
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Fitur training
    y_train : np.array
        Target training
    X_test : pd.DataFrame
        Fitur testing
    y_test : np.array
        Target testing
    
    Returns:
    --------
    model : sklearn model
        Model yang sudah dilatih
    y_pred : np.array
        Prediksi pada data test
    """
    print("\n" + "="*60)
    print("TRAINING MODEL - Logistic Regression")
    print("="*60)
    
    # Inisialisasi model
    model = LogisticRegression(random_state=42, max_iter=1000)
    
    # Training model (autolog akan otomatis mencatat parameter dan metrik)
    print("Memulai training...")
    model.fit(X_train, y_train)
    
    # Prediksi
    y_pred = model.predict(X_test)
    
    # Evaluasi
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, y_pred

def plot_confusion_matrix(y_test, y_pred, label_encoder, save_path):
    """
    Membuat dan menyimpan confusion matrix
    
    Parameters:
    -----------
    y_test : np.array
        Target sebenarnya
    y_pred : np.array
        Prediksi model
    label_encoder : LabelEncoder
        Label encoder untuk mapping label
    save_path : str
        Path untuk menyimpan gambar
    """
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    plt.title('Confusion Matrix - Wine Quality Classification')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix disimpan ke: {save_path}")
    plt.close()

def main():
    """
    Fungsi utama untuk menjalankan training model
    """
    print("="*60)
    print("MODELLING - Wine Quality Classification")
    print("Kriteria 2 - Basic (Autolog MLflow)")
    print("="*60)
    
    # Path dataset preprocessing dari argument atau default
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Gunakan path dari argument, atau cari di lokasi standar
    if args.data_path and os.path.exists(args.data_path):
        data_path = args.data_path
    elif os.path.exists(os.path.join(script_dir, args.data_path)):
        data_path = os.path.join(script_dir, args.data_path)
    else:
        # Fallback ke lokasi default
        local_data_path = os.path.join(script_dir, 'WineRed_preprocessing', 'winequality_preprocessed.csv')
        if os.path.exists(local_data_path):
            data_path = local_data_path
        else:
            project_root = os.path.dirname(script_dir)
            data_path = os.path.join(project_root, 'preprocessing', 'WineRed_preprocessing', 'winequality_preprocessed.csv')
    
    # Load data
    X, y = load_preprocessed_data(data_path)
    
    # Encode target
    y_encoded, label_encoder = encode_target(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Training model dengan autolog
    # MLflow akan otomatis mencatat:
    # - Parameter model
    # - Metrik (accuracy, dll)
    # - Model artifact
    # - Dependencies
    with mlflow.start_run(run_name="LogisticRegression_Basic"):
        model, y_pred = train_model(X_train, y_train, X_test, y_test)
        
        # Log model secara eksplisit (meskipun autolog sudah melakukannya)
        mlflow.sklearn.log_model(model, "model")
        
        # Log confusion matrix
        cm_path = os.path.join(script_dir, "confusion_matrix.png")
        plot_confusion_matrix(y_test, y_pred, label_encoder, cm_path)
        mlflow.log_artifact(cm_path, "confusion_matrix")
        
        # Log additional info
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        
        print("\n" + "="*60)
        print("MODEL TRAINING SELESAI!")
        print("="*60)
        print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
        print(f"Experiment: {mlflow.get_experiment_by_name('Wine Quality Classification - Dinda Maulidiyah').name}")
        print("="*60)

if __name__ == "__main__":
    main()

