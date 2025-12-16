# PÁGINA 5 - RISCO & CENÁRIOS (V1.0 - GOLD STANDARD - FASE 1)
# ============================================================================
# DATA: 2025-12-09
# OBJETIVO: Quantificar risco, provar robustez, vender proteção de downside
# PADRÃO: McKinsey-Grade, PDF First, Zero Hardcoded.
#
# ESTRUTURA NARRATIVA (5 ATOS):
# VIZ 5.1: TABELA EXECUTIVA MASTER + KPI CARDS (Fase 1 - Esta versão)
# VIZ 5.2: Monte Carlo Fan Chart (Tese Macro) - Fase 2
# VIZ 5.3: Tornado Plot Sensibilidade (Saúde Unitária) - Fase 2
# VIZ 5.4: Heatmap Runway Semanal (Tático) - Fase 3
# VIZ 5.5: Break-Even sob Estresse (Escala) - Fase 3
# VIZ 5.6: Gap Analysis Real vs Estresse (Vazamento) - Fase 4
#
# FILOSOFIA:
# - Mundo A (Real/5A): Cenário conservador (bootstrap R$ 2k/mês)
# - Mundo B (Ideal/5B): Cenário benchmark (mercado elite)
# - Mundo C (Estresse/5C): Cenário catastrófico (cisne negro)
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Setup de ambiente
import sys
import os
try:
    from IPython.display import display, Markdown, HTML
except ImportError:
    display = print
    Markdown = str
    HTML = str

# Import Utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from celula_0_utils import (
        setup_plot_style, formata_moeda, formata_pct,
        render_atomic_block, salvar_figura_silencioso
    )
except ImportError:
    # Fallback para desenvolvimento
    def formata_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    def formata_pct(valor):
        return f"{valor*100:.1f}%"

# Import Motor (Fallback Robusto para Ato 2)
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from celula_4_motor import executar_motor_fintech_v10_production_ready
except ImportError:
    executar_motor_fintech_v10_production_ready = None

try:
    setup_plot_style()
except:
    pass


class RiskPageOutput:
    """Wrapper para output da Página 5 para evitar poluição visual no notebook."""
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"<RiskPageOutput: {list(self.data.keys())}>"
    def __getitem__(self, key):
        return self.data[key]
    def keys(self):
        return self.data.keys()


# ============================================================================
# SEÇÃO 1: GERADOR DE CENÁRIO ESTRESSE (5C)
# ============================================================================

def gerar_cenario_estresse(df_real_m, premissas, motor_func=None):
    """
    Gera o cenário de estresse (Mundo C) aplicando multiplicadores adversos.
    
    ESTRATÉGIA:
    1. Se PREMISSAS['monte_carlo']['cenarios']['pessimista'] existir, usa como base
    2. Amplifica os multiplicadores pessimistas × 2 para criar estresse máximo
    3. Se motor_func disponível, roda o motor completo
    4. Senão, aplica aproximação no df_real_m
    
    INPUTS:
        df_real_m: DataFrame do cenário Real (36 meses)
        premissas: Dicionário PREMISSAS (deve conter 'monte_carlo' com cenários)
        motor_func: Função do motor (opcional, para recálculo completo)
    
    OUTPUTS:
        df_stress_m: DataFrame do cenário Estresse (36 meses)
    """
    
    # 1. BUSCAR MULTIPLICADORES DO MC CONFIG (ZERO HARDCODING)
    mc_config = premissas.get('monte_carlo', {})
    cenario_pessimista = mc_config.get('cenarios', {}).get('pessimista', {})
    multiplicadores_base = cenario_pessimista.get('multiplicadores', {})
    
    # 2. AMPLIFICAR PARA ESTRESSE MÁXIMO (pessimista × fator de amplificação)
    # Fator 2.0 transforma pessimista em estresse extremo
    FATOR_AMPLIFICACAO = 2.0
    
    # Construir multiplicadores de estresse dinamicamente
    MULTIPLICADORES_ESTRESSE = {}
    
    # Churn: usa do MC ou fallback
    churn_mult = multiplicadores_base.get('churn_inicial', 1.25)
    MULTIPLICADORES_ESTRESSE['churn'] = 1 + (churn_mult - 1) * FATOR_AMPLIFICACAO  # 1.25 → 1.50
    
    # Conversão: usa do MC ou fallback
    conv_mult = multiplicadores_base.get('taxa_trial_para_pagante', 0.75)
    MULTIPLICADORES_ESTRESSE['conversao'] = 1 - (1 - conv_mult) * FATOR_AMPLIFICACAO  # 0.75 → 0.50
    
    # Marketing/CAC: usa do MC ou fallback
    mkt_mult = multiplicadores_base.get('marketing_fixo_mensal', 0.70)
    MULTIPLICADORES_ESTRESSE['marketing'] = mkt_mult  # Mantém original (corte de budget no estresse)
    
    # CPC (afeta CAC indiretamente): usa média dos CPCs ou fallback
    cpc_mults = [
        multiplicadores_base.get('cpc_instagram', 1.25),
        multiplicadores_base.get('cpc_facebook', 1.25),
        multiplicadores_base.get('cpc_google', 1.25),
        multiplicadores_base.get('cpc_youtube', 1.25)
    ]
    cpc_medio = sum(cpc_mults) / len(cpc_mults)
    MULTIPLICADORES_ESTRESSE['cac'] = 1 + (cpc_medio - 1) * FATOR_AMPLIFICACAO  # 1.25 → 1.50
    
    # Tráfego e ARPU: derivados
    MULTIPLICADORES_ESTRESSE['trafego'] = 1 - 0.30  # -30% tráfego (padrão estresse)
    MULTIPLICADORES_ESTRESSE['arpu'] = 1 - 0.20      # -20% ARPU (clientes piores)
    
    if motor_func is not None:
        # Caminho completo: rodar o motor com premissas modificadas
        premissas_stress = premissas.copy()
        
        # Aplicar multiplicadores nas premissas corretas
        premissas_stress['churn_inicial'] = premissas.get('churn_inicial', 0.12) * MULTIPLICADORES_ESTRESSE['churn']
        premissas_stress['taxa_trial_para_pagante'] = premissas.get('taxa_trial_para_pagante', 0.12) * MULTIPLICADORES_ESTRESSE['conversao']
        premissas_stress['marketing_fixo_mensal'] = premissas.get('marketing_fixo_mensal', 2000) * MULTIPLICADORES_ESTRESSE['marketing']
        premissas_stress['trafego_inicial'] = premissas.get('trafego_inicial', 300) * MULTIPLICADORES_ESTRESSE['trafego']
        
        # Aplicar CPC aumentado (afeta CAC)
        for canal in ['cpc_instagram', 'cpc_facebook', 'cpc_google', 'cpc_youtube']:
            if canal in premissas_stress:
                premissas_stress[canal] = premissas.get(canal, 1.0) * MULTIPLICADORES_ESTRESSE['cac']
        
        try:
            df_stress_m, _, _, _ = motor_func(premissas_stress)
            return df_stress_m
        except Exception as e:
            print(f"⚠️ Erro ao rodar motor para estresse: {e}. Usando aproximação simplificada.")

    
    # Caminho simplificado: aplicar multiplicadores diretamente (aproximação)
    df_stress = df_real_m.copy()
    
    # Fator de impacto acumulado pelo estresse
    fator_estresse = 0.6  # Estresse reduz performance em 40%
    
    # Ajustar métricas de retenção/churn
    if 'churn_rate' in df_stress.columns:
        df_stress['churn_rate'] = df_stress['churn_rate'] * MULTIPLICADORES_ESTRESSE['churn']
        df_stress['churn_rate'] = df_stress['churn_rate'].clip(upper=0.30)  # Cap em 30%
    if 'churn' in df_stress.columns:
        df_stress['churn'] = df_stress['churn'] * MULTIPLICADORES_ESTRESSE['churn']
        df_stress['churn'] = df_stress['churn'].clip(upper=0.30)
    
    # Ajustar CAC
    if 'cac_blended' in df_stress.columns:
        df_stress['cac_blended'] = df_stress['cac_blended'] * MULTIPLICADORES_ESTRESSE['cac']
    if 'cac' in df_stress.columns:
        df_stress['cac'] = df_stress['cac'] * MULTIPLICADORES_ESTRESSE['cac']
    
    # Ajustar ARPU/Receita
    if 'arpu' in df_stress.columns:
        df_stress['arpu'] = df_stress['arpu'] * MULTIPLICADORES_ESTRESSE['arpu']
    
    # Recalcular métricas de receita
    if 'mrr' in df_stress.columns:
        df_stress['mrr'] = df_stress['mrr'] * fator_estresse
        df_stress['arr'] = df_stress['mrr'] * 12 if 'arr' in df_stress.columns else df_stress['mrr'] * 12
    
    if 'receita_liquida' in df_stress.columns:
        df_stress['receita_liquida'] = df_stress['receita_liquida'] * fator_estresse
    if 'receita_bruta' in df_stress.columns:
        df_stress['receita_bruta'] = df_stress['receita_bruta'] * fator_estresse
    if 'receita_mensal' in df_stress.columns:
        df_stress['receita_mensal'] = df_stress['receita_mensal'] * fator_estresse
    
    # Ajustar usuários (churn maior = menos usuários)
    if 'usuarios_ativos' in df_stress.columns:
        df_stress['usuarios_ativos'] = (df_stress['usuarios_ativos'] * fator_estresse).astype(int)
    if 'usuarios' in df_stress.columns:
        df_stress['usuarios'] = (df_stress['usuarios'] * fator_estresse).astype(int)
    if 'usuarios_pagos' in df_stress.columns:
        df_stress['usuarios_pagos'] = (df_stress['usuarios_pagos'] * fator_estresse).astype(int)
    
    # Aumentar custos (CAC maior = mais gasto)
    if 'gasto_marketing' in df_stress.columns:
        df_stress['gasto_marketing'] = df_stress['gasto_marketing'] * MULTIPLICADORES_ESTRESSE['cac']
    if 'total_opex' in df_stress.columns:
        df_stress['total_opex'] = df_stress['total_opex'] * 1.2  # 20% mais custos
    
    # Caixa: impacto combinado (menos receita + mais custo)
    if 'caixa' in df_stress.columns:
        # Degradação progressiva: começa igual mas termina 50% pior
        n_meses = len(df_stress)
        degradacao = np.linspace(0.95, 0.50, n_meses)  # De 95% até 50%
        df_stress['caixa'] = df_stress['caixa'] * degradacao
    
    # Recalcular LTV/CAC
    if 'ltv' in df_stress.columns:
        df_stress['ltv'] = df_stress['ltv'] * fator_estresse
    if 'ltv_cac' in df_stress.columns:
        df_stress['ltv_cac'] = df_stress['ltv_cac'] * fator_estresse
    
    # Recalcular runway se existir
    if 'runway_meses' in df_stress.columns and 'burn_rate' in df_stress.columns:
        # Burn rate aumenta no estresse
        df_stress['burn_rate'] = df_stress['burn_rate'] * 1.3
        # Runway diminui
        df_stress['runway_meses'] = df_stress['caixa'] / df_stress['burn_rate'].replace(0, 1)
        df_stress['runway_meses'] = df_stress['runway_meses'].clip(lower=0, upper=36)
        
    # =========================================================================
    # CORREÇÃO CRÍTICA (V7.7): RECALCULAR LUCROS
    # =========================================================================
    # Como alteramos Receita e Opex independentemente, precisamos forçar 
    # a consistência contábil do Lucro Líquido e EBITDA.
    if 'receita_liquida' in df_stress.columns and 'total_opex' in df_stress.columns:
        df_stress['lucro_liquido'] = df_stress['receita_liquida'] - df_stress['total_opex']
        
    if 'receita_bruta' in df_stress.columns and 'custos_totais' in df_stress.columns:
        # Se tiver CMV separado, use. Senão aproxima.
        pass
        
    # Recalcula EBITDA se possível (ou ajusta proporcionalmente ao lucro)
    if 'ebitda' in df_stress.columns and 'lucro_liquido' in df_stress.columns:
        # Mantém o delta original entre EBITDA e Lucro (Impostos/Depreciação/Juros)
        delta_fin = df_real_m['ebitda'] - df_real_m['lucro_liquido']
        df_stress['ebitda'] = df_stress['lucro_liquido'] + delta_fin

    return df_stress



# ============================================================================
# SEÇÃO 2: TABELA EXECUTIVA MASTER DE RISCO
# ============================================================================

def gerar_tabela_executiva_risco(df_real_m, df_ideal_m, mc_results, df_stress_m, premissas=None):
    """
    Gera a Tabela Executiva Master de Risco (25 métricas organizadas).
    
    INPUTS:
        df_real_m: Cenário Real mensal (36 linhas)
        df_ideal_m: Cenário Ideal mensal (36 linhas)
        mc_results: Resultados Monte Carlo (DataFrame com 10k+ sims)
        df_stress_m: Cenário Estresse mensal (36 linhas)
        premissas: Dicionário PREMISSAS (opcional, para benchmarks)
    
    OUTPUT:
        DataFrame formatado com 25 métricas de risco
    """
    
    # Extrair dados finais (M36 ou último mês disponível)
    real_final = df_real_m.iloc[-1]
    ideal_final = df_ideal_m.iloc[-1]
    stress_final = df_stress_m.iloc[-1]
    
    # Extrair colunas de MC (com fallback para nomes alternativos)
    def get_mc_col(df, options, default=0):
        for col in options:
            if col in df.columns:
                return df[col]
        return pd.Series([default] * len(df))
    
    caixa_final_mc = get_mc_col(mc_results, ['caixa_final', 'caixa', 'cash_final'])
    arr_final_mc = get_mc_col(mc_results, ['arr_final', 'arr'])
    ltv_cac_mc = get_mc_col(mc_results, ['ltv_cac_final', 'ltv_cac', 'ltv_cac_medio'])
    churn_mc = get_mc_col(mc_results, ['churn_medio', 'churn_final', 'churn'])
    
    # Calcular percentis do Monte Carlo
    p5 = caixa_final_mc.quantile(0.05)
    p50 = caixa_final_mc.quantile(0.50)
    p95 = caixa_final_mc.quantile(0.95)
    var95 = p5  # Value at Risk (pior 5%)
    
    # CVaR com tratamento de divisão por zero
    cvar_mask = caixa_final_mc < var95
    cvar95 = caixa_final_mc[cvar_mask].mean() if cvar_mask.sum() > 0 else var95
    
    # Probabilidades
    n_sims = len(mc_results)
    prob_quebra = (caixa_final_mc < 0).sum() / n_sims if n_sims > 0 else 0
    prob_caixa_50k = (caixa_final_mc < 50000).sum() / n_sims if n_sims > 0 else 0
    prob_caixa_100k = (caixa_final_mc > 100000).sum() / n_sims if n_sims > 0 else 0
    prob_arr_1m = (arr_final_mc > 1000000).sum() / n_sims if n_sims > 0 else 0
    prob_ltv_cac_5x = (ltv_cac_mc > 5).sum() / n_sims if n_sims > 0 else 0
    prob_churn_5 = (churn_mc < 0.05).sum() / n_sims if n_sims > 0 else 0
    
    # Extrair valores dos DataFrames com chaves seguras
    def safe_get(series, keys, default=0):
        for key in keys:
            if key in series.index:
                val = series[key]
                if pd.notna(val) and not np.isinf(val):
                    return val
        return default
    
    # Construir dados da tabela
    dados_tabela = [
        # PROBABILIDADES
        {'Categoria': '🎲 PROBABILIDADES', 'Métrica': '', 'Real': '', 'Ideal': '', 'Estresse': '', 'Benchmark': '', 'Status': ''},
        {'Categoria': '', 'Métrica': 'Prob. Quebra (Caixa < R$ 0)', 'Real': f'{prob_quebra:.1%}', 'Ideal': '', 'Estresse': '', 'Benchmark': '< 10%', 'Status': '🟢' if prob_quebra < 0.10 else '🔴'},
        {'Categoria': '', 'Métrica': 'Prob. Caixa < R$ 50k', 'Real': f'{prob_caixa_50k:.1%}', 'Ideal': '', 'Estresse': '', 'Benchmark': '< 20%', 'Status': '🟢' if prob_caixa_50k < 0.20 else '🔴'},
        {'Categoria': '', 'Métrica': 'Prob. Caixa > R$ 100k', 'Real': f'{prob_caixa_100k:.1%}', 'Ideal': '', 'Estresse': '', 'Benchmark': '> 50%', 'Status': '🟢' if prob_caixa_100k > 0.50 else '🔴'},
        {'Categoria': '', 'Métrica': 'Prob. ARR > R$ 1M', 'Real': f'{prob_arr_1m:.1%}', 'Ideal': '', 'Estresse': '', 'Benchmark': '> 60%', 'Status': '🟢' if prob_arr_1m > 0.60 else '🟡'},
        {'Categoria': '', 'Métrica': 'Prob. LTV/CAC > 5x', 'Real': f'{prob_ltv_cac_5x:.1%}', 'Ideal': '', 'Estresse': '', 'Benchmark': '> 30%', 'Status': '🟢' if prob_ltv_cac_5x > 0.30 else '🟡'},
        
        # CENÁRIO REAL
        {'Categoria': '💰 CENÁRIO REAL (5A)', 'Métrica': '', 'Real': '', 'Ideal': '', 'Estresse': '', 'Benchmark': '', 'Status': ''},
        {'Categoria': '', 'Métrica': 'Caixa Final', 'Real': formata_moeda(safe_get(real_final, ['caixa', 'caixa_acumulado'])), 'Ideal': '', 'Estresse': '', 'Benchmark': '> R$ 50k', 'Status': '🟢' if safe_get(real_final, ['caixa']) > 50000 else '🟡'},
        {'Categoria': '', 'Métrica': 'ARR Final', 'Real': formata_moeda(safe_get(real_final, ['arr'])), 'Ideal': '', 'Estresse': '', 'Benchmark': '> R$ 1M', 'Status': '🟢' if safe_get(real_final, ['arr']) > 1000000 else '🟡'},
        {'Categoria': '', 'Métrica': 'MRR Final', 'Real': formata_moeda(safe_get(real_final, ['mrr'])), 'Ideal': '', 'Estresse': '', 'Benchmark': '> R$ 50k', 'Status': '🟢' if safe_get(real_final, ['mrr']) > 50000 else '🟡'},
        {'Categoria': '', 'Métrica': 'LTV/CAC', 'Real': f"{safe_get(real_final, ['ltv_cac'], 0):.1f}x" if safe_get(real_final, ['ltv_cac'], 0) > 0 else f"{safe_get(real_final, ['ltv'], 0) / max(safe_get(real_final, ['cac_blended'], 1), 1):.1f}x", 'Ideal': '', 'Estresse': '', 'Benchmark': '> 3.0x', 'Status': '🟢'},
        
        # CENÁRIO IDEAL
        {'Categoria': '🌟 CENÁRIO IDEAL (5B)', 'Métrica': '', 'Real': '', 'Ideal': '', 'Estresse': '', 'Benchmark': '', 'Status': ''},
        {'Categoria': '', 'Métrica': 'Caixa Final', 'Real': '', 'Ideal': formata_moeda(safe_get(ideal_final, ['caixa', 'caixa_acumulado'])), 'Estresse': '', 'Benchmark': '> R$ 100k', 'Status': '🟢'},
        {'Categoria': '', 'Métrica': 'ARR Final', 'Real': '', 'Ideal': formata_moeda(safe_get(ideal_final, ['arr'])), 'Estresse': '', 'Benchmark': '> R$ 1.5M', 'Status': '🟢'},
        
        # CENÁRIO ESTRESSE
        {'Categoria': '⚠️ CENÁRIO ESTRESSE (5C)', 'Métrica': '', 'Real': '', 'Ideal': '', 'Estresse': '', 'Benchmark': '', 'Status': ''},
        {'Categoria': '', 'Métrica': 'Caixa Final', 'Real': '', 'Ideal': '', 'Estresse': formata_moeda(safe_get(stress_final, ['caixa', 'caixa_acumulado'])), 'Benchmark': 'N/A', 'Status': '🔴' if safe_get(stress_final, ['caixa']) < 0 else '🟡'},
        {'Categoria': '', 'Métrica': 'ARR Final', 'Real': '', 'Ideal': '', 'Estresse': formata_moeda(safe_get(stress_final, ['arr'])), 'Benchmark': 'N/A', 'Status': '🔴'},
        
        # MONTE CARLO
        {'Categoria': '📊 MONTE CARLO', 'Métrica': '', 'Real': '', 'Ideal': '', 'Estresse': '', 'Benchmark': '', 'Status': ''},
        {'Categoria': '', 'Métrica': 'VaR 95% (Pior 5%)', 'Real': formata_moeda(var95), 'Ideal': '', 'Estresse': '', 'Benchmark': '> -R$ 50k', 'Status': '🟢' if var95 > -50000 else '🔴'},
        {'Categoria': '', 'Métrica': 'CVaR 95%', 'Real': formata_moeda(cvar95), 'Ideal': '', 'Estresse': '', 'Benchmark': '> -R$ 100k', 'Status': '🟢' if cvar95 > -100000 else '🔴'},
        {'Categoria': '', 'Métrica': 'P50 (Mediana)', 'Real': formata_moeda(p50), 'Ideal': '', 'Estresse': '', 'Benchmark': '> R$ 50k', 'Status': '🟢' if p50 > 50000 else '🟡'},
        {'Categoria': '', 'Métrica': 'Dispersão (P95-P5)', 'Real': formata_moeda(p95 - p5), 'Ideal': '', 'Estresse': '', 'Benchmark': '< R$ 200k', 'Status': '🟢' if (p95-p5) < 200000 else '🟡'},
    ]
    
    df_tabela = pd.DataFrame(dados_tabela)
    
    return df_tabela


