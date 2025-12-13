########################################################################################
########################################################################################
# ATO 4: BREAK-EVEN SOB ESTRESSE (ESCALA)
########################################################################################
########################################################################################

---

## 🔷 SEÇÃO 1: CONCEITO E OBJETIVO

### **PERGUNTA CENTRAL:**
*"Em qual mês paramos de queimar caixa e nos tornamos auto-sustentáveis?"*

### **OBJETIVO:**
Identificar o **ponto de break-even operacional** (quando Receita ≥ Custos) nos 3 cenários, mostrando a trajetória de fluxo de caixa mensal até atingir rentabilidade.

### **POR QUE É IMPORTANTE:**
- **Prova de sustentabilidade:** Empresa não precisa de capital infinito
- **Valuation:** Break-even rápido aumenta múltiplo de avaliação
- **Risco de diluição:** Quanto mais tarde o break-even, mais rodadas de captação
- **Resiliência:** No Estresse, ainda atingimos break-even? Quando?

### **INSIGHT QUE REVELA:**
"No cenário Real, atingimos break-even no Mês X. No Estresse, atrasamos Y meses mas ainda chegamos lá. Isso prova robustez estrutural."

---

## 🔷 SEÇÃO 2: ARQUITETURA DE DADOS

### **INPUTS**

```python
# DataFrames Mensais
df_real_m      # 36 linhas
df_ideal_m     # 36 linhas
df_stress_m    # 36 linhas

# Colunas necessárias:
# - mes: int (0 a 36)
# - receita_mensal: float
# - custos_operacionais: float (exclui capex inicial)
# - fluxo_caixa_mensal: float (receita - custos)
# - caixa_acumulado: float
```

### **TRANSFORMAÇÕES**

```python
# LÓGICA DE CÁLCULO

def identificar_breakeven(df_mensal):
    """
    Identifica o mês de break-even operacional
    
    DEFINIÇÃO:
    Break-even = primeiro mês onde fluxo_caixa_mensal >= 0
    
    REGRAS:
    - Ignorar flutuações: precisa manter positivo por >= 2 meses consecutivos
    - Se não atingir em 36 meses: retornar "Não atingido"
    - Calcular runway no break-even (caixa restante)
    """
    
    df = df_mensal.copy()
    
    # 1. Calcular fluxo de caixa mensal
    df['fluxo_caixa_mensal'] = df['receita_mensal'] - df['custos_operacionais']
    
    # 2. Flag de break-even temporário
    df['breakeven_temp'] = df['fluxo_caixa_mensal'] >= 0
    
    # 3. Encontrar primeiro mês com 2 consecutivos positivos
    for i in range(len(df) - 1):
        if df.loc[i, 'breakeven_temp'] and df.loc[i+1, 'breakeven_temp']:
            mes_breakeven = df.loc[i, 'mes']
            caixa_no_breakeven = df.loc[i, 'caixa_acumulado']
            fluxo_no_breakeven = df.loc[i, 'fluxo_caixa_mensal']
            return {
                'mes': mes_breakeven,
                'caixa_restante': caixa_no_breakeven,
                'fluxo_positivo': fluxo_no_breakeven,
                'atingido': True
            }
    
    # 4. Se não encontrou
    return {
        'mes': None,
        'caixa_restante': df.iloc[-1]['caixa_acumulado'],
        'fluxo_positivo': None,
        'atingido': False
    }


# Aplicar aos 3 cenários
breakeven_real = identificar_breakeven(df_real_m)
breakeven_ideal = identificar_breakeven(df_ideal_m)
breakeven_stress = identificar_breakeven(df_stress_m)
```

### **OUTPUTS**

```python
# Tabela de break-even
tabela_breakeven = pd.DataFrame({
    'Cenário': ['Real 5A', 'Ideal 5B', 'Estresse 5C'],
    'Mês Break-Even': [
        breakeven_real['mes'],
        breakeven_ideal['mes'],
        breakeven_stress['mes']
    ],
    'Caixa Restante': [
        breakeven_real['caixa_restante'],
        breakeven_ideal['caixa_restante'],
        breakeven_stress['caixa_restante']
    ],
    'Fluxo Positivo': [
        breakeven_real['fluxo_positivo'],
        breakeven_ideal['fluxo_positivo'],
        breakeven_stress['fluxo_positivo']
    ],
    'Status': [
        '✅ Atingido' if breakeven_real['atingido'] else '❌ Não Atingido',
        '✅ Atingido' if breakeven_ideal['atingido'] else '❌ Não Atingido',
        '✅ Atingido' if breakeven_stress['atingido'] else '❌ Não Atingido'
    ]
})

# DataFrame para gráfico (trajetória do fluxo de caixa)
df_fluxo_comparativo = pd.DataFrame({
    'mes': df_real_m['mes'],
    'Real_5A': df_real_m['fluxo_caixa_mensal'],
    'Ideal_5B': df_ideal_m['fluxo_caixa_mensal'],
    'Estresse_5C': df_stress_m['fluxo_caixa_mensal']
})
```

---

## 🔷 SEÇÃO 3: ESPECIFICAÇÃO VISUAL

### **TIPO DE GRÁFICO**
**Line Chart** com área sombreada (Plotly `go.Scatter` com `fill='tozeroy'`)

### **ESTRUTURA**

```
EIXO X: Meses (0 a 36)
EIXO Y: Fluxo de Caixa Mensal (R$)

LINHAS:
- Linha Azul: Cenário Real (5A)
- Linha Verde: Cenário Ideal (5B)
- Linha Vermelha: Cenário Estresse (5C)

ÁREA SOMBREADA:
- Área VERMELHA abaixo de zero (fluxo negativo = queimando caixa)
- Área VERDE acima de zero (fluxo positivo = lucrando)

MARCADORES:
- Ponto destacado (círculo grande) no mês de break-even de cada cenário
- Anotação de texto: "Break-Even M[X]"

LINHA HORIZONTAL:
- Linha preta tracejada em y=0 (linha de break-even)
```

### **ELEMENTOS OBRIGATÓRIOS**

1. **Área Sombreada Negativa:**
   - `fill='tozeroy'` com cor vermelha transparente (opacity=0.2)
   - Apenas para valores < 0

2. **Área Sombreada Positiva:**
   - `fill='tozeroy'` com cor verde transparente (opacity=0.2)
   - Apenas para valores > 0

3. **Marcadores de Break-Even:**
   - Círculo grande (size=15) na interseção de cada linha com y=0
   - Anotação com seta apontando para o ponto

4. **Grid Vertical em Trimestres:**
   - Linhas verticais cinza claro em M3, M6, M9, M12, etc.

5. **Legenda:**
   - Posição: topo direito
   - Incluir: 3 cenários + "Linha de Break-Even"

### **MODELO ASCII**

```
Fluxo de Caixa (R$/mês)
   50k ┤                                          ╱╱╱╱╱╱ Ideal
       │                                      ╱╱╱╱
   40k ┤                                  ╱╱╱╱
       │                              ╱╱╱╱
   30k ┤                          ╱╱╱╱       ╱── Real
       │                      ╱╱╱╱       ╱╱╱
   20k ┤                  ╱╱╱╱       ╱╱╱
       │              ╱╱╱╱       ╱╱╱
   10k ┤          ╱╱╱╱  ●━━━━━╱━━━━━━━━━━━━━━━━━━━ (Break-Even Real: M18)
       │      ╱╱╱╱        ╱
    0k ┼══════════════════════════════════════════════════════ (Break-Even)
       │  ▓▓▓▓            ╲
  -10k ┤▓▓▓                ╲     ● Break-Even Estresse: M24
       │▓                   ╲   ╱
  -20k ┤                     ╲ ╱
       │                      ╲╱  Estresse
  -30k ┤                      ▓
       │                     ▓
  -40k ┤                    ▓
       ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
        M0  M3  M6  M9 M12 M15 M18 M21 M24 M27 M30 M33 M36

LEGENDA:
╱╱╱ = Área positiva (verde) - Lucrando
▓▓▓ = Área negativa (vermelha) - Queimando caixa
──── = Linha de Break-Even (fluxo = 0)
● = Ponto de break-even
```

---

### **TABELA AUXILIAR - COMPARAÇÃO DE BREAK-EVEN**

