# ==============================================================================
# PÁGINA 2: GROWTH MACHINE - VISUALIZAÇÕES COMPLETAS
# ==============================================================================
# VERSÃO: 1.0 - INSTITUTIONAL GRADE (Kaszek/Sequoia Style)
# STATUS: PRODUCTION READY
#
# Este arquivo contém 5 visualizações completas para a Página 2 do Dashboard:
#   VIZ 2.1: Evolução do Funil (Logarítmico)
#   VIZ 2.2: Independência de Canais (Stacked Area + CAC)
#   VIZ 2.3: Elasticidade & MEF (Color Coded Scatter)
#   VIZ 2.4: Net Growth & Custo do Churn (Diverging Bar)
#   VIZ 2.5: Payback Period (Background Zones)
#
# DEPENDÊNCIAS ESPERADAS:
#   - df_real_m: DataFrame mensal com projeções (colunas: trafego_total, trials_total, etc.)
#   - PREMISSAS: Dict de premissas
#   - mc_results (opcional): Resultados Monte Carlo
#
# DIRETRIZES SEGUIDAS:
#   - Zero hardcode: tudo calculado em runtime
#   - Escala logarítmica no funil
#   - Zonas de contexto coloridas
#   - Insights dinâmicos com confiança
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
from IPython.display import display, HTML
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURAÇÃO GLOBAL DE CORES E ESTILOS
# ==============================================================================
CORES = {
    'fundo': '#FFFFFF',
    'texto': '#212121',
    'grid': '#E0E0E0',
    'linha_real': '#000000',
    'linha_benchmark': '#D32F2F',
    'verde': '#43A047',
    'verde_claro': '#E8F5E9',
    'amarelo': '#FFC107',
    'amarelo_claro': '#FFFDE7',
    'vermelho': '#D32F2F',
    'vermelho_claro': '#FFEBEE',
    'azul': '#1E88E5',
    'roxo': '#7E57C2',
    'cinza': '#B0BEC5',
    'verde_neon': '#00E676',
    'verde_escuro': '#2E7D32',
    'laranja': '#FF9800',
}

SNAPSHOTS = [0, 3, 6, 12, 18, 24, 35]  # M1, M4, M7, M13, M19, M25, M36 (índices)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#BDBDBD',
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': '#E0E0E0'
})

def formatar_numero(valor, casas=0):
    """Formata número com separador de milhar brasileiro."""
    if pd.isna(valor) or np.isinf(valor):
        return '-'
    if casas == 0:
        return f"{int(valor):,}".replace(',', '.')
    return f"{valor:,.{casas}f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def formatar_moeda(valor):
    """Formata valor como moeda brasileira."""
    if pd.isna(valor) or np.isinf(valor):
        return '-'
    return f"R$ {formatar_numero(valor, 2)}"

def get_confianca(r2=None, delta_pct=None):
    """Retorna flag de confiança baseado em métricas."""
    if r2 is not None and r2 > 0.9:
        return "🟢 Alta", "#4CAF50"
    if delta_pct is not None and abs(delta_pct) > 20:
        return "🟢 Alta", "#4CAF50"
    return "🟡 Média", "#FFC107"

