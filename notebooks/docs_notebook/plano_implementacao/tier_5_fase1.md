# 🚀 PLANO EXECUTIVO DEFINITIVO V17.0 - PÁGINA 5: RISCO & CENÁRIOS
**Tier 5 - Enterprise Gold Standard | Fusão Completa dos 4 Planos**

**Status:** Documento Único e Definitivo para Implementação  
**Objetivo:** Guia completo, linha por linha, para desenvolvimento de código, gráficos e tabelas  
**Tempo de Leitura do Investidor:** 15 minutos  
**Decisão:** Quantificar risco, provar robustez, vender proteção de downside

---

## 📋 ÍNDICE DE NAVEGAÇÃO

```
PARTE 1: FUNDAMENTOS
  1.1 Filosofia Central da Página 5
  1.2 Mandamentos Invioláveis (10 Regras)
  1.3 Arquitetura de Dados (Inputs/Outputs)

PARTE 2: ESTRUTURA VISUAL
  2.1 Tabela Executiva Master de Risco
  2.2 KPI Cards de Risco (4 Cards)

PARTE 3: ARCO DE 5 ATOS (VISUALIZAÇÕES PRINCIPAIS)
  ATO 1: Monte Carlo Fan Chart (Tese Macro)
  ATO 2: Tornado Plot LTV/CAC (Saúde Unitária)
  ATO 3: Heatmap Runway Semanal (Tático)
  ATO 4: Break-Even sob Estresse (Escala)
  ATO 5: Gap Analysis Real vs Estresse (Vazamento)

PARTE 4: ANEXOS TÉCNICOS
  4.1 Glossário de Risco
  4.2 Metodologia Monte Carlo
  4.3 Pseudocódigo do Engine
  4.4 Estrutura JSON Completa
```

---

---

# PARTE 1: FUNDAMENTOS

---

## 1.1 FILOSOFIA CENTRAL DA PÁGINA 5

A Página 5 é o **teste de estresse do modelo de negócios**. Aqui não vendemos sonho - vendemos **proteção de downside** e **quantificação de risco**.

**Pergunta Central:**  
*"Se tudo der errado, o que acontece? E se der certo, até onde vamos?"*

**Mundos Paralelos:**
- **Mundo A (Real/5A):** Cenário conservador (bootstrap R$ 2k/mês)
- **Mundo B (Ideal/5B):** Cenário benchmark (mercado elite)
- **Mundo C (Estresse/5C):** Cenário catastrófico (cisne negro)

**Narrativa:**  
"Provamos que mesmo no cenário Real (conservador), há 95% de chance de sobrevivência. No Ideal, há upside de 3-5x. No Estresse, identificamos os pontos de quebra e mostramos como mitigar."

---

## 1.2 MANDAMENTOS INVIOLÁVEIS (10 REGRAS)

### **Mandamentos Globais (1-5)**

1. **Filosofia Dual:** Todo gráfico compara Mundo A (Real) vs Mundo B (Ideal)
2. **Arco de 5 Atos:** Tese → Saúde → Tático → Escala → Risco (ordem fixa)
3. **6 Elementos Atômicos:** Cada visualização tem:
   - Título Duplo (Coloquial + Técnico)
   - Gráfico Principal
   - "Como Ler" (Legenda Didática)
   - Tabela Executiva
   - Insight (Fato → Causa → Implicação → Ação)
   - Auditoria (Fórmulas + JSON)
4. **Print-First:** Fundo branco, sem sombras, exportável PDF/DOCX
5. **Acionabilidade:** Todo insight termina com ação concreta (R$ ou % exatos)

### **Mandamentos Específicos Página 5 (6-10)**

6. **Três Mundos Obrigatórios:** Real (5A) + Ideal (5B) + Estresse (5C)
7. **Monte Carlo Mínimo:** 10.000 simulações com seed fixo (reprodutibilidade)
8. **Probabilidades Explícitas:** Sempre mostrar P5/P10/P25/P50/P75/P90/P95
9. **VaR e CVaR:** Obrigatório calcular Value at Risk (95%) e Conditional VaR
10. **Mitigação Quantificada:** Cada risco = ação com impacto financeiro calculado

---

## 1.3 ARQUITETURA DE DADOS

### **INPUTS (O que você já tem)**

```python
# DataFrames Principais
df_real_m      # Cenário Real (5A) - Mensal (36 linhas)
df_real_s      # Cenário Real (5A) - Semanal (156 linhas)
df_ideal_m     # Cenário Ideal (5B) - Mensal (36 linhas)
df_ideal_s     # Cenário Ideal (5B) - Semanal (156 linhas)

# Premissas
PREMISSAS      # Dicionário com 150+ parâmetros

# Monte Carlo (já existe)
mc_results     # DataFrame com 10.000 simulações
```

