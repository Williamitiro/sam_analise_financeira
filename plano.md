# Plano Estratégico para Elaboração da Lógica do Modelo Financeiro Dinâmico

Analisei profundamente os dois documentos fornecidos e compreendi perfeitamente o objetivo: criar a **arquitetura lógica completa** para um sistema de modelagem financeira dinâmica que permita simular cenários de negócio do SAM com precisão cirúrgica.

## Contexto e Objetivo

Você precisa de um **sistema modular e configurável** que:
- Permita alterar premissas-chave via interface (inputs)
- Calcule automaticamente as projeções financeiras mês a mês
- Aplique lógicas de negócio complexas e condicionais
- Gere outputs visuais e KPIs para análise de viabilidade
- Seja implementável como um notebook Jupyter ou mini-app web

**Não é uma planilha estática. É um motor de simulação financeira.**

---

## FASE 1: MAPEAMENTO COMPLETO DE VARIÁVEIS

### 1.1 Painel de Controle (Inputs Configuráveis)

Estas são as **células de configuração** que o usuário poderá alterar:

#### **A. FINANCIAMENTO E CAPITAL**
```
┌─────────────────────────────────────────┬─────────────┬──────────────────────────────┐
│ Variável                                 │ Valor Base  │ Descrição                     │
├─────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ aporte_mensal_fixo                      │ R$ 1.800    │ Aporte mensal do fundador    │
│ meses_aporte_fixo                       │ 12          │ Duração do aporte fixo       │
│ capital_inicial_caixa                   │ R$ 8.000    │ Capex inicial (equipamentos) │
└─────────────────────────────────────────┴─────────────┴──────────────────────────────┘
```

#### **B. FUNIL DE AQUISIÇÃO**
```
┌─────────────────────────────────────────┬─────────────┬──────────────────────────────┐
│ Variável                                 │ Valor Base  │ Descrição                     │
├─────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ visitantes_mes1                         │ 1.000       │ Tráfego inicial              │
│ taxa_crescimento_trafego_mensal         │ 20%         │ Crescimento orgânico         │
│ taxa_conversao_trial                    │ 5%          │ Visitante → Trial            │
│ taxa_conversao_pagante                  │ 15%         │ Trial → Cliente pagante      │
│ churn_mensal                            │ 4%          │ Cancelamento mensal          │
└─────────────────────────────────────────┴─────────────┴──────────────────────────────┘
```

#### **C. MODELO DE RECEITA**
```
┌─────────────────────────────────────────┬─────────────┬──────────────────────────────┐
│ Variável                                 │ Valor Base  │ Descrição                     │
├─────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ arpu_medio                              │ R$ 97,00    │ Receita média/usuário/mês    │
│ mix_plano_lite                          │ 50%         │ Distribuição de planos       │
│ mix_plano_trader                        │ 30%         │                              │
│ mix_plano_pro                           │ 20%         │                              │
└─────────────────────────────────────────┴─────────────┴──────────────────────────────┘
```

#### **D. CUSTOS VARIÁVEIS (COGS)**
```
┌─────────────────────────────────────────┬─────────────┬──────────────────────────────┐
│ Variável                                 │ Valor Base  │ Descrição                     │
├─────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ custo_ia_por_usuario                    │ R$ 5,00     │ Custo API LLM/usuário/mês    │
│ aliquota_impostos                       │ 6%          │ Simples Nacional s/ receita  │
└─────────────────────────────────────────┴─────────────┴──────────────────────────────┘
```

#### **E. INFRAESTRUTURA ESCALÁVEL (3 TIERS)**
```
┌──────────────┬───────────────┬────────────────┬──────────────────────────────────┐
│ Tier         │ Custo Mensal  │ Limite Usuários│ Composição                        │
├──────────────┼───────────────┼────────────────┼──────────────────────────────────┤
│ TIER 1       │ R$ 209,00     │ 0 - 100        │ VPS Principal (R$55) +            │
│ (Validação)  │               │                │ VPS Coleta MT5 (R$150) +          │
│              │               │                │ Domínio (R$4)                     │
├──────────────┼───────────────┼────────────────┼──────────────────────────────────┤
│ TIER 2       │ R$ 5.559,00   │ 101 - 500      │ API Cedro (R$5.000) +             │
│ (Escala)     │               │                │ VPS Robusta (R$500) +             │
│              │               │                │ Ferramentas (R$59)                │
├──────────────┼───────────────┼────────────────┼──────────────────────────────────┤
│ TIER 3       │ Base + Var    │ 501+           │ Tier 2 + Auto-scaling             │
│ (Hiperescala)│               │                │ (R$1,50/usuário adicional)        │
└──────────────┴───────────────┴────────────────┴──────────────────────────────────┘

VARIÁVEIS DO SISTEMA:
- infra_tier1_custo_fixo        = R$ 209,00
- infra_tier1_limite            = 100 usuários
- infra_tier2_custo_fixo        = R$ 5.559,00
- infra_tier2_limite            = 500 usuários
- infra_tier3_custo_por_usuario = R$ 1,50
```