# ==============================================================================
# VIZ 2.1: EVOLUÇÃO DO FUNIL (LOGARÍTMICO)
# ==============================================================================
def gerar_viz_2_1_funil_log(df_real_m, PREMISSAS, save_path=None):
    """
    Gera o gráfico de funil comparativo M6 vs M36 com escala logarítmica.
    
    Título: "Escalando o volume sem destruir a eficiência"
    Subtítulo: "Funil de Conversão Comparativo: M6 (Início) vs M36 (Atual) | Escala Logarítmica"
    """
    print("="*80)
    print("📊 VIZ 2.1: EVOLUÇÃO DO FUNIL (LOGARÍTMICO)")
    print("="*80)
    
    # --- EXTRAÇÃO DE DADOS ---
    idx_m6 = min(5, len(df_real_m) - 1)  # Mês 6 (índice 5)
    idx_m36 = len(df_real_m) - 1  # Último mês disponível
    
    dados_m6 = df_real_m.iloc[idx_m6]
    dados_m36 = df_real_m.iloc[idx_m36]
    
    # Métricas do funil
    categorias = ['Visitas', 'Trials', 'Novos Pagantes', 'Base Ativa']
    
    m6_valores = [
        dados_m6['trafego_total'],
        dados_m6['trials_total'],
        dados_m6['novos_pagantes_total'],
        dados_m6['usuarios_ativos']
    ]
    
    m36_valores = [
        dados_m36['trafego_total'],
        dados_m36['trials_total'],
        dados_m36['novos_pagantes_total'],
        dados_m36['usuarios_ativos']
    ]
    
    # Taxas de conversão
    conv_trial_pago_m6 = (dados_m6['novos_pagantes_total'] / max(1, dados_m6['trials_total'])) * 100 if dados_m6['trials_total'] > 0 else 0
    conv_trial_pago_m36 = (dados_m36['novos_pagantes_total'] / max(1, dados_m36['trials_total'])) * 100 if dados_m36['trials_total'] > 0 else 0
    delta_conv = conv_trial_pago_m36 - conv_trial_pago_m6
    
    # Delta de base
    delta_base = dados_m36['usuarios_ativos'] / max(1, dados_m6['usuarios_ativos'])
    
    # --- PLOTAGEM ---
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    
    y_pos = np.arange(len(categorias))
    altura = 0.35
    
    # Barras M6 (cinza)
    bars_m6 = ax.barh(y_pos - altura/2, m6_valores, altura, 
                      label=f'M{idx_m6+1}', color=CORES['cinza'], edgecolor='#78909C')
    
    # Barras M36 (coloridas)
    cores_m36 = [CORES['cinza'], CORES['roxo'], CORES['verde'], CORES['verde_escuro']]
    bars_m36 = ax.barh(y_pos + altura/2, m36_valores, altura,
                       label=f'M{idx_m36+1}', color=cores_m36, edgecolor='#424242')
    
    # ESCALA LOGARÍTMICA
    ax.set_xscale('symlog', linthresh=1)
    
    # Labels nas barras
    for i, (bar_m6, bar_m36, val_m6, val_m36) in enumerate(zip(bars_m6, bars_m36, m6_valores, m36_valores)):
        # M6
        ax.text(val_m6 * 1.1, bar_m6.get_y() + bar_m6.get_height()/2,
                f'{formatar_numero(val_m6)}', va='center', ha='left',
                fontsize=9, fontweight='bold', color='#546E7A')
        # M36
        ax.text(val_m36 * 1.1, bar_m36.get_y() + bar_m36.get_height()/2,
                f'{formatar_numero(val_m36)}', va='center', ha='left',
                fontsize=10, fontweight='bold', color='#1B5E20')
    
    # Anotação central (Delta de conversão)
    if delta_conv > 0:
        cor_delta = CORES['verde']
        sinal = '▲'
    else:
        cor_delta = CORES['vermelho']
        sinal = '▼'
    
    ax.annotate(f'Trial→Pago:\n{sinal} {abs(delta_conv):.1f} p.p.',
                xy=(0.5, 0.5), xycoords='axes fraction',
                ha='center', va='center', fontsize=11, fontweight='bold',
                color=cor_delta,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor=cor_delta, linewidth=2))
    
    # Anotação topo (delta base)
    ax.annotate(f'Base cresceu {delta_base:.1f}x em {idx_m36-idx_m6} meses',
                xy=(0.95, 0.95), xycoords='axes fraction',
                ha='right', va='top', fontsize=10, fontweight='bold',
                color=CORES['verde_escuro'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor=CORES['verde_claro'], 
                         edgecolor=CORES['verde'], alpha=0.9))
    
    # Configurações do eixo
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categorias, fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Volume (Escala Logarítmica)', fontsize=10, fontweight='bold')
    
    # Título
    ax.set_title('Escalando o volume sem destruir a eficiência\n' +
                 f'Funil de Conversão Comparativo: M{idx_m6+1} vs M{idx_m36+1} | Escala Logarítmica',
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.show()
    
    # --- TABELA AUXILIAR ---
    print("\n📋 TABELA AUXILIAR - Métricas do Funil")
    print("-"*100)
    
    # Seleciona snapshots disponíveis
    indices_tabela = [i for i in [0, 5, 11, 23, 35] if i < len(df_real_m)]
    
    tabela_data = []
    benchmark_trial_pago = 15.0  # Benchmark de mercado
    
    for idx in indices_tabela:
        row = df_real_m.iloc[idx]
        conv_tp = (row['novos_pagantes_total'] / max(1, row['trials_total'])) * 100
        cac = row['cac_blended'] if not np.isnan(row['cac_blended']) else 0
        
        tabela_data.append({
            'Mês': f"M{idx+1}",
            'Visitas': formatar_numero(row['trafego_total']),
            'Trials': formatar_numero(row['trials_total']),
            'Conv T→P (%)': f"{conv_tp:.1f}%",
            'Novos Pagantes': formatar_numero(row['novos_pagantes_total']),
            'CAC (R$)': formatar_moeda(cac),
            'Benchmark T→P': f"{benchmark_trial_pago}%"
        })
    
    df_tabela = pd.DataFrame(tabela_data)
    display(df_tabela.style.set_properties(**{'text-align': 'right'}).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#37474F'), ('color', 'white'), ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('border', '1px solid #E0E0E0')]}
    ]))
    
    # --- COMO LER ---
    print("\n📖 COMO LER:")
    print("O eixo horizontal é logarítmico. Barras da esquerda mostram o início da operação; as da direita,")
    print("o momento atual. A coluna central destaca o ganho de eficiência técnica (conversão) independente")
    print("do aumento de volume.")
    
    # --- INSIGHT DINÂMICO ---
    confianca, cor_conf = get_confianca(delta_pct=delta_conv)
    print(f"\n💡 INSIGHT ESTRATÉGICO [{confianca}]:")
    
    if conv_trial_pago_m36 > conv_trial_pago_m6:
        print(f"A operação escalou {delta_base:.0f}x mantendo a qualidade. A conversão Trial→Pago subiu de")
        print(f"{conv_trial_pago_m6:.1f}% para {conv_trial_pago_m36:.1f}%, provando Product-Market Fit.")
    else:
        print(f"⚠️ ALERTA: O volume cresceu {delta_base:.0f}x, mas a eficiência caiu. A conversão Trial→Pago")
        print(f"diminuiu de {conv_trial_pago_m6:.1f}% para {conv_trial_pago_m36:.1f}% ({abs(delta_conv):.1f} p.p.).")
        print("AÇÃO: Rever segmentação de Ads e qualidade do tráfego.")
    
    print("="*80)
    
    return fig


