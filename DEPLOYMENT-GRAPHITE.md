# Deploy Graphite Message Lab

This temporary repository exercises a real four-service application: Django serves the UI and API,
PostgreSQL stores messages, Redis carries jobs, and a Celery worker processes each message.

## Target architecture

Use one 4 GB Linux VM running Docker Compose, with a Cloudflare Tunnel in front:

```text
message-lab.project-graphite.com
  -> Cloudflare Tunnel
  -> http://127.0.0.1:8000
  -> Django web/API
       -> PostgreSQL
       -> Redis -> Celery worker
```

Only Django binds a host port, and it binds to loopback. PostgreSQL and Redis remain on the private Compose
network. This keeps the experiment understandable and avoids Kubernetes before it is useful.

## Build and deployment record

`.github/workflows/main.yml` builds one immutable application image and publishes it under both `web` and
`worker` package names. The services run that image with different commands. Once the repository variable
`GRAPHITE_DEPLOY_ENABLED` is `true`, the workflow records both image tags in the Graphite platform registry.

The repository is public so it can use the organization's deployment GitHub App secrets on GitHub Free.
Secret values are never exposed to builds from untrusted pull requests.

## Prepare the host

1. Create a 4 GB Linux VM and install Docker Engine, the Compose plugin, and `cloudflared`.
2. Authenticate Docker to GHCR using a read-only package token or GitHub App credential.
3. Clone this repository into `/opt/graphite/graphite-message-lab`.
4. Copy `deploy.env.example` to `deploy.env` and replace every placeholder.
5. Set `IMAGE_TAG` to the complete `sha-<commit>` tag produced by GitHub Actions.
6. In Cloudflare Zero Trust, create a tunnel and route `message-lab.project-graphite.com` to
   `http://localhost:8000`.
7. Install the tunnel service on the host using the command Cloudflare provides.

## Start the application

```sh
docker compose --env-file deploy.env -f compose.deploy.yaml pull
docker compose --env-file deploy.env -f compose.deploy.yaml --profile tools run --rm migrate
docker compose --env-file deploy.env -f compose.deploy.yaml up -d web worker postgres redis
```

Verify the application and its dependencies before enabling the public hostname:

```sh
curl --fail http://127.0.0.1:8000/up
curl --fail http://127.0.0.1:8000/up/databases
docker compose --env-file deploy.env -f compose.deploy.yaml ps
```

Submit a test message in the browser. It should appear as `queued`, then become `processed` with a word count
after the worker consumes the job.

## Update and rollback

To update, change `IMAGE_TAG` to a newer immutable tag and repeat `pull`, `migrate`, and `up -d`. To roll back
application code, restore the prior tag and run `up -d` again. Back up PostgreSQL before any migration that is
not backward compatible.

## Cleanup

After the experiment, remove the Cloudflare hostname and tunnel route, stop the Compose project, and delete
its volumes only after confirming the test messages are disposable. Then remove the platform registry entry,
GHCR packages, VM, and repository.
