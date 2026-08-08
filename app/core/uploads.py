import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic"}
MAX_FILE_SIZE_MB = 8


async def save_upload_image(file: UploadFile, subfolder: str) -> str:
    """Rasmni /media/{subfolder}/ ostiga saqlaydi va public URL qaytaradi."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Faqat JPEG, PNG, WEBP yoki HEIC rasm yuklash mumkin")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Fayl hajmi {MAX_FILE_SIZE_MB}MB dan oshmasligi kerak")

    ext = Path(file.filename or "").suffix.lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"

    target_dir = Path(settings.MEDIA_ROOT) / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    target_path.write_bytes(contents)

    return f"{settings.MEDIA_URL}{subfolder}/{filename}"