#### **F. MARKETING (2 FASES)**
```
┌─────────────┬──────────────┬─────────────────────────────────────────────┐
│ Fase        │ Duração      │ Lógica                                       │
├─────────────┼──────────────┼─────────────────────────────────────────────┤
│ FASE 1      │ Mês 1-3      │ Gasto fixo mensal                            │
│ (Validação) │              │ marketing_fase1_custo_fixo = R$ 500          │
├─────────────┼──────────────┼─────────────────────────────────────────────┤
│ FASE 2      │ Mês 4+       │ % do Lucro Bruto do mês                      │
│ (Reinvest.) │              │ marketing_fase2_perc_lucro_bruto = 25%       │
└─────────────┴──────────────┴─────────────────────────────────────────────┘

REGRA: max(0, Lucro_Bruto × 0.25) → Nunca negativo
```

#### **G. SALÁRIO DO FUNDADOR (CONDICIONAL)**
```
┌─────────────────────────────────────┬─────────────┬──────────────────────────┐
│ Variável                             │ Valor Base  │ Lógica                    │
├─────────────────────────────────────┼─────────────┼──────────────────────────┤
│ salario_fundador_valor              │ R$ 5.000    │ Pró-labore mensal         │
│ salario_fundador_mes_inicio_ideal   │ 6           │ Quando DEVERIA começar    │
│ salario_caixa_minimo_seguranca      │ R$ 10.000   │ Saldo mínimo obrigatório  │
└─────────────────────────────────────┴─────────────┴──────────────────────────┘

REGRA DURA (Aplicada TODO mês t):
SE (t >= mes_inicio_ideal) E (Saldo_Caixa[t-1] > caixa_minimo) 
   ENTÃO Pagar = salario_valor
   SENÃO Pagar = 0
```

#### **H. PARÂMETROS DE ANÁLISE (NÃO SÃO CUSTOS)**
```
┌─────────────────────────────────────┬─────────────┬──────────────────────────┐
│ Variável                             │ Valor Base  │ Uso                       │
├─────────────────────────────────────┼─────────────┼──────────────────────────┤
│ cac_pago_meta                       │ R$ 500      │ Para calcular LTV/CAC     │
│ ltv_calculado                       │ [fórmula]   │ Valor-vida do cliente     │
└─────────────────────────────────────┴─────────────┴──────────────────────────┘
```

---

## FASE 2: MOTOR DE PROJEÇÃO (LOOP MÊS A MÊS)

### 2.1 Sequência de Cálculo para Cada Mês `t` (1 a 36)

```
┌─────┬───────────────────────────────────────────────────────────────────────┐
│ Ord │ Cálculo                                                                │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 01  │ Usuarios_Iniciais[t] = Usuarios_Finais[t-1]                           │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 02  │ Visitantes[t] = Visitantes[t-1] × (1 + taxa_cresc_trafego)           │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 03  │ Novos_Trials[t] = Visitantes[t] × taxa_conv_trial                    │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 04  │ Novos_Pagantes[t] = Novos_Trials[t] × taxa_conv_pagante              │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 05  │ Usuarios_Perdidos[t] = Usuarios_Iniciais[t] × churn_mensal           │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 06  │ Usuarios_Finais[t] = Usuarios_Iniciais[t] +                          │
│     │                       Novos_Pagantes[t] - Usuarios_Perdidos[t]        │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 07  │ MRR[t] = Usuarios_Finais[t] × arpu_medio                             │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 08  │ COGS[t] = Usuarios_Finais[t] × custo_ia_por_usuario                  │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 09  │ Impostos[t] = MRR[t] × aliquota_impostos                             │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 10  │ Lucro_Bruto[t] = MRR[t] - COGS[t] - Impostos[t]                      │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 11  │ Custo_Infra[t] = [APLICAR LÓGICA TIER - Ver 2.2]                     │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 12  │ Custo_Marketing[t] = [APLICAR LÓGICA FASES - Ver 2.3]                │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 13  │ Salario_Pago[t] = [APLICAR LÓGICA CONDICIONAL - Ver 2.4]             │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 14  │ OPEX_Total[t] = Custo_Infra[t] + Custo_Marketing[t] +                │
│     │                  Salario_Pago[t]                                       │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 15  │ Resultado_Operacional[t] = Lucro_Bruto[t] - OPEX_Total[t]            │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 16  │ Aporte[t] = SE t <= meses_aporte_fixo                                │
│     │             ENTÃO aporte_mensal_fixo                                   │
│     │             SENÃO 0                                                    │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 17  │ Fluxo_Caixa[t] = Resultado_Operacional[t] + Aporte[t]                │
├─────┼───────────────────────────────────────────────────────────────────────┤
│ 18  │ Saldo_Caixa[t] = Saldo_Caixa[t-1] + Fluxo_Caixa[t]                   │
│     │                  (Inicial: -capital_inicial_caixa)                     │
└─────┴───────────────────────────────────────────────────────────────────────┘
```

