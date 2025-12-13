# 🛡️ RELATÓRIO DE AUDITORIA ANALÍTICA COMPLETA
**Data:** 13/12/2025 05:38 | **Motor:** V13 Production | **Snapshot:** Full Coverage

---
## 1. CALIBRAGEM DO MODELO (PREMISSAS)
| Categoria | Variável | Valor Configurado |
|---|---|---|
| Growth | `usuarios_pagos_iniciais` | 5 |
| Growth | `trafego_inicial` | 100 |
| Growth | `crescimento_trafego_mes_1_6` | 0.05 |
| Growth | `churn_inicial` | 0.12 |
| Growth | `churn_base` | 0.07 |
| Pricing | `preco_lite` | 500 |
| Pricing | `preco_trader` | 1500 |
| Pricing | `preco_pro` | 5000 |
| Custos | `custo_ia_lite` | 200 |
| Custos | `custo_ia_trader` | 600 |
| Custos | `custo_ia_pro` | 2000 |
| Marketing | `marketing_fixo_mensal` | 0.0 |
| Marketing | `marketing_perc_receita` | 0.0 |
| RH | `salario_fundador` | 5000.0 |
| RH | `trigger_fundador` | 25000.0 |
| RH | `salario_dev_senior` | 30000.0 |
| RH | `trigger_dev` | 15 |
| RH | `salario_cs` | 4500.0 |
| RH | `trigger_cs` | 1000 |
| RH | `encargos_trabalhistas` | 0.7 |
| Capital | `caixa_inicial` | 4000.0 |
| Capital | `aporte_mensal` | 2000.0 |
| Capital | `meses_aporte` | 10 |

## 📑 COCKPIT EXECUTIVO (1 Blocos)

### VIZ 1.1: Tabela Executiva Master
> *Visão Geral do Negócio*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Visão consolidada dos KPIs.
- **Causa:** Performance agregada.
- **Implicação:** Diagnóstico rápido da saúde do negócio.
- **Ação:** Verificar métricas em vermelho (Críticas).

**📊 DADOS TABULADOS:**
| Métrica                          | M1        | M6         | M12        | M36       | Benchmark   | Status   |
|:---------------------------------|:----------|:-----------|:-----------|:----------|:------------|:---------|
| **💰 RECEITA**                   |           |            |            |           |             |          |
| MRR                              | R$ 9.0k   | R$ 30.0k   | R$ 28.0k   | R$ 30.5k  | R$ 42.0k    | 🔴       |
| ARR (Anual)                      | R$ 108.0k | R$ 360.0k  | R$ 336.0k  | R$ 366.0k | R$ 504.0k   | 🔴       |
| Usuários Ativos                  | 5         | 19         | 17         | 20        | 28          | 🔴       |
| ****                             |           |            |            |           |             |          |
| **📊 UNIT ECONOMICS**            |           |            |            |           |             |          |
| LTV/CAC (Índice de Retorno)      | nanx      | nanx       | nanx       | nanx      | 3.0x        | 🔴       |
| CAC (Custo Aquisição Cliente)    | R$ nan    | R$ nan     | R$ 0       | R$ 0      | R$ 250      | ✅       |
| Churn (Taxa Cancelamento %)      | 12.0%     | 11.2%      | 10.3%      | 6.8%      | 5.0%        | 🔴       |
| Payback (Meses p/ Recuperar CAC) | nanm      | nanm       | nanm       | -22.7m    | >12m        | 🔴       |
| ****                             |           |            |            |           |             |          |
| **💵 CAIXA & RUNWAY**            |           |            |            |           |             |          |
| Caixa Disponível                 | R$ 9.2k   | R$ -165.5k | R$ -443.9k | R$ -1.7M  | R$ 50.0k    | 🔴       |
| Runway (Meses de Sobrevivência)  | 2.5m      | 0.0m       | 0.0m       | -22.7m    | >12m        | 🔴       |
| Burn Rate (Queima Mensal)        | R$ 0      | R$ 46.8k   | R$ 47.7k   | R$ 46.6k  | R$ 0        | 🔴       |
| ****                             |           |            |            |           |             |          |
| **📈 MARGENS**                   |           |            |            |           |             |          |
| Margem Bruta %                   | 45.1%     | 45.1%      | 45.1%      | 45.1%     | 70.0%       | 🔴       |
| EBITDA (Lucro Operacional)       | R$ 3.2k   | R$ -46.8k  | R$ -47.7k  | R$ -46.6k | R$ 0        | 🔴       |

