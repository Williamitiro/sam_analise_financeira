# 🔬 RELATÓRIO DE AUDITORIA FORENSE V7.0

**Gerado:** 13/12/2025 18:36:28
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
| Growth | `crescimento_trafego_mes_1_6` | 20.00% |
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
| Marketing | `marketing_fixo_mensal` | R$ 1.750,00 |
| Marketing | `marketing_perc_receita` | R$ 0,40 |
| Marketing | `marketing_teto` | R$ 25.000,00 |
| RH | `salario_fundador` | R$ 5.000,00 |
| RH | `trigger_fundador` | R$ 50.000,00 |
| RH | `salario_dev_senior` | R$ 10.000,00 |
| RH | `trigger_dev` | R$ 750,00 |
| RH | `salario_cs` | R$ 4.500,00 |
| RH | `trigger_cs` | R$ 1.000,00 |
| RH | `encargos_trabalhistas` | R$ 0,70 |
| Capital | `caixa_inicial` | R$ 2.000,00 |
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
| (+) Caixa Inicial | R$ 2.000,00 |
| (+) Aportes/Investimento | R$ 2.000,00 |
| (+) Receita Bruta | R$ 749,20 |
| (+) Receita Líquida | R$ 637,70 |

## 2.2 Saídas Mês 1
| Descrição | Valor |
|---|---|
| (-) Marketing | R$ 1.750,00 |
| (-) Infraestrutura | R$ 860,00 |
| (-) Pessoal/RH | R$ 0.00 |
| (-) COGS Total | R$ 40,00 |
| (-) OPEX Total | R$ 2.610,00 |
| (-) Impostos | R$ 44,95 |
| (-) Taxas Pagamento | R$ 21,59 |
| (-) CAPEX | R$ -1,00 |

## 2.3 Resultado Mês 1
| Métrica | Valor |
|---|---|
| Caixa Final | **R$ 1.986,70** |
| Burn Rate | R$ 2.013,30 |
| Runway | 1.5 meses |
| Lucro/Prejuízo | R$ -2.012,34 |

---

# 3. 📊 TABELA COMPLETA DO MOTOR (TODAS AS COLUNAS)

> **Total de colunas disponíveis: 107**

## 3.1 Tráfego & Aquisição

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `trafego_total` | 1,123 | 1,402 | 1,759 | 2,846 | 4,755 | 8,266 | 14,535 |
| `trafego_pago` | 866 | 866 | 1,004 | 1,808 | 3,406 | 6,333 | 11,870 |
| `trafego_organico` | 257 | 535 | 754 | 1,038 | 1,349 | 1,932 | 2,664 |
| `trials_total` | 63 | 77 | 95 | 156 | 265 | 463 | 821 |
| `novos_pagantes_total` | 3 | 6 | 10 | 18 | 31 | 55 | 97 |
| `novos_ads` | 3 | 4 | 6 | 12 | 23 | 44 | 82 |
| `novos_organicos` | 0 | 2 | 4 | 6 | 8 | 11 | 15 |

## 3.2 Usuários

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `usuarios_ativos` | 8 | 26 | 58 | 107 | 200 | 373 | 693 |
| `usuarios_lite` | 4 | 13 | 29 | 54 | 99 | 183 | 340 |
| `usuarios_trader` | 3 | 9 | 20 | 37 | 71 | 134 | 249 |
| `usuarios_pro` | 1 | 4 | 9 | 16 | 30 | 56 | 104 |
| `churn_usuarios` | 0 | 2 | 5 | 8 | 13 | 20 | 37 |
| `reativacoes` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 1,00 | R$ 2,00 | R$ 3,00 | R$ 6,00 |

## 3.3 Receita

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `receita_bruta` | R$ 749,20 | R$ 2.487,40 | R$ 5.554,20 | R$ 10.189,30 | R$ 19.110,00 | R$ 35.692,70 | R$ 66.310,70 |
| `receita_assinaturas` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `receita_lite` | R$ 279,60 | R$ 908,70 | R$ 2.027,10 | R$ 3.774,60 | R$ 6.920,10 | R$ 12.791,70 | R$ 23.766,00 |
| `receita_trader` | R$ 299,70 | R$ 899,10 | R$ 1.998,00 | R$ 3.696,30 | R$ 7.092,90 | R$ 13.386,60 | R$ 24.875,10 |
| `receita_pro` | R$ 169,90 | R$ 679,60 | R$ 1.529,10 | R$ 2.718,40 | R$ 5.097,00 | R$ 9.514,40 | R$ 17.669,60 |
| `mrr` | R$ 749,20 | R$ 2.487,40 | R$ 5.554,20 | R$ 10.189,30 | R$ 19.110,00 | R$ 35.692,70 | R$ 66.310,70 |
| `arr` | R$ 8.990,40 | R$ 29.848,80 | R$ 66.650,40 | R$ 122.271,60 | R$ 229.320,00 | R$ 428.312,40 | R$ 795.728,40 |
| `arpu` | R$ 93,65 | R$ 95,67 | R$ 95,76 | R$ 95,23 | R$ 95,55 | R$ 95,69 | R$ 95,69 |