### **OUTPUTS (O que vai gerar)**

```python
# Novos DataFrames
df_stress_m         # Cenário Estresse (5C) - Mensal
df_tornado          # Análise de Sensibilidade (12 premissas)
df_runway_semanal   # Probabilidade de Runway < 4 semanas
df_breakeven        # Break-even em 3 cenários

# Tabelas Executivas
tabela_executiva_risco    # Resumo de todas as métricas de risco
tabela_probabilidades     # P5/P10/.../P95 para todas as métricas
tabela_tornado            # Impacto de cada premissa no LTV/CAC
tabela_breakeven          # Mês de break-even por cenário

# Gráficos (Figuras)
fig_fan_chart           # Monte Carlo (caixa ao longo do tempo)
fig_tornado             # Sensibilidade (barras horizontais)
fig_runway_heatmap      # Heatmap 26 semanas × 3 cenários
fig_breakeven           # 3 linhas (Pessimista/Base/Otimista)
fig_gap_analysis        # Área entre Real e Estresse

# Metadados JSON
metadata_pag5.json      # Todos os parâmetros e resultados
```

---

---

# PARTE 2: ESTRUTURA VISUAL (EXECUTIVE SUMMARY)

---

## 2.1 TABELA EXECUTIVA MASTER DE RISCO

**Objetivo:** Snapshot de 3 minutos - o investidor vê tudo de uma vez

**Localização:** Topo da página, antes dos gráficos

**Estrutura:** 25 linhas × 9 colunas

### **CÓDIGO DE CONSTRUÇÃO**

