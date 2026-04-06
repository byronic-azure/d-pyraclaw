# Multi-Account Multi-Repo Management Strategy

1. **Canonical source**: `tritathadore/pyraclaw main branch`
2. **Enterprise mirror**: `byronic-azure/pyraclaw synced via git subtree + GitHub Actions`
3. **Academic/IP protection**: `CallansInnovation/ruflo for iAiA components`
4. **Workshop integration**: `byronic-azure/ai-innovation-bridge for HF content`
5. **Anti-duplication rules**: `services/ is canonical, don't recreate elsewhere`
6. **Sync workflow**: `on push to main: validate → generate QDP capsule → merge to mirrors with commit attestation`
7. **Issue linking**: `cross-repo issues with evidence proof`
8. **Release process**: `tag on canonical, propagate to mirrors with CHANGELOG + ORCID`
9. **Access control matrix**: `ORCID 0009-0001-9561-5483 override on all repos`