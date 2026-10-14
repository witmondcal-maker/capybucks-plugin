---
name: capybucks-options
description: >-
  Fetch option expirations and an option chain with get_option_expirations
  and get_option_chain. Use when the user asks for options, strikes, calls,
  puts, or implied volatility, including "opções", "vencimentos", "calls",
  "puts", or "volatilidade implícita".
---

# Options

Only Yahoo implements options today. CoinGecko, Stooq, and Twelve Data
return `unsupported_capability`. Do not switch to another provider hoping
the chain appears. Prices, bids, asks, and implied volatility are delayed.
An option chain is not an order and not a recommendation to open or close
a position.

For the symbol rules, see `capybucks-overview`. For errors, see
`capybucks-errors-and-limits`.

## `get_option_expirations`

Parameters: `symbol`, optional `provider`.

Returns `expirations`, a list of `YYYY-MM-DD` dates. Call this first when the user did not name a date, then pass one date to `get_option_chain`.

## `get_option_chain`

Parameters:

- `symbol`: required.
- `expiration`: ISO date. Omit it to use the nearest expiration.
- `side`: `both` (default), `calls`, or `puts`.
- `near_money`: default `true`. The server makes an extra history call, same provider, for the last close and centers the strike window. That call is named in `warnings`. Pass the warning through. Set `near_money` to `false` when the user wants the unfiltered chain and then use `strike_min` and `strike_max`.
- `strike_min`, `strike_max`: optional numbers.
- `max_rows`: default 50 per side, ceiling 100.
- `provider`: optional. Use `yahoo` when you need to be explicit.

Each contract has `contract_symbol`, `strike`, `last_price`, `bid`, `ask`, `volume`, `open_interest`, `implied_volatility`, `in_the_money`. Rows are ordered by `strike`. The chain is truncated per side. Say when `truncated` is true.

The library does not attach a delay timestamp to the chain. Cite `provider` and say the delay was not reported as a timestamp. Do not call implied volatility a live quote.

If the user asks what to trade, stop at the figures and the notice. Do not rank contracts as a buy or a sell.

## Always say

- `provider`
- `delayed` (Yahoo options are delayed even when the envelope has no timestamp)
- `asof` when the envelope includes it

Portuguese notice:

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

English `notice` from the server:

> Informational data. May be delayed. Not investment advice. Read-only.
