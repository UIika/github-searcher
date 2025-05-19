# GitHub Search App

A fullstack web app to search GitHub users or repositories with caching and a clean React frontend.

**Deployed on AWS EC2 instance - http://18.184.64.217/**

## Tech Stack and Design Decisions

### Frontend: React + Vite + TypeScript + SCSS

- **Vite** was chosen for fast development and build times.
- **TypeScript** improves code reliability and developer productivity.
- **SCSS** allows for modular and maintainable styling. A dedicated `styles/` folder organizes styles cleanly.
- **Debounced Search** prevents excessive API calls by only triggering requests after typing pauses.

### Backend: Django + DRF

- **Django REST Framework** offers robust API support, authentication, and validation.
- Two endpoints were implemented:
  - `/api/search/` – handles GitHub searches and leverages Redis cache.
  - `/api/clear-cache/` – clears all cache keys starting with `gh_search:`.

### Caching: Redis

- GitHub API has rate limits. To improve performance and reduce calls, we cache responses in **Redis** for 2 hours.
- Redis key generation uses a SHA-256 hash of the query and type to ensure uniqueness and consistency.

### Documentation: Swagger

- API documentation is generated with **drf-yasg** and available at `/swagger/`.
- This allows quick testing and clear visibility of request/response formats.

### Deployment: Docker + Docker Compose

- **Docker** enables consistent, isolated environments across development and production.
- **Docker Compose** sets up the app (frontend, backend, Redis) in one command.
- Can be deployed quickly to platforms like AWS EC2, Railway, or Fly.io.


## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-user/github-search-app
cd github-search-app
```

### 2. Docker Compose

```bash
docker-compose up --build
```

This will start:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Redis instance

### 3. Environment Variables

Create a .env file in the **backend** folder like this:

```bash
DEBUG=True
SECRET_KEY="your-secret-key"
GITHUB_TOKEN="your-github-token"
```

### 4. Running Tests

```bash
docker-compose exec backend pytest
```