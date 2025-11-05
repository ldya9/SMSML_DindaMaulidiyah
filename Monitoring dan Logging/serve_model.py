"""
Script untuk Serving Model menggunakan MLflow
Script ini akan serve model yang sudah di-train menggunakan MLflow
"""

import os
import sys
import mlflow
import mlflow.pyfunc
import subprocess

def find_latest_model():
    """Find latest model dari MLflow runs"""
    # Set tracking URI
    mlflow.set_tracking_uri("http://127.0.0.1:5000/")
    
    # Get experiment
    experiment_name = "Wine Quality Classification - Dinda Maulidiyah"
    experiment = mlflow.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        print(f"❌ Experiment '{experiment_name}' not found")
        return None
    
    # Search for latest run
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1
    )
    
    if runs.empty:
        print("❌ No runs found in experiment")
        return None
    
    latest_run = runs.iloc[0]
    run_id = latest_run['run_id']
    model_uri = f"runs:/{run_id}/model"
    
    print(f"✅ Found latest model: {model_uri}")
    return model_uri

def serve_model_mlflow(model_uri, port=5002):
    """
    Serve model menggunakan MLflow models serve
    
    Args:
        model_uri: URI model (runs:/run_id/model atau models:/name/version)
        port: Port untuk serving (default: 5002)
    """
    print("="*60)
    print("MLflow Model Serving")
    print("="*60)
    print(f"Model URI: {model_uri}")
    print(f"Port: {port}")
    print("="*60)
    
    # Command untuk serve model
    cmd = [
        "mlflow", "models", "serve",
        "-m", model_uri,
        "--port", str(port),
        "--no-conda",  # Gunakan environment saat ini
        "--host", "127.0.0.1"
    ]
    
    print(f"\n🚀 Starting model server...")
    print(f"   Command: {' '.join(cmd)}")
    print(f"\n   Model will be available at: http://127.0.0.1:{port}/invocations")
    print(f"   Health check: http://127.0.0.1:{port}/health")
    print(f"\n   Press Ctrl+C to stop\n")
    
    try:
        # Run command
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n⚠️  Model server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error serving model: {e}")
        sys.exit(1)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Serve MLflow model')
    parser.add_argument(
        '--model-uri',
        type=str,
        default=None,
        help='Model URI (runs:/run_id/model atau models:/name/version). Jika tidak diisi, akan mencari latest model.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5002,
        help='Port untuk serving (default: 5002)'
    )
    
    args = parser.parse_args()
    
    # Get model URI
    if args.model_uri:
        model_uri = args.model_uri
    else:
        print("🔍 Searching for latest model...")
        model_uri = find_latest_model()
        if model_uri is None:
            print("\n❌ Cannot find model. Please specify --model-uri")
            print("   Example: python serve_model.py --model-uri runs:/<run_id>/model")
            sys.exit(1)
    
    # Serve model
    serve_model_mlflow(model_uri, args.port)

if __name__ == "__main__":
    main()

