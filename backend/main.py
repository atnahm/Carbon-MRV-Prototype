from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from jose import JWTError, jwt

from models import SessionLocal, Farm, User  # type: ignore
from auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ml_model import ml_model

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Allow Vite dev server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Carbon MRV Prototype Backend Running 🚀"}

# -----------------------------
# Database dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Pydantic Schemas
# -----------------------------
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class FarmCreate(BaseModel):
    farmer_name: str = Field(..., min_length=1)
    farm_size: float = Field(..., ge=0)
    crop_type: str = Field(..., min_length=1)
    tree_count: int = Field(..., ge=0)

class VerifyCarbonData(BaseModel):
    farm_id: int
    actual_carbon_savings: float

# -----------------------------
# Auth Dependencies
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# -----------------------------
# Endpoints
# -----------------------------
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    # Always set role to farmer on registration for security.
    # Authorities/admins must be set directly in the database by administrators.
    new_user = User(username=user.username, hashed_password=hashed_password, role="farmer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload_data")
def upload_data(payload: FarmCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_farm = Farm(
        farmer_name=payload.farmer_name,
        farm_size=payload.farm_size,
        crop_type=payload.crop_type,
        tree_count=payload.tree_count,
    )
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)
    return {"status": "success", "id": new_farm.id}

@app.get("/farm_report")
def farm_report(farmer_name: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Farm)
    if farmer_name:
        query = query.filter(Farm.farmer_name == farmer_name)
    farm = query.order_by(Farm.timestamp.desc()).first()
    if not farm:
        raise HTTPException(status_code=404, detail="No farm data found")

    # Use the ML model to predict carbon savings
    carbon_savings = ml_model.predict(farm.farm_size, farm.tree_count)

    return {
        "id": farm.id,
        "farmer_name": farm.farmer_name,
        "farm_size": farm.farm_size,
        "crop_type": farm.crop_type,
        "tree_count": farm.tree_count,
        "carbon_savings": carbon_savings,
        "timestamp": farm.timestamp.isoformat(),
    }

@app.post("/verify_carbon")
def verify_carbon(data: VerifyCarbonData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["authority", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to verify carbon data")

    farm = db.query(Farm).filter(Farm.id == data.farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm data not found")

    # Online/Recursive ML learning: update the model with ground truth data
    ml_model.partial_fit(farm.farm_size, farm.tree_count, data.actual_carbon_savings)

    return {"status": "success", "message": "ML Model updated with new verified data"}
