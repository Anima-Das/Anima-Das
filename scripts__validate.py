#!/usr/bin/env python3
"""Validate the flat-upload README package, SVGs, workflow templates and Python sources."""
import re
import sys
import xml.dom.minidom
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent
errors, notes = [], []
def err(msg): errors.append(msg)

readme_path = ROOT / "README.md"
if not readme_path.is_file():
    err("README.md is missing")
    readme = ""
else:
    readme = readme_path.read_text(encoding="utf-8")

for bad in ("<script", "<iframe", "<object", "<embed", "javascript:"):
    if bad in readme.lower(): err(f"README contains unsupported markup: {bad}")

refs = set(re.findall(r'(?:src|srcset)="([^"]+)"', readme))
refs |= set(re.findall(r'!\[[^\]]*\]\(([^)\s]+)', readme))
local, external = [], []
for ref in sorted(refs):
    if ref.startswith(("http://", "https://", "mailto:", "#")):
        external.append(ref)
    else:
        local.append(ref)
for ref in local:
    if not (ROOT / ref).is_file(): err(f"README references a missing file: {ref}")
for ref in external:
    if ref.startswith("http://"): err(f"README uses insecure http: {ref}")

for m in re.finditer(r"<img\b[^>]*>", readme):
    if "alt=" not in m.group(0): err("An <img> in README has no alt attribute: " + m.group(0)[:80])

svgs = sorted(ROOT.glob("*.svg"))
for f in svgs:
    text = f.read_text(encoding="utf-8")
    try: xml.dom.minidom.parseString(text)
    except Exception as exc: err(f"{f.name}: invalid XML ({exc})"); continue
    low = text.lower()
    for bad in ("<script", "<foreignobject", "@import", "javascript:", "onload=", "onclick="):
        if bad in low: err(f"{f.name}: contains {bad}")
    if re.search(r'(?:href|src)="https?://', text) or "url(http" in low:
        err(f"{f.name}: references an external resource")
    if len(text.encode()) > 1_000_000: err(f"{f.name}: larger than 1 MB")

workflow_files = sorted(ROOT.glob("workflow__*.yml")) + sorted(ROOT.glob("workflow__*.yaml"))
if not workflow_files:
    err("No workflow__*.yml templates found")
for f in workflow_files:
    if yaml is None:
        notes.append("PyYAML not installed; workflow templates not parsed")
        break
    try: doc = yaml.safe_load(f.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc: err(f"{f.name}: invalid YAML ({exc})"); continue
    if not isinstance(doc, dict) or "jobs" not in doc or not ("on" in doc or True in doc):
        err(f"{f.name}: needs 'on' and 'jobs'"); continue
    for name, job in doc["jobs"].items():
        if "runs-on" not in job or not job.get("steps"): err(f"{f.name}: job '{name}' needs runs-on and steps")
        for step in job.get("steps", []):
            use = step.get("uses")
            if use and "@" not in use: err(f"{f.name}: action '{use}' is not pinned to a version")
            if not use and not step.get("run"): err(f"{f.name}: a step in '{name}' has neither uses nor run")

python_files = sorted(ROOT.glob("scripts__*.py")) + sorted(ROOT.glob("design_source__*.py"))
for f in python_files:
    try: compile(f.read_text(encoding="utf-8"), str(f), "exec")
    except SyntaxError as exc: err(f"{f.name}: {exc}")

print(f"README: {len(local)} local and {len(external)} external references")
print(f"SVG files checked: {len(svgs)}")
print(f"Workflow templates checked: {len(workflow_files)}")
if notes:
    for n in notes: print("note:", n)
if errors:
    print("\nFAILED")
    for e in errors: print(" -", e)
    sys.exit(1)
print("OK: flat package checks passed")
