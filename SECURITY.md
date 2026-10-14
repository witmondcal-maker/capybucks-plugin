# Security policy

## English

Capybucks is read-only market data. The plugin does not place orders, read brokerage accounts, or collect personal data. The MCP process can write a parquet cache under `~/.cache/capybucks` (or `CAPYBUCKS_CACHE_DIR`). That is the only local write.

Outbound hosts used by the library are:

- `query1.finance.yahoo.com`
- `api.coingecko.com`
- `api.twelvedata.com`
- `stooq.com`

`mcp.json` runs `uvx capybucks-mcp==0.1.0`. The exact pin is deliberate: a new PyPI upload does not reach users until this repository changes the pin and the marketplace reviews it. The server package is published from [capybucks-mcp](https://github.com/witmondcal-maker/capybucks-mcp). Do not install an unpinned `uvx capybucks-mcp`.

The Twelve Data key is a plugin variable, `CAPYBUCKS_TWELVEDATA_KEY`. The repository stores the placeholder `${CAPYBUCKS_TWELVEDATA_KEY}` only. Set the value in the plugin configuration or in `~/.capybucks.toml`. Never send the key in chat, in a GitHub issue, or in a log paste.

### Reporting

Report a vulnerability privately. Email Ricardo Margalho at ricardo@penarede.com.br and, if you can, open a private GitHub security advisory on [witmondcal-maker/capybucks-plugin](https://github.com/witmondcal-maker/capybucks-plugin/security/advisories).

Say which repository and version, what an attacker can do, and whether a key or a provider payload is involved. You will get an acknowledgement. Fixes that change the server ship in `capybucks-mcp` first, then this plugin bumps the pin.

Please do not file a public issue that contains a live API key, a URL with `apikey`, or a dump of provider data.

## Português

O Capybucks é dado de mercado somente leitura. O plugin não envia ordens, não lê conta de corretora e não coleta dado pessoal. O processo MCP pode gravar cache parquet em `~/.cache/capybucks` (ou `CAPYBUCKS_CACHE_DIR`). Essa é a única escrita local.

Os hosts de saída da biblioteca são `query1.finance.yahoo.com`, `api.coingecko.com`, `api.twelvedata.com` e `stooq.com`.

O `mcp.json` roda `uvx capybucks-mcp==0.1.0`. O pin exato é de propósito: um upload novo no PyPI não chega ao usuário até este repositório mudar o pin e o marketplace revisar. O pacote sai de [capybucks-mcp](https://github.com/witmondcal-maker/capybucks-mcp).

A chave da Twelve Data é a variável `CAPYBUCKS_TWELVEDATA_KEY`. O repositório só guarda o placeholder. Configure no plugin ou em `~/.capybucks.toml`. Não envie a chave no chat, em issue ou em log.

### Como reportar

Reporte vulnerabilidade em privado. Escreva para Ricardo Margalho em ricardo@penarede.com.br e, se puder, abra um advisory privado em [witmondcal-maker/capybucks-plugin](https://github.com/witmondcal-maker/capybucks-plugin/security/advisories).

Diga o repositório, a versão e o que um atacante consegue fazer. Não abra issue pública com chave, URL com `apikey` ou dump de dado de provedor.