---

## 📑 GROWTH MACHINE (5 Blocos)

### VIZ 2.1: Funil de Aquisição (Conservador vs Benchmark)
> *O volume de vendas sustenta a operação no cenário conservador?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** No M36, a conversão global de 0.55% supera a meta.
- **Causa:** Otimização contínua do funil e qualificação do tráfego pago.
- **Implicação:** Maior eficiência de capital: CAC menor que o planejado.
- **Ação:** Acelerar investimento em Topo de Funil para escalar.

**📊 DADOS TABULADOS:**
| Período   |   Visitantes (Real) | Conv. Global Real   | Conv. Meta (Ideal)   | Δ (Delta)   | Status                                     |
|:----------|--------------------:|:--------------------|:---------------------|:------------|:-------------------------------------------|
| M1        |                 107 | 0.00%               | 0.31%                | -0.31 p.p.  | <span class='status-yellow'>PRÓXIMO</span> |
| M6        |                 165 | 0.00%               | 0.00%                | +0.00 p.p.  | <span class='status-green'>SUPEROU</span>  |
| M12       |                 185 | 0.54%               | 0.52%                | +0.02 p.p.  | <span class='status-green'>SUPEROU</span>  |
| M36       |                 360 | 0.55%               | 0.54%                | +0.01 p.p.  | <span class='status-green'>SUPEROU</span>  |

<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


    1. **Taxa de Conversão Global** = (Novos Pagantes / Visitantes Únicos) * 100
    2. **Benchmark (Ideal)**: Definido nas premissas (ex: 1.0% para SaaS B2C).
    3. **Delta**: Diferença percentual (p.p.) entre a conversão Real e a Meta.
    4. **Fonte dos Dados**:
       - *df_real_m*: Colunas 'trafego_total', 'novos_pagantes_total'
       - *df_ideal*: Colunas equivalentes do cenário meta.
    

</details>

---

### VIZ 2.2: Evolução LTV/CAC vs Zonas de Risco
> *O negócio para em pé? (Saúde Unitária)*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** LTV/CAC final de 0.0x está abaixo do benchmark de 3.0x.
- **Causa:** Provável CAC alto demais ou Churn impactando o LTV.
- **Implicação:** Queima de caixa ineficiente; risco de solvência na escala.
- **Ação:** Suspender aumento de mídia e focar em reduzir CAC.

**📊 DADOS TABULADOS:**
| Período   | LTV/CAC Real   | Target Mínimo   | Distância   | Saúde Financeira                        |
|:----------|:---------------|:----------------|:------------|:----------------------------------------|
| M6        | nanx           | 3.0x            | +nanx       | <span class='status-red'>CRÍTICO</span> |
| M12       | nanx           | 3.0x            | +nanx       | <span class='status-red'>CRÍTICO</span> |
| M24       | nanx           | 3.0x            | +nanx       | <span class='status-red'>CRÍTICO</span> |
| M36       | nanx           | 3.0x            | +nanx       | <span class='status-red'>CRÍTICO</span> |

<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


    1. **LTV (Lifetime Value)** = (ARPU × Margem Bruta %) / Churn Rate
    2. **CAC (Custo Aquisição)** = Gastos Marketing / Novos Clientes
    3. **LTV/CAC**: Razão de eficiência. Quanto retorna para cada R$ 1 investido.
    4. **Zonas de Risco**:
       - 🟢 > 3.0x: Alta eficiência (Escalável)
       - 🟡 1.0x - 3.0x: Operação paga contas mas cresce devagar
       - 🔴 < 1.0x: Destruição de valor (Prejuízo unitário)
    

</details>

---

### VIZ 2.3: Volatilidade Semanal do CAC (SPC)
> *Existe descontrole tático de custos?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Identificados 4 semanas com volatilidade estatística anormal.
- **Causa:** Provável teste de canal novo ou sazonalidade agressiva.
- **Implicação:** Risco de estourar budget mensal se a correção não for imediata.
- **Ação:** Investigar 'root cause' das semanas vermelhas na tabela.

