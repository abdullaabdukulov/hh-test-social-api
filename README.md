[comment]: <> (<p align="center">)
[comment]: <> (  <img src="https://i.imgur.com/uoyXjst.png" />)
[comment]: <> (</p>)

# PROJECT: Social API (Django REST) — Test Task

![python](https://img.shields.io/badge/-python-grey?style=for-the-badge&logo=python&logoColor=white&labelColor=306998)
![django](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![postgresql](https://img.shields.io/badge/postgre-SQL-%23000.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-grey?style=for-the-badge&logo=celery&logoColor=white&labelColor=37814A)
![Docker](https://img.shields.io/badge/docker-grey?style=for-the-badge&logo=docker&logoColor=white&labelColor=2496ED)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

A minimal social network backend API built as a test task:
- JWT authentication (register/login)
- Email verification (token with expiration, SMTP is optional; dev uses console backend)
- Posts, comments, likes
- Feed endpoint
- Cleanup of unverified users via Celery periodic task
- Swagger / Redoc documentation
- Docker-based environments (dev/test/prod)
- Pytest minimal coverage per app

---

## Outline
- [Prerequisites](#prerequisites)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
  - [Development](#development)
  - [Running Celery (worker/beat)](#running-celery-workerbeat)
  - [Test Environment](#test-environment)
- [API Endpoints (v1)](#api-endpoints-v1)
- [Project Structure](#project-structure)
- [Linting & Formatting](#linting--formatting)
- [Tests](#tests)
- [Notes](#notes)

---

## Prerequisites
- Python **3.11**
- Docker + Docker Compose plugin
- PostgreSQL 15 (via Docker)
- Redis (via Docker)

---

## Tech Stack
- **Django** + **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Celery** (worker + beat)
- **drf-yasg** (Swagger)
- **django-filter** (filters)
- **pytest + pytest-django + freezegun**

---

## Setup

### Development

#### 1) Clone and generate env/docker files
```bash
git clone https://github.com/abdullaabdukulov/hh-test-social-api.git
cd hh-test-social-api

chmod +x start.sh
./start.sh dev
```

This will copy development files into the project root:
- `docker-compose.yml`
- `.env` (from env_example)
- `db_configs/` for Postgres extensions
- `entrypoint.sh`

#### 2) Fill `.env`
Open `.env` and set values. For **local Django + dockerized DB/Redis** (your current workflow) use:
- `DB_HOST=127.0.0.1` (or `localhost`)
- `DB_PORT=4432` (your docker-compose port mapping)
- `REDIS_HOST=127.0.0.1`
- `REDIS_PORT=6379`

> Important: service names like `postgres` / `redis` work only **inside Docker network**.  
> If you run Django/Celery on your host machine, use `127.0.0.1`.

#### 3) Create venv and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
```

#### 4) Enable pre-commit
```bash
pre-commit install && pre-commit autoupdate
```

#### 5) Start Postgres + Redis
```bash
docker compose up -d --build
```

#### 6) Run migrations & start server
```bash
source ./.env
python manage.py migrate
python manage.py runserver
```

Swagger:
- `/swagger/`
- `/redoc/`

---

## Running Celery (worker/beat)

If you run Celery from **host machine**, Redis host must be `127.0.0.1`, not `redis`.

#### Worker (Terminal #1)
```bash
source ./.env
celery -A config worker -l info
```

#### Beat (Terminal #2)
```bash
source ./.env
celery -A config beat -l info
```

Used tasks:
- `send_verification_email_task(email, token)`
- `users.cleanup_unverified_users(hours=48)` (periodic)

---

## Test Environment

#### 1) Generate test env/docker files
```bash
chmod +x start.sh
./start.sh test
```

#### 2) Run test docker compose
```bash
docker compose up -d --build
```

#### 3) Run tests locally
```bash
source ./.env
pytest -q
```

---

## API Endpoints (v1)

Base prefix (recommended):
- `/api/v1/`

### Auth & Users
- `POST /api/v1/user/signup/`  
  Create user with `is_verified=false` and send verification token (console email in dev).
- `POST /api/v1/user/login/`  
  JWT login (access token).
- `GET /api/v1/user/me/`  
  Get current user from `Authorization: Bearer <token>`.
- `PATCH /api/v1/user/me/`  
  Update current user (e.g., `full_name`, `username`).
- `GET /api/v1/user/verify-email/?token=<uuid>`  
  Verify email token, set `is_verified=true`.

### Posts
- `GET /api/v1/posts/`  
  List posts (filters/search/ordering + pagination).
- `POST /api/v1/posts/`  
  Create post (auth required + verified required).
- `GET /api/v1/posts/<id>/`  
  Post details with comments and likes.
- `PATCH /api/v1/posts/<id>/`  
  Update (owner + verified).
- `DELETE /api/v1/posts/<id>/`  
  Delete (owner + verified).

### Comments
- `GET /api/v1/posts/<post_id>/comments/`  
  List post comments.
- `POST /api/v1/posts/<post_id>/comments/`  
  Create comment (auth + verified).
- `DELETE /api/v1/posts/<post_id>/comments/<id>/`  
  Delete comment (owner).

### Likes
- `POST /api/v1/posts/<post_id>/like/`  
  Like post (auth). Cannot like own post.
- `DELETE /api/v1/posts/<post_id>/like/`  
  Unlike post.

### Feed
- `GET /api/v1/feed/`  
  A simple feed endpoint per test task requirements.

---

## Project Structure

```
.
└── .deployments
    ├── development
    │   ├── db_configs
    │   │   ├── Dockerfile
    │   │   └── postgres-script.sh
    │   ├── docker-compose.yml
    │   └── env_example.txt
    ├── test
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   ├── env_example.txt
    │   └── test-script.sh
    ├── production
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   └── env_example.txt
    ├── staging
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   └── env_example.txt
    ├── entrypoint.sh
    └── run.sh
└── apps
    ├── common
    ├── users
    ├── posts
    ├── comments
    └──  likes
└── config
    ├── settings
    │   ├── base.py
    │   ├── development.py
    │   ├── test.py
    │   ├── staging.py
    │   └── production.py
    ├── celery.py
    ├── urls.py
    └── wsgi.py
└── requirements
    ├── base.txt
    ├── development.txt
    ├── test.txt
    ├── staging.txt
    └── production.txt
├── manage.py
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

---

## Linting & Formatting
This project uses:
- **ruff**
- **black**
- **pre-commit**

Run locally:
```bash
ruff check .
black .
```

---

## Tests

Minimal pytest testcases exist per app:
- `apps/users/tests.py`
- `apps/posts/tests.py`
- `apps/comments/tests.py`
- `apps/likes/tests.py`

Run:
```bash
pytest -q
```

---

## Notes

### Email verification (dev)
In development, SMTP is not required. Use **console email backend** so the verification link/token is printed in terminal logs.

### Common local networking rule
- Running Django/Celery on host machine → use `DB_HOST=127.0.0.1`, `REDIS_HOST=127.0.0.1`
- Running inside Docker → use `DB_HOST=postgres`, `REDIS_HOST=redis`

### Cleanup task
Unverified users with expired tokens are removed by a periodic Celery task:
- `users.cleanup_unverified_users(hours=48)`