## 3.4 Custos

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `total_cogs` | R$ 40,00 | R$ 136,00 | R$ 304,00 | R$ 555,00 | R$ 1.042,00 | R$ 1.947,00 | R$ 3.617,00 |
| `custo_ia_total` | R$ 40,00 | R$ 136,00 | R$ 304,00 | R$ 555,00 | R$ 1.042,00 | R$ 1.947,00 | R$ 3.617,00 |
| `total_opex` | R$ 2.610,00 | R$ 2.610,00 | R$ 2.889,88 | R$ 4.512,16 | R$ 7.740,80 | R$ 13.654,60 | R$ 39.769,92 |
| `gasto_marketing` | R$ 1.750,00 | R$ 1.750,00 | R$ 2.029,88 | R$ 3.652,16 | R$ 6.880,80 | R$ 12.794,60 | R$ 23.978,92 |
| `custo_infra_fixo` | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 7.290,00 |
| `custo_pessoal` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 8.500,00 |

## 3.5 Margens

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `margem_bruta` | R$ 597,70 | R$ 1.981,22 | R$ 4.423,61 | R$ 8.117,90 | R$ 15.224,00 | R$ 28.433,82 | R$ 52.825,18 |
| `margem_bruta_pct` | 79.78% | 79.65% | 79.64% | 79.67% | 79.67% | 79.66% | 79.66% |
| `ebitda` | R$ -2.012,30 | R$ -628,78 | R$ 1.533,73 | R$ 3.605,74 | R$ 7.483,20 | R$ 14.779,22 | R$ 13.055,26 |
| `ebitda_margin` | -268.59% | -25.28% | 27.61% | 35.39% | 39.16% | 41.41% | 19.69% |
| `lucro_liquido` | R$ -2.012,34 | R$ -628,82 | R$ 1.533,69 | R$ 3.605,70 | R$ 6.983,16 | R$ 14.279,22 | R$ 12.555,26 |
| `margem_liquida` | R$ -268,60 | R$ -25,28 | R$ 27,61 | R$ 35,39 | R$ 36,54 | R$ 40,01 | R$ 18,93 |

## 3.6 Caixa

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `caixa` | R$ 1.986,70 | R$ 5.882,74 | R$ 18.128,51 | R$ 33.743,72 | R$ 55.781,47 | R$ 123.576,73 | R$ 203.616,29 |
| `burn_rate` | 201329.78% | 62878.11% | 0.00% | 0.00% | 451679.80% | 0.00% | 0.00% |
| `runway_meses` | 1.5 | 2.1 | 5.7 | 6.7 | 2.7 | 7.9 | 4.7 |
| `aportes_capital` | R$ 2.000,00 | R$ 2.000,00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |

