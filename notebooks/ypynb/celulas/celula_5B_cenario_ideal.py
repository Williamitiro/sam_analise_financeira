# CÉLULA 05B — CENÁRIO IDEAL V3.0 (PREMISSAS INDEPENDENTES)
# ============================================================================
# OBJETIVO: Simular cenário Ideal com premissas FIXAS de benchmark.
# IMPORTANTE: Este cenário NÃO herda do Real/Estresse.
# VERSÃO: 3.0 - Premissas Independentes
# ============================================================================

import copy
import traceback
import time
import pandas as pd
import sys
import os

# Adiciona diretório atual para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_4_motor import executar_motor_fintech_v10_production_ready
    from celula_4A_motor_granularidade import expandir_granularidade_completa
    from celula_3_config_cenario_ideal import obter_premissas_ideal
except ImportError:
    pass

def executar_analise_ideal(premissas_base=None):
    """
    Executa a simulação do cenário Ideal.
    
    IMPORTANTE: Este cenário usa PREMISSAS_IDEAL independentes.
    O parâmetro premissas_base é IGNORADO para evitar herança.
    
    Retorna tupla: (df_mensal_ideal, df_anual_ideal, df_semanal_ideal, df_diario_ideal, metricas_ideal, alertas_ideal)
    """
    print("\n" + "="*88)
    print("🚀 INICIANDO CENÁRIO 05B — IDEAL (V3.0 - PREMISSAS INDEPENDENTES)")
    print("="*88)
    
    start_time = time.time()
    
    # ----------------------------------------------------------------------------
    # 1) Obter PREMISSAS_IDEAL independentes (NÃO herda do Real)
    # ----------------------------------------------------------------------------
    print("\n📋 Carregando PREMISSAS_IDEAL (benchmark independente)...")
    
    try:
        premissas_ideal = obter_premissas_ideal()
        print("   ✅ PREMISSAS_IDEAL carregadas com sucesso")
        print(f"   • Usuários iniciais: {premissas_ideal.get('usuarios_pagos_iniciais', 'N/A')}")
        print(f"   • Tráfego inicial: {premissas_ideal.get('trafego_inicial', 'N/A')}")
        print(f"   • Caixa inicial: R$ {premissas_ideal.get('caixa_inicial', 'N/A'):,.2f}")
        print(f"   • Marketing fixo: R$ {premissas_ideal.get('marketing_fixo_mensal', 'N/A'):,.2f}")
        print(f"   • Churn maturidade: {premissas_ideal.get('churn_maturidade', 'N/A')*100:.1f}%")
    except Exception as e:
        print(f"   ❌ Erro ao carregar PREMISSAS_IDEAL: {e}")
        print("   ⚠️ Usando fallback: criando premissas benchmark inline")
        premissas_ideal = _criar_premissas_ideal_fallback()

    # ----------------------------------------------------------------------------
    # 2) Executar Motor com PREMISSAS_IDEAL
    # ----------------------------------------------------------------------------
    try:
        print("\n⏱️ Rodando o motor financeiro com PREMISSAS_IDEAL...")
        df_mensal_ideal, df_anual_ideal, metricas_ideal, alertas_ideal = executar_motor_fintech_v10_production_ready(
            premissas_ideal,        # ← USA PREMISSAS INDEPENDENTES!
            seed=None,
            variacao_params=None,   # Sem overrides - já está tudo na premissa
            modo_debug=False
        )
        tempo_motor = time.time() - start_time
        print(f"\n✔️ Motor concluído (tempo: {tempo_motor:.2f}s).")
        
        # Log de validação
        if len(df_mensal_ideal) > 0:
            mrr_inicial = df_mensal_ideal['mrr'].iloc[0]
            mrr_final = df_mensal_ideal['mrr'].iloc[-1]
            usuarios_final = df_mensal_ideal['usuarios_ativos'].iloc[-1]
            print(f"\n📊 RESULTADOS IDEAL:")
            print(f"   • MRR M1: R$ {mrr_inicial:,.0f}")
            print(f"   • MRR M36: R$ {mrr_final:,.0f}")
            print(f"   • Usuários M36: {usuarios_final}")

    except Exception as e:
        print("\n❌ ERRO DURANTE A EXECUÇÃO DO MOTOR:")
        traceback.print_exc()
        raise e
        
    # ----------------------------------------------------------------------------
    # 3) Expansão de Granularidade
    # ----------------------------------------------------------------------------
    print("\n📐 Gerando granularidades semanal e diária para cenário IDEAL...")
    try:
        df_semanal_ideal, df_diario_ideal = expandir_granularidade_completa(
            df_mensal_ideal, 
            premissas_ideal, 
            meses_expandir=6,
            seed=premissas_ideal.get('seed_fixa', 42) + 500
        )
        print(f"   ✅ df_ideal_s: {len(df_semanal_ideal)} semanas geradas")
        print(f"   ✅ df_ideal_d: {len(df_diario_ideal)} dias gerados")
    except Exception as e:
        print(f"   ⚠️ Impossível gerar granularidade: {e}")
        df_semanal_ideal = pd.DataFrame()
        df_diario_ideal = pd.DataFrame()

    tempo_total = time.time() - start_time
    
    print("\n" + "="*88)
    print(f"✅ CENÁRIO IDEAL CONCLUÍDO em {tempo_total:.2f}s")
    print("="*88)
    
    return df_mensal_ideal, df_anual_ideal, df_semanal_ideal, df_diario_ideal, metricas_ideal, alertas_ideal


