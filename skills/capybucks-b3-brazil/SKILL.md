---
name: capybucks-b3-brazil
description: >-
  Resolve Brazilian B3 tickers, the São Paulo timezone, and exchange
  sessions. Use when the user mentions B3, Brazil, pregão, "ações
  brasileiras", PETR4, VALE3, ITUB4, or a four-letter ticker plus a number
  and no .SA suffix.
---

# B3 and Brazil

Yahoo lists Brazilian spot shares as `{ticker}.SA`. `PETR4` and `VALE3`
are not valid Yahoo symbols. `download("PETR4")` raises `SymbolNotFound`
with `hint` `PETR4.SA`. The library does not append `.SA` by itself, and
neither should you on the first call.

When `get_history`, `get_quote`, or another tool returns `symbol_not_found`
and `details.hint` is set:

1. Tell the user the symbol failed and what the hint is.
2. Retry once with `symbol` or `symbols` set to that hint.
3. If they already passed `.SA`, do not invent a second suffix.

The hint pattern is `^[A-Z]{4}\d{1,2}$` (for example `PETR4`, `VALE3`, `ITUB4`, `BOVA11`). A name outside that pattern has no hint. See `capybucks-errors-and-limits`. A Yahoo HTTP 404 can arrive as `provider_error` instead of `symbol_not_found`. Only retry with `.SA` when `details.hint` is present.

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

Portuguese notice:

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

English `notice` from the server:

> Informational data. May be delayed. Not investment advice. Read-only.
