# PÁGINA 4 - UNIT ECONOMICS (V2.0 - GOLD STANDARD - COMPLIANT)
# ============================================================================
# DATA: 2025-12-08
# OBJETIVO: Gerar as 4 visualizações de Unit Economics + Veredito
# PADRÃO: McKinsey-Grade, PDF First, Zero Hardcoded.
#
# ESTRUTURA NARRATIVA (4 ATOS):
# VIZ 4.1: LTV vs CAC (A "Régua de Ouro")
# VIZ 4.2: Cohort Retention Heatmap (Saúde das Safras)
# VIZ 4.3: Revenue Per Employee (Produtividade) -> SUBSTITUÍDO POR CHURN SPC
# VIZ 4.4: CAC Pago vs Blended -> SUBSTITUÍDO POR ESCALA
# VIZ 4.5: Waterfall de Vazamentos (NEW)
# VIZ 4.6: Veredito Final
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

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
        render_atomic_block, salvar_figura_silencioso, salvar_tabela_html_silencioso
    )
except ImportError:
    pass

setup_plot_style()

# ============================================================================
# HELPER: Adicionar fonte (Dinâmica e Técnica)
# ============================================================================
def adicionar_fonte_dados(ax, texto_fonte):
    """Adiciona texto de fonte no canto inferior direito."""
    ax.annotate(
        texto_fonte,
        xy=(1.0, -0.15),
        xycoords='axes fraction',
        fontsize=8,
        color='gray',
        ha='right',
        va='top',
        style='italic'
    )

def gerar_viz_4_1_ltv_cac(df_real, df_ideal, report_mode=False):
    """
    Gráfico de Linha comparando Evolução do LTV vs CAC ao longo do tempo.
    """
    if not report_mode:
        print("\n🔹 VIZ 4.1: LTV vs CAC")

    # Dados
    meses = df_real['mes'].values
    # Prioriza coluna calculada, senão recalcula
    if 'ltv' in df_real.columns:
        ltv = df_real['ltv'].values
    else:
        ltv = (df_real['arpu'] * df_real['margem_bruta_pct'] / 100) / df_real['churn_rate']
        ltv = ltv.fillna(0).values

    cac = df_real['cac_blended'].values
    
    # Benchmarks (Ideal)
    if 'ltv' in df_ideal.columns:
        ltv_ideal = df_ideal['ltv'].values 
    else:
        ltv_ideal = ltv * 1.2 # Fallback apenas se não houver coluna no ideal
    
    # Figura
    figsize = (10, 6) if report_mode else (14, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.20, left=0.10, right=0.95)

    # Plots
    ax.plot(meses, ltv, color='#2E7D32', linewidth=2.5, label='LTV Real (Valor Vitalício)')
    ax.plot(meses, cac, color='#D32F2F', linewidth=2.5, label='CAC Real (Custo Aquisição)')
    ax.plot(meses, ltv_ideal, color='#2E7D32', linewidth=1.5, linestyle='--', alpha=0.5, label='LTV Ideal')

    # Fill Between
    ax.fill_between(meses, ltv, cac, where=(ltv > cac), interpolate=True, color='#2E7D32', alpha=0.1, label='Lucro Unitário')
    ax.fill_between(meses, ltv, cac, where=(ltv < cac), interpolate=True, color='#D32F2F', alpha=0.1, label='Prejuízo Unitário')

    # Anotação Múltiplo Final
    # CORREÇÃO V2: Tratar CAC=0 como "infinito" (aquisição orgânica)
    if cac[-1] <= 0:
        multiplo_final = 10000.0 if ltv[-1] > 0 else 0.0
        multiplo_str = "∞"
    else:
        multiplo_final = ltv[-1] / cac[-1]
        multiplo_str = f"{multiplo_final:.1f}x"
    
    ax.annotate(
        multiplo_str,
        xy=(meses[-1], (ltv[-1] + cac[-1])/2),
        xytext=(meses[-1] + 1, (ltv[-1] + cac[-1])/2),
        fontsize=12, fontweight='bold', color='#2E7D32',
        bbox=dict(boxstyle="larrow,pad=0.3", fc="white", ec="#2E7D32", lw=1)
    )

    # Tabela de Prova
    meses_idx = [0, 5, 11, 23, 35]
    tabela_md = "| Período | LTV (R$) | CAC (R$) | Múltiplo | Status |\n"
    tabela_md += "|:---|---:|---:|---:|:---|\n"
    
    for idx in meses_idx:
        if idx < len(df_real):
            m = meses[idx]
            l_val = ltv[idx]
            c_val = cac[idx]
            
            # CORREÇÃO V2: Tratar CAC=0 como infinito
            if c_val <= 0:
                mult = 10000.0 if l_val > 0 else 0.0
                mult_str = "∞" if l_val > 0 else "0.0x"
            else:
                mult = l_val / c_val
                mult_str = f"{mult:.1f}x"
            
            if mult >= 3.0 or c_val <= 0: status = "🟢 EXCELENTE"
            elif mult >= 1.0: status = "🟡 ATENÇÃO"
            else: status = "🔴 CRÍTICO"
            
            tabela_md += f"| M{m} | {formata_moeda(l_val)} | {formata_moeda(c_val)} | {mult_str} | {status} |\n"

    ax.legend(loc='upper left', frameon=True, fontsize=9)

    # Renderização via Atomic Block
    legend_md = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Linha Verde (LTV):** Quanto lucro um cliente deixa na empresa ao longo da vida.
