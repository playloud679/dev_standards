#!/usr/bin/env python3
"""
Sync Standards Utility
Synchronizes GOLDEN_STD.md and development standards across repositories.
"""

import argparse
import os
import re
import sys
import urllib.request
from pathlib import Path

CANONICAL_RAW_BASE = "https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main"


def get_version_from_content(text: str) -> str | None:
    match = re.search(r"Specification Version:?[*\s`]*([0-9]+\.[0-9]+\.[0-9]+)", text)
    if match:
        return match.group(1)
    return None


def fetch_remote_version() -> tuple[str | None, str | None]:
    try:
        url = f"{CANONICAL_RAW_BASE}/VERSION"
        req = urllib.request.Request(url, headers={"User-Agent": "dev_standards_sync/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            version = resp.read().decode("utf-8").strip()
            return version, None
    except Exception as exc:
        return None, str(exc)


def fetch_remote_golden_std() -> tuple[str | None, str | None]:
    try:
        url = f"{CANONICAL_RAW_BASE}/GOLDEN_STD.md"
        req = urllib.request.Request(url, headers={"User-Agent": "dev_standards_sync/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8")
            return content, None
    except Exception as exc:
        return None, str(exc)


def main():
    parser = argparse.ArgumentParser(description="Synchronize GOLDEN_STD.md across projects.")
    parser.add_argument("--check", action="store_true", help="Check if local GOLDEN_STD.md is up to date")
    parser.add_argument("--target", type=str, default=".", help="Target directory (default: current directory)")
    parser.add_argument("--force", action="store_true", help="Overwrite local GOLDEN_STD.md without asking")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    target_file = target_dir / "GOLDEN_STD.md"

    print(f"Target path: {target_file}")

    local_version = None
    if target_file.exists():
        content = target_file.read_text(encoding="utf-8")
        local_version = get_version_from_content(content)
        print(f"Local version: {local_version or 'unknown'}")
    else:
        print("Local GOLDEN_STD.md not found.")

    print("Checking canonical repository...")
    remote_version, err = fetch_remote_version()
    if err:
        print(f"Note: could not fetch remote version from GitHub ({err}).")
        local_canonical = Path(__file__).resolve().parent.parent / "GOLDEN_STD.md"
        if local_canonical.exists():
            print("Using local canonical dev_standards specification...")
            content = local_canonical.read_text(encoding="utf-8")
            remote_version = get_version_from_content(content)
        else:
            sys.exit(1)
    else:
        print(f"Remote canonical version: {remote_version}")

    if args.check:
        if local_version == remote_version:
            print("Status: UP TO DATE")
            sys.exit(0)
        else:
            print(f"Status: UPDATE AVAILABLE ({local_version} -> {remote_version})")
            sys.exit(2)

    # Sync
    if target_file.exists() and local_version == remote_version and not args.force:
        print("GOLDEN_STD.md is already up to date. Use --force to overwrite.")
        return

    # Get content to write
    local_canonical = Path(__file__).resolve().parent.parent / "GOLDEN_STD.md"
    if local_canonical.exists() and local_canonical != target_file:
        new_content = local_canonical.read_text(encoding="utf-8")
    else:
        new_content, err = fetch_remote_golden_std()
        if err or not new_content:
            print(f"Error: failed to download canonical GOLDEN_STD.md ({err})")
            sys.exit(1)

    target_file.write_text(new_content, encoding="utf-8")
    print(f"Successfully synchronized GOLDEN_STD.md (v{remote_version}) to {target_file}")


if __name__ == "__main__":
    main()
