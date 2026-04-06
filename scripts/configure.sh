#!/usr/bin/env bash
# PyraClaw Configure — NVIDIA API + Environment Setup
# Replaces broken OpenClaw configure.sh with proper key management
# DD7 International GmbH | Patent: PCT/EP2025/080977
set -euo pipefail

GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; BOLD='\033[1m'; NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"

banner() {
  echo -e "${CYAN}"
  echo "  ╔═══════════════════════════════════════════════════╗"
  echo "  ║          PyraClaw Sovereign AI Runtime            ║"
  echo "  ║          Configuration & API Setup                ║"
  echo "  ╚═══════════════════════════════════════════════════╝"
  echo -e "${NC}"
}

log()  { echo -e "${GREEN}[PYRACLAW]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*"; }

# ── Validate NVIDIA API key format ──────────────────────────
validate_nvidia_key() {
  local key="$1"
  if [[ -z "$key" ]]; then
    return 1
  fi
  # NVIDIA API keys are typically nvapi-* or alphanumeric strings
  if [[ ${#key} -lt 10 ]]; then
    warn "Key seems too short (${#key} chars). NVIDIA keys are usually 40+ characters."
    return 1
  fi
  return 0
}

# ── Test NVIDIA API connectivity ────────────────────────────
test_nvidia_api() {
  local key="$1"
  local base_url="${2:-https://integrate.api.nvidia.com/v1}"
  log "Testing NVIDIA API connectivity..."
  if command -v curl &>/dev/null; then
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer $key" \
      -H "Content-Type: application/json" \
      "$base_url/models" \
      --max-time 10 2>/dev/null) || true
    if [[ "$response" == "200" ]]; then
      log "NVIDIA API connection: ${GREEN}OK${NC}"
      return 0
    elif [[ "$response" == "401" ]]; then
      err "NVIDIA API key rejected (401 Unauthorized)"
      return 1
    elif [[ "$response" == "000" ]]; then
      warn "Could not reach NVIDIA API (network issue). Key saved anyway."
      return 0
    else
      warn "NVIDIA API returned HTTP $response. Key saved — verify manually."
      return 0
    fi
  else
    warn "curl not available — skipping API test. Key saved."
    return 0
  fi
}

# ── Set a key in .env file ──────────────────────────────────
set_env_var() {
  local var_name="$1"
  local var_value="$2"
  if [[ -f "$ENV_FILE" ]] && grep -q "^${var_name}=" "$ENV_FILE"; then
    # Update existing
    sed -i "s|^${var_name}=.*|${var_name}=${var_value}|" "$ENV_FILE"
  elif [[ -f "$ENV_FILE" ]]; then
    # Append
    echo "${var_name}=${var_value}" >> "$ENV_FILE"
  else
    # Create new .env from template
    if [[ -f "$PROJECT_DIR/.env.example" ]]; then
      cp "$PROJECT_DIR/.env.example" "$ENV_FILE"
      sed -i "s|^${var_name}=.*|${var_name}=${var_value}|" "$ENV_FILE"
    else
      echo "${var_name}=${var_value}" > "$ENV_FILE"
    fi
  fi
}

# ── Read existing value ─────────────────────────────────────
get_env_var() {
  local var_name="$1"
  if [[ -f "$ENV_FILE" ]]; then
    grep "^${var_name}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2- || echo ""
  fi
}

# ── Configure NVIDIA ────────────────────────────────────────
configure_nvidia() {
  echo ""
  echo -e "${BOLD}── NVIDIA API Configuration ──${NC}"
  echo ""

  local existing_key
  existing_key=$(get_env_var "NVIDIA_API_KEY")

  if [[ -n "$existing_key" && "$existing_key" != "your_nvidia_api_key" ]]; then
    local masked="${existing_key:0:8}...${existing_key: -4}"
    log "Existing NVIDIA API key found: $masked"
    echo -n "  Replace existing key? [y/N]: "
    read -r replace
    if [[ "$replace" != "y" && "$replace" != "Y" ]]; then
      log "Keeping existing NVIDIA API key."
      return 0
    fi
  fi

  echo -e "  Enter your NVIDIA API key (from ${CYAN}build.nvidia.com${NC})."
  echo -e "  The key will be stored in ${CYAN}.env${NC} (git-ignored)."
  echo ""

  local nvidia_key=""
  local attempts=0
  while [[ $attempts -lt 3 ]]; do
    echo -n "  NVIDIA API Key: "
    read -rs nvidia_key  # -s for silent input (no echo)
    echo ""  # newline after silent input

    if validate_nvidia_key "$nvidia_key"; then
      break
    else
      err "Invalid key format. Try again (attempt $((attempts + 1))/3)."
      attempts=$((attempts + 1))
      nvidia_key=""
    fi
  done

  if [[ -z "$nvidia_key" ]]; then
    err "No valid NVIDIA API key provided after 3 attempts."
    echo "  You can set it manually: echo 'NVIDIA_API_KEY=your_key' >> .env"
    return 1
  fi

  # Store the key
  set_env_var "NVIDIA_API_KEY" "$nvidia_key"
  set_env_var "NVIDIA_NEMOTRON_API_KEY" "$nvidia_key"
  set_env_var "NVIDIA_BASE_URL" "https://integrate.api.nvidia.com/v1"

  # Test connectivity
  test_nvidia_api "$nvidia_key"

  log "NVIDIA API key configured successfully."
  return 0
}

# ── Configure other providers (optional) ────────────────────
configure_optional_providers() {
  echo ""
  echo -e "${BOLD}── Optional: Additional LLM Providers ──${NC}"
  echo ""
  echo "  These are optional. Press Enter to skip any provider."
  echo ""

  local providers=("ANTHROPIC_API_KEY" "OPENAI_API_KEY" "GROQ_API_KEY" "XAI_API_KEY")
  local labels=("Anthropic" "OpenAI" "Groq" "xAI/Grok")

  for i in "${!providers[@]}"; do
    local var="${providers[$i]}"
    local label="${labels[$i]}"
    local existing
    existing=$(get_env_var "$var")

    if [[ -n "$existing" && "$existing" != "your_"* ]]; then
      local masked="${existing:0:6}...${existing: -4}"
      log "$label: configured ($masked)"
    else
      echo -n "  $label API Key (Enter to skip): "
      read -rs key
      echo ""
      if [[ -n "$key" ]]; then
        set_env_var "$var" "$key"
        log "$label: configured"
      else
        log "$label: skipped"
      fi
    fi
  done
}

# ── Detect GPU ──────────────────────────────────────────────
detect_gpu() {
  echo ""
  echo -e "${BOLD}── GPU Detection ──${NC}"
  echo ""

  if command -v nvidia-smi &>/dev/null; then
    log "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null | while read -r line; do
      log "  $line"
    done
    set_env_var "NVIDIA_NEMOTRON_GPU_ACCEL" "true"
    echo ""
    log "GPU compose file: docker-compose.pyraclaw-gpu.yml"
  else
    log "No local GPU detected — will use NVIDIA API (cloud inference)"
    set_env_var "NVIDIA_NEMOTRON_GPU_ACCEL" "false"
    echo ""
    log "CPU compose file: docker-compose.yml"
  fi
}

# ── Verify .env is git-ignored ──────────────────────────────
ensure_gitignore() {
  local gitignore="$PROJECT_DIR/.gitignore"
  if [[ -f "$gitignore" ]]; then
    if ! grep -q "^\.env$" "$gitignore"; then
      echo ".env" >> "$gitignore"
      log ".env added to .gitignore"
    fi
  else
    echo ".env" > "$gitignore"
    log "Created .gitignore with .env"
  fi
}

# ── Summary ─────────────────────────────────────────────────
print_summary() {
  echo ""
  echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}  PyraClaw Configuration Complete${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
  echo ""

  if [[ -f "$ENV_FILE" ]]; then
    local nvidia_set="no"
    local nvidia_key
    nvidia_key=$(get_env_var "NVIDIA_API_KEY")
    [[ -n "$nvidia_key" && "$nvidia_key" != "your_nvidia_api_key" ]] && nvidia_set="yes"

    echo "  NVIDIA API:  $([ "$nvidia_set" = "yes" ] && echo -e "${GREEN}configured${NC}" || echo -e "${YELLOW}not set${NC}")"

    for var in ANTHROPIC_API_KEY OPENAI_API_KEY GROQ_API_KEY XAI_API_KEY; do
      local val
      val=$(get_env_var "$var")
      local label="${var%%_API_KEY}"
      label="${label,,}"
      if [[ -n "$val" && "$val" != "your_"* ]]; then
        echo "  $label:  ${GREEN}configured${NC}"
      fi
    done
  fi

  echo ""
  echo "  Next steps:"
  echo "    GPU:  docker compose -f docker-compose.pyraclaw-gpu.yml up -d --build"
  echo "    CPU:  docker compose up -d --build"
  echo "    Test: bash scripts/deploy-gpu.sh"
  echo ""
}

# ── Main ────────────────────────────────────────────────────
main() {
  banner
  ensure_gitignore

  # Create .env from template if missing
  if [[ ! -f "$ENV_FILE" ]]; then
    if [[ -f "$PROJECT_DIR/.env.example" ]]; then
      cp "$PROJECT_DIR/.env.example" "$ENV_FILE"
      log "Created .env from template"
    fi
  fi

  configure_nvidia
  configure_optional_providers
  detect_gpu
  print_summary
}

main "$@"
