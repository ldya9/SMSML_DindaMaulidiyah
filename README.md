# Eksperimen SML - Wine Quality Classification

Repository ini berisi eksperimen machine learning untuk klasifikasi kualitas wine menggunakan dataset Wine Quality.

## 📁 Struktur Repository

```
Eksperimen_SML_DindaMaulidiyah/
├── preprocessing/
│   ├── automate_DindaMaulidiyah.py      # Script preprocessing otomatis
│   ├── WineRed_preprocessing/
│   │   └── winequality_preprocessed.csv # Dataset hasil preprocessing
│   └── Eksperimen_Dinda_Maulidiyah.ipynb
├── Membangun_model/
│   ├── modelling.py                     # Script modelling Basic (Autolog MLflow)
│   ├── modelling_tuning.py             # Script modelling Skilled (Manual Logging + Hyperparameter Tuning)
│   ├── WineRed_preprocessing/          # Dataset preprocessing
│   ├── requirements.txt                 # Dependencies
│   ├── screenshoot_dashboard.jpg       # Screenshot MLflow dashboard
│   └── screenshoot_artifak.jpg         # Screenshot MLflow artifacts
├── RedWine_raw/
│   └── winequality-red.csv             # Dataset raw
├── .github/
│   └── workflows/
│       ├── ci-basic.yml                 # CI/CD workflow untuk Basic
│       └── ci-skilled.yml               # CI/CD workflow untuk Skilled
└── README.md                            # File ini
```

## 🚀 Cara Menjalankan

### Prerequisites

- Python 3.12.7
- pip

### Install Dependencies

```bash
pip install -r Membangun_model/requirements.txt
```

### Menjalankan Preprocessing

```bash
python preprocessing/automate_DindaMaulidiyah.py
```

### Menjalankan Modelling

**Basic (2 pts):**
```bash
cd Membangun_model
python modelling.py
```

**Skilled (3 pts):**
```bash
cd Membangun_model
python modelling_tuning.py
```

## 🔄 CI/CD Workflow

Repository ini menggunakan GitHub Actions untuk automation:

- **Basic Workflow** (`.github/workflows/ci-basic.yml`):
  - Install dependencies
  - Run preprocessing
  - Run modelling (Basic)
  - Upload artifacts to GitHub

- **Skilled Workflow** (`.github/workflows/ci-skilled.yml`):
  - Install dependencies
  - Run preprocessing
  - Run modelling dengan hyperparameter tuning
  - Upload artifacts to GitHub

## 📊 Dataset

Dataset yang digunakan: **Wine Quality Red Wine Dataset**
- Sumber: UCI Machine Learning Repository
- Format: CSV
- Lokasi: `RedWine_raw/winequality-red.csv`

## 🛠️ Teknologi yang Digunakan

- Python 3.12.7
- scikit-learn
- MLflow 2.19.0
- pandas
- numpy
- matplotlib
- seaborn

## 📝 Author

**Dinda Maulidiyah**

## 📄 License

This project is for educational purposes.

## 🔐 Secrets Configuration

Untuk menggunakan workflow CI/CD, pastikan Anda telah mengatur secrets berikut di GitHub:

1. Buka repository → **Settings** → **Secrets and variables** → **Actions**
2. Tambahkan secrets yang diperlukan (jika menggunakan upload ke Google Drive atau external storage)

**Catatan:** Untuk workflow yang menggunakan GitHub Actions artifacts, tidak diperlukan secrets tambahan.

