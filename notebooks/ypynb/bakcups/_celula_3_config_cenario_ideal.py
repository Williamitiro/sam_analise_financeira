# CÉLULA 03 — CONFIGURAÇÃO DE CENÁRIO IDEAL V9.4 (HERDA DO REAL)
# ============================================================================
# OBJETIVO: Cenário "Execution Perfect" - Herda do Real e aplica otimismo moderado
# LÓGICA: Apenas multiplicadores (não valores absolutos) para criar meta desafiadora
# ============================================================================

from copy import deepcopy

def obter_premissas_ideal(premissas_real):
    """
    Gera cenário Ideal a partir do cenário Real com multiplicadores de otimismo.
    
    Parâmetros:
    -----------
    premissas_real : dict
        Dicionário de premissas V9.2+ do cenário Real
        
    Retorna:
    --------
    dict : Premissas Ideal com otimismo aplicado
    """
    
    # 1. CÓPIA PROFUNDA (evita alterar o original)
    ideal = deepcopy(premissas_real)
    
    # 2. METADADOS (atualiza apenas versionamento)
    ideal['meta_version'] = '9.4-ideal-execution-perfect'
    ideal['meta_updated_at'] = '2025-12-15'
    
    # 3. MULTIPLICADORES DE OTIMISMO (15-30% melhor)
    # Regra: Nunca >30% de melhora (evita meta irreal)
    fatores_otimismo = {
        # FUNIL: +20% conversão
        'taxa_visitante_para_trial': 1.20,
        'taxa_trial_para_pagante': 1.20,
        
        # GROWTH: +30% viralidade, +50% budget (investimento externo)
        'fator_visitas_organicas_por_pagante': 1.30,
        'marketing_fixo_mensal': 1.50,  # Seed funding
        'marketing_perc_receita': 1.20,   # Mais agressivo
        
        # RETENÇÃO: -20% churn
        'churn_inicial': 0.90,
        'churn_maturidade': 0.80,
        
        # PRECIFICAÇÃO: +10% preços (brand premium)
        'preco_lite': 1.10,
        'preco_trader': 1.10,
        'preco_pro': 1.10,
        
        # MELHORIA DE OPERAÇÃO: +15% eficiência
        'ramp_up_inicial': 1.15,
        'ramp_up_incremento': 1.15,
        
        # CAPITAL: +100% (investimento inicial)
        'caixa_inicial': 2.00,  # Multiplicador
        'aporte_mensal': 1.50,   # Multiplicador
        
        # B2B: +50% probabilidade (network forte)
        'b2b_probabilidade_anual': 1.50,
    }
    
    # 4. APLICA MULTIPLICADORES (apenas números)
    for chave, multiplicador in fatores_otimismo.items():
        if isinstance(ideal[chave], (int, float)):
            ideal[chave] *= multiplicador
        elif chave in ['preco_lite', 'preco_trader', 'preco_pro']:  # Preços
            ideal[chave] = round(ideal[chave] * multiplicador, 2)
    
    # 5. CAMPOS IGNORADOS (remover deprecated)
    campos_remover = [
        'crescimento_trafego_mes_1_6',
        'crescimento_trafego_mes_7_12',
        'crescimento_trafego_mes_13_plus',
        'taxa_crescimento_organico_base',  # Não existe mais
    ]
    for campo in campos_remover:
        ideal.pop(campo, None)  # Remove se existir
    
    # 6. AJUSTES MANUAIS ESPECÍFICOS (não multiplicáveis)
    ideal['mix_lite'] = 0.40  # Mais planos premium no ideal
    ideal['mix_trader'] = 0.40
    ideal['mix_pro'] = 0.20
    
    ideal['marketing_teto'] = 50000.00  # Teto maior (seed)
    
    # 7. BENCHMARKS OTIMISTAS (substitui)
    ideal['benchmark_cac_m0'] = 400.0
    ideal['benchmark_cac_m6'] = 200.0
    ideal['benchmark_ltv_cac_m0'] = 3.0
    ideal['benchmark_ltv_cac_m6'] = 4.5
    ideal['benchmark_churn_m0'] = 0.08
    ideal['benchmark_churn_m6'] = 0.04
    
    return ideal


# ========================================================================
# TESTE RÁPIDO DE CONSISTÊNCIA
# ========================================================================
if __name__ == "__main__":
    from celula_2_premissas import PREMISSAS as real
    
    ideal = obter_premissas_ideal(real)
    
    print("="*80)
    print("✅ CÉLULA 03 V9.4 CARREGADA (HERDA DO REAL)")
    print("="*80)
    
    # Verifica se tem growth_tiers
    assert 'growth_tiers' in ideal, "ERRO: growth_tiers não copiado!"
    
    # Verifica se lógica antiga foi removida
    assert 'crescimento_trafego_mes_1_6' not in ideal, "ERRO: Deprecated no ideal!"
    
    # Verifica otimismo aplicado
    assert ideal['taxa_trial_para_pagante'] > real['taxa_trial_para_pagante'], "ERRO: Otimismo não aplicado!"
    
    print("🎯 COMPARATIVO REAL vs IDEAL (exemplos):")
    print(f"   • Conversão Trial→Pago: {real['taxa_trial_para_pagante']:.1%} → {ideal['taxa_trial_para_pagante']:.1%} (+20%)")
    print(f"   • Fator Viral: {real['fator_visitas_organicas_por_pagante']:.1f} → {ideal['fator_visitas_organicas_por_pagante']:.1f} (+30%)")
    print(f"   • Budget Mkt: R${real['marketing_fixo_mensal']:,.0f} → R${ideal['marketing_fixo_mensal']:,.0f} (+50%)")
    print(f"   • Churn Maturidade: {real['churn_maturidade']:.1%} → {ideal['churn_maturidade']:.1%} (-20%)")
    print(f"   • Caixa Inicial: R${real['caixa_inicial']:,.0f} → R${ideal['caixa_inicial']:,.0f} (+100%)")
    print("="*80)