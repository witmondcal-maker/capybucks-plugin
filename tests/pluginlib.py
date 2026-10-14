"""Shared loaders for the capybucks plugin layout tests."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NOTICE_PT = (
    "Dados informativos, podem estar atrasados e vir de fontes não oficiais. "
    "Isto não é recomendação de investimento. O plugin é somente leitura e "
    "não executa ordens."
)
NOTICE_EN = "Informational data. May be delayed. Not investment advice. Read-only."

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
