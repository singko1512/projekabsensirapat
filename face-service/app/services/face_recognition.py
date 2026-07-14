import json
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError


BASE_DIR = Path(__file__).resolve().parents[2]
EMBEDDINGS_FILE = BASE_DIR / "embeddings" / "users.json"


def enroll_face(user_id: str, image_bytes: bytes) -> dict:
    user_id = user_id.strip()
    if not user_id:
        return {
            "enrolled": False,
            "user_id": None,
            "message": "User ID wajib diisi.",
        }

    try:
        embedding = make_embedding(image_bytes)
    except ValueError as exc:
        return {
            "enrolled": False,
            "user_id": user_id,
            "message": str(exc),
        }

    users = load_users()
    users[user_id] = {
        "user_id": user_id,
        "embedding": embedding.tolist(),
    }
    save_users(users)

    return {
        "enrolled": True,
        "user_id": user_id,
        "message": "Wajah berhasil disimpan.",
    }


def recognize_face(image_bytes: bytes, threshold: float = 0.35) -> dict:
    users = load_users()
    if not users:
        return {
            "matched": False,
            "user_id": None,
            "distance": None,
            "message": "Belum ada data wajah. Enroll dulu minimal satu user.",
            "image_size_bytes": len(image_bytes),
        }

    try:
        embedding = make_embedding(image_bytes)
    except ValueError as exc:
        return {
            "matched": False,
            "user_id": None,
            "distance": None,
            "message": str(exc),
            "image_size_bytes": len(image_bytes),
        }

    best_user_id = None
    best_distance = float("inf")

    for user_id, user_data in users.items():
        stored_embedding = np.array(user_data.get("embedding", []), dtype=np.float32)
        if stored_embedding.shape != embedding.shape:
            continue

        distance = float(np.linalg.norm(embedding - stored_embedding))
        if distance < best_distance:
            best_distance = distance
            best_user_id = user_id

    matched = best_user_id is not None and best_distance <= threshold

    return {
        "matched": matched,
        "user_id": best_user_id if matched else None,
        "distance": best_distance if best_user_id is not None else None,
        "threshold": threshold,
        "message": "Wajah cocok." if matched else "Wajah belum cocok dengan data enroll.",
        "image_size_bytes": len(image_bytes),
    }


def make_embedding(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("File gambar tidak valid.") from exc

    image = image.resize((64, 64))
    pixels = np.asarray(image, dtype=np.float32) / 255.0

    channel_means = pixels.mean(axis=(0, 1))
    channel_stds = pixels.std(axis=(0, 1))
    histograms = [
        np.histogram(pixels[:, :, channel], bins=16, range=(0.0, 1.0), density=True)[0]
        for channel in range(3)
    ]

    embedding = np.concatenate([channel_means, channel_stds, *histograms]).astype(np.float32)
    norm = float(np.linalg.norm(embedding))
    if norm == 0:
        raise ValueError("Gambar terlalu gelap atau kosong.")

    return embedding / norm


def load_users() -> dict:
    if not EMBEDDINGS_FILE.exists():
        return {}

    try:
        return json.loads(EMBEDDINGS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_users(users: dict) -> None:
    EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_FILE.write_text(
        json.dumps(users, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
