# Face Service

Service Python terpisah untuk face recognition dan liveness detection.

Rencana stack:

- FastAPI untuk HTTP API
- MediaPipe untuk deteksi wajah dan liveness
- FaceNet untuk embedding dan verifikasi wajah

## Setup Lokal

Masuk ke folder service:

```bash
cd face-service
```

Buat virtual environment:

```bash
py -3.11 -m venv venv
```

Aktifkan virtual environment di PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Install dependency:

```bash
pip install -r requirements.txt
```

Di mesin ini, venv sudah dibuat memakai Python 3.11.9.

Jalankan API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Tes health check:

```text
GET http://127.0.0.1:8001/health
```

## Endpoint Awal

```text
GET /health
POST /recognize
```

Endpoint `/recognize` saat ini masih placeholder. Nanti endpoint ini akan menerima gambar dari Laravel, menjalankan liveness check, membuat embedding wajah, lalu mengembalikan hasil verifikasi.

## Catatan

Jangan commit:

- `venv/`
- `.env`
- file model besar
- file embedding hasil generate
- cache Python
