param(
    [string]$Project = "020_Bouncy_Ball"
)

docker compose -f container/docker-compose.yml run --rm embedded-dev bash -lc "cd /workspace/Projects/$Project && python tools/quality/run_quality_gate.py"