# Carbon MRV Platform

## Overview
The Carbon Measurement, Reporting, and Verification (MRV) platform is a production-grade, AI-driven ecosystem. It enables farmers to log their farm data and receive AI-predicted carbon savings. Regulatory authorities can supply verified ground-truth data to continuously train the integrated predictive machine learning model.

## Features
- **Production Architecture:** Containerized using Docker & Docker Compose with a PostgreSQL database.
- **Recursive Machine Learning:** Real-time AI model self-training (`partial_fit`) using authority-verified carbon data.
- **Role-Based Authentication:** JWT token authentication for Farmers, Authorities, and Admins.
- **CI/CD Pipelines:** Automated testing, linting, and build verification via GitHub Actions.

## Setup & Deployment (Docker)
The easiest way to run the entire ecosystem is using Docker Compose.

```bash
# 1. Build and start the containers in detached mode
docker-compose up -d --build

# 2. View logs
docker-compose logs -f
```

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs

## Local Development (Without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture details
Please refer to [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed information on the system components, ML integration, and data flow.
