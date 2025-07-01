from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from ..models import User, File as FileModel
from ..schemas import UserCreate, UserLogin, FileOut, DownloadLinkResponse
from ..auth import get_db, hash_password, verify_password, create_access_token, decode_token, require_role
from ..email_utils import send_verification_email
from ..config import JWT_SECRET, JWT_ALGORITHM
import jwt
from datetime import timedelta

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email exists")
    hashed = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed, role="client", is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Generate verification token
    token = create_access_token({"email": new_user.email, "role": "client", "user_id": new_user.id}, expires_delta=timedelta(hours=24))
    link = f"{request.url_for('email_verify')}?token={token}"
    send_verification_email(new_user.email, link)
    return {"verification_link": link}

@router.get("/email-verify")
def email_verify(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.email == payload["email"]).first()
        if user and not user.is_verified:
            user.is_verified = True
            db.commit()
            return {"message": "Email verified"}
        raise HTTPException(status_code=400, detail="Already verified or user not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

@router.post("/login")
def client_login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.role == "client").first()
    if not user or not user.is_verified or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials or not verified")
    token = create_access_token({"email": user.email, "role": user.role, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/files", response_model=list[FileOut])
def list_files(db: Session = Depends(get_db), user=Depends(require_role("client"))):
    return db.query(FileModel).all()

@router.post("/download-link/{file_id}", response_model=DownloadLinkResponse)
def get_download_link(file_id: int, user=Depends(require_role("client"))):
    download_token = create_access_token(
        {"file_id": file_id, "user_id": user.id, "role": "client"}, expires_delta=timedelta(minutes=15)
    )
    return DownloadLinkResponse(
        download_link=f"/client/download/{download_token}"
    )

@router.get("/download/{token}")
def download_file(token: str, db: Session = Depends(get_db), current_user=Depends(require_role("client"))):
    try:
        payload = decode_token(token)
        # Only allow if token user_id matches current user and role
        if payload["user_id"] != current_user.id or payload["role"] != "client":
            raise HTTPException(status_code=403, detail="Forbidden")
        file = db.query(FileModel).filter(FileModel.id == payload["file_id"]).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file.stored_path, filename=file.filename)
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid or expired token")