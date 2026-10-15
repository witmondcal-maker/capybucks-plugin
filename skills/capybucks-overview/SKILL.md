---
name: capybucks-overview
description: >-
  Route a market-data question to the right read-only Capybucks tool and
  cite provider, delay, and as-of time on the answer. Use when the user asks
  for a price, quote, history, financials, options, dividends, news, or
  indicators, including "preço de", "histórico", "cotação", "balanço",
  "opções", "dividendos", or "indicadores".
---

# Capybucks overview

Capybucks serves read-only market data through ten MCP tools. It does not
place orders, read brokerage accounts, or give investment advice. Yahoo
Finance is the default source for stocks. Those endpoints are unofficial and
the series is delayed by about 15 minutes. Say that whenever Yahoo is the
provider.

The plugin starts `uvx capybucks-mcp==0.1.0`. The machine needs `uv` on
`PATH`. If the server does not start, say so. The warm-up command is
`uvx capybucks-mcp==0.1.0 --version`. Do not invent prices.

## Pick a tool

| Question | Tool | Skill |
|---|---|---|
| History, return, high/low, compare symbols | `get_history` | `capybucks-price-history` |
| Latest quote | `get_quote` | `capybucks-price-history` |
| Income, balance sheet, cash flow | `get_financials` | `capybucks-fundamentals` |
| Dividends or splits | `get_dividends_and_splits` | `capybucks-fundamentals` |
| Option dates or chain, implied volatility | `get_option_expirations`, `get_option_chain` | `capybucks-options` |
| Headlines | `get_news` | `capybucks-errors-and-limits` |
| SMA, EMA, RSI, MACD, Bollinger, ATR, VWAP | `compute_indicators` | `capybucks-indicators` |
| Is this date a trading session? | `check_trading_day` | `capybucks-b3-brazil` |
| Which source, crypto, FX, API key | `list_providers` | `capybucks-providers-and-keys` |
| Any tool error, delay, or terms question | the error envelope | `capybucks-errors-and-limits` |

Call `get_history` with `view` `summary` before asking for rows.

## Symbols and defaults

- Stocks such as `AAPL` use Yahoo when `provider` is omitted.
- Crypto uses CoinGecko: a symbol containing `-` or ending in `USDT`, or the bare names `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, and `ADA`. Mapped ids are `BTC`, `ETH`, and `SOL` plus the forms in `capybucks-providers-and-keys`. Any other crypto id is the lowercased ticker, and CoinGecko can answer HTTP 200 with a different coin. CoinGecko does not provide volume.
- The server refuses a symbol that contains `/`, `..`, `?`, `#`, a space, or a control character (`invalid_argument`). Do not send `EUR/USD`. See `capybucks-providers-and-keys`.
- A hyphen is classified as crypto. For `BRK-B`, pass `provider` `yahoo`.
- Brazilian spot tickers (`PETR4`, `VALE3`: four letters plus a number) need the `.SA` suffix on the first call. Tell the user, then call `{ticker}.SA`. Do not wait for `details.hint`. Do not rewrite any other symbol silently. See `capybucks-b3-brazil`.

One series uses one provider. Do not stitch candles from two sources and present them as one history. Stooq and Twelve Data run only when the user pins `provider`.

`provider` is one of `yahoo`, `coingecko`, `stooq`, `twelvedata`.

## On every market-data answer

Take `provider`, `delayed`, and `asof` from `provenance`. Add `currency` and `timezone` when they are present. `delayed: true` means the figure is not a live print. Quotes from Yahoo and CoinGecko are the last daily bar (`quote_kind` `last_daily_bar`).

This plugin does not stream ticks, draw charts, export spreadsheets, or backtest. A question about bank balances is outside this plugin.

## Always say

- `provider`
- `delayed`
- `asof`

Every response carries a server `notice`. It says the data may be delayed, may come from unofficial sources, is not investment advice, and that the server is read-only and does not place orders. Repeat that content in the user's language. In Portuguese, say that the figures are informational, may be delayed, may come from unofficial sources, are not investment advice, and that the plugin is read-only and does not place orders.