```python
def gerar_tabela_executiva_risco(df_real_m, df_ideal_m, mc_results, df_stress_m):
    """
    Gera a Tabela Executiva Master de Risco
    
    Inputs:
        - df_real_m: Cenário Real mensal
        - df_ideal_m: Cenário Ideal mensal
        - mc_results: Resultados Monte Carlo (10k sims)
        - df_stress_m: Cenário Estresse mensal
    
    Output:
        - DataFrame formatado com 25 métricas de risco
    """
    
    # Extrair dados finais (M36)
    real_final = df_real_m.iloc[-1]
    ideal_final = df_ideal_m.iloc[-1]
    stress_final = df_stress_m.iloc[-1]
    
    # Calcular percentis do Monte Carlo
    p5 = mc_results['caixa_final'].quantile(0.05)
    p50 = mc_results['caixa_final'].quantile(0.50)
    p95 = mc_results['caixa_final'].quantile(0.95)
    var95 = p5  # Value at Risk (pior 5%)
    cvar95 = mc_results[mc_results['caixa_final'] < var95]['caixa_final'].mean()
    
    # Probabilidades
    prob_quebra = (mc_results['caixa_final'] < 0).mean()
    prob_caixa_50k = (mc_results['caixa_final'] < 50000).mean()
    prob_caixa_100k = (mc_results['caixa_final'] > 100000).mean()
    prob_arr_1m = (mc_results['arr_final'] > 1000000).mean()
    prob_ltv_cac_5x = (mc_results['ltv_cac_final'] > 5).mean()
    prob_churn_5 = (mc_results['churn_medio'] < 0.05).mean()
    
    # Construir tabela
    tabela = pd.DataFrame({
        'Categoria': [
            '🎲 PROBABILIDADES', '', '', '', '', '', '',
            '💰 CENÁRIO REAL (5A)', '', '', '', '',
            '🌟 CENÁRIO IDEAL (5B)', '', '', '', '',
            '⚠️ CENÁRIO ESTRESSE (5C)', '', '', '', '',
            '📊 MONTE CARLO', '', '', ''
        ],
        'Métrica': [
            'Caixa < R$ 0 (Quebra)', 'Caixa < R$ 50k (Risco)', 'Caixa > R$ 100k (Seguro)',
            'ARR > R$ 1M (Meta)', 'LTV/CAC > 5x', 'Churn < 5%', '',
            'Caixa Final', 'ARR Final', 'MRR Final', 'LTV/CAC', 'Churn Médio',
            'Caixa Final', 'ARR Final', 'MRR Final', 'LTV/CAC', 'Churn Médio',
            'Caixa Final', 'ARR Final', 'MRR Final', 'LTV/CAC', 'Churn Médio',
            'VaR 95%', 'CVaR 95%', 'P50 (Mediana)', 'Dispersão (P95-P5)'
        ],
        'Valor': [
            f'{prob_quebra:.1%}', f'{prob_caixa_50k:.1%}', f'{prob_caixa_100k:.1%}',
            f'{prob_arr_1m:.1%}', f'{prob_ltv_cac_5x:.1%}', f'{prob_churn_5:.1%}', '',
            formatar_moeda(real_final['caixa']), formatar_moeda(real_final['arr']),
            formatar_moeda(real_final['mrr']), f"{real_final['ltv_cac']:.1f}x",
            f"{real_final['churn']:.1%}",
            formatar_moeda(ideal_final['caixa']), formatar_moeda(ideal_final['arr']),
            formatar_moeda(ideal_final['mrr']), f"{ideal_final['ltv_cac']:.1f}x",
            f"{ideal_final['churn']:.1%}",
            formatar_moeda(stress_final['caixa']), formatar_moeda(stress_final['arr']),
            formatar_moeda(stress_final['mrr']), f"{stress_final['ltv_cac']:.1f}x",
            f"{stress_final['churn']:.1%}",
            formatar_moeda(var95), formatar_moeda(cvar95), formatar_moeda(p50),
            formatar_moeda(p95 - p5)
        ],
        'Benchmark': [
            '< 10%', '< 20%', '> 50%', '> 60%', '> 30%', '> 15%', '',
            '> R$ 50k', '> R$ 1M', '> R$ 50k', '> 3.0x', '< 7%',
            '> R$ 100k', '> R$ 1.5M', '> R$ 100k', '> 5.0x', '< 5%',
            'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
            '> -R$ 50k', '> -R$ 100k', '> R$ 50k', '< R$ 200k'
        ],
        'Status': [
            '🟢' if prob_quebra < 0.10 else '🔴',
            '🟢' if prob_caixa_50k < 0.20 else '🔴',
            '🟢' if prob_caixa_100k > 0.50 else '🔴',
            '🟢' if prob_arr_1m > 0.60 else '🟡',
            '🟢' if prob_ltv_cac_5x > 0.30 else '🟡',
            '🟡' if prob_churn_5 > 0.15 else '🔴',
            '',
            '🟢' if real_final['caixa'] > 50000 else '🟡',
            '🟢' if real_final['arr'] > 1000000 else '🟡',
            '🟢' if real_final['mrr'] > 50000 else '🟡',
            '🟢' if real_final['ltv_cac'] > 3 else '🔴',
            '🟡' if real_final['churn'] < 0.07 else '🔴',
            '🟢', '🟢', '🟢', '🟢', '🟢',
            '🔴' if stress_final['caixa'] < 0 else '🟡',
            '🔴', '🔴', '🔴', '🔴',
            '🟢' if var95 > -50000 else '🔴',
            '🟢' if cvar95 > -100000 else '🔴',
            '🟢' if p50 > 50000 else '🟡',
            '🟢' if (p95-p5) < 200000 else '🟡'
        ]
    })
    
    return tabela
```

### **OUTPUT VISUAL**

```markdown
====================================================================================================
📊 PAINEL EXECUTIVO DE RISCO - SAM INVESTIMENTOS (ANÁLISE 36 MESES)
====================================================================================================
Categoria           Métrica                          Valor        Benchmark      Status
────────────────────────────────────────────────────────────────────────────────────────────────
🎲 PROBABILIDADES
                    Caixa < R$ 0 (Quebra)            4,8%         < 10%          🟢
                    Caixa < R$ 50k (Risco)           18,2%        < 20%          🟢
                    Caixa > R$ 100k (Seguro)         52,3%        > 50%          🟢
                    ARR > R$ 1M (Meta)               64,7%        > 60%          🟢
                    LTV/CAC > 5x                     38,9%        > 30%          🟢
                    Churn < 5%                       18,4%        > 15%          🟡

💰 CENÁRIO REAL (5A - Bootstrap R$ 2k/mês)
                    Caixa Final                      R$ 81.552    > R$ 50k       🟢
                    ARR Final                        R$ 1.353.863 > R$ 1M        🟢
                    MRR Final                        R$ 112.822   > R$ 50k       🟢
                    LTV/CAC                          5,1x         > 3.0x         🟢
                    Churn Médio                      7,0%         < 7%           🟡

🌟 CENÁRIO IDEAL (5B - Benchmark Mercado)
                    Caixa Final                      R$ 287.300   > R$ 100k      🟢
                    ARR Final                        R$ 2.180.000 > R$ 1.5M      🟢
                    MRR Final                        R$ 181.667   > R$ 100k      🟢
                    LTV/CAC                          8,9x         > 5.0x         🟢
                    Churn Médio                      4,2%         < 5%           🟢

⚠️ CENÁRIO ESTRESSE (5C - Cisne Negro)
                    Caixa Final                      -R$ 15.200   N/A            🔴
                    ARR Final                        R$ 620.000   N/A            🔴
                    MRR Final                        R$ 51.667    N/A            🔴
                    LTV/CAC                          1,8x         N/A            🔴
                    Churn Médio                      14,2%        N/A            🔴

📊 MONTE CARLO (10.000 Simulações)
                    VaR 95% (Pior 5%)                -R$ 12.500   > -R$ 50k      🟢
                    CVaR 95% (Média Pior 5%)         -R$ 18.300   > -R$ 100k     🟢
                    P50 (Mediana)                    R$ 81.550    > R$ 50k       🟢
                    Dispersão (P95-P5)               R$ 228.300   < R$ 200k      🟡
====================================================================================================

🟢 = Excelente (acima benchmark)  |  🟡 = Atenção (próximo ao limite)  |  🔴 = Crítico (abaixo)

**INTERPRETAÇÃO RÁPIDA:**
- ✅ Risco de quebra < 5% (95% de sobrevivência garantida)
- ✅ Cenário Real atinge todas as metas principais
- ⚠️ Dispersão alta indica incerteza no upside
- 🔴 Cenário Estresse mostra fragilidade em churn dobrado
```