```markdown
| Métrica | Real 5A | Ideal 5B | Estresse 5C | Benchmark | Interpretação |
|---------|---------|----------|-------------|-----------|---------------|
| **TIMING** | | | | | |
| Mês de Break-Even | M[X] | M[Y] | M[Z] | < M24 | [Status] |
| Tempo até Break-Even | [X] meses | [Y] meses | [Z] meses | < 24 meses | [Status] |
| Atraso vs Ideal | [X-Y] meses | - | [Z-Y] meses | - | - |
| **CAPITAL CONSUMIDO** | | | | | |
| Caixa Queimado até Break-Even | R$ [A] | R$ [B] | R$ [C] | < R$ 500k | [Status] |
| Caixa Restante no Break-Even | R$ [D] | R$ [E] | R$ [F] | > R$ 50k | [Status] |
| Runway no Break-Even | [G] meses | [H] meses | [I] meses | > 6 meses | [Status] |
| **MÉTRICAS NO BREAK-EVEN** | | | | | |
| MRR no Break-Even | R$ [J] | R$ [K] | R$ [L] | > R$ 50k | [Status] |
| ARR no Break-Even | R$ [M] | R$ [N] | R$ [O] | > R$ 600k | [Status] |
| Clientes no Break-Even | [P] | [Q] | [R] | > 500 | [Status] |
| LTV/CAC no Break-Even | [S]x | [T]x | [U]x | > 3.0x | [Status] |
| **PÓS BREAK-EVEN** | | | | | |
| Fluxo Positivo Médio (M+1 a M+6) | R$ [V]/mês | R$ [W]/mês | R$ [X]/mês | Crescente | [Status] |
| Aceleração Pós-BE | [Y]%/mês | [Z]%/mês | [W]%/mês | > 10%/mês | [Status] |
```

---

## 🔷 SEÇÃO 4: LEGENDA DIDÁTICA ("COMO LER")

```markdown
::: {.callout-note title="📖 COMO LER ESTE GRÁFICO" collapse="false"}

### **O QUE ESTE GRÁFICO MOSTRA**
A **trajetória do fluxo de caixa mensal** (Receita - Custos Operacionais) ao longo de 36 meses, em 3 cenários paralelos.

**Break-Even** = O mês em que o fluxo de caixa cruza de negativo para positivo (empresa para de queimar caixa).

### **INTERPRETAÇÃO VISUAL**

📍 **LINHA HORIZONTAL PRETA (y=0):**
- Linha divisória entre "queimar caixa" (abaixo) e "lucrar" (acima)
- Objetivo: cruzar essa linha o mais cedo possível

📉 **ÁREA VERMELHA (abaixo de zero):**
- Cada mês aqui, a empresa está **queimando caixa**
- Quanto mais larga e profunda, mais capital consumido
- No Real: área vermelha de M0 a M[X]

📈 **ÁREA VERDE (acima de zero):**
- Cada mês aqui, a empresa está **gerando caixa**
- Quanto mais alta, maior o lucro mensal
- Empresa se torna auto-sustentável

🔵 **PONTO DE BREAK-EVEN (círculo):**
- Marca exatamente quando cada cenário cruza y=0
- Real: M[X] | Ideal: M[Y] | Estresse: M[Z]

### **COMO USAR NA PRÁTICA**

1. **Avaliar Timing:**
   - **< M18:** Excelente (raro em bootstraps)
   - **M18-M24:** Bom (dentro do esperado)
   - **> M24:** Preocupante (precisa de capital externo)

2. **Comparar Cenários:**
   - **Delta Real vs Ideal:** Quanto perdemos por não ter execução perfeita?
   - **Delta Real vs Estresse:** Quanto margem de erro temos?
   - Se Estresse nunca atinge BE → Modelo frágil

3. **Planejar Captação:**
   - Se break-even em M18 → Captar para ter runway até M24 (6 meses de margem)
   - Regra: `Capital_Necessário = Caixa_Queimado_até_BE × 1.3` (buffer)

4. **Pós Break-Even:**
   - A linha deve continuar **subindo** (crescimento acelerando)
   - Se achatar logo após BE → Crescimento estagnou

### **SINAIS DE ALERTA**

⚠️ **ALERTA 1:** Break-even > M30
→ Modelo não escala bem, precisa de capital infinito

⚠️ **ALERTA 2:** Linha desce após break-even
→ Custos cresceram mais rápido que receita (armadilha de escala)

⚠️ **ALERTA 3:** Estresse não atinge break-even
→ Modelo é insustentável sob pressão

✅ **BOA PRÁTICA:**
- Real: break-even antes de M24
- Ideal: break-even antes de M18
- Estresse: break-even antes de M30 (ainda viável)

### **REGRA DOS 3 NÚMEROS**

Olhe apenas 3 métricas:
1. **Mês de Break-Even no Real:** [X] (quanto antes, melhor)
2. **Caixa Restante no BE:** R$ [Y] (> R$ 50k = margem de segurança)
3. **Delta Real vs Estresse:** [Z] meses (< 6 meses = resiliente)

:::
```

---

## 🔷 SEÇÃO 5: INSIGHT ESTRATÉGICO

### **TEMPLATE DE NARRATIVA**

```markdown
::: {.callout-important title="💡 INSIGHT ESTRATÉGICO - BREAK-EVEN" icon=false collapse="false"}

#### **FATO**
O **Cenário Real (5A)** atinge break-even operacional no **Mês [X]**, com caixa restante de **R$ [Y]** e runway de **[Z] meses**. Nesse momento, o MRR é **R$ [A]** e a base tem **[B] clientes**.

O **Cenário Ideal (5B)** acelera o break-even para **Mês [W]** (ganho de **[X-W] meses**), enquanto o **Cenário Estresse (5C)** atrasa para **Mês [V]** (perda de **[V-X] meses**).

Até o break-even, consumimos **R$ [C]** de capital no Real, **R$ [D]** no Ideal, e **R$ [E]** no Estresse.

#### **CAUSA**
O timing do break-even é determinado por **3 fatores principais**:

1. **Crescimento de Receita (taxa de adição de MRR):**
   - Real: +R$ [F]/mês em média (M0-M[X])
   - Ideal: +R$ [G]/mês (+[H]% vs Real)
   - Estresse: +R$ [I]/mês (-[J]% vs Real)

2. **Controle de Custos Operacionais:**
   - Burn rate médio no Real: R$ [K]/mês
   - Margem bruta no Real: [L]% (cada R$ 1 de receita cobre R$ [M] de custo)

3. **Payback do CAC:**
   - CAC médio: R$ [N]
   - Payback: [O] meses
   - Cada cliente novo hoje só "paga por si" daqui [O] meses

**Por que o Ideal é mais rápido?**
- Churn [P]% menor → retenção acelera acúmulo de MRR
- CAC [Q]% menor → menos capital queimado por cliente
- Conversão [R]% maior → crescimento mais rápido com mesmo tráfego

**Por que o Estresse é mais lento?**
- Churn dobrado ([S]%) → MRR cresce devagar (2 passos à frente, 1 atrás)
- CAC +50% → consome mais caixa por cliente
- Conversão -20% → precisa de mais tráfego (mais caro)

#### **IMPLICAÇÃO**

✅ **No Cenário Real:**
- Break-even em M[X] está **[dentro/fora]** do benchmark de < M24
- Caixa restante de R$ [Y] dá **[Z] meses** de runway extra (margem de segurança)
- Após BE, fluxo positivo acelera para **R$ [T]/mês** (média M[X+1] a M[X+6])

⚠️ **No Cenário Estresse:**
- Atraso de **[V-X] meses** vs Real
- Consome **R$ [E-C]** a mais de capital
- Mas **ainda atinge BE** → Modelo resiliente

🚀 **No Cenário Ideal:**
- Antecipa **[X-W] meses** vs Real
- Economiza **R$ [C-D]** de capital
- Prova que **há upside** com melhor execução

🎯 **Comparação com Benchmarks:**
- **SaaS B2C médio:** Break-even em M24-M30
- **Top 25%:** Break-even em M18-M24
- **Top 10%:** Break-even em M12-M18
- **SAM Real (M[X]):** [Posição no ranking]

#### **AÇÃO RECOMENDADA**

**OBJETIVO:** Antecipar break-even de M[X] para M[X-6] (ganho de 6 meses)

**ALAVANCAS (em ordem de impacto):**

**Alavanca 1: Reduzir Churn Inicial**
- **Meta:** De [S]% para [S-2]%
- **Como:** Onboarding melhorado + CS proativo
- **Investimento:** R$ [U]
- **Impacto:** Antecipa break-even em **[V] meses** (MRR retido acelera)

**Alavanca 2: Reduzir CAC**
- **Meta:** De R$ [N] para R$ [N×0.8]
- **Como:** SEO + parcerias + referral program
- **Investimento:** R$ [W]
- **Impacto:** Economiza **R$ [X]** até BE, antecipa em **[Y] meses**

**Alavanca 3: Aumentar Conversão**
- **Meta:** De [Z]% para [Z×1.2]%
- **Como:** A/B tests no funil + copy otimizado
- **Investimento:** R$ [AA]
- **Impacto:** Mais clientes com mesmo CAC, antecipa em **[BB] meses**

**NÃO FAZER (baixo impacto no BE):**
- ❌ Aumentar preços (risca churn compensar ganho de ARPU)
- ❌ Cortar custos fixos drasticamente (compromete produto)

#### **CENÁRIO COMBINADO**

Se executarmos **Alavancas 1 + 2 + 3:**
- Break-even antecipa de **M[X]** para **M[X-CC]**
- Capital economizado: **R$ [DD]**
- Caixa restante no novo BE: **R$ [EE]** (vs R$ [Y] antes)
- **ROI consolidado:** Investir R$ [U+W+AA] → Economizar R$ [DD] (ROI de [FF]x)

#### **REGRA DE CAPTAÇÃO REVISADA**

**Com Break-Even em M[X]:**
- Capital necessário: R$ [C] (consumo até BE) + R$ [buffer] (margem 30%)
- **Total para captar:** R$ [GG]

**Com Break-Even antecipado (M[X-CC]):**
- Capital necessário: R$ [C-DD] + R$ [buffer_menor]
- **Total para captar:** R$ [HH] (-[II]% vs antes)

**Vantagem estratégica:**
- Menor diluição (precisa de menos capital)
- Menor risco (chega em BE antes do capital acabar)
- Maior valuation (prova de tração mais rápida)

:::
```

