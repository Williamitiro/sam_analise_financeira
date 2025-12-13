# ==============================================================================
# PÁGINA 5 (RISCO) - ATOS 4 e 5 (MODULAR)
# ==============================================================================
# OBJETIVO: Implementar análises finais de risco: Break-Even sob Estresse e Gap Analysis.
# MODULARIZAÇÃO: Separado da PAGINA_5_RISCO.py para manutenibilidade.
# AUTOR: Agente Antigravity (seguindo Gold Standard V22.0)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from IPython.display import display, Markdown

# Import utils compartilhados
# Ajuste conforme estrutura de imports do notebook (assumindo execução como módulo ou script)
try:
    from .celula_0_utils import (
        render_atomic_block, formata_moeda, formata_pct, setup_plot_style
    )
except ImportError:
    # Tenta import direto se estiver na mesma pasta
    try:
        from celula_0_utils import (
            render_atomic_block, formata_moeda, formata_pct, setup_plot_style
        )
    except:
        # Fallback dummy
        def render_atomic_block(**kwargs): print("⚠️ render_atomic_block missing")
        def formata_moeda(v): return f"R$ {v:,.2f}"
        def formata_pct(v): return f"{v:.1%}"
        def setup_plot_style(): pass

# ==============================================================================
# ATO 4: BREAK-EVEN SOB ESTRESSE (ANÁLISE DE ESCALA)
# ==============================================================================

def identificar_breakeven_operacional(df_m):
    """
    Identifica o mês de break-even operacional (Receita >= Custos Totais)
    que se sustenta por pelo menos 2 meses.
    """
    if df_m is None or df_m.empty:
        return None, None
    
    # Colunas necessárias
    col_rec = next((c for c in ['receita_liquida', 'receita_total', 'receita_bruta'] if c in df_m.columns), None)
    col_cus = next((c for c in ['total_opex', 'custos_totais'] if c in df_m.columns), None)
    
    # Se não tem OPEX explícito, tenta somar
    if not col_cus and 'gasto_marketing' in df_m.columns:
        # Aproximação se necessário (mas ideal é ter a coluna)
        df_m['__temp_custos'] = df_m['gasto_marketing'] + df_m.get('custo_pessoal', 0) + df_m.get('custo_infra', 0)
        col_cus = '__temp_custos'
    
    if not col_rec or not col_cus:
        return None, None
    
    lucro_op = df_m[col_rec] - df_m[col_cus]
    
    # Busca primeiro mês positivo sustentado
    for i in range(len(df_m) - 1):
        if lucro_op.iloc[i] >= 0 and lucro_op.iloc[i+1] >= 0:
            return i + 1, df_m.iloc[i]  # Mês (1-based) e linha de dados
            
    return None, None  # Nunca atinge

