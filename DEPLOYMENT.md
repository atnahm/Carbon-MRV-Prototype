# Deployment Guide

The Carbon MRV Platform is containerized with Docker, making it relatively straightforward to deploy to various cloud providers.

## Pre-requisites
Before deploying, ensure you have:
1. A domain name (optional, but recommended).
2. A secure string to use as the `SECRET_KEY` for JWT tokens.
3. Secure passwords for your PostgreSQL database.

## Deploying to a Virtual Private Server (VPS) via Docker Compose
This method works for providers like **DigitalOcean Droplets**, **AWS EC2**, or **Linode**.

1. SSH into your server.
2. Install Docker and Docker Compose.
3. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Carbon-MRV-Prototype.git
   cd Carbon-MRV-Prototype
   ```
4. Set up your environment variables. Create a `.env` file in the root directory:
   ```bash
   POSTGRES_USER=my_secure_user
   POSTGRES_PASSWORD=my_secure_db_password
   POSTGRES_DB=carbon_db
   SECRET_KEY=generate_a_long_random_secret_string_here
   ```
5. Build and run the containers:
   ```bash
   docker compose up -d --build
   ```
6. **Reverse Proxy:** It is highly recommended to set up **Nginx** or **Traefik** as a reverse proxy in front of the application to handle SSL/TLS certificates (e.g., via Let's Encrypt) and route traffic to ports `5173` (Frontend) and `8000` (Backend API).

## Deploying to Managed Services (e.g., Render, Railway, Heroku)

### Backend (FastAPI)
1. Create a new Web Service pointing to your repository.
2. Set the root directory to `backend`.
3. The platform will usually detect the `Dockerfile` in the `backend` directory.
4. Add the necessary Environment Variables (`DATABASE_URL`, `SECRET_KEY`).
5. Ensure the start command uses `uvicorn main:app --host 0.0.0.0 --port $PORT`.

### Database (PostgreSQL)
1. Provision a managed PostgreSQL instance on your provider.
2. Copy the connection string and supply it as the `DATABASE_URL` environment variable for your Backend Web Service.

### Frontend (React + Vite)
1. Create a new Static Site (or Web Service) pointing to your repository.
2. Set the root directory to `frontend`.
3. Set the build command to `npm install && npm run build`.
4. Set the publish directory to `dist`.
5. Add the `VITE_API_URL` environment variable pointing to your deployed Backend URL.

## Initializing the System
Once deployed, remember that the first user registration defaults to a `farmer` role. To create an `authority` or `admin` user capable of verifying carbon data and training the ML model, you will need to access the database directly and manually update the user's `role` field.
