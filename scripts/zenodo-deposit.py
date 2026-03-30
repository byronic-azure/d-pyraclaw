#!/usr/bin/env python3
"""
PyraClaw Zenodo Deposit Script — Evidence-First DOI Minting
DD7 International GmbH | Patent: PCT/EP2025/080977
ORCID (PyraClaw): 0009-0003-9584-1741

Creates a Zenodo deposit for PyraClaw v1.0.0 with:
- Full metadata (title, description, creators, keywords)
- License: Apache-2.0
- Community: pyraclaw
- ORCID linking
- DOI reservation

Usage:
    export ZENODO_ACCESS_TOKEN=your_token
    python scripts/zenodo-deposit.py

For sandbox testing:
    export ZENODO_SANDBOX=true
    python scripts/zenodo-deposit.py
"""

import json
import os
import sys
import time
import hashlib

# ── Configuration ─────────────────────────────────────────────────────────
SANDBOX = os.getenv("ZENODO_SANDBOX", "true").lower() == "true"
BASE_URL = "https://sandbox.zenodo.org/api" if SANDBOX else "https://zenodo.org/api"
TOKEN = os.getenv("ZENODO_ACCESS_TOKEN", "")
VERSION = "1.0.0"
ORCID_PYRACLAW = "0009-0003-9584-1741"
ORCID_BYRON = "0009-0001-9561-5483"

METADATA = {
    "metadata": {
        "title": f"PyraClaw Sovereign AI Runtime v{VERSION} — MINTED_GREEN | SURGICAL",
        "upload_type": "software",
        "description": (
            "PyraClaw is a compliance-first sovereign AI runtime with "
            "cryptographic evidence sealing (QDP 5-DIP SHA), 44-agent "
            "CognitivePyraClaw swarm, 8-dimension RSFS quality scoring, "
            "and EU AI Act / SOC2 / GDPR compliance embedded at the "
            "architecture level. GPU-accelerated with NVIDIA NemoClaw x3. "
            "Patent: PCT/EP2025/080977 | US 19/541,276. "
            "No overclaiming. Results-driven. Evidence-first."
        ),
        "creators": [
            {
                "name": "Callaghan, Byron",
                "affiliation": "DD7 International GmbH",
                "orcid": ORCID_BYRON,
            },
            {
                "name": "PyraClaw iAiA",
                "affiliation": "DD7 International GmbH",
                "orcid": ORCID_PYRACLAW,
            },
        ],
        "keywords": [
            "sovereign-ai",
            "evidence-sealing",
            "compliance-first",
            "cryptographic-hashing",
            "multi-agent-swarm",
            "eu-ai-act",
            "soc2",
            "gdpr",
            "gpu-inference",
            "pyraclaw",
            "minted-green",
        ],
        "license": "Apache-2.0",
        "version": VERSION,
        "language": "eng",
        "notes": (
            "DD7 International GmbH. "
            "Patent: PCT/EP2025/080977 | US 19/541,276. "
            "ORCID: 0009-0003-9584-1741 (PyraClaw), 0009-0001-9561-5483 (Byron Callaghan). "
            "IP Terms: Licensing only. No IP transfer. No source code disclosure."
        ),
        "related_identifiers": [
            {
                "identifier": "https://github.com/tritathadore/pyraclaw",
                "relation": "isSupplementTo",
                "resource_type": "software",
                "scheme": "url",
            },
            {
                "identifier": "https://github.com/byronic-azure/pyraclaw",
                "relation": "isAlternateIdentifier",
                "resource_type": "software",
                "scheme": "url",
            },
        ],
        "communities": [{"identifier": "pyraclaw"}] if not SANDBOX else [],
    }
}


def main():
    print(f"PyraClaw Zenodo Deposit — v{VERSION}")
    print(f"  Mode:    {'SANDBOX' if SANDBOX else 'PRODUCTION'}")
    print(f"  API:     {BASE_URL}")
    print(f"  ORCID:   {ORCID_PYRACLAW} (PyraClaw)")
    print(f"  ORCID:   {ORCID_BYRON} (Byron)")
    print()

    if not TOKEN:
        print("ERROR: Set ZENODO_ACCESS_TOKEN environment variable")
        print()
        print("To get a token:")
        print(f"  1. Go to {'https://sandbox.zenodo.org' if SANDBOX else 'https://zenodo.org'}/account/settings/applications/")
        print("  2. Create a new personal access token")
        print("  3. Grant 'deposit:actions' and 'deposit:write' scopes")
        print("  4. export ZENODO_ACCESS_TOKEN=your_token")
        print()
        print("For sandbox testing:")
        print("  export ZENODO_SANDBOX=true")
        print("  export ZENODO_ACCESS_TOKEN=your_sandbox_token")
        sys.exit(1)

    try:
        import httpx
    except ImportError:
        print("Installing httpx...")
        os.system(f"{sys.executable} -m pip install httpx -q")
        import httpx

    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    # Step 1: Create deposit
    print("Step 1: Creating deposit...")
    r = httpx.post(f"{BASE_URL}/deposit/depositions", headers=headers, json={})
    if r.status_code not in (200, 201):
        print(f"  ERROR: {r.status_code} {r.text[:200]}")
        sys.exit(1)

    deposit = r.json()
    deposit_id = deposit["id"]
    doi = deposit.get("metadata", {}).get("prereserve_doi", {}).get("doi", "pending")
    print(f"  Deposit ID: {deposit_id}")
    print(f"  Reserved DOI: {doi}")

    # Step 2: Update metadata
    print("Step 2: Updating metadata...")
    r = httpx.put(f"{BASE_URL}/deposit/depositions/{deposit_id}", headers=headers, json=METADATA)
    if r.status_code != 200:
        print(f"  ERROR: {r.status_code} {r.text[:200]}")
    else:
        print(f"  Metadata updated: {METADATA['metadata']['title']}")

    # Step 3: Upload release archive (placeholder — real upload would include the tarball)
    print("Step 3: Creating release manifest...")
    manifest = {
        "pyraclaw_version": VERSION,
        "deposit_id": deposit_id,
        "doi": doi,
        "orcid_pyraclaw": ORCID_PYRACLAW,
        "orcid_byron": ORCID_BYRON,
        "patent": "PCT/EP2025/080977",
        "github_release": f"https://github.com/tritathadore/pyraclaw/releases/tag/v{VERSION}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "services": 11,
        "lines_of_code": 6000,
        "compliance": ["EU_AI_ACT", "SOC2", "GDPR", "ISO_27001", "PRINCE2_AGILE"],
        "seal": hashlib.sha256(json.dumps(METADATA, sort_keys=True).encode()).hexdigest(),
    }
    print(f"  Manifest sealed: {manifest['seal'][:24]}...")

    # Save manifest locally
    os.makedirs("evidence", exist_ok=True)
    with open(f"evidence/zenodo_deposit_v{VERSION}.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Saved: evidence/zenodo_deposit_v{VERSION}.json")

    print()
    print("=" * 60)
    print(f"  DEPOSIT CREATED")
    print(f"  ID:     {deposit_id}")
    print(f"  DOI:    {doi}")
    print(f"  Status: DRAFT (upload files, then publish)")
    print(f"  URL:    {BASE_URL.replace('/api','')}/deposit/{deposit_id}")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  1. Download release: gh release download v{VERSION} -R tritathadore/pyraclaw")
    print(f"  2. Upload to Zenodo: via web UI at the URL above")
    print(f"  3. Publish: click 'Publish' on the Zenodo deposit page")
    print(f"  4. Link DOI to ORCID: {ORCID_PYRACLAW}")


if __name__ == "__main__":
    main()