# ============================================================================
# SEÇÃO 3: KPI CARDS DE RISCO (4 Cards Hero)
# ============================================================================

def gerar_kpi_cards_risco(mc_results, df_real_m):
    """
    Gera os 4 KPI Cards hero de risco.
    
    RETURNS:
        List de dicts com: titulo, valor, subtitulo, delta, status
    """
    
    # Extrair colunas com fallback
    caixa_final = mc_results.get('caixa_final', mc_results.get('caixa', pd.Series([0])))
    
    # Card 1: Probabilidade de Sobrevivência
    prob_sobrevivencia = (caixa_final > 0).mean()
    card1 = {
        'titulo': '🛡️ SOBREVIVÊNCIA',
        'valor': f'{prob_sobrevivencia:.1%}',
        'subtitulo': 'Prob. Caixa > R$ 0',
        'delta': f'+{(prob_sobrevivencia - 0.90):.1%} vs meta 90%' if prob_sobrevivencia > 0.90 else f'{(prob_sobrevivencia - 0.90):.1%} vs meta 90%',
        'status': '🟢' if prob_sobrevivencia > 0.90 else '🔴'
    }
    
    # Card 2: VaR 95%
    var95 = caixa_final.quantile(0.05)
    card2 = {
        'titulo': '⚠️ VAR 95%',
        'valor': formata_moeda(var95),
        'subtitulo': 'Pior Cenário (5%)',
        'delta': f'{abs(var95)/1000:.0f}k vs limite -50k',
        'status': '🟢' if var95 > -50000 else '🔴'
    }
    
    # Card 3: Upside Potential
    p95 = caixa_final.quantile(0.95)
    p50 = caixa_final.quantile(0.50)
    upside = (p95 / max(p50, 1)) - 1
    card3 = {
        'titulo': '🚀 UPSIDE',
        'valor': f'{upside:.0%}',
        'subtitulo': 'P95 vs P50',
        'delta': f'{upside:.0%} potencial acima mediana',
        'status': '🟢' if upside > 1.0 else '🟡'
    }
    
    # Card 4: Dispersão (Incerteza)
    p5 = caixa_final.quantile(0.05)
    dispersao = (p95 - p5) / max(abs(p50), 1)
    card4 = {
        'titulo': '📊 DISPERSÃO',
        'valor': f'{dispersao:.1f}x',
        'subtitulo': 'Incerteza (P95-P5)/P50',
        'delta': 'Alta incerteza' if dispersao > 3 else 'Incerteza controlada',
        'status': '🟡' if dispersao > 3 else '🟢'
    }
    
    return [card1, card2, card3, card4]


# ============================================================================
# SEÇÃO 4: ATO 1 - MONTE CARLO FAN CHART (TESE MACRO)
# ============================================================================

def preparar_dados_fan_chart(mc_results, df_real_m, df_ideal_m):
    """
    Prepara os percentis para o Fan Chart.
    
    VERSÃO V2.0 - GOLD STANDARD:
    Prioridade 1: Usar 'caixa_series' (série temporal real de cada simulação)
    Prioridade 2: Usar formato 'mes'/'caixa' (cada linha = 1 mês de 1 sim)
    Prioridade 3: Fallback para interpolação (último recurso)
    
    OUTPUT:
        DataFrame com colunas: mes, p5, p10, p25, p50, p75, p90, p95, real, ideal
    """
    
    # ==========================================================================
    # PRIORIDADE 1: caixa_series (IDEAL - séries temporais reais do MC)
    # ==========================================================================
    if 'caixa_series' in mc_results.columns:
        try:
            # Converter lista de séries para matriz numpy
            # Cada linha é uma simulação, cada coluna é um mês
            series_list = mc_results['caixa_series'].tolist()
            
            # Filtrar séries válidas (não vazias e com tamanho correto)
            valid_series = [s for s in series_list if isinstance(s, (list, np.ndarray)) and len(s) > 0]
            
            if len(valid_series) > 10:  # Mínimo de simulações para estatística válida
                series_matrix = np.array(valid_series)
                n_meses = series_matrix.shape[1]
                
                # Calcular percentis REAIS por mês (axis=0 = ao longo das simulações)
                percentis = pd.DataFrame({
                    'mes': np.arange(1, n_meses + 1),
                    'p5': np.percentile(series_matrix, 5, axis=0),
                    'p10': np.percentile(series_matrix, 10, axis=0),
                    'p25': np.percentile(series_matrix, 25, axis=0),
                    'p50': np.percentile(series_matrix, 50, axis=0),
                    'p75': np.percentile(series_matrix, 75, axis=0),
                    'p90': np.percentile(series_matrix, 90, axis=0),
                    'p95': np.percentile(series_matrix, 95, axis=0),
                })
                
                # Adicionar linhas Real e Ideal
                if len(percentis) == len(df_real_m):
                    percentis['real'] = df_real_m['caixa'].values if 'caixa' in df_real_m.columns else 0
                    percentis['ideal'] = df_ideal_m['caixa'].values if 'caixa' in df_ideal_m.columns else 0
                else:
                    percentis['real'] = np.interp(percentis['mes'], df_real_m['mes'], df_real_m['caixa'])
                    percentis['ideal'] = np.interp(percentis['mes'], df_ideal_m['mes'], df_ideal_m['caixa'])
                
                return percentis
        except Exception as e:
            print(f"⚠️ Erro ao processar caixa_series: {e}. Usando fallback.")
    
    # ==========================================================================
    # PRIORIDADE 2: Formato mes/caixa (cada linha = 1 mês de 1 simulação)
    # ==========================================================================
    if 'mes' in mc_results.columns and 'caixa' in mc_results.columns:
        percentis = mc_results.groupby('mes')['caixa'].quantile(
            [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
        ).unstack()
        percentis.columns = ['p5', 'p10', 'p25', 'p50', 'p75', 'p90', 'p95']
        percentis = percentis.reset_index()
        
        if len(percentis) == len(df_real_m):
            percentis['real'] = df_real_m['caixa'].values if 'caixa' in df_real_m.columns else 0
            percentis['ideal'] = df_ideal_m['caixa'].values if 'caixa' in df_ideal_m.columns else 0
        else:
            percentis['real'] = np.interp(percentis['mes'], df_real_m['mes'], df_real_m['caixa'])
            percentis['ideal'] = np.interp(percentis['mes'], df_ideal_m['mes'], df_ideal_m['caixa'])
        
        return percentis
    
    # ==========================================================================
    # PRIORIDADE 3: Fallback - Interpolação (ÚLTIMO RECURSO)
    # ==========================================================================
    caixa_final_col = 'caixa_final' if 'caixa_final' in mc_results.columns else 'caixa'
    caixa_final = mc_results[caixa_final_col] if caixa_final_col in mc_results.columns else pd.Series([0])
    
    # Calcular percentis finais
    p5_final = caixa_final.quantile(0.05)
    p10_final = caixa_final.quantile(0.10)
    p25_final = caixa_final.quantile(0.25)
    p50_final = caixa_final.quantile(0.50)
    p75_final = caixa_final.quantile(0.75)
    p90_final = caixa_final.quantile(0.90)
    p95_final = caixa_final.quantile(0.95)
    
    # Interpolar linearmente do mês 1 até o final
    meses = df_real_m['mes'].values
    n_meses = len(meses)
    caixa_inicial = df_real_m['caixa'].iloc[0] if 'caixa' in df_real_m.columns else 0
    
    # Gerar faixas que crescem do início até os percentis finais
    percentis = pd.DataFrame({
        'mes': meses,
        'p5': np.linspace(caixa_inicial * 0.8, p5_final, n_meses),
        'p10': np.linspace(caixa_inicial * 0.85, p10_final, n_meses),
        'p25': np.linspace(caixa_inicial * 0.9, p25_final, n_meses),
        'p50': np.linspace(caixa_inicial, p50_final, n_meses),
        'p75': np.linspace(caixa_inicial * 1.1, p75_final, n_meses),
        'p90': np.linspace(caixa_inicial * 1.15, p90_final, n_meses),
        'p95': np.linspace(caixa_inicial * 1.2, p95_final, n_meses),
    })
    
    # Adicionar linhas Real e Ideal
    percentis['real'] = df_real_m['caixa'].values if 'caixa' in df_real_m.columns else 0
    percentis['ideal'] = df_ideal_m['caixa'].values if 'caixa' in df_ideal_m.columns else 0
    
    return percentis


def plotar_fan_chart(dados_fan, report_mode=False, zoom_percentil=90, prob_acima_teto=0):
    """
    Gera o Fan Chart com áreas percentiladas - VERSÃO OTIMIZADA VISUALMENTE.
    
    MUDANÇAS:
    - Eixo Y travado em R$ 800k (teto) para evitar chatamento por outliers.
    - Tabela resumo (P10, P50, P90) embutida no gráfico.
    - Nota explícita sobre a % de cenários acima do teto.
    """
    
    figsize = (10, 5) if report_mode else (12, 7)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    meses = dados_fan['mes'].values
    
    # 1. LIMITES DO EIXO (HARD CAP 800k)
    y_hard_cap = 800000
    y_min = min(dados_fan['p5'].min() * 1.1, -10000)
    
    # CAMADA 1: Área P10-P90 (80% de confiança)
    ax.fill_between(meses, dados_fan['p10'], dados_fan['p90'], 
                    alpha=0.25, color='#BDBDBD', label='P10-P90 (80% cenários)')
    
    # CAMADA 2: Área P25-P75 (50% de confiança)
    ax.fill_between(meses, dados_fan['p25'], dados_fan['p75'], 
                    alpha=0.4, color='#757575', label='P25-P75 (50% mais provável)')
    
    # LINHA CENTRAL: P50 (Mediana)
    ax.plot(meses, dados_fan['p50'], color='#212121', linewidth=3.5, 
            linestyle='-', label='P50 (Mediana)', zorder=5)
    
    # LINHA REAL
    ax.plot(meses, dados_fan['real'], color='#1565C0', linewidth=3, 
            linestyle='-', label='Cenário Real', zorder=6, marker='o', 
            markersize=4, markevery=6)
    
    # LINHA IDEAL
    ax.plot(meses, dados_fan['ideal'], color='#2E7D32', linewidth=3, 
            linestyle='--', label='Cenário Ideal', zorder=6, marker='s', 
            markersize=4, markevery=6)
    
    # QUEBRA (Zero)
    ax.axhline(y=0, color='#D32F2F', linestyle='-', linewidth=2.5, 
               alpha=0.8, label='Quebra (R$ 0)', zorder=4)
    
    # MÊS 6 DECISÃO
    ax.axvline(x=6, color='#FF9800', linestyle='--', linewidth=2, alpha=0.7)
    
    # APLICAR CAP
    ax.set_ylim(y_min, y_hard_cap)
    
    # Formatação
    ax.set_xlabel('Mês', fontsize=11, fontweight='bold')
    ax.set_ylabel('Caixa Acumulado (R$)', fontsize=11, fontweight='bold')
    ax.set_title('Distribuição de Cenários (Monte Carlo)\n' + 
                 'Foco na Zona Operacional (< 800k)', 
                 fontsize=13, color='#333', fontweight='bold', pad=15)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
    ax.grid(True, alpha=0.2, linestyle=':', zorder=0)
    
    # LEGENDA SIMPLIFICADA
    ax.legend(loc='upper left', frameon=True, fontsize=9, ncol=2)
    
    # =========================================================
    # TABELA RESUMO (Top Right)
    # =========================================================
    
    # Dados finais
    v90 = dados_fan['p90'].iloc[-1]
    v50 = dados_fan['p50'].iloc[-1]
    v10 = dados_fan['p10'].iloc[-1]
    
    # Tabela dados
    celul_text = [
        [f'P90 (Otimista)', formata_moeda(v90)],
        [f'P50 (Provável)', formata_moeda(v50)],
        [f'P10 (Pessimista)', formata_moeda(v10)]
    ]
    
    # Adicionar tabela
    the_table = ax.table(cellText=celul_text,
                         colWidths=[0.3, 0.25],
                         loc='upper right',
                         bbox=[0.68, 0.75, 0.30, 0.2]) # [left, bottom, width, height]
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(9)
    the_table.scale(1, 1.3)
    
    # =========================================================
    # NOTA DE OUTLIERS
    # =========================================================
    if prob_acima_teto > 0:
        nota_text = f"⚠️ NOTA: Escala limitada a R$ 800k para visualização.\n{prob_acima_teto:.1%} dos cenários superaram este teto (cauda longa)."
        props = dict(boxstyle='round', facecolor='#FFF3E0', alpha=0.9, edgecolor='#FF9800')
        ax.text(0.98, 0.68, nota_text, transform=ax.transAxes, fontsize=8,
                verticalalignment='top', horizontalalignment='right', bbox=props, color='#E65100')

    plt.tight_layout()
    return fig


def plotar_grafico_mes6(mc_results, df_real_m, df_ideal_m, premissas, report_mode=False):
    """
    Gera gráfico específico para o Mês 6 - ponto de decisão crítica.
    
    Mostra:
    - Histograma da distribuição do caixa no mês 6
    - Linha de decisão (ponto de corte)
    - Probabilidades de cada cenário
    """
    
    # Extrair caixa no mês 6
    if 'mes' in mc_results.columns and 'caixa' in mc_results.columns:
        caixa_mes6 = mc_results[mc_results['mes'] == 6]['caixa']
    else:
        # Aproximação: interpolar do caixa_final
        caixa_final_col = 'caixa_final' if 'caixa_final' in mc_results.columns else 'caixa'
        caixa_final = mc_results[caixa_final_col] if caixa_final_col in mc_results.columns else pd.Series([0])
        # Mês 6 ≈ 16.7% do caminho até mês 36
        fator_mes6 = 6 / 36
        caixa_inicial = df_real_m['caixa'].iloc[0] if 'caixa' in df_real_m.columns else 0
        caixa_mes6 = caixa_inicial + (caixa_final - caixa_inicial) * fator_mes6 * (1 + np.random.normal(0, 0.1, len(caixa_final)))
    
    # Caixa real no mês 6
    if len(df_real_m) > 5:
        caixa_real_m6 = df_real_m['caixa'].iloc[5] if 'caixa' in df_real_m.columns else 0
        caixa_ideal_m6 = df_ideal_m['caixa'].iloc[5] if 'caixa' in df_ideal_m.columns else 0
    else:
        caixa_real_m6 = 0
        caixa_ideal_m6 = 0
    
    # DEPENDÊNCIA: Garantir import do KDE
    from scipy.stats import gaussian_kde
    
    # Criar figura
    figsize = (10, 5) if report_mode else (12, 7)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Gerar KDE (Densidade)
    # -------------------------------------------------------------------------
    density = gaussian_kde(caixa_mes6)
    
    # Definir range do eixo X para o cálculo da curva (de min a max com margem)
    xs = np.linspace(min(caixa_mes6.min(), -20000), max(caixa_mes6.max(), 100000), 1000)
    ys = density(xs)
    
    # Plotar linha de densidade
    ax.plot(xs, ys, color='#1565C0', linewidth=2.5, label='Densidade de Probabilidade')
    
    # Preencher área (Area Chart Style) com degradê simulado (transparência)
    ax.fill_between(xs, ys, alpha=0.2, color='#90CAF9')
    
    # LIMITES E ZOOM (Foco 0-100k)
    # -------------------------------------------------------------------------
    x_min_zoom = -30000  # Um pouco negativo para ver a quebra
    x_max_zoom = 100000  # Cap em 100k
    ax.set_xlim(x_min_zoom, x_max_zoom)
    
    # Calcular % acima do teto para nota
    pct_acima_100k = (caixa_mes6 > 100000).mean()
    
    # Linhas de referência verticais
    ax.axvline(x=0, color='#D32F2F', linestyle='-', linewidth=2.5, label='Quebra (R$ 0)')
    
    # Ponto Real e Ideal (se estiverem dentro do zoom)
    if caixa_real_m6 < x_max_zoom:
        ax.axvline(x=caixa_real_m6, color='#1565C0', linestyle='--', linewidth=2, 
                   label=f'Real: {formata_moeda(caixa_real_m6)}')
    
    if caixa_ideal_m6 < x_max_zoom:
        ax.axvline(x=caixa_ideal_m6, color='#2E7D32', linestyle='--', linewidth=2, 
                   label=f'Ideal: {formata_moeda(caixa_ideal_m6)}')
        
    # Mediana
    p50 = np.percentile(caixa_mes6, 50)
    if p50 < x_max_zoom:
        ax.axvline(x=p50, color='#212121', linestyle='-', linewidth=2, label=f'Mediana: {formata_moeda(p50)}')

    # Probabilidades
    prob_quebra = (caixa_mes6 < 0).mean()
    prob_risco = ((caixa_mes6 >= 0) & (caixa_mes6 < 10000)).mean()
    prob_seguro = (caixa_mes6 >= 10000).mean()
    p25 = np.percentile(caixa_mes6, 25)
    p75 = np.percentile(caixa_mes6, 75)
    
    # Caixa de texto simplificada (Top Right)
    textstr = f'📊 Zonas de Risco (M6):\n' \
              f'🔴 Quebra (<0): {prob_quebra:.1%}\n' \
              f'🟠 Risco (0-10k): {prob_risco:.1%}\n' \
              f'🟢 Seguro (>10k): {prob_seguro:.1%}'
    
    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95, edgecolor='#CCC')
    ax.text(0.97, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Nota de Outlier (> 100k)
    if pct_acima_100k > 0:
        nota_text = f"⚠️ ZOOM ATIVADO: {pct_acima_100k:.1%} dos cenários estão acima de R$ 100k (não mostrados)."
        props_nota = dict(boxstyle='round', facecolor='#E3F2FD', alpha=0.9, edgecolor='#2196F3')
        ax.text(0.02, 0.95, nota_text, transform=ax.transAxes, fontsize=8,
                verticalalignment='top', horizontalalignment='left', bbox=props_nota, color='#0D47A1')
    
    # Formatação
    ax.set_xlabel('Caixa no Mês 6 (R$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Densidade de Probabilidade', fontsize=11, fontweight='bold')
    ax.set_title('Decisão Crítica Mês 6: Distribuição de Probabilidade\n' + 
                 'Foco na Zona de Risco (-20k a 100k)', 
                 fontsize=13, color='#333', fontweight='bold', pad=15)
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
    ax.yaxis.set_visible(False) # Ocultar eixo Y (densidade pura não é intuitiva)
    
    ax.grid(True, alpha=0.2, linestyle=':', axis='x')
    
    # Legenda limpa
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.75), frameon=False, fontsize=9)
    
    plt.tight_layout()
    
    return fig, {
        'prob_quebra_m6': prob_quebra,
        'prob_risco_m6': prob_risco,
        'prob_seguro_m6': prob_seguro,
        'p25_m6': p25,
        'p50_m6': p50,
        'p75_m6': p75,
        'caixa_real_m6': caixa_real_m6,
        'caixa_ideal_m6': caixa_ideal_m6
    }
    
    
# ============================================================================
# SEÇÃO 4.5: ATO 2 - TORNADO PLOT (SENSIBILIDADE)
# ============================================================================



# ============================================================================
# SEÇÃO 4.5: ATO 2 - TORNADO PLOT (SENSIBILIDADE)
# ============================================================================

