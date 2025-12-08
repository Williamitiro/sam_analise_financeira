# 📋 CHECKLIST DE VERIFICAÇÃO - NOTEBOOKS & EXPORTAÇÃO V2

**Versão:** 2.0  
**Uso:** OBRIGATÓRIO antes de entregar qualquer alteração  
**Regra:** TODO item deve passar. Se falhar 1, não entregar.

---

## ✅ ANTES DE ESCREVER CÓDIGO

- [ ] Li `celula_0_utils.py` para ver funções disponíveis
- [ ] Li `celula_2_premissas.py` para entender parâmetros
- [ ] Li `PAGINA_1_COCKPIT_V4.py` ou `PAGINA_2_GROWTH.py` como referência
- [ ] Fiz backup/commit do estado atual

---

## ✅ DURANTE O DESENVOLVIMENTO

### Callouts Quarto (CRÍTICO!)

- [ ] **f-string com variáveis:** usar `{{` para ter `{` no output
- [ ] **string normal SEM variáveis:** usar `{` simples
- [ ] **NUNCA usar `{{{{` em f-strings** (vira `{{` literal!)

### Separadores Markdown (CRÍTICO!)

- [ ] **NUNCA usar `---` sozinho em display(Markdown())** - Quarto interpreta como YAML!
- [ ] **Usar `***` para separadores horizontais** - funciona sem problemas

### Tamanho de Gráficos (CRÍTICO para HTML!)

- [ ] **Tamanho padrão:** `figsize = (10, 5)` - evita barra de scroll
- [ ] **NUNCA usar (14, 6) ou (12, 6)** - fica muito grande para HTML
- [ ] Para report_mode: `figsize = (10, 5) if report_mode else (14, 6)`

### Estrutura da Visualização

- [ ] Título/Pergunta de negócio presente (usar `***` como separador)
- [ ] Gráfico renderizado com `salvar_figura_silencioso()`
- [ ] Seção "COMO LER" explicando o gráfico
- [ ] Tabela de prova numérica
- [ ] Callout INSIGHT (FATO + CAUSA + IMPLICAÇÃO + AÇÃO)
- [ ] Callout AUDITORIA (Fonte + Fórmulas)

### Fontes de Dados

- [ ] Fonte indica "Celulas 5A/5B" (não "Motor V13")
- [ ] DataFrame de origem explicitado

---

## ✅ ANTES DE ENTREGAR

### Teste de Renderização

- [ ] Executei: `quarto render ... --to html`
- [ ] Não há WARNINGS sobre `:::` no output
- [ ] Não há erro `YAML parse exception`
- [ ] Abri o HTML e verifiquei visual
- [ ] Gráficos não geram barra de scroll

### Revisão de Output

- [ ] Callouts aparecem como CAIXAS (não texto puro)
- [ ] Tabelas estão formatadas
- [ ] Gráficos estão legíveis e no tamanho correto

### Git

- [ ] `git add .`
- [ ] `git commit -m "mensagem descritiva"`

---

## 🚫 ERROS QUE NUNCA PODEM SER COMETIDOS

| # | ❌ PROIBIDO | Consequência | ✅ FAZER ASSIM |
|---|------------|--------------|----------------|
| 1 | `display(Markdown("---"))` | YAML parse error | Usar `***` |
| 2 | `{{{{` em f-strings para callouts | Vira `{{` literal | Usar `{{` |
| 3 | `{{` em strings normais para callouts | Vira `{{` literal | Usar `{` |
| 4 | Bulk replace de `{{` ou `}}` | Quebra f-strings existentes | NÃO FAZER |
| 5 | `figsize=(14, 6)` para HTML | Barra de scroll | Usar `(10, 5)` |
| 6 | `>` para blockquotes dinâmicos | YAML parse error | Não usar |
| 7 | Recriar funções de celula_0_utils | Duplicação e bugs | Importar |

---

## 📝 LOG DE ERROS ENCONTRADOS

| Data | Erro | Causa | Solução Aplicada |
|------|------|-------|------------------|
| 08/12 | `:::` found in document | `{{{{` em f-string | Mudar para `{{` |
| 08/12 | YAML parse exception | `---` em Markdown | Mudar para `***` |
| 08/12 | Gráficos com scroll | figsize (14,6) | Mudar para (10,5) |
| 08/12 | Callout como texto | string normal com `{{` | Usar f-string |

---

## 📐 PADRÕES DE CÓDIGO

### Padrão para Títulos/Intros VIZ:
```python
if report_mode:
    display(Markdown("***"))  # Separador (NÃO usar ---)
    display(Markdown("## VIZ X.X: Titulo"))
    display(Markdown("**Pergunta:** Texto da pergunta de negocio"))
```

### Padrão para Callouts:
```python
# COM variáveis = f-string + {{
insight_md = f"""
::: {{.callout-tip}}
## Título com {variavel}
:::
"""

# SEM variáveis = string normal + {
audit_md = """
::: {.callout-note}
## Título fixo
:::
"""
```

### Padrão para Figsize:
```python
figsize = (10, 5) if report_mode else (14, 6)
fig, ax = plt.subplots(figsize=figsize, dpi=150)
```
