"""
Script untuk mencari Run ID dari MLflow model yang sudah di-train
"""
import os
import sys
import io

# Fix encoding untuk Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_mlruns_directories(base_path='.'):
    """Mencari semua folder mlruns dan mlartifacts"""
    mlruns_paths = []
    mlartifacts_paths = []
    
    # Cek di berbagai lokasi yang mungkin
    possible_paths = [
        base_path,
        os.path.join(base_path, '..'),
        os.path.join(base_path, '..', 'Membangun_model'),
        os.path.join(base_path, 'Membangun_model'),
        os.path.join(base_path, '..', '..', 'Membangun_model'),
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        mlruns_path = os.path.join(abs_path, 'mlruns')
        mlartifacts_path = os.path.join(abs_path, 'mlartifacts')
        if os.path.exists(mlruns_path):
            mlruns_paths.append(mlruns_path)
        if os.path.exists(mlartifacts_path):
            mlartifacts_paths.append(mlartifacts_path)
    
    return mlruns_paths, mlartifacts_paths

def get_run_ids(mlruns_path, mlartifacts_path=None):
    """Mendapatkan semua run ID dari mlruns folder dan cek model di mlartifacts"""
    run_ids = []
    
    # Cari di struktur mlruns/experiment_id/run_id/
    try:
        experiment_dirs = [d for d in os.listdir(mlruns_path) if os.path.isdir(os.path.join(mlruns_path, d))]
        
        for exp_dir in experiment_dirs:
            exp_path = os.path.join(mlruns_path, exp_dir)
            if os.path.isdir(exp_path):
                # Cek apakah ini experiment directory atau run directory
                run_dirs = [d for d in os.listdir(exp_path) if os.path.isdir(os.path.join(exp_path, d))]
                
                for run_dir in run_dirs:
                    run_path = os.path.join(exp_path, run_dir)
                    # Run ID biasanya berupa UUID (32 karakter hex)
                    if len(run_dir) == 32 and all(c in '0123456789abcdef' for c in run_dir):
                        # Cek model di mlartifacts jika ada
                        model_path = None
                        if mlartifacts_path:
                            mlartifacts_exp_path = os.path.join(mlartifacts_path, exp_dir)
                            if os.path.exists(mlartifacts_exp_path):
                                mlartifacts_run_path = os.path.join(mlartifacts_exp_path, run_dir, 'artifacts', 'model')
                                if os.path.exists(mlartifacts_run_path):
                                    model_path = mlartifacts_run_path
                        
                        # Juga cek di mlruns/experiment_id/run_id/artifacts/model
                        if not model_path:
                            mlruns_model_path = os.path.join(run_path, 'artifacts', 'model')
                            if os.path.exists(mlruns_model_path):
                                model_path = mlruns_model_path
                        
                        run_ids.append((run_dir, run_path, model_path))
    except Exception as e:
        print(f"Error membaca {mlruns_path}: {e}")
    
    return run_ids

def main():
    print("=" * 60)
    print("MENCARI MLFLOW RUN ID")
    print("=" * 60)
    print()
    
    # Cari mlruns dan mlartifacts directories
    mlruns_paths, mlartifacts_paths = find_mlruns_directories()
    
    if not mlruns_paths:
        print("ERROR: Tidak ditemukan folder mlruns!")
        print()
        print("Pastikan Anda sudah menjalankan modelling.py atau modelling_tuning.py")
        print("dan folder mlruns ada di:")
        print("  - Membangun_model/mlruns/")
        print("  - atau di folder parent")
        return
    
    print(f"Ditemukan {len(mlruns_paths)} folder mlruns:")
    for path in mlruns_paths:
        print(f"   - {path}")
    if mlartifacts_paths:
        print(f"Ditemukan {len(mlartifacts_paths)} folder mlartifacts:")
        for path in mlartifacts_paths:
            print(f"   - {path}")
    print()
    
    # Kumpulkan semua run ID
    all_runs = []
    for mlruns_path in mlruns_paths:
        # Cari mlartifacts yang sesuai (dengan path yang sama)
        mlartifacts_path = None
        for ma_path in mlartifacts_paths:
            # Cek apakah mlartifacts di folder yang sama dengan mlruns
            if os.path.dirname(mlruns_path) == os.path.dirname(ma_path):
                mlartifacts_path = ma_path
                break
        
        runs = get_run_ids(mlruns_path, mlartifacts_path)
        all_runs.extend(runs)
    
    if not all_runs:
        print("ERROR: Tidak ditemukan run ID di folder mlruns!")
        print()
        print("Pastikan model sudah di-train dengan benar.")
        return
    
    print(f"Ditemukan {len(all_runs)} run(s):")
    print()
    print("-" * 60)
    
    # Tampilkan run ID, urutkan berdasarkan waktu modifikasi (terbaru dulu)
    all_runs.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)
    
    for idx, run_info in enumerate(all_runs, 1):
        if len(run_info) == 3:
            run_id, run_path, model_path = run_info
        else:
            run_id, run_path = run_info
            model_path = None
        
        has_model = "HAS MODEL" if model_path and os.path.exists(model_path) else "NO MODEL"
        
        print(f"{idx}. Run ID: {run_id} ({has_model})")
        print(f"   Path: {run_path}")
        if model_path:
            print(f"   Model: {model_path}")
        print()
    
    print("-" * 60)
    print()
    
    # Rekomendasi run ID terbaru yang punya model
    recommended = None
    for run_info in all_runs:
        if len(run_info) == 3:
            run_id, run_path, model_path = run_info
        else:
            run_id, run_path = run_info
            model_path = None
        
        if model_path and os.path.exists(model_path):
            recommended = run_id
            break
    
    if recommended:
        print("REKOMENDASI RUN ID (terbaru dengan model):")
        print(f"   {recommended}")
        print()
        print("Copy run_id ini untuk digunakan di serve_model.py atau serve_model_direct.py")
        print()
        print("Contoh penggunaan:")
        print(f'   python serve_model_direct.py --run-id {recommended}')
    else:
        print("PERINGATAN: Tidak ada run yang memiliki model artifact!")
        print("   Pastikan model sudah di-save dengan benar saat training.")

if __name__ == '__main__':
    main()