---

### **MÉTRICAS-CHAVE A CALCULAR**

```python
# No seu código, calcular para cada cenário:

metricas_breakeven = {
    'real_5a': {
        'mes_breakeven': identificar_mes_be(df_real_m),
        'caixa_restante': caixa_no_mes_be,
        'caixa_consumido': caixa_inicial - caixa_restante,
        'runway_no_be': calcular_runway(caixa_restante, burn_medio),
        'mrr_no_be': mrr_mes_be,
        'arr_no_be': mrr_no_be * 12,
        'clientes_no_be': usuarios_mes_be,
        'ltv_cac_no_be': ltv_cac_mes_be,
        'fluxo_pos_medio_pos_be': mean(fluxo[be+1:be+7]),  # 6 meses após
        'tempo_ate_be': mes_breakeven  # meses desde M0
    },
    'ideal_5b': { ... },
    'estresse_5c': { ... }
}

# Comparações
deltas = {
    'real_vs_ideal_meses': metricas['real']['mes_breakeven'] - metricas['ideal']['mes_breakeven'],
    'real_vs_stress_meses': metricas['stress']['mes_breakeven'] - metricas['real']['mes_breakeven'],
    'capital_economizado_se_ideal': metricas['real']['caixa_consumido'] - metricas['ideal']['caixa_consumido']
}
```

---

### **METADADOS JSON - ATO 4**

```json
{
  "pagina": 5,
  "secao": "5.5",
  "visualizacao_id": "5.5.1_breakeven_sob_estresse",
  "ato": 4,
  "ato_nome": "Escala",
  "timestamp": "2025-12-10T00:00:00Z",
  
  "titulos": {
    "coloquial": "Em qual mês paramos de queimar caixa e nos tornamos auto-sustentáveis?",
    "tecnico": "Trajetória de Fluxo de Caixa Mensal até Break-Even Operacional - 3 Cenários",
    "subtitulo": "Break-Even = Receita ≥ Custos Operacionais | Área vermelha = queima | Área verde = lucro"
  },
  
  "fonte_dados": {
    "inputs": ["df_real_m", "df_ideal_m", "df_stress_m"],
    "funcao_calculo": "identificar_breakeven()",
    "definicao_breakeven": "Primeiro mês onde fluxo_caixa_mensal >= 0 por 2 meses consecutivos",
    "formula_fluxo": "receita_mensal - custos_operacionais"
  },
  
  "parametros": {
    "horizonte_meses": 36,
    "criterio_confirmacao": "2_meses_consecutivos_positivos",
    "custos_incluidos": ["operacionais", "marketing", "rh", "infra"],
    "custos_excluidos": ["capex_inicial", "investimentos_nao_recorrentes"]
  },
  
  "resultados": {
    "real_5a": {
      "mes_breakeven": "CALCULAR_DINAMICAMENTE",
      "atingido": "BOOLEAN",
      "caixa_restante": "CALCULAR",
      "caixa_consumido": "CALCULAR",
      "runway_no_be": "CALCULAR",
      "metricas_no_be": {
        "mrr": "CALCULAR",
        "arr": "CALCULAR",
        "clientes": "CALCULAR",
        "ltv_cac": "CALCULAR"
      },
      "fluxo_pos_medio_6m_apos": "CALCULAR"
    },
    "ideal_5b": { "...": "..." },
    "estresse_5c": { "...": "..." },
    "comparacoes": {
      "delta_real_ideal_meses": "CALCULAR",
      "delta_real_stress_meses": "CALCULAR",
      "capital_economizado_se_ideal": "CALCULAR",
      "capital_extra_se_stress": "CALCULAR"
    }
  },
  
  "insights": {
    "fato": "Break-even em M[X] (Real), M[Y] (Ideal), M[Z] (Estresse)",
    "causa": "Timing determinado por: crescimento MRR ([A]%/mês), burn rate (R$ [B]/mês), payback CAC ([C] meses)",
    "implicacao": "Real está [dentro/fora] de benchmark (<M24). Estresse atrasa [X] meses mas ainda atinge.",
    "acao": "Reduzir churn [W]p.p. + CAC [Y]% → Antecipa BE em [Z] meses"
  },
  
  "acoes_recomendadas": [
    {
      "alavanca": "Reduzir Churn",
      "meta": "De [X]% para [Y]%",
      "investimento": "CALCULAR",
      "impacto_meses": "CALCULAR"
    },
    {
      "alavanca": "Reduzir CAC",
      "meta": "De R$ [A] para R$ [B]",
      "investimento": "CALCULAR",
      "impacto_meses": "CALCULAR"
    },
    {
      "alavanca": "Aumentar Conversão",
      "meta": "De [C]% para [D]%",
      "investimento": "CALCULAR",
      "impacto_meses": "CALCULAR"
    }
  ],
  
  "benchmarks": {
    "saas_b2c_medio": "M24-M30",
    "top_25pct": "M18-M24",
    "top_10pct": "M12-M18",
    "sam_posicionamento": "COMPARAR_DINAMICAMENTE"
  },
  
  "arquivos_output": {
    "figura_linechart": "outputs/figs/pag5_breakeven_trajetoria.png",
    "tabela": "outputs/tables/pag5_breakeven_comparacao.csv",
    "metadata": "outputs/metadata/pag5_ato4_metadata.json"
  }
}
```

---
####################################################################################
####################################################################################
# ATO 5: GAP ANALYSIS - REAL VS ESTRESSE (VAZAMENTO)
####################################################################################

---

## 🔷 SEÇÃO 1: CONCEITO E OBJETIVO

### **PERGUNTA CENTRAL:**
*"Qual a distância entre nossa projeção conservadora e o pior cenário? Onde o modelo 'vaza' sob pressão?"*

### **OBJETIVO:**
Quantificar o **gap de performance** entre o Cenário Real (5A) e o Cenário Estresse (5C) em múltiplas dimensões (Caixa, MRR, LTV/CAC, Churn), identificando os **pontos de fragilidade** do modelo de negócios.

### **POR QUE É IMPORTANTE:**
- **Stress Testing:** Investidores querem ver "onde o barco afunda primeiro"
- **Mitigação Proativa:** Identificar vulnerabilidades antes de acontecerem
- **Prova de Resiliência:** Se o gap é controlável → modelo robusto
- **Priorização de Riscos:** Onde concentrar esforços de mitigação

### **INSIGHT QUE REVELA:**
"Sob estresse, perdemos X% de caixa e Y% de MRR. O 'vazamento' crítico está em [premissa Z], que explica W% do gap total. Mitigar isso custa R$ V e reduz gap em U%."

---

## 🔷 SEÇÃO 2: ARQUITETURA DE DADOS

### **INPUTS**

```python
# DataFrames Mensais
df_real_m      # 36 linhas (cenário conservador)
df_stress_m    # 36 linhas (cenário catastrófico)

# Colunas necessárias:
# - mes: int (0 a 36)
# - caixa: float
# - mrr: float
# - arr: float
# - usuarios: int
# - ltv_cac: float
# - churn: float
# - receita_mensal: float
# - custos_totais: float
```

### **TRANSFORMAÇÕES**