**📊 DADOS TABULADOS:**
| Semana   | CAC Real   | Média (Centro)   | UCL (Limite)   | Status                                          |
|:---------|:-----------|:-----------------|:---------------|:------------------------------------------------|
| S6       | R$ 576.13  | R$ 89.49         | R$ 490.44      | <span class='status-red'>ANOMALIA (ALTA)</span> |
| S7       | R$ 550.02  | R$ 89.49         | R$ 490.44      | <span class='status-red'>ANOMALIA (ALTA)</span> |
| S8       | R$ 523.92  | R$ 89.49         | R$ 490.44      | <span class='status-red'>ANOMALIA (ALTA)</span> |
| S9       | R$ 497.81  | R$ 89.49         | R$ 490.44      | <span class='status-red'>ANOMALIA (ALTA)</span> |
| S24      | R$ nan     | R$ 89.49         | R$ 490.44      | <span class='status-green'>CONTROLADO</span>    |

<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


    1. **CAC Semanal** = Custo Marketing da Semana / Novos Clientes da Semana
    2. **Média (Central)** = Média aritmética de todas as semanas observadas.
    3. **Limites de Controle (SPC)**:
       - *UCL (Alto)* = Média + (2 × Desvio Padrão)
       - *LCL (Baixo)* = Média - (2 × Desvio Padrão)
    4. **Interpretação**: Pontos fora dos limites são estatisticamente anômalos (causas especiais).
    

</details>

---

### VIZ 2.5: Impacto do Mix de Canais (CAC Pago vs Blended)
> *Quanto economizamos com trafego organico?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Tráfego orgânico reduz o CAC em R$ 0,00 por cliente.
- **Causa:** Mix balanceado entre canais pagos e gratuitos.
- **Implicação:** Menor sensibilidade a aumentos de CPM nas plataformas de ads.
- **Ação:** Manter investimento em SEO para ampliar o gap.

**📊 DADOS TABULADOS:**
| Período | CAC Pago | CAC Blended | Economia/Cliente | Total Economizado |
|:---|---:|---:|---:|---:|
| M6 | N/A | N/A | N/A | N/A |
| M12 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 |
| M24 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 |
| M36 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 |


<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


    1. **CAC Pago** = Gasto Ads / Novos Clientes (Só de Ads)
    2. **CAC Blended** = Gasto Ads / Novos Clientes (Totais)
    3. **Economia** = CAC Pago - CAC Blended
    

</details>

---

### VIZ 2.5: Análise de Vazamento (Net Growth & Churn)
> *Quanto dinheiro estamos perdendo pelo ralo?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** O churn acima do benchmark custou R$ 3,639 no último ano.
- **Causa:** Taxa de churn superior ao benchmark de 5%.
- **Implicação:** Redução direta do Valuation e necessidade de repor receita mais rápido.
- **Ação:** Implementar squad de retenção para estancar o sangramento.

**📊 DADOS TABULADOS:**
| Período   | Churn Rate   | Perda Real   | Limite Aceitável   | Dinheiro Rasgado   | Status    |
|:----------|:-------------|:-------------|:-------------------|:-------------------|:----------|
| M6        | 11.2%        | R$ 2.952,38  | R$ 1.550,00        | -R$ 1.402,38       | VAZAMENTO |
| M12       | 10.3%        | R$ 1.647,06  | R$ 1.400,00        | -R$ 247,06         | VAZAMENTO |
| M24       | 8.5%         | R$ 1.433,33  | R$ 1.075,00        | -R$ 358,33         | VAZAMENTO |
| M36       | 6.8%         | R$ 1.578,95  | R$ 1.500,00        | -R$ 78,95          | VAZAMENTO |

<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


    1. **Churn Rate Real** = Clientes Cancelados / Clientes Ativos Iniciais
    2. **Perda Real (Churn MRR)** = Valor somado dos contratos cancelados no mês.
    3. **Perda Aceitável (Benchmark)** = MRR Inicial × 5.0% (Meta de Mercado).
    4. **Dinheiro Rasgado (Waste)** = Perda Real - Perda Aceitável.
       - Se negativo, significa que estamos perdendo mais dinheiro do que o "normal" para o setor.
    

</details>

---

## 📑 FINANCEIRO & DRE (1 Blocos)

### VIZ 3.0: Decomposição da DRE (M36)
> *De onde vem e para onde vai o dinheiro?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Estrutura de custos analisada.
- **Causa:** Breakdown de M36.
- **Implicação:** Entendimento da eficiência.
- **Ação:** Otimizar linha a linha.

