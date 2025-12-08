# 📋 CHECKLIST DE VERIFICAÇÃO - NOTEBOOKS & EXPORTAÇÃO

**Versão:** 1.0  
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
  ```python
  insight_md = f"""
  ::: {{.callout-tip}}
  Texto com {variavel}
  :::
  """
  ```

- [ ] **string normal SEM variáveis:** usar `{` simples
  ```python
  texto = """
  ::: {.callout-note}
  Texto fixo
  :::
  """
  ```

- [ ] **NUNCA usar `{{{{` em f-strings** (vira `{{` literal!)

### Estrutura da Visualização

- [ ] Título/Pergunta de negócio presente
- [ ] Gráfico renderizado com `salvar_figura_silencioso()`
- [ ] Seção "COMO LER" explicando o gráfico
- [ ] Tabela de prova numérica
- [ ] Callout INSIGHT (FATO + CAUSA + IMPLICAÇÃO + AÇÃO)
- [ ] Callout AUDITORIA (Fonte + Fórmulas)

### Fontes de Dados

- [ ] Fonte indica "Celulas 5A/5B" (não "Motor V13")
- [ ] DataFrame de origem explicitado (df_real_m, df_ideal_m, etc)

---

## ✅ ANTES DE ENTREGAR

### Teste de Renderização

- [ ] Executei: `quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx`
- [ ] Não há WARNINGS sobre `:::` no output
- [ ] Abri o DOCX e verifiquei visual

### Revisão de Output

- [ ] Callouts aparecem como CAIXAS (não texto puro)
- [ ] Tabelas estão formatadas
- [ ] Gráficos estão legíveis
- [ ] Quebras de página funcionam

### Git

- [ ] `git add .`
- [ ] `git commit -m "mensagem descritiva"`

---

## 🚫 O QUE NUNCA FAZER

| ❌ PROIBIDO | Por quê |
|------------|---------|
| Usar `>` para blockquotes em Markdown dinâmico | Causa erro YAML |
| Usar `{{{{` em f-strings para callouts | Vira `{{` literal |
| Fazer bulk replace de `{{` ou `}}` | Quebra código existente |
| Recriar funções de celula_0_utils | Duplicação e bugs |
| Esquecer de testar com `quarto render` | Erros só aparecem lá |

---

## 📝 LOG DE ERROS COMUNS

| Erro | Causa | Solução |
|------|-------|---------|
| WARNING: `:::` found in document | Callout não renderizou | Verificar `{{` vs `{` |
| YAML parse exception | Caractere especial em Markdown | Remover `>` ou caracteres estranhos |
| f-string expecting expression | `{` sozinho em f-string | Usar `{{` para escapar |
| Callout como texto puro | `{{{{` em f-string | Mudar para `{{` |