def _criar_premissas_ideal_fallback():
    """
    Cria premissas de fallback se o import falhar.
    Valores de benchmark otimistas.
    """
    return {
        'meta_version': '9.0-ideal-fallback',
        'meses_projecao': 36,
        'seed_fixa': 42,
        'semanas_por_mes': 4.33,
        'meses_por_ano': 12,
        
        'sazonalidade_trafego': {
            1: 1.30, 2: 1.10, 3: 1.15, 4: 1.00, 5: 1.05, 6: 1.00,
            7: 0.85, 8: 1.00, 9: 1.00, 10: 1.05, 11: 1.10, 12: 0.75
        },
        
        'usuarios_pagos_iniciais': 10,
        'trafego_inicial': 300,
        'crescimento_trafego_mes_1_6': 0.12,
        'crescimento_trafego_mes_7_12': 0.10,
        'crescimento_trafego_mes_13_plus': 0.06,
        'mercado_potencial_traders': 150000,
        
        'taxa_visitante_para_trial': 0.08,
        'taxa_trial_para_pagante': 0.15,
        'ramp_up_inicial': 0.70,
        'ramp_up_incremento': 0.08,
        
        'fator_visitas_organicas_por_pagante': 5.0,
        'taxa_crescimento_organico_base': 0.03,
        'elasticidade_organico': 0.70,
        
        'churn_inicial': 0.08,
        'churn_maturidade': 0.04,
        'churn_base': 0.05,
        'churn_decaimento_mensal': 0.002,
        'taxa_reativacao_base_cancelada': 0.02,
        
        'preco_lite': 500, 
        'preco_trader': 1500, 
        'preco_pro': 5000,
        'mix_lite': 0.45,
        'mix_trader': 0.40,
        'mix_pro': 0.15,
        'taxa_upgrade_lite_trader': 0.03,
        
        'mix_pagamento_cartao': 0.55, 
        'mix_pagamento_pix': 0.40, 
        'mix_pagamento_boleto': 0.05,
        'taxa_processamento_cartao': 0.045,
        'taxa_processamento_pix': 0.01,
        'taxa_processamento_boleto': 0.035,
        'taxa_chargeback': 0.003,
        'taxa_inadimplencia_cartao': 0.03,
        'taxa_inadimplencia_pix': 0.05,
        'taxa_inadimplencia_boleto': 0.02,
        
        'imposto_simples_inicial': 0.06,
        'imposto_lucro_presumido': 0.1633,
        'threshold_regime_tributario': 4800000.00,
        
        'custo_ia_lite': 200, 
        'custo_ia_trader': 600, 
        'custo_ia_pro': 2000,
        'custo_ferramentas_base': 1.00,
        'custo_suporte_por_1000_users': 1.00,
        
        'infra_tier_1_limite': 500,
        'infra_tier_2_limite': 1500,
        'infra_tier_3_limite': 5000,
        'infra_tier_4_limite': 10000,
        
        't1_vps_app_api': 120.00, 
        't1_vps_windows_mt5': 180.00, 
        't1_database_managed': 80.00,
        't1_storage_s3': 20.00, 
        't1_ferramentas_dev': 300.00, 
        't1_observability': 0.00,
        't1_scraping_news': 100.00, 
        't1_dominio_dns': 10.00, 
        't1_email_transacional': 50.00,
        
        'marketing_habilitado': True,
        'marketing_fixo_mensal': 5000.00,
        'marketing_perc_receita': 0.30,
        'marketing_teto': 30000.00,
        'marketing_budget_ref_brand_lift': 3000.0,
        'limite_inventario_mensal': 50000,
        
        'canal_instagram_pct': 0.35, 'cpc_instagram': 0.50, 'conv_instagram': 0.04,
        'canal_facebook_pct': 0.20, 'cpc_facebook': 0.70, 'conv_facebook': 0.03,
        'canal_youtube_pct': 0.35, 'cpc_youtube': 2.50, 'conv_youtube': 0.10,
        'canal_google_pct': 0.10, 'cpc_google': 5.00, 'conv_google': 0.12,
        
        'modelo_afiliado_habilitado': True,
        'pct_usuarios_via_afiliado': 0.20,
        'comissao_afiliado_tipo': 'primeira_mensalidade',
        
        'salario_fundador': 8000.00, 'trigger_fundador': 15000.00,
        'salario_dev_senior': 25000.00, 'trigger_dev': 10,
        'salario_cs': 4000.00, 'trigger_cs': 500,
        'encargos_trabalhistas': 0.70,
        
        'custo_escritorio_base': 3500.00, 
        'trigger_escritorio': 100000.00,
        'custo_contabilidade_adv': 1000.00,
        'trigger_contabilidade': 50000.00,
        'custo_juridico_compliance': 100.00,
        'verba_viagens_base': 1.00, 
        'verba_viagens_pct_receita': 0.02,
        'trigger_viagens_receita': 30000.00,
        'conselho_jeton': 3000.00, 
        'trigger_conselho_mrr': 80000.00,
        'freelancers_trimestral': 1000.00,
        'trigger_freelancer_receita': 20000.00,
        'beneficios_executivos': 5000.00, 
        'trigger_beneficios_lucro': 50000.00,
        
        'b2b_probabilidade_anual': 0.15,
        'b2b_setup_fee': 15000.00,
        'b2b_custo_implantacao': 5000.00,
        
        'caixa_inicial': 50000.00,
        'aporte_mensal': 5000.00,
        'meses_aporte': 12,
        'threshold_caixa_quebra': -10000.0,
        'caixa_reserva_operacional': 5000.0,
        'capex_inicial': 5000.00,
        'capex_recorrente_24m': 12000.00,     
        'tempo_depreciacao_equipamento_meses': 24,
        
        'percentual_distribuicao': 0.00,
        'split_fundador': 0.50,
        'split_investidor': 0.50,
    }


if __name__ == "__main__":
    executar_analise_ideal(None)