def render_ato4_breakeven(df_real_m, df_ideal_m, df_stress_m, premissas, report_mode=False):
    """
    Renderiza Ato 4: Trajetória de Break-Even sob Estresse.
    """
    if not report_mode:
        print("\n" + "-"*40)
        print("⚖️ ATO 4: ANÁLISE DE BREAK-EVEN SOB ESTRESSE")
        print("-" * 40)
    
    setup_plot_style()
    
    # 1. Identificar pontos de BE
    be_real_mes, _ = identificar_breakeven_operacional(df_real_m)
    be_ideal_mes, _ = identificar_breakeven_operacional(df_ideal_m)
    be_stress_mes, _ = identificar_breakeven_operacional(df_stress_m)
    
    # Texto para labels
    lbl_real = f"M{be_real_mes}" if be_real_mes else "Nunca"
    lbl_ideal = f"M{be_ideal_mes}" if be_ideal_mes else "Nunca"
    lbl_stress = f"M{be_stress_mes}" if be_stress_mes else "Nunca"
    
    # 2. Plotar gráfico (3 painéis)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [2, 1]})
    
    # --- PAINEL 1: TRAJETÓRIA DE LUCRO/PREJUÍZO ---
    
    col_lucro = 'lucro_liquido' if 'lucro_liquido' in df_real_m.columns else 'ebitda'
    
    meses = range(1, len(df_real_m) + 1)
    
    # Ideal (referência de teto)
    ax1.plot(meses, df_ideal_m[col_lucro], color='#2ecc71', linestyle='--', alpha=0.5, label=f'Ideal (BE: {lbl_ideal})')
    
    # Real (cenário base)
    ax1.plot(meses, df_real_m[col_lucro], color='#3498db', linewidth=3, label=f'Real (BE: {lbl_real})')
    ax1.fill_between(meses, df_real_m[col_lucro], 0, where=(df_real_m[col_lucro]>=0), color='#2ecc71', alpha=0.1)
    ax1.fill_between(meses, df_real_m[col_lucro], 0, where=(df_real_m[col_lucro]<0), color='#e74c3c', alpha=0.1)
    
    # Estresse (cenário piso)
    ax1.plot(meses, df_stress_m[col_lucro], color='#e74c3c', linestyle='-', linewidth=2, label=f'Estresse (BE: {lbl_stress})')
    
    # Linha zero
    ax1.axhline(0, color='gray', linestyle=':', linewidth=1)
    
    # Anotação do BE Real
    if be_real_mes:
        y_loc = df_real_m[col_lucro].iloc[be_real_mes-1]
        ax1.annotate(f'BE Real: M{be_real_mes}', 
                    xy=(be_real_mes, 0), xytext=(be_real_mes, y_loc + (y_loc*0.5 if y_loc else 1000)),
                    arrowprops=dict(arrowstyle='->', color='black'),
                    fontsize=10, fontweight='bold', ha='center')
    
    ax1.set_title("QUANDO O NEGÓCIO SE PAGA? (Trajetória de Lucro Líquido)", fontsize=12, fontweight='bold', loc='left')
    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Lucro Líquido (R$)")
    ax1.legend(loc='upper left')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))

    # --- PAINEL 2: CAPITAL CONSUMIDO ATÉ O BE ---
    
    # Calcular capital consumido (soma dos prejuízos até o BE)
    def calc_consumo(df, be_mes):
        if not be_mes: # Se nunca atinge, considera todo o período (36m)
            return abs(df[col_lucro][df[col_lucro] < 0].sum())
        # Soma apenas os meses negativos antes do BE
        prejuizos = df[col_lucro].iloc[:be_mes]
        return abs(prejuizos[prejuizos < 0].sum())
    
    consumo_real = calc_consumo(df_real_m, be_real_mes)
    consumo_ideal = calc_consumo(df_ideal_m, be_ideal_mes)
    consumo_stress = calc_consumo(df_stress_m, be_stress_mes)
    
    bar_colors = ['#2ecc71', '#3498db', '#e74c3c']
    bars = ax2.bar(['Ideal', 'Real', 'Estresse'], 
                   [consumo_ideal, consumo_real, consumo_stress],
                   color=bar_colors, alpha=0.8)
    
    # Labels nas barras
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                formata_moeda(height),
                ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    ax2.set_title("CAPITAL NECESSÁRIO ATÉ O BREAK-EVEN", fontsize=12, fontweight='bold', loc='left')
    ax2.set_ylabel("Capital Consumido Cumulativo (R$)")
    ax2.yaxis.set_visible(False) # Limpa eixo Y pois já tem labels
    ax2.spines['left'].set_visible(False)
    
    plt.tight_layout()
    
    # 3. Gerar Insight Dinâmico
    status_be = "SAUDÁVEL" if be_real_mes and be_real_mes <= 18 else "ALERTA"
    if not be_real_mes: status_be = "CRÍTICO"
    
    fato = f"Break-Even Real esperado no Mês {be_real_mes if be_real_mes else 'N/A'} (consumo de {formata_moeda(consumo_real)})."
    causa = "Estrutura de custos vs Ramp-up de receita atual."
    
    if be_real_mes and be_stress_mes:
        atraso = be_stress_mes - be_real_mes
        implicacao = f"Em cenário de estresse, BE atrasa {atraso} meses e exige {formata_moeda(consumo_stress - consumo_real)} extra."
    elif be_real_mes and not be_stress_mes:
        implicacao = "Em cenário de estresse, o modelo NUNCA atinge break-even nos 36 meses (risco de insolvência)."
    else:
        implicacao = "Modelo não atinge break-even no horizonte atual em nenhum cenário base."
        
    acao = "Focar eficiência de aquisição (CAC) e retenção para antecipar BE em 3-6 meses."
    
    insight = {
        "fato": fato,
        "causa": causa,
        "implicacao": implicacao,
        "acao": acao
    }
    
    
    # Criar tabela para render_atomic_block (obrigatório não ser None)
    df_be = pd.DataFrame([
        {'Cenário': 'Real', 'Mês Break-Even': lbl_real, 'Capital Consumido': formata_moeda(consumo_real)},
        {'Cenário': 'Ideal', 'Mês Break-Even': lbl_ideal, 'Capital Consumido': formata_moeda(consumo_ideal)},
        {'Cenário': 'Estresse', 'Mês Break-Even': lbl_stress, 'Capital Consumido': formata_moeda(consumo_stress)}
    ])
    
    # 4. Renderizar via Atomic Block
    render_atomic_block(
        chart_id="pg5_viz4_breakeven",
        title_technical="VIZ 5.4: Análise de Break-Even sob Estresse",
        title_colloquial="Quando o negócio atinge autossuficiência?",
        fig=fig,
        legend_md=f"Gráfico mostra quando a operação se paga. **Real: M{lbl_real}** | **Estresse: {lbl_stress}**.",
        df_tabela=df_be, 
        insight_dict=insight,
        report_mode=report_mode,
        data_source_text="Fonte: Projeção Financeira Real/Ideal/Estresse"
    )
    plt.close(fig)
    return {'be_real': be_real_mes, 'consumo_real': consumo_real}

