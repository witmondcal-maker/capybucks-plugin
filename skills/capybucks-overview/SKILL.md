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
- Crypto uses CoinGecko: a symbol containing `-` or `USDT`, or the bare names `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, and `ADA`. Only `BTC`, `ETH`, and `SOL` have mapped CoinGecko ids. CoinGecko does not provide volume. See `capybucks-providers-and-keys`.
- FX (`EUR/USD`) has no default. It needs `provider` `twelvedata` and a key. See `capybucks-providers-and-keys`.
- A hyphen is classified as crypto. For `BRK-B`, pass `provider` `yahoo`.
- Brazilian spot tickers (`PETR4`, `VALE3`) need the `.SA` suffix. See `capybucks-b3-brazil`. Tell the user, then retry with the hint. Do not rewrite the symbol silently.

One series uses one provider. Do not stitch candles from two sources and present them as one history. Stooq and Twelve Data run only when the user pins `provider`.

`provider` is one of `yahoo`, `coingecko`, `stooq`, `twelvedata`.

## On every market-data answer

Take `provider`, `delayed`, and `asof` from `provenance`. Add `currency` and `timezone` when they are present. `delayed: true` means the figure is not a live print. Quotes from Yahoo and CoinGecko are the last daily bar (`quote_kind` `last_daily_bar`).

This plugin does not stream ticks, draw charts, export spreadsheets, or backtest. A question about bank balances is outside this plugin.

## Always say

- `provider`
- `delayed`
- `asof`

Portuguese notice:

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

English `notice` from the server:

> Informational data. May be delayed. Not investment advice. Read-only.