```python
# LÓGICA DE CÁLCULO

def calcular_gap_analysis(df_real, df_stress):
    """
    Calcula gaps (diferenças) entre Real e Estresse
    
    GAPS CALCULADOS:
    1. Gap Absoluto: Stress - Real (em unidades originais)
    2. Gap Relativo: (Stress - Real) / Real (em %)
    3. Gap Acumulado: Soma dos gaps ao longo do tempo
    4. Contribuição: Quanto cada métrica explica o gap total
    """
    
    # 1. Criar DataFrame consolidado
    df_gap = pd.DataFrame({
        'mes': df_real['mes'],
        'caixa_real': df_real['caixa'],
        'caixa_stress': df_stress['caixa'],
        'mrr_real': df_real['mrr'],
        'mrr_stress': df_stress['mrr'],
        'ltv_cac_real': df_real['ltv_cac'],
        'ltv_cac_stress': df_stress['ltv_cac'],
        'churn_real': df_real['churn'],
        'churn_stress': df_stress['churn']
    })
    
    # 2. Calcular gaps absolutos
    df_gap['gap_caixa'] = df_gap['caixa_stress'] - df_gap['caixa_real']
    df_gap['gap_mrr'] = df_gap['mrr_stress'] - df_gap['mrr_real']
    df_gap['gap_ltv_cac'] = df_gap['ltv_cac_stress'] - df_gap['ltv_cac_real']
    df_gap['gap_churn'] = df_gap['churn_stress'] - df_gap['churn_real']
    
    # 3. Calcular gaps relativos (%)
    df_gap['gap_caixa_pct'] = (df_gap['gap_caixa'] / df_gap['caixa_real'].abs()) * 100
    df_gap['gap_mrr_pct'] = (df_gap['gap_mrr'] / df_gap['mrr_real']) * 100
    df_gap['gap_ltv_cac_pct'] = (df_gap['gap_ltv_cac'] / df_gap['ltv_cac_real']) * 100
    df_gap['gap_churn_pct'] = (df_gap['gap_churn'] / df_gap['churn_real']) * 100
    
    # 4. Identificar "pior gap" (maior divergência)
    df_gap['pior_gap_metrica'] = df_gap[['gap_caixa_pct', 'gap_mrr_pct', 
                                           'gap_ltv_cac_pct']].abs().idxmax(axis=1)
    
    return df_gap


def decomposicao_gap_caixa(df_real, df_stress):
    """
    Decomposição de Shapley: quanto cada fator contribui para o gap de caixa
    
    FATORES:
    1. Churn dobrado
    2. CAC +50%
    3. ARPU -20%
    4. Conversão -20%
    5. Tráfego -30%
    
    MÉTODO: Variação marginal de cada fator isoladamente
    """
    
    # Caixa final Real e Stress
    caixa_real_final = df_real.iloc[-1]['caixa']
    caixa_stress_final = df_stress.iloc[-1]['caixa']
    gap_total = caixa_stress_final - caixa_real_final
    
    # Testar cada fator isoladamente
    contribuicoes = {}
    
    # Fator 1: Churn dobrado (mantenha resto igual)
    premissas_temp = PREMISSAS.copy()
    premissas_temp['churn_inicial'] = PREMISSAS['churn_inicial'] * 2
    df_churn_isolado = gerar_cenario(premissas_temp)
    caixa_churn = df_churn_isolado.iloc[-1]['caixa']
    contribuicoes['churn'] = (caixa_churn - caixa_real_final) / gap_total
    
    # Fator 2: CAC +50%
    premissas_temp = PREMISSAS.copy()
    premissas_temp['cac_medio'] = PREMISSAS['cac_medio'] * 1.5
    df_cac_isolado = gerar_cenario(premissas_temp)
    caixa_cac = df_cac_isolado.iloc[-1]['caixa']
    contribuicoes['cac'] = (caixa_cac - caixa_real_final) / gap_total
    
    # Repetir para outros fatores...
    # (você implementa com seu motor)
    
    return contribuicoes


# Executar análises
df_gap = calcular_gap_analysis(df_real_m, df_stress_m)
contribuicoes_gap = decomposicao_gap_caixa(df_real_m, df_stress_m)
```

### **OUTPUTS**

```python
# DataFrame principal de gaps
df_gap  # 36 linhas × ~15 colunas

# Tabela de decomposição
tabela_decomposicao = pd.DataFrame({
    'Fator': ['Churn Dobrado', 'CAC +50%', 'ARPU -20%', 'Conversão -20%', 'Tráfego -30%'],
    'Contribuição %': [
        contribuicoes_gap['churn'] * 100,
        contribuicoes_gap['cac'] * 100,
        contribuicoes_gap['arpu'] * 100,
        contribuicoes_gap['conversao'] * 100,
        contribuicoes_gap['trafego'] * 100
    ],
    'Impacto R$': [
        contribuicoes_gap['churn'] * gap_total,
        contribuicoes_gap['cac'] * gap_total,
        # etc...
    ]
}).sort_values('Contribuição %', ascending=False)

# Estatísticas resumidas
resumo_gap = {
    'gap_caixa_final': caixa_stress_final - caixa_real_final,
    'gap_mrr_final': df_stress_m.iloc[-1]['mrr'] - df_real_m.iloc[-1]['mrr'],
    'gap_ltv_cac_final': df_stress_m.iloc[-1]['ltv_cac'] - df_real_m.iloc[-1]['ltv_cac'],
    'mes_maior_gap_caixa': df_gap['gap_caixa'].abs().idxmax(),
    'valor_maior_gap': df_gap.loc[df_gap['gap_caixa'].abs().idxmax(), 'gap_caixa']
}
```

---

## 🔷 SEÇÃO 3: ESPECIFICAÇÃO VISUAL

### **GRÁFICO 1: ÁREA DE GAP (PRINCIPAL)**

**TIPO:** Area Chart com 2 linhas + área sombreada entre elas

**ESTRUTURA:**
```
EIXO X: Meses (0 a 36)
EIXO Y: Caixa Acumulado (R$)

LINHAS:
- Linha Azul Sólida: Real (5A) - limite superior
- Linha Vermelha Sólida: Estresse (5C) - limite inferior

ÁREA SOMBREADA:
- Cor: Vermelho translúcido (opacity=0.3)
- Entre as duas linhas
- Representa o "vazamento" de caixa sob pressão

ANOTAÇÕES:
- Texto no ponto de maior gap: "Maior Gap: M[X] = R$ [Y]"
- Setas apontando para momentos críticos
```

**MODELO ASCII:**

```
Caixa (R$)
  150k ┤                                            ╱╱╱╱╱ Real 5A
       │                                        ╱╱╱╱
  125k ┤                                    ╱╱╱╱
       │                                ╱╱╱╱
  100k ┤                            ╱╱╱╱  ▒▒▒▒▒▒▒▒▒▒▒▒
       │                        ╱╱╱╱  ▒▒▒▒
   75k ┤                    ╱╱╱╱  ▒▒▒▒        GAP
       │                ╱╱╱╱  ▒▒▒▒           (Vazamento)
   50k ┤            ╱╱╱╱  ▒▒▒▒
       │        ╱╱╱╱  ▒▒▒▒           ← Maior Gap: M18 = R$ 45k
   25k ┤    ╱╱╱╱  ▒▒▒▒                           
       │╱╱╱╱  ▒▒▒▒╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱ Estresse 5C
    0k ┼════════════════════════════════════════════════════
       │    ▒▒▒▒
  -25k ┤        ▒▒▒▒
       ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
        M0  M3  M6  M9 M12 M15 M18 M21 M24 M27 M30 M33 M36

LEGENDA:
╱╱╱ = Cenário Real (5A)
▒▒▒ = Área de Gap (perda de performance sob estresse)
═══ = Linha de Break-Even
```

---

### **GRÁFICO 2: WATERFALL CHART - DECOMPOSIÇÃO DO GAP**

**TIPO:** Waterfall (Plotly `go.Waterfall`)

**ESTRUTURA:**
```
EIXO X: Fatores de Estresse
  - Base (Real)
  - Churn Dobrado
  - CAC +50%
  - ARPU -20%
  - Conversão -20%
  - Tráfego -30%
  - Total (Estresse)

EIXO Y: Caixa Final (R$)

BARRAS:
- Verde: Ponto de partida (Real)
- Vermelho: Cada fator reduz o caixa
- Cinza: Total final (Estresse)

CONECTORES:
- Linhas tracejadas ligando cada barra (mostram acúmulo)
```

**MODELO ASCII:**

```
Caixa Final (R$)
100k ┤ ████          
     │ ████  Base    
  80k│ ████ (Real)   
     │ ████          ▓▓▓▓
  60k│ ████          ▓▓▓▓ -18k
     │ ████          ▓▓▓▓ Churn
  40k│ ████          ▓▓▓▓          ▓▓▓▓
     │ ████          ▓▓▓▓          ▓▓▓▓ -12k
  20k│ ████          ▓▓▓▓          ▓▓▓▓ CAC      ▓▓▓▓
     │ ████          ▓▓▓▓          ▓▓▓▓          ▓▓▓▓ -8k
   0k│ ████          ▓▓▓▓          ▓▓▓▓          ▓▓▓▓ ARPU ... ░░░░
     │                                                        ░░░░ Final
 -20k│                                                        ░░░░ (Stress)
     ┴───────┴─────────┴───────────┴───────────┴─────────────┴──────
       Base    -Churn     -CAC       -ARPU     -Conversão    Total
      (Real)   (-R$18k)  (-R$12k)   (-R$8k)    (-R$7k)    (R$-15k)

INTERPRETAÇÃO:
- Churn é o maior "vazamento" (40% do gap total)
- CAC vem em segundo (27%)
- Soma dos fatores = Gap total de R$ 96k
```

---

### **TABELA AUXILIAR - ANÁLISE DE GAP MULTIDIMENSIONAL**

