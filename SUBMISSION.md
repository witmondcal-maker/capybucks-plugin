# Checklist de submissão

**Este plugin depende de publicar `capybucks-mcp` 0.1.0 no PyPI.** Em 2026-10-15, `https://pypi.org/pypi/capybucks-mcp/json` respondia 404. O pacote não está publicado. Não afirmar o contrário.

Antes de submeter, nesta ordem:

1. Publicar `capybucks-mcp` 0.1.0 no PyPI (o pin do `mcp.json` não muda neste repositório).
2. Rodar o job manual `pypi-pin` (`workflow_dispatch`). Ele só passa depois da publicação.
3. Testar o plugin no Cursor (`~/.cursor/plugins/local/capybucks`) e no Grok Bot.

**Não enviar ao marketplace a partir deste repositório.**

Baseada na checklist de <https://cursor.com/docs/reference/plugins> (lida em 2026-10-14) e na seção 11 do plano. O formulário em <https://cursor.com/marketplace/publish> fica com a conta do Ricardo. Privacidade do plugin e do servidor: `PRIVACY.md`.

Itens que este repositório já cobre:

- [x] Repositório `witmondcal-maker/capybucks-plugin` open source (MIT).
- [x] `.cursor-plugin/plugin.json` válido contra o schema publicado em `cursor/plugins` (`schemas/plugin.schema.json`). `name` é `capybucks`, kebab-case.
- [x] `description` em uma frase, sem promessa de tempo real e sem promessa de ganho. Inclui "Not investment advice".
- [x] `skills` aponta para `./skills/`. Cada skill tem frontmatter `name` e `description`. O corpo está em inglês; a `description` tem gatilho em português e em inglês.
- [x] `mcpServers` aponta para `./mcp.json`. O arquivo na raiz se chama exatamente `mcp.json`.
- [x] A única `${VAR}` do `mcp.json` (`CAPYBUCKS_TWELVEDATA_KEY`) está em `variables`. Nenhum segredo no repositório.
- [x] Caminhos do manifesto são relativos, sem `..` e sem caminho absoluto.
- [x] Logo em `assets/logo.jpg`, caminho relativo, 512×512, abaixo de 100 KB.
- [x] `README.md` explica instalação, pré-requisito `uv`, variável opcional, as 10 ferramentas, hosts de saída, avisos legais e como reportar problema (pt-BR e EN). O topo avisa que o plugin depende de publicar o MCP no PyPI.
- [x] `PRIVACY.md` na raiz, em português e em inglês, alinhado ao código do MCP conferido em 2026-10-15.
- [x] `LICENSE` MIT com a nota de que a licença não cobre os dados dos provedores.
- [x] `SECURITY.md` com canal de reporte (e-mail e advisory privado).
- [x] `category` é `integrations`, o mesmo valor dos plugins oficiais `github` e `finance` em `cursor/plugins`. O schema aceita string livre. A página `cursor.com/marketplace/publish` não expôs um enum legível na leitura de 2026-10-14.
- [x] `tags`: `finance`, `market-data`, `mcp`, `read-only`.
- [x] Sem rules `alwaysApply`. Os avisos ficam nas skills.

Itens que dependem do servidor, do cliente ou do Ricardo:

- [ ] O pin `capybucks-mcp==0.1.0` existe no PyPI. Em 2026-10-14 a URL do projeto respondia 404. O job manual `pypi-pin` (`workflow_dispatch`) falha de propósito até a publicação. Não marcar este item antes disso.
- [ ] Servidor publicado no PyPI por OIDC, com código público em `capybucks-mcp`.
- [ ] Plugin testado em `~/.cursor/plugins/local/capybucks` e no Grok Bot, com a tabela de prompts (ferramenta chamada, proveniência citada, avisos). Este ambiente não tem a janela Customize. Os testes daqui cobrem manifesto, skills e referências, não o cliente.
- [ ] Conferir no formulário, no dia do envio, se `category` ainda aceita `integrations`.
- [ ] Submissão pelo formulário, com a conta do Ricardo. Não foi feita.
- [ ] Depois da aprovação: anotar que cada bump do pin passa por revisão manual.

## Decisões já tomadas

- Licença MIT. Autor Ricardo Margalho `<ricardo@penarede.com.br>`.
- Yahoo continua fonte padrão de ações, com aviso visível nas skills e no README.
- v0.1 expõe as 10 ferramentas da seção 7.4 do plano.
- Um só manifesto, `.cursor-plugin/plugin.json`. O schema do Cursor tem cliente `grokbot` no mesmo formato (o plugin `finance` do marketplace é assim). Não há `.grok-plugin/` nem `plugin.json` na raiz: a variável da chave precisa do formato Cursor Plugin, e um segundo manifesto duplicaria o pacote.
- Sem `minClientVersions`. Não há versão mínima confirmada, e um valor chutado esconderia o plugin de um dos clientes.
- O script `scripts/validate-template.mjs` do `cursor/plugin-template` não foi copiado. O template não publica `LICENSE`, e o script exige `.cursor-plugin/marketplace.json` de repositório multi-plugin. A seção "Single plugin" do template manda um `plugin.json` na raiz do repo e nenhum marketplace. A validação equivalente está em `tests/` e roda no workflow `validate`.

## Como verificar antes de enviar

```bash
pip install -r requirements-dev.txt
python -m pytest -q
python -m pytest -q -m pypi -o addopts=
```

O segundo comando só deve passar depois que `capybucks-mcp==0.1.0` estiver no PyPI.
