from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..auth import require_role, get_db
from ..models import File as FileModel
from ..file_utils import save_file

router = APIRouter(prefix="/ops", tags=["Ops"])

@router.post("/login")
def ops_login():
    # Implement standard login (reuse from main or auth)
    pass

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(require_role("ops"))
):
    file_path = await save_file(file)
    db_file = FileModel(
        filename=file.filename, stored_path=file_path, uploaded_by=user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"file_id": db_file.id, "filename": db_file.filename}