```markdown
| Métrica | Real 5A (M36) | Estresse 5C (M36) | Gap Absoluto | Gap % | Criticidade |
|---------|---------------|-------------------|--------------|-------|-------------|
| **FINANCEIRO** | | | | | |
| Caixa | R$ [A] | R$ [B] | R$ [B-A] | [%] | [🔴/🟡/🟢] |
| MRR | R$ [C] | R$ [D] | R$ [D-C] | [%] | [🔴/🟡/🟢] |
| ARR | R$ [E] | R$ [F] | R$ [F-E] | [%] | [🔴/🟡/🟢] |
| Receita Acumulada 36M | R$ [G] | R$ [H] | R$ [H-G] | [%] | [🔴/🟡/🟢] |
| **OPERACIONAL** | | | | | |
| Clientes | [I] | [J] | [J-I] | [%] | [🔴/🟡/🟢] |
| LTV/CAC | [K]x | [L]x | [L-K]x | [%] | [🔴/🟡/🟢] |
| Churn Médio | [M]% | [N]% | +[N-M] p.p. | [%] | [🔴/🟡/🟢] |
| CAC Médio | R$ [O] | R$ [P] | +R$ [P-O] | [%] | [🔴/🟡/🟢] |
| **TIMING** | | | | | |
| Mês Break-Even | M[Q] | M[R] | +[R-Q] meses | [%] | [🔴/🟡/🟢] |
| Semanas Críticas | [S] | [T] | +[T-S] sem | [%] | [🔴/🟡/🟢] |

---

**DECOMPOSIÇÃO DO GAP DE CAIXA (R$ [TOTAL])**

| Fator | Contribuição | Valor (R$) | % do Gap | Rank | Ação de Mitigação |
|-------|--------------|------------|----------|------|-------------------|
| Churn Dobrado | 40% | R$ [A] | 40% | 1 | Reduzir de 14% para 10% |
| CAC +50% | 27% | R$ [B] | 27% | 2 | Otimizar canais para -20% |
| ARPU -20% | 18% | R$ [C] | 18% | 3 | Upsell para +10% |
| Conversão -20% | 10% | R$ [D] | 10% | 4 | Melhorar funil +5 p.p. |
| Tráfego -30% | 5% | R$ [E] | 5% | 5 | Diversificar fontes |
| **TOTAL** | 100% | R$ [TOTAL] | 100% | - | Combo reduz gap em 65% |
```

---

## 🔷 SEÇÃO 4: LEGENDA DIDÁTICA ("COMO LER")

```markdown
::: {.callout-note title="📖 COMO LER ESTES GRÁFICOS" collapse="false"}

### **GRÁFICO 1: ÁREA DE GAP**

**O QUE MOSTRA:**
A "distância" entre o Cenário Real (conservador) e o Cenário Estresse (catastrófico) ao longo de 36 meses. A área vermelha sombreada representa o **vazamento de performance** sob pressão máxima.

**INTERPRETAÇÃO:**

📏 **LARGURA DA ÁREA (horizontal):**
- Área estreita = Gap se mantém constante
- Área se expandindo = Gap aumenta com o tempo (fragilidade crescente)
- Área se contraindo = Gap diminui (modelo resiliente, se recupera)

📊 **ALTURA DA ÁREA (vertical):**
- Quanto maior, pior → Mais vulnerável a estresse
- No M36: Gap de R$ [X] = perda de [Y]% do caixa Real

🎯 **PONTO DE MAIOR GAP:**
- Identificado com anotação no gráfico
- Representa o momento de maior vulnerabilidade
- Ex: "M18: Gap de R$ 45k (55% do caixa Real)"

### **COMO INTERPRETAR O GAP**

✅ **GAP CONTROLÁVEL (< 30%):**
- Gap de R$ 30k quando Real = R$ 100k
- Perda relativa = 30%
- Modelo é **resiliente** - sobrevive a choques

⚠️ **GAP MODERADO (30-60%):**
- Gap de R$ 50k quando Real = R$ 100k
- Perda relativa = 50%
- Modelo é **vulnerável** - requer mitigação

🔴 **GAP CRÍTICO (> 60%):**
- Gap de R$ 80k quando Real = R$ 100k
- Perda relativa = 80%
- Modelo é **frágil** - alto risco de colapso

### **GRÁFICO 2: WATERFALL (DECOMPOSIÇÃO)**

**O QUE MOSTRA:**
Quanto cada fator de estresse contribui para o gap total de caixa. É como uma "autópsia" do vazamento.

**COMO LER:**

1. **Barra Verde (início):** Caixa no Real (base)
2. **Barras Vermelhas (meio):** Cada fator reduz progressivamente
   - Altura da barra = impacto em R$
   - Ordem decrescente = do pior para o menos pior
3. **Barra Cinza (fim):** Caixa no Estresse (resultado final)

**REGRA DE PARETO:**
- Tipicamente, **2-3 fatores** explicam **70-80%** do gap
- Esses são os "vazamentos críticos" a mitigar

**EXEMPLO DE LEITURA:**
- Churn dobrado: -R$ 18k (40% do gap)
- CAC +50%: -R$ 12k (27%)
- ARPU -20%: -R$ 8k (18%)
- **Top 3 = 85% do gap** → Foco aqui tem ROI máximo

### **SINAIS DE ALERTA**

⚠️ **ALERTA 1:** Gap > 50% do caixa Real
→ Modelo tem dependência excessiva de premissas otimistas

⚠️ **ALERTA 2:** Gap crescente ao longo do tempo
→ Fragilidade estrutural (problemas se acumulam)

⚠️ **ALERTA 3:** Um único fator explica > 50% do gap
→ "Single point of failure" (ponto único de falha)

✅ **BOA PRÁTICA:**
- Gap final < 40% do Real
- Gap distribuído (nenhum fator > 30%)
- Gap se estabiliza ou contrai após M18

:::
```

---

## 🔷 SEÇÃO 5: INSIGHT ESTRATÉGICO

