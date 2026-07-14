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
python run.py
```

Atau dari root project:

```bash
python face-service/run.py
```

Di Windows juga bisa jalankan:

```bash
face-service\start.bat
```

Tes health check:

```text
GET http://127.0.0.1:8001/health
```

Buka halaman kamera test:

```text
http://127.0.0.1:8001/camera
```

Root service Python hanya untuk info API:

```text
GET http://127.0.0.1:8001/
```

Halaman utama aplikasi tetap dari Laravel, bukan dari service Python.

## Endpoint Awal

```text
GET /health
GET /
GET /camera
POST /enroll
POST /recognize
```

Endpoint `/enroll` menyimpan embedding lokal ke `embeddings/users.json`.
Endpoint `/recognize` membandingkan gambar dari kamera dengan data enroll lokal.

## Catatan

Jangan commit:

- `venv/`
- `.env`
- file model besar
- file embedding hasil generate
- cache Python
