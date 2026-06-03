import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Carbon MRV Prototype Backend Running 🚀"}

def test_register_and_login():
    # Register
    res_reg = client.post("/register", json={"username": "testuser2", "password": "password"})
    assert res_reg.status_code == 200
    assert "access_token" in res_reg.json()

    # Set user as admin in DB manually for tests
    db = TestingSessionLocal()
    from models import User
    user = db.query(User).filter(User.username == "testuser2").first()
    user.role = "admin"
    db.commit()
    db.close()

    # Login
    res_log = client.post("/login", data={"username": "testuser2", "password": "password"})
    assert res_log.status_code == 200
    token = res_log.json()["access_token"]

    # Upload Data
    headers = {"Authorization": f"Bearer {token}"}
    res_up = client.post("/upload_data", json={
        "farmer_name": "John Doe",
        "farm_size": 10.5,
        "crop_type": "Corn",
        "tree_count": 100
    }, headers=headers)
    assert res_up.status_code == 200
    assert res_up.json()["status"] == "success"

    # Get Report
    res_rep = client.get("/farm_report?farmer_name=John Doe", headers=headers)
    assert res_rep.status_code == 200
    assert "carbon_savings" in res_rep.json()
    farm_id = res_rep.json()["id"]

    # Verify Carbon (Train ML)
    res_ver = client.post("/verify_carbon", json={
        "farm_id": farm_id,
        "actual_carbon_savings": 55.0
    }, headers=headers)
    assert res_ver.status_code == 200
    assert res_ver.json()["status"] == "success"
