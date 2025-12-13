# 🔬 RELATÓRIO DE AUDITORIA FORENSE V7.0

**Gerado:** 13/12/2025 16:03:07
**Premissas:** V9.0-full-documented
**Motor:** V13 | **Colunas:** 107
**Monte Carlo:** 150 simulações

> ⚠️ DOCUMENTO CONFIDENCIAL

---

# 1. 📋 TODAS AS PREMISSAS

| Categoria | Parâmetro | Valor |
|---|---|---|
| Growth | `usuarios_pagos_iniciais` | 5 |
| Growth | `trafego_inicial` | 250 |
| Growth | `crescimento_trafego_mes_1_6` | 25.00% |
| Growth | `taxa_visitante_para_trial` | 5.00% |
| Growth | `taxa_trial_para_pagante` | 12.00% |
| Churn | `churn_inicial` | 12.00% |
| Churn | `churn_maturidade` | 6.00% |
| Churn | `churn_base` | 7.00% |
| Churn | `churn_decaimento_mensal` | 0.20% |
| Pricing | `preco_lite` | R$ 69,90 |
| Pricing | `preco_trader` | R$ 99,90 |
| Pricing | `preco_pro` | R$ 169,90 |
| Pricing | `mix_lite` | 50.00% |
| Pricing | `mix_trader` | 35.00% |
| Pricing | `mix_pro` | 15.00% |
| COGS | `custo_ia_lite` | R$ 3,00 |
| COGS | `custo_ia_trader` | R$ 5,00 |
| COGS | `custo_ia_pro` | R$ 13,00 |
| Marketing | `marketing_fixo_mensal` | R$ 1,00 |
| Marketing | `marketing_perc_receita` | R$ 0,40 |
| Marketing | `marketing_teto` | R$ 25.000,00 |
| RH | `salario_fundador` | R$ 5.000,00 |
| RH | `trigger_fundador` | R$ 50.000,00 |
| RH | `salario_dev_senior` | R$ 10.000,00 |
| RH | `trigger_dev` | R$ 750,00 |
| RH | `salario_cs` | R$ 4.500,00 |
| RH | `trigger_cs` | R$ 1.000,00 |
| RH | `encargos_trabalhistas` | R$ 0,70 |
| Capital | `caixa_inicial` | R$ 3.500,00 |
| Capital | `aporte_mensal` | 2000.0 |
| Capital | `meses_aporte` | 10 |
| Capital | `caixa_reserva_operacional` | R$ 500,00 |
| Infra T1 | `t1_vps_app_api` | R$ 120,00 |
| Infra T1 | `t1_vps_windows_mt5` | R$ 180,00 |
| Infra T1 | `t1_database_managed` | R$ 80,00 |
| Infra T1 | `t1_storage_s3` | R$ 20,00 |
| Infra T1 | `t1_ferramentas_dev` | R$ 300,00 |
| Infra T1 | `t1_scraping_news` | R$ 100,00 |
| Infra T1 | `t1_email_transacional` | R$ 50,00 |

---

# 2. 🧾 EXTRATO DETALHADO MÊS 1 (AUDITORIA FORENSE)

> Estilo `auditoria_forense.py` - Cada centavo rastreado

## 2.1 Entradas Mês 1
| Descrição | Valor |
|---|---|
| (+) Caixa Inicial | R$ 3.500,00 |
| (+) Aportes/Investimento | R$ 2.000,00 |
| (+) Receita Bruta | R$ 509,50 |
| (+) Receita Líquida | R$ 433,67 |

## 2.2 Saídas Mês 1
| Descrição | Valor |
|---|---|
| (-) Marketing | R$ 1,00 |
| (-) Infraestrutura | R$ 860,00 |
| (-) Pessoal/RH | R$ 0.00 |
| (-) COGS Total | R$ 29,00 |
| (-) OPEX Total | R$ 861,00 |
| (-) Impostos | R$ 30,57 |
| (-) Taxas Pagamento | R$ 14,69 |
| (-) CAPEX | R$ -1,00 |

