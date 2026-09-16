# Upstream

This temporary deployment lab is derived from
[`nickjj/docker-django-example`](https://github.com/nickjj/docker-django-example) at commit
`b04a6d911620366f83080a9b1803486c35ced303`.

The upstream project and this copy are distributed under the MIT License. Project Graphite's changes are
limited to deployment automation, production Compose configuration, dependency automation, and support for
a single `DATABASE_URL` connection string.

To inspect later upstream changes:

```sh
git fetch upstream
git log --oneline --left-right main...upstream/main
```
