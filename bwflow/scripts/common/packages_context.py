#!/usr/bin/env python3
"""
Package discovery and context output.

Provides:
    get_packages_info           - Get structured package info
    get_context_packages_text   - Full packages text output (--mode packages)
    get_context_packages_json   - Full packages JSON output (--mode packages --json)
"""

from __future__ import annotations

import re
from pathlib import Path

from .paths import (
    DIR_SPEC,
    DIR_WORKFLOW,
    get_repo_root,
)


# =============================================================================
# Internal Helpers
# =============================================================================

def _scan_spec_layers(spec_dir: Path) -> list[str]:
    """Scan spec directory for available layers (subdirectories).

    Returns:
        List of layer names (e.g., ['backend', 'frontend', 'guides']).
    """
    if not spec_dir.is_dir():
        return []
    return sorted(
        d.name for d in spec_dir.iterdir() if d.is_dir()
    )


def _parse_guidelines_from_index(index_file: Path) -> list[dict]:
    """Parse guidelines table from index.md.

    Args:
        index_file: Path to index.md file.

    Returns:
        List of dicts with keys: name, file, description.
    """
    guidelines = []
    
    try:
        content = index_file.read_text(encoding="utf-8")
        in_table = False

        for line in content.splitlines():
            if "| Guide |" in line or "| File |" in line:
                in_table = True
                continue
            
            if in_table and line.startswith("|"):
                if "---" in line:
                    continue
                
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    guide_link = parts[1]
                    description = parts[2] if len(parts) > 2 else ""

                    match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", guide_link)
                    if match:
                        guide_name = match.group(1)
                        guide_file = match.group(2)
                        guidelines.append({
                            "name": guide_name,
                            "file": guide_file,
                            "description": description,
                        })
            elif in_table and not line.startswith("|"):
                break
    except (OSError, UnicodeDecodeError):
        pass

    return guidelines


# =============================================================================
# Public Functions
# =============================================================================

def get_packages_info(repo_root: Path | None = None) -> dict[str, dict]:
    """Get structured package info.

    Args:
        repo_root: Repository root path. Defaults to auto-detected.

    Returns:
        Dictionary mapping package name to package info.
        Package info contains: index, guidelines.
    """
    if repo_root is None:
        repo_root = get_repo_root()

    spec_dir = repo_root / DIR_WORKFLOW / DIR_SPEC
    packages = {}

    if not spec_dir.is_dir():
        return packages

    for package_dir in sorted(spec_dir.iterdir()):
        if not package_dir.is_dir():
            continue

        package_name = package_dir.name
        index_file = package_dir / "index.md"

        if not index_file.is_file():
            continue

        guidelines = _parse_guidelines_from_index(index_file)

        packages[package_name] = {
            "index": f"{DIR_WORKFLOW}/{DIR_SPEC}/{package_name}/index.md",
            "guidelines": guidelines,
        }

    return packages


def get_context_packages_text(repo_root: Path | None = None) -> str:
    """Get packages context as formatted text (for --mode packages).

    Args:
        repo_root: Repository root path. Defaults to auto-detected.

    Returns:
        Formatted text output.
    """
    if repo_root is None:
        repo_root = get_repo_root()

    packages = get_packages_info(repo_root)

    lines = []
    lines.append("========================================")
    lines.append("AVAILABLE PACKAGES AND SPEC LAYERS")
    lines.append("========================================")
    lines.append("")

    if not packages:
        lines.append("No spec packages found in bwflow/spec/")
        lines.append("")
        lines.append("Expected structure:")
        lines.append("  bwflow/spec/")
        lines.append("    backend/index.md")
        lines.append("    frontend/index.md")
        lines.append("    guides/index.md")
        return "\n".join(lines)

    for package_name, info in packages.items():
        lines.append(f"## {package_name.upper()}")
        lines.append(f"Index: {info['index']}")
        lines.append("")

        if info["guidelines"]:
            lines.append("Guidelines:")
            for guide in info["guidelines"]:
                guide_path = f"{DIR_WORKFLOW}/{DIR_SPEC}/{package_name}/{guide['file']}"
                lines.append(f"  - {guide['name']}: {guide_path}")
                if guide["description"]:
                    lines.append(f"    {guide['description']}")
        else:
            lines.append("(No guidelines found)")

        lines.append("")

    lines.append("========================================")
    lines.append("USAGE")
    lines.append("========================================")
    lines.append("")
    lines.append("Read the index file first to understand the package:")
    lines.append(f"  cat {DIR_WORKFLOW}/{DIR_SPEC}/<package>/index.md")
    lines.append("")
    lines.append("Then read specific guidelines as needed:")
    lines.append(f"  cat {DIR_WORKFLOW}/{DIR_SPEC}/<package>/<guideline>.md")
    lines.append("")

    return "\n".join(lines)


def get_context_packages_json(repo_root: Path | None = None) -> dict:
    """Get packages context as a dictionary (for --mode packages --json).

    Args:
        repo_root: Repository root path. Defaults to auto-detected.

    Returns:
        Dictionary with package information.
    """
    if repo_root is None:
        repo_root = get_repo_root()

    packages = get_packages_info(repo_root)

    if not packages:
        spec_dir = repo_root / DIR_WORKFLOW / DIR_SPEC
        layers = _scan_spec_layers(spec_dir)
        return {
            "mode": "single-repo",
            "specLayers": layers,
        }

    return {
        "mode": "packages",
        "packages": packages,
    }
