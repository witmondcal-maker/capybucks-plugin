"""Manual check: the version pinned in mcp.json is published on PyPI.

Default CI skips this module (`pytest -m 'not pypi'`). Run it from the
workflow_dispatch job, or locally with `pytest -m pypi -o addopts=`.
capybucks-mcp 0.1.0 is published from the sibling repository; until that
release exists this test fails with the PyPI status, which is expected.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

import pytest

from pluginlib import mcp_config

pytestmark = pytest.mark.pypi


def test_pinned_capybucks_mcp_exists_on_pypi():
    pin = mcp_config()["mcpServers"]["capybucks"]["args"][0]
    version = pin.removeprefix("capybucks-mcp==")
    url = f"https://pypi.org/pypi/capybucks-mcp/{version}/json"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        pytest.fail(f"{url} returned HTTP {exc.code}. Publish capybucks-mcp=={version} before marketplace submission.")
    assert payload["info"]["version"] == version
