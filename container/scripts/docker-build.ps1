param(
    [string]$Project = "020_Bouncy_Ball",
    [string]$Build = "debug",
    [string]$Target = "target",
    [string]$Test = "none"
)

docker compose -f container/docker-compose.yml run --rm embedded-dev bash -lc "cd /workspace/Projects/$Project && make target=$Target test=$Test build=$Build"