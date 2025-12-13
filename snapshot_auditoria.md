# 🔬 RELATÓRIO DE AUDITORIA FORENSE V7.0

**Gerado:** 13/12/2025 11:22:47
**Premissas:** V9.0-full-documented
**Motor:** V13 | **Colunas:** 107
**Monte Carlo:** 150 simulações

> ⚠️ DOCUMENTO CONFIDENCIAL

---

# 1. 📋 TODAS AS PREMISSAS

| Categoria | Parâmetro | Valor |
|---|---|---|
| Growth | `usuarios_pagos_iniciais` | 5 |
| Growth | `trafego_inicial` | 100 |
| Growth | `crescimento_trafego_mes_1_6` | 0.05% |
| Growth | `taxa_visitante_para_trial` | 0.05% |
| Growth | `taxa_trial_para_pagante` | 0.12% |
| Churn | `churn_inicial` | 0.12% |
| Churn | `churn_maturidade` | 0.06% |
| Churn | `churn_base` | 0.07% |
| Churn | `churn_decaimento_mensal` | 0.00% |
| Pricing | `preco_lite` | R$ 69,90 |
| Pricing | `preco_trader` | R$ 99,90 |
| Pricing | `preco_pro` | R$ 169,90 |
| Pricing | `mix_lite` | 0.50% |
| Pricing | `mix_trader` | 0.35% |
| Pricing | `mix_pro` | 0.15% |
| COGS | `custo_ia_lite` | 200 |
| COGS | `custo_ia_trader` | 600 |
| COGS | `custo_ia_pro` | 2000 |
| Marketing | `marketing_fixo_mensal` | 0.0000 |
| Marketing | `marketing_perc_receita` | 0.40% |
| Marketing | `marketing_teto` | R$ 25.000,00 |
| RH | `salario_fundador` | R$ 5.000,00 |
| RH | `trigger_fundador` | R$ 25.000,00 |
| RH | `salario_dev_senior` | R$ 30.000,00 |
| RH | `trigger_dev` | 15 |
| RH | `salario_cs` | R$ 4.500,00 |
| RH | `trigger_cs` | 1000 |
| RH | `encargos_trabalhistas` | 0.70% |
| Capital | `caixa_inicial` | R$ 4.000,00 |
| Capital | `aporte_mensal` | R$ 2.000,00 |
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
| (+) Caixa Inicial | R$ 4.000,00 |
| (+) Aportes/Investimento | R$ 2.000,00 |
| (+) Receita Bruta | R$ 509,50 |
| (+) Receita Líquida | R$ 433,67 |

## 2.2 Saídas Mês 1
| Descrição | Valor |
|---|---|
| (-) Marketing | R$ 1,00 |
| (-) Infraestrutura | R$ 860,00 |
| (-) Pessoal/RH | R$ 0.00 |
| (-) COGS Total | R$ 3.600,00 |
| (-) OPEX Total | R$ 861,00 |
| (-) Impostos | R$ 30,57 |
| (-) Taxas Pagamento | R$ 14,69 |
| (-) CAPEX | R$ -1,00 |

## 2.3 Resultado Mês 1
| Métrica | Valor |
|---|---|
| Caixa Final | **R$ 1.971,67** |
| Burn Rate | R$ 4.028,33 |
| Runway | 0.9 meses |
| Lucro/Prejuízo | R$ -4.027,37 |

---

# 3. 📊 TABELA COMPLETA DO MOTOR (TODAS AS COLUNAS)

> **Total de colunas disponíveis: 107**

## 3.1 Tráfego & Aquisição

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `trafego_total` | 107 | 137 | 163 | 207 | 241 | 300 | 346 |
| `trafego_pago` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `trafego_organico` | 107 | 137 | 163 | 207 | 241 | 300 | 346 |
| `trials_total` | 5 | 6 | 8 | 10 | 12 | 15 | 17 |
| `novos_pagantes_total` | 0 | 0 | 0 | 1 | 1 | 1 | 2 |
| `novos_ads` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `novos_organicos` | 0 | 0 | 0 | 1 | 1 | 1 | 2 |

## 3.2 Usuários

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `usuarios_ativos` | 5 | 5 | 5 | 9 | 12 | 14 | 17 |
| `usuarios_lite` | 2 | 2 | 2 | 5 | 6 | 7 | 8 |
| `usuarios_trader` | 2 | 2 | 2 | 3 | 4 | 5 | 6 |
| `usuarios_pro` | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| `churn_usuarios` | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| `reativacoes` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |

