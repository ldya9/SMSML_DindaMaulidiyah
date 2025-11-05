# Workflow CI Directory

Directory ini berisi konfigurasi workflow CI/CD untuk MLflow Project.

## Struktur

- Workflow CI menggunakan MLflow Project untuk menjalankan training model
- Workflow Basic: Menggunakan `mlflow run` dengan entry-point `basic`
- Workflow Skilled: Menggunakan `mlflow run` dengan entry-point `skilled` dan upload artifacts ke GitHub

## File Workflow

Workflow files berada di `.github/workflows/`:
- `ci-basic.yml`: Workflow untuk Basic model training
- `ci-skilled.yml`: Workflow untuk Skilled model training dengan hyperparameter tuning

