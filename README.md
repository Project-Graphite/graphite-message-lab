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
- Delivery: GitHub Actions, GitHub Container Registry, and the Project Graphite platform

## Run locally

Docker with Compose v2 is the only prerequisite.

```sh
cp .env.example .env
docker compose build
docker compose up -d
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

Retired. Message Lab proved the Project Graphite deploy path end to end, and its one feature now
lives in Graphite Hub as the messages wall at
[project-graphite.com/messages](https://project-graphite.com/messages). Nothing runs at
`message-lab.project-graphite.com`: the registry entry in `.graphite.yml` is `archived` with
`deploy: none`, and `platform` has no `deploy/graphite-message-lab/` folder. The repository stays
as the case study and runs locally as above.

A push to `main` still publishes the `web` and `worker` images to GHCR; the deploy job then finds
no deploy folder in `platform` and records nothing, by design.

To create an administrator locally:

```sh
./run manage createsuperuser
```

## Attribution

The Docker foundation was adapted from Nick Janetakis' MIT-licensed `docker-django-example`. See
[UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).
