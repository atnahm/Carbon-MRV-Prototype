# Carbon MRV Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/atnahm/Carbon-MRV-Prototype/actions/workflows/ci.yml/badge.svg)](https://github.com/atnahm/Carbon-MRV-Prototype/actions/workflows/ci.yml)

**[Live Deployment: https://carbon-mrv-platform.example.com](https://carbon-mrv-platform.example.com)** *(Note: Replace with actual URL after deployment)*

## Overview
The Carbon Measurement, Reporting, and Verification (MRV) platform is a production-grade, open-source AI-driven ecosystem. It enables farmers to log their farm data and receive AI-predicted carbon savings. Regulatory authorities can supply verified ground-truth data to continuously train the integrated predictive machine learning model.

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

## Architecture & Deployment
- **Architecture Details:** Please refer to [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed information on the system components, ML integration, and data flow.
- **Deployment Guide:** Please refer to [DEPLOYMENT.md](./DEPLOYMENT.md) for instructions on how to deploy this platform to the cloud.

## Contributing
We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest enhancements to the ML models.
