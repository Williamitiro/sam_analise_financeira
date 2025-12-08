# DOCUMENTACAO TECNICA MASTER V21.0 - JUPYTER E QUARTO REPORT
**Projeto:** SAM Analise Financeira - Investor Deck Generator  
**Versao:** 21.0 (Gold Standard - Tiers 1, 2 e 3 Completos)  
**Status:** Producao (HTML/DOCX via Quarto)  
**Data:** 08/12/2025

---

## 1. Arquitetura do Sistema

O projeto usa arquitetura modular baseada em scripts Python, orquestrada por Quarto.

### 1.1 Diagrama de Componentes

```
notebooks/ypynb/celulas/
├── celula_0_utils.py           # Shared Utils (render_atomic_block, formatadores)
├── celula_2_premissas.py       # Configuracao Central (PREMISSAS - 150+ params)
├── celula_4_motor.py           # Motor de Simulacao Financeira
├── celula_5A_bootstrap_real.py # Gera df_real_m (cenario conservador)
├── celula_5B_cenario_ideal.py  # Gera df_ideal_m (cenario benchmark)
├── PAGINA_1_COCKPIT_V4.py      # Tier 1: Executive Cockpit
├── PAGINA_2_GROWTH.py          # Tier 2: Growth Engine
└── PAGINA_3_FINANCEIRO.py      # Tier 3: Financeiro (DRE + Fluxo + Margens)

notebooks/quarto_pdf/
├── relatorio_investidores.qmd  # Template original (Tiers 1-3)
└── relatorio_completo.qmd      # Template premium com Carta ao Leitor

notebooks/docs_notebook/
├── HANDOFF_CONTEXT.md          # Contexto para handoff entre AIs
├── diretrizes_checklist.md     # CHECKLIST OBRIGATORIO antes de entregar
├── diretrizes_notebook.md      # Regras de produto/design
├── mockup_paginas.md           # Estrutura visual padrao
├── mockup_narrativa.md         # Estrutura narrativa (5 Atos)
└── DOCUMENTACAO_TECNICA_MASTER.md  # ESTE ARQUIVO
```

---

## 2. Guia de Uso (Workflow)

### 2.1 Gerando o Relatorio HTML

```bash
quarto render notebooks/quarto_pdf/relatorio_completo.qmd --to html
```

### 2.2 Gerando o Relatorio DOCX

```bash
quarto render notebooks/quarto_pdf/relatorio_completo.qmd --to docx
```

### 2.3 O que acontece nos bastidores

1. Quarto inicializa kernel Python
2. Imports dos modulos de celulas
3. Simulacoes Real e Ideal executadas silenciosamente
4. Tiers 1, 2 e 3 renderizados com `report_mode=True`
5. Graficos salvos como PNG, tabelas em Markdown puro
6. Arquivo final gerado em `notebooks/quarto_pdf/`

---

## 3. Padroes de Desenvolvimento

### 3.1 Regras ABSOLUTAS (Ver diretrizes_checklist.md)

| Proibido | Fazer Assim |
|----------|-------------|
| `---` em Markdown dinamico | Usar `***` |
| `{{` em strings normais | Usar `{` ou f-string |
| `{{{{` em f-strings | Usar `{{` |
| figsize (14,6) para HTML | Usar `(10, 5)` |
| Textos hardcoded | Tudo dinamico |
| Bulk replace de `{{` | NAO FAZER |

### 3.2 Estrutura de Visualizacao (Gold Standard)

Cada VIZ deve ter:
1. Titulo/Pergunta de negocio
2. Grafico (salvo com `salvar_figura_silencioso`)
3. COMO LER (explicacao para leigo)
4. Tabela de prova
5. Callout INSIGHT (FATO + CAUSA + IMPLICACAO + ACAO)
6. Callout AUDITORIA (Fonte + Formulas)

### 3.3 Padrao para Callouts Quarto

```python
# COM variaveis = f-string + {{
insight_md = f"""
::: {{.callout-tip}}
## Titulo com {variavel}
:::
"""

# SEM variaveis = string normal + {
audit_md = """
::: {.callout-note collapse="true"}
## Auditoria
:::
"""
```

---

## 4. Troubleshooting

### Erro: YAML parse exception
- **Causa:** `---` em display(Markdown()) ou caracteres especiais
- **Solucao:** Usar `***` para separadores

### Erro: ModuleNotFoundError
- **Causa:** `root_dir` com caminho errado
- **Solucao:** Verificar niveis de `../` no os.path.abspath()

### Graficos com Scroll no HTML
- **Causa:** figsize muito grande
- **Solucao:** Usar `figsize=(10, 5)`

### Callout aparece como texto literal
- **Causa:** `{{` em string normal (deveria ser `{`)
- **Solucao:** Verificar se e f-string ou string normal

---

## 5. Documentacao Relacionada

| Arquivo | Proposito |
|---------|-----------|
| `diretrizes_checklist.md` | Checklist OBRIGATORIO antes de entregar |
| `diretrizes_notebook.md` | Regras de produto e design |
| `HANDOFF_CONTEXT.md` | Contexto para handoff entre AIs |
| `mockup_paginas.md` | Estrutura visual padrao |
| `mockup_narrativa.md` | Estrutura narrativa (5 Atos) |

**Regra:** Sempre ler `diretrizes_checklist.md` antes de desenvolver.