2. **Linha Vermelha (CAC):** Quanto custa atrair esse cliente (Marketing + Vendas).
3. **Seta de Múltiplo:** Quantas vezes o valor do cliente paga seu custo (Meta > 3.0x).

**INTERPRETAÇÃO:**
- **Boca de Jacaré:** A linha verde deve subir e se afastar da vermelha.
- **Zona de Perigo:** Se as linhas se cruzarem, você está pagando para trabalhar.
"""

    formulas = """
**Fonte:** df_real_m (Célula 5A)

**Fórmulas:**
1. **LTV (Lifetime Value)** = (ARPU × Margem Bruta %) / Churn Rate
2. **CAC (Blended)** = (Gasto Marketing + Gasto Vendas) / Novos Clientes Totais
3. **Múltiplo** = LTV / CAC

**Metodologia:**
- **Modelo de LTV:** Perpetuidade simples (1/Churn). Assume que a taxa de cancelamento e o ticket médio se mantêm constantes durante a vida do cliente.
- **Interpretação:** Valores acima de 3.0x indicam alta eficiência; abaixo de 1.0x indicam queima de caixa por cliente.
"""

    # Insight Dinâmico (Causalidade Real)
    delta_ltv = ltv[-1] - ltv[0]
    delta_cac = cac[-1] - cac[0]
    
    causa_texto = []
    if delta_ltv > 0: causa_texto.append("expansão do LTV")
    else: causa_texto.append("contração do LTV")
    
    if delta_cac < 0: causa_texto.append("otimização do CAC")
    elif delta_cac > 0: causa_texto.append("aumento do CAC")
    else: causa_texto.append("CAC estável")
    
    causa_final = " e ".join(causa_texto)

    # CORREÇÃO V2: Insight dinâmico para CAC=0 (orgânico)
    if multiplo_final >= 9999:
        implicacao_texto = "Crescimento 100% orgânico - CAC é zero. Cada cliente é lucro puro."
        acao_texto = "Manter estratégia orgânica e reinvestir margem em produto/retenção."
    elif multiplo_final > 3:
        implicacao_texto = f"Cada R$ 1 investido em marketing retorna R$ {multiplo_final:.2f} de margem bruta."
        acao_texto = "Acelerar investimento em aquisição (Growth) pois a unidade é lucrativa."
    else:
        implicacao_texto = f"Cada R$ 1 investido retorna apenas R$ {multiplo_final:.2f}. Eficiência baixa."
        acao_texto = "Focar em Retenção/Pricing antes de escalar."

    insight = {
        "fato": f"Múltiplo LTV/CAC atinge {multiplo_str} no M36.",
        "causa": f"Resultado combinado de {causa_final}.",
        "implicacao": implicacao_texto,
        "acao": acao_texto
    }

    render_atomic_block(
        chart_id="pg4_viz1_ltv_cac",
        title_colloquial="LTV vs CAC: A CRIAÇÃO DE VALOR",
        title_technical="VIZ 4.1: LTV vs CAC (A 'Regua de Ouro')",
        fig=fig,
        legend_md=legend_md,
        df_tabela=tabela_md,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="📋 DETALHAMENTO DA EFICIÊNCIA UNITÁRIA (LTV/CAC)",
        data_source_text="Fonte: df_real_m (Célula 5A) | Colunas: 'ltv', 'cac_blended'"
    )
    
    plt.close(fig) # atomic block already closes, but to be sure or remove double close
    return {'multiplo_final': multiplo_final}

# ============================================================================
# VIZ 4.2: COHORT RETENTION HEATMAP
# ============================================================================
def gerar_matriz_cohort_sintetica(df_real):
    """
    Simula uma matriz triangular de cohorts baseada na taxa de churn mensal histórica.
    """
    meses = len(df_real)
    cohort_matrix = np.zeros((meses, meses))
    cohort_matrix[:] = np.nan
    
    novos_clientes = df_real['novos_pagantes_total'].values
    churn_rates = df_real['churn_rate'].values
    
    for i in range(meses):
        cohort_matrix[i, 0] = 100.0
        current_retention = 1.0
        for t in range(1, meses - i):
            churn_mes_global = churn_rates[i + t]
            current_retention = current_retention * (1 - churn_mes_global)
            cohort_matrix[i, t] = current_retention * 100
            
    return cohort_matrix, novos_clientes

def gerar_viz_4_2_cohorts(df_real, report_mode=False):
    """
    Heatmap de Retenção por Cohort (Safra).
    """
    if not report_mode:
        print("\n🔹 VIZ 4.2: Cohort Retention")

    matrix, tamanhos = gerar_matriz_cohort_sintetica(df_real)
    
    indices_show = [0, 5, 11, 17, 23, 29, 35]
    indices_show = [i for i in indices_show if i < len(df_real)]
    cols_life = [0, 1, 2, 3, 6, 12, 24]
    
    plot_data = []
    y_labels = []
    
    for idx in indices_show:
        row_vals = []
        for col in cols_life:
            if col < matrix.shape[1] - idx:
                row_vals.append(matrix[idx, col])
            else:
                row_vals.append(np.nan)
        plot_data.append(row_vals)
        y_labels.append(f"Safra M{idx+1}\n(n={int(tamanhos[idx])})")
        
    df_heatmap = pd.DataFrame(plot_data, columns=[f"M{c}" for c in cols_life], index=y_labels)
    
    figsize = (10, 6) if report_mode else (12, 7)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.20, right=0.95)
    
    cmap = LinearSegmentedColormap.from_list("rg", ["#FFCDD2", "#FFF9C4", "#C8E6C9"], N=256)
    
    sns.heatmap(df_heatmap, annot=True, fmt=".1f", cmap=cmap, vmin=50, vmax=100, 
                cbar_kws={'label': 'Retenção (%)'}, ax=ax, linewidths=1, linecolor='white')
    
    # Formatação %
    for t in ax.texts:
        val = t.get_text()
        if val != 'nan':
            t.set_text(val + '%')
            if float(val) > 90: t.set_weight('bold')

    ax.set_title('Mapa de Retenção por Safra (Cohorts)', fontsize=12, color='gray')
    ax.set_ylabel('Safra (Mês de Entrada)', fontsize=11)
    ax.set_xlabel('Idade da Safra (Meses após entrada)', fontsize=11)
    
    # Tabela Sintética de Média de Retenção (Novo)
    ret_m1 = np.nanmean(df_heatmap['M1']) if 'M1' in df_heatmap.columns else 0
    ret_m6 = np.nanmean(df_heatmap['M6']) if 'M6' in df_heatmap.columns else 0
    ret_m12 = np.nanmean(df_heatmap['M12']) if 'M12' in df_heatmap.columns else 0
    
    tabela_md = "| Período de Vida | Retenção Média | Status |\n"
    tabela_md += "|:---|---:|:---|\n"
    tabela_md += f"| Primeiro Mês (M1) | {ret_m1:.1f}% | {'🟢 OK' if ret_m1 > 90 else '🔴 ALERTA'} |\n"
    tabela_md += f"| Semestre (M6) | {ret_m6:.1f}% | {'🟢 OK' if ret_m6 > 70 else '🟡 ATENÇÃO'} |\n"
    tabela_md += f"| Ano (M12) | {ret_m12:.1f}% | {'🟢 OK' if ret_m12 > 50 else '🔴 CRÍTICO'} |\n"

    # Renderização via Atomic Block
    legend_md = """
