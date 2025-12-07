# 📊 PLANO DE IMPLEMENTAÇÃO V7.0 — PÁGINA 2: GROWTH MACHINE
**Data:** 2025-12-06  
**Status:** 🔴 SUBSTITUIÇÃO COMPLETA DO PLANO V6.0  
**Nível:** Institutional Grade (Kaszek/Sequoia/a16z)  
**Base:** Diretrizes V20.0 + Mockup Páginas + Mockup Narrativa (Arco de 5 Atos)

---

## 📋 SUMÁRIO EXECUTIVO

### **O Problema (Diagnóstico do V6.0)**
A implementação anterior (`modelo2.py`) possui **7 gaps críticos** em relação às diretrizes:

| # | Gap | Severidade |
|---|-----|------------|
| 1 | Nenhum gráfico usa granularidade **SEMANAL (0-24)** | 🔴 P0 |
| 2 | Não há comparação **Real (Conservador) vs Ideal (Benchmark)** | 🔴 P0 |
| 3 | Tabelas não têm colunas **IDEAL** e **DELTA** | 🟠 P1 |
| 4 | Não gera **Metadados JSON** para Quarto | 🟠 P1 |
| 5 | Não exporta **Tabelas HTML/LaTeX** | 🟠 P1 |
| 6 | VIZ 2.1 e 2.2 não seguem o **Arco Narrativo** corretamente | 🟠 P1 |
| 7 | Títulos não são **perguntas de negócio** | 🟡 P2 |

### **A Solução (V7.0)**
Reestruturar as 5 visualizações para:
1. Seguir o **Arco de 5 Atos** do `mockup_narrativa.md`
2. Incluir **1 gráfico semanal obrigatório** (Ato 3)
3. Todas as tabelas com colunas **Período | Real | Ideal | Delta | Status**
4. Gerar **metadados JSON** e **tabelas HTML**
5. Comparar **Cenário Conservador vs Benchmark de Mercado**

---

## 🎯 1. FILOSOFIA DE DESIGN (REGRAS INVIOLÁVEIS)

### 1.1 Definição de Cenários (Diretriz V20.0, Seção 1.1)

| Cenário | Definição | Representação Visual |
|---------|-----------|----------------------|
| **"REAL" (Conservador)** | Simulação com premissas modestas ("pés no chão"). A empresa **não existe** ainda. | Linha/Barra **Preta Sólida** |
| **"IDEAL" (Benchmark)** | Metas baseadas em benchmarks de mercado (SaaS B2C, Fintech). | Linha **Cinza Tracejada** ou "Ghost Bar" (fundo) |
| **"BENCHMARK"** | Referência do setor (ex: Payback 12m, LTV/CAC 3x). | Linha **Vermelha Pontilhada** |

### 1.2 O Arco de 5 Atos (Mockup Narrativa, Seção 1)

| Ato | Função Narrativa | Pergunta Letal (C-Level) | VIZ Atual → Corrigida |
|-----|------------------|--------------------------|------------------------|
| 1 | **Tese (Macro)** | "O modelo para de pé no cenário conservador?" | VIZ 2.1 → Manter, ajustar |
| 2 | **Saúde (Unitária)** | "A eficiência por unidade é saudável?" | VIZ 2.2 → **SUBSTITUIR** |
| 3 | **Tático (Semanal)** | "Houve descontrole no início?" | **NOVO** → VIZ 2.3 Semanal |
| 4 | **Escala (Futuro)** | "Se injetar dinheiro, melhora?" | VIZ 2.3 → Move para 2.4 |
| 5 | **Vazamento (Risco)** | "Onde está o dinheiro invisível?" | VIZ 2.4 → Move para 2.5 |

### 1.3 Estrutura de 6 Blocos por Célula (Diretriz V20.0, Seção 2)

Cada visualização **DEVE** conter:
```
BLOCO A: TÍTULO DUPLO (Coloquial + Técnico + Fonte dos Dados)
BLOCO B: GRÁFICO PRINCIPAL (Real vs Ideal vs Benchmark)
BLOCO C: LEGENDA "COMO LER" (Template obrigatório)
BLOCO D: TABELA AUXILIAR (Período | Real | Ideal | Delta | Status)
BLOCO E: INSIGHT ESTRATÉGICO (Fato → Causa → Implicação → Ação)
BLOCO F: METADADOS JSON (Salvar em outputs/metadata/)
```

---

## 📊 2. ESPECIFICAÇÃO DAS 5 VISUALIZAÇÕES

