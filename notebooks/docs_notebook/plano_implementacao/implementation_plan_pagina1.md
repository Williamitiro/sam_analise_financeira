# 📋 PLANO DE IMPLEMENTAÇÃO - PÁGINA 1: EXECUTIVE COCKPIT

**Versão:** 4.0 (FINAL - COM FEEDBACKS)**
**Data:** 2025-12-05
**Status:** ✅ APROVADO - Iniciando Implementação

---

## 🔄 FEEDBACKS INCORPORADOS

| Feedback | Decisão |
|----------|--------|
| 2 eixos (MRR + Usuários) | ✅ Eixo Y esquerdo: R$ / Eixo Y direito: Usuários (0-1000) |
| Sem linhas retas | ✅ Adicionar ruído/suavização para parecer real |
| Explicar siglas | ✅ MoM = Mês a Mês, sempre explicar |
| Growth Rate inovador | ✅ Gráfico Marketing vs MRR (eficiência) |
| Insights dinâmicos | ✅ 100% baseado em lógica condicional |
| save_timeseries | ✅ Já ativado pelo usuário |
| df_ideal obrigatório | ✅ Verificar existência, se não existir usar met_ideal |

---

## 🎯 OBJETIVO

Implementar a **Página 1: Executive Cockpit** 100% dinâmico, ZERO hardcoded.

---

## 📊 DADOS CONFIRMADOS (Fonte: `METADADOS_NOTEBOOK_COMPLETO.json`)

### Snapshots Temporais do `df_real_m`:

| Métrica | M1 | M6 | M12 | M36 | Benchmark |
|---------|------|------|------|------|-----------|
| **MRR** | R$ 579 | R$ 1.498 | R$ 3.576 | **R$ 34.674** | > R$ 83k |
| **Usuários** | 6 | 16 | 37 | **363** | > 1.000 |
| **Caixa** | R$ 4.603 | R$ 9.380 | R$ 17.660 | **R$ 88.786** | > R$ 50k |
| **Churn** | 12.0% | 11.25% | 10.35% | **6.75%** | < 5.0% |
| **CAC** | R$ 1.000 | R$ 365 | R$ 209 | **R$ 273** | < R$ 250 |
| **LTV/CAC** | 0.64x | 1.69x | 3.34x | **3.92x** | > 3.0x |
| **Runway** | 3.5m | 4.6m | 7.0m | **3.5m** | > 12m |
| **Burn Rate** | R$ 1.397 | R$ 751 | R$ 0 | **R$ 0** | < R$ 0 |
| **Margem Bruta** | 80.0% | 74.0% | 74.6% | **75.7%** | > 70% |
| **EBITDA** | -R$ 1.396 | -R$ 751 | R$ 543 | **R$ 4.220** | > 0 |

### Cenário Ideal (`df_ideal`) para comparação:
- MRR M36: **R$ 238.950**
- Usuários M36: **2.497**
- LTV/CAC M36: **8.56x**

### Monte Carlo (`mc_results` - 150 simulações):
- Colunas: `scenario`, `mrr_final`, `usuarios_final`, `caixa_final`, `ltv_cac`
- Cenários: `pessimista`, `base`, `otimista` (50 sims cada)

---

## 📐 ESTRUTURA PADRÃO POR CÉLULA (Diretrizes.md §2)

Cada componente **DEVE** ter os 5 blocos nesta ordem:

| Bloco | Descrição | Requisito |
|-------|-----------|-----------|
| **A** | Título Duplo | Simples (pergunta) + Técnico (método) |
| **B** | Gráfico/Tabela | DPI 300, figsize config, cores padronizadas |
| **C** | Legenda "Como Ler" | Template com 5 pontos + Regra de Ouro |
| **D** | Insight Estratégico | 3 destaques (métrica → implicação → ação) |
| **E** | Metadados | JSON com celula_id, dados_fonte, export_path |

---

## 🎨 CORES PADRONIZADAS (Diretrizes.md §2)

```python
CORES = {
    'real': '#000000',        # Preto - linha principal
    'benchmark': '#D32F2F',   # Vermelho - meta/benchmark
    'ideal': '#388E3C',       # Verde - cenário ideal
    'pessimista': '#F57C00',  # Laranja - P10
    'fundo': '#FFFFFF',       # Branco
}
```

