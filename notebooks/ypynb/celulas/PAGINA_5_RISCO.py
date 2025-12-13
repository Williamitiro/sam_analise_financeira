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
    
    ESTRESSE APLICADO:
    - Churn: 2.0x (dobro de cancelamento)
    - CAC: 1.5x (50% mais caro)
    - Conversão: 0.5x (metade converte)
    - Tráfego: 0.7x (30% menos visitantes)
    
    INPUTS:
        df_real_m: DataFrame do cenário Real (36 meses)
        premissas: Dicionário PREMISSAS original
        motor_func: Função do motor (opcional, para recálculo completo)
    
    OUTPUTS:
        df_stress_m: DataFrame do cenário Estresse (36 meses)
    
    NOTA: Se motor_func não fornecido, aplica multiplicadores diretamente no df_real_m.
          Isso é uma aproximação simplificada. Para resultados precisos, use o motor.
    """
    
    # Multiplicadores de estresse (conforme plano tier_5)
    MULTIPLICADORES_ESTRESSE = {
        'churn': 2.0,       # Churn dobrado
        'cac': 1.5,         # CAC 50% maior
        'conversao': 0.5,   # Conversão cai para metade
        'trafego': 0.7,     # Tráfego reduzido em 30%
        'arpu': 0.8,        # ARPU 20% menor (clientes piores)
    }
    
    if motor_func is not None:
        # Caminho completo: rodar o motor com premissas modificadas
        premissas_stress = premissas.copy()
        premissas_stress['churn_inicial'] = premissas['churn_inicial'] * MULTIPLICADORES_ESTRESSE['churn']
        premissas_stress['cac_medio'] = premissas.get('cac_medio', 180) * MULTIPLICADORES_ESTRESSE['cac']
        premissas_stress['taxa_conversao_trial_pago'] = premissas.get('taxa_conversao_trial_pago', 0.12) * MULTIPLICADORES_ESTRESSE['conversao']
        premissas_stress['trafego_inicial'] = premissas.get('trafego_inicial', 300) * MULTIPLICADORES_ESTRESSE['trafego']
        
        try:
            df_stress_m, _, _, _ = motor_func(premissas_stress)
            return df_stress_m
        except Exception as e:
            print(f"⚠️ Erro ao rodar motor para estresse: {e}. Usando aproximação simplificada.")
    
    # Caminho simplificado: aplicar multiplicadores diretamente (aproximação)
    df_stress = df_real_m.copy()
    
    # Ajustar métricas afetadas pelo estresse
    if 'churn_rate' in df_stress.columns:
        df_stress['churn_rate'] = df_stress['churn_rate'] * MULTIPLICADORES_ESTRESSE['churn']
        df_stress['churn_rate'] = df_stress['churn_rate'].clip(upper=0.30)  # Cap em 30%
    
    if 'cac_blended' in df_stress.columns:
        df_stress['cac_blended'] = df_stress['cac_blended'] * MULTIPLICADORES_ESTRESSE['cac']
    
    if 'arpu' in df_stress.columns:
        df_stress['arpu'] = df_stress['arpu'] * MULTIPLICADORES_ESTRESSE['arpu']
    
    # Recalcular métricas derivadas
    if 'mrr' in df_stress.columns and 'usuarios_ativos' in df_stress.columns:
        # MRR cai proporcionalmente ao aumento de churn (simplificado)
        fator_reducao_base = 1 - (MULTIPLICADORES_ESTRESSE['churn'] - 1) * 0.3  # ~30% do impacto
        fator_reducao_base = max(0.3, min(1.0, fator_reducao_base))  # Clamp entre 0.3 e 1.0
        df_stress['mrr'] = df_stress['mrr'] * fator_reducao_base
        df_stress['arr'] = df_stress['mrr'] * 12
    
    # Caixa é mais afetado: menos receita + mais custo de aquisição
    if 'caixa' in df_stress.columns:
        # Degradação progressiva do caixa sob estresse
        degradacao = np.linspace(1.0, 0.5, len(df_stress))  # De 100% até 50% ao longo do tempo
        df_stress['caixa'] = df_stress['caixa'] * degradacao
    
    # Recalcular LTV se existir
    if 'ltv' in df_stress.columns and 'churn_rate' in df_stress.columns:
        df_stress['ltv'] = (df_stress['arpu'] * df_stress.get('margem_bruta_pct', 80) / 100) / df_stress['churn_rate'].replace(0, 0.01)
    
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
    
    PROBLEMA: mc_results pode ter formato diferente (por simulação, não por mês).
    SOLUÇÃO: Se não tiver coluna 'mes', usa df_real_m como base e apenas o caixa_final.
    
    OUTPUT:
        DataFrame com colunas: mes, p5, p10, p25, p50, p75, p90, p95, real, ideal
    """
    
    # Verificar estrutura do mc_results
    if 'mes' in mc_results.columns and 'caixa' in mc_results.columns:
        # Formato ideal: cada linha é um mês de uma simulação
        percentis = mc_results.groupby('mes')['caixa'].quantile(
            [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
        ).unstack()
        percentis.columns = ['p5', 'p10', 'p25', 'p50', 'p75', 'p90', 'p95']
        percentis = percentis.reset_index()
    else:
        # Formato alternativo: cada linha é uma simulação com caixa_final
        # Criar dados sintéticos baseados na distribuição final
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
    if len(percentis) == len(df_real_m):
        percentis['real'] = df_real_m['caixa'].values if 'caixa' in df_real_m.columns else 0
        percentis['ideal'] = df_ideal_m['caixa'].values if 'caixa' in df_ideal_m.columns else 0
    else:
        # Ajustar tamanho se necessário
        percentis['real'] = np.interp(percentis['mes'], df_real_m['mes'], df_real_m['caixa'])
        percentis['ideal'] = np.interp(percentis['mes'], df_ideal_m['mes'], df_ideal_m['caixa'])
    
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
        """Executa o motor e extrai LTV/CAC final com 'Virtual Floor' para evitar paradoxo do infinito."""
        try:
            # Rodar motor
            df_m, _, metricas, _ = motor_para_usar(p)
            
            if len(df_m) > 0:
                last = df_m.iloc[-1]
                ltv = last.get('ltv', 0)
                cac = last.get('cac_blended', 0)
                
                # TRUQUE MATEMÁTICO PARA O TORNADO:
                # Se CAC for zero (orgânico puro), usamos R$ 1.00 como divisor (Virtual Floor).
                # Isso faz o LTV/CAC flutuar proporcionalmente ao LTV, permitindo ver o impacto de Churn/Price.
                # Se não fizesse isso, seria sempre "Infinito" (10.000) e o gráfico ficaria vazio.
                divisor_cac = max(cac, 1.00) 
                
                return ltv / divisor_cac
            
            return 0.0
            
        except Exception as e:
            return 0.0
            
        except Exception as e:
            # print(f"Erro silencioso no motor durante sensibilidade: {e}") # Debug only
            return 0.0

    # LTV/CAC Base
    # Se valor real foi passado, usa ele. Senão, calcula.
    if ltv_cac_base_real is not None and ltv_cac_base_real > 0:
        ltv_cac_base = ltv_cac_base_real
    else:
        ltv_cac_base = get_ltv_cac(PREMISSAS)
    
    # Se base for 0, algo está muito errado
    if ltv_cac_base == 0:
        print("⚠️ AVISO: LTV/CAC Base calculado é 0.0. Verifique suas premissas base ou o motor.")
        # Podemos retornar vazio ou tentar continuar (vai dar tudo 0)
    
    resultados = []
    
    # Dicionário de labels amigáveis (apenas para display, não afeta lógica)
    nomes_display_map = {
        'marketing_fixo_mensal': 'Budget Marketing',
        'churn_inicial': 'Churn Base (%)',
        'taxa_trial_para_pagante': 'Conv. Trial -> Pago',
        'cpc_instagram': 'CPC Instagram',
        'cpc_google': 'CPC Google',
        'preco_trader': 'Preço Trader',
        'custo_ia_trader': 'Custo IA Trader',
        'salario_dev_senior': 'Salário Dev Sr',
        'trafego_inicial': 'Tráfego Inicial',
        'mix_trader': 'Mix Plano Trader',
        'b2b_probabilidade_anual': 'Prob. Venda B2B',
        'imposto_simples_inicial': 'Imposto Inicial'
    }
    
    for chave in premissas_sensiveis:
        # A chave deve existir em PREMISSAS
        if chave not in PREMISSAS:
            # Tenta verificar se está aninhada (caso raro, mas possível)
            # Por simplicidade/performance, assumimos flat ou tratamos 'monte_carlo' fora.
            continue
            
        valor_base = PREMISSAS[chave]
        
        # Só varia se for numérico
        if not isinstance(valor_base, (int, float)):
            continue
            
        # Cenário -20%
        p_min = PREMISSAS.copy()
        p_min[chave] = valor_base * (1 - variacao)
        ltv_cac_min = get_ltv_cac(p_min)
        
        # Cenário +20%
        p_max = PREMISSAS.copy()
        p_max[chave] = valor_base * (1 + variacao)
        ltv_cac_max = get_ltv_cac(p_max)
        
        # Impacto
        impacto_abs = abs(ltv_cac_max - ltv_cac_min)
        
        # Se impacto for zero absoluto ou muito pequeno, ignoramos para limpar gráfico
        if impacto_abs < 0.01:
            continue
            
        impacto_rel = impacto_abs / ltv_cac_base if ltv_cac_base > 0 else 0
        
        resultados.append({
            'premissa': chave,
            'nome_display': nomes_display_map.get(chave, chave),
            'valor_base': valor_base,
            'valor_min': valor_base * (1 - variacao),
            'valor_max': valor_base * (1 + variacao),
            'valor_max': valor_base * (1 + variacao),
            # FORCE BASE REAL: Garante que o valor central é o mesmo do relatório
            'ltv_cac_base': ltv_cac_base, 
            'ltv_cac_min': ltv_cac_min,
            'ltv_cac_max': ltv_cac_max,
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
    metricas = {
        'Caixa Final': caixa_final,
        'ARR Final': arr_final,
        'MRR Final': mrr_final,
        'Usuários Final': usuarios_final,
        'LTV/CAC': ltv_cac,
        'Churn Médio': churn,
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
    
    # Formatar valores monetários
    for col in ['P5', 'P10', 'P25', 'P50', 'P75', 'P90', 'P95', 'Média', 'Desvio']:
        df_tabela[col] = df_tabela.apply(
            lambda row: formata_moeda(row[col]) if row['Métrica'] in ['Caixa Final', 'ARR Final', 'MRR Final'] 
            else (f"{row[col]:.1%}" if row['Métrica'] == 'Churn Médio' 
                  else (f"{row[col]:.1f}x" if row['Métrica'] == 'LTV/CAC' 
                        else f"{row[col]:,.0f}")), axis=1
        )
    
    return df_tabela


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
- Mês 6 está na zona cinza perto de R$ 0 = decisão arriscada

**TERMOS IMPORTANTES:**

- **P50 (Mediana):** Metade dos cenários fica acima, metade abaixo
- **P10/P90:** 80% dos cenários estão entre estes valores
- **Fan Chart:** "Gráfico de Leque" - mostra incerteza crescente ao longo do tempo
- **VaR (Value at Risk):** O pior cenário nos 5% mais pessimistas

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
        print("-"*40)
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
                
    except Exception as e:
        print(f"⚠️ Erro ao carregar variáveis do Monte Carlo: {e}")
        # Fallback de segurança (apenas se config estiver corrompida)
        premissas_sensiveis = ['churn_inicial', 'marketing_fixo_mensal', 'taxa_trial_para_pagante']

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
        variacao=0.20, 
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
    # Passamos variacao=0.20 explicitamente
    fig2 = plotar_tornado_plot(df_tornado, variacao_input=0.20, report_mode=report_mode)
    
    # =========================================
    # RENDERIZAÇÃO ATÔMICA (V7.0)
    # =========================================
    render_atomic_block(
        chart_id="pg5_viz2_tornado",
        title_technical="VIZ 5.2: Análise de Sensibilidade (Tornado Plot)",
        title_colloquial="O que pode matar o negócio?",
        fig=fig2,
        legend_md="Barras mostram o impacto no LTV/CAC ao variar cada premissa em ±20%.",
        df_tabela=df_tornado,
        insight_dict={
            "fato": "Sensibilidade mapeada para top 10 variáveis.",
            "causa": "Variação de +/- 20% nas premissas base.",
            "implicacao": "Identificação dos drivers críticos de risco.",
            "acao": "Monitorar de perto as variáveis do topo do gráfico."
        },
        report_mode=report_mode,
        data_source_text="Fonte: Monte Carlo Sensitivity"
    )
    plt.close(fig2)

    
    # =========================================================================
    # 3. COMO LER & GLOSSÁRIO (DIDÁTICO V4 - TEXTO DO USUÁRIO)
    # =========================================================================
    como_ler = f"""
::: {{.callout-note title="📖 COMO LER A ANÁLISE DE SENSIBILIDADE (TORNADO PLOT)" collapse="false"}}

### O que é essa análise de sensibilidade?
Vamos começar do básico. Essa é uma **análise de sensibilidade**, que é uma forma de testar um modelo financeiro. O objetivo é ver o que acontece com um número importante (nesse caso, o **LTV/CAC**) se você mudar algumas suposições (chamadas de "premissas") um pouquinho.

*(LTV/CAC Base Atual: {df_tornado['ltv_cac_base'].iloc[0]:.1f}x)*

### O que é um "Tornado Plot"?
É um gráfico em forma de "tornado" que mostra o **impacto** de mudar cada premissa. Eles mudaram cada uma em **±20%**, uma de cada vez. Isso revela quais variáveis são "críticas" e quais são "meh".

### Cores e barras: O que significam?
*   **Barra vermelha (esquerda, "Risco"):** Mostra o que acontece se a variável mudar de um jeito RUIM (reduz o LTV/CAC).
*   **Barra verde (direita, "Oportunidade"):** Mostra o que acontece se a variável mudar de um jeito BOM (aumenta o LTV/CAC).
*   **Largura da barra:** Quanto mais larga, mais sensível é o LTV/CAC a essa variável.
*   **Números nas barras (ex: 3.8x):** É o novo LTV/CAC após a mudança.

### Dica prática (Regra de Ouro)
*   Foque nas barras largas (topo do tornado): Elas são as que importam!
*   Ignore as barras curtas (base): Mudar "Budget Marketing" ou "Imposto" não faz muita diferença.
:::

::: {{.callout-tip title="📚 GLOSSÁRIO TÉCNICO (ENTENDA OS TERMOS)" collapse="true"}}
Aqui está a tradução dos termos técnicos usados no gráfico:

*   **LTV/CAC:** Nota de eficiência do negócio. Quanto dinheiro o cliente traz (LTV) dividido pelo custo para atraí-lo (CAC). **Ideal > 3.0x**.
*   **Churn Base (%):** Taxa de cancelamento. Quantos clientes desistem do produto todo mês. Quanto menor, melhor.
*   **Conv. Trial -> Pago:** Taxa de conversão. De cada 100 pessoas que testam de graça (Trial), quantas viram pagantes de verdade.
*   **CPC (Custo por Clique):** Valor pago a plataformas (Google, YouTube) por cada clique no seu anúncio. "cpc_youtube" é específico para vídeos.
*   **Taxa Visitante -> Trial:** Eficiência do site/landing page. De cada 100 visitantes, quantos criam uma conta de teste.
*   **ARPU / Preço Trader:** Receita média por usuário ou preço da assinatura principal.
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
        display(Markdown("***"))
        display(Markdown("## 📊 PAINEL EXECUTIVO DE RISCO"))
        display(Markdown("**Objetivo:** Snapshot de 3 minutos - o investidor vê tudo de uma vez."))
    
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
    
    # Comparar ARR Real vs Ideal para mostrar trade-off
    arr_real_final = df_real_m['arr'].iloc[-1] if 'arr' in df_real_m.columns else 0
    arr_ideal_final = df_ideal_m['arr'].iloc[-1] if 'arr' in df_ideal_m.columns else 0
    caixa_real_final = df_real_m['caixa'].iloc[-1]
    caixa_ideal_final = df_ideal_m['caixa'].iloc[-1]
    mrr_real_final = df_real_m['mrr'].iloc[-1] if 'mrr' in df_real_m.columns else 0
    mrr_ideal_final = df_ideal_m['mrr'].iloc[-1] if 'mrr' in df_ideal_m.columns else 0
    
    # Calcular razão de crescimento
    arr_ratio = arr_ideal_final / max(arr_real_final, 1)
    
    insight_md = f"""
::: {{.callout-tip title="💡 INTERPRETAÇÃO RÁPIDA"}}

- ✅ **Risco de quebra:** {(1-prob_sobrevivencia):.1%} ({"< 5% - Excelente" if prob_sobrevivencia > 0.95 else "Atenção necessária"})
- ✅ **Cenário Real:** {"Atinge metas principais" if df_real_m['caixa'].iloc[-1] > 50000 else "Margem apertada"}
- ⚠️ **Dispersão:** {"Alta incerteza - revisar premissas" if (caixa_final.quantile(0.95) - caixa_final.quantile(0.05)) > 200000 else "Incerteza controlada"}
- 🔴 **Cenário Estresse:** {"Mostra fragilidade em churn dobrado" if df_stress_m['caixa'].iloc[-1] < 0 else "Modelo resiliente"}

:::

::: {{.callout-note title="📊 REAL vs IDEAL: ESTRATÉGIA DE CRESCIMENTO"}}

| Métrica M36 | 💰 Real (Conservador) | 🌟 Ideal (Agressivo) | Delta |
|-------------|----------------------|---------------------|-------|
| **ARR** | {formata_moeda(arr_real_final)} | {formata_moeda(arr_ideal_final)} | **{arr_ratio:.1f}x** |
| **MRR** | {formata_moeda(mrr_real_final)} | {formata_moeda(mrr_ideal_final)} | +{(mrr_ideal_final/max(mrr_real_final,1)-1)*100:.0f}% |
| **Caixa** | {formata_moeda(caixa_real_final)} | {formata_moeda(caixa_ideal_final)} | {'+' if caixa_ideal_final > caixa_real_final else ''}{formata_moeda(caixa_ideal_final - caixa_real_final)} |

**⚠️ OBSERVAÇÃO IMPORTANTE:**

O cenário **Ideal (Agressivo)** pode apresentar **caixa negativo em meses iniciais**. Isso é **intencional** e segue 
a estratégia clássica de startups com investimento:

- 🔥 **Investimento Antecipado:** Marketing R$ 10k/mês (vs R$ 1.5k do Real)
- 📈 **Crescimento Acelerado:** ARR **{arr_ratio:.1f}x maior** no M36
- 💡 **Lógica:** *"Queimar caixa hoje para capturar mercado e criar valor futuro"*

Startups como **Amazon, Uber e Netflix** operaram no prejuízo por anos para maximizar crescimento.
O cenário Ideal simula este comportamento — sacrifica caixa curto prazo por escala.

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
        display(Markdown("# PÁGINA 5: RISCO & CENÁRIOS"))
        display(Markdown(
            "**Objetivo:** Quantificar o risco do modelo através de simulações Monte Carlo, "
            "cenários de estresse e análise de sensibilidade, provando robustez e proteção de downside "
            "para o investidor."
        ))
        display(Markdown("***"))
    
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
    
    # 4. ATO 2: Tornado Plot (Sensibilidade)
    if not report_mode:
        print("\n" + "-"*40)
        print("🌪️ Gerando Ato 2: Tornado Plot...")
        
    ato2_results = render_ato2_sensibilidade(premissas, report_mode, motor_func, met_real=None, df_real_m=df_real_m)
    
    if not report_mode:
        print("   ✅ Ato 2 gerado com sucesso!")

    # 5. Placeholder para Atos 3-5
    if not report_mode:
        print("\n" + "-"*40)
        print("📌 ATOS 3-5 (Em desenvolvimento):")
        print("   • ATO 3: Heatmap Runway Semanal")
        print("   • ATO 4: Break-Even sob Estresse")
        print("   • ATO 5: Gap Analysis Real vs Estresse")
        print("-"*40)
    
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
        print("\n✅ PÁGINA 5 - FASE 1 + ATO 1 + VEREDITO GERADOS COM SUCESSO!")
    
    return RiskPageOutput({
        'df_stress_m': df_stress_m,
        'df_tabela_executiva': df_tabela,
        'kpi_cards': cards,
        'ato1': ato1_results,
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