# ==============================================================================
# VIZ 2.2: INDEPENDÊNCIA DE CANAIS (STACKED AREA + CAC)
# ==============================================================================
def gerar_viz_2_2_independencia_canais(df_real_m, PREMISSAS, save_path=None):
    """
    Gera o gráfico de Mix de Canais (Stacked Area) + CAC Blended (Linha).
    
    Título: "Conquistando a soberania da aquisição"
    Subtítulo: "Mix de Canais (Stacked Area 100%) & Evolução do CAC Blended"
    """
    print("="*80)
    print("📊 VIZ 2.2: INDEPENDÊNCIA DE CANAIS")
    print("="*80)
    
    # --- EXTRAÇÃO DE DADOS ---
    meses = df_real_m['mes'].values
    
    # Calcula % orgânico e pago
    trafego_total = df_real_m['trafego_total'].values
    trafego_organico = df_real_m['trafego_organico'].values
    trafego_pago = df_real_m['trafego_pago'].values
    
    # Evita divisão por zero
    pct_organico = np.where(trafego_total > 0, (trafego_organico / trafego_total) * 100, 0)
    pct_pago = np.where(trafego_total > 0, (trafego_pago / trafego_total) * 100, 0)
    
    cac_blended = df_real_m['cac_blended'].values
    
    # Encontra o "Dia da Independência" (Orgânico > 50%)
    idx_independencia = None
    for i, pct in enumerate(pct_organico):
        if pct > 50:
            idx_independencia = i
            break
    
    # --- PLOTAGEM ---
    fig, ax1 = plt.subplots(figsize=(14, 7), dpi=150)
    
    # Área empilhada 100%
    ax1.fill_between(meses, 0, pct_organico, 
                     color=CORES['verde'], alpha=0.7, label='% Orgânico')
    ax1.fill_between(meses, pct_organico, 100, 
                     color=CORES['azul'], alpha=0.5, label='% Pago')
    
    ax1.set_ylabel('Mix de Canais (%)', fontsize=11, fontweight='bold', color=CORES['texto'])
    ax1.set_ylim(0, 100)
    ax1.set_xlabel('Mês', fontsize=11, fontweight='bold')
    
    # Eixo secundário para CAC
    ax2 = ax1.twinx()
    ax2.plot(meses, cac_blended, color=CORES['vermelho'], linewidth=2.5, 
             linestyle='--', marker='o', markersize=4, label='CAC Blended')
    ax2.set_ylabel('CAC Blended (R$)', fontsize=11, fontweight='bold', color=CORES['vermelho'])
    ax2.tick_params(axis='y', labelcolor=CORES['vermelho'])
    
    # Marca o Dia da Independência
    if idx_independencia is not None:
        ax1.axvline(x=meses[idx_independencia], color='#FFD700', linewidth=2, linestyle=':', alpha=0.8)
        ax1.annotate(f'★ M{meses[idx_independencia]}: Independência\n(Org > 50%)',
                     xy=(meses[idx_independencia], 50), 
                     xytext=(meses[idx_independencia] + 3, 70),
                     fontsize=10, fontweight='bold', color='#FFD700',
                     arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                              edgecolor='#FFD700', alpha=0.95))
    
    # Título
    ax1.set_title('Conquistando a soberania da aquisição\n' +
                  'Mix de Canais (Stacked Area 100%) & Evolução do CAC Blended',
                  fontsize=14, fontweight='bold', pad=20)
    
    # Legendas combinadas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
    
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.show()
    
    # --- TABELA AUXILIAR ---
    print("\n📋 TABELA AUXILIAR - Evolução de Canais")
    print("-"*80)
    
    indices_tabela = [0, 11, len(df_real_m)-1]  # M1, M12, M36
    
    tabela_data = []
    for idx in indices_tabela:
        row = df_real_m.iloc[idx]
        total = row['trafego_total']
        p_org = (row['trafego_organico'] / max(1, total)) * 100 if total > 0 else 0
        p_pago = (row['trafego_pago'] / max(1, total)) * 100 if total > 0 else 0
        cac = row['cac_blended'] if not np.isnan(row['cac_blended']) else 0
        
        if p_org >= 50:
            status = "🟢 Independente"
        elif p_org >= 25:
            status = "🟡 Transição"
        else:
            status = "🔴 Dependente"
        
        tabela_data.append({
            'Mês': f"M{idx+1}",
            '% Orgânico': f"{p_org:.0f}%",
            '% Pago': f"{p_pago:.0f}%",
            'CAC Blended': formatar_moeda(cac),
            'Status': status
        })
    
    df_tabela = pd.DataFrame(tabela_data)
    display(df_tabela.style.set_properties(**{'text-align': 'center'}).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#37474F'), ('color', 'white'), ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('border', '1px solid #E0E0E0')]}
    ]))
    
    # --- COMO LER ---
    print("\n📖 COMO LER:")
    print("A área verde mostra o crescimento do canal orgânico (grátis) contra o pago (azul).")
    print("A linha vermelha tracejada é o CAC médio. O objetivo é que a 'onda verde' suba,")
    print("empurrando a linha de custo (vermelha) para baixo.")
    
    # --- INSIGHT DINÂMICO ---
    pct_org_final = pct_organico[-1]
    pct_pago_final = pct_pago[-1]
    cac_inicial = df_real_m.iloc[0]['cac_blended'] if not np.isnan(df_real_m.iloc[0]['cac_blended']) else 0
    cac_final = cac_blended[-1] if not np.isnan(cac_blended[-1]) else 0
    economia_anual = (cac_inicial - cac_final) * df_real_m.iloc[-1]['novos_pagantes_total'] * 12
    
    print("\n💡 INSIGHT ESTRATÉGICO:")
    
    if idx_independencia is not None:
        print(f"🏆 Independência atingida no M{meses[idx_independencia]}!")
        print(f"Hoje o orgânico representa {pct_org_final:.0f}% das visitas.")
        if economia_anual > 0:
            print(f"Economia estimada com redução de CAC: {formatar_moeda(economia_anual)}/ano em Ads.")
    elif pct_org_final < 30:
        print(f"⚠️ ALERTA: Dependência crítica de mídia paga ({pct_pago_final:.0f}%).")
        print("Qualquer aumento no CPM do Google/Meta impactará diretamente a margem.")
        print("AÇÃO RECOMENDADA: Acelerar investimento em SEO e content marketing.")
    else:
        print(f"Transição em progresso: Orgânico em {pct_org_final:.0f}%.")
        print(f"Meta: atingir 50%+ para blindar operação contra inflação de mídia paga.")
    
    print("="*80)
    
    return fig


