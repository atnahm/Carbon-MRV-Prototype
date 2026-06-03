# Carbon MRV Platform Architecture

## Overview
The Carbon Measurement, Reporting, and Verification (MRV) platform is a robust, production-grade AI-powered web application. It transitions the initial prototype into a full-scale ecosystem capable of handling individual user data and institutional authority ground-truth inputs for recursive machine learning (ML) refinement.

## System Components

### 1. Frontend (React + Vite)
- **UI Framework:** React with Vite build tool. Material UI is used for clean, responsive components.
- **Authentication:** JWT-based user authentication. Users can register/login with different roles (`farmer`, `authority`, `admin`).
- **Functionality:**
  - Farmers upload their farm data (size, tree count, crop type).
  - Farmers view predicted carbon savings based on the integrated AI model.
  - Authorities/Admins have special UI access to submit measured ground-truth data to continuously train the ML model.

### 2. Backend (FastAPI)
- **API Framework:** FastAPI for high-performance, asynchronous REST APIs.
- **Authentication:** OAuth2 with Password Flow (JWT tokens). Role-based access control (RBAC) secures endpoints.
- **ML Integration:** An integrated `scikit-learn` `SGDRegressor` provides continuous/online learning (`partial_fit`).
- **Database ORM:** SQLAlchemy is used to interact with the database.

### 3. Database (PostgreSQL)
- The application uses PostgreSQL for robust, transactional data storage, replacing the initial SQLite implementation.
- A `users` table handles authentication, and a `farms` table handles farm metadata.

### 4. Machine Learning Module
- **Model:** Stochastic Gradient Descent Regressor (`SGDRegressor`) combined with a `StandardScaler`.
- **Predictive Mode:** Predicts carbon savings based on `farm_size` and `tree_count`.
- **Recursive/Online Learning:** Authorities can hit the `/verify_carbon` endpoint with actual measured data. The ML module uses `partial_fit` to incrementally update its weights, effectively creating a self-improving ecosystem without needing full model retraining.

### 5. Deployment & CI/CD
- **Docker & Docker Compose:** The entire stack (Frontend, Backend, PostgreSQL) is containerized and orchestrated via Docker Compose for consistent local development and production deployment.
- **GitHub Actions (CI):** Automated pipelines run on every push/PR to `main` to run backend `pytest` unit tests, frontend `eslint` linting, and Docker builds.