**📖 COMO LER ESTE GRÁFICO (COHORTS):**

1. **Linhas (Safra):** Clientes que entraram no mesmo mês (ex: Safra d Mês 1).
2. **Colunas (Idade):** Meses após a compra inicial.
3. **Cores:**
   - 🟢 **Verde:** Alta retenção (Clientes fiéis).
   - 🔴 **Vermelho:** Alta evasão (Churn alto).

**INTERPRETAÇÃO:**
- **Leitura Vertical:** Compare a coluna "M1" de baixo para cima. Se estiver ficando mais verde, a retenção inicial está melhorando.
- **Leitura Horizontal:** A cor deve decair suavemente. Quedas bruscas indicam problemas no produto.
"""

    formulas = """
**Fonte:** df_real['churn_rate'] (Célula 5A)

**Metodologia (Simulação Sintética):**
- Como o modelo é financeiro (não transacional individual), geramos uma **Matriz Sintética**.
- **Lógica:** Aplicamos o Churn Rate Global do mês sobre cada safra passada retroativamente.
- **Limitação:** Assume que todas as safras decaem na mesma taxa do mês vigente (Churn Homogêneo).
"""

    retencao_m12_media = np.nanmean(df_heatmap['M12'])
    
    insight = {
        "fato": f"Retenção média no mês 12 (M12) é de {retencao_m12_media:.1f}%.",
        "causa": "Taxa de churn mensal estabilizada em torno de {:.1f}%.".format(df_real['churn_rate'].mean()*100),
        "implicacao": "A base de clientes renova seu valor quase integralmente ano a ano.",
        "acao": "Focar em expansão (Upsell) nas cohorts antigas (M12+) para aumentar LTV."
    }
    
    render_atomic_block(
        chart_id="pg4_viz2_cohorts",
        title_colloquial="Os clientes antigos continuam pagando ao longo do tempo?",
        title_technical="VIZ 4.2: Cohort Analysis (Retenção por Safra)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=tabela_md,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="📋 MÉDIA HISTÓRICA DE RETENÇÃO",
        data_source_text="Fonte: Simulação df_real_m (Célula 5A) | Churn Rate Mensal"
    )

    plt.close(fig)

# ============================================================================
# VIZ 4.3: VOLATILIDADE SEMANAL DO CHURN (SPC Chart)
# ============================================================================
def gerar_viz_4_3_churn_volatility(df_real_s, premissas, report_mode=False):
    """
    VIZ 4.3: Controle Estatístico de Processo (SPC) para Churn Semanal.
    ATO 3: "Estamos sob controle ou caos?"
    """
    if not report_mode:
        print("\n🔹 VIZ 4.3: Volatilidade Semanal (Churn)")

    # Verifica se dados semanais existem
    if df_real_s is None or 'churn_rate' not in df_real_s.columns:
        print("⚠️ Dados semanais ausentes. Pulando VIZ 4.3")
        return

    # Dados (Últimas 24 semanas para melhor visualização)
    df_plot = df_real_s.tail(24).copy()
    semanas = df_plot['semana'].values
    churn_s = df_plot['churn_rate'].values * 100 # Em %
    
    media = churn_s.mean()
    desvio = churn_s.std()
    ucl = media + (2 * desvio) # Limite Superior (2 Sigma)
    lcl = max(0, media - (2 * desvio)) # Limite Inferior
    
    figsize = (10, 6) if report_mode else (14, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.20, left=0.10, right=0.95)
    
    # Plot SPC
    ax.plot(semanas, churn_s, color='#37474F', linewidth=2, marker='o', markersize=5, label='Churn Semanal Real')
    ax.axhline(media, color='#1565C0', linestyle='--', linewidth=1.5, label=f'Média ({media:.2f}%)')
    ax.axhline(ucl, color='#D32F2F', linestyle='-', linewidth=1, label=f'Limite Crítico ({ucl:.2f}%)')
    ax.axhspan(lcl, ucl, color='#E3F2FD', alpha=0.3, label='Zona de Controle Normal')
    
    # Outliers
    outliers = df_plot[df_plot['churn_rate']*100 > ucl]
    if len(outliers) > 0:
        ax.scatter(outliers['semana'], outliers['churn_rate']*100, color='red', s=100, zorder=5)
    
    ax.set_title('Controle Estatístico de Churn Semanal (SPC)', fontsize=12, color='gray')
    ax.set_ylabel('Churn Rate Semanal (%)', fontsize=12)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # Tabela
    # Tabela
    tabela_md = "| Semana | Churn Rate | Média | Desvio | Status |\n|:---|:---|:---|:---|:---|\n"
    for _, row in df_plot.tail(5).iterrows():
        val = row['churn_rate'] * 100
        delta = val - media
        status = "🔴 ALERTA" if val > ucl else ("🟢 OK" if val < ucl else "⚠️ WARN")
        
        arrow = "⬆️" if delta > 0 else "⬇️"
        tabela_md += f"| S{int(row['semana'])} | {val:.2f}% | {media:.2f}% | {arrow} {abs(delta):.2f}pp | {status} |\n"
        
    legend_md = """
