from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time
import threading
import psutil
import mlflow
import mlflow.sklearn

# --------------------------------------------
# METRICS SETUP
# --------------------------------------------
# Counter untuk jumlah request
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram untuk latensi
api_latency_seconds = Histogram(
    'api_latency_seconds',
    'API latency in seconds',
    ['endpoint']
)

# Gauge untuk throughput
throughput_per_minute = Gauge(
    'throughput_per_minute',
    'Number of requests per minute'
)

# Gauge untuk CPU usage
system_cpu_usage = Gauge(
    'system_cpu_usage',
    'System CPU usage percentage',
    ['instance', 'job']
)

# Gauge untuk RAM usage
system_ram_usage = Gauge(
    'system_ram_usage',
    'System RAM usage percentage',
    ['instance', 'job']
)

# --------------------------------------------
# FLASK APP SETUP
# --------------------------------------------
app = Flask(__name__)
model = None  # model global
request_count = 0
start_time = time.time()

# --------------------------------------------
# LOAD MODEL
# --------------------------------------------
def load_model(model_uri):
    global model
    try:
        model = mlflow.sklearn.load_model(model_uri)
        print(f"Model loaded successfully from {model_uri}")
    except Exception as e:
        print(f"Error loading model: {e}")

# --------------------------------------------
# UPDATE SYSTEM METRICS
# --------------------------------------------
def update_system_metrics():
    """Update system metrics (CPU, RAM) secara berkala"""
    while True:
        try:
            # Update CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            system_cpu_usage.labels(instance='127.0.0.1:8000', job='ml_model_exporter').set(cpu_percent)
            
            # Update RAM usage
            ram_percent = psutil.virtual_memory().percent
            system_ram_usage.labels(instance='127.0.0.1:8000', job='ml_model_exporter').set(ram_percent)
            
            time.sleep(5)  # Update setiap 5 detik
        except Exception as e:
            print(f"Error updating system metrics: {e}")
            time.sleep(5)

# --------------------------------------------
# UPDATE THROUGHPUT
# --------------------------------------------
def update_throughput():
    """Update throughput metrics"""
    global request_count, start_time
    while True:
        try:
            current_time = time.time()
            elapsed_minutes = (current_time - start_time) / 60.0
            if elapsed_minutes > 0:
                current_throughput = request_count / elapsed_minutes
                throughput_per_minute.set(current_throughput)
            time.sleep(60)  # Update setiap 1 menit
        except Exception as e:
            print(f"Error updating throughput: {e}")
            time.sleep(60)

# --------------------------------------------
# ENDPOINT: HEALTH CHECK
# --------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    http_requests_total.labels(method='GET', endpoint='/health', status='200').inc()
    if model is not None:
        return jsonify({"status": "ok"}), 200
    else:
        http_requests_total.labels(method='GET', endpoint='/health', status='500').inc()
        return jsonify({"status": "model not loaded"}), 500

# --------------------------------------------
# ENDPOINT: PREDICT
# --------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    global request_count
    start = time.time()
    
    if model is None:
        http_requests_total.labels(method='POST', endpoint='/predict', status='500').inc()
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        features = data.get("features")
        
        # Perform prediction
        preds = model.predict([features])
        
        # Calculate latency
        latency = time.time() - start
        
        # Update metrics
        request_count += 1
        http_requests_total.labels(
            method='POST',
            endpoint='/predict',
            status='200'
        ).inc()
        
        api_latency_seconds.labels(endpoint='/predict').observe(latency)
        
        return jsonify({"prediction": preds.tolist()}), 200
    except Exception as e:
        http_requests_total.labels(
            method='POST',
            endpoint='/predict',
            status='500'
        ).inc()
        return jsonify({"error": str(e)}), 500

# --------------------------------------------
# MAIN ENTRY
# --------------------------------------------
if __name__ == "__main__":
    # Path model
    model_uri = r"C:\Users\dinda\Documents\Eksperimen_SML_DindaMaulidiyah\Membangun_model\mlartifacts\192493955283675034\4e687583e8a243a090210fee3dc55b1b\artifacts\model"

    print("============================================================")
    print("PROMETHEUS MODEL MONITORING SERVER")
    print("============================================================")
    print(f"Model path  : {model_uri}")
    print("============================================================")

    # Load model
    print("Loading model...")
    load_model(model_uri)

    # Start Prometheus metrics server di port 8000
    print("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)
    print("Prometheus metrics available at: http://127.0.0.1:8000/metrics")

    # Start background threads untuk update metrics
    threading.Thread(target=update_system_metrics, daemon=True).start()
    threading.Thread(target=update_throughput, daemon=True).start()

    # Start Flask app
    print("Starting Flask inference server on port 5001...")
    print("Inference endpoint available at: http://127.0.0.1:5001/predict")
    print("============================================================")
    app.run(host="0.0.0.0", port=5001)
