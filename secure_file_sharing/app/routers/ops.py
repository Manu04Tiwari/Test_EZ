from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from ..auth import require_role
from ..database import db
from ..file_utils import save_file
from datetime import datetime

router = APIRouter(prefix="/ops", tags=["Ops"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user = Depends(require_role("ops"))
):
    file_path = await save_file(file)
    file_doc = {
        "filename": file.filename,
        "stored_path": file_path,
        "uploaded_by": user["id"],
        "uploaded_at": datetime.utcnow()
    }
    result = await db["files"].insert_one(file_doc)
    file_doc["id"] = str(result.inserted_id)
    return {"file_id": file_doc["id"], "filename": file_doc["filename"]}