**📊 DADOS TABULADOS:**
| Categoria            | Valor        | % Receita   | Status   |
|:---------------------|:-------------|:------------|:---------|
| 📈 Receita Bruta     | R$ 30,500    | 100%        | —        |
| (-) Impostos & Taxas | R$ 4,539     | 14.9%       | —        |
| = Receita Líquida    | R$ 25,961    | 85.1%       | —        |
| (-) COGS Total       | R$ 12,200    | 40.0%       | 🟡       |
| = Margem Bruta       | R$ 13,761    | 45.1%       | 🟡       |
| (-) OPEX Total       | R$ 60,360    | 197.9%      | 🟡       |
| = EBITDA             | R$ -46599.09 | -152.8%     | 🔴       |

---

## 📑 UNIT ECONOMICS (4 Blocos)

### VIZ 4.1: LTV vs CAC (A 'Regua de Ouro')
> *LTV vs CAC: A CRIAÇÃO DE VALOR*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Múltiplo LTV/CAC atinge 0.0x no M36.
- **Causa:** Resultado combinado de expansão do LTV e CAC estável.
- **Implicação:** Cada R$ 1 investido em marketing retorna R$ 0.00 de margem bruta.
- **Ação:** Focar em Retenção/Pricing antes de escalar.

**📊 DADOS TABULADOS:**
| Período | LTV (R$) | CAC (R$) | Múltiplo | Status |
|:---|---:|---:|---:|:---|
| M1 | R$ 6.767,66 | N/A | 0.0x | 🔴 CRÍTICO |
| M6 | R$ 6.332,32 | N/A | 0.0x | 🔴 CRÍTICO |
| M12 | R$ 7.179,86 | R$ 0,00 | 0.0x | 🔴 CRÍTICO |
| M24 | R$ 7.563,60 | R$ 0,00 | 0.0x | 🔴 CRÍTICO |
| M36 | R$ 10.193,27 | R$ 0,00 | 0.0x | 🔴 CRÍTICO |


<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


**Fonte:** df_real_m (Célula 5A)

**Fórmulas:**
1. **LTV (Lifetime Value)** = (ARPU × Margem Bruta %) / Churn Rate
2. **CAC (Blended)** = (Gasto Marketing + Gasto Vendas) / Novos Clientes Totais
3. **Múltiplo** = LTV / CAC

**Metodologia:**
- **Modelo de LTV:** Perpetuidade simples (1/Churn). Assume que a taxa de cancelamento e o ticket médio se mantêm constantes durante a vida do cliente.
- **Interpretação:** Valores acima de 3.0x indicam alta eficiência; abaixo de 1.0x indicam queima de caixa por cliente.


</details>

---

### VIZ 4.2: Cohort Analyis (Retencao por Safra)
> *Os clientes antigos continuam pagando ao longo do tempo?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Retenção média no mês 12 (M12) é de 31.2%.
- **Causa:** Taxa de churn mensal estabilizada em torno de 9.4%.
- **Implicação:** A base de clientes renova seu valor quase integralmente ano a ano.
- **Ação:** Focar em expansão (Upsell) nas cohorts antigas (M12+) para aumentar LTV.

**📊 DADOS TABULADOS:**
| Período de Vida | Retenção Média | Status |
|:---|---:|:---|
| Primeiro Mês (M1) | 90.3% | 🟢 OK |
| Semestre (M6) | 55.7% | 🟡 ATENÇÃO |
| Ano (M12) | 31.2% | 🔴 CRÍTICO |


<details><summary>🔍 Ver Fórmulas e Auditoria</summary>


**Fonte:** df_real['churn_rate'] (Célula 5A)

**Metodologia (Simulação Sintética):**
- Como o modelo é financeiro (não transacional individual), geramos uma **Matriz Sintética**.
- **Lógica:** Aplicamos o Churn Rate Global do mês sobre cada safra passada retroativamente.
- **Limitação:** Assume que todas as safras decaem na mesma taxa do mês vigente (Churn Homogêneo).


</details>

---

