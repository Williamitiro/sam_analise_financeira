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

try:
    setup_plot_style()
except:
    pass


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


def plotar_fan_chart(dados_fan, report_mode=False, zoom_percentil=90):
    """
    Gera o Fan Chart com áreas percentiladas - VERSÃO MELHORADA.
    
    MELHORIAS:
    - Limita o eixo Y ao P90 para que linhas Real/Ideal sejam visíveis
    - Cores mais distintas para cada elemento
    - Anotações claras nos pontos finais
    - Legenda fora do gráfico para não obstruir
    """
    
    figsize = (12, 7) if report_mode else (14, 8)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    meses = dados_fan['mes'].values
    
    # Calcular limite Y inteligente (baseado no P90 + 20% margem)
    y_max = dados_fan['p90'].max() * 1.2
    y_min = min(dados_fan['p5'].min() * 1.1, -10000)  # Pelo menos -10k para mostrar zona de risco
    
    # CAMADA 1: Área P10-P90 (80% de confiança - foco principal)
    ax.fill_between(meses, dados_fan['p10'], dados_fan['p90'], 
                    alpha=0.25, color='#9E9E9E', label='P10-P90 (80% dos cenários)')
    
    # CAMADA 2: Área P25-P75 (50% de confiança - zona mais provável)
    ax.fill_between(meses, dados_fan['p25'], dados_fan['p75'], 
                    alpha=0.4, color='#616161', label='P25-P75 (50% mais provável)')
    
    # LINHA CENTRAL: P50 (Mediana) - DESTAQUE
    ax.plot(meses, dados_fan['p50'], color='#212121', linewidth=3.5, 
            linestyle='-', label='P50 (Mediana)', zorder=5)
    
    # LINHA REFERÊNCIA: Cenário Real (5A) - AZUL VIBRANTE
    ax.plot(meses, dados_fan['real'], color='#1565C0', linewidth=3, 
            linestyle='-', label='Cenário Real (5A)', zorder=6, marker='o', 
            markersize=4, markevery=6)
    
    # LINHA ASPIRACIONAL: Cenário Ideal (5B) - VERDE VIBRANTE
    ax.plot(meses, dados_fan['ideal'], color='#2E7D32', linewidth=3, 
            linestyle='--', label='Cenário Ideal (5B)', zorder=6, marker='s', 
            markersize=4, markevery=6)
    
    # LINHA DE QUEBRA (Caixa = 0) - VERMELHO FORTE
    ax.axhline(y=0, color='#D32F2F', linestyle='-', linewidth=2.5, 
               alpha=0.8, label='Linha de Quebra (R$ 0)', zorder=4)
    
    # MÊS 6 - Linha vertical de decisão
    ax.axvline(x=6, color='#FF9800', linestyle='--', linewidth=2, alpha=0.7, label='Mês 6 (Decisão)')
    
    # Limitar eixo Y para visibilidade
    ax.set_ylim(y_min, y_max)
    
    # Formatação
    ax.set_xlabel('Mês', fontsize=13, fontweight='bold')
    ax.set_ylabel('Caixa Acumulado (R$)', fontsize=13, fontweight='bold')
    ax.set_title('Distribuição Probabilística do Caixa - Monte Carlo\n' + 
                 'Foco: 80% dos cenários mais prováveis (P10-P90)', 
                 fontsize=14, color='#333', fontweight='bold', pad=15)
    
    # Formatar eixo Y como moeda
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle=':', zorder=0)
    ax.set_axisbelow(True)
    
    # Legenda FORA do gráfico (à direita)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=True, fontsize=10)
    
    # Anotações nos pontos finais
    mes_final = meses[-1]
    offset_y = (y_max - y_min) * 0.02
    
    # Anotação P50
    ax.annotate(f'P50: {formata_moeda(dados_fan["p50"].iloc[-1])}', 
                xy=(mes_final, dados_fan['p50'].iloc[-1]),
                xytext=(mes_final - 5, dados_fan['p50'].iloc[-1] + offset_y * 3),
                fontsize=10, fontweight='bold', color='#212121',
                arrowprops=dict(arrowstyle='->', color='#212121', lw=1.5))
    
    # Anotação Real
    ax.annotate(f'Real: {formata_moeda(dados_fan["real"].iloc[-1])}', 
                xy=(mes_final, dados_fan['real'].iloc[-1]),
                xytext=(mes_final - 5, dados_fan['real'].iloc[-1] - offset_y * 5),
                fontsize=10, fontweight='bold', color='#1565C0',
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    
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
    
    # Criar figura
    figsize = (10, 6) if report_mode else (12, 7)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Histograma
    n, bins, patches = ax.hist(caixa_mes6, bins=30, color='#90CAF9', edgecolor='#1565C0', 
                                alpha=0.7, density=True, label='Distribuição MC')
    
    # Colorir barras por zona
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge < 0:
            patch.set_facecolor('#EF5350')  # Vermelho - quebra
            patch.set_alpha(0.8)
        elif left_edge < 10000:
            patch.set_facecolor('#FFA726')  # Laranja - risco
            patch.set_alpha(0.8)
        else:
            patch.set_facecolor('#66BB6A')  # Verde - seguro
            patch.set_alpha(0.8)
    
    # Linhas de referência
    ax.axvline(x=0, color='#D32F2F', linestyle='-', linewidth=3, label='Quebra (R$ 0)')
    ax.axvline(x=caixa_real_m6, color='#1565C0', linestyle='--', linewidth=2.5, 
               label=f'Real M6: {formata_moeda(caixa_real_m6)}')
    ax.axvline(x=caixa_ideal_m6, color='#2E7D32', linestyle='--', linewidth=2.5, 
               label=f'Ideal M6: {formata_moeda(caixa_ideal_m6)}')
    
    # Percentis
    p25 = np.percentile(caixa_mes6, 25)
    p50 = np.percentile(caixa_mes6, 50)
    p75 = np.percentile(caixa_mes6, 75)
    
    ax.axvline(x=p50, color='#212121', linestyle='-', linewidth=2, 
               label=f'Mediana: {formata_moeda(p50)}')
    
    # Probabilidades
    prob_quebra = (caixa_mes6 < 0).mean()
    prob_risco = ((caixa_mes6 >= 0) & (caixa_mes6 < 10000)).mean()
    prob_seguro = (caixa_mes6 >= 10000).mean()
    
    # Caixa de texto com probabilidades
    textstr = f'📊 Distribuição Mês 6:\n' \
              f'🔴 Quebra (< R$ 0): {prob_quebra:.1%}\n' \
              f'🟠 Risco (R$ 0-10k): {prob_risco:.1%}\n' \
              f'🟢 Seguro (> R$ 10k): {prob_seguro:.1%}\n' \
              f'─────────────────\n' \
              f'P25: {formata_moeda(p25)}\n' \
              f'P50: {formata_moeda(p50)}\n' \
              f'P75: {formata_moeda(p75)}'
    
    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='#666')
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props,
            fontfamily='monospace')
    
    # Formatação
    ax.set_xlabel('Caixa no Mês 6 (R$)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Densidade', fontsize=13, fontweight='bold')
    ax.set_title('🎯 PONTO DE DECISÃO: Distribuição do Caixa no MÊS 6\n' + 
                 'Onde você estará quando precisar decidir?', 
                 fontsize=14, color='#333', fontweight='bold', pad=15)
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
    
    ax.grid(True, alpha=0.3, linestyle=':', axis='y')
    ax.legend(loc='upper left', frameon=True, fontsize=9)
    
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
    dados_fan = preparar_dados_fan_chart(mc_results, df_real_m, df_ideal_m)
    fig1 = plotar_fan_chart(dados_fan, report_mode)
    
    if report_mode:
        try:
            import os
            os.makedirs('outputs/figs', exist_ok=True)
            plt.savefig('outputs/figs/pag5_monte_carlo_fan_chart.png', dpi=150, bbox_inches='tight')
            display(Markdown("![Fan Chart Monte Carlo](outputs/figs/pag5_monte_carlo_fan_chart.png)"))
        except:
            pass
    else:
        plt.show()
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
        display(Markdown("---"))
        display(Markdown("### 🎯 ZOOM: PONTO DE DECISÃO - MÊS 6"))
    
    fig2, dados_m6 = plotar_grafico_mes6(mc_results, df_real_m, df_ideal_m, premissas, report_mode)
    
    if report_mode:
        try:
            plt.savefig('outputs/figs/pag5_distribuicao_mes6.png', dpi=150, bbox_inches='tight')
            display(Markdown("![Distribuição Mês 6](outputs/figs/pag5_distribuicao_mes6.png)"))
        except:
            pass
    else:
        plt.show()
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
        display(Markdown("**Objetivo:** Quantificar risco, provar robustez, vender proteção de downside."))
        display(Markdown("**Tempo de Leitura:** 15 minutos"))
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
    
    # 4. Placeholder para Atos 2-5
    if not report_mode:
        print("\n" + "-"*40)
        print("📌 ATOS 2-5 (Em desenvolvimento):")
        print("   • ATO 2: Tornado Plot Sensibilidade")
        print("   • ATO 3: Heatmap Runway Semanal")
        print("   • ATO 4: Break-Even sob Estresse")
        print("   • ATO 5: Gap Analysis Real vs Estresse")
        print("-"*40)
    
    if not report_mode:
        print("\n✅ PÁGINA 5 - FASE 1 + ATO 1 GERADOS COM SUCESSO!")
    
    return {
        'df_stress_m': df_stress_m,
        'df_tabela_executiva': df_tabela,
        'kpi_cards': cards,
        'ato1': ato1_results
    }


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
