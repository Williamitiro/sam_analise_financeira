# ATO 3: HEATMAP RUNWAY SEMANAL (TÁTICO)
########################################################################################
########################################################################################

---

## 🔷 SEÇÃO 1: CONCEITO E OBJETIVO

### **PERGUNTA CENTRAL:**
*"Em qual semana o caixa fica perigosamente baixo e precisamos agir?"*

### **OBJETIVO:**
Identificar **janelas críticas de liquidez** ao longo de 36 meses (156 semanas) em 3 cenários (Real/Ideal/Estresse), mostrando quando o runway cai abaixo de 3 meses.

### **POR QUE É IMPORTANTE:**
- Investidores querem ver **gestão proativa de caixa**
- Identifica **momentos de vulnerabilidade** antes que aconteçam
- Permite **planejar captações** com antecedência
- Mostra diferença entre **cenário conservador** (Real) e **catastrófico** (Estresse)

### **INSIGHT QUE REVELA:**
"Mesmo no cenário Real, há X semanas críticas onde runway < 3 meses. No Estresse, há Y semanas. Mas identificamos com Z meses de antecedência."

---

## 🔷 SEÇÃO 2: ARQUITETURA DE DADOS

### **INPUTS**

```python
# DataFrames Semanais (você já tem)
df_real_s      # 156 linhas (semanas 0-155)
df_ideal_s     # 156 linhas
df_stress_s    # 156 linhas (você vai gerar)

# Colunas necessárias em cada DataFrame:
# - semana: int (0 a 155)
# - caixa: float
# - receita_semanal: float
# - custos_totais_semana: float
# - burn_rate_semanal: float (custos - receita)
```

### **TRANSFORMAÇÕES**

```python
# LÓGICA DE CÁLCULO

def calcular_runway_semanal(df_semanal):
    """
    Calcula runway (em semanas) para cada semana
    
    Runway = Caixa_Atual / |Burn_Rate_Semanal_Médio_Últimas_4_Semanas|
    
    REGRAS:
    - Se burn_rate > 0 (lucrando): runway = infinito (ou 52 semanas como cap)
    - Se burn_rate < 0 (queimando): runway = caixa / abs(burn_rate)
    - Se caixa < 0: runway = 0 (já quebrou)
    """
    
    df = df_semanal.copy()
    
    # 1. Calcular burn rate semanal
    df['burn_rate_semanal'] = df['custos_totais_semana'] - df['receita_semanal']
    
    # 2. Média móvel de 4 semanas (para suavizar)
    df['burn_rate_ma4'] = df['burn_rate_semanal'].rolling(window=4, min_periods=1).mean()
    
    # 3. Calcular runway
    df['runway_semanas'] = df.apply(lambda row: 
        52 if row['burn_rate_ma4'] <= 0 else  # Lucrando ou break-even
        0 if row['caixa'] < 0 else             # Já quebrou
        row['caixa'] / abs(row['burn_rate_ma4']),  # Queimando caixa
        axis=1
    )
    
    # 4. Classificar risco (baseado no seu critério: 3 meses = 12 semanas)
    df['status_risco'] = df['runway_semanas'].apply(lambda x:
        'CRÍTICO' if x < 6 else      # < 1.5 meses
        'ATENÇÃO' if x < 12 else     # < 3 meses
        'SEGURO'                      # >= 3 meses
    )
    
    return df[['semana', 'caixa', 'burn_rate_ma4', 'runway_semanas', 'status_risco']]


# Aplicar para os 3 cenários
df_runway_real = calcular_runway_semanal(df_real_s)
df_runway_ideal = calcular_runway_semanal(df_ideal_s)
df_runway_stress = calcular_runway_semanal(df_stress_s)

# Consolidar em matriz 156×3
df_runway_heatmap = pd.DataFrame({
    'semana': df_runway_real['semana'],
    'Real_5A': df_runway_real['runway_semanas'],
    'Ideal_5B': df_runway_ideal['runway_semanas'],
    'Estresse_5C': df_runway_stress['runway_semanas']
})
```

### **OUTPUTS**