## 2.3 Resultado Mês 1
| Métrica | Valor |
|---|---|
| Caixa Final | **R$ 5.042,67** |
| Burn Rate | R$ 457,33 |
| Runway | 7.9 meses |
| Lucro/Prejuízo | R$ -456,37 |

---

# 3. 📊 TABELA COMPLETA DO MOTOR (TODAS AS COLUNAS)

> **Total de colunas disponíveis: 107**

## 3.1 Tráfego & Aquisição

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `trafego_total` | 257 | 593 | 1,033 | 1,758 | 2,896 | 5,081 | 8,926 |
| `trafego_pago` | 0 | 148 | 458 | 971 | 1,889 | 3,655 | 7,000 |
| `trafego_organico` | 257 | 445 | 575 | 786 | 1,007 | 1,425 | 1,925 |
| `trials_total` | 12 | 30 | 55 | 95 | 159 | 283 | 502 |
| `novos_pagantes_total` | 0 | 2 | 6 | 10 | 19 | 33 | 59 |
| `novos_ads` | 0 | 0 | 3 | 6 | 13 | 25 | 48 |
| `novos_organicos` | 0 | 2 | 3 | 4 | 6 | 8 | 11 |

## 3.2 Usuários

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `usuarios_ativos` | 5 | 10 | 28 | 57 | 113 | 216 | 410 |
| `usuarios_lite` | 2 | 5 | 14 | 28 | 55 | 107 | 202 |
| `usuarios_trader` | 2 | 4 | 10 | 20 | 41 | 77 | 147 |
| `usuarios_pro` | 1 | 1 | 4 | 9 | 17 | 32 | 61 |
| `churn_usuarios` | 0 | 0 | 2 | 4 | 7 | 11 | 22 |
| `reativacoes` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 1,00 | R$ 1,00 | R$ 3,00 |

## 3.3 Receita

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `receita_bruta` | R$ 509,50 | R$ 919,00 | R$ 2.657,20 | R$ 5.484,30 | R$ 10.828,70 | R$ 20.608,40 | R$ 39.169,00 |
| `receita_assinaturas` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `receita_lite` | R$ 139,80 | R$ 349,50 | R$ 978,60 | R$ 1.957,20 | R$ 3.844,50 | R$ 7.479,30 | R$ 14.119,80 |
| `receita_trader` | R$ 199,80 | R$ 399,60 | R$ 999,00 | R$ 1.998,00 | R$ 4.095,90 | R$ 7.692,30 | R$ 14.685,30 |
| `receita_pro` | R$ 169,90 | R$ 169,90 | R$ 679,60 | R$ 1.529,10 | R$ 2.888,30 | R$ 5.436,80 | R$ 10.363,90 |
| `mrr` | R$ 509,50 | R$ 919,00 | R$ 2.657,20 | R$ 5.484,30 | R$ 10.828,70 | R$ 20.608,40 | R$ 39.169,00 |
| `arr` | R$ 6.114,00 | R$ 11.028,00 | R$ 31.886,40 | R$ 65.811,60 | R$ 129.944,40 | R$ 247.300,80 | R$ 470.028,00 |
| `arpu` | R$ 101,90 | R$ 91,90 | R$ 94,90 | R$ 96,22 | R$ 95,83 | R$ 95,41 | R$ 95,53 |

## 3.4 Custos

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `total_cogs` | R$ 29,00 | R$ 48,00 | R$ 144,00 | R$ 301,00 | R$ 591,00 | R$ 1.122,00 | R$ 2.134,00 |
| `custo_ia_total` | R$ 29,00 | R$ 48,00 | R$ 144,00 | R$ 301,00 | R$ 591,00 | R$ 1.122,00 | R$ 2.134,00 |
| `total_opex` | R$ 861,00 | R$ 1.159,68 | R$ 1.787,04 | R$ 2.821,96 | R$ 4.676,00 | R$ 8.244,28 | R$ 15.001,20 |
| `gasto_marketing` | R$ 1,00 | R$ 299,68 | R$ 927,04 | R$ 1.961,96 | R$ 3.816,00 | R$ 7.384,28 | R$ 14.141,20 |
| `custo_infra_fixo` | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 |
| `custo_pessoal` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |

