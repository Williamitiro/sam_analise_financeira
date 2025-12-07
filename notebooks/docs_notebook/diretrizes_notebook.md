# 📘 DOCUMENTO MESTRE - DIRETRIZES DE VISUALIZAÇÃO GOLD STANDARD V20.0

**Objetivo:** Este documento define a **receita canônica** para cada célula de visualização do Investor Deck. É o **único ponto de verdade** antes de qualquer linha de código. Todas as páginas devem seguir estas diretrizes rigorosamente para garantir a geração automática do PDF via Quarto.

---

## 🎯 **1. FILOSOFIA DE DESIGN E DEFINIÇÕES (Regras de Ouro)**

### **1.1 Definição de Cenários (Contexto Crítico)**

Como a empresa ainda não existe, os dados seguem esta lógica obrigatória:

- **CENÁRIO "REAL" (Simulação Conservadora):** Dados modestos, "pés no chão", Hard Mode. É o teste de estresse. **IMPORTANTE:** Este não é um dado real da empresa (que ainda não existe), mas sim uma simulação com premissas conservadoras.
- **CENÁRIO "IDEAL" (Benchmark/Meta):** Dados de alta performance de mercado, baseados em benchmarks do setor.
- **CENÁRIO "MONTE CARLO" (Probabilístico):** Faixa de possibilidades (P10, P50, P90) gerada por simulação estocástica.
- **O OBJETIVO:** Provar que o modelo se sustenta no cenário "Real" (conservador) e mostrar o *gap* para o "Ideal" (meta de mercado).

### **1.2 Princípios de Storytelling Visual**

- **Nenhum gráfico vive sozinho:** Cada visualização é um "pacote completo" contendo:
  - **Título Duplo** (Coloquial + Técnico)
  - **Gráfico Principal** (Visual limpo e profissional)
  - **Tabela Auxiliar** (Dados numéricos com Delta)
  - **Legenda "Como Ler"** (Manual de instruções)
  - **Insight Estratégico** (Diagnóstico + Ação)
  - **Metadados Técnicos** (JSON para automação)

- **Tripla Comparação Sempre Presente:**
  - **Real (Conservador):** Linha/Barra Sólida, cores fortes (Preto, Azul Marinho, Verde Floresta)
  - **Ideal (Meta):** Linha Tracejada, "Ghost Bar" (barra larga transparente ao fundo) ou Área Sombreada Cinza
  - **Benchmark de Mercado:** Linha Vermelha pontilhada (referência do setor)