def calcular_sensibilidade_ltv_cac(PREMISSAS, premissas_sensiveis, variacao=0.20, motor_func=None, ltv_cac_base_real=None):
    """
    Calcula o impacto de cada premissa no LTV/CAC (V3 - GOLD STANDARD).
    
    Diferenciais da V3:
    1. ZERO HARDCODED: Aceita lista de premissas dinâmica.
    2. MOTOR ROBUSTO: Se motor_func não for passado, tenta usar o import global.
    3. FAIL-SAFE: Se motor falhar, captura erro mas não quebra tudo.
    4. BASE REAL: Usa o LTV/CAC do cenário atual se passado (evita re-simulação e divergência).
    """

    # --- SANITIZAÇÃO DE MARKETING ---
    # Se o budget fixo for zero, assumimos que a estratégia é orgânica pura.
    # Forçamos as variáveis percentuais a zero para impedir que o motor gaste dinheiro automaticamente.
    if PREMISSAS.get('marketing_fixo_mensal', 0) == 0:
        PREMISSAS['marketing_perc_receita'] = 0.0
        PREMISSAS['marketing_teto'] = 0.0
    # --------------------------------
    
    # Validação do Motor
    motor_para_usar = motor_func
    if motor_para_usar is None:
        if 'executar_motor_fintech_v10_production_ready' in globals() and executar_motor_fintech_v10_production_ready is not None:
             motor_para_usar = executar_motor_fintech_v10_production_ready
        else:
            print("⚠️ ERRO CRÍTICO: Motor Financeiro não disponível para análise de sensibilidade.")
            print("   Verifique se 'celula_4_motor.py' está no path ou passe motor_func.")
            return pd.DataFrame()

    def get_ltv_cac(p):
        """
        Executa o motor e extrai LTV/CAC médio.
        
        FIX V2: Usa a MÉDIA de LTV/CAC (metricas['ltv_cac_medio']) em vez do valor do mês 36.
        Isso captura melhor a sensibilidade a parâmetros que decaem (como churn_inicial),
        porque o churn no mês 36 já convergiu para churn_maturidade, mascarando o efeito.
        """
        try:
            # Rodar motor
            df_m, _, metricas, _ = motor_para_usar(p)
            
            if len(df_m) > 0:
                # V2: Usar média do período todo, não snapshot final
                ltv_cac_medio = metricas.get('ltv_cac_medio', 0.0)
                
                # Fallback para cálculo manual se média não disponível
                if ltv_cac_medio is None or ltv_cac_medio <= 0:
                    last = df_m.iloc[-1]
                    ltv = last.get('ltv', 0)
                    cac = last.get('cac_blended', 0)
                    divisor_cac = max(cac, 1.00)
                    ltv_cac_medio = ltv / divisor_cac
                
                return float(ltv_cac_medio)
            
            return 0.0
            
        except Exception as e:
            # print(f"Erro no motor durante sensibilidade: {e}")
            return 0.0

    import copy # Ensure this is available

    # LTV/CAC Base Interno (Apple-to-Apples)
    # Recalculamos a base usando deepcopy para não sujar a PREMISSAS original
    ltv_cac_base_interno = get_ltv_cac(copy.deepcopy(PREMISSAS))
    
    # Se valor real foi passado, usaremos ele como âncora visual, mas os deltas vêm do interno
    if ltv_cac_base_real is not None and ltv_cac_base_real > 0:
        base_display = ltv_cac_base_real
    else:
        base_display = ltv_cac_base_interno
    
    # Se base for 0, algo está muito errado
    if ltv_cac_base_interno == 0:
        print("⚠️ AVISO: LTV/CAC Base calculado é 0.0. Verifique suas premissas base ou o motor.")
        return pd.DataFrame() 
    
    resultados = []
    
    # Dicionário de labels amigáveis
    nomes_display_map = {
        'marketing_fixo_mensal': 'Budget Marketing',
        'churn_inicial': 'Churn Base (%)',
        'taxa_trial_para_pagante': 'Conv. Trial -> Pago',
        'cpc_instagram': 'CPC Instagram',
        'cpc_facebook': 'CPC Facebook',
        'cpc_youtube': 'CPC Youtube',
        'cpc_google': 'CPC Google',
        'preco_trader': 'Preço Trader',
        'custo_ia_trader': 'Custo IA Trader',
        'salario_dev_senior': 'Salário Dev Sr',
        'trafego_inicial': 'Tráfego Inicial',
        'mix_trader': 'Mix Plano Trader',
        'b2b_probabilidade_anual': 'Prob. Venda B2B',
        'imposto_simples_inicial': 'Imposto Inicial'
    }
    
    # DEBUG: Print header
    # print(f"DEBUG SENSITIVIDADE: Variacao={variacao}")
    
    for chave in premissas_sensiveis:
        # A chave deve existir em PREMISSAS
        if chave not in PREMISSAS:
            continue
            
        valor_base = PREMISSAS[chave]
        
        # Só varia se for numérico
        if not isinstance(valor_base, (int, float)):
            continue
            
        # Cenário -20% (DEEPCOPY É CRÍTICO AQUI)
        p_min = copy.deepcopy(PREMISSAS)
        p_min[chave] = valor_base * (1 - variacao)
        ltv_cac_min_raw = get_ltv_cac(p_min)
        
        # Cenário +20% (DEEPCOPY É CRÍTICO AQUI)
        p_max = copy.deepcopy(PREMISSAS)
        p_max[chave] = valor_base * (1 + variacao)
        ltv_cac_max_raw = get_ltv_cac(p_max)
        
        # DEBUG: Verificar se rodou
        if ltv_cac_min_raw == 0 or ltv_cac_max_raw == 0:
             print(f"⚠️ ERRO SILENCIOSO no Tornado Plot para '{chave}': Retornou 0.0. O Motor falhou.")
        
        # DEBUG DETALHADO PARA CHURN (PROBLEMA ESPECÍFICO)
        if chave == 'churn_inicial':
            print(f"\n🔍 DEBUG CHURN:")
            print(f"   Valor Base: {valor_base:.4f} ({valor_base*100:.2f}%)")
            print(f"   Cenário -20%: {valor_base * (1 - variacao):.4f} → LTV/CAC = {ltv_cac_min_raw:.2f}x")
            print(f"   Cenário +20%: {valor_base * (1 + variacao):.4f} → LTV/CAC = {ltv_cac_max_raw:.2f}x")
            print(f"   Base Interno: {ltv_cac_base_interno:.2f}x | Base Display: {base_display:.2f}x")
            print(f"   Delta Min: {ltv_cac_min_raw - ltv_cac_base_interno:+.2f} | Delta Max: {ltv_cac_max_raw - ltv_cac_base_interno:+.2f}")
            print(f"   Proj Min: {base_display + (ltv_cac_min_raw - ltv_cac_base_interno):.2f}x")
            print(f"   Proj Max: {base_display + (ltv_cac_max_raw - ltv_cac_base_interno):.2f}x")
        
        # CALCULAR DELTAS (Diferença pura vs Base Interna)
        delta_min = ltv_cac_min_raw - ltv_cac_base_interno
        delta_max = ltv_cac_max_raw - ltv_cac_base_interno
        
        # PROJETAR NO DISPLAY (Base Real + Delta)
        val_min_proj = base_display + delta_min
        val_max_proj = base_display + delta_max
        
        # Impacto Absoluto (Tamanho da barra total)
        impacto_abs = abs(val_max_proj - val_min_proj)
        
        # Se impacto for zero absoluto ou muito pequeno, ignoramos para limpar gráfico
        if impacto_abs < 0.01:
            continue
            
        # Impacto Relativo
        impacto_rel = impacto_abs / base_display
        
        resultados.append({
            'premissa': chave,
            'nome_display': nomes_display_map.get(chave, chave),
            'valor_base': valor_base,
            'valor_min': valor_base * (1 - variacao),
            'valor_max': valor_base * (1 + variacao),
            
            # VALORES CORRIGIDOS PARA DISPLAY
            'ltv_cac_base': base_display, 
            'ltv_cac_min': val_min_proj,
            'ltv_cac_max': val_max_proj,
            
            'impacto_absoluto': impacto_abs,
            'impacto_relativo': impacto_rel
        })
    
    df_tornado = pd.DataFrame(resultados)
    if not df_tornado.empty:
        df_tornado = df_tornado.sort_values('impacto_absoluto', ascending=False)
        df_tornado['ranking'] = range(1, len(df_tornado) + 1)
        
    return df_tornado
    if not df_tornado.empty:
        df_tornado = df_tornado.sort_values('impacto_absoluto', ascending=False)
        df_tornado['ranking'] = range(1, len(df_tornado) + 1)
        
    return df_tornado



def plotar_tornado_plot(df_tornado, variacao_input=0.20, report_mode=False):
    """
    Gera o Tornado Plot (Gráfico de Sensibilidade) - V3 Gold Standard.
    
    Melhorias V3:
    1. Legenda: Usa Patches reais (quadrados coloridos) em vez de texto unicode que falha.
    2. Layout: Título ajustado para não sobrepor.
    3. Didática: Eixo X explicado como "Múltiplo LTV/CAC".
    4. Dinâmico: Texto de rodapé reflete a variação real (ex: ±15% se mudar na config).
    """
    
    # Setup de estilo
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Ajuste de tamanho para PDF vs Notebook (Gold Standard)
    figsize = (10, 6) if report_mode else (12, 7)
    fig, ax = plt.subplots(figsize=figsize)
    
    if df_tornado.empty:
        return fig
    
    # Ordenação (Apenas top 10 para não poluir)
    df_plot = df_tornado.sort_values('impacto_absoluto', ascending=True).tail(10)
    
    # Cores (Paleta Semântica)
    # Vermelho = Risco (Reduz LTV/CAC), Verde = Oportunidade (Aumenta LTV/CAC)
    cor_pos = '#4CAF50' # Verde Material Design
    cor_neg = '#E53935' # Vermelho Material Design
    cor_base_line = '#333333'
    
    y = np.arange(len(df_plot))
    base_val = df_plot['ltv_cac_base'].iloc[0] if len(df_plot) > 0 else 0
    
    # Barras (Hbar)
    for i, row in enumerate(df_plot.itertuples()):
        # Lógica de cor: 
        # Esquerda: desenha de (Base - Delta) até Base. Cor depende se reduz LTV.
        # Direita: desenha de Base até (Base + Delta). Cor depende se aumenta LTV.
        
        # Barra ESQUERDA (Efeito negativo, abaixo da base)
        # Queremos mostrar a amplitude da variação MINIMA
        val_min = min(row.ltv_cac_min, row.ltv_cac_max)
        width_left = base_val - val_min
        
        # Se o valor minimo é MENOR que a base (normal), desenha pra esquerda
        if width_left > 0:
            ax.barh(i, -width_left, left=base_val, height=0.6, color=cor_neg, alpha=0.9)
            ax.text(base_val - width_left - 0.05, i, f"{val_min:.1f}x", 
                    va='center', ha='right', fontsize=9, color='#C62828', fontweight='bold')
            
        # Barra DIREITA (Efeito positivo, acima da base)
        val_max = max(row.ltv_cac_min, row.ltv_cac_max)
        width_right = val_max - base_val
        
        # Se o valor máximo é MAIOR que a base (normal), desenha pra direita
        if width_right > 0:
            ax.barh(i, width_right, left=base_val, height=0.6, color=cor_pos, alpha=0.9)
            ax.text(base_val + width_right + 0.05, i, f"{val_max:.1f}x", 
                    va='center', ha='left', fontsize=9, color='#2E7D32', fontweight='bold')

    # Linha de Base Vertical
    ax.axvline(base_val, color=cor_base_line, linewidth=2, linestyle='-')
    ax.text(base_val, len(df_plot) + 0.2, f'Base: {base_val:.1f}x', 
            ha='center', va='bottom', fontsize=11, fontweight='bold', color=cor_base_line)
    
    # Eixos e Títulos
    ax.set_yticks(y)
    # Limpa nomes (remove underscores)
    labels = [str(x).replace('_', ' ').title() for x in df_plot['nome_display']]
    ax.set_yticklabels(labels, fontsize=11)
    
    # Título Principal e Subtítulo (Com padding para evitar sobreposição)
    pct_txt = int(variacao_input * 100)
    ax.set_title(f"Análise de Sensibilidade - Tornado Plot LTV/CAC\nVariação de ±{pct_txt}% nas Premissas | Impacto no Unit Economics", 
                 fontsize=14, fontweight='bold', pad=40)
    
    ax.set_xlabel("Índice LTV/CAC (x) - Quanto maior, melhor", fontsize=11, fontweight='bold')
    
    # Remover grid desnecessário e bordas
    ax.grid(axis='y', alpha=0)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False) # Clean look
    
    # --- CONFECÇÃO DA LEGENDA (CORREÇÃO V3) ---
    from matplotlib.lines import Line2D
    import matplotlib.patches as mpatches
    
    legend_patches = [
        mpatches.Patch(color=cor_neg, label='Risco (Reduz LTV/CAC)'),
        mpatches.Patch(color=cor_pos, label='Oportunidade (Aumenta LTV/CAC)'),
        Line2D([0], [0], color='black', lw=2, label=f'Cenário Base ({base_val:.1f}x)')
    ]
    ax.legend(handles=legend_patches, loc='lower right', frameon=True, fontsize=10)
    
    # Rodapé Dinâmico
    fig.text(0.02, 0.02, f"Fonte: Simulação Paramétrica (Variação de ±{pct_txt}% ceteris paribus).", 
             fontsize=9, color='gray', style='italic')

    # Ajuste de Limites para evitar sobreposição de texto
    # Calcula os extremos dos dados
    min_x = df_plot[['ltv_cac_min', 'ltv_cac_max']].min().min()
    max_x = df_plot[['ltv_cac_min', 'ltv_cac_max']].max().max()
    
    # Adiciona margem de 10% nas laterais
    amplitude = max_x - min_x
    ax.set_xlim(min_x - (amplitude * 0.15), max_x + (amplitude * 0.15))

    plt.tight_layout()
    # Ajuste fino extra pro título não cortar
    plt.subplots_adjust(top=0.88, bottom=0.15) 
    
    return fig





def gerar_tabela_probabilidades_mc(mc_results):
    """
    Gera tabela com todas as probabilidades do Monte Carlo.
    
    OUTPUT:
        DataFrame formatado com percentis e probabilidades críticas
    """
    
    # Identificar colunas disponíveis com fallback
    def get_col(df, options, default_series=None):
        for opt in options:
            if opt in df.columns:
                return df[opt]
        return default_series if default_series is not None else pd.Series([0])
    
    caixa_final = get_col(mc_results, ['caixa_final', 'caixa'])
    arr_final = get_col(mc_results, ['arr_final', 'arr'])
    mrr_final = get_col(mc_results, ['mrr_final', 'mrr'])
    usuarios_final = get_col(mc_results, ['usuarios_final', 'usuarios_ativos', 'usuarios'])
    ltv_cac = get_col(mc_results, ['ltv_cac_final', 'ltv_cac', 'ltv_cac_medio'])
    churn = get_col(mc_results, ['churn_medio', 'churn_final', 'churn'])
    payback = get_col(mc_results, ['payback_meses', 'payback'])
    
    # Calcular percentis
    # VERSÃO V2.0 - Inclui NRR e Burn Rate (antes órfãos)
    nrr = get_col(mc_results, ['nrr', 'net_revenue_retention'])
    burn_rate = get_col(mc_results, ['burn_rate_medio', 'burn_rate'])
    
    metricas = {
        'Caixa Final': caixa_final,
        'ARR Final': arr_final,
        'MRR Final': mrr_final,
        'Usuários Final': usuarios_final,
        'LTV/CAC': ltv_cac,
        'Churn Médio': churn,
        'NRR (%)': nrr,
        'Burn Rate (R$/mês)': burn_rate,
        'Payback (meses)': payback
    }
    
    tabela = []
    for nome, serie in metricas.items():
        if serie.sum() != 0:  # Só inclui se tiver dados
            row = {
                'Métrica': nome,
                'P5': serie.quantile(0.05),
                'P10': serie.quantile(0.10),
                'P25': serie.quantile(0.25),
                'P50': serie.quantile(0.50),
                'P75': serie.quantile(0.75),
                'P90': serie.quantile(0.90),
                'P95': serie.quantile(0.95),
                'Média': serie.mean(),
                'Desvio': serie.std()
            }
            tabela.append(row)
    
    df_tabela = pd.DataFrame(tabela)
    
    # Formatar valores conforme tipo de métrica
    # VERSÃO V2.0: Inclui NRR e Burn Rate
    for col in ['P5', 'P10', 'P25', 'P50', 'P75', 'P90', 'P95', 'Média', 'Desvio']:
        df_tabela[col] = df_tabela.apply(
            lambda row: formata_moeda(row[col]) if row['Métrica'] in ['Caixa Final', 'ARR Final', 'MRR Final', 'Burn Rate (R$/mês)'] 
            else (f"{row[col]:.1%}" if row['Métrica'] in ['Churn Médio', 'NRR (%)']
                  else (f"{row[col]:.1f}x" if row['Métrica'] == 'LTV/CAC' 
                        else f"{row[col]:,.0f}")), axis=1
        )
    
    return df_tabela


