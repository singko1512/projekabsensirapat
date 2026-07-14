from io import BytesIO

from PIL import Image, UnidentifiedImageError


def check_liveness(image_bytes: bytes) -> dict:
    if not image_bytes:
        return {
            "is_live": False,
            "score": 0,
            "message": "Gambar kosong.",
            "image_size_bytes": 0,
        }

    try:
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size
    except UnidentifiedImageError:
        return {
            "is_live": False,
            "score": 0,
            "message": "File bukan gambar yang valid.",
            "image_size_bytes": len(image_bytes),
        }

    is_large_enough = width >= 120 and height >= 120

    return {
        "is_live": is_large_enough,
        "score": 1 if is_large_enough else 0,
        "message": "Gambar valid." if is_large_enough else "Resolusi gambar terlalu kecil.",
        "image_size_bytes": len(image_bytes),
        "width": width,
        "height": height,
    }
