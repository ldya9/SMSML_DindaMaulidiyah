# Setup Prometheus dan Grafana di Windows

## 🔧 Install Prometheus di Windows

### Step 1: Download Prometheus

1. Buka: https://prometheus.io/download/
2. Download **prometheus-2.xx.x.windows-amd64.zip** (versi terbaru)
3. Extract ke folder yang diinginkan, contoh: `C:\prometheus`

### Step 2: Setup Prometheus

1. Extract file zip ke folder (misalnya `C:\prometheus`)
2. Copy file `prometheus.yml` dari folder `Monitoring dan Logging` ke folder Prometheus:
   ```powershell
   Copy-Item "Monitoring dan Logging\prometheus.yml" "C:\prometheus\prometheus.yml" -Force
   ```
3. Buka PowerShell di folder Prometheus dan jalankan:
   ```powershell
   cd C:\prometheus
   .\prometheus.exe --config.file=prometheus.yml
   ```

### Step 3: Verify Prometheus

- Buka browser: http://127.0.0.1:9090
- Jika berhasil, akan muncul Prometheus UI

---

## 📊 Install Grafana di Windows

### Step 1: Download Grafana

1. Buka: https://grafana.com/grafana/download?platform=windows
2. Download installer Windows (`.msi` file)
3. Install dengan double-click installer

### Step 2: Start Grafana

**Option A: Via Service (Recommended)**
- Grafana akan otomatis berjalan sebagai Windows Service setelah install
- Buka: http://127.0.0.1:3000

**Option B: Via Command Line**
```powershell
# Navigate ke folder Grafana
cd "C:\Program Files\GrafanaLabs\grafana\bin"

# Start Grafana
.\grafana-server.exe
```

### Step 3: Login Grafana

- URL: http://127.0.0.1:3000
- Username: `admin`
- Password: `admin` (akan diminta untuk ganti password pertama kali)

---

## 🚀 Quick Start Script untuk Windows

Buat file `start_monitoring.ps1` untuk memudahkan:

```powershell
# start_monitoring.ps1
Write-Host "Starting Monitoring Services..." -ForegroundColor Green

# Start Prometheus (jika sudah di PATH atau adjust path)
$prometheusPath = "C:\prometheus\prometheus.exe"
if (Test-Path $prometheusPath) {
    Start-Process $prometheusPath -ArgumentList "--config.file=prometheus.yml"
    Write-Host "✅ Prometheus started" -ForegroundColor Green
} else {
    Write-Host "⚠️  Prometheus not found at $prometheusPath" -ForegroundColor Yellow
    Write-Host "   Please install Prometheus first!" -ForegroundColor Yellow
}

# Start Grafana (via service, biasanya sudah running)
Write-Host "✅ Grafana should be running at http://127.0.0.1:3000" -ForegroundColor Green

Write-Host "`nMonitoring services started!" -ForegroundColor Green
Write-Host "Prometheus: http://127.0.0.1:9090" -ForegroundColor Cyan
Write-Host "Grafana: http://127.0.0.1:3000" -ForegroundColor Cyan
```

---

## 📝 Alternative: Menggunakan Docker (Lebih Mudah)

Jika Anda sudah install Docker Desktop, bisa menggunakan Docker:

### Prometheus via Docker:

```powershell
docker run -d `
  --name prometheus `
  -p 9090:9090 `
  -v ${PWD}/Monitoring dan Logging/prometheus.yml:/etc/prometheus/prometheus.yml `
  prom/prometheus
```

### Grafana via Docker:

```powershell
docker run -d `
  --name grafana `
  -p 3000:3000 `
  grafana/grafana
```

---

## 🔍 Troubleshooting

### Prometheus tidak bisa dijalankan

1. **Check apakah file prometheus.exe ada:**
   ```powershell
   Test-Path "C:\prometheus\prometheus.exe"
   ```

2. **Check apakah prometheus.yml ada di folder yang benar:**
   ```powershell
   Test-Path "C:\prometheus\prometheus.yml"
   ```

3. **Jalankan dengan full path:**
   ```powershell
   C:\prometheus\prometheus.exe --config.file=C:\prometheus\prometheus.yml
   ```

### Port sudah digunakan

Jika port 9090 atau 3000 sudah digunakan:

```powershell
# Check port yang digunakan
netstat -ano | findstr :9090
netstat -ano | findstr :3000

# Kill process jika perlu (ganti PID dengan process ID)
taskkill /PID <PID> /F
```

### Grafana tidak bisa diakses

1. Check apakah Grafana service running:
   ```powershell
   Get-Service | Where-Object {$_.Name -like "*grafana*"}
   ```

2. Start service jika belum running:
   ```powershell
   Start-Service Grafana
   ```

---

## ✅ Checklist Setup

- [ ] Prometheus downloaded dan extracted
- [ ] prometheus.yml copied ke folder Prometheus
- [ ] Prometheus bisa dijalankan dan accessible di http://127.0.0.1:9090
- [ ] Grafana installed
- [ ] Grafana accessible di http://127.0.0.1:3000
- [ ] Prometheus data source added di Grafana

