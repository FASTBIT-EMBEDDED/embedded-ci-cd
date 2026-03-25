param(
    [string]$Project = "020_Bouncy_Ball",
    [string]$Cmd = "make summary"
)

docker compose -f container/docker-compose.yml run --rm embedded-dev bash -lc "cd /workspace/Projects/$Project && $Cmd"