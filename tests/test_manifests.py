"""JSON, paths, logo, and the files the marketplace checklist asks for."""

from __future__ import annotations

import re
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from PIL import Image

from pluginlib import ROOT, SKILLS, EXPECTED_SKILLS, load_json, mcp_config, plugin_manifest

PATH_FIELDS = ("logo", "rules", "skills", "agents", "commands", "hooks", "mcpServers")
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
EGRESS_HOSTS = (
    "query1.finance.yahoo.com",
    "api.coingecko.com",
    "api.twelvedata.com",
    "stooq.com",
)


def _validator(schema: dict):
    cls = validator_for(schema)
    cls.check_schema(schema)
    return cls(schema, format_checker=FormatChecker())


def _path_values(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        found = []
        for item in value:
            found.extend(_path_values(item))
        return found
    return []


def _is_safe_relative(value: str) -> bool:
    if value.startswith(("http://", "https://")):
        return True
    if value.startswith(("/", "\\")):
        return False
    parts = Path(value).parts
    return ".." not in parts and value not in {"..", ""}


def test_plugin_manifest_matches_cursor_schema():
    schema = load_json(ROOT / "tests" / "fixtures" / "plugin.schema.json")
    manifest = plugin_manifest()
    _validator(schema).validate(manifest)
    assert manifest["name"] == "capybucks"
    assert NAME_RE.fullmatch(manifest["name"])
    assert manifest["displayName"] == "Capybucks"
    assert manifest["version"] == "0.1.0"
    assert manifest["license"] == "MIT"
    assert manifest["author"] == {
        "name": "Ricardo Margalho",
        "email": "ricardo@penarede.com.br",
    }
    assert manifest["category"] == "integrations"
    assert "real-time" not in manifest["description"].lower()
    assert "real time" not in manifest["description"].lower()
    assert "Not investment advice" in manifest["description"]


def test_manifest_paths_are_relative_and_exist():
    manifest = plugin_manifest()
    for field in PATH_FIELDS:
        if field not in manifest:
            continue
        for value in _path_values(manifest[field]):
            assert _is_safe_relative(value), value
            if value.startswith(("http://", "https://")):
                continue
            resolved = (ROOT / value).resolve()
            assert resolved.is_relative_to(ROOT.resolve())
            assert resolved.exists(), value

    assert (ROOT / manifest["skills"]).is_dir()
    mcp_path = (ROOT / manifest["mcpServers"]).resolve()
    assert mcp_path.name == "mcp.json"
    assert mcp_path.is_file()


def test_mcp_json_matches_agent_plugins_schema_and_pins_exact_version():
    schema = load_json(ROOT / "tests" / "fixtures" / "mcp.schema.json")
    config = mcp_config()
    _validator(schema).validate(config)
    server = config["mcpServers"]["capybucks"]
    assert server["type"] == "stdio"
    assert server["command"] == "uvx"
    assert server["args"] == ["capybucks-mcp==0.1.0"]
    assert re.fullmatch(r"capybucks-mcp==\d+\.\d+\.\d+", server["args"][0])


def test_logo_is_a_512px_image_under_100kb():
    logo = ROOT / plugin_manifest()["logo"]
    assert logo.is_file()
    assert logo.stat().st_size < 100 * 1024
    with Image.open(logo) as image:
        assert image.size == (512, 512)


def test_eight_skills_and_checklist_files():
    found = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())
    assert tuple(found) == tuple(sorted(EXPECTED_SKILLS))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "uv" in readme
    assert "capybucks-mcp==0.1.0" in readme
    for host in EGRESS_HOSTS:
        assert host in readme
    assert "not licensed for redistribution" in " ".join(license_text.split())
    assert "ricardo@penarede.com.br" in security
    assert (ROOT / "SUBMISSION.md").is_file()
    assert (ROOT / "CHANGELOG.md").is_file()