### 2.2 LÓGICA: Custo de Infraestrutura por Tier

```python
def calcular_custo_infra(usuarios_finais):
    """
    Retorna o custo de infraestrutura baseado em tiers escaláveis.
    
    TIER 1 (0-100 usuários): R$ 209/mês (Validação com MT5)
    TIER 2 (101-500 usuários): R$ 5.559/mês (API Profissional)
    TIER 3 (501+ usuários): TIER 2 + R$ 1,50 por usuário adicional
    """
    if usuarios_finais <= 100:
        return 209.00
    
    elif usuarios_finais <= 500:
        return 5559.00
    
    else:  # TIER 3
        usuarios_adicionais = usuarios_finais - 500
        custo_variavel = usuarios_adicionais * 1.50
        return 5559.00 + custo_variavel
```

**Para Planilha/Frontend:**
```
Célula: Custo_Infra[t]

Fórmula (Excel/Google Sheets):
=SE(Usuarios_Finais[t] <= $Config.Tier1_Limite;
    $Config.Tier1_Custo;
    SE(Usuarios_Finais[t] <= $Config.Tier2_Limite;
        $Config.Tier2_Custo;
        $Config.Tier2_Custo + 
        ((Usuarios_Finais[t] - $Config.Tier2_Limite) * $Config.Tier3_Custo_Usuario)
    )
)
```

### 2.3 LÓGICA: Gasto de Marketing em Fases

```python
def calcular_custo_marketing(mes_atual, lucro_bruto, config):
    """
    FASE 1 (Meses 1-3): Gasto fixo de validação
    FASE 2 (Mês 4+): 25% do Lucro Bruto do mês
    """
    if mes_atual <= config['marketing_fase1_meses']:
        return config['marketing_fase1_custo_fixo']
    
    else:  # FASE 2
        gasto = lucro_bruto * config['marketing_fase2_perc_lucro_bruto']
        return max(0, gasto)  # Nunca negativo
```

**Para Planilha:**
```
Célula: Custo_Marketing[t]

Fórmula:
=SE(t <= $Config.Marketing_Fase1_Meses;
    $Config.Marketing_Fase1_Fixo;
    MAX(0; Lucro_Bruto[t] * $Config.Marketing_Fase2_Perc)
)
```

### 2.4 LÓGICA: Salário do Fundador (Condicional Dura)

```python
def calcular_salario_fundador(mes_atual, saldo_caixa_anterior, config):
    """
    REGRA DURA: Só paga se (mês >= início) E (caixa > mínimo segurança)
    
    Permite que o fundador configure:
    - Mês de início ideal (6, 8, 12, etc.)
    - Valor do pró-labore
    - Saldo mínimo de segurança
    """
    inicio_ok = (mes_atual >= config['salario_fundador_mes_inicio'])
    caixa_ok = (saldo_caixa_anterior > config['salario_caixa_minimo'])
    
    if inicio_ok and caixa_ok:
        return config['salario_fundador_valor']
    else:
        return 0
```

**Para Planilha:**
```
Célula: Salario_Pago[t]

Fórmula:
=SE(E(
    t >= $Config.Salario_Mes_Inicio;
    Saldo_Caixa[t-1] > $Config.Salario_Caixa_Minimo
);
    $Config.Salario_Valor;
    0
)
```