```python
# DataFrame principal
df_runway_heatmap  # 156 linhas × 4 colunas (semana + 3 cenários)

# Tabela executiva
tabela_runway_critico = {
    'cenario': ['Real 5A', 'Ideal 5B', 'Estresse 5C'],
    'semanas_criticas': [count onde runway < 6, ...],
    'semanas_atencao': [count onde 6 <= runway < 12, ...],
    'semanas_seguras': [count onde runway >= 12, ...],
    'primeira_semana_critica': [primeira semana onde runway < 6, ...],
    'pior_runway': [min(runway_semanas), ...]
}
```

---

## 🔷 SEÇÃO 3: ESPECIFICAÇÃO VISUAL

### **TIPO DE GRÁFICO**
**Heatmap** (Plotly `go.Heatmap` ou Seaborn `sns.heatmap`)

### **ESTRUTURA**

```
EIXO Y (vertical): 3 cenários
  - Real (5A)
  - Ideal (5B)
  - Estresse (5C)

EIXO X (horizontal): 156 semanas (ou agregado em 36 meses)
  - Opção 1: Mostrar todas as 156 semanas (pode ficar denso)
  - Opção 2: Agregar em meses (36 colunas) usando média ou mínimo do mês
  
CORES:
  - Verde escuro: runway >= 12 semanas (seguro)
  - Amarelo: 6 <= runway < 12 (atenção)
  - Vermelho: runway < 6 (crítico)
  - Cinza escuro: runway = 0 (quebrou)
  
ESCALA DE CORES:
  - Use colorscale customizada:
    [0, 'darkred'],      # 0 semanas
    [0.2, 'red'],        # 3 semanas
    [0.4, 'orange'],     # 6 semanas
    [0.6, 'yellow'],     # 9 semanas
    [0.8, 'lightgreen'], # 12 semanas
    [1.0, 'darkgreen']   # 52+ semanas
```

### **ELEMENTOS OBRIGATÓRIOS**

1. **Linha Horizontal Divisória** entre cada cenário
2. **Anotações de texto** em células críticas (runway < 6):
   - Exemplo: "S42: 2,3 sem" (Semana 42: 2,3 semanas de runway)
3. **Legenda de Cores** (colorbar) com rótulos:
   - "< 6 sem (CRÍTICO)"
   - "6-12 sem (ATENÇÃO)"
   - "> 12 sem (SEGURO)"
4. **Linha Vertical** marcando trimestres (S13, S26, S39, S52, etc.)

### **MODELO ASCII**

```
Runway (semanas)
Cenário     │ M1  M2  M3  M4  M5  M6  M7  M8  M9 M10 M11 M12 ... M36
────────────┼─────────────────────────────────────────────────────────
Real 5A     │ 🟢  🟢  🟢  🟡  🟢  🟢  🟢  🟡  🟢  🟢  🟢  🟢 ... 🟢
            │ 18  15  14  11  13  16  17  10  14  15  18  20 ... 22
────────────┼─────────────────────────────────────────────────────────
Ideal 5B    │ 🟢  🟢  🟢  🟢  🟢  🟢  🟢  🟢  🟢  🟢  🟢  🟢 ... 🟢
            │ 25  28  30  32  35  38  40  42  45  48  50  52 ... 52+
────────────┼─────────────────────────────────────────────────────────
Estresse 5C │ 🟡  🔴  🔴  🔴  🟡  🟡  🟢  🟡  🟢  🟢  🟢  🟢 ... 🟢
            │ 10  4   2   3   8   9   13  11  14  15  16  18 ... 20
────────────┴─────────────────────────────────────────────────────────
            ↑   ↑               ↑               ↑
           Q1  Crítico         Q2              Q3
           
LEGENDA:
🟢 = Seguro (>= 12 semanas)
🟡 = Atenção (6-12 semanas)
🔴 = Crítico (< 6 semanas)
Números = Runway em semanas
```

### **GRÁFICO COMPLEMENTAR (OPCIONAL)**

**Line Chart** mostrando evolução do runway ao longo do tempo:
- 3 linhas (Real/Ideal/Estresse)
- Área sombreada em vermelho quando runway < 6
- Linha horizontal tracejada em runway = 12 (threshold seguro)

---

### **TABELA AUXILIAR - ESTATÍSTICAS DE RUNWAY**

