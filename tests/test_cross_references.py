"""Skills and evals only name tools and skills that exist."""

from __future__ import annotations

import re

from pluginlib import EXPECTED_SKILLS, ROOT, SKILLS, load_json, tool_names

TOOL_RE = re.compile(r"`((?:get|list|compute|check)_[a-z0-9_]+)`")
SKILL_RE = re.compile(r"`(capybucks-[a-z0-9-]+)`")
KNOWN_SKILLS = set(EXPECTED_SKILLS)


def _skill_texts() -> list[tuple[str, str]]:
    texts = []
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        texts.append((path.parent.name, path.read_text(encoding="utf-8")))
        for extra in sorted(path.parent.rglob("*.md")):
            if extra.name == "SKILL.md":
                continue
            texts.append((path.parent.name, extra.read_text(encoding="utf-8")))
    return texts


def test_skill_citations_resolve():
    known_tools = tool_names()
    cited_tools: set[str] = set()
    for skill, text in _skill_texts():
        for match in TOOL_RE.findall(text):
            assert match in known_tools, f"{skill} cites unknown tool {match}"
            cited_tools.add(match)
        for match in SKILL_RE.findall(text):
            assert match in KNOWN_SKILLS, f"{skill} cites unknown skill {match}"
    assert cited_tools == known_tools


def test_evals_name_real_tools_and_skills():
    known_tools = tool_names()
    payload = load_json(ROOT / "evals" / "evals.json")
    cases = payload["cases"]
    assert len(cases) >= 20
    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids))
    for case in cases:
        assert case["skill"] in KNOWN_SKILLS
        tool = case["tool"]
        if tool is not None:
            assert tool in known_tools
        for extra in case.get("may_call", []):
            assert extra in known_tools
        if case.get("refuses_advice"):
            assert tool is None