---

## FASE 3: ESTRUTURA DE DADOS E IMPLEMENTAÇÃO

### 3.1 Tabela de Configuração (Inputs)

```
┌────────────────────────┬─────────────┬─────────────────────────┐
│ Categoria              │ Variável    │ Valor Padrão            │
├────────────────────────┼─────────────┼─────────────────────────┤
│ CAPITAL                │             │                         │
│                        │ aporte_m    │ 1800                    │
│                        │ meses_apo   │ 12                      │
│                        │ capex_ini   │ 8000                    │
├────────────────────────┼─────────────┼─────────────────────────┤
│ AQUISIÇÃO              │             │                         │
│                        │ visit_m1    │ 1000                    │
│                        │ tx_cresc    │ 0.20                    │
│                        │ tx_trial    │ 0.05                    │
│                        │ tx_pag      │ 0.15                    │
│                        │ churn       │ 0.04                    │
├────────────────────────┼─────────────┼─────────────────────────┤
│ RECEITA                │             │                         │
│                        │ arpu        │ 97                      │
│                        │ impostos    │ 0.06                    │
├────────────────────────┼─────────────┼─────────────────────────┤
│ COGS                   │             │                         │
│                        │ custo_ia    │ 5                       │
├────────────────────────┼─────────────┼─────────────────────────┤
│ INFRA (TIER 1)         │             │                         │
│                        │ t1_custo    │ 209                     │
│                        │ t1_limite   │ 100                     │
├────────────────────────┼─────────────┼─────────────────────────┤
│ INFRA (TIER 2)         │             │                         │
│                        │ t2_custo    │ 5559                    │
│                        │ t2_limite   │ 500                     │
├────────────────────────┼─────────────┼─────────────────────────┤
│ INFRA (TIER 3)         │             │                         │
│                        │ t3_custo_u  │ 1.50                    │
├────────────────────────┼─────────────┼─────────────────────────┤
│ MARKETING (FASE 1)     │             │                         │
│                        │ mkt_f1_fix  │ 500                     │
│                        │ mkt_f1_mes  │ 3                       │
├────────────────────────┼─────────────┼─────────────────────────┤
│ MARKETING (FASE 2)     │             │                         │
│                        │ mkt_f2_pct  │ 0.25                    │
├────────────────────────┼─────────────┼─────────────────────────┤
│ SALÁRIO                │             │                         │
│                        │ sal_valor   │ 5000                    │
│                        │ sal_inicio  │ 6                       │
│                        │ sal_caixa   │ 10000                   │
└────────────────────────┴─────────────┴─────────────────────────┘
```

### 3.2 Tabela de Projeção (36 linhas × Colunas)

```
Colunas obrigatórias:
├─ [01] Mes
├─ [02] Usuarios_Iniciais
├─ [03] Visitantes
├─ [04] Novos_Trials
├─ [05] Novos_Pagantes
├─ [06] Usuarios_Perdidos
├─ [07] Usuarios_Finais
├─ [08] MRR
├─ [09] COGS
├─ [10] Impostos
├─ [11] Lucro_Bruto
├─ [12] Custo_Infra
├─ [13] Custo_Marketing
├─ [14] Salario_Pago
├─ [15] OPEX_Total
├─ [16] Resultado_Operacional
├─ [17] Aporte
├─ [18] Fluxo_Caixa
└─ [19] Saldo_Caixa
```

---

## FASE 4: CÁLCULO DE KPIs

### 4.1 KPIs Essenciais

