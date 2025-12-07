# CÉLULA 3 — CONFIGURAÇÃO DE CENÁRIO IDEAL + BENCHMARKS DA INDÚSTRIA
# SEM HARD-CODE — TUDO CONFIGURÁVEL
# ============================================================================

def atualizar_premissas_ideais(premissas):
    """Atualiza o dicionário de premissas com benchmarks ideais."""
    premissas.update({

        # ========================================================================
        # BENCHMARKS DE MERCADO — SaaS / FinTech / Trading (2024)
        # ========================================================================

        # CAC (Custo de Aquisição de Cliente)
        'benchmark_cac_min': 150,       # R$ 100 – limite inferior saudável
        'benchmark_cac_max': 1500,      # R$ 1500 – fintech B2C madura

        # LTV (Lifetime Value)
        'benchmark_ltv_bom_min': 500,   # LTV > R$ 500 = saudável
        'benchmark_ltv_excelente_min': 800,  # fintech geralmente 800–1200

        # LTV/CAC Ratio
        'benchmark_ltv_cac_min': 3,     # mínimo aceitável
        'benchmark_ltv_cac_bom': 5,     # saudável
        'benchmark_ltv_cac_excelente': 5,  # classe mundial >5
        'benchmark_ltv_cac_suspeito': 10,  # >10 deve ser revisado

        # Payback
        'benchmark_payback_excelente': 6,   # <6 meses
        'benchmark_payback_alto': 18,       # >18 meses ruim

        # Churn
        'benchmark_churn_bom': 0.06,       # <5% excelente B2C
        'benchmark_churn_max': 0.12,       # trading aceita até 12%

        # Conversão trial → pagante
        'benchmark_trial_min': 0.10,       # 10% é mínimo
        'benchmark_trial_bom': 0.12,
        'benchmark_trial_excelente': 0.15,

        # Crescimento mensal (conservador / base / agressivo)
        'growth_m1_6_base': 0.10,
        'growth_m7_12_base': 0.08,
        'growth_m13_36_base': 0.05,

        'growth_m1_6_otimista': 0.15,
        'growth_m7_12_otimista': 0.10,
        'growth_m13_36_otimista': 0.07,

        # Taxas e impostos
        'taxa_pagamento': 0.035,   # 3.5% realista
        'impostos': 0.08,          # Simples projetado

        # Configuração de afiliados (default)
        'modelo_afiliado': 'primeira_mensalidade',
        'pct_usuarios_via_afiliado': 0.20,
        'comissao_primeira_mensalidade': 1.0,
        'comissao_afiliado_fixo': 50.00,
        'comissao_afiliado_pct': 0.20,
        'comissao_afiliado_meses': 12,
    })
    return premissas
