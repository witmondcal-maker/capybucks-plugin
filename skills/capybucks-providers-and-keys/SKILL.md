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

CoinGecko maps ids for `BTC`, `ETH`, and `SOL`, plus `BTC-USD`, `BTCUSD`, `ETH-USD`, `ETHUSD`, and `SOL-USD`. `SOLUSD` is not mapped. Any other crypto symbol is sent as `symbol.lower()` to `/coins/{id}/ohlc`. CoinGecko often answers HTTP 200 with a different coin. On 2026-10-14 the server notes record that `doge` returned a price on the order of 4.6e-5, while `dogecoin` was about 0.084. The tool payload has no CoinGecko `id` and no coin `name`. `data.symbol` on `get_quote` is the ticker you sent, uppercased. That echo is not the resolved asset. When the unmapped-id warning is present, tell the user the series may be a different coin and do not present the price as the coin they named. Pass the warning through. Say this before calling for `DOGE`, `XRP`, or `ADA`. CoinGecko does not provide volume. `get_history` returns `volume: null` plus a warning. The public CoinGecko limit is tight (about one second between calls).

A symbol containing `-` is inferred as crypto. `BRK-B` needs `provider` `yahoo`.

The server refuses `/`, `..`, `?`, `#`, spaces, and control characters in a symbol. That is `invalid_argument`. `EUR/USD` contains `/`, so do not send it and do not invent another spelling. Tell the user the server will not accept the slash. A symbol the server still classifies as FX, called without `provider`, returns `no_provider`. FX has no default. Twelve Data is the FX provider and needs the key. Do not send FX to Yahoo.

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

Every response carries a server `notice`. It says the data may be delayed, may come from unofficial sources, is not investment advice, and that the server is read-only and does not place orders. Repeat that content in the user's language. In Portuguese, say that the figures are informational, may be delayed, may come from unofficial sources, are not investment advice, and that the plugin is read-only and does not place orders.
