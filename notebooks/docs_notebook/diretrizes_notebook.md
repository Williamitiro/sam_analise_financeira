# 📘 DOCUMENTO MESTRE - DIRETRIZES DE PRODUTO & DESIGN V21.1 (BÍBLIA DO PROJETO)

**Versão:** V21.3 (Gold Standard + Word Export + Regras Técnicas)
**Status:** DEFINITIVO
**Aplicação:** Todas as páginas do relatório (Notebook Jupyter & DOCX via Quarto).

---

## 🚨 **0. LEIA ANTES DE DESENVOLVER QUALQUER CÓDIGO**

### **0.1 Arquivos que DEVEM ser lidos ANTES de começar:**

| Arquivo | Conteúdo | Por que ler? |
|---------|----------|--------------|
| `celula_0_utils.py` | Funções compartilhadas (render_atomic_block, formata_moeda, etc) | **USAR estas funções**, não recriar |
| `celula_2_premissas.py` | Dicionário PREMISSAS com +150 parâmetros | Fonte de todas as configurações |
| `celula_5A_bootstrap_real.py` | Gera df_real_m (cenário conservador) | Fonte dos dados REAL |
| `celula_5B_cenario_ideal.py` | Gera df_ideal_m (cenário benchmark) | Fonte dos dados IDEAL |
| `PAGINA_1_COCKPIT_V4.py` | Exemplo de página funcional | Padrão a seguir |
| `PAGINA_2_GROWTH.py` | Exemplo de página funcional | Padrão a seguir |

### **0.2 O QUE NÃO PODE FAZER (REGRAS ABSOLUTAS):**

| ❌ NÃO FAZER | ✅ FAZER ASSIM | Por quê |
|--------------|----------------|---------|
| Usar `>` para blockquotes em Markdown dinâmico | Usar texto simples ou callouts Quarto | Causa erro YAML no Quarto |
| Usar `{{` em strings normais para callouts | Usar f-string ou `{` simples | `{{` em string normal fica literal |
| Usar `{{{{` em f-strings para callouts | Usar `{{` | `{{{{` vira `{{` literal |
| Fazer bulk replace de `{{` ou `}}` | NÃO MEXER - são escapes de f-string | Quebra todo o código existente |
| Usar `---` em display(Markdown()) | Usar `***` para separadores | `---` causa YAML parse error |
| Usar figsize (14,6) ou (12,6) para HTML | Usar `figsize=(10,5)` | Gráficos grandes geram scroll |
| Criar funções que já existem em celula_0_utils | Importar de celula_0_utils | Evita duplicação e bugs |
| Adicionar títulos/headers dinâmicos | Usar `***` como separador (não `---`) | `---` quebra Quarto |

### **0.3 Padrão para Callouts Quarto:**

```python
# ✅ CORRETO: f-string com {{ escape
insight_md = f"""
::: {{.callout-tip}}
## Título
Conteúdo com {variavel}
:::
"""

# ✅ CORRETO: string normal SEM variáveis usa { simples
audit_md = """
::: {.callout-note collapse="true"}
## Auditoria
Texto fixo sem variáveis
:::
"""

# ❌ ERRADO: string normal com {{
audit_md = """
::: {{.callout-note}}  # VAI APARECER LITERAL!
"""
```

### **0.4 Antes de qualquer mudança arriscada:**

```bash
git add .
git commit -m "Backup antes de alteracao"
```

### **0.5 Após qualquer mudança:**

```bash
quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx
```

---

## 🏛️ **1. ARQUITETURA E NARRATIVA (O PORQUÊ)**

O relatório não é uma coleção aleatória de gráficos. É um **processo jurídico de prova** que deve responder a perguntas letais de investidores em 15 minutos.

### **1.1 A Estrutura de 6 Páginas (Roadmap)**

O Dashboard segue esta jornada linear obrigatória:

```
┌─────────────────────────────────────────────────────────┐
│  PÁGINA 1: EXECUTIVE COCKPIT (Overview + War Room)     │  ← 3 min: Prove que o piloto está no controle.
│  PÁGINA 2: GROWTH MACHINE (Funil + Canais + Eficiência)│  ← 5 min: Prove que sabe adquirir clientes.
│  PÁGINA 3: FINANCEIRO (DRE + Fluxo + Sankey)           │  ← 4 min: Prove que a conta fecha.
│  PÁGINA 4: UNIT ECONOMICS (LTV/CAC + Cohorts + RPE)    │  ← 4 min: Prove que a unidade é lucrativa.
│  PÁGINA 5: RISCO & CENÁRIOS (MC + Sensibilidade + Gap) │  ← 5 min: Prove que conhece os perigos.
│  PÁGINA 6: APÊNDICE (Glossário + Metodologia + Premissas)│ ← 2 min: As letras miúdas (Auditoria).
└─────────────────────────────────────────────────────────┘
```

### **1.2 O "Arco de 5 Atos" (Estrutura de Cada Página)**

**Toda página** deve contar uma história completa seguindo este arco. Não adicione gráficos que não atendam a uma destas 5 funções (Perguntas de Negócio):

| Célula | Função Narrativa | A Pergunta Letal (C-Level) | O Que Provar (Tese) |
| :--- | :--- | :--- | :--- |
| **Viz 1** | **A Tese (Macro)** | "O modelo para de pé no cenário conservador?" | Provar que o acumulado final é positivo. |
| **Viz 2** | **A Saúde (Unitária)** | "A eficiência por unidade é saudável?" | Provar que não perdemos dinheiro a cada venda. |
| **Viz 3** | **O Tático (Semanal)** | "Houve descontrole no início da operação?" | Provar capacidade de correção rápida (0-24 sem). |
| **Viz 4** | **A Escala (Futuro)** | "Se injetar dinheiro, melhora ou piora?" | Provar elasticidade e identificar o teto. |
| **Viz 5** | **O Vazamento (Risco)** | "Onde está o dinheiro invisível?" | Quantificar a perda que ninguém vê (Tax, Churn). |