```markdown
::: {.callout-important title="💡 INSIGHT ESTRATÉGICO - VAZAMENTO CRÍTICO" icon=false collapse="false"}

#### **FATO**
Entre o **Cenário Real (5A)** e o **Cenário Estresse (5C)**, há um gap de **R$ [X]** no caixa final (M36), representando **[Y]%** de perda de performance. O gap se manifesta progressivamente:
- **M12:** R$ [A] ([B]% do Real)
- **M24:** R$ [C] ([D]% do Real)
- **M36:** R$ [X] ([Y]% do Real)

O **pior momento** de vulnerabilidade ocorre no **Mês [Z]**, com gap de **R$ [W]** ([V]% do caixa Real naquele mês).

#### **CAUSA (DECOMPOSIÇÃO SHAPLEY)**

Análise marginal revela que **3 fatores** explicam **[P]%** do gap total:

**1. Churn Dobrado (14% vs 7%)** → **[Q]%** do gap
- Impacto: -R$ [R]
- Mecânica: MRR cresce devagar (alta rotatividade anula novos clientes)
- Efeito cascata: Menor base → menor ARR → menor caixa acumulado

**2. CAC +50% (R$ 273 vs R$ 182)** → **[S]%** do gap
- Impacto: -R$ [T]
- Mecânica: Cada cliente custa 50% mais para adquirir
- Efeito cascata: Burn rate mais alto → caixa queima mais rápido

**3. ARPU -20% (R$ 76 vs R$ 95)** → **[U]%** do gap
- Impacto: -R$ [V]
- Mecânica: Receita por cliente menor (downgrade ou desconto)
- Efeito cascata: Mesmo volume de clientes gera menos MRR

**Fatores Secundários (20% do gap):**
- Conversão -20%: -[W]%
- Tráfego -30%: -[Z]%

#### **IMPLICAÇÃO**

🎯 **LEI DE PARETO APLICADA:**
Mitigar os **Top 3 fatores** (Churn/CAC/ARPU) reduz o gap em **[P]%**, transformando o Estresse em algo próximo ao Real.

📊 **ANÁLISE DE SENSIBILIDADE CRUZADA:**
- Se melhorarmos **apenas Churn** (de 14% para 10%):
  - Gap cai de R$ [X] para R$ [Y] (-[Z]%)
  - Estresse passa de "crítico" para "moderado"

- Se melhorarmos **Churn + CAC**:
  - Gap cai para R$ [A] (-[B]%)
  - Estresse se aproxima do Real em [C]%

- Se melhorarmos **Top 3 simultaneamente**:
  - Gap cai para R$ [D] (-[E]%)
  - **Estresse se torna viável** (caixa positivo, break-even atingido)

⚠️ **RISCO DE CORRELAÇÃO:**
Na prática, esses fatores **não são independentes**:
- Alto churn → Precisa gastar mais em CAC (para compensar)
- Alto CAC → Atrai clientes ruins → Aumenta churn
- **Espiral negativa:** Churn ↑ → CAC ↑ → Margem ↓ → Caixa ↓↓↓

#### **AÇÃO RECOMENDADA**

**ESTRATÉGIA: MITIGAÇÃO HIERÁRQUICA (DO PIOR PARA O MELHOR)**

---

**PRIORIDADE 1: BLINDAR CONTRA CHURN (40% do gap)**

**Ação 1.1: Sistema de Early Warning (Churn Prediction)**
- **O quê:** ML model para prever churn com 7 dias de antecedência
- **Investimento:** R$ [F] (dev + dados)
- **Impacto:** Reduz churn de 14% (estresse) para 10% → Gap cai [G]%

**Ação 1.2: Onboarding Obrigatório (First Value < 5min)**
- **O quê:** Tutorial interativo + quick win na primeira sessão
- **Investimento:** R$ [H]
- **Impacto:** Melhora retenção M1 de 80% para 92% → Churn inicial cai 30%

**ROI Prioridade 1:** Investir R$ [I] → Reduzir gap em R$ [J] (ROI de [K]x)



**PRIORIDADE 2: OTIMIZAR CAC (27% do gap)**

**Ação 2.1: Referral Program (CAC ~R$ 0)**
- **O quê:** Usuário indica 3 amigos → ganha 1 mês grátis
- **Investimento:** R$ [L] (sistema + incentivos)
- **Impacto:** 20% dos novos clientes vêm via referral → CAC mix cai 15%

**Ação 2.2: SEO + Content Marketing (CAC orgânico R$ 50)**
- **O quê:** 20 artigos otimizados + backlinks
- **Investimento:** R$ [M]
- **Impacto:** 30% do tráfego vira orgânico em 6 meses → CAC cai 20%

**ROI Prioridade 2:** Investir R$ [N] → Reduzir gap em R$ [O] (ROI de [P]x)

---

**PRIORIDADE 3: PROTEGER ARPU (18% do gap)**

**Ação 3.1: Feature Gating (Versão Freemium → Premium)**
- **O quê:** Limitar features críticas no plano Lite
- **Investimento:** R$ [Q] (dev)
- **Impacto:** Conversão de Lite para Pro aumenta de 8% para 15%

**Ação 3.2: Upsell Proativo (IA sugere upgrade)**
- **O quê:** Quando usuário atinge limite, sugerir upgrade
- **Investimento:** R$ [R]
- **Impacto:** ARPU mix sobe de R$ 76 para R$ 85 (+12%)

**ROI Prioridade 3:** Investir R$ [S] → Reduzir gap em R$ [T] (ROI de [U]x)

---

#### **CENÁRIO COMBINADO (MITIGAÇÃO TOTAL)**

Se executarmos **Prioridades 1 + 2 + 3:**

**INVESTIMENTO TOTAL:** R$ [I+N+S] = R$ [V]

**IMPACTO NO GAP:**
- Gap original: R$ [X] (100%)
- Gap após mitigação: R$ [W] (35%)
- **Redução de 65%** do gap total

**NOVO CENÁRIO ESTRESSE MITIGADO:**
- Caixa final: R$ [Y] (vs R$ [B] original)
- MRR final: R$ [Z] (vs R$ [C] original)
- Break-even: M[AA] (vs M[BB] original)
- **Status:** "Estresse Moderado" → Viável com margem apertada

**ROI CONSOLIDADO:**
- Investir R$ [V] → Ganhar R$ [W] de proteção
- ROI de **[W/V]x**
- Payback em **[meses] meses**

#### **PLANO DE CONTINGÊNCIA**

**Se o Estresse se materializar:**

**Fase 1 (Mês 0-6):** Sinais precoces
- Monitor: Churn > 10% por 2 meses consecutivos
- Ação: Ativar Prioridade 1 imediatamente

**Fase 2 (Mês 6-12):** Confirmação de tendência
- Monitor: CAC > R$ 250 ou MRR growth < 5%/mês
- Ação: Ativar Prioridade 2 + cortar custos não-essenciais

**Fase 3 (Mês 12-18):** Crise instalada
- Monitor: Runway < 3 meses
- Ação: Captação emergencial ou pivot estratégico

**Gatilhos de Alerta Vermelho:**
- Churn > 12% por 3 meses
- CAC > R$ 300
- Caixa < R$ 20k
→ **Ação:** Convocar board, revisar modelo completo

:::
```

---

### **MÉTRICAS-CHAVE A CALCULAR**

```python
# No seu código, calcular:

metricas_gap = {
    'gap_caixa_m36': df_stress_m.iloc[-1]['caixa'] - df_real_m.iloc[-1]['caixa'],
    'gap_caixa_pct': (gap_caixa_m36 / df_real_m.iloc[-1]['caixa']) * 100,
    'gap_mrr_m36': df_stress_m.iloc[-1]['mrr'] - df_real_m.iloc[-1]['mrr'],
    'gap_ltv_cac_m36': df_stress_m.iloc[-1]['ltv_cac'] - df_real_m.iloc[-1]['ltv_cac'],
    'mes_maior_gap': df_gap['gap_caixa'].abs().idxmax(),
    'valor_maior_gap': df_gap.loc[mes_maior_gap, 'gap_caixa'],
    'gap_medio_12_meses': df_gap['gap_caixa'].iloc[-12:].mean()
}

# Decomposição Shapley
contribuicoes = {
    'churn': calcular_impacto_isolado('churn_dobrado') / gap_total,
    'cac': calcular_impacto_isolado('cac_50pct') / gap_total,
    'arpu': calcular_impacto_isolado('arpu_menos20pct') / gap_total,
    'conversao': calcular_impacto_isolado('conversao_menos20pct') / gap_total,
    'trafego': calcular_impacto_isolado('trafego_menos30pct') / gap_total
}

# Ordenar por contribuição
top_fatores = sorted(contribuicoes.items(), key=lambda x: abs(x[1]), reverse=True)
```

---

### **METADADOS JSON - ATO 5**

```json
{
  "pagina": 5,
  "secao": "5.6",
  "visualizacao_id": "5.6.1_gap_analysis_real_vs_stress",
  "ato": 5,
  "ato_nome": "Vazamento",
  "timestamp": "2025-12-10T00:05:00Z",
  
  "titulos": {
    "coloquial": "Onde o modelo 'vaza' sob pressão?",
    "tecnico": "Gap Analysis Multidimensional - Real vs Estresse | Decomposição Shapley dos Fatores",
    "subtitulo": "Área vermelha = vazamento de performance | Waterfall = contribuição de cada fator"
  },
  
  "fonte_dados": {
    "inputs": ["df_real_m", "df_stress_m"],
    "funcoes_calculo": [
      "calcular_gap_analysis()",
      "decomposicao_gap_caixa()"
    ],
    "metodo_decomposicao": "Shapley Value (impacto marginal isolado)"
  },
  
  "parametros": {
    "metricas_analisadas": ["caixa", "mrr", "arr", "ltv_cac", "churn", "clientes"],
    "fatores_estresse": [
      {"fator": "churn", "variacao": "2x", "de": "7%", "para": "14%"},
      {"fator": "cac", "variacao": "+50%", "de": "R$182", "para": "R$273"},
      {"fator": "arpu", "variacao": "-20%", "de": "R$95", "para": "R$76"},
      {"fator": "conversao", "variacao": "-20%", "de": "12%", "para": "9.6%"},
      {"fator": "trafego", "variacao": "-30%", "de": "300", "para": "210"}
    ]
  },
  
  "resultados": {
    "gap_caixa_m36": {
      "absoluto": "CALCULAR_DINAMICAMENTE",
      "relativo_pct": "CALCULAR",
      "mes_maior_gap": "CALCULAR",
      "valor_maior_gap": "CALCULAR"
    },
    "decomposicao_shapley": {
      "churn": {"contribuicao_pct": "CALCULAR", "valor_rs": "CALCULAR", "rank": 1},
      "cac": {"contribuicao_pct": "CALCULAR", "valor_rs": "CALCULAR", "rank": 2},
      "arpu": {"contribuicao_pct": "CALCULAR", "valor_rs": "CALCULAR", "rank": 3},
      "conversao": {"contribuicao_pct": "CALCULAR", "valor_rs": "CALCULAR", "rank": 4},
      "trafego": {"contribuicao_pct": "CALCULAR", "valor_rs": "CALCULAR", "rank": 5}
    },
    "top_3_explicam_pct": "CALCULAR: sum(top3.contribuicao)"
  },
  
  "insights": {
    "fato": "Gap de R$ [X] (Y% do Real). Top 3 fatores explicam [Z]% do gap.",
    "causa": "Churn dobrado ([A]%) + CAC +50% ([B]%) + ARPU -20% ([C]%)",
    "implicacao": "Mitigar Top 3 reduz gap em [D]%, tornando Estresse viável",
    "acao": "Investir R$ [E] em CS + SEO + Upsell → Gap cai 65%"
  },
  
  "acoes_mitigacao": [
    {
      "prioridade": 1,
      "foco": "Churn",
      "acoes": ["Early warning ML", "Onboarding obrigatório"],
      "investimento": "CALCULAR",
      "reducao_gap_pct": "CALCULAR"
    },
    {
      "prioridade": 2,
      "foco": "CAC",
      "acoes": ["Referral program", "SEO + Content"],
      "investimento": "CALCULAR",
      "reducao_gap_pct": "CALCULAR"
    },
    {
      "prioridade": 3,
      "foco": "ARPU",
      "acoes": ["Feature gating", "Upsell proativo"],
      "investimento": "CALCULAR",
      "reducao_gap_pct": "CALCULAR"
    }
  ],
  
  "plano_contingencia": {
    "fase_1": {
      "trigger": "Churn > 10% por 2 meses",
      "acao": "Ativar Prioridade 1"
    },
    "fase_2": {
      "trigger": "CAC > R$250 ou MRR growth < 5%",
      "acao": "Ativar Prioridade 2 + cortes"
    },
    "fase_3": {
      "trigger": "Runway < 3 meses",
      "acao": "Captação emergencial ou pivot"
    }
  },
  
  "arquivos_output": {
    "figura_area_gap": "outputs/figs/pag5_gap_area_chart.png",
    "figura_waterfall": "outputs/figs/pag5_gap_waterfall.png",
    "tabela_decomposicao": "outputs/tables/pag5_gap_shapley.csv",
    "metadata": "outputs/metadata/pag5_ato5_metadata.json"
  }
}
```

