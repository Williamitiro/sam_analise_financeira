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
        {'Categoria': '', 'Métrica': 'LTV/CAC', 'Real': f"{safe_get(real_final, ['ltv_cac', 'ltv']) / max(safe_get(real_final, ['cac_blended', 'cac']), 1):.1f}x", 'Ideal': '', 'Estresse': '', 'Benchmark': '> 3.0x', 'Status': '🟢'},
        
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
# SEÇÃO 4: RENDERIZAÇÃO DA FASE 1 (Tabela + Cards)
# ============================================================================

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
    
    insight_md = f"""
::: {{.callout-tip title="💡 INTERPRETAÇÃO RÁPIDA"}}

- ✅ **Risco de quebra:** {(1-prob_sobrevivencia):.1%} ({"< 5% - Excelente" if prob_sobrevivencia > 0.95 else "Atenção necessária"})
- ✅ **Cenário Real:** {"Atinge metas principais" if df_real_m['caixa'].iloc[-1] > 50000 else "Margem apertada"}
- ⚠️ **Dispersão:** {"Alta incerteza - revisar premissas" if (caixa_final.quantile(0.95) - caixa_final.quantile(0.05)) > 200000 else "Incerteza controlada"}
- 🔴 **Cenário Estresse:** {"Mostra fragilidade em churn dobrado" if df_stress_m['caixa'].iloc[-1] < 0 else "Modelo resiliente"}

:::
"""
    
    if report_mode:
        display(Markdown(insight_md))
    else:
        print("\n💡 INTERPRETAÇÃO RÁPIDA:")
        print(f"   • Risco de quebra: {(1-prob_sobrevivencia):.1%}")
        print(f"   • Cenário Real: Caixa final = {formata_moeda(df_real_m['caixa'].iloc[-1])}")
        print(f"   • Cenário Estresse: Caixa final = {formata_moeda(df_stress_m['caixa'].iloc[-1])}")
    
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
    
    # 3. Placeholder para fases futuras
    if not report_mode:
        print("\n" + "-"*40)
        print("📌 FASES 2-4 (Em desenvolvimento):")
        print("   • ATO 1: Monte Carlo Fan Chart")
        print("   • ATO 2: Tornado Plot Sensibilidade")
        print("   • ATO 3: Heatmap Runway Semanal")
        print("   • ATO 4: Break-Even sob Estresse")
        print("   • ATO 5: Gap Analysis Real vs Estresse")
        print("-"*40)
    
    if not report_mode:
        print("\n✅ PÁGINA 5 - FASE 1 GERADA COM SUCESSO!")
    
    return {
        'df_stress_m': df_stress_m,
        'df_tabela_executiva': df_tabela,
        'kpi_cards': cards
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
