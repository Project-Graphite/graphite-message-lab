# Upstream

This temporary deployment lab is derived from
[`nickjj/docker-django-example`](https://github.com/nickjj/docker-django-example) at commit
`b04a6d911620366f83080a9b1803486c35ced303`.

The upstream project and this copy are distributed under the MIT License. Project Graphite replaced the
example page with the message inbox (the inbox app with its JSON API, moderation and Celery task, the page
templates, JavaScript client and theme). It also added dependency automation and a main-branch build that
publishes the images and records their tag in the `platform` repository, which defines production; this
repository has no production Compose file.

To inspect later upstream changes:

```sh
git remote add upstream https://github.com/nickjj/docker-django-example.git
git fetch upstream
git log --oneline --left-right main...upstream/main
```
