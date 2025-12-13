# RELATÓRIO DE AUDITORIA E DADOS BRUTOS
**Data:** 2025-12-12 10:06:22
**Versão Premissas:** 9.0-full-documented

##  1. PREMISSAS CONFIGURADAS (AUDITORIA)
| Categoria | Variável | Valor Configurado |
|---|---|---|
| Calendário | Data Início | 2025-11-01 |
| Pricing | Preço Lite | R$ 69.9 |
| Pricing | Preço Trader | R$ 99.9 |
| Pricing | Preço Pro | R$ 169.9 |
| Custos | Custo IA Lite | R$ 2.5 |
| Custos | Custo IA Trader | R$ 4.5 |
| Custos | Custo IA Pro | R$ 13.0 |
| Growth | Tráfego Inicial | 300 |
| Growth | Mkt Fixo | R$ 1500.0 |
| RH | Salário Dev Sr | R$ 10000.0 (Trigger: 750) |

---

## PÁGINA 1: COCKPIT (Resumo)
| Métrica | Valor Final (M36) | Média Anual |
|---|---|---|
| Caixa Final | R$ 141,820.36 | - |
| Receita Total (3 Anos) | R$ 619,981.50 | - |
| Lucro Líquido Acum. | R$ 123,320.36 | - |
| Runway (meses) | N/A | - |

## PÁGINA 2: GROWTH MACHINE
- **Usuários Ativos (Final):** 624
- **CAC Blended (Médio):** R$ 240.51
- **LTV (Final):** R$ 1,135.54
- **LTV/CAC (Final):** 4.72x

## PÁGINA 3: FINANCEIRO (DRE)
### DRE Anual (Resumo)
|    |   receita_bruta |   custo_total |   margem_bruta |   opex_total |   ebitda |   lucro_liquido |
|---:|----------------:|--------------:|---------------:|-------------:|---------:|----------------:|
|  0 |         33075.3 |        1651   |        31424.3 |      28904.2 | -2402.29 |        -2402.79 |
|  1 |        139114   |        6971   |       132144   |      60543.4 | 50896.7  |        50396.2  |
|  2 |        447792   |       22428.5 |       425363   |     277395   | 81327    |        75327    |

## PÁGINA 4: UNIT ECONOMICS
- ARPU: R$ 95.69
- Churn Rate: 6.75%

## PÁGINA 5: RISCO E SENSIBILIDADE

### TORNADO PLOT (Top 5 Sensibilidade)
| nome_display              |   valor_base |   impacto_relativo |   ltv_cac_min |   ltv_cac_max |
|:--------------------------|-------------:|-------------------:|--------------:|--------------:|
| Churn Base (%)            |         0.12 |          0.428115  |       4.80406 |       3.15613 |
| Conv. Trial -> Pago       |         0.12 |          0.275188  |       3.35055 |       4.40983 |
| cpc_youtube               |         3    |          0.0997536 |       4.05181 |       3.66783 |
| taxa_visitante_para_trial |         0.05 |          0.0884776 |       3.66561 |       4.00618 |
| CPC Google                |         6    |          0.0582368 |       3.96664 |       3.74247 |

### MONTE CARLO (Estatísticas)
Dados de Monte Carlo indisponíveis.