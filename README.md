# Graphite Message Lab

An intentionally small, interactive application for exercising Project Graphite's complete deployment path.

Visitors can post a message in the browser. Django validates it through a JSON API, PostgreSQL persists it,
Redis delivers a background job, and a Celery worker counts its words and marks it processed. The browser
polls the API so the status change is visible without a reload.

## Stack

- Frontend: server-rendered HTML, Tailwind CSS, and a small JavaScript client
- Backend: Django and Gunicorn
- Database: PostgreSQL
- Queue: Redis
- Worker: Celery
- Local packaging: Docker and Docker Compose
- Delivery: GitHub Actions, GitHub Container Registry, and Kubernetes

## Run locally

Docker with Compose v2 is the only prerequisite.

```sh
cp .env.example .env
docker compose build
docker compose up
docker compose exec web python manage.py migrate
```

Open <http://localhost:8000>, submit a message, and watch its status move from `queued` to `processed`.

Useful checks:

```sh
./run manage test
./run lint
curl --fail http://localhost:8000/up/databases
```

## API

`GET /api/messages/` returns the latest 25 messages. `POST /api/messages/` accepts:

```json
{
  "display_name": "Ada",
  "body": "Hello Graphite"
}
```

The public feed is deliberate for this disposable experiment. Do not enter private or sensitive information.

## Deployment

Production resources are generated from
[`projects/graphite-message-lab.yml`](https://github.com/project-graphite/platform/blob/main/projects/graphite-message-lab.yml)
in the private platform repository. Docker Compose is local-development tooling only. Cluster
creation, secret setup, deployment, rollback, and cleanup are documented in the organisation's
private operations runbook.

## Attribution

The Docker foundation was adapted from Nick Janetakis' MIT-licensed `docker-django-example`. See
[UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).
