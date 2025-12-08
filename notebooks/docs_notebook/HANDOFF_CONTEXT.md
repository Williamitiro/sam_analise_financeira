# 🛑 LEIA-ME PRIMEIRO (HANDOFF CONTEXT)
**Data:** 08/12/2025  
**Status:** HTML FUNCIONAL - Página 3 completa com títulos, COMO LER melhorado e auditorias

---

## ⚠️ REGRAS ABSOLUTAS - LER 3X ANTES DE QUALQUER AÇÃO

### 🚫 REGRA 1: NUNCA usar `---` em display(Markdown())
```
❌ ERRADO: display(Markdown("---"))     # CAUSA YAML PARSE ERROR!
✅ CERTO:  display(Markdown("***"))     # Usar asteriscos
```

### 🚫 REGRA 2: CALLOUTS - {{ vs {
```
❌ ERRADO: audit_md = """ ::: {{.callout }} """    # String normal com {{ = literal
✅ CERTO:  audit_md = """ ::: {.callout } """      # String normal usa {
✅ CERTO:  insight_md = f""" ::: {{.callout }} """ # F-string usa {{
```

### 🚫 REGRA 3: NUNCA fazer bulk replace de {{ ou }}
```
# QUEBRA TODO O CÓDIGO EXISTENTE!
```

### 🚫 REGRA 4: TAMANHO DE GRÁFICOS PARA HTML
```
❌ ERRADO: figsize = (14, 6)   # Muito grande, gera scroll
✅ CERTO:  figsize = (10, 5)   # Cabe na tela sem scroll
```

### 🚫 REGRA 5: COMMIT ANTES DE QUALQUER REPLACE GLOBAL
```bash
git add .
git commit -m "Backup antes de alteracao arriscada"
```

---

## 📁 Arquivos que DEVEM ser lidos ANTES de desenvolver:

| Arquivo | Por que ler? |
|---------|--------------|
| `celula_0_utils.py` | Funções compartilhadas - USAR, não recriar |
| `PAGINA_1_COCKPIT_V4.py` | Padrão a seguir |
| `PAGINA_2_GROWTH.py` | Padrão a seguir |
| `diretrizes_checklist.md` | Checklist OBRIGATÓRIO antes de entregar |

---

## ✅ Estado Atual - Página 3 Completa

| Item | Status |
|------|--------|
| Fontes "Celulas 5A/5B" | ✅ |
| COMO LER melhorado (todos VIZ) | ✅ |
| Auditorias com fórmulas (todos VIZ) | ✅ |
| Títulos/Intros (todos VIZ) | ✅ |
| Tamanho gráficos ajustado | ✅ |

---

## 📝 Erros Cometidos Nesta Sessão (NÃO REPETIR!)

| # | Erro | Consequência | Vezes |
|---|------|--------------|-------|
| 1 | Usar `---` em Markdown dinâmico | YAML parse error | 2x |
| 2 | Usar `{{{{` em f-strings | Callout vira texto literal | 2x |
| 3 | Usar `{{` em string normal | Callout vira texto literal | 3x |
| 4 | figsize (14,6) para HTML | Barra de scroll | 1x |
| 5 | Bulk replace de {{ | Quebrou f-strings | 1x |

---

## 🔧 Comando de Renderização

```bash
quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to html
```

---

## 📂 Arquitetura

```
notebooks/ypynb/celulas/
├── celula_0_utils.py        # Funções compartilhadas
├── PAGINA_1_COCKPIT_V4.py   # Página 1
├── PAGINA_2_GROWTH.py       # Página 2
├── PAGINA_3_FINANCEIRO.py   # Página 3

notebooks/quarto_pdf/
└── relatorio_investidores.qmd  # Orquestrador Quarto

notebooks/docs_notebook/
├── diretrizes_checklist.md     # CHECKLIST OBRIGATÓRIO
├── diretrizes_notebook.md      # Regras de produto/design
├── mockup_paginas.md           # Estrutura visual
├── mockup_narrativa.md         # Estrutura narrativa
└── HANDOFF_CONTEXT.md          # ESTE ARQUIVO
```
