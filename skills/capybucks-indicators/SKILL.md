---
name: capybucks-indicators
description: >-
  Compute SMA, EMA, RSI, MACD, Bollinger Bands, ATR, and VWAP with
  compute_indicators. Use when the user asks for those indicators or for
  "média móvel", "IFR", "RSI", "MACD", "Bandas de Bollinger", "ATR", or
  "VWAP".
---

# Indicators

`compute_indicators` downloads one series and runs textbook formulas from
`capybucks.ta`. The formulas are not a trading system. Do not turn a
reading into a buy or sell. See `capybucks-price-history` for the series
and `capybucks-errors-and-limits` for failures.

The server does not call `enrich`. That helper fixes RSI and ATR at 14 and
adds columns the user did not ask for. Pass only the indicators requested.

## `compute_indicators`

Parameters:

- `symbol`: required.
- `indicators`: optional list drawn from `sma`, `ema`, `rsi`, `macd`, `bollinger`, `atr`, `vwap`. Default `sma` and `rsi`.
- `period`: default `6mo`. Same period names as `get_history`.
- `interval`: default `1d`.
- `provider`: optional.
- `window`: default 20, allowed 2 to 400. Used by SMA, EMA, and Bollinger.
- `rsi_window`: default 14. `atr_window`: default 14.
- `macd_fast`: 12. `macd_slow`: 26. `macd_signal`: 9.
- `bands_std`: default 2.0.
- `last_n`: default 30, ceiling 200.

The return is columnar: `columns` and `rows`, the last `last_n` bars. Warmup rows are `null` until the window fills. Indicator values are rounded to 6 decimal places. The underlying closes are not rounded. If `period` is shorter than the warmup, the values stay `null` and `warnings` says so. Repeat that warning. Ask for a longer `period` rather than inventing numbers.

Formulas, matching the library:

- SMA: rolling mean, `min_periods` equal to the window.
- EMA: `span` equal to `window`, `adjust` false.
- RSI: Wilder smoothing, `alpha` = 1 / `rsi_window`.
- MACD: fast EMA minus slow EMA, then an EMA of that line. Columns `macd`, `macd_signal`, `macd_histogram`. The column `macd_signal` is the signal line. The parameter `macd_signal` above is the signal window (default 9).
- Bollinger: columns `bb_mid`, `bb_upper`, `bb_lower`, from the SMA plus or minus `bands_std` times the rolling standard deviation.
- ATR: true range, then Wilder smoothing with `atr_window`.
- VWAP: cumulative typical price `(high + low + close) / 3` weighted by volume.

CoinGecko volume is null, so VWAP on a CoinGecko series is not meaningful. Say so and skip VWAP unless the user pinned a provider that sends volume.

Cite the history `provenance` (`provider`, `delayed`, `asof`) with the indicator values. The indicator columns are computed locally from that series.

## Always say

- `provider`
- `delayed`
- `asof`

Every response carries a server `notice`. It says the data may be delayed, may come from unofficial sources, is not investment advice, and that the server is read-only and does not place orders. Repeat that content in the user's language. In Portuguese, say that the figures are informational, may be delayed, may come from unofficial sources, are not investment advice, and that the plugin is read-only and does not place orders.