---

## 2.2 KPI CARDS DE RISCO (4 Cards)

**Objetivo:** Destacar visualmente as 4 métricas hero de risco

**Localização:** Logo abaixo da tabela executiva

### **ESTRUTURA DOS CARDS**

```python
def gerar_kpi_cards_risco(mc_results, df_real_m):
    """
    Gera 4 KPI Cards de Risco
    """
    
    # Card 1: Probabilidade de Sobrevivência
    prob_sobrevivencia = (mc_results['caixa_final'] > 0).mean()
    card1 = {
        'titulo': '🛡️ SOBREVIVÊNCIA',
        'valor': f'{prob_sobrevivencia:.1%}',
        'subtitulo': 'Prob. Caixa > R$ 0',
        'delta': f'+{(prob_sobrevivencia - 0.90):.1%} vs meta 90%',
        'status': '🟢' if prob_sobrevivencia > 0.90 else '🔴'
    }
    
    # Card 2: VaR 95%
    var95 = mc_results['caixa_final'].quantile(0.05)
    card2 = {
        'titulo': '⚠️ VAR 95%',
        'valor': formatar_moeda(var95),
        'subtitulo': 'Pior Cenário (5%)',
        'delta': f'{abs(var95)/1000:.0f}k vs limite -50k',
        'status': '🟢' if var95 > -50000 else '🔴'
    }
    
    # Card 3: Upside Potential
    p95 = mc_results['caixa_final'].quantile(0.95)
    p50 = mc_results['caixa_final'].quantile(0.50)
    upside = (p95 / p50) - 1
    card3 = {
        'titulo': '🚀 UPSIDE',
        'valor': f'{upside:.0%}',
        'subtitulo': 'P95 vs P50',
        'delta': f'{upside:.0%} potencial acima mediana',
        'status': '🟢' if upside > 1.0 else '🟡'
    }
    
    # Card 4: Dispersão (Incerteza)
    p5 = mc_results['caixa_final'].quantile(0.05)
    dispersao = (p95 - p5) / p50
    card4 = {
        'titulo': '📊 DISPERSÃO',
        'valor': f'{dispersao:.1f}x',
        'subtitulo': 'Incerteza (P95-P5)/P50',
        'delta': 'Alta incerteza' if dispersao > 3 else 'Incerteza controlada',
        'status': '🟡' if dispersao > 3 else '🟢'
    }
    
    return [card1, card2, card3, card4]
```

### **OUTPUT VISUAL**

```markdown
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│  🛡️ SOBREVIVÊNCIA │  ⚠️ VAR 95%      │  🚀 UPSIDE       │  📊 DISPERSÃO    │
│  95,2%           │  -R$ 12.500      │  +164%           │  2,8x            │
│  Prob. Caixa>0   │  Pior 5%         │  P95 vs P50      │  (P95-P5)/P50    │
│  ▲ +5,2% vs 90%  │  13k vs -50k ✅  │  164% potencial  │  Controlada      │
│  Status: 🟢      │  Status: 🟢      │  Status: 🟢      │  Status: 🟢      │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

---