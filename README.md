# Capybucks

Read-only market data for agents: price history, quotes, financial statements, options, dividends, news and technical indicators, with provider and delay shown on every answer. Not investment advice.

Plugin version **0.1.0** starts the stdio server `capybucks-mcp==0.1.0`. The server package lives in [capybucks-mcp](https://github.com/witmondcal-maker/capybucks-mcp). The library lives in [capybucks](https://github.com/witmondcal-maker/capybucks). This repository is the marketplace plugin: manifest, skills, and the `uvx` pin. It does not contain the Python server.

Yahoo Finance is the default source for stocks. Those endpoints are unofficial and delayed by about 15 minutes. Every answer should show `provider`, `delayed`, and `asof`.

## English

### What you get

Eight skills and one MCP server, `capybucks`, with ten read-only tools:

| Tool | Use |
|---|---|
| `list_providers` | Sources, capabilities, and whether a key is configured (never the key) |
| `get_history` | OHLCV history, one provider per series |
| `get_quote` | Latest quote (Yahoo and CoinGecko: last daily bar) |
| `get_financials` | Income, balance sheet, cash flow |
| `get_dividends_and_splits` | Dividends and split ratios |
| `get_option_expirations` | Option expiration dates |
| `get_option_chain` | Calls and puts for one expiration |
| `get_news` | Headlines, marked as untrusted text |
| `compute_indicators` | SMA, EMA, RSI, MACD, Bollinger, ATR, VWAP |
| `check_trading_day` | Whether a date is an exchange session |

There is no order entry, no brokerage login, and no streaming. This plugin is market data. It does not link bank, card, or custody accounts.

### Install

Prerequisite: [`uv`](https://docs.astral.sh/uv/) on `PATH`. The first `uvx` run downloads `capybucks-mcp` and its dependencies (`pandas`, `pyarrow`) and can take longer than a later start. Warm the cache before relying on the client timeout:

```bash
uvx capybucks-mcp==0.1.0 --version
```

Stocks (Yahoo) and crypto (CoinGecko) need no key. FX and the Twelve Data feed need `CAPYBUCKS_TWELVEDATA_KEY`, set in the plugin configuration (Plugins → Configure) or in `~/.capybucks.toml`:

```toml
[keys]
twelvedata = "paste-the-key-here"
```

Leave the plugin variable empty to keep the Yahoo and CoinGecko defaults. Do not commit the key. If `uv` is not available, the fallback is `pipx run capybucks-mcp==0.1.0` or `python -m capybucks_mcp` inside a virtualenv that has the pinned package. Those fallbacks are not what `mcp.json` runs.

### Local check

Copy this repository to `~/.cursor/plugins/local/capybucks` (a symlink counts only when the target stays inside that folder). Reload the window and open Customize. You should see eight skills and the `capybucks` MCP server. On Enterprise, an admin may have to allow local plugin imports.

### Network and disk

The server calls only these hosts:

- `query1.finance.yahoo.com`
- `api.coingecko.com`
- `api.twelvedata.com`
- `stooq.com`

The only local write is the library's parquet cache at `~/.cache/capybucks` (or `CAPYBUCKS_CACHE_DIR`). There is no telemetry.

### Legal

The software is MIT. The data is not. Yahoo's terms restrict automated collection. Do not redistribute provider data. Twelve Data plan limits belong to Twelve Data. CoinGecko's public API is rate limited; read that provider's terms and attribution rules before you depend on it. `delayed: true` means the figure is not real time. Nothing in this plugin is financial, legal, or tax advice. Indicator results are textbook formulas.

> Informational data. May be delayed. Not investment advice. Read-only.

### Version pin

`mcp.json` depends on `capybucks-mcp==0.1.0` exactly, so a new PyPI release cannot change what users run until this repo bumps the pin and the marketplace reviews the plugin. Plugin version and server version are independent SemVer numbers. They match only for this first release.

Marketplace submission is a separate step and is not done from this repository's CI. See `SUBMISSION.md`.

## Português

### O que é

Plugin do Cursor e do Grok Bot com oito skills e um servidor MCP somente leitura. A versão **0.1.0** do plugin fixa `uvx capybucks-mcp==0.1.0`. O servidor está no repositório [capybucks-mcp](https://github.com/witmondcal-maker/capybucks-mcp). A biblioteca está em [capybucks](https://github.com/witmondcal-maker/capybucks).

A Yahoo é a fonte padrão de ações, com aviso visível: endpoints não oficiais e atraso de cerca de 15 minutos. Cada resposta de dado de mercado cita `provider`, `delayed` e `asof`.

São 10 ferramentas: `list_providers`, `get_history`, `get_quote`, `get_financials`, `get_dividends_and_splits`, `get_option_expirations`, `get_option_chain`, `get_news`, `compute_indicators`, `check_trading_day`.

O plugin não envia ordens, não lê conta de corretora e não transmite ticks. É dado de mercado. Não conecta conta bancária, cartão ou custódia.

### Instalação

É preciso ter o [`uv`](https://docs.astral.sh/uv/) no `PATH`. A primeira execução baixa o pacote e dependências pesadas (`pandas`, `pyarrow`). Aqueça antes de contar com o tempo de partida do cliente:

```bash
uvx capybucks-mcp==0.1.0 --version
```

Ações (Yahoo) e cripto (CoinGecko) não pedem chave. FX e a Twelve Data pedem `CAPYBUCKS_TWELVEDATA_KEY` na configuração do plugin ou em `~/.capybucks.toml` (`[keys]`, chave `twelvedata`). Deixe a variável vazia para continuar na Yahoo e no CoinGecko. Não commite a chave e não cole a chave no chat.

Sem `uv`, o plano B é `pipx run capybucks-mcp==0.1.0` ou `python -m capybucks_mcp` num venv. O `mcp.json` publicado usa `uvx`.

### Teste local

Copie este repositório para `~/.cursor/plugins/local/capybucks`. Symlink só vale se o alvo estiver dentro dessa pasta. Recarregue a janela e abra Customize: 8 skills e o servidor `capybucks`. Em Enterprise, o admin pode precisar ligar a importação de plugins locais.

### Rede e disco

Hosts de saída: `query1.finance.yahoo.com`, `api.coingecko.com`, `api.twelvedata.com`, `stooq.com`. A única escrita local é o cache parquet em `~/.cache/capybucks` (ou `CAPYBUCKS_CACHE_DIR`). Sem telemetria.

### Aviso legal

A licença MIT cobre o software. Os dados seguem os termos de cada provedor e não estão licenciados para redistribuição por este pacote. A Yahoo restringe coleta automatizada. Os limites da Twelve Data são do plano dela. O CoinGecko público tem limite apertado; leia os termos e a regra de atribuição desse provedor antes de depender dele. `delayed: true` não é tempo real. Nada aqui é aconselhamento financeiro, jurídico ou tributário. Indicadores são fórmulas de livro.

> Dados informativos, podem estar atrasados e vir de fontes não oficiais. Isto não é recomendação de investimento. O plugin é somente leitura e não executa ordens.

### Logo

`assets/logo.jpg` é um JPEG de 512×512 gerado a partir de `docs/assets/logo.jpg` no repositório da biblioteca (o original tem cerca de 1,7 MB). O manifesto aponta para o arquivo leve.

### Onde reportar

Veja `SECURITY.md`. Não abra issue pública com chave, URL com `apikey` ou dado de provedor anexado.
