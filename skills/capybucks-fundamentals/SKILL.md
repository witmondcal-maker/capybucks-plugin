---
name: capybucks-fundamentals
description: >-
  Fetch financial statements, dividends, and splits with get_financials and
  get_dividends_and_splits. Use when the user asks for revenue, earnings,
  balance sheet, cash flow, dividends, or splits, including "receita",
  "lucro", "balanço", "fluxo de caixa", "dividendos", or "desdobramento".
---

# Fundamentals

Statements, dividends, and splits use the same provider as the symbol's
default, or the `provider` you pass. Yahoo implements statements, dividends,
and splits. Twelve Data implements statements. CoinGecko and Stooq return
`unsupported_capability` for these tools. Dividends and splits on Twelve Data
also return `unsupported_capability`. Switch provider only when the user asks.
See `capybucks-providers-and-keys` and `capybucks-errors-and-limits`.

The library does not attach `delayed` or `asof` to statements. The envelope
still carries `provider`. Repeat the warning that delay was not reported by
the source. Do not present the table as a live or audited filing.

## `get_financials`

Parameters:

- `symbol`: required. Brazilian spot names need `.SA`. See `capybucks-b3-brazil`.
- `statement`: `income` (default), `balance`, or `cashflow`.
- `frequency`: `annual` (default) or `quarterly`.
- `provider`: optional.
- `items`: optional list of line-item names. Matching ignores case. Pass it so the answer stays small.
- `max_periods`: default 4. The server keeps at most 8 periods and 60 items.

Map the words the user used: revenue or earnings to `income`, balance sheet or "balanço" to `balance`, cash flow or "fluxo de caixa" to `cashflow`. "Trimestral" is `quarterly`.

Return shape: `statement`, `frequency`, `periods` (ISO dates or `null`), `items` (name to a list aligned with `periods`). Names stay as the source published them. Yahoo uses names like `totalRevenue`. Twelve Data uses names like `revenue`. Do not treat those strings as the same line. Dropped all-null items are already removed.

An empty statement is an error, not a table of zeros.

## `get_dividends_and_splits`

Parameters:

- `symbol`: required.
- `kind`: `both` (default), `dividends`, or `splits`.
- `since`: optional ISO date. Events before it are omitted.
- `max_rows`: default 100, ceiling 500.
- `provider`: optional.

Returns `dividends` as `{date, amount}` and `splits` as `{date, ratio}`. `ratio` is numerator over denominator: `4.0` is a 4-for-1 split. No events returns empty lists and `ok: true`. That is success. Say that the symbol had no matching events in the window.

## Always say

- `provider`
- `delayed` when provenance includes it; otherwise say the source did not report delay
- `asof` when provenance includes it

Every response carries a server `notice`. It says the data may be delayed, may come from unofficial sources, is not investment advice, and that the server is read-only and does not place orders. Repeat that content in the user's language. In Portuguese, say that the figures are informational, may be delayed, may come from unofficial sources, are not investment advice, and that the plugin is read-only and does not place orders.
