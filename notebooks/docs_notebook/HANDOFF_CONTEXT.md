# 🛑 LEIA-ME PRIMEIRO (HANDOFF CONTEXT)
**Data:** 08/12/2025
**Status:** PÁGINA 3 IMPLEMENTADA - ERRO QUARTO PENDENTE

---

## 1. O Que Foi Feito (Sessão Atual - 08/12)

### ✅ PÁGINA 3: FINANCEIRO - COMPLETA
O arquivo `PAGINA_3_FINANCEIRO.py` foi **criado e implementado** com 5 visualizações:
- **VIZ 3.1:** Evolução Financeira Correlacionada (DRE + Dual Y-Axis)
- **VIZ 3.2:** Estrutura de Custos (Waterfall + Breakdown detalhado)
- **VIZ 3.3:** Fluxo de Caixa Semanal (identifica vale crítico)
- **VIZ 3.4:** Alavancagem Operacional (scatter receita vs margem)
- **VIZ 3.5:** Heatmap DRE Evolutivo (Real vs Ideal)
- **VIZ 3.6:** Veredito Financeiro Final

### ✅ Polimentos Aplicados
1. **VIZ Headers:** Cada visualização agora tem título + pergunta de negócio antes do gráfico
2. **VIZ 3.4 Melhorada:** Intro explicando "O que é alavancagem operacional" + COMO LER detalhado
3. **Linhas tracejadas mais visíveis:** Cor roxa (#7B1FA2), linewidth 2.5
4. **Heatmap explicação:** COMO LER explica diferença entre Delta e Valores Absolutos
5. **Espaçamento insight/tabela:** Adicionado separador visual

---

## 2. ⚠️ ERROS COMETIDOS E COMO EVITAR

### ERRO 1: Parâmetros de função inconsistentes
**O que aconteceu:** `loader_dados_relatorio.py` chamava `executar_pagina_3_financeiro(df_real=...)` mas a função esperava `df_real_m=...`.
**Sintoma:** `TypeError: got an unexpected keyword argument 'df_real'`
**Correção:** Alinhar nomes de parâmetros entre caller e function.
> 🛑 **REGRA:** Sempre verificar a assinatura da função antes de chamá-la.

### ERRO 2: Replace_file_content corrompendo arquivos
**O que aconteceu:** A ferramenta de edição tentou replacements em blocos grandes e corrompeu o código (funções truncadas, código misturado).
**Sintoma:** `SyntaxError: invalid character` ou código faltando.
**Correção:** Restaurar via `git checkout HEAD -- [arquivo]` e refazer com edições menores.
> 🛑 **REGRA:** Preferir `write_to_file` para reescrever funções inteiras. Usar `replace_file_content` apenas para edições cirúrgicas de 5-10 linhas.

### ERRO 3: Blockquote (>) no Quarto causa YAML parse error
**O que aconteceu:** Usei sintaxe `> **texto**` para criar blockquotes no Markdown.
**Sintoma:** `YAML parse exception at line 4, column 0`
**Correção:** NÃO RESOLVIDO AINDA - ver próximo passo.
> 🛑 **REGRA:** Evitar caracteres `>` em strings Markdown que serão renderizadas pelo Quarto.

---

## 3. Arquitetura Atual

```
notebooks/ypynb/
├── loader_dados_relatorio.py   # Orquestrador - roda tudo
├── real_vs_ideal_v7_GOLD.ipynb # Painel de desenvolvimento
└── celulas/
    ├── celula_0_utils.py       # Funções compartilhadas
    ├── celula_2_premissas.py   # PREMISSAS dict
    ├── celula_4_motor.py       # Motor de simulação
    ├── PAGINA_1_COCKPIT_V4.py  # ✅ Página 1
    ├── PAGINA_2_GROWTH.py      # ✅ Página 2
    └── PAGINA_3_FINANCEIRO.py  # ✅ Página 3 (NOVA)

notebooks/quarto_pdf/
└── relatorio_investidores.qmd  # Gera DOCX via Quarto
```

---

## 4. 🚨 PRÓXIMO PASSO (IMEDIATO)

### TAREFA NÃO CONCLUÍDA: Corrigir erro de renderização Quarto

**Erro:**
```
YAML parse exception at line 4, column 0,
while parsing a flow node:
did not find expected node content
```

**Causa provável:** Caracteres `>` (blockquote) no texto `intro_alavancagem` em `PAGINA_3_FINANCEIRO.py` (linhas 721-728).

**Ação necessária:**
1. Abrir `PAGINA_3_FINANCEIRO.py`
2. Localizar linhas ~721-728 (buscar "O QUE")
3. Remover os caracteres `>` do início de cada linha
4. Testar: `quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx`

---

## 5. Referências
- **Diretrizes:** `notebooks/docs_notebook/diretrizes_notebook.md`
- **Mockup narrativa:** `notebooks/docs_notebook/mockup_narrativa.md`
- **Log anterior:** `notebooks/docs_notebook/Finalizing Page 3 Financials.md`
