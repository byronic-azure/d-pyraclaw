"""
iAiA 2 Cyber Specialist — Claude API Security Tools
PyraClaw Sovereign AI Runtime | DD7 International GmbH
Patent: PCT/EP2025/080977 | ORCID: 0009-0003-9584-1741

Eight security tools exposed to Claude via @beta_tool decorators.
The tool_runner handles the agentic loop automatically — Claude calls
these tools during analysis and the SDK feeds results back until done.

COMPLEXITY, DECIPHERED. REALITY, REDEFINED.
"""

import hashlib
import json
import re
import time
from typing import Optional

from anthropic import beta_tool

# ── OWASP Top 10 (2021) Patterns ────────────────────────────────────────
OWASP_PATTERNS = {
    "A01:2021-Broken Access Control": [
        r"(?i)(admin|root|superuser)\s*=\s*(true|1|\"true\")",
        r"(?i)@app\.route.*methods.*without.*auth",
        r"(?i)os\.system\s*\(",
        r"(?i)subprocess\.(call|run|Popen)\s*\(",
    ],
    "A02:2021-Cryptographic Failures": [
        r"(?i)(md5|sha1)\s*\(",
        r"(?i)password\s*=\s*[\"'][^\"']+[\"']",
        r"(?i)(DES|RC4|Blowfish)",
        r"(?i)ssl\.PROTOCOL_TLSv1[^_23]",
    ],
    "A03:2021-Injection": [
        r"(?i)(execute|cursor\.execute)\s*\(\s*f[\"']",
        r"(?i)eval\s*\(",
        r"(?i)exec\s*\(",
        r"(?i)os\.popen\s*\(",
        r"(?i)__import__\s*\(",
        r'(?i)format\s*\(.*user|input|request',
    ],
    "A05:2021-Security Misconfiguration": [
        r"(?i)debug\s*=\s*(true|1|True)",
        r"(?i)CORS.*\*",
        r"(?i)allow_all|AllowAny",
        r"(?i)SECRET_KEY\s*=\s*[\"'][a-z]+[\"']",
    ],
    "A07:2021-XSS": [
        r"(?i)innerHTML\s*=",
        r"(?i)document\.write\s*\(",
        r"(?i)\|\s*safe\b",
        r"(?i)dangerouslySetInnerHTML",
    ],
    "A08:2021-Software and Data Integrity": [
        r"(?i)pickle\.loads?\s*\(",
        r"(?i)yaml\.load\s*\([^)]*\)(?!.*Loader)",
        r"(?i)marshal\.loads?\s*\(",
        r"(?i)deserialize\s*\(",
    ],
    "A09:2021-Security Logging Failures": [
        r"(?i)except.*pass\s*$",
        r"(?i)except.*:\s*$",
        r"(?i)logging\.disable",
    ],
    "A10:2021-SSRF": [
        r"(?i)requests?\.(get|post|put|delete)\s*\(\s*(f[\"']|.*\+|.*format)",
        r"(?i)urllib\.request\.urlopen\s*\(\s*(f[\"']|.*\+)",
        r"(?i)httpx?\.(get|post)\s*\(\s*(f[\"']|.*\+)",
    ],
}

# ── CWE References ───────────────────────────────────────────────────────
CWE_MAP = {
    "A01": ["CWE-200", "CWE-284", "CWE-285", "CWE-639"],
    "A02": ["CWE-259", "CWE-327", "CWE-328", "CWE-330"],
    "A03": ["CWE-20", "CWE-78", "CWE-79", "CWE-89", "CWE-94"],
    "A05": ["CWE-16", "CWE-611", "CWE-942"],
    "A07": ["CWE-79", "CWE-80"],
    "A08": ["CWE-502", "CWE-829"],
    "A09": ["CWE-117", "CWE-223", "CWE-532", "CWE-778"],
    "A10": ["CWE-918"],
}

