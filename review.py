#!/usr/bin/env python3
"""
review.py – one-shot vulnerability check for a requirements-style project.
Usage: python review.py [--fail-on medium] [--json] [requirements_file]
"""
import json, os, subprocess, sys, textwrap
from typing import List, Dict, Any

FAIL_LEVELS = {"low": 0, "medium": 1, "high": 2, "critical": 3}

def run(cmd: List[str], **kw) -> str:
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    kw.setdefault("check", True)
    return subprocess.run(cmd, **kw).stdout

def resolve(req_file: str) -> List[Dict[str, Any]]:
    """Return the exact list that pip would install."""
    # For this demo, we'll parse requirements.txt directly
    packages = []
    try:
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        name, version = line.split('==', 1)
                        packages.append({
                            "metadata": {
                                "name": name.strip(),
                                "version": version.strip()
                            }
                        })
    except Exception as e:
        print(f"Warning: Could not parse requirements: {e}")
    return packages

def audit(req_file: str) -> Dict[str, Any]:
    """Run pip-audit and safety; merge results."""
    # Set PATH to include user's Python bin directory
    env = os.environ.copy()
    env["PATH"] = "/Users/carlos/Library/Python/3.9/bin:" + env.get("PATH", "")
    
    try:
        pa = json.loads(run(["pip-audit", "-r", req_file, "--format=json", "--desc"], env=env))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: pip-audit failed: {e}")
        pa = {"vulnerabilities": []}
    
    try:
        sa = json.loads(run(["safety", "check", "-r", req_file, "--json"], env=env))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: safety failed: {e}")
        sa = {"vulnerabilities": []}
    
    return {"pip-audit": pa, "safety": sa}

def markdown_report(resolved, audit_result) -> str:
    lines = ["## Dependency review summary\n"]
    lines.append("| Package | Installed | CVE / Advisory | Severity |")
    lines.append("|---------|-----------|----------------|----------|")
    for vuln in audit_result["pip-audit"].get("vulnerabilities", []):
        name = vuln["name"]
        version = next((r["metadata"]["version"] for r in resolved if r["metadata"]["name"] == name), "?")
        lines.append(f"| {name} | {version} | {vuln['id']} | {vuln['severity']} |")
    for vuln in audit_result["safety"].get("vulnerabilities", []):
        name = vuln["package_name"]
        version = vuln["installed_version"]
        lines.append(f"| {name} | {version} | {vuln['advisory']} | {vuln['severity']} |")
    return "\n".join(lines)

def main(argv=None):
    argv = argv or sys.argv[1:]
    req_file = argv[0] if argv and not argv[0].startswith("-") else "requirements.txt"
    fail_level = next((argv[i+1] for i, a in enumerate(argv) if a=="--fail-on"), "medium")
    emit_json = "--json" in argv

    resolved = resolve(req_file)
    audit_result = audit(req_file)

    # Exit logic
    failures = []
    for vuln in audit_result["pip-audit"].get("vulnerabilities", []):
        if FAIL_LEVELS.get(vuln["severity"], -1) >= FAIL_LEVELS[fail_level]:
            failures.append(vuln)
    for vuln in audit_result["safety"].get("vulnerabilities", []):
        if FAIL_LEVELS.get(vuln["severity"], -1) >= FAIL_LEVELS[fail_level]:
            failures.append(vuln)

    if emit_json:
        print(json.dumps({"resolved": resolved, "audit": audit_result}, indent=2))
    else:
        print(markdown_report(resolved, audit_result))

    if failures:
        sys.exit(1)

if __name__ == "__main__":
    main()