---

## 📝 DETALHAMENTO DOS 5 COMPONENTES

---

### 📊 1.1 TABELA EXECUTIVA MASTER

**Objetivo:** Snapshot completo de todas as métricas em M1, M6, M12, M36.

**Fonte de dados:**
```python
m1 = df_real_m.iloc[0]   # Mês 1
m6 = df_real_m.iloc[5]   # Mês 6
m12 = df_real_m.iloc[11] # Mês 12
m36 = df_real_m.iloc[-1] # Mês 36
```

**Colunas a usar:**
- `mrr`, `arr`, `usuarios_ativos`, `churn_rate`, `cac_blended`, `ltv_cac`
- `caixa`, `runway_meses`, `burn_rate`, `margem_bruta_pct`, `ebitda`

**Layout:**
```
=================================================================================
📊 PAINEL EXECUTIVO COMPLETO - PROJEÇÃO 36 MESES (CENÁRIO REAL - BOOTSTRAP)
=================================================================================
Categoria       Métrica                 M1          M6          M12         M36         Benchmark    Status
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
💰 RECEITA     MRR                  R$ 579    R$ 1.498    R$ 3.576   R$ 34.674    > R$ 83k      ⚠️
               ARR                  R$ 7.0k   R$ 18.0k    R$ 42.9k   R$ 416.1k    > R$ 1M       ⚠️
...
```

**Regras de Status:**
```python
def get_status(valor, benchmark, inversao=False):
    if inversao:
        if valor <= benchmark: return '✅'
        elif valor <= benchmark * 1.3: return '⚠️'
        else: return '🔴'
    else:
        if valor >= benchmark: return '✅'
        elif valor >= benchmark * 0.7: return '⚠️'
        else: return '🔴'
```

**Estilo:** Tabela neutra (sem cores de fundo), apenas status com emojis. Fonte `Courier New` para alinhamento.

---

### 📊 1.2 KPI CARDS (4 Métricas Hero)

**Objetivo:** 4 cards visuais com as métricas mais críticas para investidores.

**Cards:**
1. **MRR M36:** R$ 34.674 | Meta: R$ 83k | Gap: -R$ 48.3k (-58%)
2. **LTV/CAC:** 3.92x | Meta: 3.0x | Status: ✅ Saudável
3. **Churn:** 6.75% | Meta: 5.0% | Gap: +1.75pp | Status: ⚠️
4. **Runway:** 3.5m | Meta: 12m | Status: ⚠️ (ATENÇÃO: baixo!)

**Tamanho:** `figsize=(14, 6)` - cards menores e compactos (2x2 grid)

**Layout de cada card:**
```
┌────────────────────────┐
│ 💰 MRR Mês 36          │
│                        │
│     R$ 34.674          │
│     ↑ 5.886% vs M1     │
│                        │
│ Meta: R$ 83.333        │
│ Gap: -R$ 48.7k (-58%)  │
│                        │
│ Status: ⚠️ ABAIXO META │
└────────────────────────┘
```

**NÃO incluir descrições extensas nos cards** - isso vai para o Bloco D (Insight).

---

### 📊 1.3 GRÁFICO TEMPORAL COM CORRELAÇÃO (2 EIXOS)

**NOVO:** Mostrar MRR + Usuários Ativos no mesmo gráfico com 2 eixos Y.

**Layout:**
- **Eixo Y Esquerdo:** MRR em R$ (escala automática)
- **Eixo Y Direito:** Usuários (escala 0 a max usuários * 1.2)

**Séries:**
- Linha preta grossa: MRR Real (com pequena oscilação para parecer natural)
- Linha verde: MRR Ideal (benchmark)
- Linha roxa tracejada: Usuários Ativos (eixo direito)
- Área sombreada cinza: Faixa P10-P90 Monte Carlo

**Para evitar linhas retas:**
```python
# Adicionar ruído suave para parecer mais natural
ruido = np.random.normal(0, mrr * 0.02, len(mrr))  # 2% de variação
mrr_visual = mrr + ruido
```

