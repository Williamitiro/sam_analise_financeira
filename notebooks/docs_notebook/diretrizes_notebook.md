# 📘 DOCUMENTO MESTRE - DIRETRIZES DE PRODUTO & DESIGN V21.1 (BÍBLIA DO PROJETO)

**Versão:** V21.2 (Gold Standard + Word Export)
**Status:** DEFINITIVO
**Aplicação:** Todas as páginas do relatório (Notebook Jupyter & DOCX via Quarto).

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
  - *Representação Visual:* Linhas Sólidas, Cores Escuras (Preto/Azul).
- **CENÁRIO "IDEAL" (Benchmark/Meta):** Onde queremos chegar (Padrão de Mercado).
  - *Representação Visual:* Linhas Tracejadas, "Ghost Bars" (Fundo Cinza).
- **CENÁRIO "MONTE CARLO" (Probabilístico):** Faixa de incerteza (P10-P90).
  - *Representação Visual:* Área Sombreada (`alpha=0.2`).

### **2.2 Granularidade Obrigatória**
O sistema exige três níveis de resolução para passar na auditoria:
1.  **Mensal (M0-M36):** Visão Estratégica (Padrão para a maioria).
2.  **Semanal (S0-S24):** Visão Tática (Obrigatório em Viz 3).
3.  **Diário (D0-D180):** Visão Forense (Fluxo de Caixa curto prazo).

---

## 📐 **3. RECEITA CANÔNICA DE UMA CÉLULA (O LAYOUT)**

Toda visualização ("Viz") é um bloco atômico composto por **6 elementos obrigatórios**, nesta ordem exata de renderização (ver `celula_0_utils.py`):

### **BLOCO A: TÍTULO DUPLO**
```python
TÍTULO COLOQUIAL: "O dinheiro está voltando rápido o suficiente?" (Pergunta de Negócio)
TÍTULO TÉCNICO: "Payback Period - Simulação Conservadora vs Benchmark (Semanas 0-24)"
FONTE DOS DADOS: "Dados: df_real_m + benchmarks_saas_b2c"
```

### **BLOCO B: O GRÁFICO (GOLD STANDARD)**
- **Comparação Tripla:** Real Sólido vs Ideal Tracejado vs Benchmark Vermelho.
- **Log Scale:** Obrigatória quando misturar milhões (Receita) com unidades (Clientes).
- **Anotações:** Setas e Badges para eventos importantes (ex: Cruzamento de Meta).
- **Tamanho:** `figsize=(10, 6)` (Otimizado para A4 PDF).

### **BLOCO C: LEGENDA "COMO LER"**
- Manual de instrução obrigatório.
- *Template:* "A linha preta representa sua simulação conservadora. A área cinza é a meta de mercado. Se a preta sair da área cinza, temos um problema."

### **BLOCO D: TABELA PROVA NUMÉRICA (A VERDADE)**
A tabela deve eliminar qualquer dúvida deixada pelo gráfico.
- **Colunas Obrigatórias:**
  1.  **Período:** Mês/Semana.
  2.  **Real (Conservador):** Valor simulado.
  3.  **Ideal (Meta):** Valor alvo.
  4.  **Δ (Delta):** Diferença Absoluta ou %. **Obrigatório.**
  5.  **Status:** Badge colorido (Verde/Amarelo/Vermelho).

**Código de Estilo (Exemplo):**
```python
def format_delta(val):
    if val > 0: return 'color: green; font-weight: bold'
    return 'color: red; font-weight: bold'
```

### **BLOCO E: INSIGHT ESTRATÉGICO (O Veredito)**
- **Estrutura:** Fato (Dado) -> Causa (Por que) -> Implicação (R$) -> Ação (O que fazer).
- **Dinâmico:** Texto deve usar variáveis (`f"O valor é {x}"`), nunca hardcoded.
- **Visual:** Box Colorido (Notebook) ou Callout Tip (PDF).

### **BLOCO F: AUDITORIA & FÓRMULAS (Check Técnico)**
**Localizado logo APÓS o Insight** para validação rápida (Ordem Fixada).
- **Conteúdo:** Fórmula matemática explicada e valores base.
- **Formato:** Callout Colapsável no PDF (`::: {.callout-note collapse="true"} :::`).
- *Exemplo:* "LTV = ARPU * Margem / Churn. Check: 100 * 0.8 / 0.05 = 1600."

