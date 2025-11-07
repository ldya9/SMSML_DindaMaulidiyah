"""
Modelling Tuning Script - Wine Quality Classification
Script ini melakukan training model dengan hyperparameter tuning
menggunakan manual logging MLflow (bukan autolog)
Untuk Kriteria 2 - Skilled (3 pts)
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    classification_report, 
    confusion_matrix,
    roc_auc_score,
    log_loss
)
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

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

# Create a new MLflow Experiment untuk tuning
# Tapi jangan set experiment jika dipanggil dari mlflow run (sudah di-set oleh mlflow run)
mlflow_run_id = os.getenv("MLFLOW_RUN_ID")
if mlflow_run_id is None:
    # Hanya set experiment jika dipanggil langsung (bukan dari mlflow run)
    mlflow.set_experiment("Wine Quality Classification - Tuning - Dinda Maulidiyah")

# PENTING: Jangan menggunakan autolog untuk Skilled
# Kita akan melakukan manual logging

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
    # Drop NaN values sebelum encoding
    y_clean = y.dropna()
    
    # Check if there are any NaN values
    if y.isna().any():
        print(f"Warning: Found {y.isna().sum()} NaN values in target. Dropping them.")
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_clean)
    
    print(f"Label mapping: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")
    
    return y_encoded, label_encoder, y_clean

def calculate_metrics(y_true, y_pred, y_pred_proba=None, label_encoder=None):
    """
    Menghitung berbagai metrik evaluasi model
    
    Parameters:
    -----------
    y_true : np.array
        Target sebenarnya
    y_pred : np.array
        Prediksi model
    y_pred_proba : np.array, optional
        Probabilitas prediksi (untuk log_loss dan roc_auc)
    label_encoder : LabelEncoder, optional
        Label encoder untuk multi-class
    
    Returns:
    --------
    metrics : dict
        Dictionary berisi semua metrik
    """
    metrics = {}
    
    # Basic metrics
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    metrics['precision_macro'] = precision_score(y_true, y_pred, average='macro')
    metrics['precision_weighted'] = precision_score(y_true, y_pred, average='weighted')
    metrics['recall_macro'] = recall_score(y_true, y_pred, average='macro')
    metrics['recall_weighted'] = recall_score(y_true, y_pred, average='weighted')
    metrics['f1_macro'] = f1_score(y_true, y_pred, average='macro')
    metrics['f1_weighted'] = f1_score(y_true, y_pred, average='weighted')
    
    # Log loss dan ROC AUC jika ada probabilitas
    if y_pred_proba is not None:
        try:
            metrics['log_loss'] = log_loss(y_true, y_pred_proba)
            # ROC AUC untuk multi-class
            if label_encoder is not None and len(label_encoder.classes_) > 2:
                metrics['roc_auc_ovr'] = roc_auc_score(y_true, y_pred_proba, 
                                                      multi_class='ovr', average='macro')
                metrics['roc_auc_ovo'] = roc_auc_score(y_true, y_pred_proba, 
                                                      multi_class='ovo', average='macro')
        except Exception as e:
            print(f"Warning: Tidak bisa menghitung log_loss atau roc_auc: {e}")
    
    return metrics

def train_with_hyperparameter_tuning(X_train, y_train, X_test, y_test):
    """
    Melatih model dengan hyperparameter tuning menggunakan GridSearchCV
    
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
    best_model : sklearn model
        Model terbaik setelah tuning
    y_pred : np.array
        Prediksi pada data test
    y_pred_proba : np.array
        Probabilitas prediksi
    best_params : dict
        Parameter terbaik
    """
    print("\n" + "="*60)
    print("HYPERPARAMETER TUNING - Random Forest Classifier")
    print("="*60)
    
    # Define parameter grid untuk Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }
    
    # Base model
    base_model = RandomForestClassifier(random_state=42)
    
    # GridSearchCV
    print("Memulai GridSearchCV...")
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    # Fit grid search
    grid_search.fit(X_train, y_train)
    
    # Best model
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    
    print(f"\nBest parameters: {best_params}")
    print(f"Best CV score: {grid_search.best_score_:.4f}")
    
    # Prediksi
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)
    
    return best_model, y_pred, y_pred_proba, best_params, grid_search

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
    
    # Filter out NaN from classes
    valid_classes = [str(cls) for cls in label_encoder.classes_ if pd.notna(cls)]
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=valid_classes,
                yticklabels=valid_classes)
    plt.title('Confusion Matrix - Wine Quality Classification (Tuned Model)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix disimpan ke: {save_path}")
    plt.close()

def plot_feature_importance(model, feature_names, save_path):
    """
    Membuat dan menyimpan feature importance plot
    
    Parameters:
    -----------
    model : sklearn model
        Model yang sudah dilatih (Random Forest)
    feature_names : list
        Nama-nama fitur
    save_path : str
        Path untuk menyimpan gambar
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        plt.title("Feature Importance - Random Forest")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.ylabel('Importance')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Feature importance plot disimpan ke: {save_path}")
        plt.close()

