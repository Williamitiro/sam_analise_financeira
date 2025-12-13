# RELATÓRIO DE AUDITORIA E DADOS BRUTOS
**Data:** 2025-12-12 09:59:46
**Premissas Chave:**
- Churn Inicial: 0.12
- CAC Médio: N/A
- Budget Mkt: 0.0
- Taxa Trial->Pago: 0.12

---

## PÁGINA 1: COCKPIT (Resumo)
| Métrica | Valor Final (M36) | Média Anual |
|---|---|---|
| Caixa Final | R$ -1,247,547.93 | - |
| Receita Total (3 Anos) | R$ 430,057.20 | - |
| Lucro Líquido Acum. | R$ -1,266,047.93 | - |
| Runway (meses) | N/A | - |

## PÁGINA 2: GROWTH MACHINE
- **Usuários Ativos (Final):** 18
- **CAC Blended (Médio):** R$ 41.35
- **LTV (Final):** R$ 7,961.21
- **LTV/CAC (Final):** 192.51x

## PÁGINA 3: FINANCEIRO (DRE)
### DRE Anual (Resumo)
|    |   receita_bruta |   custo_total |   margem_bruta |   opex_total |   ebitda |   lucro_liquido |
|---:|----------------:|--------------:|---------------:|-------------:|---------:|----------------:|
|  0 |          118688 |       40003   |        78684.8 |       440879 |  -379858 |         -379859 |
|  1 |          132987 |       44455.5 |        88531.4 |       520320 |  -451580 |         -452081 |
|  2 |          178382 |       59624   |       118758   |       520320 |  -428109 |         -434109 |

## PÁGINA 4: UNIT ECONOMICS
- ARPU: R$ 1,033.23
- Churn Rate: 6.75%

## PÁGINA 5: RISCO E SENSIBILIDADE

### TORNADO PLOT (Top 5 Sensibilidade)
| nome_display        |   valor_base |   impacto_relativo |   ltv_cac_min |   ltv_cac_max |
|:--------------------|-------------:|-------------------:|--------------:|--------------:|
| Churn Base (%)      |         0.12 |           0.404732 |       9.24247 |       6.21441 |
| Conv. Trial -> Pago |         0.12 |           0.304857 |       5.72417 |       8.005   |
| cpc_youtube         |         3.5  |           0.211378 |       8.005   |       6.42355 |
| CPC Instagram       |         0.6  |           0.141427 |       7.48165 |       6.42355 |
| cpc_facebook        |         0.8  |           0.141427 |       7.48165 |       6.42355 |

### MONTE CARLO (Estatísticas)
Dados de Monte Carlo indisponíveis.


---

# ============================================================================
# MODIFICAÇÕES PARA TESTE DE INTEGRIDADE (CENÁRIO C)
# ============================================================================

PREMISSAS['meta_version'] = 'Cenario-C-HighTicket-StressTest'

# 1. TESTE DE CALENDÁRIO
PREMISSAS['data_inicio'] = '2026-06-01' 

# 2. TESTE DE RECEITA (Preços Premium)
PREMISSAS['preco_lite'] = 500.00
PREMISSAS['preco_trader'] = 1500.00
PREMISSAS['preco_pro'] = 5000.00

# 3. TESTE DE CUSTO VARIÁVEL (Margem Esmagada)
PREMISSAS['custo_ia_lite'] = 200.00
PREMISSAS['custo_ia_trader'] = 600.00
PREMISSAS['custo_ia_pro'] = 2000.00

# 4. TESTE DE GATILHO AUTOMÁTICO DE RH
PREMISSAS['trigger_dev'] = 15  # Contrata Dev Senior ao atingir 15 usuários
PREMISSAS['salario_dev_senior'] = 30000.00 # Salário fácil de ver no gráfico

# 5. TRAVANDO O GROWTH (Para isolar o efeito do preço)
PREMISSAS['trafego_inicial'] = 100
PREMISSAS['crescimento_trafego_mes_1_6'] = 0.05 # Crescimento lento
PREMISSAS['marketing_fixo_mensal'] = 0.0 # Sem ads, orgânico puro