---

## 🎨 **4. NOMENCLATURA E ESTRUTURA DE ARQUIVOS (PADRONIZAÇÃO)**

### **4.1 Estrutura de Diretórios**
```
notebooks/
├── quarto_pdf/relatorio_investidores.qmd
├── ypynb/
│   ├── loader_dados_relatorio.py    (Orquestrador)
│   ├── celulas/
│   │   ├── celula_0_utils.py        (Renderizador Atômico)
│   │   ├── PAGINA_1_COCKPIT.py      (Módulo Pág 1)
│   │   ├── PAGINA_2_GROWTH.PY       (Módulo Pág 2)
│   │   └── ...
```

### **4.2 Padrão de Nomenclatura de Arquivos (Outputs)**
Os arquivos gerados pelos scripts devem seguir rigorosamente:
- **Figuras:** `outputs/figs/pg{PÁGINA}_viz{NUM}_{NOME_NO_SNAKE_CASE}.png`
  - *Ex:* `pg2_viz1_funil_aquisicao.png`
- **Metadados:** `outputs/metadata/pg{PÁGINA}_viz{NUM}.json`
- **Tabelas:** `outputs/tables/pg{PÁGINA}_viz{NUM}_tabela.html`

### **4.3 Padrão de Nomenclatura de Funções (Python)**
Toda função de visualização deve seguir esta assinatura:
```python
def gerar_pg{NUM}_viz{NUM}_{NOME}(df_real, df_ideal, mc_results, benchmarks, report_mode=False):
    """
    Parâmetros:
      - df_real: DataFrame do cenário conservador.
      - df_ideal: DataFrame da meta.
      - mc_results: DataFrame da simulação de Monte Carlo.
      - benchmarks: Dicionário de constantes de mercado.
      - report_mode: Booleano (True=DOCX Clean, False=Notebook Rich).
    """
    pass
```

## 📝 **5. EXPORTAÇÃO (WORD FIRST)**
A partir de V21.2, a saída principal é **Microsoft Word (.docx)** para permitir edição final de layout.
- **Tabelas:** Devem ser Markdown puro (`df.to_markdown()`). NUNCA `plt.table`.
- **Gráficos:** `.png` salvos em alta resolução (300dpi).
- **Quebras:** `display(Markdown("\\newpage"))` funciona no Word via Pandoc.

---

## 📊 **5. DIRETRIZES VISUAIS ESPECÍFICAS (POR TIPO)**

### **5.1 Gráficos de Linhas (Evolução)**
- **Linha Real:** `color='#000000'`, `linewidth=2` (Sólido).
- **Linha Ideal:** `color='#AAAAAA'`, `linestyle='--'` (Tracejado).
- **Benchmark:** `color='red'`, `linestyle=':'` (Pontilhado).
- **Anastomoses:** Use `ax.annotate` com setas para mostrar onde cruzamos o benchmark.

### **5.2 Gráficos de Barras (Comparação)**
- **Ghost Bar:** Barra Ideal larga e cinza ao fundo (`alpha=0.3`). Barra Real estreita e sólida na frente.
- **Rótulos:** Valor absoluto no topo da barra. Conversão % no meio da barra (se aplicável).

### **5.3 Tabelas (Auditoria)**
- **Fonte:** Monospace/Courier para alinhamento vertical dos números.
- **Cabeçalho:** Fundo escuro, texto branco.
- **Status:** Badges visuais (Ex: `<span style='color:green'>✔</span>`).

---

## � **6. O RESULTADO FINAL ESPERADO**

Cada célula executada no notebook deve se parecer com um **Slide Profissional da McKinsey**, mas gerado via código:
1.  Começa com uma pergunta instigante.
2.  Mostra o gráfico limpo e direto.
3.  Explica como ler (para o leigo).
4.  Prova os números com uma tabela (para o cético).
5.  Entrega a conclusão estratégica (para o CEO).
6.  **Mostra as fórmulas (Auditoria) ao final** (para o CFO).

**Esta é a definição de "Gold Standard". Nenhuma célula deve ser menos que isso.**
