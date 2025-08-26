# 📚 Bookstall - Django + Docker + Postgres Setup

This project runs a **Django application** (`bookstall`) inside **Docker containers** with **Postgres** as the database.

---

## 🚀 Getting Started

### 1️⃣ Build and Start Containers
```bash
docker compose -f bookstalll.yaml up -d --build
```
- Builds the Docker image.
- Creates and starts the containers (web + db).
- Runs in detached mode (`-d`).

---

### 2️⃣ Apply Migrations
Run inside the **web** container:
```bash
docker compose -f bookstall.yaml exec web python manage.py makemigrations
docker compose -f bookstall.yaml exec web python manage.py migrate
```

---

### 3️⃣ Create Superuser (optional)
```bash
docker compose -f bookstall.yaml exec web python manage.py createsuperuser
```

---

### 4️⃣ Access the App
- Django server: 👉 http://127.0.0.1:8000  
- Admin panel: 👉 http://127.0.0.1:8000/admin  

---

## 🔄 Next Time (Re-Starting Project)
If containers already exist, just run:
```bash
docker compose -f bookstall.yaml up -d
```

If you want to stop containers:
```bash
docker compose -f bookstall.yaml down
```
Check Running containers:
```bash
docker ps
```
---

## 🐳 Running Without Docker Compose
If you want to run only the image **(not recommended for multi-container projects)**:
```bash
docker run -d -p 8000:8000 bookstall-web
```

But usually, **use `docker compose`** since it manages both Django + Postgres together.

---

## ⚡ Useful Commands

### View logs
```bash
docker compose -f bookstalll.yaml logs -f
```

### Access a shell inside web container
```bash
docker compose -f bookstalll.yaml exec web bash
```

### Rebuild after code changes
```bash
docker compose -f bookstalll.yaml up -d --build
```

---

✅ You now have Django + Postgres running inside Docker containers.
