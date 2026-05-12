# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos

**Instalar dependências:**
```
pip install -r requirements.txt
```

**Rodar o servidor:**
```
python app.py
```
Acesse em `http://localhost:5000`

## Arquitetura

Aplicação Flask de arquivo único (`app.py`) com fluxo de dados em pipeline:

1. `buscar_dados()` — baixa preços de fechamento via `yfinance` para `PETR4.SA`, `ITUB4.SA` e `VALE3.SA` desde `2026-01-02` até a data atual
2. `calcular_performance(df)` — calcula variação percentual acumulada em relação ao primeiro pregão do ano
3. `gerar_grafico_cotacao(df)` / `gerar_grafico_performance(df_perf)` — geram strings HTML com gráficos Plotly embutíveis
4. Rota `/` executa o pipeline e renderiza `templates/index.html` via Jinja2

Os gráficos são gerados server-side e injetados no template com o filtro `| safe`. O Plotly.js é carregado via CDN apenas no primeiro gráfico (`include_plotlyjs="cdn"`); o segundo usa `include_plotlyjs=False` para evitar duplicação.

Para adicionar uma nova ação, inclua o ticker em `TICKERS` e a cor hex em `CORES` em `app.py`.

## Repositório GitHub

O projeto está hospedado em `https://github.com/thobi31/dashboard-acoes-brasileiras`.

A sincronização com o GitHub é **automática**: ao final de cada resposta do Claude Code, o hook de Stop em `.claude/settings.json` executa `git add -A`, faz commit com a mensagem `auto: atualização via Claude Code` e empurra para o repositório — mas somente se houver alterações. Nenhuma ação manual é necessária.