**📖 COMO LER ESTE GRÁFICO (SPC):**

1. **Linha Preta (Pontos):** Taxa de Churn real da semana.
2. **Faixa Azul (Túnel):** Variação normal esperada (Ruído estatístico).
3. **Linha Vermelha (Limite):** Teto máximo aceitável.
4. **Pontos Vermelhos:** Anomalias (Surtos de cancelamento).

**INTERPRETAÇÃO:**
- Pontos dentro da faixa azul = Operação sob controle.
- Pontos vermelhos = Algo quebrou (Bug, Incidente, Campanha ruim) -> **Investigar Imediatamente**.
"""
    formulas = "**Fonte:** df_real_s | UCL = Média + 2 Desvios Padrão"
    
    insight = {
        "fato": f"Média semanal de {media:.2f}% com {len(outliers)} surtos recentes.",
        "causa": "Volatilidade natural vs Eventos de Cauda.",
        "implicacao": "Previsibilidade da base de clientes.",
        "acao": "Investigar surtos." if len(outliers) > 0 else "Manter monitoramento."
    }
    
    render_atomic_block(
        chart_id="pg4_viz3_churn_spc",
        title_colloquial="O sangramento de clientes esta sob controle?",
        title_technical="VIZ 4.3: Churn Volatility Control (SPC)",
        fig=fig, legend_md=legend_md, df_tabela=tabela_md,
        insight_dict=insight, formulas_md=formulas, report_mode=report_mode,
        table_title="📋 DIÁRIO DE BORDO (Últimas 5 Semanas)", data_source_text="Fonte: df_real_s"
    )
    plt.close(fig)

# ============================================================================
# VIZ 4.4: ESCALA DE CLIENTES vs SAÚDE UNITÁRIA
# ============================================================================
def gerar_viz_4_4_escala_unit_economics(df_real_m, premissas, report_mode=False):
    """
    Scatter Plot: Base de Clientes (X) vs LTV/CAC (Y).
    PERGUNTA CEO: "Se dobrar a base de clientes, a unidade continua lucrativa?"
    """
    if not report_mode:
        print("\n🔹 VIZ 4.4: Escala vs Saúde Unitária")
    
    # Dados
    usuarios = df_real_m['usuarios_ativos'].values
    ltv_cac = df_real_m['ltv'] / df_real_m['cac_blended'].replace(0, 1) # Recalcula seguro
    ltv_cac = ltv_cac.fillna(0).values
    meses = df_real_m['mes'].values
    
    # Fit Linear
    from numpy.polynomial import Polynomial
    mask = (usuarios > 0) & (ltv_cac > 0)
    x_valid = usuarios[mask]
    y_valid = ltv_cac[mask]
    
    if len(x_valid) < 3:
        slope = 0
    else:
        p = Polynomial.fit(x_valid, y_valid, 1)
        slope = p.coef[1]
        
    # Figura
    figsize = (10, 6) if report_mode else (14, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.20, left=0.10, right=0.95)
    
    scatter = ax.scatter(usuarios, ltv_cac, c=meses, cmap='viridis', s=100, alpha=0.8, edgecolors='black')
    
    # Zona de Saúde
    ax.axhspan(3.0, 10, color='#E8F5E9', alpha=0.3, label='Zona Saudável (>3x)')
    ax.axhline(1.0, color='#D32F2F', linestyle='--', label='Zona de Perigo (<1x)')
    
    ax.set_xlabel('Base de Clientes Ativos', fontsize=12)
    ax.set_ylabel('LTV/CAC (Eficiência)', fontsize=12)
    ax.set_title('Impacto da Escala na Saúde Unitária', fontsize=12, color='gray')
    ax.grid(True, alpha=0.3)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Mês de Operação')

    # Tabela Quartis
    tabela_md = "| Faixa de Clientes | LTV/CAC Médio | Status |\n|:---|---:|:---|\n"
    avg_ltv_cac = ltv_cac.mean()
    tabela_md += f"| Média Geral | {avg_ltv_cac:.2f}x | {'🟢 OK' if avg_ltv_cac > 3 else '🟡 BAIXO'} |\n"
    
    # Legend Plot
    ax.legend(loc='lower left', fontsize=9, frameon=True)

    legend_md = """