> **REGRA DE OURO:** Se um gráfico não responde a uma pergunta fundamental, **APAGUE-O**.

---

## 🎯 **2. FILOSOFIA DE DESIGN E DADOS (REGRAS DE OURO)**

### **2.1 Definição de Cenários (Contexto Crítico)**

Como a empresa é um projeto (ainda não operacional), usamos simulações:

- **CENÁRIO "REAL" (Simulação Conservadora):** "Pés no chão", nível Difícil. É o teste de estresse.
- **CENÁRIO "IDEAL" (Benchmark de Mercado):** "Benchmark do que a indústria alcança". Métrica aspiracional.

### **2.2 Granularidade Temporal (Regra de Inversão)**

| Horizonte | Granularidade | Lógica |
| :--- | :--- | :--- |
| **M0 - M6** | Semanal (0W - 24W) | Caixa curto, riscos rápidos demais para mensal. |
| **M7 - M36** | Mensal (M7 - M36) | Erros mensais se compensam, visão de tendência. |

---

## 🧱 **3. ESTRUTURA CANÔNICA DA CÉLULA (O "Gold Standard")**

Uma célula de visualização **DEVE** conter estes 6 elementos obrigatórios, nesta ordem:

```
[1. TÍTULO/PERGUNTA DE NEGÓCIO] - "A empresa vai sobreviver ao vale de caixa?"
[2. GRÁFICO/VISUAL]             - Matplotlib/Plotly, limpo e profissional.
[3. LEGENDA "COMO LER"]         - Explicação para quem nunca viu o gráfico.
[4. TABELA DE PROVA]            - Números que validam o insight (auditável).
[5. CALLOUT INSIGHT]            - FATO + CAUSA + IMPLICAÇÃO + AÇÃO.
[6. CALLOUT AUDITORIA]          - Formulas e fonte dos dados.
```

### **3.1 Cada Elemento em Detalhe:**

1. **Título/Pergunta:** Pode estar no .qmd (estático) ou no código (dinâmico) - ambos funcionam
2. **Gráfico:** Usar `salvar_figura_silencioso()` para salvar sem exibir duplicado
3. **COMO LER:** Markdown simples explicando cada elemento do gráfico
4. **Tabela:** `df.to_markdown(index=False)` em report_mode, HTML rico no notebook
5. **Insight:** Callout `::: {.callout-tip}` com as 4 partes obrigatórias
6. **Auditoria:** Callout `::: {.callout-note collapse="true"}` com fonte e fórmulas

---

## 📁 **4. CONVENÇÕES DE ARQUIVOS**

| Tipo | Nomenclatura | Local |
|------|--------------|-------|
| Módulo de página | `PAGINA_X_NOME.py` | `notebooks/ypynb/celulas/` |
| Utilitários | `celula_0_utils.py` | `notebooks/ypynb/celulas/` |
| Premissas | `celula_2_premissas.py` | `notebooks/ypynb/celulas/` |
| Motor | `celula_4_motor.py` | `notebooks/ypynb/celulas/` |
| Simulações | `celula_5A/5B/5C/5D_*.py` | `notebooks/ypynb/celulas/` |
| Relatório QMD | `relatorio_investidores.qmd` | `notebooks/quarto_pdf/` |

---

## 📝 **5. EXPORTAÇÃO (WORD FIRST)**

A partir de V21.2, a saída principal é **Microsoft Word (.docx)** para permitir edição final de layout.
- **Tabelas:** Devem ser Markdown puro (`df.to_markdown()`). NUNCA `plt.table`.
- **Gráficos:** `.png` salvos em alta resolução (300dpi).
- **Quebras:** `display(Markdown("\\newpage"))` funciona no Word via Pandoc.

---

## 📊 **6. DIRETRIZES VISUAIS ESPECÍFICAS (POR TIPO)**

### **6.1 Gráficos de Linhas (Evolução)**
- **Linha Real:** `color='#000000'`, `linewidth=2` (Sólido).
- **Linha Ideal:** `color='#AAAAAA'`, `linestyle='--'` (Tracejado).
- **Benchmark:** `color='red'`, `linestyle=':'` (Pontilhado).
- **Anastomoses:** Use `ax.annotate` com setas para mostrar onde cruzamos o benchmark.

### **6.2 Gráficos de Barras (Comparação)**
- **Ghost Bar:** Barra Ideal larga e cinza ao fundo (`alpha=0.3`). Barra Real estreita e sólida na frente.
- **Rótulos:** Valor absoluto no topo da barra. Conversão % no meio da barra (se aplicável).

### **6.3 Tabelas (Auditoria)**
- **Fonte:** Monospace/Courier para alinhamento vertical dos números.
- **Cabeçalho:** Fundo escuro, texto branco.
- **Status:** Badges visuais (Ex: `<span style='color:green'>✔</span>`).

---

## 🎯 **7. O RESULTADO FINAL ESPERADO**

Cada célula executada no notebook deve se parecer com um **Slide Profissional da McKinsey**, mas gerado via código:
1.  Começa com uma pergunta instigante.
2.  Mostra o gráfico limpo e direto.
3.  Explica como ler (para o leigo).
4.  Prova os números com uma tabela (para o cético).
5.  Entrega a conclusão estratégica (para o CEO).
6.  **Mostra as fórmulas (Auditoria) ao final** (para o CFO).

**Esta é a definição de "Gold Standard". Nenhuma célula deve ser menos que isso.**