### VIZ 2.1: A TESE MACRO (Ato 1)

#### A. Conteúdo Textual
```python
TÍTULO_COLOQUIAL = "O volume de vendas sustenta a operação no cenário conservador?"
TÍTULO_TÉCNICO = "Funil de Aquisição: Conservador vs Benchmark | Escala Logarítmica (M0-M36)"
FONTE_DADOS = "df_real_m (Conservador) + benchmarks_saas_b2c (Mercado)"
```

#### B. Gráfico Principal
- **Tipo:** Horizontal Bar Chart com escala logarítmica no eixo X
- **Comparação:**
  - **Barras Sólidas (Escuras):** Cenário Conservador (`df_real_m`)
  - **Ghost Bars (Fundo Cinza):** Benchmark de Mercado (ex: taxa de conversão do setor)
- **Métricas:** Visitas → Trials → Pagantes → Base Ativa
- **Anotações:**
  - Delta de conversão entre Real e Benchmark
  - Crescimento da base (M1 vs M36)

#### C. Legenda "Como Ler"
```text
**COMO LER ESTE GRÁFICO:**
1. **Barras Escuras:** Representam nossa projeção conservadora (cenário "Real").
2. **Barras Cinza ao Fundo:** Representam o benchmark de mercado (cenário "Ideal").
3. **Eixo X:** Volume em escala logarítmica (para ver 14.000 visitas e 6 vendas no mesmo gráfico).
4. **Coluna Central:** Mostra o Delta (diferença) entre Real e Benchmark.
5. **Regra de Ouro:** Se a barra escura preencher a cinza, atingimos o benchmark.

**Se você só tiver 30 segundos:** Olhe para a taxa de conversão Trial→Pago e compare com o benchmark (15%).
```

#### D. Tabela Auxiliar
| Mês | Conversão Real | Benchmark | Δ (Delta) | Status |
|-----|----------------|-----------|-----------|--------|
| M1  | 8.0%           | 15%       | -7.0 p.p. | 🔴 |
| M6  | 12.0%          | 15%       | -3.0 p.p. | 🟡 |
| M12 | 14.5%          | 15%       | -0.5 p.p. | 🟢 |
| M36 | 16.0%          | 15%       | +1.0 p.p. | 🟢 |

#### E. Insight Estratégico
```text
**INSIGHT ESTRATÉGICO:**
1. **FATO:** A conversão Trial→Pago está em 16% no M36, superando o benchmark de 15%.
2. **CAUSA:** O onboarding automatizado (semana 8) aumentou a ativação em 25%.
3. **IMPLICAÇÃO:** Cada 1% de melhoria na conversão gera +R$ 3k/mês de MRR.
4. **AÇÃO:** Manter investimento em educação do usuário (P1).
```

#### F. Metadados JSON
```json
{
  "chart_id": "pg2_viz1_funil_macro",
  "section": "growth_machine",
  "page_number": 2,
  "title_simple": "O volume sustenta a operação?",
  "data_source": "df_real_m",
  "benchmark_source": "benchmarks_saas_b2c",
  "files": {
    "png_path": "outputs/figs/pg2_viz1_funil_macro.png",
    "json_path": "outputs/metadata/pg2_viz1.json",
    "table_path": "outputs/tables/pg2_viz1_tabela.html"
  },
  "validation_status": "ok"
}
```

---

### VIZ 2.2: EFICIÊNCIA UNITÁRIA (Ato 2) — **NOVA**

**Substituiu:** Antiga VIZ 2.2 (Mix de Canais) → Move para VIZ 2.3 ou remove

#### A. Conteúdo Textual
```python
TÍTULO_COLOQUIAL = "Cada cliente novo paga o custo de aquisição rápido o suficiente?"
TÍTULO_TÉCNICO = "LTV/CAC Ratio: Conservador vs Benchmark SaaS B2C (M0-M36)"
FONTE_DADOS = "df_real_m (Conservador) + SaaS Benchmarks (LTV/CAC 3x)"
```

#### B. Gráfico Principal
- **Tipo:** Line Chart com duas linhas + área de referência
- **Séries:**
  - **Linha Preta Sólida:** LTV/CAC Real (Conservador)
  - **Linha Verde Tracejada:** Benchmark (3x)
  - **Área Sombreada (Verde Claro):** Zona saudável (>3x)
  - **Área Sombreada (Vermelha Claro):** Zona de risco (<1.5x)
- **Período:** M0 a M36 (mensal)

