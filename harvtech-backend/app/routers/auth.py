from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import UserLogin, UserLoginResponse, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_fin_id(phone_number: str) -> str:
    return f"HT{phone_number}"


@router.post("/register", response_model=dict)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    existing_phone = db.query(User).filter(User.phone_number == payload.phone_number).first()

    if existing_phone:
        if verify_password(str(payload.password), existing_phone.hashed_password):
            access_token = create_access_token({"sub": existing_phone.fin_id})
            return {
                "message": "User already registered. Logged in successfully",
                "fin_id": existing_phone.fin_id,
                "name": existing_phone.name,
                "access_token": access_token,
                "token_type": "bearer",
            }

        raise HTTPException(status_code=409, detail="User with this phone number already exists")

    fin_id = _build_fin_id(payload.phone_number)

    user = User(
        name=payload.name,
        phone_number=payload.phone_number,
        location=payload.location,
        acres_of_land=payload.land_area,
        fin_id=fin_id,
        hashed_password=get_password_hash(str(payload.password)),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "fin_id": user.fin_id,
        "name": user.name,
    }


@router.post("/login", response_model=UserLoginResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.fin_id == payload.fin_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(str(payload.password), user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token({"sub": user.fin_id})
    return {
        "success": True,
        "message": "Login successful",
        "fin_id": user.fin_id,
        "name": user.name,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/user/{fin_id}", response_model=dict)
def get_user_by_fin_id(fin_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.fin_id == fin_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "place": user.place,
        "aadhar_number": user.aadhar_number,
        "phone_number": user.phone_number,
        "location": user.location,
        "acres_of_land": user.acres_of_land,
        "fin_id": user.fin_id,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.get("/users", response_model=list[dict])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "place": user.place,
            "aadhar_number": user.aadhar_number,
            "phone_number": user.phone_number,
            "location": user.location,
            "acres_of_land": user.acres_of_land,
            "fin_id": user.fin_id,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        for user in users
    ]