def render_var_histogram(mc_results, df_real_m, premissas, report_mode=False):
    """
    VIZ 5.X: HISTOGRAMA DE DISTRIBUIÇÃO VAR (Value at Risk)
    
    VERSÃO V1.0 - GOLD STANDARD
    Mostra a distribuição de caixa final com zonas de risco coloridas.
    Essencial para investidores institucionais.
    
    ELEMENTOS:
    1. Histograma com bins coloridos (Vermelho/Laranja/Verde)
    2. Linha vertical VaR95 (5% piores cenários)
    3. Linha vertical CVaR95 (média dos 5% piores)
    4. Linha vertical P50 (mediana)
    5. Linha vertical do Cenário Real
    """
    
    # Extrair caixa final
    caixa_final_col = 'caixa_final' if 'caixa_final' in mc_results.columns else 'caixa'
    if caixa_final_col not in mc_results.columns:
        return None
    
    caixa_final = mc_results[caixa_final_col].dropna()
    
    if len(caixa_final) < 10:
        return None
    
    # Calcular métricas de risco
    var95 = caixa_final.quantile(0.05)  # VaR95 = P5
    cvar95 = caixa_final[caixa_final <= var95].mean()  # Média dos piores 5%
    p50 = caixa_final.median()
    caixa_real_final = df_real_m['caixa'].iloc[-1] if 'caixa' in df_real_m.columns else 0
    
    # Probabilidades por zona
    prob_quebra = (caixa_final < 0).mean()
    prob_risco = ((caixa_final >= 0) & (caixa_final < 50000)).mean()
    prob_seguro = (caixa_final >= 50000).mean()
    
    # Criar figura
    figsize = (10, 5) if report_mode else (12, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Definir bins
    n_bins = 40
    bins = np.linspace(caixa_final.min() * 1.1, caixa_final.quantile(0.95), n_bins)
    
    # Plotar histograma com cores por zona
    n, bins_out, patches = ax.hist(caixa_final.clip(upper=caixa_final.quantile(0.95)), 
                                    bins=bins, edgecolor='white', linewidth=0.5, alpha=0.8)
    
    # Colorir cada bin conforme a zona
    for patch, left_edge in zip(patches, bins_out[:-1]):
        if left_edge < 0:
            patch.set_facecolor('#EF4444')  # Vermelho - Quebra
        elif left_edge < 50000:
            patch.set_facecolor('#F59E0B')  # Laranja - Risco
        else:
            patch.set_facecolor('#10B981')  # Verde - Seguro
    
    # Linhas verticais de referência
    ax.axvline(x=var95, color='#DC2626', linewidth=2.5, linestyle='--', 
               label=f'VaR95: {formata_moeda(var95)}')
    ax.axvline(x=cvar95, color='#991B1B', linewidth=2, linestyle=':', 
               label=f'CVaR95: {formata_moeda(cvar95)}')
    ax.axvline(x=p50, color='#1F2937', linewidth=2.5, linestyle='-', 
               label=f'Mediana (P50): {formata_moeda(p50)}')
    ax.axvline(x=caixa_real_final, color='#2563EB', linewidth=2.5, linestyle='-', 
               label=f'Cenário Real: {formata_moeda(caixa_real_final)}')
    ax.axvline(x=0, color='#000000', linewidth=1.5, linestyle='-', alpha=0.5)
    
    # Formatação
    ax.set_xlabel('Caixa Final M36 (R$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequência (nº de simulações)', fontsize=11, fontweight='bold')
    ax.set_title('DISTRIBUIÇÃO DE RISCO: Onde Estaremos no M36?\n' + 
                 f'P(Quebra)={prob_quebra:.1%} | P(Risco)={prob_risco:.1%} | P(Seguro)={prob_seguro:.1%}',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Formatar eixo X em milhares
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
    
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adicionar anotações de zona
    ax.text(0.02, 0.95, '🔴 QUEBRA', transform=ax.transAxes, fontsize=10, 
            color='#DC2626', fontweight='bold', verticalalignment='top')
    ax.text(0.02, 0.88, f'{prob_quebra:.1%}', transform=ax.transAxes, fontsize=9, 
            color='#DC2626', verticalalignment='top')
    
    plt.tight_layout()
    
    # Salvar se report_mode
    if report_mode:
        try:
            import os
            os.makedirs('outputs/figs', exist_ok=True)
            plt.savefig('outputs/figs/pag5_var_histogram.png', dpi=150, bbox_inches='tight')
        except:
            pass
    
    return fig, {
        'var95': var95,
        'cvar95': cvar95,
        'p50': p50,
        'prob_quebra': prob_quebra,
        'prob_risco': prob_risco,
        'prob_seguro': prob_seguro
    }


def render_survival_curve(mc_results, premissas, report_mode=False):
    """
    VIZ 5.X: CURVA DE SOBREVIVÊNCIA ACUMULADA
    
    VERSÃO V1.0 - GOLD STANDARD
    Mostra a probabilidade de sobrevivência (caixa > 0) ao longo dos 36 meses.
    Responde: "QUANDO é a zona de perigo, não apenas SE sobrevive."
    
    REQUER: caixa_series no mc_results (lista de 36 valores por simulação)
    """
    
    # Verificar se temos time series
    if 'caixa_series' not in mc_results.columns:
        # Fallback: usar apenas caixa_final (curva plana)
        caixa_final_col = 'caixa_final' if 'caixa_final' in mc_results.columns else 'caixa'
        if caixa_final_col not in mc_results.columns:
            return None, None
        
        # Criar curva sintética (linear do mês 1 ao 36)
        prob_final = (mc_results[caixa_final_col] > 0).mean()
        meses = np.arange(1, 37)
        prob_sobrevivencia = np.linspace(1.0, prob_final, 36)
        
        source_note = "⚠️ Curva sintética (caixa_series não disponível)"
    else:
        # Extrair séries temporais reais
        try:
            series_list = mc_results['caixa_series'].tolist()
            valid_series = [s for s in series_list if isinstance(s, (list, np.ndarray)) and len(s) > 0]
            
            if len(valid_series) < 10:
                return None, None
            
            series_matrix = np.array(valid_series)
            n_meses = series_matrix.shape[1]
            meses = np.arange(1, n_meses + 1)
            
            # Calcular P(caixa > 0) para cada mês
            prob_sobrevivencia = (series_matrix > 0).mean(axis=0)
            source_note = f"✅ Baseado em {len(valid_series)} simulações MC reais"
        except Exception as e:
            return None, None
    
    # Criar figura
    figsize = (10, 5) if report_mode else (12, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Plotar curva principal (APENAS LINHA - sem preenchimento por feedback do usuário)
    ax.plot(meses, prob_sobrevivencia, color='#047857', linewidth=3, marker='o', 
            markersize=3, markevery=3, label='P(Sobrevivência)')
    
    # Linhas de threshold
    ax.axhline(y=0.95, color='#10B981', linestyle='--', linewidth=1.5, 
               alpha=0.7, label='95% - Zona Segura')
    ax.axhline(y=0.80, color='#F59E0B', linestyle='--', linewidth=1.5, 
               alpha=0.7, label='80% - Zona de Atenção')
    ax.axhline(y=0.50, color='#EF4444', linestyle='--', linewidth=1.5, 
               alpha=0.7, label='50% - Zona Crítica')
    
    # Ponto de decisão no Mês 6
    if len(meses) >= 6:
        prob_m6 = prob_sobrevivencia[5]  # Índice 5 = Mês 6
        ax.scatter([6], [prob_m6], s=200, color='#1D4ED8', zorder=5, 
                   edgecolors='white', linewidth=2)
        ax.annotate(f'M6: {prob_m6:.1%}', xy=(6, prob_m6), 
                    xytext=(8, prob_m6 + 0.05), fontsize=10, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='#1D4ED8', lw=1.5))
    
    # Formatação
    ax.set_xlabel('Mês', fontsize=11, fontweight='bold')
    ax.set_ylabel('Probabilidade de Sobrevivência', fontsize=11, fontweight='bold')
    ax.set_title('CURVA DE SOBREVIVÊNCIA: Quando é a Zona de Perigo?\n' + 
                 f'P(Caixa > 0) ao Longo de 36 Meses | {source_note}',
                 fontsize=13, fontweight='bold', pad=15)
    
    ax.set_xlim(1, len(meses))
    ax.set_ylim(0, 1.05)
    ax.set_xticks(range(1, len(meses) + 1, 3))
    
    # Formatar eixo Y como porcentagem
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax.legend(loc='lower left', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Background zones removidas por feedback do usuário - gráfico mais limpo
    
    plt.tight_layout()
    
    # Salvar se report_mode
    if report_mode:
        try:
            import os
            os.makedirs('outputs/figs', exist_ok=True)
            plt.savefig('outputs/figs/pag5_survival_curve.png', dpi=150, bbox_inches='tight')
        except:
            pass
    
    # Identificar mês mais crítico (menor probabilidade)
    mes_critico = meses[np.argmin(prob_sobrevivencia)]
    prob_minima = prob_sobrevivencia.min()
    
    return fig, {
        'meses': meses,
        'prob_sobrevivencia': prob_sobrevivencia,
        'mes_critico': mes_critico,
        'prob_minima': prob_minima,
        'prob_m6': prob_sobrevivencia[5] if len(prob_sobrevivencia) >= 6 else None,
        'prob_m36': prob_sobrevivencia[-1] if len(prob_sobrevivencia) > 0 else None
    }


def render_ato1_fan_chart(mc_results, df_real_m, df_ideal_m, premissas, report_mode=False):
    """
    Renderiza o Ato 1 completo: Fan Chart + Mês 6 + Tabela + Insight.
    Segue padrão Gold Standard com elementos didáticos completos.
    """
    
    if not report_mode:
        print("\n" + "="*80)
        print("📊 ATO 1: MONTE CARLO FAN CHART - TESE MACRO")
        print("="*80)
    else:
        display(Markdown("***"))
        display(Markdown("## 📊 ATO 1: Monte Carlo Fan Chart"))
        display(Markdown('**Pergunta Central:** *"Qual a probabilidade real de chegarmos vivos aos 36 meses?"*'))
    
    # =========================================================================
    # 1. GRÁFICO FAN CHART PRINCIPAL
    # =========================================================================
    # Calcular probabilidade acima do teto (800k) para a nota
    caixa_final_col = 'caixa_final' if 'caixa_final' in mc_results.columns else 'caixa'
    if caixa_final_col in mc_results.columns:
        caixa_final = mc_results[caixa_final_col]
        prob_acima_teto = (caixa_final > 800000).mean()
    else:
        prob_acima_teto = 0
        
    dados_fan = preparar_dados_fan_chart(mc_results, df_real_m, df_ideal_m)
    fig1 = plotar_fan_chart(dados_fan, report_mode, prob_acima_teto=prob_acima_teto)
    
    if report_mode:
        try:
            import os
            os.makedirs('outputs/figs', exist_ok=True)
            plt.savefig('outputs/figs/pag5_monte_carlo_fan_chart.png', dpi=150, bbox_inches='tight')
            display(Markdown("![Fan Chart Monte Carlo](outputs/figs/pag5_monte_carlo_fan_chart.png)"))
            display(Markdown("_Fonte: mc_results (Célula 5D - Monte Carlo) | df_real_m vs df_ideal_m (Célula 5A/5B)_"))
        except:
            pass
    else:
        display(fig1)
    plt.close(fig1)
    
    # =========================================================================
    # 2. COMO LER O GRÁFICO (PADRÃO DIDÁTICO COMPLETO)
    # =========================================================================
    como_ler_grafico = """
::: {.callout-note title="📖 COMO LER O GRÁFICO FAN CHART" collapse="false"}

**O QUE ESTOU VENDO?**
Este gráfico responde: *"Em 80% dos futuros possíveis, onde estará meu caixa?"*

**ELEMENTOS VISUAIS:**

- **Área CINZA ESCURO (centro):** P25-P75 = 50% dos cenários mais prováveis
  - Se seu planejamento estiver nesta faixa, você está alinhado com a maioria das simulações
  
- **Área CINZA CLARO (externa):** P10-P90 = 80% dos cenários
  - Esta é a faixa de "realidade" - cenários fora disso são outliers
  
- **Linha PRETA (P50):** Resultado mais provável (mediana)
  - Use como referência principal de planejamento
  
- **Linha AZUL com ●:** Cenário Real (conservador)
  - Trajetória se tudo correr "ok" - sem grandes vitórias ou perdas
  
- **Linha VERDE TRACEJADA com ■:** Cenário Ideal (benchmark)
  - O que alcançaríamos com execução perfeita + sorte
  
- **Linha VERMELHA HORIZONTAL:** Ponto de quebra (R$ 0)
  - Cruzar esta linha = morte da startup
  
- **Linha LARANJA VERTICAL (Mês 6):** Seu ponto de decisão
  - Marcador para avaliar se continua ou para

**COMO INTERPRETAR:**

✅ **Cenário Saudável:**
- Área cinza escuro (P25-P75) está ACIMA de R$ 0 durante todos os 36 meses
- Linha Real (azul) está próxima ou dentro da área cinza escuro
- Linha P50 (preta) sobe consistentemente

⚠️ **Sinais de Alerta:**
- Área P10 (borda inferior cinza claro) cruza a linha vermelha
- Linha Real está abaixo de P25 = execução pior que 75% dos cenários
- Fan abre muito = alta incerteza, modelo instável

🔴 **Cenário Crítico:**
- P25 cruza linha vermelha = mais de 25% de chance de quebra
- Linha Real está fora da área cinza = modelo descalibrado
- Mês 6 está na zona cinza perto de R$ 0
:::
"""
    
    if report_mode:
        display(Markdown(como_ler_grafico))
    else:
        print("\n📖 COMO LER O GRÁFICO:")
        print("   • Área escura = 50% dos cenários mais prováveis")
        print("   • Linha azul = seu cenário Real (conservador)")
        print("   • Linha vermelha = ponto de quebra (caixa zero)")
        print("   • Faixa saudável: P25 sempre acima de R$ 0")
    
    # =========================================================================
    # 3. GRÁFICO ESPECÍFICO MÊS 6 (PONTO DE DECISÃO)
    # =========================================================================
    if not report_mode:
        print("\n" + "-"*40)
        print("🎯 ZOOM: PONTO DE DECISÃO - MÊS 6")
    else:
        display(Markdown("***"))
        display(Markdown("### 🎯 ZOOM: PONTO DE DECISÃO - MÊS 6"))
    
    fig2, dados_m6 = plotar_grafico_mes6(mc_results, df_real_m, df_ideal_m, premissas, report_mode)
    
    if report_mode:
        try:
            plt.savefig('outputs/figs/pag5_distribuicao_mes6.png', dpi=150, bbox_inches='tight')
            display(Markdown("![Distribuição Mês 6](outputs/figs/pag5_distribuicao_mes6.png)"))
            display(Markdown("_Fonte: mc_results (Célula 5D) | df_real_m, df_ideal_m (Célula 5A/5B)_"))
        except:
            pass
    else:
        display(fig2)
    plt.close(fig2)
    
    # Como ler o gráfico do Mês 6
    como_ler_mes6 = f"""
::: {{.callout-note title="📖 COMO LER O GRÁFICO MÊS 6" collapse="false"}}

**O QUE ESTOU VENDO?**
Histograma mostrando: *"Onde provavelmente estarei no mês 6?"*

**CORES DAS BARRAS:**
- 🔴 **VERMELHO (esquerda):** Cenários de QUEBRA (caixa < R$ 0)
  - Probabilidade: **{dados_m6['prob_quebra_m6']:.1%}** das simulações
  
- 🟠 **LARANJA (centro-esquerda):** Cenários de RISCO (R$ 0 a R$ 10k)
  - Probabilidade: **{dados_m6['prob_risco_m6']:.1%}** das simulações
  - Caixa insuficiente para emergências
  
- 🟢 **VERDE (direita):** Cenários SEGUROS (> R$ 10k)
  - Probabilidade: **{dados_m6['prob_seguro_m6']:.1%}** das simulações
  - Margem confortável para continuar

**LINHAS VERTICAIS:**
- Linha AZUL = Cenário Real projetado para M6
- Linha VERDE = Cenário Ideal para M6
- Linha PRETA = Mediana (50% acima, 50% abaixo)

**SUA DECISÃO NO MÊS 6:**
- Se caixa < R$ 0 → Fechar ou buscar investimento urgente
- Se caixa entre R$ 0-10k → Continuar com cautela extrema
- Se caixa > R$ 10k → Continuar com confiança

:::
"""
    
    if report_mode:
        display(Markdown(como_ler_mes6))
    else:
        print(f"\n🎯 RESUMO MÊS 6:")
        print(f"   🔴 Prob. Quebra: {dados_m6['prob_quebra_m6']:.1%}")
        print(f"   🟠 Prob. Risco: {dados_m6['prob_risco_m6']:.1%}")
        print(f"   🟢 Prob. Seguro: {dados_m6['prob_seguro_m6']:.1%}")
        print(f"   📊 Mediana M6: {formata_moeda(dados_m6['p50_m6'])}")
    
    # =========================================================================
    # 4. TABELA DE PERCENTIS + EXPLICAÇÃO
    # =========================================================================
    df_tabela_probs = gerar_tabela_probabilidades_mc(mc_results)
    
    explicacao_tabela = """
::: {.callout-note title="📖 COMO LER A TABELA DE PERCENTIS" collapse="false"}

**O QUE ESTA TABELA MOSTRA?**
Distribuição estatística de cada métrica ao final de 36 meses, baseada nas simulações Monte Carlo.

**COLUNAS EXPLICADAS:**

| Coluna | Significado | Como usar |
|--------|-------------|-----------|
| **P5** | Pior cenário (5% mais pessimistas) | Use para VaR - quanto pode perder |
| **P10** | Cenário pessimista conservador | Use para planejamento de contingência |
| **P25** | Limite inferior "normal" | 75% dos cenários superam este valor |
| **P50** | **MEDIANA - USE ESTE PARA PLANEJAR** | Valor mais provável |
| **P75** | Limite superior "normal" | 25% dos cenários superam este valor |
| **P90** | Cenário otimista realista | Meta stretch alcançável |
| **P95** | Melhor cenário (5% mais otimistas) | Upside máximo provável |

**LEITURA RÁPIDA:**
1. Olhe o P50 (mediana) para cada métrica - é seu caso base
2. Compare P5 vs P50 - se diferença for grande, há muito risco
3. Compare P50 vs P95 - se diferença for grande, há muito upside
4. Largura (P95-P5) mostra a incerteza total

**MÉTRICAS-CHAVE:**
- **Caixa Final:** Quanto dinheiro sobra no mês 36
- **ARR Final:** Receita Recorrente Anual no final
- **LTV/CAC:** Saúde unitária - deve ser > 3x para ser sustentável
- **Churn:** Taxa de cancelamento - menor é melhor

:::
"""
    
    if report_mode:
        display(Markdown("\n### 📋 TABELA DE PERCENTIS MONTE CARLO"))
        display(Markdown(df_tabela_probs.to_markdown(index=False)))
        display(Markdown(explicacao_tabela))
    else:
        print("\n📋 TABELA DE PERCENTIS:")
        print(df_tabela_probs.to_string(index=False))
    
    # =========================================================================
    # 5. PROBABILIDADES CRÍTICAS
    # =========================================================================
    caixa_final = mc_results.get('caixa_final', mc_results.get('caixa', pd.Series([0])))
    arr_final = mc_results.get('arr_final', mc_results.get('arr', pd.Series([0])))
    ltv_cac = mc_results.get('ltv_cac_final', mc_results.get('ltv_cac', pd.Series([0])))
    
    n_sims = len(mc_results)
    prob_quebra = (caixa_final < 0).sum() / n_sims if n_sims > 0 else 0
    prob_caixa_50k = (caixa_final > 50000).sum() / n_sims if n_sims > 0 else 0
    prob_caixa_100k = (caixa_final > 100000).sum() / n_sims if n_sims > 0 else 0
    prob_arr_1m = (arr_final > 1000000).sum() / n_sims if n_sims > 0 else 0
    prob_ltv_5x = (ltv_cac > 5).sum() / n_sims if n_sims > 0 else 0
    
    probs_md = f"""
### 🎯 PROBABILIDADES CRÍTICAS (Final M36)

| Evento | Probabilidade | O que significa | Status |
|:-------|:-------------:|:----------------|:------:|
| Caixa < R$ 0 (Quebra) | **{prob_quebra:.1%}** | Risco de morte da startup | {'🟢 Baixo' if prob_quebra < 0.10 else '🔴 Alto'} |
| Caixa > R$ 50k | **{prob_caixa_50k:.1%}** | Caixa mínimo para emergências | {'🟢 Bom' if prob_caixa_50k > 0.70 else '🟡 Atenção'} |
| Caixa > R$ 100k | **{prob_caixa_100k:.1%}** | Caixa confortável para growth | {'🟢 Ótimo' if prob_caixa_100k > 0.50 else '🟡 Médio'} |
| ARR > R$ 1M | **{prob_arr_1m:.1%}** | Faturamento mínimo para Série A | {'🟢 Atrativo' if prob_arr_1m > 0.60 else '🟡 Desenvolver'} |
| LTV/CAC > 5x | **{prob_ltv_5x:.1%}** | Unit Economics excelente | {'🟢 Saudável' if prob_ltv_5x > 0.30 else '🟡 Melhorar'} |
"""
    
    if report_mode:
        display(Markdown(probs_md))
    else:
        print(f"\n🎯 PROBABILIDADES CRÍTICAS:")
        print(f"   • Prob. Quebra: {prob_quebra:.1%} {'🟢' if prob_quebra < 0.10 else '🔴'}")
        print(f"   • Prob. Caixa > R$ 50k: {prob_caixa_50k:.1%}")
        print(f"   • Prob. Caixa > R$ 100k: {prob_caixa_100k:.1%}")
        print(f"   • Prob. ARR > R$ 1M: {prob_arr_1m:.1%}")
    
    # =========================================================================
    # 6. INSIGHT ESTRATÉGICO
    # =========================================================================
    p5 = caixa_final.quantile(0.05)
    p50 = caixa_final.quantile(0.50)
    p95 = caixa_final.quantile(0.95)
    var95 = p5
    cvar_mask = caixa_final < var95
    cvar95 = caixa_final[cvar_mask].mean() if cvar_mask.sum() > 0 else var95
    
    # Diagnóstico do Mês 6
    diagnostico_m6 = "🟢 Seguro" if dados_m6['prob_seguro_m6'] > 0.70 else ("🟡 Risco" if dados_m6['prob_seguro_m6'] > 0.50 else "🔴 Crítico")
    
    insight_md = f"""
::: {{.callout-important title="💡 INSIGHT ESTRATÉGICO - ROBUSTEZ DO MODELO" icon=false}}

#### FATO (O que os números dizem)
- **Sobrevivência (M36):** {(1-prob_quebra):.1%} de probabilidade de caixa positivo
- **Mediana do Caixa:** {formata_moeda(p50)} - valor mais provável ao final
- **VaR 95%:** {formata_moeda(var95)} - pior cenário nos 5% mais pessimistas
- **Dispersão:** {formata_moeda(p95 - p5)} entre P5 e P95

#### PONTO DE DECISÃO MÊS 6
- **Status:** {diagnostico_m6}
- **Caixa Mediana M6:** {formata_moeda(dados_m6['p50_m6'])}
- **Prob. Seguro (>R$ 10k):** {dados_m6['prob_seguro_m6']:.1%}
- **Recomendação M6:** {"Continuar com confiança" if dados_m6['prob_seguro_m6'] > 0.70 else "Reavaliar métricas de churn e CAC" if dados_m6['prob_seguro_m6'] > 0.50 else "Alto risco - considerar pivot ou captação"}

#### IMPLICAÇÃO
- {"✅ Modelo robusto com proteção estrutural" if prob_quebra < 0.05 else "⚠️ Modelo funcional mas com margem apertada" if prob_quebra < 0.15 else "🔴 Modelo frágil - alta dependência de execução perfeita"}
- {"✅ Dispersão controlada - premissas confiáveis" if (p95-p5) < p50 * 3 else "⚠️ Alta dispersão - incerteza significativa nas premissas"}

#### AÇÃO RECOMENDADA
{"✅ **Manter curso atual** - modelo validado, focar em execução" if prob_quebra < 0.05 and dados_m6['prob_seguro_m6'] > 0.70 else "⚠️ **Criar buffer de R$ 30-50k** antes do mês 6 para proteção" if prob_quebra < 0.15 else "🔴 **Revisar estrutura de custos** e/ou buscar captação urgente"}

:::
"""
    
    if report_mode:
        display(Markdown(insight_md))
    else:
        print(f"\n💡 INSIGHT ESTRATÉGICO:")
        print(f"   • Sobrevivência: {(1-prob_quebra):.1%}")
        print(f"   • P50 (Mediana): {formata_moeda(p50)}")
        print(f"   • VaR95: {formata_moeda(var95)}")
        print(f"   • Mês 6: {diagnostico_m6} ({dados_m6['prob_seguro_m6']:.1%} seguro)")
    
    # =========================================================================
    # 7. AUDITORIA TÉCNICA
    # =========================================================================
    audit_md = f"""
::: {{.callout-note title="🔍 AUDITORIA TÉCNICA" collapse="true"}}

#### PARÂMETROS DA SIMULAÇÃO
- **Número de simulações:** {n_sims:,}
- **Horizonte:** 36 meses
- **Seed:** 42 (reprodutível)
- **Variáveis estocásticas:** Churn, CAC, Conversão, Tráfego

#### FÓRMULAS UTILIZADAS
```
Caixa[t] = Caixa[t-1] + (MRR[t] - Custos_Totais[t])
VaR_95 = Percentil_5(caixa_final_array)
CVaR_95 = Média(caixa | caixa < VaR_95)
P(Quebra) = Count(caixa < 0) / n_simulações
```

#### FONTE DE DADOS
- Monte Carlo: `celula_5D_monte_carlo.py`
- Premissas: `celula_2_premissas.py` + `celula_2B_config_MC.py`

#### ARQUIVOS GERADOS
- `outputs/figs/pag5_monte_carlo_fan_chart.png`
- `outputs/figs/pag5_distribuicao_mes6.png`

:::
"""
    
    if report_mode:
        display(Markdown(audit_md))
    
    return {
        'dados_fan': dados_fan,
        'dados_mes6': dados_m6,
        'df_tabela_probs': df_tabela_probs,
        'probabilidades': {
            'prob_quebra': prob_quebra,
            'prob_caixa_50k': prob_caixa_50k,
            'prob_caixa_100k': prob_caixa_100k,
            'prob_arr_1m': prob_arr_1m,
            'prob_ltv_5x': prob_ltv_5x,
            'var95': var95,
            'cvar95': cvar95,
            'p50': p50
        }
    }



def render_ato2_sensibilidade(premissas, report_mode=False, motor_func=None, met_real=None, df_real_m=None):
    """
    Renderiza o Ato 2 completo: Tornado Plot Sensibilidade.
    Segue padrão Gold Standard V22.0.
    """
    
    if not report_mode:
        print("\n" + "="*80)
        print("🌪️ ATO 2: TORNADO PLOT - ANÁLISE DE SENSIBILIDADE (UNIT ECONOMICS)")
        print("="*80)
    else:
        display(Markdown("***"))
        display(Markdown("## 🌪️ ATO 2: Tornado Plot (Sensibilidade)"))
        display(Markdown('**Pergunta Central:** *"Qual premissa, se errarmos, mata o negócio?"*'))
        
    # =========================================================================
    # 1. PREPARAÇÃO DOS DADOS
    # =========================================================================
    
    # 3.1: Lista Dinâmica de Premissas (Zero Hardcode)
    # Extrai as chaves do dicionário de Monte Carlo (Célula 2B)
    try:
        dict_mc = premissas.get('monte_carlo', {})
        dict_vars = dict_mc.get('variaveis', {})
        premissas_sensiveis = list(dict_vars.keys())
        
        # Adiciona algumas chaves estruturais extras se não estiverem lá
        extras = ['trafego_inicial', 'preco_trader'] 
        for e in extras:
            if e not in premissas_sensiveis and e in premissas:
                premissas_sensiveis.append(e)
        
        # CALCULAR VARIAÇÃO DINÂMICA: usa std médio das variáveis MC (zero hardcoding)
        stds = [v.get('std', 0.20) for v in dict_vars.values() if isinstance(v, dict) and 'std' in v]
        variacao_dinamica = sum(stds) / len(stds) if stds else 0.20
                
    except Exception as e:
        print(f"⚠️ Erro ao carregar variáveis do Monte Carlo: {e}")
        # Fallback de segurança (apenas se config estiver corrompida)
        premissas_sensiveis = ['churn_inicial', 'marketing_fixo_mensal', 'taxa_trial_para_pagante']
        variacao_dinamica = 0.20  # Fallback se MC config não disponível

    if not report_mode:
        print(f"🔍 Analisando sensibilidade para {len(premissas_sensiveis)} variáveis dinâmicas...")
    
    # Extrai LTV/CAC real se disponível
    # Extrai LTV/CAC real se disponível (SNAPSHOT FINAL)
    ltv_cac_real_val = 0
    if df_real_m is not None:
        if 'ltv_cac' in df_real_m.columns:
            ltv_cac_real_val = df_real_m['ltv_cac'].iloc[-1]
        elif 'ltv_cac_final' in df_real_m.columns:
            ltv_cac_real_val = df_real_m['ltv_cac_final'].iloc[-1]
    
    # Se falhou no df, usa metricas (fallback) ou 0
    if ltv_cac_real_val == 0 and met_real:
        ltv_cac_real_val = met_real.get('ltv_cac_medio', 0)
    
    df_tornado = calcular_sensibilidade_ltv_cac(
        premissas, 
        premissas_sensiveis, 
        variacao=variacao_dinamica,  # ← DINÂMICO do MC config
        motor_func=motor_func,
        ltv_cac_base_real=ltv_cac_real_val
    )
    
    # Se falhar ou vazio, mostrar erro
    if df_tornado.empty:
        if report_mode: display(Markdown("⚠️ Não foi possível gerar dados de sensibilidade."))
        else: print("⚠️ Erro dados sensibilidade.")
        return None
        
    # =========================================================================
    # 2. GRÁFICO TORNADO PLOT
    # =========================================================================
    fig2 = plotar_tornado_plot(df_tornado, variacao_input=variacao_dinamica, report_mode=report_mode)
    
    # =========================================
    # RENDERIZAÇÃO ATÔMICA (V7.0)
    # =========================================
    render_atomic_block(
        chart_id="pg5_viz2_tornado",
        title_technical="VIZ 5.2: Análise de Sensibilidade (Tornado Plot)",
        title_colloquial="Quais alavancas realmente movem o ponteiro?",
        fig=fig2,
        legend_md=f"Barras mostram o impacto no LTV/CAC ao variar cada premissa em ±{variacao_dinamica*100:.0f}%.",
        df_tabela=df_tornado,
        insight_dict={
            "fato": f"A variável **{df_tornado.iloc[0]['nome_display']}** é o maior vetor de volatilidade, com {(df_tornado.iloc[0]['impacto_absoluto']/df_tornado['impacto_absoluto'].sum()*100):.0f}% do impacto total.",
            "causa": f"As top 3 variáveis ({', '.join(df_tornado['nome_display'].head(3))}) explicam {(df_tornado['impacto_absoluto'].head(3).sum()/df_tornado['impacto_absoluto'].sum()*100):.0f}% da sensibilidade do modelo devido à natureza multiplicativa do Unit Economics.",
            "implicacao": f"Erros de estimativa nestes drivers custam desproporcionalmente caro. Otimizar **{df_tornado.iloc[0]['nome_display']}** traz maior ROI que qualquer outra ação.",
            "acao": f"Criar dashboard semanal específico para monitorar: {', '.join(df_tornado['nome_display'].head(3).tolist())}."
        },
        report_mode=report_mode,
        data_source_text="Fonte: Monte Carlo Sensitivity"
    )
    plt.close(fig2)

    # =========================================================================
    # 3. COMO LER & GLOSSÁRIO (DIDÁTICO V4 - TEXTO DO USUÁRIO)
    # =========================================================================
    ltv_base_val = df_tornado['ltv_cac_base'].iloc[0]
    como_ler = f"""
::: {{.callout-note title="🧠 COMO INTERPRETAR A SENSIBILIDADE (TORNADO)" collapse="false"}}

**OBJETIVO ESTRATÉGICO:**
Identificar a **elasticidade** do modelo de negócios. O gráfico hierarquiza as premissas onde um erro de estimativa (ou sucesso na execução) tem maior alavancagem sobre o resultado final.

**LEITURA TÉCNICA:**
*   **Eixo Central ({ltv_base_val:.1f}x):** O LTV/CAC projetado no cenário base.
*   **Largura das Barras:** A volatilidade gerada ao oscilar cada premissa individualmente em **±{variacao_dinamica*100:.0f}%** (Ceteris Paribus).
*   **Assimetria:** Observe se a barra cresce mais para a esquerda (Risco de Downside) ou direita (Oportunidade de Upside).

**DECISÃO GERENCIAL (PARETO 80/20):**
As variáveis no **topo do funil** são os "Control Levers" do negócio. O CEO deve focar 80% do tempo em otimizar e controlar estas métricas críticas, pois elas ditam a viabilidade da empresa. Variáveis na base são ruído e não merecem microgerenciamento.
:::

::: {{.callout-tip title="📚 GLOSSÁRIO TÉCNICO (ENTENDA OS TERMOS)" collapse="true"}}
Aqui está a tradução dos termos técnicos usados no gráfico:

*   **LTV/CAC:** Relação entre o Valor Vitalício do Cliente e o Custo de Aquisição. Indica o retorno sobre o investimento em marketing. **Benchmark Seguro: > 3.0x**.
*   **Churn Base (%):** Taxa de cancelamento mensal. Percentual da base de clientes que deixa de pagar o produto.
*   **Conv. Trial -> Pago:** Taxa de conversão de usuários em teste (Trial) para assinantes pagantes.
*   **CPC (Custo por Clique):** Valor pago às plataformas de anúncios (Ads) por cada clique gerado.
*   **Taxa Visitante -> Trial:** Eficiência da Landing Page em converter tráfego frio em cadastros (Leads/Trial).
*   **ARPU:** Receita Média por Usuário (Average Revenue Per User). Ticket médio mensal pago por cada cliente ativo.
:::
"""
    if report_mode:
        display(Markdown(como_ler))
    else:
        print("\n📖 LEITURA RÁPIDA: As variáveis no topo são as mais perigosas. Foque nelas.")
        
    # =========================================================================
    # 4. TABELA RANKING (Top 5)
    # =========================================================================
    top5 = df_tornado.head(5)[['ranking', 'nome_display', 'valor_base', 'impacto_relativo', 'ltv_cac_min', 'ltv_cac_max']].copy()
    
    # Formatação Tabela
    tabela_data = []
    for _, row in top5.iterrows():
        tabela_data.append({
            '#': row['ranking'],
            'Premissa Crítica': row['nome_display'],
            'Base': f"{row['valor_base']:.2f}" if row['valor_base'] < 100 else f"{row['valor_base']:.0f}",
            'Impacto Relativo': f"{row['impacto_relativo']:.0%}",
            'Range LTV/CAC': f"{row['ltv_cac_min']:.1f}x ↔ {row['ltv_cac_max']:.1f}x"
        })
    df_tabela_top5 = pd.DataFrame(tabela_data)
        
    if report_mode:
        display(Markdown(f"**Tabela 5.2: Top 5 Variáveis de Maior Sensibilidade (Ranking de Risco)**"))
        display(Markdown(df_tabela_top5.to_markdown(index=False)))
    
    msg_tabela = """
::: {.callout-tip title="📋 COMO LER ESTA TABELA" collapse="true"}
*   **Premissa Crítica:** O nome da variável de negócio.
*   **Base:** Valor atual utilizado no modelo.
*   **Impacto Relativo:** Quanto o LTV/CAC muda em relação à base. 43% significa que esta variável sozinha controla quase metade da eficiência do modelo.
*   **Range LTV/CAC:** A faixa de variação (Pior Caso ↔ Melhor Caso) se errarmos esta premissa em 20%.
:::
"""
    if report_mode:
        display(Markdown(msg_tabela))
    else:
        print("\n📋 TOP 5 VARIÁVEIS CRÍTICAS:")
        print(df_tabela_top5.to_string(index=False))

    # =========================================================================
    # 5. INSIGHT ESTRATÉGICO (100% DINÂMICO)
    # =========================================================================
    # Analisar Top 1 vs Top 3
    top1 = df_tornado.iloc[0]
    top3 = df_tornado.iloc[:3]
    top3_impacto_total = top3['impacto_relativo'].sum()
    resto_impacto_total = df_tornado.iloc[3:]['impacto_relativo'].sum()
    
    insight_md = f"""
::: {{.callout-important title="💡 INSIGHT ESTRATÉGICO - ONDE FOCAR A ATENÇÃO" icon=false}}

#### FATO
A premissa **{top1['nome_display']}** é o maior vetor de risco, com **{top1['impacto_relativo']:.0%} de impacto** no LTV/CAC. 
 sozinha, ela afeta o resultado mais do que as {len(df_tornado)-3} últimas variáveis somadas.

#### CAUSA
As **3 variáveis do topo** ({', '.join(top3['nome_display'].tolist())}) explicam **{top3_impacto_total/(top3_impacto_total+resto_impacto_total):.0%}** de toda a variabilidade do modelo. Isso ocorre pela natureza multiplicativa da fórmula do Unit Economics.

#### IMPLICAÇÃO PRÁTICA
Otimizar **{top1['nome_display']}** em 10% trará **{top1['impacto_relativo']/2:.1f}x mais retorno** do que qualquer esforço nas variáveis da base. 
**Ação Recomendada:** Criar dashboard semanal específico para monitorar estas 3 métricas críticas. Errar aqui custa caro.

:::
"""
    if report_mode:
        display(Markdown(insight_md))
    else:
        print(f"\n💡 INSIGHT: Foco total em {top1['nome_display']}. É o maior risco do negócio.")
        
    # =========================================================================
    # 6. AUDITORIA
    # =========================================================================
    audit_md = """
::: {.callout-note title="🔍 AUDITORIA TÉCNICA" collapse="true"}
**Metodologia:** Análise One-at-a-Time (OAT). Variamos cada premissa individualmente em ±20% enquanto mantemos as outras constantes (Ceteris Paribus).
**Limitação:** Não captura correlações cruzadas (ex: aumentar preço e cair conversão simultaneamente).
**Fórmula:** Impacto = |LTV/CAC(+20%) - LTV/CAC(-20%)|
:::
"""
    if report_mode:
        display(Markdown(audit_md))

    return df_tornado


# ============================================================================
# SEÇÃO 5: ATO 3 - ANÁLISE DE RESILIÊNCIA DE RUNWAY (TÁTICO)
# ============================================================================

def calcular_metricas_runway_profundas(df_real_m, df_ideal_m, df_stress_m, premissas):
    """
    Calcula métricas profundas de runway para análise multi-dimensional.
    
    RETORNA:
    - Trajetória de runway ao longo do tempo
    - Decomposição do burn rate (o que está comendo o caixa)
    - Correlações caixa vs burn vs receita
    - Pontos de inflexão críticos
    - Gap Real vs Ideal vs Estresse
    """
    
    threshold = premissas.get('threshold_caixa_quebra', -10000)
    meses = np.arange(1, len(df_real_m) + 1)
    
    metricas = {}
    
    for nome, df in [('Real', df_real_m), ('Ideal', df_ideal_m), ('Estresse', df_stress_m)]:
        if df is None or len(df) == 0:
            continue
            
        caixa = df['caixa'].values if 'caixa' in df.columns else np.zeros(len(df))
        
        # Calcular componentes do burn rate
        if 'total_cogs' in df.columns:
            cogs = df['total_cogs'].values
        else:
            cogs = np.zeros(len(df))
            
        if 'total_opex' in df.columns:
            opex = df['total_opex'].values
        else:
            opex = np.zeros(len(df))
            
        if 'gasto_marketing' in df.columns:
            marketing = df['gasto_marketing'].values
        else:
            marketing = np.zeros(len(df))
            
        if 'custo_pessoal' in df.columns:
            pessoal = df['custo_pessoal'].values
        else:
            pessoal = np.zeros(len(df))
            
        if 'custo_infra_fixo' in df.columns:
            infra = df['custo_infra_fixo'].values
        else:
            infra = np.zeros(len(df))
        
        receita = df['receita_liquida'].values if 'receita_liquida' in df.columns else np.zeros(len(df))
        
        # Burn rate = saídas - entradas
        custos_totais = cogs + opex
        burn_rate = custos_totais - receita
        burn_rate = np.maximum(burn_rate, 0)  # Se negativo, está lucrando = burn 0
        
        # Runway em cada mês
        # Runway em cada mês (ZERO REVENUE SCENARIO - Alinhado com Título)
        # "Quanto tempo a empresa sobrevive se a receita parar?"
        runway = np.zeros(len(df))
        for i in range(len(df)):
            if caixa[i] <= threshold:
                runway[i] = 0
            elif custos_totais[i] <= 0:
                runway[i] = 36  # Sem custos = infinito
            else:
                # Fórmula de Sobrevivência: Caixa / Custos Brutos (sem considerar receita)
                runway[i] = min(36, caixa[i] / custos_totais[i])
        
        # Identificar mês mais crítico
        mes_critico = np.argmin(runway) + 1
        runway_minimo = runway.min()
        
        # Calcular velocidade de deterioração
        delta_runway = np.diff(runway, prepend=runway[0])
        pior_queda = delta_runway.min()
        mes_pior_queda = np.argmin(delta_runway) + 1
        
        # Decomposição dos CUSTOS (% do custo total, não do burn rate)
        # O burn rate = custos - receita, mas para decomposição devemos usar custos brutos
        custos_medio = custos_totais.mean()
        burn_medio = burn_rate.mean()
        
        if custos_medio > 0:
            # Calcular percentuais sobre os custos totais (não sobre o burn)
            pct_marketing = (marketing.mean() / custos_medio) * 100 if marketing.mean() > 0 else 0
            pct_pessoal = (pessoal.mean() / custos_medio) * 100 if pessoal.mean() > 0 else 0
            pct_infra = (infra.mean() / custos_medio) * 100 if infra.mean() > 0 else 0
            pct_outros = max(0, 100 - pct_marketing - pct_pessoal - pct_infra)
            
            # Se soma > 100%, normalizar (pode acontecer se categorias se sobrepõem)
            soma_pcts = pct_marketing + pct_pessoal + pct_infra + pct_outros
            if soma_pcts > 100:
                fator = 100 / soma_pcts
                pct_marketing *= fator
                pct_pessoal *= fator
                pct_infra *= fator
                pct_outros *= fator
        else:
            pct_marketing = pct_pessoal = pct_infra = pct_outros = 0

        
        # Correlação caixa vs burn
        if len(caixa) > 5:
            corr_caixa_burn = np.corrcoef(caixa, burn_rate)[0, 1]
        else:
            corr_caixa_burn = 0
        
        # Meses em cada zona
        meses_criticos = np.sum(runway < 3)  # < 3 meses
        meses_atencao = np.sum((runway >= 3) & (runway < 6))
        meses_seguros = np.sum(runway >= 6)
        
        # Primeiro mês crítico (runway < 3)
        idx_crit = np.where(runway < 3)[0]
        primeiro_critico = idx_crit[0] + 1 if len(idx_crit) > 0 else None
        
        # Taxa de cobertura: receita / custos
        taxa_cobertura = receita.mean() / custos_totais.mean() if custos_totais.mean() > 0 else 0
        
        metricas[nome] = {
            'caixa': caixa,
            'runway': runway,
            'burn_rate': burn_rate,
            'receita': receita,
            'custos_totais': custos_totais,
            'mes_critico': mes_critico,
            'runway_minimo': runway_minimo,
            'pior_queda': pior_queda,
            'mes_pior_queda': mes_pior_queda,
            'meses_criticos': meses_criticos,
            'meses_atencao': meses_atencao,
            'meses_seguros': meses_seguros,
            'primeiro_critico': primeiro_critico,
            'pct_marketing': pct_marketing,
            'pct_pessoal': pct_pessoal,
            'pct_infra': pct_infra,
            'pct_outros': max(0, pct_outros),
            'corr_caixa_burn': corr_caixa_burn,
            'taxa_cobertura': taxa_cobertura,
            'burn_medio': burn_medio
        }
    
    return metricas


def plotar_analise_runway_profunda(metricas, premissas, report_mode=False, mc_runway_percentis=None):
    """
    Gera visualização multi-painel com profundidade analítica:
    
    PAINEL 1: Trajetória de Runway (3 cenários + MC Percentis)
    - Linhas de runway ao longo do tempo
    - Bandas de zona crítica (< 3 meses) e atenção (3-6 meses)
    - Marcação do ponto mais crítico
    - V2.0: Linhas P10/P50/P90 do Monte Carlo
    
    PAINEL 2: Decomposição do Burn Rate
    - Stacked area mostrando o que consome o caixa
    - Marketing vs Pessoal vs Infra vs Outros
    
    PAINEL 3: Correlação Caixa × Burn Rate
    - Scatter plot mostrando a relação
    - Linha de tendência
    """
    
    figsize = (10, 12) if report_mode else (14, 14)
    fig = plt.figure(figsize=figsize, dpi=150)
    
    # Grid: 3 linhas (Painel 1 Topo, Painéis 2-3 Meio, Tabela Baixo)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.3, 1, 0.4], hspace=0.45, wspace=0.25)
    
    cores = {'Real': '#2563EB', 'Ideal': '#10B981', 'Estresse': '#EF4444'}
    meses = np.arange(1, 37)
    
    # =========================================================================
    # PAINEL 1: TRAJETÓRIA DE RUNWAY (ocupa as 2 colunas)
    # =========================================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    # Zonas de risco (fundo)
    ax1.axhspan(0, 3, alpha=0.15, color='red', label='Zona Crítica (<3m)')
    ax1.axhspan(3, 6, alpha=0.10, color='orange', label='Zona Atenção (3-6m)')
    ax1.axhspan(6, 36, alpha=0.05, color='green', label='Zona Segura (>6m)')
    
    # =========================================================================
    # V2.0: LINHAS P10/P50/P90 DO MONTE CARLO (antes das linhas determinísticas)
    # =========================================================================
    if mc_runway_percentis is not None:
        mc_meses = mc_runway_percentis['meses']
        p10 = mc_runway_percentis['P10']
        p50 = mc_runway_percentis['P50']
        p90 = mc_runway_percentis['P90']
        
        # Faixa P10-P90 (área sombreada)
        ax1.fill_between(mc_meses, p10, p90, alpha=0.15, color='#6366F1', 
                        label='MC: P10-P90 (80% cenários)')
        
        # Linha P50 (mediana MC)
        ax1.plot(mc_meses, p50, color='#6366F1', linewidth=2, linestyle='--',
                label='MC: P50 (Mediana)', alpha=0.8)
    
    # Linhas de runway determinísticas
    for nome, cor in cores.items():
        if nome in metricas:
            m = metricas[nome]
            runway = m['runway'][:36]
            ax1.plot(meses[:len(runway)], runway, color=cor, linewidth=2.5, 
                    label=f'{nome}', marker='o', markersize=3, alpha=0.9)
            
            # Marcar ponto crítico
            mes_crit = m['mes_critico']
            if mes_crit <= len(runway):
                ax1.scatter([mes_crit], [runway[mes_crit-1]], color=cor, s=150, 
                           zorder=5, edgecolors='black', linewidth=2)
                ax1.annotate(f'M{mes_crit}: {runway[mes_crit-1]:.1f}m', 
                           xy=(mes_crit, runway[mes_crit-1]),
                           xytext=(mes_crit+2, runway[mes_crit-1]+2),
                           fontsize=9, fontweight='bold',
                           arrowprops=dict(arrowstyle='->', color=cor, lw=1.5))
    
    # Linhas de threshold
    ax1.axhline(y=3, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.axhline(y=6, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.axhline(y=12, color='green', linestyle='--', linewidth=1, alpha=0.5)
    
    ax1.set_xlim(1, 36)
    ax1.set_ylim(0, min(36, max([metricas[n]['runway'].max() for n in metricas]) * 1.1))
    ax1.set_xlabel('Mês', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Runway (meses de sobrevivência)', fontsize=11, fontweight='bold')
    
    # Título dinâmico baseado em se temos MC ou não
    titulo_mc = " + Monte Carlo P10/P50/P90" if mc_runway_percentis else ""
    ax1.set_title(f'TRAJETÓRIA DE RUNWAY: Real vs Ideal vs Estresse{titulo_mc}\n' +
                 'Quanto tempo a empresa sobrevive se a receita parar?', 
                 fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', fontsize=9, ncol=2)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(1, 37, 3))
    
    # =========================================================================
    # PAINEL 2: DECOMPOSIÇÃO DO BURN RATE (coluna esquerda)
    # =========================================================================
    ax2 = fig.add_subplot(gs[1, 0])
    
    if 'Real' in metricas:
        m = metricas['Real']
        categorias = ['Marketing', 'Pessoal', 'Infra', 'Outros']
        valores = [m['pct_marketing'], m['pct_pessoal'], m['pct_infra'], m['pct_outros']]
        cores_cat = ['#EF4444', '#3B82F6', '#8B5CF6', '#6B7280']
        
        # Ordenar por valor
        sorted_idx = np.argsort(valores)[::-1]
        categorias = [categorias[i] for i in sorted_idx]
        valores = [valores[i] for i in sorted_idx]
        cores_cat = [cores_cat[i] for i in sorted_idx]
        
        bars = ax2.barh(categorias, valores, color=cores_cat, edgecolor='white', linewidth=1.5)
        
        # Adicionar valores
        for bar, val in zip(bars, valores):
            width = bar.get_width()
            ax2.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=11, fontweight='bold')
        
        ax2.set_xlabel('% do Burn Rate Mensal', fontsize=11, fontweight='bold')
        ax2.set_title(f'O QUE ESTÁ "COMENDO" O CAIXA?\nBurn Médio: {formata_moeda(m["burn_medio"])}/mês',
                     fontsize=12, fontweight='bold')
        ax2.set_xlim(0, max(valores) * 1.2 if max(valores) > 0 else 100)
        ax2.grid(True, alpha=0.3, axis='x')
    
    # =========================================================================
    # PAINEL 3: GAP DE RESILIÊNCIA (coluna direita)
    # =========================================================================
    ax3 = fig.add_subplot(gs[1, 1])
    
    if 'Real' in metricas and 'Ideal' in metricas:
        real_m = metricas['Real']
        ideal_m = metricas['Ideal']
        
        # Gap = Ideal - Real (quanto estamos deixando na mesa)
        gap_runway = ideal_m['runway'] - real_m['runway']
        
        # Plotar gap
        positivo = np.maximum(gap_runway, 0)
        negativo = np.minimum(gap_runway, 0)
        
        ax3.fill_between(meses[:len(gap_runway)], 0, positivo, 
                        alpha=0.5, color='#10B981', label='Ideal > Real (✅ Oportunidade)')
        ax3.fill_between(meses[:len(gap_runway)], 0, negativo, 
                        alpha=0.5, color='#EF4444', label='Real > Ideal (⚠️ Conservador)')
        ax3.axhline(y=0, color='black', linewidth=1.5)
        
        # Estatísticas do gap
        gap_medio = gap_runway.mean()
        gap_maximo = gap_runway.max()
        mes_gap_max = np.argmax(gap_runway) + 1
        
        ax3.set_xlabel('Mês', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Gap de Runway (meses)', fontsize=11, fontweight='bold')
        ax3.set_title(f'GAP REAL vs IDEAL: Quanto runway estamos "perdendo"?\n' +
                     f'Gap médio: {gap_medio:.1f} meses | Máximo: {gap_maximo:.1f}m (M{mes_gap_max})',
                     fontsize=12, fontweight='bold')
        ax3.legend(loc='upper right', fontsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(1, 36)
    
    # =========================================================================
    # PAINEL 4: COMPARATIVO FINAL (Minilinha inferior)
    # =========================================================================
    ax5 = fig.add_subplot(gs[2, :])
    
    # Tabela visual de comparação
    cenarios = ['Real', 'Ideal', 'Estresse']
    metricas_labels = ['Runway Mínimo', 'Mês Crítico', '% Meses <3m', 'Burn Médio']
    
    data = []
    for c in cenarios:
        if c in metricas:
            m = metricas[c]
            pct_crit = (m['meses_criticos'] / 36) * 100
            data.append([
                f"{m['runway_minimo']:.1f}m",
                f"M{m['mes_critico']}",
                f"{pct_crit:.0f}%",
                f"{m['burn_medio']/1000:.1f}k"
            ])
        else:
            data.append(['N/A'] * 4)
    
    ax5.axis('off')
    
    # Criar tabela - V3.0: Escala reduzida e posicionada no topo para evitar sobreposição
    table = ax5.table(
        cellText=np.array(data).T.tolist(),
        rowLabels=metricas_labels,
        colLabels=cenarios,
        cellLoc='center',
        loc='upper center',  # Mudou de 'center' para 'upper center'
        colColours=['#DBEAFE', '#D1FAE5', '#FEE2E2'],
        rowColours=['#F3F4F6'] * 4
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)  # Reduzido de 11 para 9
    table.scale(0.8, 1.2)  # V3.0: Reduzido de (1.0, 1.5) para (0.8, 1.2)
    
    # Colorir células baseado em valor
    for i in range(3):  # colunas
        for j in range(4):  # linhas
            cell = table[(j+1, i)]
            if j == 0:  # Runway mínimo
                if data[i][j] != 'N/A':
                    val = float(data[i][j].replace('m', ''))
                    if val < 3:
                        cell.set_facecolor('#FEE2E2')
                    elif val < 6:
                        cell.set_facecolor('#FEF3C7')
                    else:
                        cell.set_facecolor('#D1FAE5')
    
    ax5.set_title('COMPARATIVO DE RESILIÊNCIA', fontsize=12, fontweight='bold', pad=5)
    
    plt.tight_layout(pad=2.0)  # Aumentado padding para evitar sobreposição
    return fig


def gerar_tabela_analise_runway(metricas, premissas):
    """Gera tabela de análise profunda de runway."""
    
    rows = []
    for nome in ['Real', 'Ideal', 'Estresse']:
        if nome not in metricas:
            continue
        m = metricas[nome]
        
        # Calcular indicadores derivados
        resiliencia = 'Alta' if m['meses_criticos'] == 0 else ('Média' if m['meses_criticos'] < 6 else 'Baixa')
        risco_emoji = '🟢' if resiliencia == 'Alta' else ('🟡' if resiliencia == 'Média' else '🔴')
        
        rows.append({
            'Cenário': nome,
            'Runway Mínimo': f"{m['runway_minimo']:.1f} meses",
            'Mês Crítico': f"M{m['mes_critico']}",
            'Meses <3m': f"{m['meses_criticos']} ({m['meses_criticos']/36*100:.0f}%)",
            'Burn Médio': formata_moeda(m['burn_medio']) + '/mês',
            'Cobertura': f"{m['taxa_cobertura']*100:.0f}%",
            'Driver Principal': f"Marketing {m['pct_marketing']:.0f}%" if m['pct_marketing'] > 30 else f"Pessoal {m['pct_pessoal']:.0f}%",
            'Resiliência': f"{risco_emoji} {resiliencia}"
        })
    
    return pd.DataFrame(rows)


def gerar_insight_runway_profundo(metricas, premissas):
    """
    Gera insight estratégico profundo no padrão Tornado Plot.
    """
    
    if 'Real' not in metricas:
        return {'fato': 'Dados insuficientes', 'causa': '-', 'implicacao': '-', 'acao': '-'}
    
    real = metricas['Real']
    ideal = metricas.get('Ideal', {})
    stress = metricas.get('Estresse', {})
    
    # Métricas principais
    runway_min = real['runway_minimo']
    mes_crit = real['mes_critico']
    meses_criticos = real['meses_criticos']
    burn_medio = real['burn_medio']
    cobertura = real['taxa_cobertura']
    driver_principal = 'Marketing' if real['pct_marketing'] > real['pct_pessoal'] else 'Pessoal'
    driver_pct = max(real['pct_marketing'], real['pct_pessoal'])
    
    # Gap com ideal
    gap_runway = 0
    if ideal:
        gap_runway = ideal['runway_minimo'] - real['runway_minimo']
    
    # Vulnerabilidade do estresse
    stress_delta = 0
    if stress:
        stress_delta = real['meses_criticos'] - stress.get('meses_criticos', 0)
    
    # =========================================================================
    # FATO - O que os números dizem (DETALHADO)
    # =========================================================================
    if meses_criticos == 0:
        fato = (
            f"O modelo apresenta **zero meses críticos** (runway < 3 meses) ao longo dos 36 meses. "
            f"O ponto de menor resiliência ocorre no **mês {mes_crit}**, quando o runway atinge "
            f"**{runway_min:.1f} meses** de sobrevivência. A taxa de cobertura média (receita/custos) "
            f"é de **{cobertura*100:.0f}%**, indicando que a receita cobre **{cobertura*100:.0f}%** "
            f"dos custos operacionais."
        )
    elif meses_criticos < 6:
        fato = (
            f"Identificamos **{meses_criticos} meses críticos** (runway < 3 meses), concentrados "
            f"principalmente no período M1-M{mes_crit}. O pior momento ocorre no **mês {mes_crit}** "
            f"com apenas **{runway_min:.1f} meses** de caixa. O burn rate médio de "
            f"**{formata_moeda(burn_medio)}/mês** consome o caixa antes da receita estabilizar."
        )
    else:
        fato = (
            f"⚠️ **ALERTA ESTRUTURAL:** O modelo apresenta **{meses_criticos} meses críticos** "
            f"(runway < 3 meses), o que representa **{meses_criticos/36*100:.0f}%** do período total. "
            f"O ponto mais vulnerável é o **mês {mes_crit}** com runway de apenas **{runway_min:.1f} meses**. "
            f"A taxa de cobertura de **{cobertura*100:.0f}%** indica que a receita não cobre os custos."
        )
    
    # Adicionar comparação com cenários
    if gap_runway > 0:
        fato += (
            f"\n\n📊 **Gap com Cenário Ideal:** O modelo Real está **{gap_runway:.1f} meses** "
            f"abaixo do potencial. Isso representa oportunidade de melhoria via otimização "
            f"de custos ou aceleração de receita."
        )
    
    # =========================================================================
    # CAUSA - Por que isso acontece (DETALHADO)
    # =========================================================================
    causa = (
        f"O driver principal do burn rate é **{driver_principal}**, responsável por "
        f"**{driver_pct:.0f}%** das saídas de caixa mensais. "
    )
    
    if real['pct_marketing'] > 30:
        causa += (
            f"O investimento agressivo em marketing ({real['pct_marketing']:.0f}% do burn) "
            f"ocorre **antes** do payback dos clientes adquiridos, criando uma curva J típica "
            f"de startups em fase de growth. "
        )
    
    if real['pct_pessoal'] > 40:
        causa += (
            f"A estrutura de pessoal representa {real['pct_pessoal']:.0f}% do burn, "
            f"indicando modelo intensivo em capital humano com curva de diluição lenta. "
        )
    
    if cobertura < 0.8:
        causa += (
            f"Com cobertura de apenas {cobertura*100:.0f}%, cada mês de operação consome "
            f"**{formata_moeda((1-cobertura) * burn_medio)}** do caixa antes de atingir break-even."
        )
    elif cobertura >= 1.0:
        causa += (
            f"Com cobertura de {cobertura*100:.0f}%, o modelo já opera em regime de "
            f"**auto-financiamento** após o período inicial de investimento."
        )
    
    # =========================================================================
    # IMPLICAÇÃO - O que significa para o negócio (PRÁTICO)
    # =========================================================================
    if meses_criticos == 0 and cobertura >= 0.9:
        implicacao = (
            f"✅ **Modelo Robusto:** O negócio tem **proteção estrutural** contra "
            f"volatilidade de curto prazo. Mesmo no pior mês (M{mes_crit}), há margem "
            f"de {runway_min:.1f} meses para correção de rota sem risco de death spiral."
        )
    elif meses_criticos < 6:
        primeiro_crit = real.get('primeiro_critico', mes_crit)
        implicacao = (
            f"⚠️ **Janela de Vulnerabilidade:** Entre M1 e M{primeiro_crit or mes_crit}, "
            f"o modelo opera com margem apertada. Qualquer atraso em receita ou "
            f"aumento inesperado de custos pode acionar espiral de morte. "
            f"**Probabilidade de precisar de capital bridge: Alta.**"
        )
    else:
        implicacao = (
            f"🔴 **Modelo Frágil:** Com {meses_criticos} meses críticos, o negócio depende "
            f"de **execução perfeita** e **zero imprevistos** para sobreviver. "
            f"O risco de insolvência é estrutural, não conjuntural."
        )
    
    # Adicionar análise de sensibilidade
    if stress and stress.get('meses_criticos', 0) > meses_criticos:
        stress_criticos = stress.get('meses_criticos', 0)
        resiliencia_stress = "baixa" if stress_criticos > 12 else "moderada"
        implicacao += (
            f"\n\n🔥 **Teste de Estresse:** Sob condições adversas (churn 2x, CAC 1.5x), "
            f"os meses críticos saltam de {meses_criticos} para **{stress_criticos}**. "
            f"Isso expõe {resiliencia_stress} resiliência a choques."
        )
    
    # =========================================================================
    # AÇÃO RECOMENDADA - O que fazer (ESPECÍFICO)
    # =========================================================================
    if meses_criticos == 0:
        acao = (
            f"✅ **MANTER CURSO ATUAL:**\n"
            f"1. Continuar monitoramento mensal do runway\n"
            f"2. Considerar aceleração de growth se runway > 6 meses\n"
            f"3. Criar reserva estratégica de {formata_moeda(burn_medio * 3)} (3 meses de burn)"
        )
    elif meses_criticos < 6:
        primeiro_crit = real.get('primeiro_critico', mes_crit)
        mes_captacao = max(1, (primeiro_crit or mes_crit) - 3)
        acao = (
            f"⚠️ **AÇÃO PREVENTIVA (Prioridade Moderada):**\n"
            f"1. **CAPTAÇÃO:** Iniciar processo no M{mes_captacao} (3 meses antes do vale)\n"
            f"2. **CUSTO:** Revisar {driver_principal.lower()} — representa {driver_pct:.0f}% do burn\n"
            f"3. **BUFFER:** Criar reserva de {formata_moeda(burn_medio * 6)} antes de M{primeiro_crit or mes_crit}\n"
            f"4. **TRIGGER:** Se runway < 4 meses em qualquer momento → ativar plano de contingência"
        )
    else:
        acao = (
            f"🔴 **AÇÃO URGENTE (Prioridade Máxima):**\n"
            f"1. **IMEDIATO:** Cortar {driver_principal.lower()} em 30% (economia de {formata_moeda(burn_medio * driver_pct/100 * 0.3)}/mês)\n"
            f"2. **CURTO PRAZO:** Buscar capital bridge de {formata_moeda(burn_medio * 6)} nas próximas 4 semanas\n"
            f"3. **RENEGOCIAR:** Alongar prazos com fornecedores para preservar caixa\n"
            f"4. **PIVOT:** Avaliar modelo de receita — cobertura de {cobertura*100:.0f}% é insustentável"
        )
    
    return {
        'fato': fato,
        'causa': causa,
        'implicacao': implicacao,
        'acao': acao
    }


def render_ato3_heatmap_runway(df_real_m, df_ideal_m, df_stress_m, premissas, mc_results=None, report_mode=False):
    """
    Renderiza Ato 3 completo: Análise de Resiliência de Runway.
    Segue padrão Gold Standard V22.0 com profundidade analítica.
    
    V2.0: Agora aceita mc_results para adicionar linhas P10/P50/P90 do Monte Carlo.
    """
    
    # =========================================================================
    # 0. CABEÇALHO
    # =========================================================================
    if not report_mode:
        print("\n" + "="*80)
        print("🛡️ ATO 3: ANÁLISE DE RESILIÊNCIA DE RUNWAY")
        print("="*80)
    else:
        display(Markdown("***"))
        display(Markdown("## 🛡️ ATO 3: Análise de Resiliência de Runway"))
        display(Markdown('*"Por quanto tempo sobrevivemos se tudo der errado?"*'))
    
    # =========================================================================
    # 1. CÁLCULO DAS MÉTRICAS PROFUNDAS
    # =========================================================================
    if not report_mode:
        print("📊 Calculando métricas profundas de runway...")
    
    metricas = calcular_metricas_runway_profundas(df_real_m, df_ideal_m, df_stress_m, premissas)
    
    if not metricas:
        display(Markdown("⚠️ Erro: dados insuficientes para análise."))
        return None
    
    # =========================================================================
    # 1B. CALCULAR PERCENTIS DO MONTE CARLO (V2.0 - RUNWAY PROBABILÍSTICO)
    # =========================================================================
    mc_runway_percentis = None
    if mc_results is not None and 'caixa_series' in mc_results.columns:
        try:
            # Extrair séries de caixa de cada simulação
            series_list = mc_results['caixa_series'].tolist()
            valid_series = [s for s in series_list if isinstance(s, (list, np.ndarray)) and len(s) > 0]
            
            if len(valid_series) > 10:
                series_matrix = np.array(valid_series)
                n_meses = series_matrix.shape[1]
                
                # Calcular burn rate médio por simulação (aproximado)
                # Burn = diferença média de caixa mês a mês quando negativa
                burn_approx = premissas.get('custos_operacionais_mensais', 3000)
                
                # Calcular runway por mês: caixa / burn
                runway_p10 = np.percentile(series_matrix, 10, axis=0) / max(burn_approx, 100)
                runway_p50 = np.percentile(series_matrix, 50, axis=0) / max(burn_approx, 100)
                runway_p90 = np.percentile(series_matrix, 90, axis=0) / max(burn_approx, 100)
                
                # Limitar a valores razoáveis (0-36 meses)
                runway_p10 = np.clip(runway_p10, 0, 36)
                runway_p50 = np.clip(runway_p50, 0, 36)
                runway_p90 = np.clip(runway_p90, 0, 36)
                
                mc_runway_percentis = {
                    'meses': np.arange(1, n_meses + 1),
                    'P10': runway_p10,
                    'P50': runway_p50,
                    'P90': runway_p90
                }
                if not report_mode:
                    print("   ✅ Percentis MC de Runway calculados!")
        except Exception as e:
            if not report_mode:
                print(f"   ⚠️ Erro ao calcular percentis MC: {e}")
    
    # =========================================================================
    # 2. VISUALIZAÇÃO MULTI-PAINEL
    # =========================================================================
    fig = plotar_analise_runway_profunda(metricas, premissas, report_mode, mc_runway_percentis)
    display(fig)
    display(Markdown(""))
    display(Markdown("_Fonte: df_real_m (5A), df_ideal_m (5B), df_stress_m (5C), mc_results (5D) | Motor V13 | Célula 4_"))
    plt.close(fig)
    
    # =========================================================================
    # 3. COMO LER ESTA ANÁLISE (DETALHADO COMO O TORNADO)
    # =========================================================================
    real = metricas.get('Real', {})
    runway_min = real.get('runway_minimo', 0)
    mes_crit = real.get('mes_critico', 1)
    
    como_ler = f"""
::: {{.callout-note title="📖 COMO LER A ANÁLISE DE RESILIÊNCIA DE RUNWAY" collapse="false"}}

### O que é essa análise?
Você tem razão: o Runway deve mostrar a **segurança real**. Por isso, ajustamos o cálculo para o cenário "Pior Caso": **Zero Revenue Runway**.
Isso responde: *"Se todos os clientes cancelarem hoje e a receita for a zero, quantos meses eu pago as contas com o que tenho no banco?"*

Isso explica por que o gráfico oscila em vez de "explodir" para 36 meses. Mesmo lucrando, se seu caixa for baixo e seus custos altos, seu risco de **morte súbita** (caso a receita pare) é alto.

*(Seu Runway 'Zero Revenue' Mínimo: **{runway_min:.1f} meses** no mês **M{mes_crit}**)*

---

### 📊 PAINEL 1 - Trajetória de Runway (Gráfico Principal)

Este é o coração da análise. Mostra a evolução do runway ao longo de 36 meses em **3 cenários determinísticos** + **intervalo de confiança Monte Carlo**:

**Linhas Sólidas (Cenários Determinísticos):**
- 🔵 **Linha Azul (Real):** Trajetória usando suas premissas atuais (bootstrap conservador)
- 🟢 **Linha Verde (Ideal):** O que aconteceria se você atingisse benchmarks de mercado
- 🔴 **Linha Vermelha (Estresse):** Cenário adverso com churn 2x maior e CAC 1.5x mais caro

**Linhas Tracejadas (Monte Carlo - Análise Probabilística):**
- 💜 **Linha Roxa Tracejada (P50 - Mediana):** O resultado "típico" — 50% das simulações ficam acima e 50% abaixo desta linha. Use esta linha para planejamento realista.
- 💜 **Área Sombreada Roxa (P10-P90):** O "corredor de confiança" — 80% das simulações caem dentro desta faixa. Quanto mais larga a faixa, maior a incerteza do modelo.

**Zonas de Risco (Fundo Colorido):**
- 🔴 **Zona Vermelha (<3 meses):** Perigo iminente — você tem menos de 90 dias para reagir
- 🟡 **Zona Laranja (3-6 meses):** Atenção — hora de buscar capital ou otimizar custos
- 🟢 **Zona Verde (>6 meses):** Seguro — você pode focar em crescimento

**💡 Dica de Leitura:** Procure o ponto mais baixo da linha azul (Real). É ali que sua empresa estará mais vulnerável. Se esse ponto estiver na zona vermelha, você precisa agir AGORA.

---

### 📊 PAINEL 2 - Decomposição do Burn Rate

Responde à pergunta: **"O que está comendo meu caixa?"**

As barras mostram a participação percentual de cada categoria nas saídas de caixa:
- **Marketing:** Investimento em aquisição de clientes (Ads, conteúdo, parcerias)
- **Pessoal:** Folha de pagamento, encargos, benefícios da equipe
- **Infra:** Servidores, ferramentas SaaS, custos técnicos fixos
- **Outros:** Administrativo, jurídico, impostos operacionais

**💡 Dica de Leitura:** Se uma barra domina mais de 50% do gráfico, esse é seu maior "vilão". É ali que um corte de 10-20% terá maior impacto no runway.

---

### 📊 PAINEL 3 - Gap Real vs Ideal

Mostra quanto runway você está **"deixando na mesa"** por não operar no benchmark de mercado.

- **Área Verde (Ideal > Real):** Representa oportunidade — se você melhorar eficiência, pode ganhar esses meses extras de runway
- **Área Rosa (Real > Ideal):** Significa que você está mais conservador que o benchmark — pode não ser ruim, mas talvez esteja crescendo devagar demais

**💡 Dica de Leitura:** Quanto maior a área verde, maior o potencial de melhoria. Se a área verde for grande nos meses iniciais, priorize otimização de custos antes de escalar marketing.

---

### 📊 PAINEL 4 - Tabela Comparativa

Resume as **métricas-chave de resiliência** dos 3 cenários lado a lado:
- **Runway Mínimo:** O pior momento de cada cenário
- **Mês Crítico:** Quando ocorre o ponto mais vulnerável
- **% Meses <3m:** Quantos meses você passa na "zona vermelha"
- **Burn Médio:** Quanto sai de caixa por mês em média

**💡 Dica de Leitura:** Compare a coluna "Real" com "Estresse". Se o estresse mostra muito mais meses críticos, seu modelo é frágil a choques externos.

---

### 🎯 Regras de Ouro para Decisão Gerencial

1. **Se a linha azul toca a zona vermelha:** Ative plano de contingência imediatamente
2. **Se P10-P90 (área roxa) é muito larga:** Seu modelo tem alta incerteza — reduza variáveis de risco
3. **Se a linha P50 está acima da linha Real:** A simulação Monte Carlo é mais otimista — revise suas premissas conservadoras
4. **Se Marketing > 50% do burn:** Seu CAC está caro — otimize antes de escalar
5. **Se o gap verde é grande nos meses iniciais:** Foque em eficiência operacional primeiro

:::
"""
    display(Markdown(como_ler))

    
    # =========================================================================
    # 4. TABELA DE ANÁLISE
    # =========================================================================
    df_tabela = gerar_tabela_analise_runway(metricas, premissas)
    
    display(Markdown(""))
    display(Markdown("### 📋 Tabela 5.3: Análise Comparativa de Resiliência"))
    display(Markdown(""))
    display(Markdown(df_tabela.to_markdown(index=False)))
    display(Markdown(""))
    
    # =========================================================================
    # 5. COMO LER A TABELA
    # =========================================================================
    como_ler_tabela = """
::: {.callout-tip title="📋 COMO LER ESTA TABELA" collapse="true"}

- **Runway Mínimo:** O pior momento — quanto menor, mais frágil o modelo
- **Mês Crítico:** Quando ocorre o pior momento — é ali que você precisa de caixa
- **Meses <3m:** Quantos meses o runway fica abaixo de 3 meses — deveria ser ZERO
- **Burn Médio:** Quanto sai de caixa por mês em média
- **Cobertura:** Receita ÷ Custos — ideal é ≥ 100% (break-even)
- **Driver Principal:** O maior vilão do burn rate — é onde você deve cortar se precisar
- **Resiliência:** 🟢 Alta (0 meses críticos) | 🟡 Média (1-5) | 🔴 Baixa (>5)

**Benchmarks:**
- Startups seed: Runway mínimo > 6 meses
- Startups Série A: Runway mínimo > 12 meses
- Cobertura mínima viável: > 70%

:::
"""
    display(Markdown(como_ler_tabela))
    
    # =========================================================================
    # 6. INSIGHT ESTRATÉGICO PROFUNDO
    # =========================================================================
    display(Markdown(""))
    display(Markdown("***"))
    
    insight = gerar_insight_runway_profundo(metricas, premissas)
    
    insight_md = f"""
::: {{.callout-important title="💡 INSIGHT ESTRATÉGICO - RESILIÊNCIA FINANCEIRA" icon=false}}

### FATO (O que os números dizem)
{insight['fato']}

### CAUSA (Por que isso acontece)
{insight['causa']}

### IMPLICAÇÃO (O que significa na prática)
{insight['implicacao']}

### AÇÃO RECOMENDADA (O que fazer agora)
{insight['acao']}

:::

"""
    display(Markdown(insight_md))
    
    # =========================================================================
    # 7. AUDITORIA TÉCNICA
    # =========================================================================
    audit = """
::: {.callout-note title="🔍 AUDITORIA TÉCNICA" collapse="true"}

### Metodologia
- **Runway:** `Caixa[t] / Burn_Rate[t]` — quantos meses o caixa sustenta o burn atual
- **Burn Rate:** `(COGS + OPEX) - Receita Líquida` — saída líquida de caixa mensal
- **Cobertura:** `Receita / (COGS + OPEX)` — % dos custos cobertos pela receita
- **Decomposição:** Participação % de cada categoria no burn total

### Classificação de Risco
- **Crítico (< 3 meses):** Risco iminente de insolvência
- **Atenção (3-6 meses):** Margem apertada, exige monitoramento
- **Seguro (> 6 meses):** Buffer adequado para growth

### Cenários
- **Real (5A):** Premissas conservadoras (bootstrap R$ 2k/mês marketing)
- **Ideal (5B):** Benchmarks de mercado (R$ 10k/mês marketing)
- **Estresse (5C):** Churn 2x, CAC 1.5x, Conversão 0.5x

### Fonte de Dados
- Motor Financeiro V13 (`celula_4_motor.py`)
- Cenários 5A, 5B, 5C (`celula_5A/5B/stress`)

:::
"""
    display(Markdown(audit))
    
    return {
        'metricas': metricas,
        'df_tabela': df_tabela,
        'insight': insight
    }




# ============================================================================
# SEÇÃO 4B: VEREDITO NARRATIVO (GOLD STANDARD V22.0)
# ============================================================================


def gerar_veredito_risco(df_real_m, mc_results, df_stress_m, ato1_results, report_mode=False):
    """
    Gera o veredito narrativo final da Página 5, conectando todos os Atos em uma conclusão.
    
    REGRA V22.0: Texto corrido (storytelling), NÃO lista de bullets.
    
    INPUTS:
        df_real_m: DataFrame Real mensal
        mc_results: DataFrame Monte Carlo
        df_stress_m: DataFrame Estresse
        ato1_results: Dict com resultados do Ato 1 (probabilidades, dados_mes6, etc)
        report_mode: Se True, formata para Quarto/DOCX
    """
    
    # =========================================================================
    # 1. EXTRAIR MÉTRICAS PARA A NARRATIVA (100% DINÂMICO)
    # =========================================================================
    
    # Probabilidades do Monte Carlo
    probs = ato1_results.get('probabilidades', {})
    prob_sobrevivencia = 1 - probs.get('prob_quebra', 0)
    var95 = probs.get('var95', 0)
    p50 = probs.get('p50', 0)
    
    # Dados do Mês 6 (Ponto de Decisão)
    dados_m6 = ato1_results.get('dados_mes6', {})
    prob_seguro_m6 = dados_m6.get('prob_seguro_m6', 0)
    p50_m6 = dados_m6.get('p50_m6', 0)
    
    # Cenário Estresse
    caixa_stress_final = df_stress_m['caixa'].iloc[-1] if 'caixa' in df_stress_m.columns else 0
    stress_sobrevive = caixa_stress_final > 0
    
    # Cenário Real
    caixa_real_final = df_real_m['caixa'].iloc[-1] if 'caixa' in df_real_m.columns else 0
    arr_real_final = df_real_m['arr'].iloc[-1] if 'arr' in df_real_m.columns else 0
    
    # Dispersão (mede incerteza)
    caixa_final_col = mc_results.get('caixa_final', mc_results.get('caixa', pd.Series([0])))
    p5 = caixa_final_col.quantile(0.05) if len(caixa_final_col) > 0 else 0
    p95 = caixa_final_col.quantile(0.95) if len(caixa_final_col) > 0 else 0
    dispersao = p95 - p5
    dispersao_relativa = dispersao / max(abs(p50), 1)
    
    # =========================================================================
    # 2. DETERMINAR STATUS GERAL
    # =========================================================================
    
    # Critérios de aprovação
    criterio_1_sobrevivencia = prob_sobrevivencia > 0.90  # >90% chance de caixa positivo
    criterio_2_mes6 = prob_seguro_m6 > 0.60  # >60% seguro no M6
    criterio_3_stress = stress_sobrevive  # Sobrevive ao estresse
    criterio_4_dispersao = dispersao_relativa < 4  # Incerteza controlada
    
    criterios_ok = sum([criterio_1_sobrevivencia, criterio_2_mes6, criterio_3_stress, criterio_4_dispersao])
    
    if criterios_ok >= 4:
        status_geral = "APROVADO"
        emoji_status = "✅"
        tendencia = "robusto e resiliente"
    elif criterios_ok >= 2:
        status_geral = "APROVADO COM RESSALVAS"
        emoji_status = "⚠️"
        tendencia = "funcional mas com margem apertada"
    else:
        status_geral = "REPROVADO"
        emoji_status = "🔴"
        tendencia = "frágil e dependente de execução perfeita"
    
    # =========================================================================
    # 3. CONSTRUIR NARRATIVA DINÂMICA (TEXTO CORRIDO)
    # =========================================================================
    
    # Diagnóstico do Mês 6
    if prob_seguro_m6 > 0.70:
        diagnostico_m6 = "seguro para continuar"
        recomendacao_m6 = "manter o curso atual"
    elif prob_seguro_m6 > 0.50:
        diagnostico_m6 = "viável mas exige atenção"
        recomendacao_m6 = "criar buffer de R$ 30-50k antes do mês 6"
    else:
        diagnostico_m6 = "crítico e arriscado"
        recomendacao_m6 = "revisar estrutura de custos ou buscar captação"
    
    # Diagnóstico do Estresse
    if stress_sobrevive:
        diagnostico_stress = f"sobrevive ao estresse, terminando com {formata_moeda(caixa_stress_final)}"
    else:
        diagnostico_stress = f"não sobrevive ao estresse (caixa final: {formata_moeda(caixa_stress_final)})"
    
    veredito_md = f"""
### 🏁 VEREDITO FINAL: GESTÃO DE RISCO (Status: {emoji_status} {status_geral})

A análise probabilística desta seção confirma que o modelo é **{tendencia}** para os próximos 36 meses.

Começamos com a **Simulação Monte Carlo** (Ato 1), que revelou uma probabilidade de sobrevivência 
de **{prob_sobrevivencia:.1%}** — ou seja, em {prob_sobrevivencia*100:.0f} de cada 100 futuros 
simulados, a startup termina com caixa positivo. O **P50 (mediana)** projeta um caixa final de 
**{formata_moeda(p50)}**, enquanto o **VaR 95%** (pior cenário nos 5% mais pessimistas) indica 
risco máximo de **{formata_moeda(var95)}**.

O **Ponto de Decisão no Mês 6** mostrou-se **{diagnostico_m6}**, com **{prob_seguro_m6:.1%}** de 
probabilidade de caixa acima de R$ 10k. A recomendação tática para este marco é: **{recomendacao_m6}**.

O **Cenário de Estresse** (Mundo C) aplicou multiplicadores adversos (churn 2x, CAC 1.5x, conversão 0.5x) 
e verificou que o modelo **{diagnostico_stress}**. {"Isso demonstra resiliência estrutural." if stress_sobrevive else "Isso indica fragilidade e necessidade de colchão de segurança."}

A **dispersão entre P5 e P95** foi de **{formata_moeda(dispersao)}** ({dispersao_relativa:.1f}x a mediana), 
indicando {"incerteza controlada e premissas confiáveis" if dispersao_relativa < 3 else "alta incerteza que exige revisão de premissas"}.

**CONCLUSÃO ESTRATÉGICA:**

O modelo {"passa" if "APROVADO" in status_geral else "não passa"} no teste de risco com nota 
**{criterios_ok}/4** nos critérios de robustez. {"A startup está pronta para acelerar com confiança." if criterios_ok >= 3 else "Recomenda-se aumentar runway antes de escalar agressivamente."} 
O gargalo principal identificado é {"a dispersão das premissas" if dispersao_relativa > 3 else "o cenário de estresse" if not stress_sobrevive else "nenhum crítico no momento"}.

**PRÓXIMOS PASSOS:**
1. {"Manter curso atual e executar conforme planejado" if criterios_ok >= 4 else "Criar buffer financeiro de R$ 30-50k antes do Mês 6"}
2. {"Monitorar métricas mensalmente" if criterios_ok >= 3 else "Revisar CAC e churn semanalmente nos primeiros 3 meses"}
3. {"Preparar deck para Série A" if criterios_ok >= 4 else "Focar em break-even antes de buscar investimento"}
"""
    
    # =========================================================================
    # 4. RENDERIZAÇÃO CONDICIONAL
    # =========================================================================
    
    if report_mode:
        # Quarto Callout para o Veredito
        callout_type = "tip" if "APROVADO" == status_geral else "warning" if "RESSALVAS" in status_geral else "important"
        display(Markdown(f"::: {{.callout-{callout_type}}}\n{veredito_md}\n:::"))
    else:
        display(Markdown(veredito_md))
    
    return {
        'status_geral': status_geral,
        'criterios_ok': criterios_ok,
        'prob_sobrevivencia': prob_sobrevivencia,
        'tendencia': tendencia
    }


# ============================================================================
# SEÇÃO 5: RENDERIZAÇÃO DA FASE 1 (Tabela + Cards)

def render_fase1_tabela_kpi(df_real_m, df_ideal_m, mc_results, df_stress_m, premissas, report_mode=False):
    """
    Renderiza a Fase 1 da Página 5: Tabela Executiva Master + KPI Cards.
    
    Esta é a entrada principal para a Fase 1.
    """
    
    if not report_mode:
        print("\n" + "="*80)
        print("📊 PÁGINA 5 - FASE 1: PAINEL EXECUTIVO DE RISCO")
        print("="*80)
    else:
        # Título removido para evitar duplicidade com cabeçalho Tier 5 do report
        pass
    
    # Gerar KPI Cards
    cards = gerar_kpi_cards_risco(mc_results, df_real_m)
    
    # Renderizar KPI Cards
    if report_mode:
        # Formato Markdown para Quarto/DOCX
        cards_md = """
| 🛡️ SOBREVIVÊNCIA | ⚠️ VAR 95% | 🚀 UPSIDE | 📊 DISPERSÃO |
|:---:|:---:|:---:|:---:|
| **{v1}** | **{v2}** | **{v3}** | **{v4}** |
| {s1} | {s2} | {s3} | {s4} |
| {d1} | {d2} | {d3} | {d4} |
| {st1} | {st2} | {st3} | {st4} |
""".format(
            v1=cards[0]['valor'], v2=cards[1]['valor'], v3=cards[2]['valor'], v4=cards[3]['valor'],
            s1=cards[0]['subtitulo'], s2=cards[1]['subtitulo'], s3=cards[2]['subtitulo'], s4=cards[3]['subtitulo'],
            d1=cards[0]['delta'], d2=cards[1]['delta'], d3=cards[2]['delta'], d4=cards[3]['delta'],
            st1=cards[0]['status'], st2=cards[1]['status'], st3=cards[2]['status'], st4=cards[3]['status']
        )
        display(Markdown(cards_md))
        
        # INSERÇÃO DO GLOSSÁRIO COMPLETO (Atualizado por feedback do usuário)
        glossario_md = """
::: {.callout-note title="📚 GLOSSÁRIO TÉCNICO: TERMOS DE RISCO E ESTATÍSTICA" collapse="false"}

### 1. CARDS DE RISCO

| Termo | Significado | Por que importa |
|-------|-------------|-----------------|
| **Sobrevivência** | % de simulações com caixa > R$ 0 no M36 | Probabilidade de não quebrar |
| **VaR (Value at Risk)** | Pior resultado nos 5% mais pessimistas | Quanto pode perder no cenário extremo |
| **CVaR (Conditional VaR)** | Média das perdas nos 5% piores cenários | Mais conservador que VaR |
| **Upside** | Diferença % entre P95 e P50 | Potencial de ganho se tudo der certo |
| **Dispersão** | Razão (P95-P5) / P50 | Mede a incerteza do modelo |

### 2. PERCENTIS (P5, P10, P25, P50, P75, P90, P95)

Os percentis dividem os resultados das simulações Monte Carlo em faixas:

| Percentil | Significado | Uso prático |
|-----------|-------------|-------------|
| **P5** | 5% piores cenários (VaR 95%) | Planejamento de contingência extrema |
| **P10** | 10% piores cenários | Orçamento conservador |
| **P25** | Limite inferior "normal" | 75% dos cenários superam este valor |
| **P50** | **MEDIANA** - Use para planejar | Resultado mais provável |
| **P75** | Limite superior "normal" | Apenas 25% superam este valor |
| **P90** | Cenário otimista realista | Meta stretch alcançável |
| **P95** | Top 5% (melhor caso) | Upside máximo provável |

### 3. MÉTRICAS FINANCEIRAS

| Termo | Fórmula | Benchmark |
|-------|---------|-----------|
| **NRR (Net Revenue Retention)** | (MRR fim + Expansão - Churn) / MRR início | > 100% = expansão |
| **Burn Rate** | Custos - Receita (saída líquida mensal) | < R$ 0 = lucrando |
| **Runway** | Caixa ÷ Burn Rate | > 12 meses = seguro |
| **Desvio Padrão (σ)** | Dispersão dos resultados | Alto = incerteza |

### 4. LEITURA RÁPIDA

- **P50 é sua bússola:** Use como caso base para planejamento
- **P5 vs P50:** Se a diferença for grande, há muito risco
- **P50 vs P95:** Se a diferença for grande, há muito upside
- **Largura (P95-P5):** Mede a incerteza total do modelo

:::
"""
        display(Markdown(glossario_md))
    else:
        # Formato Console
        print("\n┌" + "─"*18 + "┬" + "─"*18 + "┬" + "─"*18 + "┬" + "─"*18 + "┐")
        print(f"│ {cards[0]['titulo']:^16} │ {cards[1]['titulo']:^16} │ {cards[2]['titulo']:^16} │ {cards[3]['titulo']:^16} │")
        print(f"│ {cards[0]['valor']:^16} │ {cards[1]['valor']:^16} │ {cards[2]['valor']:^16} │ {cards[3]['valor']:^16} │")
        print(f"│ {cards[0]['subtitulo']:^16} │ {cards[1]['subtitulo']:^16} │ {cards[2]['subtitulo']:^16} │ {cards[3]['subtitulo']:^16} │")
        print(f"│ {cards[0]['status']:^16} │ {cards[1]['status']:^16} │ {cards[2]['status']:^16} │ {cards[3]['status']:^16} │")
        print("└" + "─"*18 + "┴" + "─"*18 + "┴" + "─"*18 + "┴" + "─"*18 + "┘")
    
    # Gerar Tabela Executiva
    df_tabela = gerar_tabela_executiva_risco(df_real_m, df_ideal_m, mc_results, df_stress_m, premissas)
    
    # Renderizar Tabela
    if report_mode:
        tabela_md = df_tabela.to_markdown(index=False)
        display(Markdown("\n### 📋 TABELA EXECUTIVA MASTER DE RISCO\n"))
        display(Markdown(tabela_md))
        
        # Legenda
        display(Markdown("""
**LEGENDA:**
- 🟢 = Excelente (acima benchmark)
- 🟡 = Atenção (próximo ao limite)
- 🔴 = Crítico (abaixo benchmark)
"""))
    else:
        print("\n📋 TABELA EXECUTIVA MASTER DE RISCO")
        print("="*80)
        print(df_tabela.to_string(index=False))
        print("\n🟢 = Excelente | 🟡 = Atenção | 🔴 = Crítico")
    
    # Insight Dinâmico
    caixa_final = mc_results.get('caixa_final', mc_results.get('caixa', pd.Series([0])))
    prob_sobrevivencia = (caixa_final > 0).mean()
    
    # Comparar Real vs Monte Carlo P50 (Mediana)
    mc_arr = mc_results['arr_final'] if 'arr_final' in mc_results.columns else mc_results.get('arr', pd.Series([0]))
    mc_caixa = mc_results['caixa_final'] if 'caixa_final' in mc_results.columns else mc_results.get('caixa', pd.Series([0]))
    
    p50_arr = mc_arr.median()
    p50_caixa = mc_caixa.median()

    # Extrair valores do cenário Real (Necessário para a comparação)
    arr_real_final = df_real_m['arr'].iloc[-1] if 'arr' in df_real_m.columns else 0
    caixa_real_final = df_real_m['caixa'].iloc[-1] if 'caixa' in df_real_m.columns else 0
    
    # Delta Real vs P50
    delta_arr_pct = (arr_real_final / p50_arr - 1) if p50_arr > 0 else 0
    delta_caixa_pct = (caixa_real_final / p50_caixa - 1) if p50_caixa > 0 else 0
    
    insight_md = f"""
::: {{.callout-tip title="💡 INTERPRETAÇÃO RÁPIDA"}}

- ✅ **Risco de quebra:** {(1-prob_sobrevivencia):.1%} ({"< 5% - Excelente" if prob_sobrevivencia > 0.95 else "Atenção necessária"})
- ✅ **Cenário Real:** {"Atinge metas principais" if df_real_m['caixa'].iloc[-1] > 50000 else "Margem apertada"}
- ⚠️ **Dispersão:** {"Alta incerteza - revisar premissas" if (caixa_final.quantile(0.95) - caixa_final.quantile(0.05)) > 200000 else "Incerteza controlada"}
- 🔴 **Cenário Estresse:** {"Mostra fragilidade em churn dobrado" if df_stress_m['caixa'].iloc[-1] < 0 else "Modelo resiliente"}

:::

::: {{.callout-note title="📊 REAL (PROJETADO) vs P50 (MEDIANA MONTE CARLO)"}}

Esta análise verifica se sua projeção "Real" está otimista ou pessimista comparada à mediana das 100 simulações.

| Métrica M36 | 💰 Cenário Real (Você) | 🎲 Simulação P50 (Mediana) | Status |
|-------------|----------------------|---------------------------|--------|
| **ARR** | {formata_moeda(arr_real_final)} | {formata_moeda(p50_arr)} | {f'🟢 Acima da média (+{delta_arr_pct:.1%})' if delta_arr_pct > 0 else f'🟡 Conservador ({delta_arr_pct:.1%})'} |
| **Caixa Final** | {formata_moeda(caixa_real_final)} | {formata_moeda(p50_caixa)} | {f'🟢 Acima da média (+{delta_caixa_pct:.1%})' if delta_caixa_pct > 0 else f'🟡 Conservador ({delta_caixa_pct:.1%})'} |

**O QUE ISSO SIGNIFICA?**
*   **Conservador (Real < P50):** Sua projeção oficial é mais segura que a maioria dos cenários simulados. "Promete menos, entrega mais".
*   **Otimista (Real > P50):** Sua projeção assume que a execução será melhor que a média da sorte/azar. Exige atenção redobrada.
:::
"""

    
    if report_mode:
        display(Markdown(insight_md))
    else:
        print("\n💡 INTERPRETAÇÃO RÁPIDA:")
        print(f"   • Risco de quebra: {(1-prob_sobrevivencia):.1%}")
        print(f"   • Cenário Real: Caixa final = {formata_moeda(df_real_m['caixa'].iloc[-1])}")
        print(f"   • Cenário Estresse: Caixa final = {formata_moeda(df_stress_m['caixa'].iloc[-1])}")
        print(f"\n📊 REAL vs IDEAL (M36):")
        print(f"   • ARR Real: {formata_moeda(arr_real_final)} | ARR Ideal: {formata_moeda(arr_ideal_final)} ({arr_ratio:.1f}x)")
        print(f"   • Caixa Real: {formata_moeda(caixa_real_final)} | Caixa Ideal: {formata_moeda(caixa_ideal_final)}")
        print(f"   ⚠️ NOTA: Ideal usa estratégia agressiva (R$ 10k/mês em marketing) - caixa baixo é intencional")
    
    return df_tabela, cards


# ============================================================================
# EXECUTOR PRINCIPAL
# ============================================================================

def executar_pagina_5_risco(df_real_m, df_ideal_m, mc_results, premissas, 
                             df_real_s=None, df_ideal_s=None, motor_func=None,
                             report_mode=False):
    """
    Orquestra a geração da Página 5 completa.
    
    INPUTS:
        df_real_m: DataFrame Real mensal (36 linhas)
        df_ideal_m: DataFrame Ideal mensal (36 linhas)
        mc_results: DataFrame Monte Carlo (10k+ sims)
        premissas: Dicionário PREMISSAS
        df_real_s: DataFrame Real semanal (opcional, para Ato 3)
        df_ideal_s: DataFrame Ideal semanal (opcional)
        motor_func: Função do motor (opcional, para cenário estresse preciso)
        report_mode: Se True, formata para DOCX/PDF via Quarto
    
    NOTA FASE 1:
        Esta versão implementa apenas a Tabela Executiva Master + KPI Cards.
        Os Atos 1-5 serão implementados nas fases seguintes.
    """
    
    if not report_mode:
        print("\n" + "="*80)
        print("🚀 INICIANDO PÁGINA 5: RISCO & CENÁRIOS")
        print("="*80)
    else:
        # Título removido para evitar duplicidade com cabeçalho Tier 5 do report
        # display(Markdown("# PÁGINA 5: RISCO & CENÁRIOS"))
        pass
    
    # 1. Gerar Cenário Estresse (Mundo C)
    if not report_mode:
        print("\n⏳ Gerando Cenário de Estresse (5C)...")
    df_stress_m = gerar_cenario_estresse(df_real_m, premissas, motor_func)
    if not report_mode:
        print("   ✅ Cenário Estresse gerado com sucesso!")
    
    # 2. FASE 1: Tabela Executiva + KPI Cards
    df_tabela, cards = render_fase1_tabela_kpi(
        df_real_m, df_ideal_m, mc_results, df_stress_m, premissas, report_mode
    )
    
    # 3. ATO 1: Monte Carlo Fan Chart
    if not report_mode:
        print("\n" + "-"*40)
        print("� Gerando Ato 1: Monte Carlo Fan Chart...")
    
    ato1_results = render_ato1_fan_chart(
        mc_results, df_real_m, df_ideal_m, premissas, report_mode
    )
    
    if not report_mode:
        print("   ✅ Ato 1 gerado com sucesso!")
    
    # =========================================================================
    # 3B. VaR HISTOGRAM (NEW - V2.0 GOLD STANDARD)
    # =========================================================================
    if not report_mode:
        print("\n   📊 Gerando VaR Histogram...")
    
    try:
        var_result = render_var_histogram(mc_results, df_real_m, premissas, report_mode)
        if var_result and var_result[0] is not None:
            fig_var, var_data = var_result
            if report_mode:
                display(Markdown("***"))
                display(Markdown("### 📊 DISTRIBUIÇÃO DE RISCO (VaR)"))
                display(Markdown("![VaR Histogram](outputs/figs/pag5_var_histogram.png)"))
                display(Markdown(f"_Fonte: mc_results (Célula 5D) | {len(mc_results)} simulações_"))
                
                # Callout explicativo
                var_callout = f"""
::: {{.callout-note title="📖 COMO LER O HISTOGRAMA VAR" collapse="false"}}

**O QUE É VaR (Value at Risk)?**
O VaR responde: *"Nos 5% piores cenários, quanto posso perder?"*

**ZONAS DO GRÁFICO:**
- 🔴 **VERMELHO:** Cenários de quebra (caixa < R$ 0)
- 🟠 **LARANJA:** Cenários de risco (R$ 0 a R$ 50k)
- 🟢 **VERDE:** Cenários seguros (> R$ 50k)

**LINHAS DE REFERÊNCIA:**
- **VaR95:** {formata_moeda(var_data['var95'])} - pior resultado nos 5% mais pessimistas
- **CVaR95:** {formata_moeda(var_data['cvar95'])} - média dos 5% piores cenários
- **P50:** {formata_moeda(var_data['p50'])} - resultado mais provável

**INTERPRETAÇÃO RÁPIDA:**
- P(Quebra) = {var_data['prob_quebra']:.1%} → {"🟢 Risco baixo" if var_data['prob_quebra'] < 0.10 else "🔴 Risco elevado"}
:::
"""
                display(Markdown(var_callout))
            else:
                display(fig_var)
            plt.close(fig_var)
            if not report_mode:
                print("   ✅ VaR Histogram gerado!")
    except Exception as e:
        if not report_mode:
            print(f"   ⚠️ VaR Histogram não disponível: {e}")
    
    # =========================================================================
    # 3C. SURVIVAL CURVE (NEW - V2.0 GOLD STANDARD)
    # =========================================================================
    if not report_mode:
        print("\n   📈 Gerando Curva de Sobrevivência...")
    
    try:
        survival_result = render_survival_curve(mc_results, premissas, report_mode)
        if survival_result and survival_result[0] is not None:
            fig_surv, surv_data = survival_result
            if report_mode:
                display(Markdown("***"))
                display(Markdown("### 📈 CURVA DE SOBREVIVÊNCIA"))
                display(Markdown("![Survival Curve](outputs/figs/pag5_survival_curve.png)"))
                display(Markdown(f"_Fonte: mc_results (Célula 5D) | caixa_series por mês_"))
                
                # Callout explicativo
                surv_callout = f"""
::: {{.callout-note title="📖 COMO LER A CURVA DE SOBREVIVÊNCIA" collapse="false"}}

**O QUE ESTA CURVA MOSTRA?**
A probabilidade de sobrevivência (caixa > R$ 0) ao longo dos 36 meses.

**ZONAS COLORIDAS:**
- 🟢 **VERDE (>80%):** Zona segura - probabilidade alta de sobrevivência
- 🟡 **AMARELO (50-80%):** Zona de atenção - risco moderado
- 🔴 **VERMELHO (<50%):** Zona crítica - probabilidade de morte > 50%

**PONTOS-CHAVE:**
- **Mês mais crítico:** M{surv_data['mes_critico']} com {surv_data['prob_minima']:.1%} de sobrevivência
- **Mês 6 (decisão):** {surv_data['prob_m6']:.1%} de sobrevivência
- **Mês 36 (final):** {surv_data['prob_m36']:.1%} de sobrevivência

**INTERPRETAÇÃO:**
{"🟢 Trajetória saudável - sobrevivência consistente acima de 80%" if surv_data['prob_minima'] > 0.80 else "⚠️ Há período(s) de risco durante a trajetória" if surv_data['prob_minima'] > 0.50 else "🔴 Alta probabilidade de morte em algum momento da trajetória"}
:::
"""
                display(Markdown(surv_callout))
            else:
                display(fig_surv)
            plt.close(fig_surv)
            if not report_mode:
                print("   ✅ Curva de Sobrevivência gerada!")
    except Exception as e:
        if not report_mode:
            print(f"   ⚠️ Curva de Sobrevivência não disponível: {e}")
    
    # 4. ATO 2: Tornado Plot (Sensibilidade)
    if not report_mode:
        print("\n" + "-"*40)
        print("🌪️ Gerando Ato 2: Tornado Plot...")
        
    ato2_results = render_ato2_sensibilidade(premissas, report_mode, motor_func, met_real=None, df_real_m=df_real_m)
    
    if not report_mode:
        print("   ✅ Ato 2 gerado com sucesso!")


    # 5. ATO 3: Heatmap Runway Semanal
    if not report_mode:
        print("\n" + "-"*40)
        print("🗓️ Gerando Ato 3: Heatmap Runway...")
        
    ato3_results = render_ato3_heatmap_runway(
        df_real_m, df_ideal_m, df_stress_m, premissas, mc_results, report_mode
    )
    
    if not report_mode:
        print("   ✅ Ato 3 gerado com sucesso!")

    # 6. ATOS 4-5 + EXTRAS: Análises Finais (Import Dinâmico)
    try:
        # Tenta importar do módulo separado
        try:
            from .PAGINA_5_RISCO_ATO4_5 import (
                render_ato4_breakeven, render_ato5_gap_analysis, 
                render_ato_use_of_funds, render_ato_valuation_probabilistico
            )
        except ImportError:
            try:
                from celulas.PAGINA_5_RISCO_ATO4_5 import (
                    render_ato4_breakeven, render_ato5_gap_analysis,
                    render_ato_use_of_funds, render_ato_valuation_probabilistico
                )
            except ImportError:
                import PAGINA_5_RISCO_ATO4_5
                render_ato4_breakeven = PAGINA_5_RISCO_ATO4_5.render_ato4_breakeven
                render_ato5_gap_analysis = PAGINA_5_RISCO_ATO4_5.render_ato5_gap_analysis
                render_ato_use_of_funds = PAGINA_5_RISCO_ATO4_5.render_ato_use_of_funds
                render_ato_valuation_probabilistico = PAGINA_5_RISCO_ATO4_5.render_ato_valuation_probabilistico
    except Exception as e:
        print(f"⚠️ Erro ao importar Atos 4-5 + Extras: {e}")
        render_ato4_breakeven = None
        render_ato5_gap_analysis = None
        render_ato_use_of_funds = None
        render_ato_valuation_probabilistico = None
    
    ato4_results = None
    ato5_results = None
    
    if render_ato4_breakeven:
        # ATO 4
        if not report_mode:
            print("\n" + "-"*40)
            print("⚖️ Gerando Ato 4: Break-Even sob Estresse...")
            
        ato4_results = render_ato4_breakeven(
            df_real_m, df_ideal_m, df_stress_m, premissas, report_mode
        )
        
        if not report_mode:
            print("   ✅ Ato 4 gerado com sucesso!")
            
        # ATO 5
        if not report_mode:
            print("\n" + "-"*40)
            print("📉 Gerando Ato 5: Gap Analysis...")
            
        ato5_results = render_ato5_gap_analysis(
            df_real_m, df_stress_m, premissas, motor_func, report_mode
        )
        
        if not report_mode:
            print("   ✅ Ato 5 gerado com sucesso!")

        # ATO EXTRA 1: USE OF FUNDS
        if render_ato_use_of_funds:
            render_ato_use_of_funds(df_real_m, premissas, report_mode)
            
        # ATO EXTRA 2: VALUATION PROBABILÍSTICO
        if render_ato_valuation_probabilistico:
            render_ato_valuation_probabilistico(df_real_m, mc_results, premissas, report_mode)


    
    # 5. VEREDITO NARRATIVO FINAL (GOLD STANDARD V22.0)
    if not report_mode:
        print("\n" + "-"*40)
        print("🏁 Gerando Veredito Final...")
    else:
        display(Markdown("***"))
    
    veredito_results = gerar_veredito_risco(
        df_real_m, mc_results, df_stress_m, ato1_results, report_mode
    )
    
    if not report_mode:
        print("   ✅ Veredito gerado com sucesso!")
        print("\n✅ PÁGINA 5 - ATOS 1-3 + VEREDITO GERADOS COM SUCESSO!")
    
    return RiskPageOutput({
        'df_stress_m': df_stress_m,
        'df_tabela_executiva': df_tabela,
        'kpi_cards': cards,
        'ato1': ato1_results,
        'ato2': ato2_results,
        'ato3': ato3_results,
        'ato4': ato4_results,
        'ato5': ato5_results,
        'veredito': veredito_results
    })



# ============================================================================
# EXECUÇÃO STANDALONE (para testes)
# ============================================================================

if __name__ == "__main__":
    print("Este módulo deve ser importado pelo notebook principal.")
    print("Exemplo de uso:")
    print("""
    from celulas.PAGINA_5_RISCO import executar_pagina_5_risco
    
    resultados = executar_pagina_5_risco(
        df_real_m=df_real_m,
        df_ideal_m=df_ideal_m,
        mc_results=mc_results,
        premissas=PREMISSAS,
        report_mode=False
    )
    """)
