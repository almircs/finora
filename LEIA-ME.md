# Finora

Controle de receitas e despesas para Windows e Mac, com contas, categorias com ícones, lançamentos recorrentes, relatórios, orçamento e dois visuais (Clara e Noite). Abre e grava o backup do Gastos Diários (`database.sqlite`).

## Estrutura
- `finora.src.html`: o código do app (uma página só). Edite aqui.
- `build.py`: gera `desktop/app/index.html` (programa) e `web/finora.html` (versão web). Rode `npm run build:html` para atualizar `app/index.html`.
- `main.js` e `preload.js`: o programa Electron (janela, gravação em disco, cópia diária, migração da pasta do Caixa Diário).
- `instalador/finora-windows.nsi`: script do instalador Windows (NSIS).

## Onde ficam os dados
- Windows: `%APPDATA%\Finora\finora.json`
- Mac: `~/Library/Application Support/Finora/finora.json`
Cópias automáticas dos últimos 30 dias na subpasta `backups`. Na primeira abertura, se existir a pasta do Caixa Diário, os lançamentos de lá são aproveitados.

## Gerar instaladores com Node.js
```
npm install
npm start          # abre o programa
npm run dist:win   # instalador Windows (rodar no Windows)
npm run dist:mac   # instaladores Mac (rodar no Mac)
```
Ou envie esta pasta para um repositório no GitHub e rode a ação **Gerar instaladores** na aba Actions.
