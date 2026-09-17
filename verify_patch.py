#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Check source hashes and apply the patch to temporary copies, not the source tree."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
manifest = json.loads((root / "SOURCE.json").read_text())
if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 verify_patch.py /path/to/backports-6.12.96")
source = Path(sys.argv[1]).resolve()
patch = root / manifest["patch"]
def digest(data):
    return hashlib.sha256(data).hexdigest()
if digest(patch.read_bytes()) != manifest["patch_sha256"]:
    raise SystemExit("Patch hash mismatch")
with tempfile.TemporaryDirectory(prefix="iwlwifi-source-check-") as tmp:
    scratch = Path(tmp)
    for name, expected in manifest["files"].items():
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts:
            raise SystemExit("Unsafe manifest path")
        data = (source / rel).read_bytes()
        if digest(data) != expected["baseline_sha256"]:
            raise SystemExit("Baseline hash mismatch: " + name)
        dest = scratch / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    for dry_run in (True, False):
        args = ["patch", "--batch", "-p1", "-i", str(patch)]
        if dry_run:
            args.append("--dry-run")
        subprocess.run(args, cwd=scratch, check=True)
    for name, expected in manifest["files"].items():
        actual = digest((scratch / name).read_bytes())
        if expected.get("patched_sha256") and actual != expected["patched_sha256"]:
            raise SystemExit("Patched source hash mismatch: " + name)
        print("Verified", name, actual)
print("Source/hash/patch checks passed. This is not a compile or device test.")
