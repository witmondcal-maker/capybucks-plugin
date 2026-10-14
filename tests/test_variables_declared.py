"""Every ${VAR} in mcp.json is declared on the plugin manifest."""

from __future__ import annotations

import json
import re

from pluginlib import mcp_config, plugin_manifest

PLACEHOLDER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def test_mcp_placeholders_are_declared_and_not_required():
    raw = json.dumps(mcp_config())
    names = set(PLACEHOLDER.findall(raw))
    assert names == {"CAPYBUCKS_TWELVEDATA_KEY"}
    variables = plugin_manifest()["variables"]
    assert variables["type"] == "object"
    assert names <= set(variables["properties"])
    assert "required" not in variables
    key = variables["properties"]["CAPYBUCKS_TWELVEDATA_KEY"]
    assert key["type"] == "string"
    assert "optional" in key["title"].lower() or "optional" in key["description"].lower()


def test_log_level_is_a_literal_not_a_secret():
    env = mcp_config()["mcpServers"]["capybucks"]["env"]
    assert env["CAPYBUCKS_MCP_LOG_LEVEL"] == "WARNING"
    assert "KEY" not in env["CAPYBUCKS_MCP_LOG_LEVEL"]
