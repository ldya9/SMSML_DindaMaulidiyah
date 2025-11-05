# 🚀 Panduan Setup Repository GitHub

## 📋 Checklist Sebelum Push ke GitHub

### ✅ 1. Pastikan Struktur File Lengkap

```
Eksperimen_SML_DindaMaulidiyah/
├── .github/
│   ├── workflows/
│   │   ├── ci-basic.yml
│   │   ├── ci-skilled.yml
│   │   └── README.md
│   └── SETUP_SECRETS.md
├── preprocessing/
│   ├── automate_DindaMaulidiyah.py
│   └── WineRed_preprocessing/
│       └── winequality_preprocessed.csv
├── Membangun_model/
│   ├── modelling.py
│   ├── modelling_tuning.py
│   ├── requirements.txt
│   ├── WineRed_preprocessing/
│   │   └── winequality_preprocessed.csv
│   ├── screenshoot_dashboard.jpg  (tambahkan sendiri)
│   └── screenshoot_artifak.jpg    (tambahkan sendiri)
├── RedWine_raw/
│   └── winequality-red.csv
├── .gitignore
├── README.md
└── GITHUB_SETUP.md
```

### ✅ 2. Inisialisasi Git Repository

```bash
# Inisialisasi git (jika belum)
git init

# Tambahkan remote repository
git remote add origin https://github.com/USERNAME/REPOSITORY_NAME.git

# Atau jika sudah ada remote
git remote set-url origin https://github.com/USERNAME/REPOSITORY_NAME.git
```

### ✅ 3. Buat Repository di GitHub

1. Buka [GitHub](https://github.com)
2. Klik **New repository** (ikon + di kanan atas)
3. Isi:
   - **Repository name:** `Eksperimen_SML_DindaMaulidiyah` (atau nama lain)
   - **Description:** "Wine Quality Classification using MLflow"
   - **Visibility:** ✅ **Public** (penting untuk Kriteria 3!)
   - Jangan centang "Initialize with README" (karena sudah ada)
4. Klik **Create repository**

### ✅ 4. Commit dan Push

```bash
# Stage semua file
git add .

# Commit
git commit -m "Initial commit: Setup CI/CD pipeline for Wine Quality Classification"

# Push ke GitHub (branch main)
git branch -M main
git push -u origin main
```

## 🔄 Workflow CI/CD

### Cara Menjalankan Workflow

1. **Otomatis:** Workflow akan berjalan otomatis saat:
   - Push ke branch `main` atau `master`
   - Pull request ke branch `main` atau `master`

2. **Manual:**
   - Buka tab **Actions** di GitHub
   - Pilih workflow (Basic atau Skilled)
   - Klik **Run workflow**
   - Pilih branch dan klik **Run workflow**

### Verifikasi Workflow

1. Buka tab **Actions** di repository
2. Klik pada workflow run yang sedang berjalan
3. Monitor setiap step:
   - ✅ Data Preprocessing
   - ✅ Model Training
   - ✅ Upload Artifacts
4. Setelah selesai, download artifacts untuk verifikasi

## 🔐 Secrets (Opsional)

Jika ingin upload ke Google Drive, ikuti langkah di [.github/SETUP_SECRETS.md](.github/SETUP_SECRETS.md).

**Catatan:** Untuk Kriteria 3, upload ke GitHub Actions artifacts sudah cukup. Tidak perlu setup Google Drive.

## 📝 Tips

1. **Pastikan repository Public:**
   - Repository harus **Public** agar reviewer bisa melihat
   - Settings → Change visibility → Make public

2. **Test Workflow:**
   - Setelah push pertama, cek tab Actions
   - Pastikan workflow berjalan tanpa error
   - Download artifacts untuk verifikasi

3. **Commit Message:**
   - Gunakan commit message yang jelas
   - Contoh: "Add CI/CD workflow for Basic model training"

4. **Branch Protection (Opsional):**
   - Jika ingin, bisa setup branch protection rules
   - Settings → Branches → Add rule

## ✅ Checklist Final

Sebelum submit, pastikan:

- [ ] Repository sudah Public
- [ ] Semua file sudah di-commit dan push
- [ ] Workflow CI/CD sudah berjalan dengan sukses
- [ ] Artifacts sudah ter-upload dengan benar
- [ ] README.md sudah lengkap dan informatif
- [ ] .gitignore sudah mengabaikan file yang tidak perlu
- [ ] Screenshots sudah ditambahkan (jika diperlukan)

## 🆘 Troubleshooting

### Error: "remote origin already exists"

**Solusi:**
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/REPOSITORY_NAME.git
```

### Error: "failed to push some refs"

**Solusi:**
```bash
git pull origin main --rebase
git push -u origin main
```

### Workflow tidak berjalan

**Solusi:**
- Pastikan file workflow ada di `.github/workflows/`
- Pastikan syntax YAML benar
- Cek tab Actions untuk error message

## 📚 Referensi

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Repository Settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)

---

**Selamat! Repository GitHub Anda sudah siap untuk Kriteria 3! 🎉**