#### C. Legenda "Como Ler"
```text
**COMO LER ESTE GRÁFICO:**
1. **Linha Preta:** Nosso LTV/CAC real (cenário conservador).
2. **Linha Verde Tracejada:** Benchmark do mercado (3x).
3. **Zona Verde:** Valores acima de 3x indicam saúde financeira.
4. **Zona Vermelha:** Valores abaixo de 1.5x indicam queima insustentável.

**Se você só tiver 30 segundos:** Veja quando a linha preta cruza a verde (benchmark atingido).
```

#### D. Tabela Auxiliar
| Mês | LTV/CAC Real | Benchmark | Δ (Delta) | Status |
|-----|--------------|-----------|-----------|--------|
| M6  | 1.8x         | 3.0x      | -1.2x     | 🔴 |
| M12 | 2.5x         | 3.0x      | -0.5x     | 🟡 |
| M24 | 3.2x         | 3.0x      | +0.2x     | 🟢 |
| M36 | 4.1x         | 3.0x      | +1.1x     | 🟢 |

#### E. Insight Estratégico
```text
**INSIGHT ESTRATÉGICO:**
1. **FATO:** LTV/CAC atingiu 4.1x no M36, superando o benchmark de 3x.
2. **CAUSA:** Redução do CAC pago (de R$ 250 para R$ 180) via SEO.
3. **IMPLICAÇÃO:** Cada R$ 1 investido retorna R$ 4.10 em LTV.
4. **AÇÃO:** Expandir investimento em canais com CAC baixo (P0).
```

---

### VIZ 2.3: CONTROLE TÁTICO SEMANAL (Ato 3) — **NOVA E OBRIGATÓRIA**

**Esta é a visualização obrigatória com granularidade SEMANAL (0-24 semanas)**

#### A. Conteúdo Textual
```python
TÍTULO_COLOQUIAL = "Houve descontrole de custos nas primeiras 24 semanas?"
TÍTULO_TÉCNICO = "CAC Semanal: Volatilidade vs Limites de Controle (Semanas 0-24)"
FONTE_DADOS = "df_semanal (Simulação Conservadora) + UCL/LCL (Controle Estatístico)"
```

#### B. Gráfico Principal
- **Tipo:** Line Chart com faixas de controle
- **Eixo X:** Semanas (0 a 24)
- **Eixo Y:** CAC (R$)
- **Séries:**
  - **Linha Preta Sólida:** CAC semanal real
  - **Linha Verde Tracejada:** Meta de CAC (ex: R$ 200)
  - **Faixa Sombreada (Cinza):** Limites de controle (±2σ)
  - **Pontos Vermelhos:** Semanas fora dos limites (alertas)
- **Anotações:**
  - Seta apontando para semana de maior volatilidade
  - Texto: "Semana 8: Pico corrigido em 3 dias"

#### C. Legenda "Como Ler"
```text
**COMO LER ESTE GRÁFICO:**
1. **Linha Preta:** CAC real semana a semana.
2. **Linha Verde Tracejada:** Meta de CAC (R$ 200).
3. **Faixa Cinza:** Variação aceitável (±2 desvios padrão).
4. **Pontos Vermelhos:** Semanas com CAC fora dos limites.
5. **Setas:** Indicam correções realizadas.

**Se você só tiver 30 segundos:** Conte quantos pontos vermelhos existem. Menos = melhor controle.
```

#### D. Tabela Auxiliar
| Semana | CAC Real | Meta | Δ (Delta) | Status |
|--------|----------|------|-----------|--------|
| S4     | R$ 350   | R$ 200 | +R$ 150 (75%) | 🔴 |
| S8     | R$ 420   | R$ 200 | +R$ 220 (110%) | 🔴 PICO |
| S12    | R$ 180   | R$ 200 | -R$ 20 (-10%) | 🟢 |
| S24    | R$ 190   | R$ 200 | -R$ 10 (-5%) | 🟢 |

#### E. Insight Estratégico
```text
**INSIGHT ESTRATÉGICO:**
1. **FATO:** Houve 2 semanas com CAC acima do limite (S4 e S8).
2. **CAUSA:** Campanha de lançamento no Instagram com CPC 40% maior.
3. **IMPLICAÇÃO:** Queima extra de R$ 3.500 nas 2 semanas.
4. **AÇÃO:** Implementar alertas automáticos de CAC semanal (P0).
```

---

### VIZ 2.4: CURVA DE ESCALA (Ato 4)