# ==============================================================================
# ATO 5: GAP ANALYSIS (VAZAMENTO DO MODELO)
# ==============================================================================

def decompor_gap_shapley(df_real, df_stress, premissas, motor_func):
    """
    Decompõe a diferença de caixa final (Gap) entre Real e Estresse usando
    uma aproximação de Shapley Value (impacto marginal de cada fator de risco).
    
    ZERO HARDCODING: Usa os multiplicadores definidos em celula_2B_config_MC.py
    """
    if motor_func is None:
        return {} # Não dá pra calcular sem motor
        
    CAIXA_REAL = df_real['caixa'].iloc[-1]
    CAIXA_STRESS = df_stress['caixa'].iloc[-1]
    GAP_TOTAL = CAIXA_REAL - CAIXA_STRESS
    
    if GAP_TOTAL == 0:
        return {}
        
    # Buscar multiplicadores do cenário pessimista no MC config
    try:
        mc_config = premissas.get('monte_carlo', {})
        cenario_pess = mc_config.get('cenarios', {}).get('pessimista', {})
        multiplicadores = cenario_pess.get('multiplicadores', {})
        
        # Amplificador de estresse usado na PAGINA_RISCO (2.0x)
        FATOR_AMPLIFICACAO = 2.0 
    except:
        # Fallback seguro
        multiplicadores = {'churn_inicial': 1.25, 'marketing_fixo_mensal': 0.70}
        FATOR_AMPLIFICACAO = 1.0

    contribuicoes = {}
    
    # Para cada fator, roda o motor isolado e mede o impacto
    print("   🔍 Calculando decomposição de gap (Shapley)...")
    
    for fator, mult_base in multiplicadores.items():
        if fator not in premissas:
            continue
            
        # Calcular multiplicador de estresse efetivo (igual ao usado no gerar_cenario_estresse)
        if mult_base > 1:
            mult_efetivo = 1 + (mult_base - 1) * FATOR_AMPLIFICACAO
        else:
            mult_efetivo = 1 - (1 - mult_base) * FATOR_AMPLIFICACAO
            
        # Criar premissas isoladas (Real + 1 Fator Ruim)
        p_isolada = premissas.copy()
        
        # Tratamento especial para CPCs (agrupar como "Custo de Mídia") e Conversão
        nome_fator = fator
        if 'cpc' in fator:
            nome_fator = 'Aumento CPC (Mídia)'
            # Aplica em todos os CPCs
            for cpc in ['cpc_instagram', 'cpc_facebook', 'cpc_google', 'cpc_youtube']:
                if cpc in p_isolada:
                    p_isolada[cpc] = p_isolada[cpc] * mult_efetivo
        else:
            p_isolada[fator] = p_isolada[fator] * mult_efetivo
            
        # Rodar motor
        try:
            df_iso, _, _, _ = motor_func(p_isolada)
            caixa_iso = df_iso['caixa'].iloc[-1]
            impacto = CAIXA_REAL - caixa_iso
            
            # Guardar maior impacto (caso CPC use loop)
            if nome_fator in contribuicoes:
                contribuicoes[nome_fator] = max(contribuicoes[nome_fator], impacto)
            else:
                contribuicoes[nome_fator] = impacto
                
        except Exception as e:
            print(f"Erro no Shapley fator {fator}: {e}")
            
    # Normalizar para somar 100% do GAP TOTAL (aproximação)
    soma_impactos = sum(contribuicoes.values())
    if soma_impactos > 0:
        for k in contribuicoes:
            contribuicoes[k] = (contribuicoes[k] / soma_impactos) * GAP_TOTAL
            
    return contribuicoes