# ── MITRE ATT&CK Technique Mappings ─────────────────────────────────────
MITRE_TECHNIQUES = {
    "initial_access": ["T1190", "T1133", "T1566", "T1078"],
    "execution": ["T1059", "T1203", "T1047"],
    "persistence": ["T1098", "T1136", "T1543"],
    "privilege_escalation": ["T1548", "T1134", "T1068"],
    "credential_access": ["T1110", "T1003", "T1552"],
    "lateral_movement": ["T1021", "T1080", "T1550"],
    "exfiltration": ["T1041", "T1048", "T1567"],
    "impact": ["T1485", "T1486", "T1490"],
}

# ── Weak Cipher List ─────────────────────────────────────────────────────
WEAK_CIPHERS = {
    "DES", "3DES", "RC2", "RC4", "Blowfish", "MD4", "MD5", "SHA1",
    "SSL_RSA_WITH_RC4_128_MD5", "TLS_RSA_WITH_RC4_128_SHA",
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA",
}


def _severity(count: int, critical: bool = False) -> str:
    if critical or count >= 5:
        return "CRITICAL"
    if count >= 3:
        return "HIGH"
    if count >= 1:
        return "MEDIUM"
    return "INFO"


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 1: Vulnerability Scanner
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def vuln_scan(code: str, language: str = "python") -> str:
    """Scan source code for OWASP Top 10 vulnerabilities and CWE patterns.

    Args:
        code: The source code to analyze for security vulnerabilities.
        language: The programming language of the code (python, javascript, go, rust, java, etc.).
    """
    findings = []
    total_issues = 0

    for owasp_id, patterns in OWASP_PATTERNS.items():
        matches = []
        for pattern in patterns:
            for i, line in enumerate(code.split("\n"), 1):
                if re.search(pattern, line):
                    matches.append({"line": i, "content": line.strip()[:120], "pattern": pattern})
        if matches:
            cat_key = owasp_id.split("-")[0].replace(":", "")
            cwes = CWE_MAP.get(cat_key, [])
            total_issues += len(matches)
            findings.append({
                "owasp": owasp_id,
                "cwes": cwes,
                "severity": _severity(len(matches), "Injection" in owasp_id or "Crypto" in owasp_id),
                "matches": matches[:10],
                "count": len(matches),
            })

    findings.sort(key=lambda f: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}[f["severity"]])

    return json.dumps({
        "scanner": "iAiA-2-vuln-scan",
        "language": language,
        "total_issues": total_issues,
        "categories_hit": len(findings),
        "findings": findings,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 2: Network Reconnaissance (Passive)
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def network_recon(target: str) -> str:
    """Perform passive network reconnaissance on a target domain or IP.
    Returns DNS records, WHOIS hints, certificate transparency data.
    This is passive-only — no active scanning or probing.

    Args:
        target: The domain name or IP address to investigate passively.
    """
    # Passive analysis — no actual network calls in the tool itself.
    # Claude uses this to structure its reconnaissance findings.
    return json.dumps({
        "scanner": "iAiA-2-passive-recon",
        "target": target,
        "note": "Passive reconnaissance results. No active probing performed.",
        "recommended_checks": [
            f"DNS lookup: dig {target} ANY",
            f"Certificate transparency: crt.sh/?q={target}",
            f"WHOIS: whois {target}",
            f"Subdomain enumeration: subfinder -d {target}",
            f"Historical records: web.archive.org/web/*/{target}",
            f"Shodan: shodan search hostname:{target}",
        ],
        "mitre_technique": "T1596 - Search Open Technical Databases",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 3: Cryptographic Audit
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def crypto_audit(code: str) -> str:
    """Audit source code for cryptographic implementation weaknesses.
    Checks for weak ciphers, poor key management, insecure random generation,
    deprecated TLS versions, and hardcoded secrets.

    Args:
        code: The source code to audit for cryptographic issues.
    """
    issues = []

    # Check for weak ciphers
    for cipher in WEAK_CIPHERS:
        if cipher.lower() in code.lower():
            issues.append({"type": "weak_cipher", "cipher": cipher, "severity": "HIGH",
                           "cwe": "CWE-327", "fix": f"Replace {cipher} with AES-256-GCM or ChaCha20-Poly1305"})

    # Check for insecure random
    insecure_random = [r"(?i)random\.random\(\)", r"(?i)Math\.random\(\)", r"(?i)rand\(\)"]
    for pattern in insecure_random:
        if re.search(pattern, code):
            issues.append({"type": "insecure_random", "severity": "HIGH",
                           "cwe": "CWE-330", "fix": "Use secrets module (Python) or crypto.getRandomValues (JS)"})

    # Check for hardcoded keys/secrets
    secret_patterns = [
        r"(?i)(api_key|secret_key|password|token)\s*=\s*[\"'][A-Za-z0-9+/=]{8,}[\"']",
        r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----",
        r"(?i)AKIA[0-9A-Z]{16}",  # AWS access key
    ]
    for pattern in secret_patterns:
        if re.search(pattern, code):
            issues.append({"type": "hardcoded_secret", "severity": "CRITICAL",
                           "cwe": "CWE-798", "fix": "Move secrets to environment variables or a secrets manager"})

    # Check for deprecated TLS
    tls_patterns = [r"(?i)TLSv1[^_23]", r"(?i)SSLv[23]", r"(?i)ssl\.PROTOCOL_TLS(?!v1_[23])"]
    for pattern in tls_patterns:
        if re.search(pattern, code):
            issues.append({"type": "deprecated_tls", "severity": "HIGH",
                           "cwe": "CWE-326", "fix": "Use TLS 1.2+ minimum. Prefer TLS 1.3."})

    issues.sort(key=lambda i: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[i["severity"]])

    return json.dumps({
        "scanner": "iAiA-2-crypto-audit",
        "total_issues": len(issues),
        "issues": issues,
        "recommendation": "All cryptographic operations should use AES-256-GCM, Ed25519/X25519, or ChaCha20-Poly1305. TLS 1.3 preferred.",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 4: Pentest Plan Generator
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def pentest_plan(scope: str, target_type: str = "web_application") -> str:
    """Generate a structured penetration testing plan following PTES methodology.
    For authorized engagements only.

    Args:
        scope: Description of the target scope and boundaries for the pentest.
        target_type: Type of target — web_application, api, network, mobile, cloud, iot.
    """
    phases = {
        "web_application": [
            {"phase": "1-Reconnaissance", "tasks": ["Subdomain enumeration", "Technology fingerprinting", "Directory bruteforce", "Parameter discovery"], "mitre": "T1595, T1596"},
            {"phase": "2-Scanning", "tasks": ["Port scanning", "Service version detection", "SSL/TLS audit", "WAF detection"], "mitre": "T1046"},
            {"phase": "3-Vulnerability Analysis", "tasks": ["OWASP Top 10 testing", "Business logic flaws", "Authentication bypass", "Session management"], "mitre": "T1190"},
            {"phase": "4-Exploitation", "tasks": ["SQL injection", "XSS (stored/reflected/DOM)", "SSRF", "File upload bypass", "Deserialization"], "mitre": "T1059, T1190"},
            {"phase": "5-Post-Exploitation", "tasks": ["Privilege escalation", "Data exfiltration paths", "Lateral movement", "Persistence mechanisms"], "mitre": "T1068, T1041"},
            {"phase": "6-Reporting", "tasks": ["Executive summary", "Technical findings", "Risk ratings (CVSS)", "Remediation roadmap", "QDP-sealed evidence"], "mitre": "N/A"},
        ],
        "api": [
            {"phase": "1-Discovery", "tasks": ["Endpoint enumeration", "OpenAPI/Swagger analysis", "Authentication mechanism review", "Rate limiting tests"], "mitre": "T1595"},
            {"phase": "2-Authentication", "tasks": ["Token analysis (JWT/OAuth)", "Brute force resistance", "Session fixation", "MFA bypass vectors"], "mitre": "T1078, T1110"},
            {"phase": "3-Authorization", "tasks": ["IDOR testing", "Privilege escalation", "Horizontal access", "Role manipulation"], "mitre": "T1548"},
            {"phase": "4-Input Validation", "tasks": ["Injection (SQL/NoSQL/GraphQL)", "Mass assignment", "Parameter tampering", "File upload"], "mitre": "T1190"},
            {"phase": "5-Business Logic", "tasks": ["Race conditions", "Price manipulation", "Workflow bypass", "Data exposure"], "mitre": "T1059"},
            {"phase": "6-Reporting", "tasks": ["API security scorecard", "OWASP API Top 10 mapping", "Remediation priority", "QDP-sealed evidence"], "mitre": "N/A"},
        ],
    }

    plan = phases.get(target_type, phases["web_application"])

    return json.dumps({
        "scanner": "iAiA-2-pentest-plan",
        "scope": scope,
        "target_type": target_type,
        "methodology": "PTES (Penetration Testing Execution Standard)",
        "phases": plan,
        "rules_of_engagement": [
            "Written authorization required before testing begins",
            "Testing window must be defined and agreed upon",
            "Critical findings reported immediately",
            "No denial-of-service or destructive testing without explicit approval",
            "All evidence QDP-sealed and delivered to evidence ledger",
        ],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 5: Incident Response
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def incident_response(incident_type: str, severity: str = "high") -> str:
    """Generate an incident response playbook for a given incident type and severity.

    Args:
        incident_type: Type of incident — data_breach, ransomware, phishing, insider_threat, ddos, supply_chain, credential_compromise.
        severity: Severity level — critical, high, medium, low.
    """
    playbooks = {
        "data_breach": {
            "immediate": ["Isolate affected systems", "Preserve forensic evidence", "Activate IR team", "Notify CISO/DPO"],
            "containment": ["Block exfiltration channels", "Revoke compromised credentials", "Enable enhanced logging", "Deploy network segmentation"],
            "eradication": ["Identify root cause", "Patch exploited vulnerability", "Remove attacker persistence", "Verify system integrity"],
            "recovery": ["Restore from clean backups", "Monitor for re-compromise", "Update detection rules", "Conduct lessons learned"],
            "compliance": ["GDPR 72-hour notification (if EU data)", "Notify affected individuals", "File regulatory reports", "Update risk register"],
        },
        "ransomware": {
            "immediate": ["Disconnect affected systems from network", "Do NOT pay ransom", "Preserve encrypted samples", "Contact law enforcement"],
            "containment": ["Identify patient zero", "Block C2 communications", "Isolate network segments", "Disable SMB/RDP where possible"],
            "eradication": ["Identify ransomware variant", "Check for decryption tools (nomoreransom.org)", "Remove malware artifacts", "Patch entry vector"],
            "recovery": ["Restore from offline backups", "Verify backup integrity before restore", "Rebuild if no clean backup", "Enhanced monitoring for 30 days"],
            "compliance": ["Report to relevant authorities", "Document timeline", "Update business continuity plan", "Review backup strategy"],
        },
    }

    playbook = playbooks.get(incident_type, playbooks.get("data_breach"))

    return json.dumps({
        "scanner": "iAiA-2-incident-response",
        "incident_type": incident_type,
        "severity": severity.upper(),
        "playbook": playbook,
        "mitre_mapping": MITRE_TECHNIQUES.get("exfiltration", []),
        "sla": {"critical": "15 min", "high": "1 hour", "medium": "4 hours", "low": "24 hours"}.get(severity.lower(), "1 hour"),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 6: Threat Modeling
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def threat_model(system_desc: str, methodology: str = "STRIDE") -> str:
    """Perform threat modeling on a system description using STRIDE or DREAD methodology.

    Args:
        system_desc: Description of the system architecture, components, data flows, and trust boundaries.
        methodology: Threat modeling methodology — STRIDE or DREAD.
    """
    stride_categories = {
        "Spoofing": {"desc": "Impersonating something or someone else", "mitre": "T1078, T1134", "controls": ["Multi-factor authentication", "Certificate pinning", "Token validation"]},
        "Tampering": {"desc": "Modifying data or code", "mitre": "T1565", "controls": ["Input validation", "Digital signatures", "Integrity monitoring"]},
        "Repudiation": {"desc": "Claiming to have not performed an action", "mitre": "T1070", "controls": ["Audit logging", "Digital signatures", "Timestamps", "QDP sealing"]},
        "Information Disclosure": {"desc": "Exposing information to unauthorized parties", "mitre": "T1005, T1039", "controls": ["Encryption at rest/transit", "Access controls", "Data classification"]},
        "Denial of Service": {"desc": "Deny or degrade service to users", "mitre": "T1498, T1499", "controls": ["Rate limiting", "CDN/WAF", "Auto-scaling", "Circuit breakers"]},
        "Elevation of Privilege": {"desc": "Gain capabilities without authorization", "mitre": "T1068, T1548", "controls": ["Least privilege", "RBAC", "Sandboxing", "Container isolation"]},
    }

    return json.dumps({
        "scanner": "iAiA-2-threat-model",
        "system": system_desc[:500],
        "methodology": methodology,
        "categories": stride_categories if methodology == "STRIDE" else {},
        "recommendation": "Map each component and data flow against all 6 STRIDE categories. Prioritize by risk = likelihood x impact.",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 7: Digital Forensics
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def forensics_analyze(artifact_type: str, data: str) -> str:
    """Analyze digital forensic artifacts — logs, network captures, file metadata, memory dumps.

    Args:
        artifact_type: Type of artifact — access_log, auth_log, network_capture, file_metadata, memory_dump, email_header.
        data: The raw artifact data to analyze (log entries, metadata, headers, etc.).
    """
    analysis = {
        "artifact_type": artifact_type,
        "data_size": len(data),
        "data_hash": hashlib.sha256(data.encode()).hexdigest()[:16],
    }

    # Artifact-specific indicators
    if artifact_type == "access_log":
        analysis["indicators"] = {
            "suspicious_status_codes": len(re.findall(r"\b(403|401|500|502)\b", data)),
            "sql_injection_attempts": len(re.findall(r"(?i)(union|select|drop|insert|update|delete|;--)", data)),
            "xss_attempts": len(re.findall(r"(?i)(<script|javascript:|onerror|onload)", data)),
            "directory_traversal": len(re.findall(r"\.\./|\.\.\\", data)),
            "scanner_signatures": len(re.findall(r"(?i)(nikto|sqlmap|nmap|burp|dirbuster|gobuster)", data)),
        }
    elif artifact_type == "auth_log":
        analysis["indicators"] = {
            "failed_logins": len(re.findall(r"(?i)(failed|failure|invalid|denied)", data)),
            "successful_logins": len(re.findall(r"(?i)(accepted|success|opened)", data)),
            "privilege_escalation": len(re.findall(r"(?i)(sudo|su |root|admin|SYSTEM)", data)),
            "brute_force_pattern": len(re.findall(r"(?i)failed.*failed.*failed", data)),
        }
    elif artifact_type == "email_header":
        analysis["indicators"] = {
            "spf_fail": bool(re.search(r"(?i)spf=(fail|softfail|neutral)", data)),
            "dkim_fail": bool(re.search(r"(?i)dkim=(fail|none)", data)),
            "dmarc_fail": bool(re.search(r"(?i)dmarc=(fail|none)", data)),
            "suspicious_sender": bool(re.search(r"(?i)(reply-to|return-path).*differs", data)),
            "encoding_tricks": bool(re.search(r"(?i)(base64|quoted-printable).*subject", data)),
        }
    else:
        analysis["indicators"] = {"raw_lines": len(data.split("\n")), "note": "Manual analysis recommended for this artifact type."}

    return json.dumps({
        "scanner": "iAiA-2-forensics",
        **analysis,
        "chain_of_custody": "Artifact hash recorded. QDP seal applied to analysis output.",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  TOOL 8: Social Engineering Simulation
# ═══════════════════════════════════════════════════════════════════════════

@beta_tool
def social_engineer_sim(scenario: str) -> str:
    """Design a social engineering awareness training simulation.
    For authorized security awareness training only — not for actual attacks.

    Args:
        scenario: The social engineering scenario to simulate — phishing_email, vishing, smishing, pretexting, tailgating, baiting.
    """
    templates = {
        "phishing_email": {
            "attack_vector": "Email-based social engineering",
            "mitre": "T1566.001 - Spearphishing Attachment / T1566.002 - Spearphishing Link",
            "training_elements": [
                "Urgency/fear tactics (account suspension, security alert)",
                "Authority impersonation (IT department, CEO, vendor)",
                "Link manipulation (lookalike domains, URL shorteners)",
                "Attachment lures (invoice, shipping notification, document)",
            ],
            "detection_indicators": [
                "Sender domain mismatch",
                "Generic greeting instead of personal name",
                "Hover-over reveals different URL than displayed",
                "Unexpected attachment from unknown sender",
                "Pressure to act immediately",
                "Grammar/spelling inconsistencies",
                "SPF/DKIM/DMARC failures in headers",
            ],
            "recommended_training": [
                "Monthly simulated phishing campaigns",
                "Click-rate tracking with targeted follow-up training",
                "Report button in email client",
                "Reward reporting, don't punish clicking",
            ],
        },
        "vishing": {
            "attack_vector": "Voice-based social engineering (phone calls)",
            "mitre": "T1566.004 - Spearphishing Voice",
            "training_elements": [
                "Caller ID spoofing",
                "Authority impersonation (bank, IT support, law enforcement)",
                "Urgency creation (your account has been compromised)",
                "Information gathering through seemingly innocent questions",
            ],
            "detection_indicators": [
                "Unsolicited call requesting sensitive information",
                "Caller refuses to provide callback number",
                "Pressure to stay on the line",
                "Requests for passwords, OTPs, or remote access",
            ],
            "recommended_training": [
                "Verification procedures for phone requests",
                "Call-back policy for sensitive operations",
                "Never share OTP/MFA codes by phone",
            ],
        },
    }

    template = templates.get(scenario, templates["phishing_email"])

    return json.dumps({
        "scanner": "iAiA-2-social-engineering-sim",
        "scenario": scenario,
        "purpose": "AUTHORIZED SECURITY AWARENESS TRAINING ONLY",
        **template,
        "legal_notice": "This simulation is for defensive training purposes only. Unauthorized use is prohibited.",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2)


# ── Tool Registry ────────────────────────────────────────────────────────
ALL_TOOLS = [
    vuln_scan,
    network_recon,
    crypto_audit,
    pentest_plan,
    incident_response,
    threat_model,
    forensics_analyze,
    social_engineer_sim,
]

# White hat gets defensive tools only
WHITE_HAT_TOOLS = [vuln_scan, crypto_audit, incident_response, threat_model, forensics_analyze]

# Grey hat adds research tools
GREY_HAT_TOOLS = [vuln_scan, network_recon, crypto_audit, incident_response, threat_model, forensics_analyze]

# Black hat gets the full arsenal
BLACK_HAT_TOOLS = ALL_TOOLS

TOOLS_BY_HAT = {
    "white": WHITE_HAT_TOOLS,
    "grey": GREY_HAT_TOOLS,
    "black": BLACK_HAT_TOOLS,
}
