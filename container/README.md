# Container Environment

This folder contains the shared container setup for all embedded projects in this repository.

## Repo layout

- `container/` -> all Docker-related setup
- `Projects/` -> actual firmware projects

## Build image

From repo root:

```powershell
docker compose -f container/docker-compose.yml build