```markdown
| Métrica | Real 5A | Ideal 5B | Estresse 5C | Benchmark |
|---------|---------|----------|-------------|-----------|
| **DISTRIBUIÇÃO DE RISCO** | | | | |
| Semanas Críticas (< 6 sem) | [COUNT] | [COUNT] | [COUNT] | < 10% |
| Semanas Atenção (6-12 sem) | [COUNT] | [COUNT] | [COUNT] | < 20% |
| Semanas Seguras (>= 12 sem) | [COUNT] | [COUNT] | [COUNT] | > 70% |
| **MOMENTOS CRÍTICOS** | | | | |
| Primeira Semana Crítica | S[X] | N/A | S[Y] | Depois S26 |
| Pior Runway (mínimo) | [X] sem | [Y] sem | [Z] sem | > 4 sem |
| Mês do Pior Runway | M[N] | M[N] | M[N] | - |
| **RECUPERAÇÃO** | | | | |
| Semanas até Runway > 12 | [X] sem | [Y] sem | [Z] sem | < 26 sem |
| Break-even (runway infinito) | S[X] | S[Y] | S[Z] | Antes M24 |
```

---

## 🔷 SEÇÃO 4: LEGENDA DIDÁTICA ("COMO LER")

```markdown
::: {.callout-note title="📖 COMO LER ESTE HEATMAP" collapse="false"}

### **O QUE ESTE GRÁFICO MOSTRA**
Este heatmap visualiza o **runway semanal** (quantas semanas de operação o caixa sustenta) ao longo de 36 meses, em 3 cenários paralelos.

**Runway** = Quanto tempo a empresa sobrevive se a receita parar hoje.

Fórmula: `Runway = Caixa / |Burn Rate Semanal Médio|`

### **INTERPRETAÇÃO DAS CORES**

🟢 **VERDE (Seguro):** Runway >= 12 semanas (3 meses)
- Empresa tem margem confortável
- Tempo suficiente para reagir a imprevistos
- Estado ideal para operar

🟡 **AMARELO (Atenção):** Runway entre 6-12 semanas
- Margem apertada mas ainda controlável
- Requer monitoramento próximo
- Ideal planejar ações corretivas

🔴 **VERMELHO (Crítico):** Runway < 6 semanas
- Zona de perigo iminente
- Requer ação imediata (captação ou corte de custos)
- Risco de morte súbita

⚫ **CINZA ESCURO:** Runway = 0 (caixa negativo)
- Empresa quebrou tecnicamente
- Cenário de recuperação ou game over

### **COMO USAR NA PRÁTICA**

1. **Visão Panorâmica:** Conte quantas células vermelhas há em cada linha
   - Real 5A: X células vermelhas → X semanas críticas
   - Se > 10% das semanas são vermelhas → Risco estrutural

2. **Identificar Padrões:**
   - **Vermelho no início:** Problema de bootstrap (caixa inicial baixo)
   - **Vermelho no meio:** Crescimento desordenado (custos > receita)
   - **Vermelho recorrente:** Sazonalidade mal gerida

3. **Comparar Cenários:**
   - Real vs Ideal: Quanto upside há em melhor execução?
   - Real vs Estresse: Quão frágil é o modelo?

4. **Planejar Captações:**
   - Se Real tem células vermelhas em S40-S50 → Captar em S30
   - Regra: Captar 10 semanas **antes** da primeira semana crítica

### **SINAIS DE ALERTA**

⚠️ **ALERTA 1:** Mais de 15% das semanas em vermelho
→ Modelo de negócio não sustentável

⚠️ **ALERTA 2:** Células vermelhas consecutivas (> 4 semanas seguidas)
→ Risco de espiral de morte (cortes não resolvem)

⚠️ **ALERTA 3:** Cenário Real tem vermelho mas Ideal não
→ Problema de execução (churn, CAC, conversão)

✅ **BOA PRÁTICA:**
- Real: < 5% de semanas críticas
- Ideal: 0% de semanas críticas
- Estresse: < 20% de semanas críticas (modelo resiliente)

:::
```

---

## 🔷 SEÇÃO 5: INSIGHT ESTRATÉGICO

### **TEMPLATE DE NARRATIVA**

