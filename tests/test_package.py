"""Packaging checks for the Narwal Cloud US build."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "narwal_cloud" / "manifest.json"


def test_manifest_identifies_us_build() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["name"] == "Narwal Cloud US (unofficial)"
    assert data["domain"] == "narwal_cloud"
    assert data["documentation"].endswith("archieprichard/narwhal-cloud")