- **Design Flat (Sem Efeitos):**
  - ❌ **Proibido:** Sombras, gradientes, efeitos 3D, arco-íris
  - ✅ **Obrigatório:** Gráficos vetoriais limpos, alto contraste, fundo 100% branco (#FFFFFF)
  - ✅ **Pronto para impressão:** DPI 300, formato A4

- **SEPARAÇÃO CLARA:** Cada seção deve ter uma linha divisória visual ou quebra de espaço clara para facilitar a leitura e impressão via Quarto.

---

## 📐 **2. ESTRUTURA PADRÃO DE CADA CÉLULA (O LAYOUT)**

Toda célula de visualização **deve conter** estes 6 blocos, nesta ordem exata:

### **Bloco A: TÍTULO DUPLO**

```python
# Formato Obrigatório
TÍTULO COLOQUIAL: "O dinheiro está voltando rápido o suficiente?" (Pergunta de Negócio)
TÍTULO TÉCNICO: "Payback Period - Simulação Conservadora vs Benchmark (Semanas 0-24)"
FONTE DOS DADOS: "Dados: df_real_m_v2 (Simulação) + benchmarks_saas_b2c (Mercado)"
```

**Regras:**
- **Título Coloquial:** Pergunta que qualquer pessoa (investidor não-técnico, dono de bar) faria.
- **Título Técnico:** Após o " - ", especifique método, período, e contexto técnico.
- **Fonte dos Dados:** Sempre explicitar de onde vêm os dados (DataFrame, API, simulação, etc.).

### **Bloco B: GRÁFICO PRINCIPAL**

**Especificações Técnicas:**
- **Tamanho:** `figsize=(12, 6)` para gráficos, `(12, 4)` para tabelas
- **DPI:** `300` (qualidade de impressão profissional)
- **Fonte:** `Arial` ou `Helvetica`, tamanho 10-12 pontos
- **Cores:** Máximo 4 cores distintas por página
  - **Real (Conservador):** Preto (`#000000`) ou Azul Marinho (`#1E3A8A`)
  - **Ideal (Meta):** Cinza Claro (`#EEEEEE`) para "Ghost Bar" ou Verde (`#388E3C`)
  - **Benchmark:** Vermelho (`#D32F2F`)
  - **Alerta/Pessimista:** Laranja (`#F57C00`)
  - **Fundos:** Branco puro (`#FFFFFF`)

**Granularidade Obrigatória:**
- **Pelo menos 1 gráfico por seção** deve mostrar a visão **SEMANAL (Semanas 0-24)** para ajuste tático nos primeiros 6 meses.
- **Demais gráficos:** Podem usar granularidade mensal (Meses 0-36) para visão estratégica.

### **Bloco C: LEGENDA EXPLICATIVA (COMO LER)**

**Template Obrigatório:**

```markdown
**COMO LER ESTE GRÁFICO:**
1. **[Elemento Visual 1 - ex: Barra Azul Sólida]:** Representa nossa simulação conservadora (cenário "Real").
2. **[Elemento Visual 2 - ex: Barra Cinza Larga ao Fundo]:** Representa a meta ideal (benchmark de mercado).
3. **[Eixo X]:** Período em [semanas/meses], escala [linear/logarítmica].
4. **[Eixo Y]:** Métrica em [R$, %, unidades], escala [linear/logarítmica].
5. **[Ponto de Interesse - ex: Cruzamento]:** Quando a linha azul cruza a vermelha, significa [explicação].
6. **[Zona de Alerta]:** Área sombreada em vermelho indica [risco/oportunidade].

**Regra de Ouro para Investidor:** "Se você só tiver 30 segundos, olhe para [elemento X]."
```

### **Bloco D: TABELA AUXILIAR (A PROVA NUMÉRICA)**

**Colunas Obrigatórias:**
1. **Período** (Semana/Mês)
2. **Real (Conservador)** - Valor da simulação conservadora
3. **Ideal (Meta)** - Valor do benchmark/meta
4. **Δ (Delta)** - Diferença Absoluta ou % com cor (Verde se positivo, Vermelho se negativo)

**Explicação da Tabela:**
- Sempre incluir um texto logo acima ou abaixo da tabela explicando o que os dados mostram.
- Exemplo: *"A tabela abaixo compara os valores simulados (Real) com as metas de mercado (Ideal). O Delta mostra a diferença percentual."*

**Estilo de Formatação:**
- **Fonte:** `Courier New` ou `Monospace` para alinhamento numérico perfeito
- **Cores de Background:**
  - Verde (`#C8E6C9`): Delta positivo (acima da meta)
  - Amarelo (`#FFF9C4`): Delta neutro (próximo da meta)
  - Vermelho (`#FFCDD2`): Delta negativo (abaixo da meta)
- **Alinhamento:** Números à direita, texto à esquerda
- **Bordas:** `border: 1px solid #303030` (preto suave)

**Exemplo de Código:**
```python
def format_delta(val):
    if val > 0: return 'background-color: #C8E6C9; color: #2E7D32; font-weight: bold'
    if val < 0: return 'background-color: #FFCDD2; color: #C62828; font-weight: bold'
    return 'background-color: #FFF9C4; color: #F57C00'

styled_df = df.style\
    .format(precision=0, na_rep='-')\
    .applymap(format_delta, subset=['Delta'])\
    .set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#303030'),
                                     ('color', 'white'),
                                     ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('border', '1px solid #E0E0E0')]}
    ])
```

### **Bloco E: INSIGHT ESTRATÉGICO (DIAGNÓSTICO + AÇÃO)**

**Template Obrigatório (Zero Hardcoded - Texto Dinâmico):**

```markdown
**INSIGHT ESTRATÉGICO: O que Fazer com Isso**

**Destaque 1 (O Fato):** [Métrica Real] está [X]% [acima/abaixo] da [Meta Ideal] no período [Y].

**Causa Raiz:** Isso ocorre devido a [razão específica identificada nos dados, ex: saturação do canal pago na semana 12].

**Implicação Financeira:** Isso significa que [consequência financeira concreta, ex: perderemos R$ 50k em MRR] em [período, ex: próximos 3 meses].

**Ação Recomendada:** Portanto, [decisão concreta e acionável, ex: redirecionar 30% do budget de Ads para SEO] deve ser prioridade [P0/P1/P2].

**Destaque 2:** [Repetir estrutura para segunda métrica relevante]
```

**Nota Importante:** O insight deve ser **dinâmico** e mudar se os dados mudarem. Evite textos hardcoded.

### **Bloco F: METADADOS TÉCNICOS (JSON)**

Essencial para o motor de geração de PDF (Quarto). Deve ser salvo em arquivo `.json`.

```python
metadata = {
    "chart_id": "pg2_viz1_funil",
    "section": "growth_engine",
    "page_number": 2,
    "title_simple": "Escalando sem perder qualidade",
    "title_technical": "Funil de Aquisição - Simulação Conservadora vs Benchmark",
    "data_source": "df_real_m_v2",
    "columns_used": ["novos_usuarios", "ativacoes", "conversoes"],
    "insight_generated": "O funil real superou a meta em 15% devido ao canal orgânico...",
    "files": {
        "png_path": "outputs/figs/pg2_viz1_funil.png",
        "json_path": "outputs/metadata/pg2_viz1.json",
        "table_path": "outputs/tables/pg2_viz1_tabela.html"
    },
    "validation_status": "ok",  # "ok", "atencao", "erro"
    "generation_time": "0.3s",
    "quarto_include": true
}
```

---

## 📊 **3. DIRETRIZES GLOBAIS POR TIPO DE VISUALIZAÇÃO**

### **3.1 GRÁFICOS DE LINHAS TEMPORAIS**

**Aplicação:** MRR, Caixa, Usuários Ativos, Churn, etc.

**Regras Visuais:**
- **Linha Real (Conservador):** Traço preto sólido, `linewidth=2.5`
- **Linha Ideal (Meta):** Tracejado cinza ou verde, `linestyle='--'`, `linewidth=1.5`
- **Linha Benchmark:** Tracejado vermelho, `linestyle=':'`, `linewidth=1.5`
- **Área de Incerteza (Monte Carlo):** Duas linhas finas (P10 e P90), `linewidth=0.8`, `alpha=0.6`, sem preenchimento

**Anastomoses (Cruzamentos):**
- Quando linha Real cruza Benchmark: Adicionar anotação com seta e badge
  ```python
  ax.annotate('✓ Meta Atingida', xy=(mes_cruzamento, valor),
              arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
  ```

### **3.2 GRÁFICOS DE BARRAS**

**Aplicação:** Canais de Aquisição, Cohort, Comparativos, etc.

**Técnica "Ghost Bar" (Comparação Real vs Ideal):**
- **Barra Ideal (Fundo):** Larga (`width=0.8`), cor cinza claro (`#EEEEEE`), sem borda ou borda tracejada
- **Barra Real (Frente):** Estreita (`width=0.4`), cor sólida (`#1E88E5` ou `#2E7D32`), centralizada

**Barras Empilhadas:**
- Use `bottom=` para sobrepor (ex: Novos vs Churn)
- Cores monocromáticas (ex: verde claro → verde escuro), nunca arco-íris

**Labels:**
- Mostre **valor absoluto** e **% de atingimento** no topo de cada barra

### **3.3 GRÁFICOS DE DISPERSÃO**

**Aplicação:** Elasticidade, Correlações, etc.

**Regras:**
- **Tamanho dos pontos:** `s=60` (visível mas não obstrutivo)
- **Cor:** Mapeie para 3ª variável (ex: mês) usando `cmap='viridis'`
- **Linha de Tendência:**
  - ❌ **Proibido:** Regressão Linear simples (reta) para fenômenos não-lineares
  - ✅ **Obrigatório:** Curva Polinomial ou Logarítmica para mostrar saturação/teto
  - Intervalo de confiança: `ci=95`, `alpha=0.15` (sombreado leve)
- **R²:** Anotar no canto superior direito
  ```python
  plt.text(0.95, 0.95, f'R² = {r2:.2f}', transform=ax.transAxes,
           ha='right', va='top', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
  ```

### **3.4 TABELAS**

**Aplicação:** DRE, Executiva, Cohort, Comparativos, etc.

**Regras de Formatação:**
- **Fonte:** `Courier New` ou `Monospace` (alinhamento numérico)
- **Cores de Status:**
  - 🟢 Verde (`#2E7D32`): Positivo/Bom
  - 🟡 Amarelo (`#F57C00`): Atenção/Neutro
  - 🔴 Vermelho (`#C62828`): Negativo/Ruim
- **Alinhamento:** Números à direita, texto à esquerda
- **Bordas:** Sutis (`1px solid #303030`)

---

## 📋 **4. CHECKLIST DE VALIDAÇÃO (DOER)**

Antes de considerar uma célula **pronta para produção**, verifique:

- [ ] **Título Duplo** (Coloquial + Técnico) está presente e claro
- [ ] **Fonte dos Dados** está especificada
- [ ] **Gráfico** tem DPI 300, fontes legíveis (Arial/Helvetica 10-12pt)
- [ ] **Cores** seguem a paleta definida (máximo 4 cores por página)
- [ ] **Fundo** é branco puro (#FFFFFF), sem sombras ou gradientes
- [ ] **Granularidade:** Pelo menos 1 gráfico por seção mostra visão semanal (0-24)
- [ ] **Legenda "Como Ler"** explica cada elemento visual
- [ ] **Tabela Auxiliar** tem colunas obrigatórias (Período, Real, Ideal, Delta)
- [ ] **Explicação da Tabela** está presente (texto acima/abaixo)
- [ ] **Insight Estratégico** segue template (Fato → Causa → Implicação → Ação)
- [ ] **Insight é dinâmico** (muda se os dados mudarem, não é hardcoded)
- [ ] **Metadados JSON** salvos em `outputs/metadata/`
- [ ] **Figura PNG** salva em `outputs/figs/` com nome padronizado `pg{X}_viz{Y}_{nome}.png`
- [ ] **Tabela HTML/LaTeX** salva em `outputs/tables/`
- [ ] **Nomes técnicos** explicados em linguagem simples (ex: "CAC (Custo de Aquisição)")
- [ ] **Código é idempotente:** Rodar 2x gera o mesmo resultado (seed fixa para Monte Carlo)
- [ ] **Comparação Real vs Ideal** está visualmente clara
- [ ] **Separação clara** entre seções (para impressão via Quarto)

---

## 🎨 **5. NOMENCLATURA E ESTRUTURA DE ARQUIVOS**

### **5.1 Estrutura de Diretórios (Obrigatória)**

O código deve garantir que estas pastas existam:

```
projeto_dashboard/
├── inputs/                  # CSVs, Excel, dados brutos
├── outputs/
│   ├── figs/               # PNGs 300dpi (gráficos)
│   ├── metadata/           # JSONs (metadados para Quarto)
│   └── tables/             # HTML ou LaTeX (tabelas formatadas)
├── notebooks/              # Jupyter Notebooks
└── scripts/                # Scripts Python auxiliares
```

### **5.2 Padrão de Nomenclatura de Arquivos**

- **Figuras:** `pg{PÁGINA}_viz{NUM}_{NOME_CURTO}.png`
  - Exemplo: `pg2_viz1_funil.png`, `pg1_viz3_mrr_semanal.png`
- **Metadados:** `pg{PÁGINA}_viz{NUM}.json`
  - Exemplo: `pg2_viz1.json`
- **Tabelas:** `pg{PÁGINA}_viz{NUM}_tabela.html`
  - Exemplo: `pg2_viz1_tabela.html`

### **5.3 Padrão de Nomenclatura de Funções**

```python
def gerar_pg{NUM}_viz{NUM}_{NOME}(df_real, df_ideal, mc_results, benchmarks):
    """
    Gera visualização completa: título, gráfico, tabela, insight, metadata.
   
    Parâmetros:
    - df_real: DataFrame mensal cenário conservador (simulação "Real")
    - df_ideal: DataFrame mensal cenário ideal (benchmark de mercado)
    - mc_results: DataFrame agregado Monte Carlo (P10, P50, P90)
    - benchmarks: dict de benchmarks de mercado
   
    Retorna:
    - fig: objeto matplotlib.figure (gráfico)
    - styled_df: pandas.io.formats.style.Styler (tabela formatada)
    - insight: str multilinha com análise estratégica
    - metadata: dict para Quarto (JSON)
    """
    pass
```

---

## ⚠️ **6. BOAS PRÁTICAS DE LINGUAGEM (ANTI-PORTUNHOL)**

### **6.1 Tradução Imediata de Siglas**

**Regra de Ouro:** NUNCA usar siglas soltas sem explicação.

| ❌ Errado | ✅ Certo |
|-----------|----------|
| "Evolução do CAC" | "Evolução do Custo de Aquisição (CAC)" |
| "LTV/CAC Ratio" | "Retorno do Investimento em Aquisição (LTV/CAC)" |
| "Churn Rate" | "Taxa de Cancelamento (Churn)" |
| "Runway" | "Dias de Sobrevivência (Runway)" |

### **6.2 Glossário de Termos Técnicos**

Não usar glossário no final do documento. Explicar a sigla **na primeira vez** que ela aparece no título, eixo ou legenda.

| Técnico | Tradução Simples |
|---------|------------------|
| CAC | "Custo para Conquistar Cliente" |
| LTV/CAC | "Retorno do Investimento em Aquisição" |
| Churn | "Taxa de Cancelamento" |
| Runway | "Dias de Sobrevivência" |
| NRR | "Receita que Cresce Sozinha" |
| EBITDA | "Lucro Operacional Real" |
| ARPU | "Ticket Médio por Cliente" |
| MRR | "Receita Recorrente Mensal" |
| ARR | "Receita Recorrente Anual" |

---

## 🎯 **7. ESPECIFICAÇÕES DE GRANULARIDADE**

### **Período 0-24 semanas (Validação Tática):**
- **Unidade:** **SEMANAS** (24 semanas = ~6 meses)
- **Razão:** Mostrar detalhes da ramp-up inicial, identificar problemas rapidamente
- **Visualização:** Linhas com pontos semanais, barras semanais
- **Obrigatoriedade:** Pelo menos 1 gráfico por seção deve usar esta granularidade

### **Período 0-36 meses (Visão Estratégica):**
- **Unidade:** **MESES** (36 meses = 3 anos)
- **Razão:** Visão estratégica de longo prazo, suficiente para identificar tendências
- **Visualização:** Linhas mensais suavizadas, barras mensais

### **Snapshots Estratégicos (Marcos):**
- **M6 (Semana 24):** Primeiro breakpoint (validação do modelo)
- **M12:** Um ano (aniversário, revisão anual)
- **M36:** Meta final (ex: ARR $1M, Break-even)

---

## 🔄 **8. ITERAÇÃO E VALIDAÇÃO (FLUXO DE TRABALHO)**

### **Processo de Criação:**

1. **Planeje a Célula:**
   - Defina qual métrica será visualizada
   - Escolha o tipo de gráfico mais adequado
   - Identifique os dados necessários (Real, Ideal, Benchmark)

2. **Crie o Código:**
   - Siga a estrutura de 6 blocos (A a F)
   - Use as funções padronizadas (`gerar_pg{X}_viz{Y}_{nome}`)
   - Garanta que o código é idempotente (seed fixa)

3. **Rode e Inspecione:**
   - Execute o código e gere o gráfico
   - Zoom a 200% para verificar legibilidade
   - Verifique se as cores estão corretas

4. **Teste de Clareza:**
   - Leia em voz alta o "Como Ler" e "Insight"
   - Soa natural? Um investidor não-técnico entenderia?
   - Passe para um co-fundador sem contexto: ele entende em 30 segundos?

5. **Refine se Necessário:**
   - Se não estiver claro, refaça título, legenda ou callouts
   - Simplifique a linguagem técnica
   - Adicione anotações visuais (setas, badges)

6. **Salve e Exporte:**
   - Salve metadados em JSON (`outputs/metadata/`)
   - Exporte figura em PNG 300dpi (`outputs/figs/`)
   - Exporte tabela em HTML/LaTeX (`outputs/tables/`)

7. **Valide com Checklist:**
   - Use o checklist da Seção 4 para garantir completude
   - Marque todos os itens antes de considerar pronto

---

## 🎨 **9. PADRÕES VISUAIS ADICIONAIS**

### **9.1 Callouts e Anotações**

**Seta para cima (Positivo):**
```python
ax.annotate('🔥 Meta batida\n3 meses antes!',
            xy=(6, 10000), xytext=(8, 15000),
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7),
            fontsize=9, fontweight='bold')
```

**Seta para baixo (Negativo):**
```python
ax.annotate('⚠️ Risco: Churn\nacima da meta',
            xy=(6, 0.07), xytext=(9, 0.09),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7),
            fontsize=9, fontweight='bold')
```

### **9.2 Zonas de Alerta**

**Zona de Risco (Sombreado Vermelho):**
```python
ax.axvspan(xmin=mes_inicio, xmax=mes_fim, color='red', alpha=0.05, label='Zona de Risco')
```

**Zona de Oportunidade (Sombreado Verde):**
```python
ax.axvspan(xmin=mes_inicio, xmax=mes_fim, color='green', alpha=0.05, label='Zona de Oportunidade')
```

---

## 📝 **10. RESUMO EXECUTIVO**

Este documento define **diretrizes globais** para todas as visualizações do Investor Deck. As regras são:

1. **Estrutura de 6 Blocos:** Título Duplo, Gráfico, Legenda, Tabela, Insight, Metadados
2. **Comparação Tripla:** Real (Conservador) vs Ideal (Meta) vs Benchmark (Mercado)
3. **Design Flat:** Sem sombras, gradientes ou 3D. Fundo branco, DPI 300.
4. **Granularidade Dupla:** Semanal (0-24) para tática, Mensal (0-36) para estratégia.
5. **Linguagem Clara:** Traduzir siglas imediatamente, evitar portunhol.
6. **Tabelas com Delta:** Sempre incluir coluna de diferença (Real vs Ideal).
7. **Insights Dinâmicos:** Texto gerado a partir dos dados, não hardcoded.
8. **Automação:** Metadados JSON para geração de PDF via Quarto.
9. **Validação:** Checklist de 17 itens antes de considerar pronto.
10. **Nomenclatura Padronizada:** Arquivos, funções e diretórios seguem padrão definido.

---

**Versão:** V20.0  
**Data:** 2025-12-06  
**Status:** Documento Único e Definitivo  
**Próximos Passos:** Aplicar estas diretrizes em todas as células de visualização do projeto.