### VIZ 4.4: Qualidade Marginal na Escala (LTV/CAC vs Volume)
> *A qualidade do cliente cai quando a empresa cresce?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** A inclinação da curva é -350.3095.
- **Causa:** Comportamento dos custos marginais e retenção em escala.
- **Implicação:** Viabilidade de escalar agressivamente.
- **Ação:** Revisar funil antes de escalar.

**📊 DADOS TABULADOS:**
| Faixa de Clientes | LTV/CAC Médio | Status |
|:---|---:|:---|
| Média Geral | 5900.21x | 🟢 OK |


<details><summary>🔍 Ver Fórmulas e Auditoria</summary>

**Fonte:** df_real_m | 'usuarios_ativos' vs 'ltv/cac'

</details>

---

### VIZ 4.5: Unit Profitability Waterfall
> *Onde fica o dinheiro do cliente?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Sobram R$ 7.934,01 de lucro limpo por cliente.
- **Causa:** Estrutura de custos e eficiência de aquisição.
- **Implicação:** Potencial de reinvestimento.
- **Ação:** Otimizar.

**📊 DADOS TABULADOS:**
| Componente | Valor |
|:---|---:|
| LTV Bruto | R$ 22.592,59 |
| COGS | R$ -12.399,32 |
| Impostos | R$ -2.259,26 |
| CAC | R$ -0,00 |
| LUCRO LÍQUIDO | R$ 7.934,01 |


<details><summary>🔍 Ver Fórmulas e Auditoria</summary>

Profit = LTV Bruto - COGS - Impostos - CAC

</details>

---

## 📑 RISCO & CENÁRIOS (1 Blocos)

### VIZ 5.2: Análise de Sensibilidade (Tornado Plot)
> *O que pode matar o negócio?*

**🧠 INSIGHT AUTOMÁTICO:**
- **Fato:** Sensibilidade mapeada para top 10 variáveis.
- **Causa:** Variação de +/- 20% nas premissas base.
- **Implicação:** Identificação dos drivers críticos de risco.
- **Ação:** Monitorar de perto as variáveis do topo do gráfico.

**📊 DADOS TABULADOS:**
| premissa                    | nome_display                |   valor_base |   valor_min |   valor_max |   ltv_cac_base |   ltv_cac_min |   ltv_cac_max |   impacto_absoluto |   impacto_relativo |   ranking |
|:----------------------------|:----------------------------|-------------:|------------:|------------:|---------------:|--------------:|--------------:|-------------------:|-------------------:|----------:|
| churn_inicial               | Churn Base (%)              |         0.12 |       0.096 |       0.144 |        11009.1 |      11100.4  |       7396.35 |           3704.05  |          0.336452  |         1 |
| preco_trader                | Preço Trader                |      1500    |    1200     |    1800     |        11009.1 |       9673.94 |      12344.3  |           2670.36  |          0.242559  |         2 |
| custo_ia_pro                | custo_ia_pro                |      2000    |    1600     |    2400     |        11009.1 |      12054.9  |       9963.37 |           2091.5   |          0.189979  |         3 |
| custo_ia_trader             | Custo IA Trader             |       600    |     480     |     720     |        11009.1 |      11636.6  |      10381.7  |           1254.9   |          0.113987  |         4 |
| taxa_trial_para_pagante     | Conv. Trial -> Pago         |         0.12 |       0.096 |       0.144 |        11009.1 |       9580.56 |      10193.3  |            612.71  |          0.0556548 |         5 |
| taxa_visitante_para_trial   | taxa_visitante_para_trial   |         0.05 |       0.04  |       0.06  |        11009.1 |       9580.56 |      10193.3  |            612.71  |          0.0556548 |         6 |
| trafego_inicial             | Tráfego Inicial             |       100    |      80     |     120     |        11009.1 |       9580.56 |      10193.3  |            612.71  |          0.0556548 |         7 |
| imposto_simples_inicial     | Imposto Inicial             |         0.06 |       0.048 |       0.072 |        11009.1 |      11301.9  |      10716.3  |            585.621 |          0.0531941 |         8 |
| custo_ia_lite               | custo_ia_lite               |       200    |     160     |     240     |        11009.1 |      11288    |      10730.3  |            557.734 |          0.0506611 |         9 |
| crescimento_trafego_mes_1_6 | crescimento_trafego_mes_1_6 |         0.05 |       0.04  |       0.06  |        11009.1 |      11009.1  |      10583.2  |            425.948 |          0.0386905 |        10 |

---