## 3.3 Receita

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `receita_bruta` | R$ 509,50 | R$ 509,50 | R$ 509,50 | R$ 819,10 | R$ 1.158,80 | R$ 1.328,60 | R$ 1.668,30 |
| `receita_assinaturas` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `receita_lite` | R$ 139,80 | R$ 139,80 | R$ 139,80 | R$ 349,50 | R$ 419,40 | R$ 489,30 | R$ 559,20 |
| `receita_trader` | R$ 199,80 | R$ 199,80 | R$ 199,80 | R$ 299,70 | R$ 399,60 | R$ 499,50 | R$ 599,40 |
| `receita_pro` | R$ 169,90 | R$ 169,90 | R$ 169,90 | R$ 169,90 | R$ 339,80 | R$ 339,80 | R$ 509,70 |
| `mrr` | R$ 509,50 | R$ 509,50 | R$ 509,50 | R$ 819,10 | R$ 1.158,80 | R$ 1.328,60 | R$ 1.668,30 |
| `arr` | R$ 6.114,00 | R$ 6.114,00 | R$ 6.114,00 | R$ 9.829,20 | R$ 13.905,60 | R$ 15.943,20 | R$ 20.019,60 |
| `arpu` | R$ 101,90 | R$ 101,90 | R$ 101,90 | R$ 91,01 | R$ 96,57 | R$ 94,90 | R$ 98,14 |

## 3.4 Custos

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `total_cogs` | R$ 3.600,00 | R$ 3.600,00 | R$ 3.600,00 | R$ 4.800,00 | R$ 7.600,00 | R$ 8.400,00 | R$ 11.200,00 |
| `custo_ia_total` | R$ 3.600,00 | R$ 3.600,00 | R$ 3.600,00 | R$ 4.800,00 | R$ 7.600,00 | R$ 8.400,00 | R$ 11.200,00 |
| `total_opex` | R$ 861,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 51.860,00 |
| `gasto_marketing` | R$ 1,00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `custo_infra_fixo` | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 | R$ 860,00 |
| `custo_pessoal` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 51.000,00 |

## 3.5 Margens

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `margem_bruta` | R$ -3.166,33 | R$ -3.166,33 | R$ -3.166,33 | R$ -4.102,80 | R$ -6.613,66 | R$ -7.269,13 | R$ -9.779,98 |
| `margem_bruta_pct` | -621.46% | -621.46% | -621.46% | -500.89% | -570.73% | -547.13% | -586.22% |
| `ebitda` | R$ -4.027,33 | R$ -4.026,33 | R$ -4.026,33 | R$ -4.962,80 | R$ -7.473,66 | R$ -8.129,13 | R$ -61.639,98 |
| `ebitda_margin` | -790.45% | -790.25% | -790.25% | -605.88% | -644.95% | -611.86% | -3694.78% |
| `lucro_liquido` | R$ -4.027,37 | R$ -4.026,37 | R$ -4.026,37 | R$ -4.962,84 | R$ -7.973,70 | R$ -8.629,13 | R$ -62.139,98 |
| `margem_liquida` | R$ -790,45 | R$ -790,26 | R$ -790,26 | R$ -605,89 | R$ -688,10 | R$ -649,49 | R$ -3.724,75 |

## 3.6 Caixa

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `caixa` | R$ 1.971,67 | R$ -8.363,75 | R$ -24.521,70 | R$ -50.833,61 | R$ -103.028,30 | R$ -150.585,57 | R$ -458.463,12 |
| `burn_rate` | 402832.51% | 402632.51% | 402632.51% | 496280.05% | 1947365.55% | 812912.56% | 6163998.06% |
| `runway_meses` | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `aportes_capital` | R$ 2.000,00 | R$ 2.000,00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |

## 3.7 Unit Economics

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `ltv` | R$ -5.277,21 | R$ -5.629,02 | R$ -6.118,50 | R$ -4.823,99 | R$ -6.446,06 | R$ -6.787,23 | R$ -8.522,86 |
| `cac_blended` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `cac_paid` | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| `ltv_cac` | 0.00x | 0.00x | 0.00x | 0.00x | 0.00x | 0.00x | 0.00x |
| `payback_meses` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 3.8 Churn

| Métrica | M1 | M6 | M12 | M18 | M24 | M30 | M36 |
|---|---|---|---|---|---|---|---|
| `churn_rate` | 12.00% | 11.25% | 10.35% | 9.45% | 8.55% | 7.65% | 6.75% |
| `retention_rate` | 88.00% | 88.75% | 89.65% | 90.55% | 91.45% | 92.35% | 93.25% |

---

# 4. ⚖️ COMPARATIVO: REAL vs IDEAL vs ESTRESSE

## 4.1 Snapshot M36

