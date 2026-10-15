"""Shared loaders for the capybucks plugin layout tests."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NOTICE_DESCRIPTION = (
    "may come from unofficial sources, is not investment advice, "
    "and that the server is read-only and does not place orders"
)
SHORT_NOTICE = "Informational data. May be delayed. Not investment advice. Read-only."

EXPECTED_SKILLS = (
    "capybucks-overview",
    "capybucks-price-history",
    "capybucks-fundamentals",
    "capybucks-options",
    "capybucks-indicators",
    "capybucks-b3-brazil",
    "capybucks-providers-and-keys",
    "capybucks-errors-and-limits",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plugin_manifest() -> dict:
    return load_json(ROOT / ".cursor-plugin" / "plugin.json")


def mcp_config() -> dict:
    return load_json(ROOT / "mcp.json")


def tool_names() -> set[str]:
    snapshot = load_json(ROOT / "tests" / "fixtures" / "tools.json")
    return {tool["name"] for tool in snapshot["tools"]}


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter not closed")
    loaded = yaml.safe_load(text[4:end])
    if not isinstance(loaded, dict):
        raise ValueError("frontmatter is not a mapping")
    return loaded, text[end + 5 :]
