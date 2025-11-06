"""
Inference Script untuk Testing Model Serving
Script ini melakukan inference ke model yang sedang di-serve
untuk generate metrics di Prometheus
"""

import requests
import time
import random
import json
import pandas as pd
import numpy as np

# URL endpoint untuk inference
INFERENCE_URL = "http://127.0.0.1:5001/predict"
HEALTH_URL = "http://127.0.0.1:5001/health"

def generate_sample_features():
    """
    Generate sample features untuk wine quality prediction
    Berdasarkan dataset wine quality, features adalah:
    - fixed acidity
    - volatile acidity
    - citric acid
    - residual sugar
    - chlorides
    - free sulfur dioxide
    - total sulfur dioxide
    - density
    - pH
    - sulphates
    - alcohol
    """
    return {
        'features': [
            random.uniform(4.0, 16.0),      # fixed acidity
            random.uniform(0.1, 1.6),      # volatile acidity
            random.uniform(0.0, 1.0),       # citric acid
            random.uniform(0.5, 15.0),      # residual sugar
            random.uniform(0.01, 0.6),      # chlorides
            random.uniform(1.0, 72.0),      # free sulfur dioxide
            random.uniform(6.0, 289.0),     # total sulfur dioxide
            random.uniform(0.99, 1.0),      # density
            random.uniform(2.7, 4.0),        # pH
            random.uniform(0.2, 2.0),       # sulphates
            random.uniform(8.0, 15.0)       # alcohol
        ]
    }

def check_health():
    """Check health endpoint"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print("Model server is healthy")
            return True
        else:
            print(f"Model server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Cannot connect to model server: {e}")
        print("   Make sure prometheus_exporter.py is running!")
        return False

def send_inference_request(features):
    """Send inference request ke model server"""
    try:
        start_time = time.time()
        response = requests.post(
            INFERENCE_URL,
            json=features,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        latency = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result.get('prediction', 'N/A')}, Latency: {latency:.3f}s")
            return True, latency
        else:
            print(f"Request failed: {response.status_code} - {response.text}")
            return False, latency
    except Exception as e:
        print(f"Request error: {e}")
        return False, 0

def main():
    """Main function untuk running inference"""
    print("="*60)
    print("ML Model Inference Testing")
    print("="*60)
    print(f"Inference URL: {INFERENCE_URL}")
    print(f"Health URL: {HEALTH_URL}")
    print("="*60)
    
    # Check health first
    if not check_health():
        print("\nPlease start prometheus_exporter.py first!")
        print("   Command: python prometheus_exporter.py")
        return
    
    print("\nStarting inference requests...")
    print("   Press Ctrl+C to stop\n")
    
    request_count = 0
    success_count = 0
    
    try:
        while True:
            # Generate sample features
            features = generate_sample_features()
            
            # Send inference request
            success, latency = send_inference_request(features)
            
            if success:
                success_count += 1
            request_count += 1
            
            # Print summary setiap 10 requests
            if request_count % 10 == 0:
                success_rate = (success_count / request_count) * 100
                print(f"\nSummary: {request_count} requests, {success_count} successful ({success_rate:.1f}%)")
                print("   Check Prometheus at http://127.0.0.1:9090 to see metrics\n")
            
            # Wait sebelum request berikutnya
            time.sleep(2)  # 2 detik antara requests
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Inference testing stopped")
        print("="*60)
        print(f"Total requests: {request_count}")
        print(f"Successful: {success_count}")
        print(f"Success rate: {(success_count/request_count*100) if request_count > 0 else 0:.1f}%")
        print("="*60)

if __name__ == "__main__":
    main()