| Métrica | Real | Ideal | Estresse | Gap Real/Ideal |
|---|---|---|---|---|
| MRR | R$ 1.668,30 | R$ 1.977,90 | R$ 509,50 | 15.7% |
| ARR | R$ 20.019,60 | R$ 23.734,80 | R$ 6.114,00 | 15.7% |
| Usuários | 17 | 21 | 5 | 19.0% |
| Caixa | R$ -458.463,12 | R$ -1.722.476,62 | R$ -117.453,90 | 73.4% |
| Receita | R$ 1.668,30 | R$ 1.977,90 | R$ 509,50 | 15.7% |
| Lucro | R$ -62.139,98 | R$ -63.076,46 | R$ -4.526,33 | 1.5% |
| LTV/CAC | 0.00x | 0.00x | 0.00x | 0.0% |
| Churn | 6.75% | 6.00% | 18.75% | -12.5% |
| Runway | 0.0m | 0.0m | 0.0m | 0.0% |

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
| seed | R$ 1.152.694.214,85 | R$ 1.719.181.864,50 | R$ 1.791.669.362,15 | R$ 1.554.515.147,17 |
| time_elapsed | R$ 0,05 | R$ 0,06 | R$ 0,07 | R$ 0,06 |
| caixa_final | R$ -1.067.786,48 | R$ -160.449,41 | R$ 30.433,87 | R$ -348.662,12 |
| mrr_final | R$ 509,50 | R$ 1.498,40 | R$ 4.315,99 | R$ 1.860,85 |
| arr_final | R$ 6.114,00 | R$ 17.980,80 | R$ 51.791,88 | R$ 22.330,26 |
| usuarios_final | 5 | 16 | 45 | 19 |
| cac_medio | R$ 0.00 | R$ 0.00 | R$ 0.00 | R$ 0.00 |
| ltv_medio | R$ 446,39 | R$ 805,66 | R$ 1.115,61 | R$ 796,62 |
| churn_medio | R$ 0,06 | R$ 0,09 | R$ 0,16 | R$ 0,10 |
| margem_bruta_media | R$ 66,70 | R$ 68,68 | R$ 70,19 | R$ 68,56 |
| ebitda_margin_media | R$ -1.327,57 | R$ -354,49 | R$ -50,99 | R$ -532,50 |
| nrr | R$ 1,00 | R$ 1,00 | R$ 1,00 | R$ 0,99 |
| burn_rate_medio | R$ 630,54 | R$ 5.541,71 | R$ 30.329,46 | R$ 10.583,77 |
| runway_final | R$ 0.00 | R$ 0.00 | R$ 27,58 | R$ 4,33 |
| var95_caixa | R$ -982.200,00 | R$ -71.707,91 | R$ 8.116,40 | R$ -305.862,62 |
| cvar95_caixa | R$ -1.043.356,82 | R$ -135.114,44 | R$ 6.242,15 | R$ -339.120,15 |
| roi_total_pct | -10988.09% | -745.62% | 58.59% | -2518.75% |
| ltv_cac | 10000.00x | 10000.00x | 10000.00x | 10000.00x |

## 5.3 Probabilidades de Risco

| Indicador | Valor |
|---|---|
| Prob. Caixa < 0 | 🔴 **70.7%** |
| Prob. Quebra | 🔴 **70.0%** |

---

# 6. ⚠️ ALERTAS DO MOTOR

- ℹ️ {'tipo': 'runway_critico', 'mes': 1, 'runway': np.float64(0.8901109225123263)}
- ℹ️ {'tipo': 'runway_critico', 'mes': 2, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 3: Marketing CORTADO (100%). Caixa negativo: R$ -258.45. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 3, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 4: Marketing CORTADO (100%). Caixa negativo: R$ -2284.78. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 4, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 5: Marketing CORTADO (100%). Caixa negativo: R$ -4311.10. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 5, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 6: Marketing CORTADO (100%). Caixa negativo: R$ -6337.43. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 6, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 7: Marketing CORTADO (100%). Caixa negativo: R$ -8363.75. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 7, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 8: Marketing CORTADO (100%). Caixa negativo: R$ -10390.08. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 8, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 9: Marketing CORTADO (100%). Caixa negativo: R$ -12416.40. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 9, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 10: Marketing CORTADO (100%). Caixa negativo: R$ -14442.73. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 10, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 11: Marketing CORTADO (100%). Caixa negativo: R$ -16469.05. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 11, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 12: Marketing CORTADO (100%). Caixa negativo: R$ -20495.38. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 12, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 13: Marketing CORTADO (100%). Caixa negativo: R$ -24521.70. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 13, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 14: Marketing CORTADO (100%). Caixa negativo: R$ -28548.03. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 14, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 15: Marketing CORTADO (100%). Caixa negativo: R$ -32574.35. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 15, 'runway': np.float64(0.0)}
- ℹ️ ⚠️ Mês 16: Marketing CORTADO (100%). Caixa negativo: R$ -36741.18. Sobrevivência ameaçada.
- ℹ️ {'tipo': 'runway_critico', 'mes': 16, 'runway': np.float64(0.0)}

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
| Timestamp | 13/12/2025 11:22:47 |
| Colunas Motor | 107 |
| Métricas MC | 78 |
| Alertas | 71 |

---
*Fim do Relatório*