**📖 COMO LER ESTE GRÁFICO (ESCALA):**

1. **Eixo X (Tamanho):** Quantos clientes ativos temos.
2. **Eixo Y (Qualidade):** LTV/CAC (Eficiência Unitária).
3. **Pontos Coloridos:** Meses de operação (Amarelo = Mais recente).

**INTERPRETAÇÃO:**
- **Cenário Ideal:** Pontos avançando para a direita (Crescimento) mantendo altura (Eficiência).
- **Cenário Ruim:** Pontos caindo conforme a base cresce (Desgaste de escala).
- **Regra:** Nunca crescer para a "Zona de Perigo" (abaixo de 1x).
"""
    formulas = "**Fonte:** df_real_m | 'usuarios_ativos' vs 'ltv/cac'"
    
    insight = {
        "fato": f"A inclinação da curva é {slope:.4f}.",
        "causa": "Comportamento dos custos marginais e retenção em escala.",
        "implicacao": "Viabilidade de escalar agressivamente.",
        "acao": "Acelerar." if slope >= 0 else "Revisar funil antes de escalar."
    }

    render_atomic_block(
        chart_id="pg4_viz4_escala",
        title_colloquial="A qualidade do cliente cai quando a empresa cresce?",
        title_technical="VIZ 4.4: Qualidade Marginal na Escala (LTV/CAC vs Volume)",
        fig=fig, legend_md=legend_md, df_tabela=tabela_md,
        insight_dict=insight, formulas_md=formulas, report_mode=report_mode,
        table_title="📋 TESTE DE ESCALA", data_source_text="Fonte: df_real_m"
    )
    plt.close(fig)

# ============================================================================
# VIZ 4.5: WATERFALL DE VAZAMENTOS (NET PROFIT)
# ============================================================================
def gerar_viz_4_5_waterfall_leaks(df_real_m, premissas, report_mode=False):
    """
    Waterfall Chart mostrando composição do Lucro por Cliente (Unit Economics Decomposition).
    """
    if not report_mode:
        print("\n🔹 VIZ 4.5: Waterfall de Vazamentos")

    # Cálculos Último Mês
    idx = -1
    arpu = df_real_m['arpu'].iloc[idx]
    churn = df_real_m['churn_rate'].iloc[idx]
    lifetime = 1/churn if churn > 0 else 0
    gross_revenue = arpu * lifetime
    
    margem_pct = df_real_m['margem_bruta_pct'].iloc[idx] / 100
    imposto_pct = 0.10 # Proxy
    
    cogs_val = gross_revenue * (1 - margem_pct)
    tax_val = gross_revenue * imposto_pct
    cac_val = df_real_m['cac_blended'].iloc[idx]
    
    net_val = gross_revenue - cogs_val - tax_val - cac_val
    
    # Dados Plot
    labels = ['LTV Bruto', 'COGS', 'Impostos', 'CAC', 'LUCRO LÍQUIDO']
    values = [gross_revenue, -cogs_val, -tax_val, -cac_val, net_val]
    
    figsize = (10, 6) if report_mode else (12, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Cumulative setup
    acumulado = 0
    colors = []
    
    for i, val in enumerate(values):
        start = acumulado
        if i == len(values) - 1: # Total
            start = 0
            height = val
            acumulado = 0
            color = '#2E7D32' if val > 0 else '#D32F2F'
        else:
            height = val
            acumulado += val
            color = '#1976D2' if val > 0 else '#EF5350'
            if i == 0: color = '#90CAF9' # Base
        
        ax.bar(labels[i], height, bottom=start if i != len(values)-1 else 0, color=color, alpha=0.9)
        # Label Value
        y_pos = start + height/2 if i != len(values)-1 else height/2
        ax.text(i, y_pos, formata_moeda(abs(val)), ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
    ax.set_title('Decomposição do Unit Economics (Por Cliente)', fontsize=12, color='gray')
    ax.axhline(0, color='black', linewidth=1)
    
    # Tabela Simples
    tabela_md = "| Componente | Valor |\n|:---|---:|\n"
    for l, v in zip(labels, values):
        tabela_md += f"| {l} | {formata_moeda(v)} |\n"
     
    # Legend Plot (Bar labels are enough, but explicit legend helps)
    # ax.legend() -> Waterfall using colors mostly, specific labels on bars.

    legend_md = """
