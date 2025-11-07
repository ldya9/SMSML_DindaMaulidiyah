# Eksperimen SML - Dinda Maulidiyah

Repository ini berisi eksperimen machine learning untuk klasifikasi kualitas wine menggunakan dataset Wine Quality.

## 📁 Struktur Repository

```
Eksperimen_SML_DindaMaulidiyah/
├── preprocessing/
│   ├── automate_DindaMaulidiyah.py      # Script preprocessing otomatis
│   ├── Eksperimen_Dinda_Maulidiyah.ipynb # Notebook eksperimen
│   └── WineRed_preprocessing/
│       └── winequality_preprocessed.csv # Dataset hasil preprocessing
├── RedWine_raw/
│   └── winequality-red.csv              # Dataset raw
└── README.md                             # File ini
```

## 🚀 Cara Menggunakan

### 1. Preprocessing Data

Jalankan script preprocessing untuk memproses dataset raw:

```bash
python preprocessing/automate_DindaMaulidiyah.py
```

Script ini akan:
- Memuat dataset raw dari `RedWine_raw/winequality-red.csv`
- Menghapus duplikat
- Menangani outlier menggunakan metode IQR
- Standarisasi fitur numerik
- Binning kualitas wine menjadi kategori (Low, Medium, High)
- Menyimpan hasil ke `preprocessing/WineRed_preprocessing/winequality_preprocessed.csv`

### 2. Eksperimen dengan Jupyter Notebook

Buka dan jalankan notebook `preprocessing/Eksperimen_Dinda_Maulidiyah.ipynb` untuk melihat eksperimen lengkap.

## 📊 Dataset

Dataset yang digunakan adalah **Wine Quality Dataset** dari UCI Machine Learning Repository:
- **Sumber**: [UCI ML Repository - Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- **Format**: CSV dengan separator `;`
- **Fitur**: 11 fitur numerik (fixed acidity, volatile acidity, dll.)
- **Target**: Quality (0-10)

## 🔧 Requirements

```txt
pandas>=2.1.0
numpy>=1.26.0
scikit-learn>=1.3.0
matplotlib>=3.8.0
seaborn>=0.13.0
jupyter
```

Install dengan:
```bash
pip install -r requirements.txt
```

## 📝 Catatan

- Dataset hasil preprocessing siap digunakan untuk training model
- Preprocessing meliputi: removal duplikat, outlier handling, standardisasi, dan binning
- Kualitas wine dikategorikan menjadi: Low (0-4), Medium (5-6), High (7-10)

## 👤 Author

**Dinda Maulidiyah**

---

*Repository ini merupakan bagian dari tugas Machine Learning - Eksperimen Dataset*

