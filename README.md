# Graphite Message Lab

An intentionally small, interactive application for exercising Project Graphite's complete deployment path.

Visitors send a message privately or ask for it to be published. Django validates it through a JSON API,
PostgreSQL persists it, Redis delivers a background job, and a Celery worker counts its words. A message
appears on the public wall only when its sender asked for publication and an administrator publishes it in
/admin/; the browser polls the API to refresh the wall.

## Stack

- Frontend: server-rendered HTML, Tailwind CSS, and a small JavaScript client
- Backend: Django and Gunicorn
- Database: PostgreSQL
- Queue: Redis
- Worker: Celery
- Local packaging: Docker and Docker Compose
- Delivery: GitHub Actions, GitHub Container Registry, Coolify, and Docker Compose

## Run locally

Docker with Compose v2 is the only prerequisite.

```sh
cp .env.example .env
docker compose build
docker compose up
docker compose exec web python manage.py migrate
```

Open <http://localhost:8000>, choose "Public after review" and submit a message. It stays private until you
publish it from /admin/ (create an account with `./run manage createsuperuser`), and then it appears on the
public wall within 15 seconds.

Useful checks:

```sh
./run manage test
./run lint
curl --fail http://localhost:8000/up/databases
```

## API

`GET /api/messages/` returns the latest 25 published messages. `POST /api/messages/` accepts:

```json
{
  "display_name": "Ada",
  "body": "Hello Graphite",
  "requested_visibility": "public"
}
```

`requested_visibility` defaults to `"private"`.

Messages are stored and read by the administrator. Do not enter private or sensitive information.

## Deployment

Production metadata is registered in
[`projects/graphite-message-lab.yml`](https://github.com/project-graphite/platform/blob/main/projects/graphite-message-lab.yml)
in the private platform repository. Coolify deploys `compose.production.yaml`, which pulls the
prebuilt GHCR images, limits memory and CPU, persists PostgreSQL and Redis in named volumes, runs
database migrations before Gunicorn starts, and exposes only the web service through Coolify's
proxy. VPS setup, secret entry, deployment, rollback, backup, and cleanup are documented in the
organisation's private operations runbook.

## Attribution

The Docker foundation was adapted from Nick Janetakis' MIT-licensed `docker-django-example`. See
[UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).
