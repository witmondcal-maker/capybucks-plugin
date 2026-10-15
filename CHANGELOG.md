# Changelog

## 0.1.0

First marketplace plugin.

- Cursor manifest (`.cursor-plugin/plugin.json`) and stdio `mcp.json` pinned to `capybucks-mcp==0.1.0`.
- Eight skills: overview, price history, fundamentals, options, indicators, B3, providers and keys, errors and limits.
- Optional `CAPYBUCKS_TWELVEDATA_KEY`. Yahoo stays the default stock source, with an explicit delay warning.
- 512×512 logo derived from the library's `docs/assets/logo.jpg`.
- Layout tests for the manifest, skill frontmatter, variables, and cross-references.

The server package is built in `capybucks-mcp`. It was not on PyPI on 2026-10-15 (`https://pypi.org/pypi/capybucks-mcp/json` returned 404). This plugin does not vendor that code.
