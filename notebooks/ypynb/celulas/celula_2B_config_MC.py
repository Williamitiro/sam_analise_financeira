
try:
    # Tenta usar a variavel global se existir (Notebook)
    if 'PREMISSAS' not in globals():
        from celula_2_premissas import PREMISSAS
except ImportError:
    # Fallback se não conseguir importar (cria dict vazio para nao quebrar)
    PREMISSAS = {}


PREMISSAS['monte_carlo'] = {
    # ------------------------------------------------------------------------
    # CONFIGURAÇÃO GERAL
    # ------------------------------------------------------------------------
    'n_simulacoes': 50,              # Número de simulações por cenário
    'enable_scenarios': True,         # Roda Pessimista/Base/Otimista
    'enable_correlations': True,      # Ativa correlações entre variáveis
    'save_timeseries': True,         # Economiza memória (não salva séries)
    'timeout_seconds': 30,            # Timeout por simulação (evita travamento)
    'checkpoint_every': 50,           # Salva a cada N simulações
    'save_folder': 'mc_outputs',      # Pasta de saída
    'random_seed': 42,                # Seed base (reprodutibilidade)
    
    # ------------------------------------------------------------------------
    # CENÁRIOS (MÚLTIPLOS FUTUROS)
    # ------------------------------------------------------------------------
    # Cada cenário aplica multiplicadores sobre as premissas base
    'cenarios': {
        'pessimista': {
            'nome': 'Recessão / Crise',
            'descricao': 'CAC alto, churn elevado, conversão baixa',
            'multiplicadores': {
                'churn_inicial': 1.25,           # +25% churn
                'taxa_trial_para_pagante': 0.75, # -25% conversão
                'marketing_fixo_mensal': 0.70,   # -30% budget
                'cpc_instagram': 1.25,           # +25% CPC
                'cpc_facebook': 1.25,
                'cpc_google': 1.25,
                'cpc_youtube': 1.25,
            }
        },
        'base': {
            'nome': 'Expectativa Realista',
            'descricao': 'Condições esperadas com variação estocástica',
            'multiplicadores': {
                # Todos os multiplicadores = 1.0 (sem alteração)
            }
        },
        'otimista': {
            'nome': 'Bull Market / PMF Forte',
            'descricao': 'Viralidade alta, retenção excelente',
            'multiplicadores': {
                'churn_inicial': 0.70,           # -30% churn
                'taxa_trial_para_pagante': 1.35, # +35% conversão
                'marketing_fixo_mensal': 1.30,   # +30% budget
                'cpc_instagram': 0.80,           # -20% CPC
                'cpc_facebook': 0.80,
                'cpc_google': 0.80,
                'cpc_youtube': 0.80,
                'fator_visitas_organicas_por_pagante': 1.50,  # +50% viralidade
            }
        }
    },
    
    # ------------------------------------------------------------------------
    # VARIÁVEIS ESTOCÁSTICAS (O QUE VARIA EM CADA SIMULAÇÃO)
    # ------------------------------------------------------------------------
    # Cada variável define:
    # - 'std': Desvio padrão relativo (ex: 0.15 = ±15% do valor base)
    # - 'min': Limite inferior (proteção contra valores absurdos)
    # - 'max': Limite superior (proteção contra valores absurdos)
    # - 'dist': Tipo de distribuição ('normal', 'lognormal', 'uniform')
    # ------------------------------------------------------------------------
    'variaveis': {
        # GROWTH
        'marketing_fixo_mensal': {
            'std': 0.15,          # ±15% variação
            'min': 0,             # Mínimo R$ 0 (Corrigido: Permite Zero)
            'max': 10000,         # Máximo R$ 10k (fase bootstrap)
            'dist': 'normal'
        },
        'taxa_trial_para_pagante': {
            'std': 0.20,          # ±20% variação (corrigido de 30%)
            'min': 0.01,          # 1% mínimo
            'max': 0.60,          # 60% máximo (muito otimista)
            'dist': 'normal'
        },
        'taxa_visitante_para_trial': {
            'std': 0.25,
            'min': 0.01,
            'max': 0.15,
            'dist': 'normal'
        },
        
        # RETENÇÃO
        'churn_inicial': {
            'std': 0.20,          # ±20% variação (corrigido de 30%)
            'min': 0.05,         # 0.5% mínimo (mundo perfeito)
            'max': 0.35,          # 50% máximo (desastre)
            'dist': 'normal'
        },
        
        # CPC (CANAIS)
        'cpc_instagram': {
            'std': 0.20,          # ±20% (mercado de ads flutua)
            'min': 0.10,
            'max': 5.0,
            'dist': 'lognormal'   # CPC tende a ter cauda longa
        },
        'cpc_facebook': {
            'std': 0.20,
            'min': 0.10,
            'max': 5.0,
            'dist': 'lognormal'
        },
        'cpc_google': {
            'std': 0.25,          # Google varia mais
            'min': 0.50,
            'max': 15.0,
            'dist': 'lognormal'
        },
        'cpc_youtube': {
            'std': 0.25,
            'min': 0.50,
            'max': 10.0,
            'dist': 'lognormal'
        },
        
        # MIX DE PLANOS
        'mix_lite': {
            'std': 0.10,          # ±10%
            'min': 0.20,
            'max': 0.80,
            'dist': 'normal'
        },
        
        # CUSTOS VARIÁVEIS
        'custo_ia_lite': {
            'std': 0.20,          # Custo de IA pode variar (otimizações)
            'min': 0.50,
            'max': 10.0,
            'dist': 'normal'
        },
        'custo_ia_trader': {
            'std': 0.20,
            'min': 1.0,
            'max': 15.0,
            'dist': 'normal'
        },
        'custo_ia_pro': {
            'std': 0.25,
            'min': 5.0,
            'max': 30.0,
            'dist': 'normal'
        },
        
        # IMPOSTOS
        'imposto_simples_inicial': {
            'std': 0.10,          # Variação pequena (lei)
            'min': 0.03,
            'max': 0.15,
            'dist': 'normal'
        },
        
        # B2B (ALTA INCERTEZA)
        'b2b_probabilidade_anual': {
            'std': 0.50,          # ±50% (muito incerto)
            'min': 0.0,
            'max': 0.80,
            'dist': 'uniform'     # Não sabemos a distribuição
        },
        
        # CRESCIMENTO ORGÂNICO
        'crescimento_trafego_mes_1_6': {
            'std': 0.20,          # ±20% variação (corrigido de 30%)
            'min': 0.05,
            'max': 0.40,
            'dist': 'normal'
        },
    },
    
    # ------------------------------------------------------------------------
    # MATRIZ DE CORRELAÇÃO (COPULAS)
    # ------------------------------------------------------------------------
    # Define como as variáveis se movem juntas.
    # Valores: -1.0 (correlação negativa perfeita) a +1.0 (correlação positiva perfeita)
    # 
    # LÓGICA ECONÔMICA:
    # - CAC ↑ → Churn ↑ (clientes caros são piores)
    # - Conversão ↓ → CAC ↑ (precisa mais budget para mesmo resultado)
    # - Churn ↑ → Custos IA ↑ (clientes ruins consomem mais suporte)
    # ------------------------------------------------------------------------
    'correlacoes': {
        # Formato: ('var1', 'var2'): correlação
        ('churn_inicial', 'cpc_instagram'): 0.60,          # CAC alto → Churn alto
        ('churn_inicial', 'cpc_google'): 0.55,
        ('taxa_trial_para_pagante', 'cpc_instagram'): -0.45,  # Conversão ↓ → CAC ↑
        ('taxa_trial_para_pagante', 'churn_inicial'): -0.40,  # Boa conversão → Baixo churn
        ('custo_ia_lite', 'churn_inicial'): 0.30,          # Clientes problemáticos gastam mais IA
        ('marketing_fixo_mensal', 'crescimento_trafego_mes_1_6'): 0.70,  # + Budget → + Growth
    },
    
    # ------------------------------------------------------------------------
    # CHOQUES ESTRUTURAIS (EVENTOS RAROS)
    # ------------------------------------------------------------------------
    # Probabilidade de eventos disruptivos que alteram múltiplos parâmetros
    'choques': {
        'atraso_aporte': {
            'probabilidade': 0.20,        # 20% chance por simulação
            'descricao': 'Aporte atrasado 1-3 meses',
            'efeito': {
                'meses_aporte': -2,       # Reduz 2 meses de garantia
                'marketing_fixo_mensal': 0.50,  # Corta 50% do budget
            }
        },
        'perda_funcionario_chave': {
            'probabilidade': 0.10,        # 10% chance
            'descricao': 'Dev sênior sai',
            'efeito': {
                'ramp_up_incremento': 0.03,  # Reduz eficiência pela metade
            }
        },
        'viral_boost': {
            'probabilidade': 0.05,        # 5% chance (raro)
            'descricao': 'Produto vira viral (ex: HN front page)',
            'efeito': {
                'fator_visitas_organicas_por_pagante': 10.0,  # 10x viralidade por 3 meses
                'duracao_meses': 3,
            }
        }
    },
    
    # ------------------------------------------------------------------------
    # KPIS A CALCULAR (ENTERPRISE GRADE)
    # ------------------------------------------------------------------------
    'kpis': {
        # KPIs Básicos (já no motor)
        'basicos': [
            'mrr_final', 'arr_final', 'usuarios_final', 'caixa_final',
            'cac_medio', 'ltv_medio', 'churn_medio', 'margem_bruta_media',
            'ebitda_margin_media', 'runway_final'
        ],
        
        # KPIs Avançados (requer cálculo adicional)
        'avancados': [
            'nrr',           # Net Revenue Retention
            'grr',           # Gross Revenue Retention
            'cohort_m6',     # Retenção da cohort do mês 6 após 6 meses
            'payback_meses', # Payback médio
            'roi_total',     # ROI acumulado
            'burn_rate_medio',
            'prob_quebra',   # Probabilidade de caixa < 0
            'var95_caixa',   # Value at Risk (95%)
            'cvar95_caixa',  # Conditional VaR
        ],
        
        # Análise de Risco
        'risco': {
            'caixa_minimo_critico': -5000,      # Threshold de quebra
            'runway_minimo_alerta': 3,          # Runway < 3 meses = alerta
            'churn_critico': 0.15,              # Churn > 15% = crítico
            'ltv_cac_minimo': 1.0,              # LTV/CAC < 1 = insustentável
        }
    },
    
    # ------------------------------------------------------------------------
    # VALIDAÇÃO PRÉ-EXECUÇÃO
    # ------------------------------------------------------------------------
    'validacao': {
        'rodar_teste_previo': True,        # Testa 1 sim antes de rodar tudo
        'timeout_teste': 30,                # Timeout do teste (segundos)
        'abort_se_teste_falhar': True,     # Aborta MC se teste falhar
    },
    
    # ------------------------------------------------------------------------
    # OUTPUT & RELATÓRIOS
    # ------------------------------------------------------------------------
    'output': {
        'salvar_checkpoint': True,
        'salvar_csv': True,                # Exporta CSV além de pickle
        'salvar_resumo_txt': True,         # Relatório em texto puro
        'nivel_detalhe': 'completo',       # 'basico', 'intermediario', 'completo'
    }
}