---

---
##########################################################################################
# PARTE 4: ANEXOS TÉCNICOS
##########################################################################################

---

## 4.1 GLOSSÁRIO DE RISCO

```markdown
### **TERMOS FUNDAMENTAIS**

**RUNWAY**
- **Definição:** Número de semanas/meses que a empresa pode operar com o caixa atual, assumindo burn rate constante
- **Fórmula:** `Runway = Caixa / |Burn Rate|`
- **Threshold Seguro:** >= 12 semanas (3 meses)
- **Uso:** Métrica tática de liquidez

**BREAK-EVEN OPERACIONAL**
- **Definição:** Momento em que Receita >= Custos Operacionais (fluxo de caixa mensal >= 0)
- **Importância:** Empresa para de queimar caixa e se torna auto-sustentável
- **Benchmark:** < 24 meses para SaaS B2C

**VAR (VALUE AT RISK)**
- **Definição:** Perda máxima esperada no pior cenário de uma distribuição (ex: P5)
- **Fórmula:** `VaR_95% = Percentil_5(distribuição)`
- **Interpretação:** "Em 95% dos casos, a perda não será pior que isso"
- **Uso:** Quantificar downside risk

**CVAR (CONDITIONAL VAR)**
- **Definição:** Média das perdas no pior X% dos cenários (mais conservador que VaR)
- **Fórmula:** `CVaR_95% = Mean(valores < VaR_95%)`
- **Interpretação:** "Se as coisas derem muito errado (pior 5%), a perda média será essa"
- **Uso:** Stress testing extremo

**MONTE CARLO**
- **Definição:** Método de simulação que gera milhares de cenários aleatórios variando premissas-chave
- **Inputs:** Distribuições probabilísticas (normal, lognormal, triangular)
- **Outputs:** Distribuição de resultados (P5, P50, P95, etc.)
- **Uso:** Quantificar incerteza e probabilidades

**TORNADO PLOT**
- **Definição:** Gráfico de sensibilidade que mostra o impacto de variar cada premissa em ±X%
- **Visual:** Barras horizontais ordenadas por impacto (formato de tornado)
- **Uso:** Identificar premissas críticas (maior impacto = maior sensibilidade)

**GAP ANALYSIS**
- **Definição:** Comparação quantitativa entre dois cenários (ex: Real vs Estresse)
- **Métrica:** Gap absoluto (diferença em R$) e gap relativo (diferença em %)
- **Uso:** Identificar vulnerabilidades e priorizar mitigações

**SHAPLEY VALUE / DECOMPOSIÇÃO**
- **Definição:** Método para calcular a contribuição individual de cada fator para um resultado total
- **Lógica:** Variar cada fator isoladamente e medir impacto marginal
- **Uso:** Responder "quanto do gap vem do churn vs CAC vs ARPU?"

---

### **MÉTRICAS DERIVADAS**

**DISPERSÃO**
- **Fórmula:** `P95 - P5` ou `(P95 - P5) / P50`
- **Interpretação:** Largura da distribuição = grau de incerteza
- **Ideal:** Dispersão < 2x a mediana

**PROBABILIDADE DE QUEBRA**
- **Fórmula:** `P(Caixa_Final < 0) = Count(caixa < 0) / N_simulacoes`
- **Benchmark:** < 10% é aceitável
- **Uso:** Quantificar risco de falência

**CONCENTRAÇÃO DE RISCO**
- **Fórmula:** `Contribuição_Top3 / Contribuição_Total`
- **Interpretação:** Se > 70%, modelo depende muito de poucas premissas
- **Ideal:** Risco distribuído (nenhum fator > 30%)

---

### **CENÁRIOS**

**CENÁRIO REAL (5A)**
- Bootstrap com R$ 2k/mês
- Premissas conservadoras baseadas na realidade atual
- Churn 7%, CAC R$ 182, ARPU R$ 95

**CENÁRIO IDEAL (5B)**
- Benchmarks de mercado (top 25%)
- Execução perfeita sem erros
- Churn 4,2%, CAC R$ 120, ARPU R$ 120

**CENÁRIO ESTRESSE (5C)**
- Cisne negro (tudo dá errado)
- Churn dobrado (14%), CAC +50% (R$ 273), ARPU -20% (R$ 76)
- Tráfego -30%, Conversão -20%

---

### **THRESHOLDS E BENCHMARKS**

| Métrica | Crítico | Atenção | Seguro | Excelente |
|---------|---------|---------|--------|-----------|
| Runway | < 6 sem | 6-12 sem | 12-24 sem | > 24 sem |
| Break-Even | > M30 | M24-M30 | M18-M24 | < M18 |
| Prob. Quebra | > 15% | 10-15% | 5-10% | < 5% |
| VaR 95% | < -R$100k | -R$50k a -R$100k | -R$20k a -R$50k | > -R$20k |
| Gap Real/Stress | > 60% | 40-60% | 20-40% | < 20% |
| LTV/CAC | < 2x | 2-3x | 3-5x | > 5x |
| Churn | > 10% | 7-10% | 5-7% | < 5% |
```

---

## 4.2 METODOLOGIA MONTE CARLO DETALHADA

```markdown
### **1. FUNDAMENTOS TEÓRICOS**

**OBJETIVO:**
Gerar uma distribuição probabilística de resultados (caixa, MRR, LTV/CAC, etc.) considerando a incerteza inerente às premissas do modelo.

**PREMISSA CENTRAL:**
Nenhuma premissa é exata - todas têm variabilidade natural. Ex:
- Churn não é sempre 7% - varia entre 5-9%
- CAC não é fixo R$ 182 - depende do canal, creative, sazonalidade

**MÉTODO:**
1. Modelar cada premissa incerta como uma **distribuição probabilística**
2. Sortear valores aleatórios dessas distribuições
3. Rodar o modelo financeiro completo com esses valores
4. Repetir 10.000 vezes
5. Agregar resultados em percentis (P5, P10, ..., P95)

---

### **2. ESCOLHA DAS DISTRIBUIÇÕES**

**PREMISSA: CHURN**
- **Distribuição:** Normal truncada
- **Parâmetros:** μ = 0.07, σ = 0.023, min = 0.03, max = 0.15
- **Justificativa:**
  - Taxa de cancelamento varia mensalmente por motivos aleatórios
  - Truncada para evitar valores impossíveis (churn negativo ou > 100%)
- **Código:**
```python
churn_sample = np.clip(np.random.normal(0.07, 0.023, size=10000), 0.03, 0.15)
```

**PREMISSA: CAC**
- **Distribuição:** Normal truncada
- **Parâmetros:** μ = R$ 182, σ = R$ 87, min = R$ 50, max = R$ 500
- **Justificativa:**
  - CPCs variam diariamente (competição, sazonalidade)
  - σ alto (47% do μ) reflete volatilidade real de ads
- **Código:**
```python
cac_sample = np.clip(np.random.normal(182, 87, size=10000), 50, 500)
```

**PREMISSA: ARPU**
- **Distribuição:** Lognormal
- **Parâmetros:** μ_log = 4.55, σ_log = 0.12 → médiareal ≈ R$ 95
- **Justificativa:**
  - ARPU não pode ser negativo
  - Distribuição assimétrica (cauda longa para valores altos)
  - Captura mix de planos (Lite R$ 70 + Pro R$ 120)
- **Código:**
```python
arpu_sample = np.random.lognormal(4.55, 0.12, size=10000)
```

**PREMISSA: TRÁFEGO INICIAL**
- **Distribuição:** Triangular
- **Parâmetros:** min = 250, mode = 300, max = 400
- **Justificativa:**
  - Não temos histórico → usar estimativa pessimista/base/otimista
  - Mode = valor mais provável (base do plano)
  - Min/Max = bounds realistas
- **Código:**
```python
trafego_sample = np.random.triangular(250, 300, 400, size=10000)
```

---

### **3. CORRELAÇÕES ENTRE VARIÁVEIS**

**POR QUE IMPORTA:**
Na prática, premissas não são independentes:
- Churn alto → clientes ruins → provavelmente vieram de CAC alto (anúncios baratos, mal segmentados)
- Conversão baixa → precisa gastar mais (aumentar CAC) para compensar

**CORRELAÇÕES APLICADAS:**

**Corr(Churn, CAC) = +0.42**
- Clientes de CAC alto tendem a churnar mais
- Método: Usar Cholesky decomposition ou copula
```python
# Matriz de correlação
corr_matrix = np.array([[1.0, 0.42], [0.42, 1.0]])

