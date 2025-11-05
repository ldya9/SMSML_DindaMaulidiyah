# Bukti Serving Model

Folder ini berisi screenshot bukti bahwa model sudah di-serve.

## Screenshot yang Diperlukan:

1. **serving_model.png** atau **serving_model.jpg** - Screenshot terminal saat menjalankan `mlflow models serve`

## Cara Mengambil Screenshot:

### Option 1: Menggunakan serve_model.py
```bash
python serve_model.py
```
Screenshot terminal yang menunjukkan:
- Model URI
- Port serving
- Status "Serving on http://127.0.0.1:5002"

### Option 2: Menggunakan MLflow CLI langsung
```bash
mlflow models serve -m "runs:/<run_id>/model" --port 5002 --no-conda
```
Screenshot terminal yang menunjukkan:
- Command yang dijalankan
- Status "Serving on http://127.0.0.1:5002"

## Contoh Output yang Harus Terlihat:

```
INFO mlflow.models.flavor_backend_registry: Selected backend for flavor 'python_function'
INFO mlflow.pyfunc.backend: === Running command 'waitress-serve --host=127.0.0.1 --port=5002 --ident=mlflow mlflow.pyfunc.scoring_server.wsgi:app'
INFO: waitress: Serving on http://127.0.0.1:5002
```

