from fastapi import APIRouter,Depends
from backend.app.core.exceptions import AppException
import re
from backend.app.core.database import get_db
from backend.app.schemas.user import UserCreate,LoginRequest,Token,UserRead
from sqlalchemy.orm import Session
from backend.app.services.user_service import Create_user,get_user_by_email
from backend.app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

def validate_password(password):
    if len(password) < 8:
        raise AppException("Le mot de passe doit contenir au moins 8 caractères")
    if not re.search(r"[A-Z]", password):
        raise AppException("Le mot de passe doit contenir une majuscule")
    if not re.search(r"[a-z]", password):
        raise AppException("Le mot de passe doit contenir une minuscule")
    if not re.search(r"[0-9]", password):
        raise AppException("Le mot de passe doit contenir un chiffre")
    
    
@router.post("/register")
def register(request: LoginRequest, db: Session=Depends(get_db)):
    token = authenticate_user(db,request.email,request.password)
    if token:
        raise AppException("Utilisateur déjà existant")
    validate_password(request.password)
    Create_user(db,request)
    token = authenticate_user(db,request.email,request.password)
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session=Depends(get_db)):
    token = authenticate_user(db, request.email, request.password)
    if not token:
        raise AppException("Email ou mot de passe incorrect")
    return {"access_token": token}

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: UserRead = Depends(get_user_by_email)):
    return current_user