## 3.5 Margens

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `margem_bruta` | R$ 404,67 | R$ 734,23 | R$ 2.117,75 | R$ 4.367,11 | R$ 8.626,15 | R$ 16.419,41 | R$ 31.205,77 |
| `margem_bruta_pct` | 79.43% | 79.89% | 79.70% | 79.63% | 79.66% | 79.67% | 79.67% |
| `ebitda` | R$ -456,33 | R$ -425,45 | R$ 330,71 | R$ 1.545,15 | R$ 3.950,15 | R$ 8.175,13 | R$ 16.204,57 |
| `ebitda_margin` | -89.56% | -46.29% | 12.45% | 28.17% | 36.48% | 39.67% | 41.37% |
| `lucro_liquido` | R$ -456,37 | R$ -425,49 | R$ 330,67 | R$ 1.545,11 | R$ 3.450,10 | R$ 7.675,13 | R$ 15.704,57 |
| `margem_liquida` | R$ -89,57 | R$ -46,30 | R$ 12,44 | R$ 28,17 | R$ 31,86 | R$ 37,24 | R$ 40,09 |

## 3.6 Caixa

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `caixa` | R$ 5.042,67 | R$ 12.259,37 | R$ 20.169,97 | R$ 26.055,01 | R$ 30.682,24 | R$ 67.522,96 | R$ 142.679,54 |
| `burn_rate` | 45732.51% | 42544.79% | 0.00% | 0.00% | 804985.42% | 0.00% | 0.00% |
| `runway_meses` | 7.9 | 10.2 | 10.4 | 8.3 | 1.8 | 7.2 | 8.3 |
| `aportes_capital` | R$ 2.000,00 | R$ 2.000,00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |

## 3.7 Unit Economics

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `ltv` | R$ 674,46 | R$ 667,48 | R$ 771,77 | R$ 890,88 | R$ 1.031,59 | R$ 1.226,06 | R$ 1.268,53 |
| `cac_blended` | R$ 0.00 | R$ 149,84 | R$ 154,51 | R$ 196,20 | R$ 200,84 | R$ 223,77 | R$ 239,68 |
| `cac_paid` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `ltv_cac` | ∞ | 4.45x | 5.00x | 4.54x | 5.14x | 5.48x | 5.29x |
| `payback_meses` | 0.0 | 2.0 | 2.0 | 2.6 | 2.6 | 2.9 | 3.1 |

## 3.8 Churn

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `churn_rate` | 12.00% | 11.00% | 9.80% | 8.60% | 7.40% | 6.20% | 6.00% |
| `retention_rate` | 88.00% | 89.00% | 90.20% | 91.40% | 92.60% | 93.80% | 94.00% |

---

# 4. ⚖️ COMPARATIVO: REAL vs IDEAL vs ESTRESSE

## 4.1 Snapshot M36

| Métrica | Real | Ideal | Estresse | Gap Real/Ideal |
|---|---|---|---|---|
| MRR | R$ 39.169,00 | R$ 116.718,00 | R$ 1.668,30 | 66.4% |
| ARR | R$ 470.028,00 | R$ 1.400.616,00 | R$ 20.019,60 | 66.4% |
| Usuários | 410 | 1,220 | 17 | 66.4% |
| Caixa | R$ 142.679,54 | R$ 319.098,87 | R$ -2.223,16 | 55.3% |
| Receita | R$ 39.169,00 | R$ 116.718,00 | R$ 1.668,30 | 66.4% |
| Lucro | R$ 15.704,57 | R$ 25.939,52 | R$ -32,98 | 39.5% |
| LTV/CAC | 5.29x | 5.59x | 10000.00x | 5.3% |
| Churn | 6.00% | 6.00% | 17.00% | 0.0% |
| Runway | 8.3m | 4.4m | 0.0m | -90.2% |