**Callouts obrigatórios:**
- M6: "Validação: R$ X.XXX | XX users"
- M12: "🎯 Break-Even Atingido"
- M36: "Gap vs Ideal: -R$ XX.XXX"

**Subplot separado (opcional):** Gráfico semanal para M0-M6

---

### 📊 1.4 TABELA DE STATUS TEMPORAL (Milestones)

**Objetivo:** Roadmap de metas com status de atingimento.

**Milestones a incluir (baseado em `df_real_m`):**

| Milestone | Meta | Real (calculado) | Status |
|-----------|------|------------------|--------|
| Primeiro Cliente | M1 | M1 | ✅ OK |
| R$ 1k MRR | M3 | Verificar df_real_m | ? |
| R$ 5k MRR | M12 | Verificar | ? |
| Break-Even | M12 | M12 (verificar lucro_liquido > 0) | ? |
| 100 Usuários | M24 | Verificar usuarios_ativos | ? |
| R$ 20k MRR | M24 | Verificar | ? |
| 300 Usuários | M36 | M36 (363 ✅) | ✅ Antes |
| LTV/CAC > 3x | M36 | M36 (3.92x ✅) | ✅ OK |

**Cálculo automático:**
```python
def encontrar_mes_milestone(df, coluna, valor):
    mask = df[coluna] >= valor
    if mask.any():
        return df[mask].iloc[0]['mes']
    return None
```

**Layout:**
```
┌────────┬─────────────────────────────────┬──────────┬────────┬──────────┐
│ Mês    │ Milestone                       │ Meta     │ Real   │ Status   │
├────────┼─────────────────────────────────┼──────────┼────────┼──────────┤
│ M3     │ 🚀 R$ 1k MRR                    │ M3       │ M5     │ ⚠️ Atraso│
│ M12    │ 💰 Break-Even                   │ M12      │ M12    │ ✅ OK    │
│ M36    │ 👥 300+ Usuários                │ M36      │ M35    │ ✅ Antes │
└────────┴─────────────────────────────────┴──────────┴────────┴──────────┘
```

---

### 📊 1.5 EFICIÊNCIA DE MARKETING (Investimento vs Retorno)

**NOVO:** Gráfico inovador mostrando correlação Marketing → MRR

**Tipo:** Gráfico de barras + linha (combo chart)

**Layout:**
- **Barras azuis:** Gasto de Marketing por mês (eixo Y esquerdo, R$)
- **Linha verde:** MRR conquistado (eixo Y direito, R$)
- **Linha vermelha:** Eficiência = MRR / Gasto (R$ de MRR por R$ investido)

**Cálculo:**
```python
eficiencia = df_real_m['mrr'] / df_real_m['gasto_marketing'].replace(0, np.nan)
# Cada R$ 1 investido gerou R$ X de MRR
```

**Insights visuais:**
- Destacar meses com melhor eficiência (ROI alto)
- Destacar meses com desperdício (muito gasto, pouco MRR)
- Tendência de eficiência ao longo do tempo

**Título explicativo:**
```
"Eficiência de Marketing: Quanto cada R$ 1 investido gerou de MRR?"
Subtítulo: "Barras = Investimento | Linha = Retorno | Meta: >5x"
```

**Alternativa:** Scatter plot com regressão (Marketing vs Novos Clientes)

---

## 📢 BLOCO D - INSIGHTS ESTRATÉGICOS 100% DINÂMICOS

**REGRA FUNDAMENTAL:** ZERO texto hardcoded. Todo insight é gerado por lógica condicional.

