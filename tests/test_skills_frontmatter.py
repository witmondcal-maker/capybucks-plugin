"""Skill frontmatter, length, and the bilingual trigger lines."""

from __future__ import annotations

from pluginlib import EXPECTED_SKILLS, NOTICE_EN, NOTICE_PT, SKILLS, split_frontmatter

PT_TRIGGERS = {
    "capybucks-overview": "histórico",
    "capybucks-price-history": "cotação",
    "capybucks-fundamentals": "balanço",
    "capybucks-options": "opções",
    "capybucks-indicators": "média móvel",
    "capybucks-b3-brazil": "PETR4",
    "capybucks-providers-and-keys": "qual fonte",
    "capybucks-errors-and-limits": "devo comprar",
}


def test_each_skill_has_name_description_and_notices():
    for name in EXPECTED_SKILLS:
        path = SKILLS / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) < 150, name
        meta, _body = split_frontmatter(text)
        assert meta["name"] == name
        description = meta["description"]
        assert isinstance(description, str) and description.strip()
        assert "use when" in description.lower()
        assert PT_TRIGGERS[name].lower() in description.lower()
        assert NOTICE_PT in text
        assert NOTICE_EN in text
        assert "`provider`" in text
        assert "`delayed`" in text
        assert "`asof`" in text
