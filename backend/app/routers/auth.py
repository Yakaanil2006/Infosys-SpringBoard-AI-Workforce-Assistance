from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_current_user, require_admin, hash_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserOut, CreateAdmin

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/admins", response_model=UserOut)
def create_admin(
    payload: CreateAdmin,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/admins", response_model=list[UserOut])
def admins(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.execute(
        select(User)
        .where(
            User.role == "admin",
            User.is_active.is_(True),
        )
        .order_by(User.created_at.desc())
    ).scalars().all()


@router.delete("/admins/{user_id}")
def delete_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current: User = Depends(require_admin),
):
    if current.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account",
        )

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Admin not found",
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=400,
            detail="Only administrator accounts can be removed",
        )

    user.is_active = False

    db.commit()
    db.refresh(user)

    return {
        "message": "Admin deactivated",
        "id": user.id,
    }