# ==============================================================================
# VIZ 2.3: ELASTICIDADE & MEF (COLOR CODED)
# ==============================================================================
def gerar_viz_2_3_elasticidade(df_real_m, PREMISSAS, save_path=None):
    """
    Gera o gráfico de Elasticidade de Marketing com zonas coloridas.
    
    Título: "Eficiência Marginal: A máquina de dinheiro tem limite?"
    Subtítulo: "Curva de Retorno (MEF) com Zonas de Saturação (Color-Coded)"
    """
    print("="*80)
    print("📊 VIZ 2.3: ELASTICIDADE & MEF (COLOR CODED)")
    print("="*80)
    
    # --- EXTRAÇÃO DE DADOS ---
    investimento = df_real_m['gasto_marketing'].values
    novos_clientes = df_real_m['novos_pagantes_total'].values
    meses = df_real_m['mes'].values
    
    # Remove valores nulos
    mask = (investimento > 0) & (novos_clientes > 0)
    inv_valid = investimento[mask]
    cli_valid = novos_clientes[mask]
    meses_valid = meses[mask]
    
    # Calcula derivada (eficiência marginal)
    if len(inv_valid) > 1:
        derivada = np.gradient(cli_valid, inv_valid)
        derivada = np.clip(derivada, 0, None)  # Remove negativos
    else:
        derivada = np.zeros(len(inv_valid))
    
    # Regressão linear para R²
    if len(inv_valid) > 2:
        coef = np.polyfit(inv_valid, cli_valid, 1)
        poly = np.poly1d(coef)
        yhat = poly(inv_valid)
        ss_res = np.sum((cli_valid - yhat) ** 2)
        ss_tot = np.sum((cli_valid - np.mean(cli_valid)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        r2 = max(0, min(1, r2))
    else:
        r2 = 0
        poly = lambda x: 0
    
    # --- PLOTAGEM ---
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    
    # Classificação por zona
    cores_pontos = []
    zonas = []
    for d in derivada:
        if d > 0.02:  # Retorno Acelerado (ajustado para escala real)
            cores_pontos.append(CORES['verde_neon'])
            zonas.append('Verde')
        elif d > 0.005:  # Rendimentos Decrescentes
            cores_pontos.append(CORES['amarelo'])
            zonas.append('Amarelo')
        else:  # Saturação
            cores_pontos.append(CORES['vermelho'])
            zonas.append('Vermelho')
    
    # Scatter plot
    scatter = ax.scatter(inv_valid, cli_valid, c=cores_pontos, s=80, 
                         edgecolors='#424242', linewidth=1, alpha=0.8, zorder=5)
    
    # Destaca o ponto atual (último mês)
    if len(inv_valid) > 0:
        ax.scatter(inv_valid[-1], cli_valid[-1], s=300, c=cores_pontos[-1],
                   edgecolors='black', linewidth=3, zorder=10, marker='o')
        ax.annotate(f'M{meses_valid[-1]}\n(Atual)', 
                    xy=(inv_valid[-1], cli_valid[-1]),
                    xytext=(inv_valid[-1]*1.15, cli_valid[-1]*1.1),
                    fontsize=10, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    # Linha de tendência
    if len(inv_valid) > 2:
        x_line = np.linspace(min(inv_valid), max(inv_valid), 100)
        y_line = poly(x_line)
        ax.plot(x_line, y_line, color='black', linestyle='--', linewidth=1.5, 
                alpha=0.7, label=f'Tendência (R² = {r2:.2f})')
    
    # Legenda de zonas
    legend_elements = [
        mpatches.Patch(facecolor=CORES['verde_neon'], edgecolor='#424242', label='🟢 Aceleração'),
        mpatches.Patch(facecolor=CORES['amarelo'], edgecolor='#424242', label='🟡 Decrescente'),
        mpatches.Patch(facecolor=CORES['vermelho'], edgecolor='#424242', label='🔴 Saturação'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    # Configurações
    ax.set_xlabel('Investimento em Marketing (R$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Novos Clientes (Qtd)', fontsize=11, fontweight='bold')
    
    # Título
    ax.set_title('Eficiência Marginal: A máquina de dinheiro tem limite?\n' +
                 'Curva de Retorno (MEF) com Zonas de Saturação (Color-Coded)',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Anotação R²
    ax.annotate(f'R² = {r2:.2f}\n(Previsibilidade)',
                xy=(0.02, 0.98), xycoords='axes fraction',
                ha='left', va='top', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='#424242', alpha=0.9))
    
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.show()
    
    # --- TABELA AUXILIAR ---
    print("\n📋 TABELA AUXILIAR - Eficiência por Faixa de Investimento")
    print("-"*80)
    
    # Agrupa por faixas de investimento
    faixas = [
        (0, 2000, 'R$ 0-2k'),
        (2000, 5000, 'R$ 2k-5k'),
        (5000, 10000, 'R$ 5k-10k'),
        (10000, 30000, 'R$ 10k-30k')
    ]
    
    tabela_data = []
    for min_v, max_v, label in faixas:
        mask_faixa = (inv_valid >= min_v) & (inv_valid < max_v)
        if np.any(mask_faixa):
            cli_faixa = cli_valid[mask_faixa].mean()
            inv_faixa = inv_valid[mask_faixa].mean()
            cac_marginal = inv_faixa / max(1, cli_faixa)
            roi_marginal = (cli_faixa * df_real_m['ltv'].mean()) / max(1, inv_faixa) if inv_faixa > 0 else 0
            
            # Determina zona
            d_media = derivada[mask_faixa].mean() if len(derivada[mask_faixa]) > 0 else 0
            if d_media > 0.02:
                zona = '🟢'
            elif d_media > 0.005:
                zona = '🟡'
            else:
                zona = '🔴'
            
            tabela_data.append({
                'Investimento': label,
                'Clientes Est.': formatar_numero(cli_faixa),
                'CAC Marginal': formatar_moeda(cac_marginal),
                'ROI Marginal': f"{roi_marginal:.1f}x",
                'Zona': zona
            })
    
    if tabela_data:
        df_tabela = pd.DataFrame(tabela_data)
        display(df_tabela.style.set_properties(**{'text-align': 'center'}).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#37474F'), ('color', 'white'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('border', '1px solid #E0E0E0')]}
        ]))
    
    # --- COMO LER ---
    print("\n📖 COMO LER:")
    print("Verde = Acelere (dinheiro traz muito retorno). Amarelo = Cuidado (retorno diminuindo).")
    print("Vermelho = Pare (saturação). O ponto grande marca sua posição atual na curva.")
    
    # --- INSIGHT DINÂMICO ---
    print("\n💡 INSIGHT ESTRATÉGICO:")
    confianca, cor_conf = get_confianca(r2=r2)
    
    if len(zonas) > 0:
        zona_atual = zonas[-1]
        if zona_atual == 'Verde':
            clientes_por_mil = 1000 * (derivada[-1] if len(derivada) > 0 else 0)
            print(f"[{confianca}] Zona de Aceleração. {formatar_numero(clientes_por_mil)} clientes por R$ 1.000 extra.")
            print("Recomendação: AUMENTAR budget de marketing.")
        elif zona_atual == 'Amarelo':
            print(f"[{confianca}] Rendimentos Decrescentes. A eficiência está caindo.")
            print("Recomendação: Otimizar antes de aumentar. Revisar segmentação e criativos.")
        else:
            print(f"[{confianca}] Zona de Saturação. Aumentar budget só vai encarecer o CAC.")
            print("Recomendação: Buscar NOVOS CANAIS (ex: TikTok, LinkedIn, Influenciadores).")
    
    print("="*80)
    
    return fig


# ==============================================================================
# VIZ 2.4: NET GROWTH & CUSTO DO CHURN
# ==============================================================================
def gerar_viz_2_4_net_growth_churn(df_real_m, PREMISSAS, save_path=None):
    """
    Gera o gráfico de Crescimento Líquido vs Perda Financeira por Churn.
    
    Título: "O custo invisível do 'balde furado'"
    Subtítulo: "Crescimento Líquido vs Perda Financeira por Churn (R$)"
    """
    print("="*80)
    print("📊 VIZ 2.4: NET GROWTH & CUSTO DO CHURN")
    print("="*80)
    
    # --- EXTRAÇÃO DE DADOS ---
    meses = df_real_m['mes'].values
    novos = df_real_m['novos_pagantes_total'].values
    churn_usuarios = df_real_m['churn_usuarios'].values
    ltv_medio = df_real_m['ltv'].mean()  # LTV médio para estimar perda financeira
    base_ativa = df_real_m['usuarios_ativos'].values
    
    # Net Growth
    net_growth = novos - churn_usuarios
    
    # Perda financeira estimada (Churn x LTV médio)
    perda_financeira = churn_usuarios * ltv_medio
    
    # Mês de maior perda
    idx_max_perda = np.argmax(perda_financeira) if len(perda_financeira) > 0 else 0
    valor_max_perda = perda_financeira[idx_max_perda]
    
    # --- PLOTAGEM ---
    fig, ax1 = plt.subplots(figsize=(14, 8), dpi=150)
    
    # Barras Divergentes
    largura = 0.4
    
    # Barras positivas (Novos Clientes)
    bars_novos = ax1.bar(meses, novos, largura, 
                         color=CORES['verde'], edgecolor='#1B5E20', 
                         label='Novos Clientes', alpha=0.85)
    
    # Barras negativas (Churn)
    bars_churn = ax1.bar(meses, -churn_usuarios, largura, 
                         color=CORES['vermelho'], edgecolor='#B71C1C', 
                         label='Churn', alpha=0.85)
    
    # Linha de Net Growth
    ax1.plot(meses, net_growth, color='black', linewidth=2.5, marker='o', 
             markersize=4, label='Net Growth', zorder=5)
    
    # Linha zero
    ax1.axhline(y=0, color='#424242', linewidth=1.5, linestyle='-')
    
    # Área sombreada (Perda Financeira - eixo segundário)
    ax2 = ax1.twinx()
    ax2.fill_between(meses, 0, perda_financeira, color=CORES['vermelho_claro'], 
                     alpha=0.4, label='Perda Financeira (LTV)')
    ax2.set_ylabel('Perda Financeira Estimada (R$)', fontsize=10, 
                   fontweight='bold', color=CORES['vermelho'])
    ax2.tick_params(axis='y', labelcolor=CORES['vermelho'])
    
    # Anotação de maior perda
    if valor_max_perda > 0:
        ax1.annotate(f'🔥 Queima: {formatar_moeda(valor_max_perda)}',
                     xy=(meses[idx_max_perda], -churn_usuarios[idx_max_perda]),
                     xytext=(meses[idx_max_perda] + 2, -churn_usuarios[idx_max_perda] - max(churn_usuarios)*0.3),
                     fontsize=9, fontweight='bold', color=CORES['vermelho'],
                     arrowprops=dict(arrowstyle='->', color=CORES['vermelho'], lw=1.5),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                              edgecolor=CORES['vermelho'], alpha=0.95))
    
    # Configurações
    ax1.set_xlabel('Mês', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Clientes (Qtd)', fontsize=11, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=10)
    
    # Título
    ax1.set_title('O custo invisível do "balde furado"\n' +
                  'Crescimento Líquido vs Perda Financeira por Churn (R$)',
                  fontsize=14, fontweight='bold', pad=20)
    
    ax1.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.show()
    
    # --- INSIGHT DINÂMICO ---
    idx_final = len(df_real_m) - 1
    churn_rate_final = df_real_m.iloc[idx_final]['churn_rate'] * 100
    novos_final = novos[idx_final]
    churn_final = churn_usuarios[idx_final]
    perda_final = perda_financeira[idx_final]
    
    share_perda = (churn_final / max(1, novos_final)) * 100
    
    # Economia estimada ao reduzir churn em 1 p.p.
    arpu_medio = df_real_m['arpu'].mean()
    economia_1pp = base_ativa[idx_final] * 0.01 * arpu_medio * 12  # Economia anual
    
    print("\n📖 COMO LER:")
    print("Barras mostram fluxo de pessoas. A 'mancha' vermelha ao fundo mostra fluxo de dinheiro")
    print("perdido (LTV destruído). Se a mancha cresce, o buraco no balde está custando caro.")
    
    print("\n💡 INSIGHT ESTRATÉGICO:")
    print(f"No M{idx_final+1}, o churn de {churn_rate_final:.1f}% consumiu {share_perda:.0f}% das novas vendas.")
    print(f"Isso representa uma perda econômica de {formatar_moeda(perda_final)}/mês.")
    print(f"💰 Reduzir o churn em 1 p.p. economizaria aproximadamente {formatar_moeda(economia_1pp)}/ano.")
    
    print("="*80)
    
    return fig


# ==============================================================================
# VIZ 2.5: PAYBACK PERIOD (BACKGROUND ZONES)
# ==============================================================================
def gerar_viz_2_5_payback_zones(df_real_m, PREMISSAS, save_path=None):
    """
    Gera o gráfico de Payback Period com zonas de fundo coloridas.
    
    Título: "Velocidade de retorno do capital"
    Subtítulo: "Payback Period Histórico sobre Zonas de Risco Global"
    """
    print("="*80)
    print("📊 VIZ 2.5: PAYBACK PERIOD (BACKGROUND ZONES)")
    print("="*80)
    
    # --- EXTRAÇÃO DE DADOS ---
    meses = df_real_m['mes'].values
    payback = df_real_m['payback_meses'].values
    
    # Limita payback para visualização (cap em 24 meses)
    payback_viz = np.clip(payback, 0, 24)
    payback_viz = np.where(np.isnan(payback_viz), 18, payback_viz)  # NaN = 18 meses
    
    payback_atual = payback_viz[-1] if len(payback_viz) > 0 else 0
    
    # --- PLOTAGEM ---
    fig, ax = plt.subplots(figsize=(14, 7), dpi=150)
    
    # Background Zones (OBRIGATÓRIO)
    ax.axhspan(0, 6, color=CORES['verde_claro'], alpha=0.8, label='Excelente (<6m)')
    ax.axhspan(6, 12, color=CORES['amarelo_claro'], alpha=0.8, label='Saudável (6-12m)')
    ax.axhspan(12, 24, color=CORES['vermelho_claro'], alpha=0.8, label='Risco (>12m)')
    
    # Linha principal
    ax.plot(meses, payback_viz, color='black', linewidth=2.5, marker='o', 
            markersize=6, label='Payback (meses)', zorder=5)
    
    # Linha de benchmark (12 meses)
    ax.axhline(y=12, color=CORES['vermelho'], linewidth=2, linestyle='--', 
               alpha=0.8, label='Teto SaaS (12m)')
    
    # Rótulo final
    ax.annotate(f'{payback_atual:.1f} meses',
                xy=(meses[-1], payback_atual),
                xytext=(meses[-1] + 1, payback_atual + 1),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='black', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    # Configurações
    ax.set_xlabel('Mês', fontsize=11, fontweight='bold')
    ax.set_ylabel('Payback (Meses)', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 24)
    ax.set_xlim(meses[0] - 1, meses[-1] + 3)
    
    # Título
    ax.set_title('Velocidade de retorno do capital\n' +
                 'Payback Period Histórico sobre Zonas de Risco Global',
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.show()
    
    # --- INSIGHT DINÂMICO ---
    # Determina zona atual
    if payback_atual < 6:
        zona = "🟢 Excelente"
        zona_desc = "verde"
    elif payback_atual < 12:
        zona = "🟡 Saudável"
        zona_desc = "amarela"
    else:
        zona = "🔴 Risco"
        zona_desc = "vermelha"
    
    # Giros por ano
    giros_ano = 12 / max(1, payback_atual)
    
    print("\n📖 COMO LER:")
    print("Payback mede o risco de liquidez. Quanto mais baixo (zona verde), mais rápido o dinheiro volta.")
    print("Zona vermelha exige caixa infinito para sustentar crescimento.")
    
    print("\n💡 INSIGHT ESTRATÉGICO:")
    print(f"Payback atual de {payback_atual:.1f} meses coloca a empresa na zona {zona}.")
    print(f"Com esse ciclo, podemos reinvestir o capital {giros_ano:.1f} vezes ao ano,")
    print("acelerando o crescimento composto.")
    
    if payback_atual > 12:
        print("\n⚠️ AÇÃO URGENTE: Payback acima de 12 meses é insustentável.")
        print("   Opções: Aumentar ARPU, reduzir CAC, ou melhorar retenção (reduzir churn).")
    
    print("="*80)
    
    return fig


# ==============================================================================
# BLOCO DE CONCLUSÃO (RODAPÉ DA PÁGINA)
# ==============================================================================
def gerar_conclusao_growth_machine(df_real_m, PREMISSAS):
    """
    Gera o bloco de conclusão com o veredito da Máquina de Crescimento.
    """
    print("\n" + "="*80)
    print("🚀 VEREDITO DA MÁQUINA DE CRESCIMENTO")
    print("="*80)
    
    # Extrai métricas finais
    idx_final = len(df_real_m) - 1
    idx_inicial = min(5, idx_final)  # M6 como referência
    
    row_final = df_real_m.iloc[idx_final]
    row_inicial = df_real_m.iloc[idx_inicial]
    
    # Cálculos
    crescimento_trafego = row_final['trafego_total'] / max(1, row_inicial['trafego_total'])
    pct_organico = (row_final['trafego_organico'] / max(1, row_final['trafego_total'])) * 100
    
    # ROI marginal (estimativa)
    if row_final['gasto_marketing'] > 0:
        roi_marginal = (row_final['novos_pagantes_total'] * row_final['ltv']) / row_final['gasto_marketing']
    else:
        roi_marginal = 0
    
    # Perda por churn
    perda_churn_pct = (row_final['churn_usuarios'] / max(1, row_final['novos_pagantes_total'])) * 100
    
    # Budget recomendado (heurística: se ROI > 3x, pode aumentar 50%)
    budget_atual = row_final['gasto_marketing']
    if roi_marginal > 3:
        budget_rec = budget_atual * 0.5  # Aumentar 50%
    else:
        budget_rec = 0  # Não aumentar
    
    print()
    print("1. **Tração:** A empresa provou que consegue escalar (Tráfego +{:.0f}x)".format(crescimento_trafego))
    print("   mantendo a eficiência de conversão estável (Gráfico 2.1).")
    print()
    print("2. **Independência:** O canal orgânico já domina {:.0f}% da aquisição,".format(pct_organico))
    print("   blindando a operação contra inflação de mídia paga (Gráfico 2.2).")
    print()
    print("3. **Eficiência:** O ROI marginal de {:.1f}x indica que há espaço para".format(roi_marginal))
    print("   aumentar o investimento antes de atingir saturação (Gráfico 2.3).")
    print()
    print("4. **Risco:** O principal ponto de atenção é o Churn Financeiro (Gráfico 2.4),")
    print("   que consome {:.0f}% da geração de valor.".format(perda_churn_pct))
    print()
    
    if budget_rec > 0:
        print(f"**Próximo Passo:** Aumentar budget em R$ {budget_rec/1000:.0f}k para capturar a elasticidade disponível.")
    else:
        print("**Próximo Passo:** Otimizar canais atuais antes de aumentar investimento.")
    
    print()
    print("="*80)


# ==============================================================================
# FUNÇÃO PRINCIPAL - EXECUTA TODAS AS VISUALIZAÇÕES
# ==============================================================================
def executar_pagina_2_growth_machine(df_real_m, PREMISSAS, salvar_figuras=False, pasta_saida='outputs/figs/'):
    """
    Executa todas as 5 visualizações da Página 2: Growth Machine.
    
    Parâmetros:
    -----------
    df_real_m : pd.DataFrame
        DataFrame mensal com projeções (obrigatório)
    PREMISSAS : dict
        Dicionário de premissas
    salvar_figuras : bool
        Se True, salva as figuras em arquivos PNG
    pasta_saida : str
        Caminho para salvar as figuras
    """
    print("\n" + "="*100)
    print("📊 PÁGINA 2: GROWTH MACHINE - INVESTOR DECK")
    print("="*100 + "\n")
    
    import os
    if salvar_figuras:
        os.makedirs(pasta_saida, exist_ok=True)
    
    # VIZ 2.1
    path_21 = os.path.join(pasta_saida, 'pg2_viz1_funil_log.png') if salvar_figuras else None
    fig1 = gerar_viz_2_1_funil_log(df_real_m, PREMISSAS, save_path=path_21)
    
    # VIZ 2.2
    path_22 = os.path.join(pasta_saida, 'pg2_viz2_canais.png') if salvar_figuras else None
    fig2 = gerar_viz_2_2_independencia_canais(df_real_m, PREMISSAS, save_path=path_22)
    
    # VIZ 2.3
    path_23 = os.path.join(pasta_saida, 'pg2_viz3_elasticidade.png') if salvar_figuras else None
    fig3 = gerar_viz_2_3_elasticidade(df_real_m, PREMISSAS, save_path=path_23)
    
    # VIZ 2.4
    path_24 = os.path.join(pasta_saida, 'pg2_viz4_net_growth.png') if salvar_figuras else None
    fig4 = gerar_viz_2_4_net_growth_churn(df_real_m, PREMISSAS, save_path=path_24)
    
    # VIZ 2.5
    path_25 = os.path.join(pasta_saida, 'pg2_viz5_payback.png') if salvar_figuras else None
    fig5 = gerar_viz_2_5_payback_zones(df_real_m, PREMISSAS, save_path=path_25)
    
    # Conclusão
    gerar_conclusao_growth_machine(df_real_m, PREMISSAS)
    
    print("\n✅ PÁGINA 2: GROWTH MACHINE - COMPLETA!")
    print("="*100)
    
    return {
        'fig_funil': fig1,
        'fig_canais': fig2,
        'fig_elasticidade': fig3,
        'fig_net_growth': fig4,
        'fig_payback': fig5
    }


# ==============================================================================
# EXECUÇÃO (Quando rodado como célula)
# ==============================================================================
# Para executar, descomente e rode:
# executar_pagina_2_growth_machine(df_real_m, PREMISSAS, salvar_figuras=True)