**Baseada na antiga VIZ 2.3 (Elasticidade)**

#### A. Conteúdo Textual
```python
TÍTULO_COLOQUIAL = "Se eu dobrar o investimento em marketing, o retorno também dobra?"
TÍTULO_TÉCNICO = "Curva de Retorno Marginal (MEF): Investimento vs Clientes | Color-Coded"
FONTE_DADOS = "df_real_m (Conservador) + Regressão Polinomial"
```

#### B. Gráfico Principal
- **Mantém** a especificação da VIZ 2.3 original (Scatter + Curva de Saturação)
- **Adiciona:**
  - **Ghost Line (Tracejada):** Curva ideal (retorno linear)
  - **Ponto de Saturação:** Anotação "Saturação em R$ 50k"

#### C. Tabela Auxiliar — **COM DELTA**
| Investimento | Clientes Real | Clientes Ideal | Δ (Delta) | Zona |
|--------------|---------------|----------------|-----------|------|
| R$ 5k        | 80            | 100            | -20 (-20%) | 🟡 |
| R$ 20k       | 350           | 400            | -50 (-12%) | 🟢 |
| R$ 50k       | 550           | 1000           | -450 (-45%) | 🔴 |

---

### VIZ 2.5: VAZAMENTO INVISÍVEL (Ato 5)

**Baseada na antiga VIZ 2.4 (Churn) + VIZ 2.5 (Payback)**

#### A. Conteúdo Textual
```python
TÍTULO_COLOQUIAL = "Quanto dinheiro estamos perdendo por cancelamentos?"
TÍTULO_TÉCNICO = "Custo Financeiro do Churn: Conservador vs Meta de Retenção (M0-M36)"
FONTE_DADOS = "df_real_m (Conservador) + Benchmark Retenção 94%"
```

#### B. Gráfico Principal
- **Tipo:** Diverging Bar Chart (Novos ↑ vs Churn ↓) + Área de Perda Financeira
- **Adiciona:**
  - **Ghost Bars (Fundo):** Meta de retenção (94%)
  - **Área Vermelha:** Perda financeira (Churn × LTV)

#### C. Tabela Auxiliar — **COM DELTA**
| Mês | Churn Real | Meta | Δ (Delta) | Perda (R$) | Status |
|-----|------------|------|-----------|------------|--------|
| M6  | 10%        | 6%   | +4 p.p.   | R$ 8k      | 🔴 |
| M12 | 7%         | 6%   | +1 p.p.   | R$ 12k     | 🟡 |
| M36 | 5.5%       | 6%   | -0.5 p.p. | R$ 45k     | 🟢 |

---

## 🔧 3. CHECKLIST DE IMPLEMENTAÇÃO

### 3.1 Para Cada Visualização

