## Como instalar

**Windows** — baixe `Instalar-Finora-Windows.exe`, dê dois cliques e siga o instalador.
Se aparecer o aviso azul "O Windows protegeu o computador", clique em **Mais informações → Executar assim mesmo**.

**Mac com chip Apple (M1 a M4)** — baixe `Finora-Mac-chip-Apple-M1-a-M4.zip`, abra o arquivo e arraste o **Finora** para a pasta **Aplicativos**.
Na primeira vez, o Mac avisa que não consegue verificar o Finora, porque ele não tem assinatura paga da Apple. Para liberar:
- **macOS 15 Sequoia ou mais novo:** tente abrir o Finora uma vez e feche o aviso. Depois vá em **Ajustes do Sistema → Privacidade e Segurança**, role até o fim e clique em **Abrir Mesmo Assim** ao lado do aviso do Finora. Confirme com a senha do Mac.
- **macOS 14 Sonoma ou mais antigo:** clique no Finora com o botão direito → **Abrir** → **Abrir**.
- **Se nada disso aparecer** (ou o Mac disser que o app está danificado): abra o **Terminal** e rode `xattr -dr com.apple.quarantine /Applications/Finora.app`, depois abra o Finora de novo.

Isso só é preciso na primeira vez.

**Mac com processador Intel** — mesmo procedimento com `Finora-Mac-Intel.zip`.

Não sabe qual é o seu Mac? Menu  → **Sobre este Mac**: se aparecer "Chip Apple M…", use o primeiro; se aparecer "Processador Intel", use o segundo.

## Novidades da versão 2.5.2
- Reconhece também a categoria **Ajustes** (usada no Gastos Diários atual) como ajuste de mês: o Saldo atual passa a bater com o do Gastos Diários

## Versão 2.5.1
- Resumo geral: **Saldo atual** calculado como no Gastos Diários — parte do último "Ajuste do mês anterior" e soma o que foi lançado depois

## Versão 2.5
- Resumo geral não conta os lançamentos de ajuste/saldo do mês anterior
- Resumo geral com letras maiores, separado do menu e sem a lista de contas
- Buscar categoria: ao clicar, mostra as categorias já usadas (mais usadas primeiro) para escolher com um toque

## Versão 2.4
- No menu lateral, "Contas" virou **Resumo geral**: receitas totais, despesas totais e saldo total de todo o período lançado
- A escolha de conta continua disponível logo abaixo do resumo

## Versão 2.3
- Novos ícones ilustrados e coloridos (azul e laranja) para todas as categorias
- Em Aparência → Ícones das categorias, escolha entre **Ilustrado** e **Linha**

## Versão 2.2
- Tela inicial sem o "Saldo acumulado": mostra só os valores do mês
- Mais de 80 ícones de categoria, organizados por grupos (Alimentação, Casa, Transporte, Saúde, Contas, Lazer, Compras e família, Receitas)
- Busca de ícone pelo nome (ex.: "gás", "pix", "academia")
- 20 cores prontas e opção de escolher qualquer outra cor

## O que o Finora faz
- Tela inicial com o saldo do mês corrente
- Restaurar e juntar backups do Gastos Diários sem perder lançamentos antigos
- Movimentos, Calendário, Relatórios por data e por categoria
- Categorias com ícones, visual Clara/Noite e paletas de cores