**Estrutura da função geradora:**
```python
def gerar_insight_dinamico(met_real, met_ideal, df_real_m):
    """
    Gera insights que mudam conforme os dados mudam.
    """
    insights = []
    
    # INSIGHT 1: LTV/CAC
    ltv_cac = met_real.get('ltv_cac_medio', 0)
    ltv_cac_ideal = met_ideal.get('ltv_cac_medio', 3.0)
    
    if ltv_cac >= 5.0:
        status = "EXCELENTE (TOP 10%)"
        acao = "Escalar agressivamente - ROI comprovado"
    elif ltv_cac >= 3.0:
        status = "SAUDÁVEL"
        acao = "Otimizar churn para melhorar LTV"
    elif ltv_cac >= 1.5:
        status = "ATENÇÃO"
        acao = "Reduzir CAC ou aumentar retenção urgente"
    else:
        status = "CRÍTICO"
        acao = "PARAR aquisição paga. Focar em retenção."
    
    insights.append({
        'titulo': 'Saúde da Unidade Econômica',
        'metrica': f'LTV/CAC = {ltv_cac:.1f}x (ideal: {ltv_cac_ideal:.1f}x)',
        'status': status,
        'implicacao': f'Cada R$ 1 em aquisição retorna R$ {ltv_cac:.2f}',
        'acao': acao
    })
    
    # INSIGHT 2: GAP MRR
    mrr_real = met_real.get('mrr_final', 0)
    mrr_ideal = met_ideal.get('mrr_final', mrr_real)
    gap = mrr_ideal - mrr_real
    gap_pct = (gap / mrr_ideal * 100) if mrr_ideal > 0 else 0
    
    if gap <= 0:
        status = "SUPERANDO META"
        acao = "Manter estratégia atual"
    elif gap_pct < 30:
        status = "PRÓXIMO DA META"
        acao = "Ajustes finos em conversão e retenção"
    else:
        status = "GAP SIGNIFICATIVO"
        custo_oportunidade = gap * 36  # 3 anos
        acao = f"R$ {custo_oportunidade:,.0f} deixados na mesa em 3 anos"
    
    insights.append({
        'titulo': 'Gap de Receita',
        'metrica': f'Real: R$ {mrr_real:,.0f} | Ideal: R$ {mrr_ideal:,.0f}',
        'gap': f'-R$ {gap:,.0f} ({gap_pct:.0f}% abaixo)',
        'status': status,
        'acao': acao
    })
    
    # ... mais insights dinâmicos
    return insights
```

---

## 📁 ARQUIVOS A GERAR

```
outputs/
├── figs/
│   ├── pg1_viz1_kpi_cards.png         # 1.2 KPI Cards
│   ├── pg1_viz2_temporal_semanal.png  # 1.3 Gráfico semanal
│   ├── pg1_viz3_temporal_mensal.png   # 1.3 Gráfico mensal
│   ├── pg1_viz4_growth_rate.png       # 1.5 Growth Rate
├── metadata/
│   └── pg1_cockpit_master.json        # Metadados completos
└── tabelas/
    ├── pg1_tabela_executiva.html      # 1.1 Tabela (styled)
    └── pg1_tabela_milestones.html     # 1.4 Milestones
```

---

## ✅ VERIFICAÇÃO

### Testes Manuais

1. **Teste de Dados:**
   - Executar célula de diagnóstico no notebook
   - Verificar que valores nos gráficos batem com `METADADOS_NOTEBOOK_COMPLETO.json`

2. **Teste Visual:**
   - Abrir cada PNG gerado
   - Verificar legibilidade (zoom 200%)
   - Confirmar cores padronizadas (#000000, #D32F2F, etc.)

3. **Teste de Completude:**
   - Cada componente tem os 5 blocos (A, B, C, D, E)?
   - Callouts presentes nos gráficos?
   - Insights estratégicos com ações concretas?

---

## ⚠️ PONTOS DE ATENÇÃO

1. **Runway vs Burn Rate:** M36 mostra burn_rate=0 mas runway=3.5m. Verificar fórmula no motor.

2. **Monte Carlo:** Se `mc_results` não tiver coluna por mês, usar apenas P10/P50/P90 finais para fan chart simplificado.

3. **Cenário Ideal:** Se `df_ideal` não existir, omitir linha verde e focar em Real + Monte Carlo.

4. **Milestones:** Calcular dinamicamente baseado nos dados, não hardcodar.

---

## 🔄 PRÓXIMOS PASSOS

1. ✅ Aprovar este plano
2. Criar arquivo `pagina1_cockpit_gold_standard_v3.py`
3. Testar no notebook
4. Iterar baseado em feedback visual