# Gerar samples correlacionados
samples = np.random.multivariate_normal(
    mean=[churn_mean, cac_mean],
    cov=corr_matrix,
    size=10000
)
```

**Corr(Conversão, CAC) = -0.58**
- Menor conversão exige mais gasto para atingir mesmo volume
- Se conversão cai 1 p.p. → CAC sobe ~R$ 23

---

### **4. ALGORITMO COMPLETO**

```python
def rodar_monte_carlo(PREMISSAS, n_sims=10000, seed=42):
    """
    Executa simulação Monte Carlo
    
    Returns:
        DataFrame com n_sims linhas × colunas de resultados
    """
    
    np.random.seed(seed)  # Reprodutibilidade
    resultados = []
    
    for sim_id in range(n_sims):
        # 1. SORTEAR PREMISSAS (com correlações)
        premissas_sim = PREMISSAS.copy()
        
        # Churn
        premissas_sim['churn_inicial'] = np.clip(
            np.random.normal(0.07, 0.023), 0.03, 0.15
        )
        
        # CAC (correlacionado com churn)
        cac_base = np.random.normal(182, 87)
        ajuste_churn = (premissas_sim['churn_inicial'] - 0.07) * 500  # Se churn +1% → CAC +R$5
        premissas_sim['cac_medio'] = np.clip(cac_base + ajuste_churn, 50, 500)
        
        # ARPU
        premissas_sim['arpu_base'] = np.random.lognormal(4.55, 0.12)
        
        # Tráfego
        premissas_sim['trafego_inicial'] = np.random.triangular(250, 300, 400)
        
        # Conversão (correlacionada com CAC)
        conv_base = np.random.normal(0.12, 0.02)
        ajuste_cac = (premissas_sim['cac_medio'] - 182) / 500 * -0.03  # CAC alto → conversão baixa
        premissas_sim['taxa_conversao_trial_pago'] = np.clip(conv_base + ajuste_cac, 0.08, 0.18)
        
        # 2. RODAR MODELO COMPLETO
        df_sim_m, df_sim_s = gerar_cenario_completo(premissas_sim)
        
        # 3. EXTRAIR MÉTRICAS FINAIS
        resultados.append({
            'simulacao_id': sim_id,
            'caixa_final': df_sim_m.iloc[-1]['caixa'],
            'arr_final': df_sim_m.iloc[-1]['arr'],
            'mrr_final': df_sim_m.iloc[-1]['mrr'],
            'usuarios_final': df_sim_m.iloc[-1]['usuarios'],
            'ltv_cac_final': df_sim_m.iloc[-1]['ltv_cac'],
            'churn_medio': df_sim_m['churn'].mean(),
            'payback_meses': calcular_payback(df_sim_m),
            'mes_breakeven': identificar_breakeven(df_sim_m)['mes']
        })
    
    return pd.DataFrame(resultados)
```

---

### **5. VALIDAÇÃO ESTATÍSTICA**

**TESTE 1: Kolmogorov-Smirnov (Normalidade)**
```python
from scipy.stats import kstest

# Testar se caixa_final segue distribuição esperada
stat, p_value = kstest(mc_results['caixa_final'], 'norm')

# Interpretação:
# p_value > 0.05 → Não rejeita normalidade (distribuição válida)
# p_value < 0.05 → Distribuição anômala (investigar)
```

**TESTE 2: Convergência**
```python
# Calcular P50 a cada 1000 sims
p50_evolution = []
for n in range(1000, 10001, 1000):
    p50 = mc_results.iloc[:n]['caixa_final'].median()
    p50_evolution.append(p50)

# Se estabilizou (variação < 2%) → convergiu
variacao = np.std(p50_evolution[-3:]) / np.mean(p50_evolution[-3:])
converged = variacao < 0.02
```

**TESTE 3: Reprodutibilidade**
```python
# Rodar 2x com mesmo seed
mc_1 = rodar_monte_carlo(PREMISSAS, seed=42)
mc_2 = rodar_monte_carlo(PREMISSAS, seed=42)

# Deve ser idêntico
assert mc_1.equals(mc_2)
```

---

### **6. LIMITAÇÕES E CUIDADOS**

⚠️ **Limitação 1: Independência Temporal**
- Assume que churn em M12 não afeta churn em M13
- Na prática, há momentum (mês ruim → próximo mês também ruim)
- Solução: Modelar autocorrelação (AR(1) model)

⚠️ **Limitação 2: Eventos Raros**
- Monte Carlo captura variabilidade normal, não cisnes negros
- Ex: Pandemia, concorrente gigante entrando no mercado
- Solução: Modelar Estresse 5C separadamente

⚠️ **Limitação 3: Correlações Fixas**
- Assumimos Corr(Churn, CAC) = 0.42 sempre
- Na prática, correlação pode mudar ao longo do tempo
- Solução: Usar correlações time-varying (mais complexo)

⚠️ **Limitação 4: Distribuições Assumidas**
- Churn como Normal pode não ser ideal (pode ter cauda pesada)
- Testar distribuições alternativas (Beta, Gamma)
```

---

## 4.3 PSEUDOCÓDIGO DO ENGINE COMPLETO

```markdown
### **FLUXO GERAL DO MOTOR FINANCEIRO**

```
MAIN():
  1. CARREGAR PREMISSAS (dict com 150+ parâmetros)
  2. GERAR CENÁRIO REAL (5A)
  3. GERAR CENÁRIO IDEAL (5B)  
  4. GERAR CENÁRIO ESTRESSE (5C)
  5. RODAR MONTE CARLO (10k sims)
  6. CALCULAR SENSIBILIDADE TORNADO
  7. CALCULAR RUNWAY SEMANAL
  8. IDENTIFICAR BREAK-EVEN
  9. CALCULAR GAP ANALYSIS
  10. GERAR VISUALIZAÇÕES
  11. GERAR METADADOS JSON
  12. EXPORTAR OUTPUTS
```

---

### **FUNÇÃO 1: GERAR_CENARIO**

```python
FUNCTION gerar_cenario(premissas, tipo='real'):
    """
    Gera DataFrames mensais e semanais para um cenário
    
    Args:
        premissas: dict com parâmetros
        tipo: 'real', 'ideal' ou 'estresse'
    
    Returns:
        (df_mensal, df_semanal)
    """
    
    # PASSO 1: APLICAR MULTIPLICADORES POR TIPO
    IF tipo == 'ideal':
        premissas['churn_inicial'] *= 0.6
        premissas['cac_medio'] *= 0.66
        premissas['arpu_base'] *= 1.26
        premissas['taxa_conversao'] *= 1.5
    ELIF tipo == 'estresse':
        premissas['churn_inicial'] *= 2.0
        premissas['cac_medio'] *= 1.5
        premissas['arpu_base'] *= 0.8
        premissas['taxa_conversao'] *= 0.8
        premissas['trafego_inicial'] *= 0.7
    
    # PASSO 2: INICIALIZAR ARRAYS
    meses = 36
    caixa = [premissas['caixa_inicial']]
    usuarios = [0]
    mrr = [0]
    
    # PASSO 3: LOOP MENSAL
    FOR mes IN range(1, meses + 1):
        # 3.1. CRESCIMENTO DE TRÁFEGO
        trafego = premissas['trafego_inicial'] * (1 + premissas['growth_trafego']) ** mes
        trafego *= aplicar_sazonalidade(mes, premissas['sazonalidade_amplitude'])
        
        # 3.2. NOVOS USUÁRIOS
        trials = trafego * premissas['taxa_conversao_trial']
        novos_pagos = trials * premissas['taxa_conversao_trial_pago']
        
        # 3.3. CHURN (perda de usuários)
        churn_mes = usuarios[mes-1] * premissas['churn_inicial']
        usuarios_mes = usuarios[mes-1] + novos_pagos - churn_mes
        
        # 3.4. RECEITA (MRR)
        arpu_mix = calcular_arpu_mix(premissas['mix_lite_pct'], 
                                      premissas['preco_lite'], 
                                      premissas['preco_pro'])
        mrr_mes = usuarios_mes * arpu_mix
        receita_mes = mrr_mes + (novos_pagos * arpu_mix * 0.5)  # Pro-rata
        
        # 3.5. CUSTOS
        custo_marketing = novos_pagos * premissas['cac_medio']
        custo