# Atualiza variáveis antigas para compatibilidade (deprecated)
PREMISSAS['mc_n_simulacoes'] = PREMISSAS['monte_carlo']['n_simulacoes']
PREMISSAS['mc_std_churn'] = PREMISSAS['monte_carlo']['variaveis']['churn_inicial']['std']
PREMISSAS['mc_std_trial_pag'] = PREMISSAS['monte_carlo']['variaveis']['taxa_trial_para_pagante']['std']
PREMISSAS['mc_std_marketing'] = PREMISSAS['monte_carlo']['variaveis']['marketing_fixo_mensal']['std']
PREMISSAS['mc_prob_atraso_aporte'] = PREMISSAS['monte_carlo']['choques']['atraso_aporte']['probabilidade']

print("\n" + "="*80)
print("🎲 CONFIGURAÇÃO MONTE CARLO CARREGADA")
print("="*80)
print(f"   • Simulações por cenário: {PREMISSAS['monte_carlo']['n_simulacoes']}")
print(f"   • Cenários ativos: {len([k for k,v in PREMISSAS['monte_carlo']['cenarios'].items() if PREMISSAS['monte_carlo']['enable_scenarios'] or k=='base'])}")
print(f"   • Variáveis estocásticas: {len(PREMISSAS['monte_carlo']['variaveis'])}")
print(f"   • Correlações definidas: {len(PREMISSAS['monte_carlo']['correlacoes'])}")
print(f"   • KPIs a calcular: {len(PREMISSAS['monte_carlo']['kpis']['basicos']) + len(PREMISSAS['monte_carlo']['kpis']['avancados'])}")
print("="*80)