```markdown
::: {.callout-important title="💡 INSIGHT ESTRATÉGICO - RUNWAY CRÍTICO" icon=false collapse="false"}

#### **FATO**
No **Cenário Real (5A)**, identificamos **[X] semanas críticas** (runway < 6 semanas) concentradas principalmente em **[período: ex: M8-M12]**. O **pior runway** ocorre na **Semana [Y]** com apenas **[Z] semanas** de caixa. 

No **Cenário Estresse (5C)**, o número de semanas críticas sobe para **[W]**, com **[V] semanas consecutivas** em zona vermelha entre **S[A]-S[B]**.

#### **CAUSA**
A concentração de risco no período M8-M12 se deve a:

1. **Fase de Investimento em Growth:**
   - Custos de marketing aumentam [X]% (de R$ [A] para R$ [B]/mês)
   - Receita ainda não acompanhou (crescimento defasado de [N] meses)
   - Burn rate sobe de R$ [C]/semana para R$ [D]/semana

2. **Efeito Sazonalidade:**
   - [Se aplicável: "Trimestre de baixa conversão (verão/inverno)"]
   - Churn temporariamente mais alto ([X]% vs média de [Y]%)

3. **Payback Lag:**
   - CAC pago hoje (R$ [Z])
   - LTV retorna ao longo de [N] meses
   - Gap de caixa durante fase de escala

#### **IMPLICAÇÃO**

✅ **No Cenário Real:**
- **[X]% das semanas** estão em zona segura (verde)
- Risco é **gerenciável** mas requer monitoramento ativo
- Janela de vulnerabilidade identificada: **S[A] a S[B]**

⚠️ **No Cenário Estresse:**
- **[Y]% das semanas** em zona crítica
- Risco de **espiral de morte** se não houver intervenção
- Primeira semana crítica: **S[C]** (Mês [M])

🎯 **Comparação com Benchmark:**
- Startups SaaS saudáveis: < 10% de semanas críticas
- SAM Real: [X]% → [Acima/Dentro/Abaixo] do benchmark
- SAM Estresse: [Y]% → [Interpretação]

#### **AÇÃO RECOMENDADA**

**CURTO PRAZO (30 dias):**

**Ação 1: Buffer de Segurança**
- **O quê:** Criar reserva de R$ [Z] (equivalente a 12 semanas de burn)
- **Como:** [Captação/Empréstimo/Bootstrap mais lento]
- **Investimento:** R$ [Z]
- **Impacto:** Elimina [X] semanas críticas, runway mínimo sobe de [A] para [B] semanas

**MÉDIO PRAZO (60-90 dias):**

**Ação 2: Reduzir Burn Rate no Vale (M8-M12)**
- **O quê:** Otimizar CAC de R$ [A] para R$ [B] via [canais específicos]
- **Como:** [Tática específica: SEO, parcerias, etc.]
- **Investimento:** R$ [C]
- **Impacto:** Burn rate cai [X]%, runway médio aumenta [Y] semanas

**Ação 3: Antecipar Receita**
- **O quê:** Oferecer desconto de [X]% para anual (antecipa 12 meses de MRR)
- **Como:** Campanha para [Y]% da base (clientes com NPS > 8)
- **Investimento:** Desconto de R$ [Z] (custo de oportunidade)
- **Impacto:** Injeta R$ [W] de caixa antecipado, elimina [N] semanas críticas

**LONGO PRAZO (6-12 meses):**

**Ação 4: Alcançar Break-Even Operacional**
- **Meta:** Receita >= Custos Operacionais até Mês [X]
- **Milestone:** Runway torna-se infinito (ou capped em 52 semanas)
- **Plano:** [Crescimento MRR de [A]% a.m. + manter burn < R$ [B]/mês]

#### **REGRA DE CAPTAÇÃO**

Com base no heatmap:
- **Primeira semana crítica:** S[X] (Mês [M])
- **Iniciar captação:** S[X-10] = **Semana [Y]** (Mês [N])
- **Runway ideal no início da captação:** [Z] semanas

**Recomendação:** Iniciar processo de **[Série Seed/Série A]** em **[mês/ano]** para estar capitalizado antes do vale M8-M12.

#### **CENÁRIO OTIMISTA**

Se executarmos **Ações 1 + 2 + 3:**
- Semanas críticas caem de [X] para [Y] (-[Z]%)
- Runway mínimo sobe de [A] para [B] semanas
- Probabilidade de crise de liquidez cai de [C]% para [D]%

:::
```

