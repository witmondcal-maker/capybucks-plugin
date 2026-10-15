"""Locks the 2026-10-15 review fixes against the MCP names we checked."""

from __future__ import annotations

from pluginlib import SKILLS

INDICATOR_COLUMNS = (
    "macd_signal",
    "macd_histogram",
    "bb_mid",
    "bb_upper",
    "bb_lower",
)


def _text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def test_indicator_columns_match_the_server_rename():
    text = _text("capybucks-indicators")
    for column in INDICATOR_COLUMNS:
        assert f"`{column}`" in text
    assert "Columns `macd`, `signal`, `histogram`" not in text
    assert "`mid`, `upper`, `lower`" not in text
    assert "Default `sma` and `rsi`" in text
    assert "Required." not in text.split("indicators")[1][:80]


def test_b3_suffix_does_not_wait_for_a_hint():
    text = _text("capybucks-b3-brazil")
    assert "before the first call" in text
    assert "no `details.hint`" in text
    assert "Only retry with `.SA` when `details.hint` is present" not in text
    overview = _text("capybucks-overview")
    assert "Do not wait for `details.hint`" in overview


def test_explicit_provider_interval_is_invalid_argument():
    history = _text("capybucks-price-history")
    assert "When `provider` is set, an interval outside that list is `invalid_argument`" in history
    errors = _text("capybucks-errors-and-limits")
    assert "only when `provider` was omitted" in errors


def test_unmapped_crypto_is_a_different_asset_not_a_failure():
    text = _text("capybucks-providers-and-keys")
    assert "often fails" not in text
    assert "HTTP 200" in text
    assert "no CoinGecko `id`" in text


def test_readme_and_submission_say_pypi_is_still_missing():
    from pluginlib import ROOT

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    submission = (ROOT / "SUBMISSION.md").read_text(encoding="utf-8")
    privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
    for blob in (readme, submission):
        assert "capybucks-mcp" in blob
        assert "PyPI" in blob
        assert "não está publicado" in blob or "It is not published" in blob
        assert "pypi-pin" in blob
        assert "Grok Bot" in blob
        assert "PRIVACY.md" in blob
    assert "dev@sofle.com.br" in privacy
    assert "não há telemetria" in privacy.lower() or "Não há telemetria" in privacy
    assert "There is no telemetry" in privacy
    assert "query1.finance.yahoo.com" in privacy
    assert "api.coingecko.com" in privacy
    assert "api.twelvedata.com" in privacy
    assert "stooq.com" in privacy
