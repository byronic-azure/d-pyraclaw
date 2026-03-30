#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
# PyraClaw GCP Setup — Vertex AI + NPU/GPU + 2TB Drive Integration
# DD7 International GmbH | Patent: PCT/EP2025/080977
# ORCID: 0009-0001-9561-5483 | Byron Callaghan
#
# Run this from Google Cloud Shell or local gcloud CLI:
#   bash scripts/gcp-setup.sh
# ══════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT_ID="iaia-457300"
PROJECT_NUMBER="725993730956"
REGION="europe-west2"
SA_NAME="pyraclaw-runtime"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
log() { echo -e "${GREEN}[pyraclaw-gcp]${NC} $*"; }
warn() { echo -e "${YELLOW}[pyraclaw-gcp]${NC} $*"; }

log "PyraClaw GCP Setup | Project: ${PROJECT_ID} | Region: ${REGION}"
echo ""

# ── Step 1: Set project ──────────────────────────────────────────────
log "Step 1: Setting active project..."
gcloud config set project ${PROJECT_ID}

# ── Step 2: Enable APIs ──────────────────────────────────────────────
log "Step 2: Enabling APIs..."
APIS=(
    "aiplatform.googleapis.com"        # Vertex AI
    "compute.googleapis.com"           # Compute Engine (GPU/NPU VMs)
    "container.googleapis.com"         # GKE (Kubernetes)
    "artifactregistry.googleapis.com"  # Container Registry
    "run.googleapis.com"               # Cloud Run
    "cloudbuild.googleapis.com"        # Cloud Build
    "secretmanager.googleapis.com"     # Secret Manager
    "storage.googleapis.com"           # Cloud Storage (2TB backing)
    "drive.googleapis.com"             # Google Drive API
    "sheets.googleapis.com"            # Sheets API (evidence export)
    "monitoring.googleapis.com"        # Cloud Monitoring
    "logging.googleapis.com"           # Cloud Logging
    "iam.googleapis.com"               # IAM
)

for api in "${APIS[@]}"; do
    log "  Enabling ${api}..."
    gcloud services enable ${api} --quiet 2>/dev/null || warn "  Already enabled or error: ${api}"
done

# ── Step 3: Create service account ───────────────────────────────────
log "Step 3: Creating service account..."
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="PyraClaw Sovereign Runtime" \
    --description="Service account for PyraClaw AI runtime — DD7 International GmbH" \
    2>/dev/null || warn "  Service account may already exist"

# ── Step 4: Grant roles ──────────────────────────────────────────────
log "Step 4: Granting IAM roles..."
ROLES=(
    "roles/aiplatform.user"            # Vertex AI inference
    "roles/aiplatform.admin"           # Vertex AI management
    "roles/storage.admin"              # Cloud Storage (2TB)
    "roles/compute.instanceAdmin.v1"   # GPU/NPU VM management
    "roles/container.admin"            # GKE management
    "roles/artifactregistry.writer"    # Push container images
    "roles/secretmanager.secretAccessor" # Read secrets
    "roles/monitoring.editor"          # Metrics
    "roles/logging.logWriter"          # Logging
)

for role in "${ROLES[@]}"; do
    log "  Granting ${role}..."
    gcloud projects add-iam-policy-binding ${PROJECT_ID} \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="${role}" \
        --quiet 2>/dev/null || warn "  Role may already be bound"
done

# ── Step 5: Create service account key ───────────────────────────────
log "Step 5: Creating service account key..."
KEY_FILE="credentials/gcp-service-account.json"
mkdir -p credentials
gcloud iam service-accounts keys create ${KEY_FILE} \
    --iam-account=${SA_EMAIL} \
    2>/dev/null || warn "  Key creation failed — may need manual creation"

if [ -f "${KEY_FILE}" ]; then
    log "  Key saved to: ${KEY_FILE}"
    log "  ${YELLOW}SECURITY: Add credentials/ to .gitignore (already done)${NC}"
else
    warn "  Key file not created — generate manually:"
    warn "  gcloud iam service-accounts keys create ${KEY_FILE} --iam-account=${SA_EMAIL}"
fi

# ── Step 6: Create Cloud Storage bucket for 2TB data ─────────────────
log "Step 6: Creating Cloud Storage bucket..."
BUCKET="gs://pyraclaw-${PROJECT_ID}-data"
gsutil mb -p ${PROJECT_ID} -l ${REGION} -c STANDARD ${BUCKET} 2>/dev/null \
    || warn "  Bucket may already exist"
log "  Bucket: ${BUCKET}"

# ── Step 7: Create Artifact Registry for container images ────────────
log "Step 7: Creating Artifact Registry..."
gcloud artifacts repositories create pyraclaw-images \
    --repository-format=docker \
    --location=${REGION} \
    --description="PyraClaw container images" \
    2>/dev/null || warn "  Registry may already exist"

# ── Step 8: Create Secret Manager entries ────────────────────────────
log "Step 8: Setting up Secret Manager..."
SECRETS=(
    "pyraclaw-nvidia-api-key"
    "pyraclaw-anthropic-api-key"
    "pyraclaw-openai-api-key"
    "pyraclaw-qdp-super-hash"
)
for secret in "${SECRETS[@]}"; do
    gcloud secrets create ${secret} --replication-policy="automatic" 2>/dev/null \
        || warn "  Secret ${secret} may already exist"
done

# ── Step 9: Verify GPU/NPU quota ────────────────────────────────────
log "Step 9: Checking GPU/NPU quota..."
echo ""
log "  Check your GPU quota at:"
log "  https://console.cloud.google.com/iam-admin/quotas?project=${PROJECT_ID}"
echo ""
log "  Required for NemoClaw x3:"
log "    - NVIDIA T4:  3 GPUs (or A100/H100 for production)"
log "    - NPU/TPU:    Available via Vertex AI endpoints"
log "    - Memory:     128GB+ recommended"
echo ""

# ── Summary ──────────────────────────────────────────────────────────
echo ""
log "══════════════════════════════════════════════════════════════"
log "  GCP Setup Complete"
log "══════════════════════════════════════════════════════════════"
log "  Project:       ${PROJECT_ID}"
log "  Region:        ${REGION}"
log "  Service Acct:  ${SA_EMAIL}"
log "  Key File:      ${KEY_FILE}"
log "  Storage:       ${BUCKET}"
log "  Registry:      ${REGION}-docker.pkg.dev/${PROJECT_ID}/pyraclaw-images"
log "  APIs enabled:  ${#APIS[@]}"
log "  Roles granted: ${#ROLES[@]}"
log "  Secrets:       ${#SECRETS[@]}"
log ""
log "  Next steps:"
log "    1. Copy ${KEY_FILE} to your .env as GOOGLE_APPLICATION_CREDENTIALS"
log "    2. Run: gcloud auth configure-docker ${REGION}-docker.pkg.dev"
log "    3. Push images: docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/pyraclaw-images/SERVICE:TAG"
log "    4. Deploy to Vertex AI or GKE"
log "══════════════════════════════════════════════════════════════"