def main():
    """
    Fungsi utama untuk menjalankan training model dengan tuning
    """
    print("="*60)
    print("MODELLING TUNING - Wine Quality Classification")
    print("Kriteria 2 - Skilled (Manual Logging MLflow)")
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
    
    # Encode target (akan drop NaN)
    y_encoded, label_encoder, y_clean = encode_target(y)
    
    # Drop corresponding rows in X if y has NaN
    if y.isna().any():
        X = X.loc[y_clean.index]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Training dengan hyperparameter tuning
    best_model, y_pred, y_pred_proba, best_params, grid_search = train_with_hyperparameter_tuning(
        X_train, y_train, X_test, y_test
    )
    
    # Calculate metrics
    metrics = calculate_metrics(y_test, y_pred, y_pred_proba, label_encoder)
    
    # Print metrics
    print("\n" + "="*60)
    print("EVALUATION METRICS")
    print("="*60)
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value:.4f}")
    
    print("\nClassification Report:")
    # Filter out NaN from classes (jika ada)
    valid_classes = [str(cls) for cls in label_encoder.classes_ if pd.notna(cls)]
    print(classification_report(y_test, y_pred, target_names=valid_classes))
    
    # Manual logging ke MLflow (PENTING: tidak menggunakan autolog)
    # Note: mlflow run sudah membuat run sendiri
    mlflow_run_id = os.getenv("MLFLOW_RUN_ID")
    is_mlflow_run = mlflow_run_id is not None
    
    # PENTING: Jika dipanggil dari mlflow run, gunakan MLflowClient untuk logging langsung
    # Jangan start run karena akan conflict dengan run yang sudah dibuat mlflow run
    if is_mlflow_run:
        # Gunakan MLflowClient untuk logging langsung ke run ID yang sudah ada
        print(f"Using MLflowClient to log to existing run (ID: {mlflow_run_id})")
        client = MlflowClient(tracking_uri=mlflow.get_tracking_uri())
        
        # Log parameters (manual)
        print("\n" + "="*60)
        print("LOGGING KE MLFLOW (MANUAL)")
        print("="*60)
        
        # Log best parameters
        for param_name, param_value in best_params.items():
            client.log_param(mlflow_run_id, f"best_{param_name}", param_value)
        
        # Log additional parameters
        client.log_param(mlflow_run_id, "model_type", "RandomForestClassifier")
        client.log_param(mlflow_run_id, "test_size", 0.2)
        client.log_param(mlflow_run_id, "random_state", 42)
        client.log_param(mlflow_run_id, "cv_folds", 5)
        client.log_param(mlflow_run_id, "scoring", "accuracy")
        client.log_param(mlflow_run_id, "best_cv_score", grid_search.best_score_)
        
        # Log metrics (manual)
        for metric_name, metric_value in metrics.items():
            client.log_metric(mlflow_run_id, metric_name, metric_value)
        
        # Log model dan artifacts menggunakan MLflowClient
        # Jangan start run karena akan conflict dengan run yang sudah ada
        # Gunakan client untuk log model dan artifacts
        
        # Prepare artifacts first
        # Confusion matrix
        cm_path = os.path.join(script_dir, "confusion_matrix_tuned.png")
        plot_confusion_matrix(y_test, y_pred, label_encoder, cm_path)
        
        # Feature importance
        fi_path = os.path.join(script_dir, "feature_importance.png")
        plot_feature_importance(best_model, X.columns.tolist(), fi_path)
        
        # Classification report as text
        report_path = os.path.join(script_dir, "classification_report.txt")
        with open(report_path, 'w') as f:
            f.write(classification_report(y_test, y_pred, target_names=valid_classes))
        
        # Log artifacts menggunakan client
        client.log_artifact(mlflow_run_id, cm_path, "confusion_matrix")
        client.log_artifact(mlflow_run_id, fi_path, "feature_importance")
        client.log_artifact(mlflow_run_id, report_path, "classification_report")
        
        # Log model - perlu start run sementara untuk log_model
        # Tapi kita akan end run segera setelah log model
        mlflow.start_run(run_id=mlflow_run_id)
        try:
            mlflow.sklearn.log_model(best_model, "model")
        finally:
            # End run segera setelah log model untuk menghindari conflict
            mlflow.end_run()
    else:
        # Hanya start run baru jika dipanggil langsung (bukan dari mlflow run)
        # Untuk testing lokal saja
        mlflow.start_run(run_name="RandomForest_Tuned_Manual")
        try:
            # Log parameters (manual)
            print("\n" + "="*60)
            print("LOGGING KE MLFLOW (MANUAL)")
            print("="*60)
            
            # Log best parameters
            for param_name, param_value in best_params.items():
                mlflow.log_param(f"best_{param_name}", param_value)
            
            # Log additional parameters
            mlflow.log_param("model_type", "RandomForestClassifier")
            mlflow.log_param("test_size", 0.2)
            mlflow.log_param("random_state", 42)
            mlflow.log_param("cv_folds", 5)
            mlflow.log_param("scoring", "accuracy")
            mlflow.log_param("best_cv_score", grid_search.best_score_)
            
            # Log metrics (manual - sama seperti autolog)
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model
            mlflow.sklearn.log_model(best_model, "model")
            
            # Log artifacts
            # Confusion matrix
            cm_path = os.path.join(script_dir, "confusion_matrix_tuned.png")
            plot_confusion_matrix(y_test, y_pred, label_encoder, cm_path)
            mlflow.log_artifact(cm_path, "confusion_matrix")
            
            # Feature importance
            fi_path = os.path.join(script_dir, "feature_importance.png")
            plot_feature_importance(best_model, X.columns.tolist(), fi_path)
            mlflow.log_artifact(fi_path, "feature_importance")
            
            # Classification report as text
            report_path = os.path.join(script_dir, "classification_report.txt")
            with open(report_path, 'w') as f:
                f.write(classification_report(y_test, y_pred, target_names=valid_classes))
            mlflow.log_artifact(report_path, "classification_report")
        finally:
            mlflow.end_run()
    
    print("\n" + "="*60)
    print("MODEL TRAINING DAN TUNING SELESAI!")
    print("="*60)
    print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    try:
        exp = mlflow.get_experiment_by_name('Wine Quality Classification - Tuning - Dinda Maulidiyah')
        if exp:
            print(f"Experiment: {exp.name}")
    except:
        print("Experiment info not available")
    print("="*60)

if __name__ == "__main__":
    main()

