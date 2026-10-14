---
name: capybucks-providers-and-keys
description: >-
  Choose a market-data provider and explain API keys without revealing
  secrets. Use when the user asks which source to use, mentions crypto, FX,
  Twelve Data, Stooq, CoinGecko, or Yahoo, or says "qual fonte", "preciso de
  chave", "API key", or "provedor".
---

# Providers and keys

Call `list_providers` before guessing what a source can do. It takes no
parameters. Each entry has `name`, `requires_key`, `key_configured`,
`default_for`, `supports`, `delayed`, and `notes`. `key_configured` is a
boolean. Never print, log, or ask the user to paste a key in the chat.

## Defaults and pins

| Provider | Key | Default for | Supports |
|---|---|---|---|
| `yahoo` | no | stocks | history, quote, statements, options, news, actions |
| `coingecko` | no | crypto | history, quote |
| `stooq` | no | nothing (pin only) | history |
| `twelvedata` | yes | nothing (pin only) | history, quote, statements, stream |

`provider` on every other tool is the enum `yahoo`, `coingecko`, `stooq`, `twelvedata`. An unknown name is `unknown_provider`.

Yahoo is the stock default because it needs no key. The endpoints are unofficial (`query1.finance.yahoo.com`), delayed by about 15 minutes, and Yahoo's terms restrict automated collection. `delayed` is true. Say that in the answer. Twelve Data is the paid path when the user wants a keyed feed. This plugin does not expose Twelve Data streaming. REST history and the REST quote stay `delayed: true`.

Stooq is daily CSV from `stooq.com` and often returns an HTML bot-check. That is `provider_error`, not a parsed table. Do not stitch a Stooq series onto a Yahoo series.

## Crypto and FX

CoinGecko maps ids for `BTC`, `ETH`, and `SOL` (and the `-USD` / `USD` forms). Any other crypto symbol is sent as `symbol.lower()` and often fails. Say that before calling for `DOGE`, `XRP`, or `ADA`. CoinGecko does not provide volume. `get_history` returns `volume: null` plus a warning. The public CoinGecko limit is tight (about one second between calls).

A symbol containing `-` is inferred as crypto. `BRK-B` needs `provider` `yahoo`.

`EUR/USD` and any `BASE/QUOTE` symbol have no default. Calling without `provider` returns `no_provider`. Retry only with `provider` `twelvedata` after the key is configured. Do not send FX to Yahoo.

## Where the key lives

Resolution order for Twelve Data:

1. Environment variable `CAPYBUCKS_TWELVEDATA_KEY` when it is non-empty.
2. `~/.capybucks.toml`, table `[keys]`, key `twelvedata`.

The plugin declares `CAPYBUCKS_TWELVEDATA_KEY` and forwards `${CAPYBUCKS_TWELVEDATA_KEY}` in `mcp.json`. The user sets it in the plugin configuration, not in the chat. An empty value or an unresolved `${CAPYBUCKS_TWELVEDATA_KEY}` placeholder is dropped at server start so the library can still read the toml file. A missing key is `missing_api_key` with `env_var` `CAPYBUCKS_TWELVEDATA_KEY`. Point the user at the plugin setting or the toml file. Do not ask them to paste the key.

`CAPYBUCKS_CACHE_DIR` overrides the parquet cache (`~/.cache/capybucks`). Do not set `CAPYBUCKS_NO_RATELIMIT`. That variable is for library tests.

Polygon is not implemented.

## Always say

- `provider`
- `delayed`
- `asof`

Portuguese notice:

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

English `notice` from the server:

> Informational data. May be delayed. Not investment advice. Read-only.
