# GitHub Actions Workflows

Repository ini berisi workflow CI/CD untuk automation pipeline machine learning.

## Workflows yang Tersedia

### 1. `ci-basic.yml` - Basic Workflow

Workflow untuk **Basic (2 pts)** yang mencakup:
- Install dependencies
- Run preprocessing (`automate_DindaMaulidiyah.py`)
- Run modelling (`modelling.py`) dengan MLflow autolog
- Upload artifacts ke GitHub Actions

### 2. `ci-skilled.yml` - Skilled Workflow

Workflow untuk **Skilled (3 pts)** yang mencakup:
- Install dependencies
- Run preprocessing (`automate_DindaMaulidiyah.py`)
- Run modelling dengan hyperparameter tuning (`modelling_tuning.py`) dengan manual logging MLflow
- Upload artifacts ke GitHub Actions
- Opsional: Upload ke Google Drive (dengan konfigurasi secrets)

## Cara Menggunakan

### Trigger Otomatis
Workflow akan otomatis berjalan ketika:
- Push ke branch `main` atau `master`
- Pull request ke branch `main` atau `master`

### Trigger Manual
1. Buka tab **Actions** di repository GitHub
2. Pilih workflow yang ingin dijalankan (Basic atau Skilled)
3. Klik **Run workflow**
4. Pilih branch dan klik **Run workflow**

## Artifacts

Setelah workflow selesai, artifacts dapat diunduh dari:
- **Preprocessed Data:** Retained selama 7 hari
- **Model Artifacts:** Retained selama 30 hari

Cara download:
1. Buka tab **Actions**
2. Klik pada run yang sudah selesai
3. Scroll ke bagian **Artifacts**
4. Klik nama artifact untuk download

## Konfigurasi

### MLflow Tracking URI

Di CI/CD environment, workflow secara otomatis mengubah MLflow tracking URI dari:
```python
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
```

menjadi:
```python
mlflow.set_tracking_uri("file:./mlruns")
```

Ini memungkinkan MLflow bekerja di GitHub Actions tanpa perlu MLflow server.

### Python Version

Workflow menggunakan Python 3.12.7 sesuai requirement.

### Dependencies

Dependencies diinstall dari:
- `Membangun_model/requirements.txt`
- Preprocessing dependencies diinstall secara eksplisit

## Secrets (Opsional)

Untuk upload ke Google Drive, lihat [SETUP_SECRETS.md](../SETUP_SECRETS.md).

## Troubleshooting

### Workflow gagal di step "Run preprocessing"

**Kemungkinan penyebab:**
- Dataset raw tidak ditemukan
- Path file tidak sesuai

**Solusi:**
- Pastikan `RedWine_raw/winequality-red.csv` ada di repository
- Cek path di `automate_DindaMaulidiyah.py`

### Workflow gagal di step "Run modelling"

**Kemungkinan penyebab:**
- Preprocessed data tidak ditemukan
- Dependencies tidak terinstall dengan benar

**Solusi:**
- Pastikan step preprocessing berhasil
- Cek log error untuk detail lebih lanjut

### MLflow tidak bekerja

**Solusi:**
- Workflow sudah mengubah tracking URI secara otomatis
- Pastikan tidak ada error di log MLflow

## Notes

- Workflow akan berjalan di Ubuntu latest
- Setiap job berjalan di environment yang fresh
- Artifacts di-pass antar jobs menggunakan GitHub Actions artifacts
- MLflow runs disimpan sebagai artifacts dan dapat diunduh

