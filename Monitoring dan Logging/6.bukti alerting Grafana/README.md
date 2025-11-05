# Bukti Alerting Grafana

Folder ini berisi screenshot alert rules dan notifikasi alert di Grafana.

## Screenshot yang Diperlukan (untuk Skilled):

1. **1.rules_cpu_usage.png** - Screenshot alert rule untuk CPU usage
2. **2.notifikasi_cpu_usage.png** - Screenshot notifikasi alert ketika CPU usage tinggi
3. **3.rules_ram_usage.png** - Screenshot alert rule untuk RAM usage (opsional, untuk multiple alerts)
4. **4.notifikasi_ram_usage.png** - Screenshot notifikasi alert ketika RAM usage tinggi (opsional)

## Minimum Requirement:

Untuk Skilled, minimal diperlukan:
- 1 alert rule (screenshot rules)
- 1 notifikasi alert (screenshot notifikasi)

## Cara Mengambil Screenshot:

### Screenshot Alert Rules:
1. Buka Grafana → Alerting → Alert rules
2. Klik pada alert rule yang dibuat
3. Screenshot halaman konfigurasi alert rule
4. Simpan dengan nama `1.rules_<metrik>.png`

### Screenshot Notifikasi Alert:
1. Trigger alert (dengan cara mengirim banyak request atau membuat CPU/RAM tinggi)
2. Buka Alerting → Alert rules → Klik alert yang firing
3. Atau cek notifikasi di contact point
4. Screenshot notifikasi alert
5. Simpan dengan nama `2.notifikasi_<metrik>.png`