---

# 5. 🎲 MONTE CARLO COMPLETO

## 5.1 Configuração

- **Simulações:** 50
- **Cenários:** ['pessimista', 'base', 'otimista']
- **Variáveis:** ['marketing_fixo_mensal', 'taxa_trial_para_pagante', 'taxa_visitante_para_trial', 'churn_inicial', 'cpc_instagram', 'cpc_facebook', 'cpc_google', 'cpc_youtube', 'mix_lite', 'custo_ia_lite', 'custo_ia_trader', 'custo_ia_pro', 'imposto_simples_inicial', 'b2b_probabilidade_anual', 'crescimento_trafego_mes_1_6']

## 5.2 Estatísticas Percentis

> **Colunas MC disponíveis:** ['sim', 'scenario', 'seed', 'success', 'time_elapsed', 'caixa_final', 'mrr_final', 'arr_final', 'usuarios_final', 'cac_medio', 'ltv_medio', 'churn_medio', 'margem_bruta_media', 'ebitda_margin_media', 'nrr', 'burn_rate_medio', 'runway_final', 'quebrou', 'runway_critico', 'var95_caixa', 'cvar95_caixa', 'roi_total_pct', 'payback_meses_medio', 'ltv_cac', 'caixa_series', 'mrr_series']

| Métrica | P5 | P50 | P95 | Média |
|---|---|---|---|---|
| sim | R$ 2,00 | R$ 24,50 | R$ 47,00 | R$ 24,50 |
| seed | R$ 131.951.950,85 | R$ 1.093.315.554,50 | R$ 1.363.213.179,15 | R$ 862.826.894,83 |
| time_elapsed | R$ 0,07 | R$ 0,08 | R$ 0,10 | R$ 0,09 |
| caixa_final | R$ 8.607,94 | R$ 77.377,77 | R$ 1.121.471,47 | R$ 218.330,98 |
| mrr_final | R$ 1.699,76 | R$ 6.982,70 | R$ 232.385,19 | R$ 48.147,71 |
| arr_final | R$ 20.397,06 | R$ 83.792,40 | R$ 2.788.622,28 | R$ 577.772,46 |
| usuarios_final | 17 | 73 | 2,458 | 503 |
| cac_medio | R$ 0.00 | R$ 0.00 | R$ 249,56 | R$ 72,05 |
| ltv_medio | R$ 519,21 | R$ 968,31 | R$ 1.274,34 | R$ 942,27 |
| churn_medio | R$ 0,06 | R$ 0,08 | R$ 0,15 | R$ 0,09 |
| margem_bruta_media | R$ 75,79 | R$ 78,81 | R$ 80,88 | R$ 78,60 |
| ebitda_margin_media | R$ -40,70 | R$ 14,16 | R$ 44,39 | R$ 9,10 |
| nrr | R$ 1,00 | R$ 1,00 | R$ 1,03 | R$ 1,01 |
| burn_rate_medio | R$ 53,96 | R$ 353,28 | R$ 634,08 | R$ 346,54 |
| runway_final | R$ 2,92 | R$ 20,73 | R$ 83,09 | R$ 31,61 |
| var95_caixa | R$ -1.943,49 | R$ 7.666,87 | R$ 15.384,97 | R$ 6.707,77 |
| cvar95_caixa | R$ -2.622,79 | R$ 5.804,15 | R$ 9.753,55 | R$ 4.866,30 |
| roi_total_pct | -35.96% | 350.79% | 4695.62% | 1121.78% |
| payback_meses_medio | R$ 1,47 | R$ 2,54 | R$ 4,07 | R$ 2,70 |
| ltv_cac | 3.99x | 10000.00x | 10000.00x | 6247.50x |