- [ ] **Título Duplo** presente (Coloquial + Técnico)
- [ ] **Fonte dos Dados** especificada no título
- [ ] **Comparação Real vs Ideal** visualmente clara (sólido vs tracejado)
- [ ] **Tabela** com colunas: Período | Real | Ideal | Delta | Status
- [ ] **Insight** segue template: Fato → Causa → Implicação → Ação
- [ ] **Metadados JSON** gerados em `outputs/metadata/`
- [ ] **PNG 300dpi** salvo em `outputs/figs/`
- [ ] **Tabela HTML** salva em `outputs/tables/`
- [ ] **Fundo branco puro** (#FFFFFF)
- [ ] **Cores** seguem paleta (máximo 4 por página)

### 3.2 Para a Página Completa

- [ ] **VIZ 2.3** usa granularidade **SEMANAL (0-24)**
- [ ] **Cabeçalho** com Big Numbers (KPIs principais)
- [ ] **Conclusão** conecta os 5 atos em frase jurídica
- [ ] **Código integrado** ao notebook `real_vs_ideal.ipynb`

---

## 📐 4. ESTRUTURA DE ARQUIVOS ESPERADA

```
notebooks/
├── outputs/
│   ├── figs/
│   │   ├── pg2_viz1_funil_macro.png
│   │   ├── pg2_viz2_ltv_cac.png
│   │   ├── pg2_viz3_cac_semanal.png  ← NOVO (OBRIGATÓRIO)
│   │   ├── pg2_viz4_elasticidade.png
│   │   └── pg2_viz5_churn_custo.png
│   ├── metadata/
│   │   ├── pg2_viz1.json
│   │   ├── pg2_viz2.json
│   │   ├── pg2_viz3.json  ← NOVO
│   │   ├── pg2_viz4.json
│   │   └── pg2_viz5.json
│   └── tables/
│       ├── pg2_viz1_tabela.html
│       ├── pg2_viz2_tabela.html
│       ├── pg2_viz3_tabela.html  ← NOVO
│       ├── pg2_viz4_tabela.html
│       └── pg2_viz5_tabela.html
├── modelo2_v7.py  ← NOVA VERSÃO
└── real_vs_ideal.ipynb  ← INTEGRAR
```

---

## 🚀 5. BLOCO DE CONCLUSÃO (VEREDITO)

**Template obrigatório para o rodapé da página:**

```text
🔍 VEREDITO ANALÍTICO DA PÁGINA:

"Nesta análise de GROWTH MACHINE, nós provamos que:

1. O modelo PASSA no teste macro de viabilidade (Viz 2.1).
   → Conversão Trial→Pago de 16% supera benchmark de 15%.

2. A operação mantém saúde unitária com LTV/CAC de 4.1x (Viz 2.2).
   → Cada R$ 1 investido retorna R$ 4.10.

3. Demonstramos controle tático ao corrigir a volatilidade da semana 8 em 3 dias (Viz 2.3).
   → Apenas 2 semanas fora dos limites em 24.

4. Identificamos que podemos escalar até R$ 30k antes de saturar (Viz 2.4).
   → Além disso, o CAC marginal dobra.

5. E mapeamos o risco crítico de Churn que custa R$ 45k/ano (Viz 2.5).
   → Reduzir 1 p.p. economiza R$ 15k/ano."
```

---

## 📋 6. PRÓXIMOS PASSOS

**✅ CONCLUÍDO:**
1. ~~**Adicionar dados semanais** ao motor de simulação~~ → **FEITO!** (`motor_granularidade.py`)

**🔄 EM ANDAMENTO:**
2. **Criar `modelo2_v7.py`** com as novas especificações
3. **Gerar benchmarks** de mercado para comparação (`df_ideal` já disponível)
4. **Integrar ao notebook** `real_vs_ideal.ipynb`
5. **Validar com checklist** completo

---

## 📊 7. DADOS DISPONÍVEIS PARA IMPLEMENTAÇÃO

### DataFrames Gerados pelo Motor V2.0

| DataFrame | Granularidade | Período | Linhas | Cenário | Arquivo |
|-----------|---------------|---------|--------|---------|---------|
| `df_real_m` | Mensal | M1-M36 | 36 | Conservador | `celula_5A_bootstrap_real.py` |
| `df_real_s` | **Semanal** | S1-S26 | 26 | Conservador | `celula_5A_bootstrap_real.py` |
| `df_real_d` | **Diário** | D1-D180 | 180 | Conservador | `celula_5A_bootstrap_real.py` |
| `df_ideal` | Mensal | M1-M36 | 36 | Benchmark | `celula_5B_cenario_ideal.py` |
| `df_ideal_s` | **Semanal** | S1-S26 | 26 | Benchmark | `celula_5B_cenario_ideal.py` |
| `df_ideal_d` | **Diário** | D1-D180 | 180 | Benchmark | `celula_5B_cenario_ideal.py` |

### Módulo de Granularidade

```
notebooks/celulas/motor_granularidade.py
```

**Funções disponíveis:**
- `gerar_granularidade_semanal(df_mensal, premissas, meses=6)` → `df_semanal`
- `gerar_granularidade_diaria(df_mensal, premissas, meses=6)` → `df_diario`
- `expandir_granularidade_completa(df_mensal, premissas)` → `(df_s, df_d)`

### Uso para VIZ 2.3 (Controle Tático Semanal)

```python
# Dados para o gráfico semanal:
semanas = df_real_s['semana']  # 1-26
cac_semanal = df_real_s['cac_blended']  # CAC por semana
meta_cac = df_ideal_s['cac_blended']  # Benchmark por semana

# Limites de controle (calculados):
media_cac = cac_semanal.mean()
std_cac = cac_semanal.std()
ucl = media_cac + 2 * std_cac  # Upper Control Limit
lcl = media_cac - 2 * std_cac  # Lower Control Limit
```

---

**Versão:** V7.1 (Atualizado com dados semanais/diários)  
**Data:** 2025-12-06  
**Autor:** [Gemini/Claude]  
**Status:** ✅ DADOS DISPONÍVEIS - PRONTO PARA IMPLEMENTAÇÃO DAS VISUALIZAÇÕES
