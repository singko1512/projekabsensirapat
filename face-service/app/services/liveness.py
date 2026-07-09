def check_liveness(image_bytes: bytes) -> dict:
    """Placeholder untuk MediaPipe liveness detection."""
    return {
        "is_live": True,
        "score": None,
        "message": "MediaPipe liveness belum diimplementasikan.",
        "image_size_bytes": len(image_bytes),
    }