```python
def calcular_kpis(projecao_df, config):
    """
    Calcula os principais indicadores de viabilidade do negócio.
    """
    kpis = {}
    
    # 1. Ponto de Equilíbrio (Break-Even)
    break_even = projecao_df[projecao_df['Resultado_Operacional'] > 0]
    if not break_even.empty:
        kpis['Break_Even_Mes'] = break_even.iloc[0]['Mes']
    else:
        kpis['Break_Even_Mes'] = "Não atingido"
    
    # 2. Payback do Investimento
    payback = projecao_df[projecao_df['Saldo_Caixa'] > 0]
    if not payback.empty:
        kpis['Payback_Mes'] = payback.iloc[0]['Mes']
    else:
        kpis['Payback_Mes'] = "Não atingido"
    
    # 3. Vale da Morte (Necessidade Máxima de Caixa)
    kpis['Vale_da_Morte'] = projecao_df['Saldo_Caixa'].min()
    
    # 4. Runway (Meses até acabar o dinheiro)
    saldo_negativo = projecao_df[projecao_df['Saldo_Caixa'] < 0]
    if not saldo_negativo.empty:
        kpis['Runway_Meses'] = saldo_negativo.iloc[0]['Mes'] - 1
    else:
        kpis['Runway_Meses'] = "> 36"
    
    # 5. LTV (Lifetime Value)
    lucro_bruto_por_usuario = (
        config['arpu'] * (1 - config['impostos']) - config['custo_ia']
    )
    kpis['LTV'] = lucro_bruto_por_usuario / config['churn']
    
    # 6. LTV/CAC Ratio
    kpis['LTV_CAC_Ratio'] = kpis['LTV'] / config.get('cac_pago_meta', 500)
    
    # 7. MRR Final (Ano 3)
    kpis['MRR_Ano3'] = projecao_df.iloc[-1]['MRR']
    
    # 8. Total de Usuários (Ano 3)
    kpis['Usuarios_Ano3'] = projecao_df.iloc[-1]['Usuarios_Finais']
    
    return kpis
```

### 4.2 Fórmula do LTV

```
LTV = (ARPU × (1 - Taxa_Imposto) - COGS_por_Usuario) / Churn_Mensal

Exemplo:
LTV = (97 × (1 - 0.06) - 5) / 0.04
LTV = (97 × 0.94 - 5) / 0.04
LTV = (91.18 - 5) / 0.04
LTV = 86.18 / 0.04
LTV = R$ 2.154,50
```

---

## FASE 5: RESPOSTA ÀS SUAS PERGUNTAS ESPECÍFICAS

### Q1: "Qual VPS suporta 100 usuários?"

**Resposta Técnica:**

```
TIER 1 (0-100 usuários): Hostinger KVM 4
├─ Specs: 4 vCPU, 16GB RAM, 200GB NVMe
├─ Custo: R$ 55/mês
├─ Justificativa: 
│  └─ Backend: PostgreSQL + Redis + API FastAPI
│  └─ Processamento: Celery Workers (leve)
│  └─ Latência: < 500ms (P99)
│  └─ Estimativa conservadora: 100 usuários concorrentes OK
│
└─ LIMITE REAL: Monitorar CPU/RAM. Se CPU > 70% em média,
   considerar upgrade para Tier 2 ANTES de 100 usuários.
```

### Q2: "Como implementar a lógica do salário em planilha?"

**Resposta: Estrutura em Células**

```
Aba: Config
├─ C5: salario_valor = 5000
├─ C6: salario_mes_inicio = 6  ← CÉLULA EDITÁVEL
├─ C7: salario_caixa_minimo = 10000

Aba: Projecao
Coluna N (Salario_Pago):

Célula N2 (Mês 1):
=SE(E(A2>=$Config.$C$6; M1>$Config.$C$7); $Config.$C$5; 0)
         ↑          ↑            ↑            ↑       ↑
         │          │            │            │       └─ Salário = 0
         │          │            │            └─ Salário = valor
         │          │            └─ Caixa anterior > mínimo?
         │          └─ Saldo_Caixa[t-1]
         └─ Mês atual >= mês de início?

Arrastar para N2:N37
```

### Q3: "Como dividir infraestrutura crescente?"

**Resposta: Lógica de IF Aninhado**

```
Coluna L (Custo_Infra):

Célula L2:
=SE(G2<=$Config.$C$14;  
    $Config.$C$13;      
    SE(G2<=$Config.$C$16;
        $Config.$C$15;
        $Config.$C$15 + ((G2-$Config.$C$16)*$Config.$C$17)
    )
)

Onde:
├─ G2 = Usuarios_Finais[t]
├─ C13 = tier1_custo (209)
├─ C14 = tier1_limite (100)
├─ C15 = tier2_custo (5559)
├─ C16 = tier2_limite (500)
└─ C17 = tier3_custo_usuario (1.50)
```

---

## PRÓXIMOS PASSOS

Agora que você tem a **lógica completa**, preciso saber:

1. **Implementação desejada:**
   - [ ] Python (Notebook Jupyter + Pandas)
   - [ ] Planilha Google Sheets (com Apps Script)
   - [ ] Mini-app Web (Streamlit/Dash)

2. **Faltou algo?** Alguma lógica que não ficou clara?

3. **Pronto para o código?** Posso gerar o script Python completo + estrutura de dados?