## 5.3 Probabilidades de Risco

| Indicador | Valor |
|---|---|
| Prob. Caixa < 0 | ✅ **2.0%** |
| Prob. Quebra | ✅ **4.7%** |

---

# 6. ⚠️ ALERTAS DO MOTOR

- ℹ️ {'tipo': 'runway_critico', 'mes': 2, 'runway': np.float64(5.841462182009517)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 24, 'runway': np.float64(1.776929519372213)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 25, 'runway': np.float64(5.999806751967696)}

---

# 7. 📋 LISTA COMPLETA DE COLUNAS DO DataFrame

> Total: 107 colunas

```
  1. mes
  2. trafego_total
  3. trafego_pago
  4. trafego_organico
  5. trials_total
  6. trials_pagos
  7. trials_organicos
  8. novos_pagantes_total
  9. novos_ads
 10. novos_organicos
 11. novos_afiliados
 12. reativacoes
 13. taxa_trafego_trial
 14. taxa_trial_pago
 15. eficiencia_time
 16. usuarios_ativos
 17. usuarios_lite
 18. usuarios_trader
 19. usuarios_pro
 20. churn_usuarios
 21. churn_mrr
 22. upgrades_lite_trader
 23. expansion_mrr
 24. mrr_cohort_m0
 25. cogs_recorrente
 26. churn_mrr_cohort_m0
 27. receita_bruta
 28. receita_assinaturas
 29. receita_b2b
 30. receita_lite
 31. receita_trader
 32. receita_pro
 33. mrr
 34. arr
 35. arpu
 36. crescimento_mrr_mom
 37. crescimento_mrr_yoy
 38. net_new_mrr
 39. impostos
 40. aliquota_efetiva
 41. taxas_pagamento
 42. inadimplencia
 43. chargeback
 44. total_deducoes
 45. receita_liquida
 46. custo_ia_lite
 47. custo_ia_trader
 48. custo_ia_pro
 49. custo_ia_total
 50. comissao_afiliados
 51. custo_suporte_variavel
 52. total_cogs
 53. margem_bruta
 54. margem_bruta_pct
 55. custo_infra_fixo
 56. infra_tier_ativo
 57. headcount_total
 58. headcount_fundadores
 59. headcount_dev
 60. headcount_cs
 61. custo_pessoal
 62. salarios_brutos
 63. encargos
 64. gasto_marketing
 65. gasto_instagram
 66. gasto_facebook
 67. gasto_youtube
 68. gasto_google
 69. cpc_blended
 70. custo_escritorio
 71. custo_contabilidade
 72. despesas_viagens
 73. despesas_conselho
 74. despesas_freelancer
 75. despesas_beneficios
 76. total_opex
 77. margem_contribuicao
 78. margem_contribuicao_pct
 79. ebitda
 80. ebitda_margin
 81. depreciacao
 82. ebit
 83. ebit_margin
 84. lucro_liquido
 85. margem_liquida
 86. fluxo_operacional
 87. fluxo_investimento
 88. fluxo_financiamento
 89. aportes_capital
 90. capex
 91. distribuicao_lucros
 92. caixa
 93. burn_rate
 94. runway_meses
 95. ltv
 96. cac_blended
 97. cac_paid
 98. ltv_cac
 99. payback_meses
100. payback_semanas
101. vida_media_cliente
102. churn_rate
103. retention_rate
104. regra_40
105. burn_multiple
106. trafego_potencial_perdido
107. saturacao_mercado
```

---

# 📋 METADADOS

| Campo | Valor |
|---|---|
| Timestamp | 13/12/2025 16:03:07 |
| Colunas Motor | 107 |
| Métricas MC | 82 |
| Alertas | 3 |

---
*Fim do Relatório*