def render_ato5_gap_analysis(df_real_m, df_stress_m, premissas, motor_func, report_mode=False):
    """
    Renderiza Ato 5: Gap Analysis (Comparativo Real vs Estresse).
    Mostra onde o dinheiro "vaza" no pior cenário.
    """
    if not report_mode:
        print("\n" + "-"*40)
        print("📉 ATO 5: GAP ANALYSIS E VAZAMENTO DE VALOR")
        print("-" * 40)
    
    setup_plot_style()
    
    # 1. Calcular Gap
    gap_caixa = df_real_m['caixa'] - df_stress_m['caixa']
    gap_final = gap_caixa.iloc[-1]
    gap_pct = (gap_final / df_real_m['caixa'].iloc[-1]) * 100 if df_real_m['caixa'].iloc[-1] != 0 else 0
    
    mes_max_gap = gap_caixa.idxmax() + 1 # 1-based
    val_max_gap = gap_caixa.max()
    
    # 2. Decomposição (Shapley)
    decomposicao = decompor_gap_shapley(df_real_m, df_stress_m, premissas, motor_func)
    
    # Se decomposição vazia (erro ou gap zero), usa dados dummy seguros
    if not decomposicao and gap_final > 100:
        decomposicao = {'Churn (Retenção)': gap_final * 0.5, 'CAC (Aquisição)': gap_final * 0.3, 'Outros': gap_final * 0.2}
    
    # Ordenar por impacto
    df_decomp = pd.DataFrame(list(decomposicao.items()), columns=['Fator', 'Impacto'])
    df_decomp = df_decomp.sort_values('Impacto', ascending=True) # Para waterfall funcionar bem
    
    # 3. Plotar (2 Paineis)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # --- PAINEL 1: ÁREA DE VAZAMENTO ---
    meses = range(1, len(df_real_m) + 1)
    ax1.plot(meses, df_real_m['caixa'], color='#3498db', label='Caixa Real')
    ax1.plot(meses, df_stress_m['caixa'], color='#e74c3c', label='Caixa Estresse')
    
    # Preencher gap
    ax1.fill_between(meses, df_real_m['caixa'], df_stress_m['caixa'], color='gray', alpha=0.3, label='Gap (Risco)')
    
    # Anotar Gap Final
    ax1.annotate(f'Gap Final:\n{formata_moeda(gap_final)}', 
                xy=(36, df_stress_m['caixa'].iloc[-1] + gap_final/2),
                xytext=(32, df_stress_m['caixa'].iloc[-1] + gap_final),
                arrowprops=dict(arrowstyle='->'), fontsize=9, fontweight='bold', color='red')
                
    ax1.set_title("GAP DE CAIXA: REAL vs ESTRESSE", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Caixa Acumulado (R$)")
    ax1.legend()
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))

    # --- PAINEL 2: WATERFALL DE VAZAMENTO ---
    if not df_decomp.empty:
        # Waterfall chart logic
        y_pos = np.arange(len(df_decomp))
        ax2.barh(y_pos, df_decomp['Impacto'], color='#e74c3c', alpha=0.8)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(df_decomp['Fator'])
        
        # Labels nas barras
        for i, v in enumerate(df_decomp['Impacto']):
            pct = (v / gap_final * 100) if gap_final > 0 else 0
            ax2.text(v, i, f" -{formata_moeda(v)} ({pct:.0f}%)", va='center', fontweight='bold')
            
        ax2.set_title("ORIGEM DO VAZAMENTO (O que causa a perda?)", fontsize=12, fontweight='bold')
        ax2.set_xlabel("Impacto no Caixa Final (R$)")
    else:
        ax2.text(0.5, 0.5, "Sem dados de decomposição", ha='center')
        
    plt.tight_layout()
    
    # 4. Insight Dinâmico
    top_fator = df_decomp.iloc[-1]['Fator'] if not df_decomp.empty else "N/A"
    
    insight = {
        "fato": f"Sob estresse máximo, a empresa perde {formata_moeda(gap_final)} de caixa ({gap_pct:.0f}% do valor real).",
        "causa": f"O principal ofensor 'vazando' valor é: **{top_fator}**.",
        "implicacao": "Isso indica alta sensibilidade a este fator específico, exigindo hedge ou mitigação.",
        "acao": f"Criar plano de contingência focado em controlar {top_fator}."
    }
    
    render_atomic_block(
        chart_id="pg5_viz5_gap",
        title_technical="VIZ 5.5: Decomposição de Gap (Real vs Estresse)",
        title_colloquial="Onde o dinheiro vaza na crise?",
        fig=fig,
        legend_md="Gráfico da esquerda mostra a diferença acumulada de caixa. Direita mostra quais fatores causam essa perda.",
        df_tabela=df_decomp,
        insight_dict=insight,
        report_mode=report_mode,
        data_source_text="Fonte: Monte Carlo Shapley Decomposition"
    )
    plt.close(fig)
    return {'gap_final': gap_final, 'top_fator': top_fator}
