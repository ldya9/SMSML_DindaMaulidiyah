# Docker Hub Link

## MLflow Project Docker Image

Untuk menjalankan MLflow Project menggunakan Docker, Anda dapat menggunakan image berikut:

### Docker Hub Repository
```
https://hub.docker.com/r/[username]/wine-quality-mlflow
```

### Menjalankan dengan Docker

```bash
# Pull image dari Docker Hub
docker pull [username]/wine-quality-mlflow:latest

# Atau build image lokal
docker build -t wine-quality-mlflow .

# Run MLflow Project dengan Docker
mlflow run . --backend docker --docker-image wine-quality-mlflow:latest
```

### Catatan

- Docker image bersifat opsional untuk Kriteria 3
- Untuk CI/CD, kita menggunakan MLflow Project tanpa Docker (menggunakan conda environment)
- Jika ingin menggunakan Docker, pastikan Dockerfile sudah dibuat di root MLProject

