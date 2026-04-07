#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
log() { echo -e "${GREEN}[PYRACLAW]${NC} $*"; }
err() { echo -e "${RED}[PYRACLAW]${NC} $*"; exit 1; }

log "PyraClaw GPU Deploy | $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Check GPU
if command -v nvidia-smi &>/dev/null; then
  log "GPU detected:"
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
  log "No GPU detected — falling back to CPU compose"
  COMPOSE_FILE="docker-compose.yml"
fi

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.pyraclaw-gpu.yml}"

# Pull latest
if [ -d ".git" ]; then
  log "Pulling latest..."
  git pull --ff-only 2>/dev/null || true
fi

# Build and deploy
log "Building with $COMPOSE_FILE..."
docker compose -f "$COMPOSE_FILE" build 2>&1 | tail -5

log "Starting services..."
docker compose -f "$COMPOSE_FILE" up -d

# Health checks
log "Waiting 20s for startup..."
sleep 20

HEALTHY=0; UNHEALTHY=0
for port in 8001 8002 8005 8006 8009 8010 8011 8012 9044 9045 9046 9047 9048 3000; do
  if curl -sf "http://localhost:$port/health" --max-time 4 | grep -q "healthy"; then
    log "  :$port HEALTHY"
    HEALTHY=$((HEALTHY + 1))
  else
    log "  :$port PENDING"
    UNHEALTHY=$((UNHEALTHY + 1))
  fi
done

log "Health: $HEALTHY healthy, $UNHEALTHY pending"
log "Deploy complete | $COMPOSE_FILE"
