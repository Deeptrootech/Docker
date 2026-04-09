# Bookstall

Bookstall is a Django project that runs with Docker Compose in development.

The development stack in this repository includes:

- Django application containers: `webapp1`, `webapp2`, `webapp3`
- PostgreSQL database: `db`
- Redis: `redis`
- Nginx load balancer / reverse proxy: `nginx`

Nginx sits in front of the Django containers, so the main application entrypoint is `http://127.0.0.1:8080`.

## 1. What This Project Runs

When you start the development environment, Docker Compose creates these services:

- `db`: PostgreSQL database
- `redis`: Redis instance for cache / broker style use
- `webapp1`, `webapp2`, `webapp3`: three Django app containers
- `nginx`: routes incoming traffic to the Django app containers

Development ports exposed on your machine:

- `8080` -> Nginx -> main app entrypoint
- `8003` -> Django `webapp1`
- `8004` -> Django `webapp2`
- `8005` -> Django `webapp3`
- `9006` -> PostgreSQL
- `9007` -> Redis

## 2. Prerequisites

Install these into your system before running the project:

- Docker
- Docker Compose plugin

Check they are available:

```bash
docker --version
docker compose version
```

## 3. Project Files You Should Know

- `docker-compose.dev.yaml`: development environment
- `Dockerfile.dev`: Django development image
- `.env`: environment variables used by the development setup
- `nginx.dev.conf`: Nginx config for local development

## 4. First-Time Setup

### Step 1: Move into the project directory

```bash
cd /home/jitendra/Desktop/Deep/4.DOCKER/Simple_django/bookstall
```

### Step 2: Build and start the containers

```bash
docker compose -f docker-compose.dev.yaml up -d --build
```

What this does:

- builds the Django image from `Dockerfile.dev`
- starts PostgreSQL, Redis, three Django containers, and Nginx
- runs everything in detached mode

### Step 3: Confirm the containers are running

```bash
docker compose -f docker-compose.dev.yaml ps
```

You should see services for:

- `db`
- `redis`
- `webapp1`
- `webapp2`
- `webapp3`
- `nginx`

### Step 4: Apply database migrations

Run migrations from one Django container. Use `webapp1`.

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py migrate
```

Notes:

- `makemigrations` is only needed when you change models
- `migrate` applies migration files to the database
- you do not need to run the same migration command in all three app containers

If you create or modify models later:

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py makemigrations
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py migrate
```

### Step 5: Create an admin user

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py createsuperuser
```

### Step 6: Open the application

Main entrypoint through Nginx:

- App: `http://127.0.0.1:8080`
- Admin: `http://127.0.0.1:8080/admin`

Direct Django container access is also available:

- `http://127.0.0.1:8003`
- `http://127.0.0.1:8004`
- `http://127.0.0.1:8005`

For normal use, prefer `8080` because that matches the full local setup with Nginx in front.

## 5. Daily Development Workflow

### Start the existing containers

```bash
docker compose -f docker-compose.dev.yaml up -d
```

### Stop the containers

```bash
docker compose -f docker-compose.dev.yaml down
```

### Stop and remove containers, networks, and volumes

Use this only if you intentionally want a fresh database state.

```bash
docker compose -f docker-compose.dev.yaml down -v
```

### Rebuild after Docker-related changes

Use this after changing Dockerfiles, Python dependencies, or container setup.

```bash
docker compose -f docker-compose.dev.yaml up -d --build
```

## 6. Useful Commands

### View logs from all services

```bash
docker compose -f docker-compose.dev.yaml logs -f
```

### View logs for one service

```bash
docker compose -f docker-compose.dev.yaml logs -f webapp1
docker compose -f docker-compose.dev.yaml logs -f nginx
docker compose -f docker-compose.dev.yaml logs -f db
```

### Open a shell inside a Django container

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 bash
```

### Run Django management commands

Examples:

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py showmigrations
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py collectstatic --noinput
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py shell
```

### Check running containers

```bash
docker ps
```

## 7. How Requests Flow in Development

If you open `http://127.0.0.1:8080`, the request flow is:

1. browser sends request to `nginx`
2. Nginx forwards the request to one of the Django containers
3. Django reads/writes data from PostgreSQL when needed
4. Redis is available for caching or broker-related tasks
5. response returns through Nginx to the browser

If you open `8003`, `8004`, or `8005` directly, you bypass Nginx and talk to a single Django container.

## 8. Environment Notes

Development settings use:

- `.env`
- `bookstall.settings.dev`

The current development setup expects values such as:

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- Redis URLs

If the `.env` file is missing, development startup can fail because the Django settings explicitly load it.

## 9. Beginner Notes

- `docker compose up -d --build` builds images and starts containers
- `docker compose up -d` starts existing containers without rebuilding
- `exec webapp1 ...` means "run this command inside the running `webapp1` container"
- `migrate` updates the database schema
- `createsuperuser` creates a login for Django admin
- `logs -f` shows live logs and keeps streaming output

## 10. Common Problems

### Port already in use

If Docker says a port is already busy, check what is using it:

```bash
docker ps
```

Common ports in this project:

- `8080`
- `8003`
- `8004`
- `8005`
- `9006`
- `9007`

### App starts but database commands fail

Make sure the database container is running:

```bash
docker compose -f docker-compose.dev.yaml ps
```

Then retry:

```bash
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py migrate
```

### Changes are not reflected

Try rebuilding:

```bash
docker compose -f docker-compose.dev.yaml up -d --build
```

### Need a clean restart

```bash
docker compose -f docker-compose.dev.yaml down
docker compose -f docker-compose.dev.yaml up -d --build
```

## 11. One-Minute Quick Start

If you already understand Docker and only want the minimum steps:

```bash
docker compose -f docker-compose.dev.yaml up -d --build
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py migrate
docker compose -f docker-compose.dev.yaml exec webapp1 python manage.py createsuperuser
```

Then open:

- `http://127.0.0.1:8080`
- `http://127.0.0.1:8080/admin`

## 12. Summary

For this repository, the correct development flow is:

1. start the stack with `docker-compose.dev.yaml`
2. run Django commands inside `webapp1`
3. access the app through Nginx on port `8080`
4. use `8003`, `8004`, and `8005` only when you specifically want direct access to individual Django containers
