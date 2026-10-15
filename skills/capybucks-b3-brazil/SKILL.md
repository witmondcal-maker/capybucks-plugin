---
name: capybucks-b3-brazil
description: >-
  Resolve Brazilian B3 tickers, the São Paulo timezone, and exchange
  sessions. Use when the user mentions B3, Brazil, pregão, "ações
  brasileiras", PETR4, VALE3, ITUB4, or a four-letter ticker plus a number
  and no .SA suffix.
---

# B3 and Brazil

Yahoo lists Brazilian spot shares as `{ticker}.SA`. A bare B3 ticker is four letters plus one or two digits, matching `^[A-Z]{4}\d{1,2}$` (`PETR4`, `VALE3`, `ITUB4`, `BOVA11`). Apply the `.SA` suffix yourself, before the first call. Do not wait for a hint from the server.

1. Tell the user the Yahoo symbol is `{ticker}.SA`.
2. Call the tool with that suffixed symbol on the first try.
3. If they already passed `.SA`, do not add another suffix.
4. A name outside that pattern is not this rule. Do not invent `.SA` for it.

A Yahoo HTTP 404 for the bare ticker arrives as `provider_error`. That error has no `details.hint`. The live Yahoo chart call does not raise `symbol_not_found` for `PETR4`. The suffix rule does not read `details.hint`.

`symbol_not_found` can still include `details.hint` when the library actually raises `SymbolNotFound`. For this pattern the hint is `{ticker}.SA`. That is not the Yahoo 404 path. If the field is present, tell the user and retry once with it. You do not need the field to apply the rule above. See `capybucks-errors-and-limits`.

## What the series looks like

For `PETR4.SA` and other `.SA` names, `currency` is `BRL` and the index timezone is `America/Sao_Paulo` when Yahoo sends that metadata (the parser falls back to `America/Sao_Paulo` if the zone is missing and the symbol ends in `.SA`). Quote those two fields with `provider`, `delayed`, and `asof`. The series is still the delayed unofficial Yahoo feed. See `capybucks-price-history`.

## `check_trading_day`

Parameters:

- `symbol`: required. `.SA` selects calendar `BVMF`. `.L` selects `XLON`. Anything else selects `XNYS`.
- `date`: optional ISO date. Default is today in the calendar's zone.
- `calendar`: optional `exchange_calendars` code, when the user names one.

Returns `calendar`, `date`, and `is_session`.

The tool answers whether that civil date is a session. It does not know the opening bell, the closing bell, or whether the market is open at this minute. If the user asks "a bolsa está aberta agora?" or "is the market open right now?", say the tool cannot answer the clock, and offer `is_session` for today's date instead.

`PETR4.SA` uses `BVMF`. Pass `calendar` `BVMF` when the user says B3 or Bovespa without a symbol you can suffix.

## Always say

- `provider`
- `delayed`
- `asof`

Every response carries a server `notice`. It says the data may be delayed, may come from unofficial sources, is not investment advice, and that the server is read-only and does not place orders. Repeat that content in the user's language. In Portuguese, say that the figures are informational, may be delayed, may come from unofficial sources, are not investment advice, and that the plugin is read-only and does not place orders.