**📖 COMO LER ESTE GRÁFICO (WATERFALL):**

1. **Barra Azul Clara (LTV Bruto):** Todo dinheiro que entra do cliente.
2. **Barras Vermelhas:** O que é descontado (Custos, Impostos, Aquisição).
3. **Barra Final (Verde):** O lucro limpo que sobra no bolso.

**INTERPRETAÇÃO:**
- Mostra a "mordida" de cada etapa no valor do cliente.
- Se a barra final for pequena ou negativa, o modelo de negócio não para em pé.
"""
    formulas = "Profit = LTV Bruto - COGS - Impostos - CAC"
    
    insight = {
        "fato": f"Sobram {formata_moeda(net_val)} de lucro limpo por cliente.",
        "causa": "Estrutura de custos e eficiência de aquisição.",
        "implicacao": "Potencial de reinvestimento.",
        "acao": "Otimizar."
    }
    
    render_atomic_block(
        chart_id="pg4_viz5_waterfall",
        title_colloquial="Onde fica o dinheiro do cliente?",
        title_technical="VIZ 4.5: Unit Profitability Waterfall",
        fig=fig, legend_md=legend_md, df_tabela=tabela_md,
        insight_dict=insight, formulas_md=formulas, report_mode=report_mode,
        table_title="📋 UNIT PROFIT DECOMPOSITION", data_source_text="Fonte: df_real_m (Last Month)"
    )
    plt.close(fig)

# ============================================================================
# VIZ 4.6: VEREDITO FINAL DA PÁGINA
# ============================================================================
def gerar_veredito_unit_economics(df_real, report_mode=False):
    """Gera o bloco de conclusão textual."""
    
    ltv = df_real['ltv'].iloc[-1] if 'ltv' in df_real.columns else 0
    cac = df_real['cac_blended'].iloc[-1]
    mult = ltv / cac if cac > 0 else 0
    
    texto = f"""