---

### **MÉTRICAS-CHAVE A CALCULAR**

```python
# No seu código, calcular:

metricas_runway = {
    'real_5a': {
        'semanas_criticas': count(runway < 6),
        'semanas_atencao': count(6 <= runway < 12),
        'semanas_seguras': count(runway >= 12),
        'pct_criticas': semanas_criticas / 156,
        'primeira_critica': first_index(runway < 6),
        'pior_runway': min(runway),
        'semana_pior_runway': argmin(runway),
        'semanas_consecutivas_criticas': max_consecutive(runway < 6)
    },
    'ideal_5b': { ... },
    'estresse_5c': { ... }
}

# Comparação com benchmark
benchmark = {
    'pct_criticas_max': 0.10,  # < 10% é saudável
    'runway_minimo': 4  # Nunca abaixo de 4 semanas
}
```

---

### **METADADOS JSON - ATO 3**

```json
{
  "pagina": 5,
  "secao": "5.4",
  "visualizacao_id": "5.4.1_heatmap_runway_semanal",
  "ato": 3,
  "ato_nome": "Tático",
  "timestamp": "2025-12-09T23:55:00Z",
  
  "titulos": {
    "coloquial": "Em qual semana o caixa fica perigosamente baixo?",
    "tecnico": "Heatmap de Runway Semanal - 156 Semanas × 3 Cenários (Real/Ideal/Estresse)",
    "subtitulo": "Verde = Seguro (>12 sem) | Amarelo = Atenção (6-12 sem) | Vermelho = Crítico (<6 sem)"
  },
  
  "fonte_dados": {
    "inputs": ["df_real_s", "df_ideal_s", "df_stress_s"],
    "funcao_calculo": "calcular_runway_semanal()",
    "formula_runway": "Caixa / |Burn_Rate_Semanal_MA4|",
    "threshold_critico": 6,
    "threshold_seguro": 12
  },
  
  "parametros": {
    "horizonte_semanas": 156,
    "janela_ma_burn": 4,
    "cenarios": ["Real_5A", "Ideal_5B", "Estresse_5C"],
    "escala_cores": {
      "critico": "runway < 6",
      "atencao": "6 <= runway < 12",
      "seguro": "runway >= 12",
      "infinito_cap": 52
    }
  },
  
  "resultados": {
    "real_5a": {
      "semanas_criticas": "CALCULAR_DINAMICAMENTE",
      "pct_criticas": "CALCULAR_DINAMICAMENTE",
      "primeira_critica": "CALCULAR_DINAMICAMENTE",
      "pior_runway_semanas": "CALCULAR_DINAMICAMENTE",
      "semana_pior_runway": "CALCULAR_DINAMICAMENTE"
    },
    "ideal_5b": { "...": "..." },
    "estresse_5c": { "...": "..." },
    "comparacao": {
      "delta_criticas_real_vs_stress": "CALCULAR",
      "delta_pior_runway": "CALCULAR"
    }
  },
  
  "insights": {
    "fato": "[X] semanas críticas no Real, concentradas em M[Y]-M[Z]",
    "causa": "Burn rate alto em fase de growth + payback lag do CAC",
    "implicacao": "[X]% das semanas em risco vs benchmark de <10%",
    "acao": "Buffer R$ [Z], otimizar CAC, antecipar receita anual"
  },
  
  "acoes_recomendadas": [
    {
      "prioridade": 1,
      "acao": "Criar buffer de segurança",
      "investimento": "CALCULAR: 12 semanas × burn_rate_medio",
      "impacto": "Elimina [X] semanas críticas"
    },
    {
      "prioridade": 2,
      "acao": "Reduzir burn rate no vale",
      "investimento": "R$ [Y]",
      "impacto": "Runway médio aumenta [Z] semanas"
    }
  ],
  
  "arquivos_output": {
    "figura_heatmap": "outputs/figs/pag5_heatmap_runway_semanal.png",
    "figura_linechart": "outputs/figs/pag5_runway_evolution.png",
    "tabela": "outputs/tables/pag5_runway_statistics.csv",
    "metadata": "outputs/metadata/pag5_ato3_metadata.json"
  }
}
```