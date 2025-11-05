# PowerShell Script untuk Start Prometheus di Windows
# Pastikan Prometheus sudah di-install dan prometheus.yml sudah di-copy

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Starting Prometheus" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Default Prometheus path (adjust sesuai lokasi install Anda)
$prometheusPath = "C:\prometheus\prometheus.exe"
$configPath = "C:\prometheus\prometheus.yml"

# Check jika Prometheus ada
if (-not (Test-Path $prometheusPath)) {
    Write-Host "`n❌ Prometheus tidak ditemukan di: $prometheusPath" -ForegroundColor Red
    Write-Host "`n📥 Silakan:" -ForegroundColor Yellow
    Write-Host "   1. Download Prometheus dari: https://prometheus.io/download/" -ForegroundColor Yellow
    Write-Host "   2. Extract ke C:\prometheus (atau folder lain)" -ForegroundColor Yellow
    Write-Host "   3. Copy prometheus.yml ke folder Prometheus" -ForegroundColor Yellow
    Write-Host "   4. Edit script ini untuk set path yang benar" -ForegroundColor Yellow
    Write-Host "`n   Atau gunakan Docker (lebih mudah):" -ForegroundColor Cyan
    Write-Host "   docker run -d --name prometheus -p 9090:9090 -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus" -ForegroundColor Cyan
    exit 1
}

# Check jika config file ada
if (-not (Test-Path $configPath)) {
    Write-Host "`n⚠️  Config file tidak ditemukan: $configPath" -ForegroundColor Yellow
    Write-Host "   Copying prometheus.yml..." -ForegroundColor Yellow
    
    $currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $sourceConfig = Join-Path $currentDir "prometheus.yml"
    
    if (Test-Path $sourceConfig) {
        Copy-Item $sourceConfig $configPath -Force
        Write-Host "   ✅ Config file copied!" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Source config file tidak ditemukan!" -ForegroundColor Red
        exit 1
    }
}

# Start Prometheus
Write-Host "`n🚀 Starting Prometheus..." -ForegroundColor Green
Write-Host "   Config: $configPath" -ForegroundColor Gray
Write-Host "`n   Prometheus akan berjalan di: http://127.0.0.1:9090" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop`n" -ForegroundColor Yellow

# Change to Prometheus directory
$prometheusDir = Split-Path -Parent $prometheusPath
Set-Location $prometheusDir

# Run Prometheus
& $prometheusPath --config.file=$configPath