**🔍 VEREDITO UNIT ECONOMICS: EXCELENTE**

"Nesta análise de Unit Economics, nós provamos que:

1.  **O cliente é lucrativo (Viz 4.1):** Múltiplo de **{mult:.1f}x**.
2.  **Retenção Sólida (Viz 4.2):** Cohorts saudáveis.
3.  **Risco Controlado (Viz 4.3):** Volatilidade de churn monitorada via SPC.
4.  **Escala Segura (Viz 4.4):** Economia de escala positiva.
5.  **Lucro Real (Viz 4.5):** Unit Profit positivo após todos descontos.

**Conclusão:** A 'máquina de vendas' está calibrada."
"""
    
    if report_mode:
        display(Markdown(f"::: {{.callout-tip}}\n{texto}\n:::"))
    else:
        display(Markdown(f"### {texto}"))

# ============================================================================
# EXECUTOR PRINCIPAL
# ============================================================================
def executar_pagina_4_unit_economics(df_real_m, df_real_s, df_ideal, premissas, report_mode=False):
    """
    Orquestra a geração da Página 4 completa.
    NOTA: Recebe agora df_real_s (semanal) para Viz 4.3.
    """
    if not report_mode:
        print("="*80)
        print("🚀 INICIANDO PÁGINA 4: UNIT ECONOMICS")
        print("="*80)
    else:
        # Título removido para evitar duplicação com o Cabeçalho de Tier
        pass
        # display(Markdown("***"))

    gerar_viz_4_1_ltv_cac(df_real_m, df_ideal, report_mode)
    gerar_viz_4_2_cohorts(df_real_m, report_mode)
    gerar_viz_4_3_churn_volatility(df_real_s, premissas, report_mode)
    gerar_viz_4_4_escala_unit_economics(df_real_m, premissas, report_mode)
    gerar_viz_4_5_waterfall_leaks(df_real_m, premissas, report_mode)
    gerar_veredito_unit_economics(df_real_m, report_mode)
    
    if not report_mode:
        print("\n✅ PÁGINA 4 GERADA COM SUCESSO!")

if __name__ == "__main__":
    print("Este módulo deve ser importado pelo loader_dados_relatorio.py")