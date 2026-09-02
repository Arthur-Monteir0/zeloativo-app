from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from app.database import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(payload: RegisterIn):
    try:
        res = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: LoginIn):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })

        # res.session.access_token / res.user.id
        session = res.session
        user = res.user

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user_id": user.id,
            "email": user.email,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))