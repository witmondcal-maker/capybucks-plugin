---
name: capybucks-price-history
description: >-
  Fetch OHLCV price history and delayed quotes with get_history and get_quote.
  Use when the user asks for historical prices, returns over a period, highs
  and lows, a comparison of symbols, or "histórico", "cotação histórica",
  "retorno em", "máxima", "mínima", or "cotação".
---

# Price history and quotes

Read `capybucks-overview` for the source defaults. Yahoo is unofficial and
delayed by about 15 minutes. Cite `provider`, `delayed`, and `asof` from the
symbol's own `provenance`. A batch keeps provenance per symbol.

## `get_history`

Parameters:

- `symbols`: one string or a list, at most 10. Required.
- `period`: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `max`, `ytd`. Default `1mo`. Ignored when `start` is set. Any other value is `invalid_argument`.
- `interval`: default `1d`. Yahoo accepts `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1w`, `1mo`. Twelve Data accepts `1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1wk`, `1w`, `1mo`. CoinGecko accepts `1d` and `1h`. Stooq accepts `1d`, `1wk`, `1w`, `1mo`. An unsupported interval is `provider_error`, not a resample.
- `start`, `end`: ISO 8601. A naive datetime is read as UTC. `end` defaults to now.
- `auto_adjust`: default `true`. On Yahoo, `close` is then the split-and-dividend adjusted close. Say that when you quote a return.
- `provider`: optional enum `yahoo`, `coingecko`, `stooq`, `twelvedata`.
- `view`: `rows` (default) or `summary`. Call `summary` first.
- `max_rows`: default 100, ceiling 500. The server keeps the most recent rows and reports `rows_total`, `rows_returned`, and `truncated`.
- `use_cache`: default `true`. The on-disk cache has no TTL. Pass `false` when the user needs a fresh download after a restatement.

`summary` returns `count`, `first_date`, `last_date`, `first_close`, `last_close`, `change_pct`, `high_max`, `low_min`, `avg_volume`, and the last 5 rows. The server computes those numbers from `close`. They are not a provider summary field.

Row objects use `date`, `open`, `high`, `low`, `close`, `adj_close`, `volume`. Prices are not rounded. For CoinGecko, `volume` is `null` and a warning says the source did not provide it. Do not treat that as zero.

Intraday windows are short. Ask for `period` `5d` with `interval` `1m`, not `max`.

Several symbols: `data.series` maps each symbol to its rows and its provenance. A partial failure sits in `data.errors`. Every symbol failing is `all_symbols_failed`. Do not compare a Yahoo series with a Stooq or Twelve Data series as if they were one adjusted history.

If the symbol contains `-` and `provider` is omitted, the server warns that the symbol is treated as crypto. For `BRK-B`, retry with `provider` `yahoo` after telling the user.

## `get_quote`

Parameters: `symbol`, optional `provider`.

Returns `symbol`, `price`, `timestamp`, `currency`, `delayed`, and `quote_kind`.

- `last_daily_bar`: Yahoo and CoinGecko. This is the last daily bar, not a live price.
- `provider_quote`: Twelve Data REST. `delayed` is still true. `timestamp` is when the call was made, not the trade time.

There is no streaming tool. Do not describe either quote as real time.

## Always say

- `provider`
- `delayed`
- `asof`

Portuguese notice:

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

English `notice` from the server:

> Informational data. May be delayed. Not investment advice. Read-only.