## 3.7 Unit Economics

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `ltv` | R$ 622,61 | R$ 692,73 | R$ 778,26 | R$ 882,19 | R$ 1.028,65 | R$ 1.229,52 | R$ 1.270,45 |
| `cac_blended` | R$ 583,33 | R$ 291,67 | R$ 202,99 | R$ 202,90 | R$ 221,96 | R$ 232,63 | R$ 247,21 |
| `cac_paid` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `ltv_cac` | 1.07x | 2.38x | 3.83x | 4.35x | 4.63x | 5.29x | 5.14x |
| `payback_meses` | 7.8 | 3.8 | 2.7 | 2.7 | 2.9 | 3.1 | 3.2 |

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
| MRR | R$ 66.310,70 | R$ 112.252,70 | R$ 2.557,30 | 40.9% |
| ARR | R$ 795.728,40 | R$ 1.347.032,40 | R$ 30.687,60 | 40.9% |
| Usuários | 693 | 1,173 | 27 | 40.9% |
| Caixa | R$ 203.616,29 | R$ 280.141,62 | R$ -3.266,90 | 27.3% |
| Receita | R$ 66.310,70 | R$ 112.252,70 | R$ 2.557,30 | 40.9% |
| Lucro | R$ 12.555,26 | R$ 22.381,80 | R$ 677,72 | 43.9% |
| LTV/CAC | 5.14x | 5.49x | 10000.00x | 6.4% |
| Churn | 6.00% | 6.00% | 17.00% | 0.0% |
| Runway | 4.7m | 3.9m | 0.0m | -21.7% |

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
| seed | R$ 934.632.962,85 | R$ 1.275.628.338,50 | R$ 1.376.532.267,15 | R$ 1.195.597.856,17 |
| time_elapsed | R$ 0,05 | R$ 0,06 | R$ 0,09 | R$ 0,06 |
| caixa_final | R$ 4.501,28 | R$ 154.967,14 | R$ 1.762.484,93 | R$ 427.569,40 |
| mrr_final | R$ 4.325,50 | R$ 39.234,05 | R$ 304.412,76 | R$ 94.124,55 |
| arr_final | R$ 51.906,00 | R$ 470.808,60 | R$ 3.652.953,18 | R$ 1.129.494,64 |
| usuarios_final | 45 | 409 | 3,229 | 985 |
| cac_medio | R$ 116,79 | R$ 270,20 | R$ 462,99 | R$ 272,79 |
| ltv_medio | R$ 507,23 | R$ 955,54 | R$ 1.257,45 | R$ 926,65 |
| churn_medio | R$ 0,06 | R$ 0,08 | R$ 0,15 | R$ 0,09 |
| margem_bruta_media | R$ 76,96 | R$ 78,84 | R$ 80,91 | R$ 78,88 |
| ebitda_margin_media | R$ -52,57 | R$ 0,53 | R$ 26,12 | R$ -5,30 |
| nrr | R$ 1,00 | R$ 1,00 | R$ 1,40 | R$ 1,07 |
| burn_rate_medio | R$ 91,36 | R$ 499,34 | R$ 1.019,80 | R$ 502,03 |
| runway_final | R$ 1,60 | R$ 7,39 | R$ 18,57 | R$ 8,05 |
| var95_caixa | R$ -5.791,04 | R$ 2.485,51 | R$ 7.364,64 | R$ 1.698,63 |
| cvar95_caixa | R$ -7.637,53 | R$ 1.865,99 | R$ 3.642,05 | R$ 740,65 |
| roi_total_pct | -29.60% | 897.39% | 17847.28% | 5470.92% |
| payback_meses_medio | R$ 1,51 | R$ 3,29 | R$ 5,72 | R$ 3,44 |
| ltv_cac | 1.53x | 3.67x | 10.32x | 71.22x |

## 5.3 Probabilidades de Risco

| Indicador | Valor |
|---|---|
| Prob. Caixa < 0 | ✅ **1.3%** |
| Prob. Quebra | ✅ **10.7%** |

---

# 6. ⚠️ ALERTAS DO MOTOR

- ℹ️ {'tipo': 'runway_critico', 'mes': 1, 'runway': np.float64(1.5038484281403244)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 2, 'runway': np.float64(0.8395916745600899)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 3, 'runway': np.float64(1.0035137170954511)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 4, 'runway': np.float64(1.2804658240022173)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 5, 'runway': np.float64(1.6574273068515797)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 6, 'runway': np.float64(2.1422928050801167)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 7, 'runway': np.float64(2.7598666279279276)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 8, 'runway': np.float64(3.4946603180028633)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 9, 'runway': np.float64(4.342669824796171)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 10, 'runway': np.float64(5.327176469155275)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 11, 'runway': np.float64(5.677079601846657)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 12, 'runway': np.float64(5.676016317535411)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 13, 'runway': np.float64(5.831914430329931)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 14, 'runway': np.float64(5.965130624904721)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 24, 'runway': np.float64(2.6840210107035625)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 34, 'runway': np.float64(4.706177177067826)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 35, 'runway': np.float64(4.671841060236905)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 36, 'runway': np.float64(4.693033959791339)}

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
| Timestamp | 13/12/2025 18:36:28 |
| Colunas Motor | 107 |
| Métricas MC | 82 |
| Alertas | 18 |

---
*Fim do Relatório*