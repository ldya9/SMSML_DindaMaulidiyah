"""
Script untuk serve MLflow model secara langsung menggunakan path artifact
"""
import os
import sys
import subprocess
import argparse
import io

# Fix encoding untuk Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_model_artifact_path(run_id):
    """Mencari path artifact model dari run_id"""
    # Cek di berbagai lokasi yang mungkin
    possible_bases = [
        '.',
        '..',
        os.path.join('..', 'Membangun_model'),
        'Membangun_model',
        os.path.join('..', '..', 'Membangun_model'),
    ]
    
    for base in possible_bases:
        abs_base = os.path.abspath(base)
        
        # Cek mlruns
        mlruns_path = os.path.join(abs_base, 'mlruns')
        if os.path.exists(mlruns_path):
            # Cari di semua experiment
            for exp_dir in os.listdir(mlruns_path):
                exp_path = os.path.join(mlruns_path, exp_dir)
                if os.path.isdir(exp_path):
                    run_path = os.path.join(exp_path, run_id)
                    if os.path.exists(run_path):
                        model_path = os.path.join(run_path, 'artifacts', 'model')
                        if os.path.exists(model_path):
                            return os.path.abspath(model_path)
        
        # Cek mlartifacts
        mlartifacts_path = os.path.join(abs_base, 'mlartifacts')
        if os.path.exists(mlartifacts_path):
            # Cari di struktur mlartifacts/experiment_id/run_id/artifacts/model
            for exp_dir in os.listdir(mlartifacts_path):
                exp_path = os.path.join(mlartifacts_path, exp_dir)
                if os.path.isdir(exp_path):
                    run_path = os.path.join(exp_path, run_id)
                    if os.path.exists(run_path):
                        model_path = os.path.join(run_path, 'artifacts', 'model')
                        if os.path.exists(model_path):
                            return os.path.abspath(model_path)
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Serve MLflow model menggunakan path langsung')
    parser.add_argument('--run-id', type=str, help='MLflow run ID (opsional, akan cari otomatis jika tidak diberikan)')
    parser.add_argument('--port', type=int, default=5002, help='Port untuk serve model (default: 5002)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SERVE MLFLOW MODEL")
    print("=" * 60)
    print()
    
    # Cari run_id jika tidak diberikan
    if not args.run_id:
        print("Mencari run_id terbaru...")
        try:
            result = subprocess.run(
                [sys.executable, 'find_run_id.py'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            # Parse run_id dari output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'REKOMENDASI RUN ID' in line or 'Run ID:' in line:
                    # Extract run_id
                    parts = line.split()
                    for part in parts:
                        if len(part) == 32 and all(c in '0123456789abcdef' for c in part):
                            args.run_id = part
                            break
                    if args.run_id:
                        break
        except Exception as e:
            print(f"Error mencari run_id: {e}")
            print("Silakan berikan --run-id secara manual")
            return
    
    if not args.run_id:
        print("ERROR: Tidak dapat menemukan run_id!")
        print("Gunakan: python find_run_id.py untuk mencari run_id terlebih dahulu")
        return
    
    print(f"Run ID: {args.run_id}")
    print(f"Port: {args.port}")
    print()
    
    # Cari path model artifact
    print("Mencari path model artifact...")
    model_path = find_model_artifact_path(args.run_id)
    
    if not model_path:
        print(f"ERROR: Model artifact tidak ditemukan untuk run_id: {args.run_id}")
        print()
        print("Coba:")
        print("1. Jalankan: python find_run_id.py untuk melihat run_id yang tersedia")
        print("2. Pastikan model sudah di-train dengan benar")
        return
    
    print(f"Model ditemukan di: {model_path}")
    print()
    
    # Serve model menggunakan mlflow models serve
    print("=" * 60)
    print(f"Memulai serve model di port {args.port}...")
    print("=" * 60)
    print()
    print("Endpoint akan tersedia di:")
    print(f"  - Health: http://127.0.0.1:{args.port}/health")
    print(f"  - Predict: http://127.0.0.1:{args.port}/invocations")
    print()
    print("Tekan Ctrl+C untuk menghentikan server")
    print()
    
    # Jalankan mlflow models serve
    try:
        cmd = [
            sys.executable, '-m', 'mlflow', 'models', 'serve',
            '--model-uri', model_path,
            '--port', str(args.port),
            '--host', '127.0.0.1'
        ]
        
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\nServer dihentikan oleh user")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Gagal serve model: {e}")
        print("\nPastikan:")
        print("1. MLflow sudah terinstall: pip install mlflow")
        print("2. Model artifact valid")
        print("3. Port tidak digunakan aplikasi lain")

if __name__ == '__main__':
    main()

