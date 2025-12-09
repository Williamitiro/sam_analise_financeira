# CHECKLIST DE VERIFICACAO - NOTEBOOKS E EXPORTACAO V3
Versao: 3.0
Uso: OBRIGATORIO antes de entregar qualquer alteracao
Regra: TODO item deve passar. Se falhar 1, nao entregar.

---

## 🚨🚨🚨 REGRA FUNDAMENTAL - ZERO HARDCODED 🚨🚨🚨
### **TUDO DEVE SER DINAMICO E INTELIGENTE!**

| ❌ PROIBIDO | ✅ OBRIGATORIO |
|------------|----------------|
| Textos fixos em insights | Insights gerados a partir dos dados |
| Valores hardcoded | Valores calculados das premissas |
| Conclusoes estaticas | Conclusoes que mudam conforme os numeros |
| Titulo generico "A PROVA NUMERICA" | Titulo especifico da tabela (ex: "Tabela de Conversao M36") |
| Fonte estatica "V10" | Fonte dinamica "df_real_m vs df_ideal" |

**SE MUDAR AS PREMISSAS, OS TEXTOS DEVEM MUDAR AUTOMATICAMENTE!**

---

## ✅ ANTES DE ESCREVER CODIGO

- [ ] Li `celula_0_utils.py` para ver funcoes disponiveis
- [ ] Li `celula_2_premissas.py` para entender parametros
- [ ] Fiz backup/commit do estado atual

---

## ✅ DURANTE O DESENVOLVIMENTO

### Tabelas e Dados (CRITICO!)
- [ ] **NUNCA usar titulo generico "A PROVA NUMERICA"** -> Usar titulo especifico
- [ ] **Tabelas devem ser MARKDOWN** no PDF -> `df.to_markdown()` (nunca texto puro)
- [ ] **Fonte Dinamica OBRIGATORIA** -> `Fonte: {df_usado} | {descricao}`
- [ ] Tabela tem explicacao logo abaixo?

### Graficos e Visualizacao
- [ ] **Labels nao sobrepoe titulo/legenda** -> Usar `plt.subplots_adjust`
- [ ] **figsize=(10, 5)** para HTML -> Evita scroll
- [ ] **COMO LER Compacto (Inline)** -> Nada de listas verticais. Texto corrido.
- [ ] **Fonte Externa** -> Passar `data_source_text` para `render_atomic_block` (Nunca `ax.text`)
- [ ] **Conv% e anotacoes FORA do grafico** -> Evita poluição visual

### Callouts Quarto
- [ ] **Auditoria/Formulas SEM tags HTML** (`<b>`, `<i>`) -> Usar Markdown puro
- [ ] **f-string com variaveis:** usar `{{` para ter `{` no output
- [ ] **string normal SEM variaveis:** usar `{` simples

### Separadores Markdown
- [ ] **NUNCA usar `---` sozinho** -> Usar `***`

---

## ✅ ANTES DE ENTREGAR

### Teste de Renderizacao
- [ ] Executei: `quarto render ... --to html`
- [ ] Nao ha WARNINGS sobre `:::` no output
- [ ] Nao ha erro `YAML parse exception`
- [ ] Tabelas aparecem formatadas (com bordas), nao texto solto

### Revisao de Output
- [ ] Fontes estao corretas e dinamicas?
- [ ] Graficos estao legiveis sem sobreposicao?
- [ ] Tabelas tem titulos especificos?

---

## 🚫 ERROS QUE NUNCA PODEM SER COMETIDOS

| # | ❌ PROIBIDO | Consequencia | ✅ FAZER ASSIM |
|---|------------|--------------|----------------|
| 1 | `display(Markdown("---"))` | YAML parse error | Usar `***` |
| 2 | Titulo "A PROVA NUMERICA" | Generico/Amador | "Detalhe da Conversao" |
| 3 | Tabela como Texto | Ilegivel | Markdown Table |
| 4 | HTML (`<b>`) em Callout | Texto literal | Markdown (`**`) |
| 5 | Annotations DENTRO grafico | Poluicao | Legenda externa |
| 6 | Fonte "Modelo V10" | Informacao Falsa | Fonte Dinamica |

---

## 📝 LOG DE ERROS ENCONTRADOS

| Data | Erro | Causa | Solucao Aplicada |
|------|------|-------|------------------|
| 08/12 | Tabela como texto | Tabela sem formatacao Markdown | `df.to_markdown()` |
| 08/12 | Titulo Generico | Hardcoded "A PROVA NUMERICA" | Parametro `table_title` |
| 08/12 | Labels cortados | Falta de Margem | `subplots_adjust` |
| 08/12 | Fonte Estatica | Texto hardcoded | Fonte Dinamica |
