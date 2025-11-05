# 🔐 Setup Secrets untuk CI/CD Workflow

## 📋 Overview

Dokumentasi ini menjelaskan cara mengatur secrets di GitHub untuk workflow CI/CD, terutama jika Anda ingin menggunakan fitur upload ke Google Drive atau storage eksternal lainnya.

## 🚀 Setup Dasar (Tidak Memerlukan Secrets)

**Workflow Basic dan Skilled** yang sudah dibuat **TIDAK memerlukan secrets** untuk:
- ✅ Run preprocessing
- ✅ Run modelling
- ✅ Upload artifacts ke GitHub Actions

Artifacts akan otomatis tersimpan di GitHub Actions dan dapat diunduh selama 30 hari (model artifacts) dan 7 hari (preprocessed data).

## 🔑 Setup Secrets (Opsional - untuk Upload External)

Jika Anda ingin upload artifacts ke Google Drive atau storage eksternal, ikuti langkah berikut:

### Cara 1: Setup Google Drive Upload

1. **Buat Google Drive Service Account:**
   - Buka [Google Cloud Console](https://console.cloud.google.com/)
   - Buat project baru atau pilih project yang ada
   - Aktifkan Google Drive API
   - Buat Service Account
   - Download credentials sebagai JSON

2. **Setup Folder di Google Drive:**
   - Buat folder baru di Google Drive
   - Share folder dengan Service Account email (dari JSON credentials)
   - Copy Folder ID dari URL Google Drive

3. **Tambahkan Secrets di GitHub:**
   - Buka repository → **Settings** → **Secrets and variables** → **Actions**
   - Klik **New repository secret**
   - Tambahkan secrets berikut:
     - **Name:** `GOOGLE_DRIVE_FOLDER_ID`
       - **Value:** Folder ID dari Google Drive (contoh: `1a2b3c4d5e6f7g8h9i0j`)
     
     - **Name:** `GOOGLE_DRIVE_CREDENTIALS`
       - **Value:** Isi dari file JSON credentials (copy seluruh isinya)

4. **Uncomment bagian Upload di Workflow:**
   - Buka `.github/workflows/ci-skilled.yml` atau `ci-basic.yml`
   - Uncomment bagian "Upload to Google Drive"
   - Save dan commit

### Cara 2: Setup GitHub LFS (untuk Large Files)

Jika Anda ingin menggunakan GitHub LFS untuk menyimpan model files yang besar:

1. **Install Git LFS:**
   ```bash
   git lfs install
   ```

2. **Track file types:**
   ```bash
   git lfs track "*.pkl"
   git lfs track "*.h5"
   git lfs track "*.joblib"
   ```

3. **Commit .gitattributes:**
   ```bash
   git add .gitattributes
   git commit -m "Add Git LFS tracking"
   ```

4. **Push files:**
   ```bash
   git push origin main
   ```

**Tidak diperlukan secrets tambahan** untuk GitHub LFS.

## ✅ Verifikasi Setup

1. **Test workflow:**
   - Buka tab **Actions** di repository GitHub
   - Klik workflow yang ingin dijalankan
   - Klik **Run workflow**
   - Pilih branch dan klik **Run workflow**

2. **Cek hasil:**
   - Tunggu workflow selesai
   - Klik pada run yang sudah selesai
   - Scroll ke bawah ke bagian **Artifacts**
   - Download artifacts untuk memverifikasi

## 📝 Catatan Penting

- ⚠️ **Jangan commit secrets ke repository!**
- 🔒 Secrets hanya dapat dilihat oleh repository owner dan collaborators dengan akses
- 🗑️ Secrets dapat dihapus atau diupdate kapan saja
- 📦 Artifacts di GitHub Actions akan otomatis terhapus setelah retention period (7-30 hari)

## 🆘 Troubleshooting

### Workflow gagal di step "Run modelling"

**Solusi:**
- Pastikan semua dependencies terinstall dengan benar
- Cek log error di GitHub Actions
- Pastikan dataset preprocessing sudah di-generate dengan benar

### Upload ke Google Drive gagal

**Solusi:**
- Pastikan Service Account memiliki akses ke folder
- Pastikan credentials JSON valid
- Pastikan Folder ID benar
- Cek permissions di Google Drive

### MLflow tracking tidak bekerja

**Solusi:**
- Di CI/CD, MLflow menggunakan file store (bukan server)
- Workflow sudah di-configure untuk menggunakan `file:./mlruns`
- Tidak perlu setup MLflow server di GitHub Actions

## 📚 Referensi

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub LFS](https://git-lfs.github.com/)
- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)

