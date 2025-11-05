# Bukti Monitoring Prometheus

Folder ini berisi screenshot monitoring metrics di Prometheus.

## Screenshot yang Diperlukan:

1. **1.monitoring_http_requests_total.png** - Screenshot query `http_requests_total` di Prometheus
2. **2.monitoring_system_cpu_usage.png** - Screenshot query `system_cpu_usage` di Prometheus
3. **3.monitoring_system_ram_usage.png** - Screenshot query `system_ram_usage` di Prometheus
4. **4.monitoring_api_latency_seconds.png** - Screenshot query `api_latency_seconds` di Prometheus (untuk Skilled)
5. **5.monitoring_throughput_per_minute.png** - Screenshot query `throughput_per_minute` di Prometheus (untuk Skilled)

## Cara Mengambil Screenshot:

1. Buka Prometheus di http://127.0.0.1:9090
2. Masuk ke tab "Query"
3. Ketik query metric (contoh: `http_requests_total{instance="127.0.0.1:8000", job="ml_model_exporter"}`)
4. Klik "Execute"
5. Screenshot hasil query
6. Simpan dengan nama sesuai di atas

