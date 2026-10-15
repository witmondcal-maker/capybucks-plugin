# Privacidade / Privacy

Conferido no código em 2026-10-15. Servidor: `witmondcal-maker/capybucks-mcp`, commit `d6368277b847dd7dc0c96c07544837f23bcc9c77`, branch `cursor/capybucks-mcp-server-04c5`. Biblioteca: `witmondcal-maker/capybucks`, branch `main`, nesse dia.

Checked against the code on 2026-10-15. Server: `witmondcal-maker/capybucks-mcp` commit `d6368277b847dd7dc0c96c07544837f23bcc9c77` on branch `cursor/capybucks-mcp-server-04c5`. Library: `witmondcal-maker/capybucks` `main` the same day.

## Português

O plugin Capybucks e o servidor MCP `capybucks-mcp` não coletam, não armazenam e não enviam dado pessoal ao autor.

Eles só consultam provedores públicos de dados de mercado: Yahoo Finance (`query1.finance.yahoo.com`), CoinGecko (`api.coingecko.com`), Twelve Data (`api.twelvedata.com`) e Stooq (`stooq.com`). Esses quatro hosts são os que o código do servidor (`ALLOWED_HOSTS` em `config.py`) e da biblioteca chamam. A busca de notícias da Yahoo usa o mesmo host `query1.finance.yahoo.com` (`/v1/finance/search`). O servidor não abre o websocket de stream da Twelve Data. A ferramenta `check_trading_day` usa o calendário local da dependência `exchange_calendars` e não acrescenta host.

A chave de API, quando o provedor pede uma, é a chave do próprio usuário. Neste servidor isso vale para a Twelve Data. A resolução está em `capybucks.core.config.get_api_key`: primeiro a variável de ambiente `CAPYBUCKS_TWELVEDATA_KEY`, depois o arquivo local `~/.capybucks.toml`, tabela `[keys]`, chave `twelvedata`. O repositório do plugin guarda só o placeholder `${CAPYBUCKS_TWELVEDATA_KEY}`. O servidor roda na máquina do usuário (`uvx`, stdio). O dado consultado sai do computador do usuário direto para o provedor e fica sujeito à política desse provedor.

O servidor é somente leitura. As ferramentas declaram `readOnlyHint` verdadeiro e `destructiveHint` falso (`server.py`). Ele não envia ordens e não escreve em conta de corretora, banco ou custódia. A escrita local é o cache parquet em `~/.cache/capybucks` (ou `CAPYBUCKS_CACHE_DIR`).

Dado de mercado não é recomendação financeira. Cada resposta traz o campo `notice` com esse aviso.

Não há telemetria. A busca em `src/capybucks_mcp` no commit acima e em `src/capybucks` não achou cliente de telemetria, analytics ou envio de evento para o autor. O log do servidor vai para o stderr local.

Dúvidas sobre privacidade: dev@sofle.com.br.

## English

The Capybucks plugin and the `capybucks-mcp` server do not collect, store, or send personal data to the author.

They only query public market-data providers: Yahoo Finance (`query1.finance.yahoo.com`), CoinGecko (`api.coingecko.com`), Twelve Data (`api.twelvedata.com`), and Stooq (`stooq.com`). Those four hosts are the ones in the server (`ALLOWED_HOSTS` in `config.py`) and in the library. Yahoo news uses the same `query1.finance.yahoo.com` host (`/v1/finance/search`). The server does not open the Twelve Data streaming websocket. `check_trading_day` uses the local `exchange_calendars` data shipped with the dependency and does not add a host.

When a provider needs an API key, the key belongs to the user. On this server that is Twelve Data. Resolution is `capybucks.core.config.get_api_key`: the environment variable `CAPYBUCKS_TWELVEDATA_KEY` first, then the local file `~/.capybucks.toml`, table `[keys]`, key `twelvedata`. This plugin repository stores only the `${CAPYBUCKS_TWELVEDATA_KEY}` placeholder. The server runs on the user's machine (`uvx`, stdio). Queried data goes from the user's computer straight to the provider and is subject to that provider's policy.

The server is read-only. Tools set `readOnlyHint` true and `destructiveHint` false (`server.py`). It does not place orders and does not write to a brokerage, bank, or custody account. The local write is the parquet cache at `~/.cache/capybucks` (or `CAPYBUCKS_CACHE_DIR`).

Market data is not investment advice. Every response includes a `notice` field that says so.

There is no telemetry. A search of `src/capybucks_mcp` at the commit above and of `src/capybucks` found no telemetry client, analytics SDK, or event upload to the author. Server logs go to local stderr.

Privacy questions: dev@sofle.com.br.
