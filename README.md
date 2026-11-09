☕ Café Report — Containerized Data Pipeline

An enterprise-grade containerization project for a Python data processing script integrated with PostgreSQL, built following modern Docker production standards, multi-stage builds, and multi-architecture packaging.

🛠️ Tech Stack & Architecture

Runtime: Python 3.12 (Slim & Multi-stage)

Database: PostgreSQL 18 (Alpine)

Orchestration: Docker Compose (Internal DNS routing, Health checks, Named Volumes)

Security: Non-root execution (UID 10001), read-only root files, strict .dockerignore isolation

Registry: Docker Hub multi-platform builds (linux/amd64, linux/arm64)

[ PostgreSQL Service (db) ] <--- Internal Network ---> [ Report Service (python) ]
             |                                                    |
    (Named Vol: pgdata)                                 (Bind Mount: ./output)


🚀 Quickstart

1. Environment Setup

cp .env.example .env
# Update the POSTGRES_PASSWORD value inside the .env file


2. Run the Application

docker compose up -d


3. Verify Database Records

docker compose exec db psql -U cafe -d cafe -c "SELECT * FROM revenue_by_drink;"


4. Cleanup

docker compose down -v
