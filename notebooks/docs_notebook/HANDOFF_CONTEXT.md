# 🛑 LEIA-ME PRIMEIRO (HANDOFF CONTEXT)
**Data:** 08/12/2025  
**Status:** DOCX FUNCIONAL - MELHORIAS PENDENTES

---

## ⚠️ REGRAS ABSOLUTAS - LER 3X ANTES DE QUALQUER AÇÃO

### 🚫 REGRA 1: TÍTULOS/HEADERS VÃO NO .QMD, NÃO NO PYTHON
```
❌ ERRADO: display(Markdown("## VIZ 3.1: Titulo"))  # NO PYTHON
✅ CERTO:  ## VIZ 3.1: Titulo                       # NO ARQUIVO .QMD
```

### 🚫 REGRA 2: NUNCA FAZER BULK REPLACE DE {{ ou }}
```
❌ ERRADO: c.replace('}}', '}')  # QUEBRA F-STRINGS!
✅ CERTO:  Não tocar em {{ ou }}
```

### 🚫 REGRA 3: COMMIT ANTES DE QUALQUER REPLACE GLOBAL
```
git add .
git commit -m "Backup antes de alteracao arriscada"
```

### 🚫 REGRA 4: TESTAR QUARTO APÓS CADA MUDANÇA
```
quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx
```

---

## Lista de Mudanças Perdidas (A RESTAURAR)

| # | Mudança | Arquivo | Status |
|---|---------|---------|--------|
| 1 | Linhas tracejadas visiveis VIZ 3.4 (roxo #7B1FA2, laranja #FF9800) | PAGINA_3_FINANCEIRO.py | ⏳ PENDENTE |
| 2 | Espacamento insight/tabela VIZ 3.3 | PAGINA_3_FINANCEIRO.py | ⏳ PENDENTE |
| 3 | COMO LER heatmap expandido VIZ 3.5 | PAGINA_3_FINANCEIRO.py | ⏳ PENDENTE |
| 4 | Headers VIZ com perguntas de negócio | relatorio_investidores.qmd | ⏳ PENDENTE |

---

## Arquitetura

```
notebooks/ypynb/celulas/
├── PAGINA_3_FINANCEIRO.py  # Gráficos e insights dinâmicos APENAS

notebooks/quarto_pdf/
└── relatorio_investidores.qmd  # Títulos, headers, texto estático
```

---

## Por Que o Erro YAML Acontece

O Quarto/Pandoc é MUITO sensível. Estas coisas QUEBRAM:
- `>` no início de linhas em strings Markdown
- Markdown mal formatado gerado dinamicamente
- Caracteres especiais em contextos errados

O que FUNCIONA (não mudar):
- Callouts `:::` dentro de f-strings com escape `{{...}}`
- Markdown básico em display()
- Texto sem caracteres especiais

---

## Commit Seguro

Ultimo commit funcional: `c807e29`
Para restaurar: `git checkout c807e29 -- <arquivo>`
