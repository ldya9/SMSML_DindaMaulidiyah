"""
Prometheus Exporter untuk ML Model Monitoring
Script ini mengekspor metrics ke Prometheus untuk monitoring model ML
"""

from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time
import psutil
import os
from flask import Flask, request, jsonify
import threading
import mlflow
import mlflow.pyfunc

# Inisialisasi Flask app untuk inference endpoint
app = Flask(__name__)

# Inisialisasi Prometheus metrics
# Counter untuk jumlah request
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram untuk latensi
api_latency = Histogram(
    'api_latency_seconds',
    'API latency in seconds',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Gauge untuk throughput (requests per minute)
throughput_gauge = Gauge(
    'throughput_per_minute',
    'Number of requests per minute'
)

# Gauge untuk penggunaan CPU
cpu_usage = Gauge(
    'system_cpu_usage',
    'System CPU usage percentage',
    ['instance', 'job']
)

# Gauge untuk penggunaan RAM
ram_usage = Gauge(
    'system_ram_usage',
    'System RAM usage percentage',
    ['instance', 'job']
)

# Gauge untuk jumlah request API model
api_requests_count = Gauge(
    'api_model_requests_total',
    'Total number of API model requests'
)

# Gauge untuk model prediction accuracy (jika tersedia)
model_accuracy = Gauge(
    'model_accuracy',
    'Model prediction accuracy'
)

# Variabel global untuk tracking
request_count = 0
start_time = time.time()
model = None

def load_model(model_uri):
    """Load MLflow model"""
    global model
    try:
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Model loaded successfully from {model_uri}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def update_system_metrics():
    """Update system metrics (CPU, RAM) secara berkala"""
    while True:
        try:
            # Update CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_usage.labels(instance='127.0.0.1:8000', job='ml_model_exporter').set(cpu_percent)
            
            # Update RAM usage
            ram_percent = psutil.virtual_memory().percent
            ram_usage.labels(instance='127.0.0.1:8000', job='ml_model_exporter').set(ram_percent)
            
            time.sleep(5)  # Update setiap 5 detik
        except Exception as e:
            print(f"Error updating system metrics: {e}")
            time.sleep(5)

def update_throughput():
    """Update throughput metrics"""
    global request_count, start_time
    while True:
        try:
            current_time = time.time()
            elapsed_minutes = (current_time - start_time) / 60.0
            if elapsed_minutes > 0:
                current_throughput = request_count / elapsed_minutes
                throughput_gauge.set(current_throughput)
            time.sleep(60)  # Update setiap 1 menit
        except Exception as e:
            print(f"Error updating throughput: {e}")
            time.sleep(60)

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint untuk inference model"""
    global request_count
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    start = time.time()
    
    try:
        # Get request data
        data = request.get_json()
        
        # Perform prediction
        prediction = model.predict([data['features']])
        
        # Calculate latency
        latency = time.time() - start
        
        # Update metrics
        request_count += 1
        http_requests_total.labels(
            method='POST',
            endpoint='/predict',
            status='200'
        ).inc()
        
        api_latency.labels(endpoint='/predict').observe(latency)
        api_requests_count.set(request_count)
        
        return jsonify({
            'prediction': prediction[0].tolist() if hasattr(prediction[0], 'tolist') else int(prediction[0]),
            'latency': latency
        }), 200
        
    except Exception as e:
        http_requests_total.labels(
            method='POST',
            endpoint='/predict',
            status='500'
        ).inc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint (akan di-handle oleh prometheus_client)"""
    from prometheus_client import generate_latest
    from flask import Response
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    # Load model dari MLflow
    # Ganti dengan path model Anda
    # Contoh: "runs:/<run_id>/model" atau "models:/<model_name>/<version>"
    # Atau path lokal: "file:///path/to/model"
    
    # Untuk testing, kita akan menggunakan model dari MLflow runs
    # User perlu mengganti ini dengan path model mereka
    model_uri = os.getenv('MLFLOW_MODEL_URI', 'runs:/latest/model')
    
    print("Loading model...")
    load_model(model_uri)
    
    # Start Prometheus metrics server di port 8000
    print("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)
    
    # Start background threads untuk update metrics
    threading.Thread(target=update_system_metrics, daemon=True).start()
    threading.Thread(target=update_throughput, daemon=True).start()
    
    # Start Flask app untuk inference endpoint di port 5001
    print("Starting Flask inference server on port 5001...")
    print("Prometheus metrics available at: http://127.0.0.1:8000/metrics")
    print("Inference endpoint available at: http://127.0.0.1:5001/predict")
    
    app.run(host='127.0.0.1', port=5001, debug=False)

