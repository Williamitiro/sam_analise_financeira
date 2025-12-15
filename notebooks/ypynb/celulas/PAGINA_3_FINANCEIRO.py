# PÁGINA 3 - FINANCEIRO (V1.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-07
# OBJETIVO: Gerar as 5 visualizações da Página 3 + Veredito Final
#
# ESTRUTURA NARRATIVA (5 ATOS):
# VIZ 3.1: Evolução Financeira Correlacionada (Tese Macro)
# VIZ 3.2: Sankey + Barras Benchmark (Saúde Unitária)
# VIZ 3.3: Fluxo de Caixa Semanal (Tático)
# VIZ 3.4: Alavancagem Operacional (Escala)
# VIZ 3.5: Heatmap DRE Evolutivo (Vazamento)
# VIZ 3.6: Veredito Final (Conclusão)
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from IPython.display import display, Markdown, HTML

# Caminho para utils
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_0_utils import (
        CORES, setup_plot_style, formata_moeda, formata_pct,
        render_atomic_block, salvar_figura_silencioso
    )
except ImportError:
    print("⚠️  celula_0_utils não encontrado. Definindo helpers locais...")
    CORES = {
        'sucesso': '#388E3C', 'alerta': '#FBC02D', 'critico': '#D32F2F',
        'receita': '#2196F3', 'despesa': '#F44336', 'neutro': '#9E9E9E'
    }
    def setup_plot_style(): pass
    def formata_moeda(v): 
        s = f"{float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {s}"
    def formata_pct(v): return f"{v:.1f}%"
    def render_atomic_block(**kwargs): display(Markdown(f"## {kwargs.get('title_colloquial', '')}"))
    def salvar_figura_silencioso(fig, path): fig.savefig(path, dpi=300, bbox_inches='tight')

setup_plot_style()


# ============================================================================
# HELPER: Adicionar fonte dos dados no rodapé do gráfico
# ============================================================================
def adicionar_fonte_dados(ax, fonte="Fonte: Simulação Motor V13 | df_real_m, df_ideal_m"):
    """
    Adiciona texto de fonte no canto inferior direito, abaixo da área de plotagem,
    alinhado com o eixo X.
    
    Args:
        ax: Axes do matplotlib
        fonte: String com a fonte dos dados
    """
    ax.annotate(
        fonte,
        xy=(1.0, -0.12),  # Posição: canto direito, abaixo do eixo X
        xycoords='axes fraction',
        fontsize=8,
        color='gray',
        ha='right',
        va='top',
        style='italic'
    )

# ============================================================================
#     VIZ 3.1: EVOLUÇÃO FINANCEIRA CORRELACIONADA (Dual Y-Axis) + TABELA DRE
# ============================================================================
def gerar_viz_3_1_evolucao_financeira(df_real, df_ideal, report_mode=False):
    """
    Gráfico com duplo eixo Y + Tabela DRE detalhada mostrando lucro real.
    Esta é a primeira visualização que mostra LUCRO - precisa ser detalhada!
    """
    if not report_mode:
        print("\n🔹 VIZ 3.1: Evolução Financeira Correlacionada")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.1: Evolucao Financeira"))
        display(Markdown("**Pergunta:** A empresa caminha para o break-even? Quando o caixa fica positivo?"))
    
    # =========================================
    # TABELA DRE DETALHADA (ANTES DO GRÁFICO!)
    # =========================================
    meses_key = [0, 5, 11, 17, 23, 29, 35]
    meses_key = [m for m in meses_key if m < len(df_real)]
    
    tabela_dre = []
    for m in meses_key:
        row = df_real.iloc[m]
        row_ideal = df_ideal.iloc[m] if m < len(df_ideal) else row
        
        # Calcular delta vs ideal
        delta_ebitda = row['ebitda'] - row_ideal.get('ebitda', row['ebitda'])
        status = '🟢' if row['ebitda'] > 0 else ('🟡' if row['ebitda'] > -1000 else '🔴')
        
        tabela_dre.append({
            'Mês': f'M{m+1}',
            'Receita Bruta': formata_moeda(row['receita_bruta']),
            '(-) Deduções': formata_moeda(row['total_deducoes']),
            'Receita Líquida': formata_moeda(row['receita_liquida']),
            '(-) COGS': formata_moeda(row['total_cogs']),
            'Margem Bruta': formata_moeda(row['margem_bruta']),
            '(-) OPEX': formata_moeda(row['total_opex']),
            'EBITDA': formata_moeda(row['ebitda']),
            'Margem %': f"{row['ebitda_margin']:.1f}%",
            'Status': status
        })
    
    df_tabela_dre = pd.DataFrame(tabela_dre)
    
    if report_mode:
        display(Markdown("### 📊 DRE - Demonstração de Resultado (Marcos Principais)"))
        display(Markdown("*Esta é a primeira tabela que mostra o LUCRO REAL da operação.*"))
        display(Markdown(df_tabela_dre.to_markdown(index=False)))
        display(Markdown(""))
    else:
        display(HTML("<h3>📊 DRE - Demonstração de Resultado (Marcos Principais)</h3>"))
        display(HTML(df_tabela_dre.to_html(index=False, escape=False)))
    
    # =========================================
    # GRÁFICO DUAL Y-AXIS
    # =========================================
    meses = range(1, len(df_real) + 1)
    caixa_real = df_real['caixa'].values
    caixa_ideal = df_ideal['caixa'].values if 'caixa' in df_ideal.columns else caixa_real * 1.2
    ebitda_real = df_real['ebitda'].values
    ebitda_ideal = df_ideal['ebitda'].values if 'ebitda' in df_ideal.columns else ebitda_real * 1.3
    burn_rate = df_real['burn_rate'].values
    
    figsize = (10, 5) if report_mode else (14, 6)
    fig, ax1 = plt.subplots(figsize=figsize, dpi=150)
    ax2 = ax1.twinx()
    
    # Eixo Esquerdo: Caixa
    ax1.plot(meses, caixa_real, color='#1976D2', linewidth=2.5, label='Caixa Real')
    ax1.plot(meses, caixa_ideal, color='#1976D2', linewidth=1.5, linestyle='--', alpha=0.5, label='Caixa Ideal')
    ax1.fill_between(meses, 0, burn_rate, color='#F44336', alpha=0.2, label='Burn Rate')
    ax1.set_xlabel('Mês', fontsize=12)
    ax1.set_ylabel('Caixa / Burn Rate (R$)', fontsize=12, color='#1976D2')
    ax1.tick_params(axis='y', labelcolor='#1976D2')
    ax1.set_ylim(bottom=0)
    
    # Eixo Direito: EBITDA
    ax2.plot(meses, ebitda_real, color='#388E3C', linewidth=2.5, label='EBITDA Real')
    ax2.plot(meses, ebitda_ideal, color='#388E3C', linewidth=1.5, linestyle='--', alpha=0.5, label='EBITDA Ideal')
    ax2.axhline(y=0, color='#D32F2F', linestyle=':', linewidth=1, alpha=0.7)
    ax2.set_ylabel('EBITDA (R$)', fontsize=12, color='#388E3C')
    ax2.tick_params(axis='y', labelcolor='#388E3C')
    
    # BUSCA INTELIGENTE DE BREAK-EVEN (Consistência Financeira)
    # Break-even Operacional = EBITDA > 0 com sustentação
    mes_breakeven_real = None
    for i in range(len(ebitda_real)):
        if ebitda_real[i] > 0:
            # Verifica consistência: precisa ser positivo pelos próximos 3 meses (se existirem)
            futuro = ebitda_real[i:i+3]
            if all(val > 0 for val in futuro):
                mes_breakeven_real = i + 1
                break

    mes_breakeven_ideal = None
    if len(ebitda_ideal) > 0:
        for i in range(len(ebitda_ideal)):
            if ebitda_ideal[i] > 0:
                # Verifica consistência ideal também
                futuro = ebitda_ideal[i:i+3]
                if all(val > 0 for val in futuro):
                    mes_breakeven_ideal = i + 1
                    break
    
    if mes_breakeven_real:
        ax2.axvline(x=mes_breakeven_real, color='#388E3C', linestyle=':', alpha=0.7)
        ax2.annotate(f'Break-even M{mes_breakeven_real}', 
                    xy=(mes_breakeven_real, 0), xytext=(mes_breakeven_real + 2, ebitda_real.max() * 0.3),
                    fontsize=10, color='#388E3C',
                    arrowprops=dict(arrowstyle='->', color='#388E3C', alpha=0.5))
    
    fig.suptitle('💰 EVOLUÇÃO FINANCEIRA CORRELACIONADA', fontsize=14, fontweight='bold', y=1.02)
    ax1.set_title('Caixa & EBITDA: Real vs Ideal (M0-M36)', fontsize=11, color='gray')
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    # Fonte dos dados
    adicionar_fonte_dados(ax1, "Fonte: Celulas 5A/5B | df_real_m['caixa', 'ebitda', 'burn_rate']")
    
    plt.tight_layout()
    salvar_figura_silencioso(fig, 'outputs/figs/pg3_viz1_evolucao_financeira.png')
    
    if report_mode:
        display(fig)
        
        # COMO LER
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

**O QUE ESTOU VENDO?**
Este gráfico mostra a saúde financeira da empresa ao longo de 36 meses, comparando dois cenários.

**ELEMENTOS DO GRÁFICO:**
- **Linha Azul Sólida (Caixa Real):** Quanto dinheiro temos no banco no cenário conservador
- **Linha Azul Tracejada (Caixa Ideal):** Quanto teriamos se atingissemos benchmarks de mercado
- **Area Vermelha (Burn Rate):** Quanto dinheiro "queimamos" por mes para operar - se esta area e grande, estamos gastando muito
- **Linha Verde Solida (EBITDA Real):** Lucro operacional antes de impostos - quando cruza o zero, paramos de dar prejuizo
- **Linha Verde Tracejada (EBITDA Ideal):** Lucro que teriamos no cenario otimista

**COMO INTERPRETAR:**
- Se a linha verde esta ABAIXO de zero = prejuizo operacional (normal no inicio)
- Se a linha verde CRUZA o zero = break-even (empresa se paga)
- Se a linha azul CAI muito = cuidado, caixa acabando
- Se area vermelha DIMINUI = estamos ficando mais eficientes

**TERMOS IMPORTANTES:**
- **EBITDA:** Lucro antes de juros, impostos, depreciacao e amortizacao - mede eficiencia operacional
- **Burn Rate:** Taxa de queima de caixa - quanto gastamos por mes alem do que ganhamos
- **Break-even:** Ponto onde receita = despesas, sem lucro nem prejuizo
"""
        display(Markdown(como_ler))
        display(Markdown("\\newpage"))
    else:
        plt.show()
    
    # Insight Dinâmico
    gap_meses = (mes_breakeven_real - mes_breakeven_ideal) if mes_breakeven_real and mes_breakeven_ideal else 0
    caixa_final = caixa_real[-1]
    caixa_ideal_final = caixa_ideal[-1]
    burn_m1 = burn_rate[0]
    burn_m36 = burn_rate[-1]
    # Lógica Textual de Burn Rate (Correção V1.1)
    if burn_m1 > burn_m36:
        reducao_burn = ((burn_m1 - burn_m36) / max(burn_m1, 1)) * 100
        texto_burn = f"cai de {formata_moeda(burn_m1)} para {formata_moeda(burn_m36)} (-{reducao_burn:.0f}% de redução)"
    else:
        aumento_burn = ((burn_m36 - burn_m1) / max(burn_m1, 1)) * 100
        texto_burn = f"sobe de {formata_moeda(burn_m1)} para {formata_moeda(burn_m36)} (+{aumento_burn:.0f}% de aumento)"
    
    # Ação Dinâmica
    if gap_meses > 0:
        acao_txt = "Acelerar receita para antecipar break-even ou reduzir OPEX em 15%."
    elif caixa_final < 0:
        acao_txt = "Injeção de capital urgente necessária para cobrir burn rate."
    else:
        acao_txt = "Manter estratégia atual e reinvestir excedente em growth."

    insight = {
        "fato": f"Break-even no M{mes_breakeven_real if mes_breakeven_real else 'N/A'} (Real) vs M{mes_breakeven_ideal if mes_breakeven_ideal else 'N/A'} (Ideal). Gap de {abs(gap_meses)} meses.",
        "causa": f"Burn Rate mensal {texto_burn}.",
        "implicacao": f"Caixa final de {formata_moeda(caixa_final)} (Real) vs {formata_moeda(caixa_ideal_final)} (Ideal).",
        "acao": acao_txt
    }
    
    if report_mode:
        insight_md = f"""
::: {{.callout-tip}}
## 💡 INSIGHT: Viabilidade Financeira
- **FATO:** {insight['fato']}
- **CAUSA:** {insight['causa']}
- **IMPLICAÇÃO:** {insight['implicacao']}
- **AÇÃO:** {insight['acao']}
:::
"""
        display(Markdown(insight_md))
        # Auditoria VIZ 3.1
        audit_md = f"""
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.1
**Fonte:** df_real_m (Celula 5A), df_ideal_m (Celula 5B)

**Formulas:**
- Break-even = Primeiro mes onde EBITDA maior que 0
- Gap = Mes break-even Real - Mes break-even Ideal
- Reducao Burn = (Burn M1 - Burn M36) / Burn M1 x 100
:::
"""
        display(Markdown(audit_md))
    else:
        display(HTML(f"""
<div style="background-color: #E8F5E9; border-left: 5px solid #388E3C; padding: 15px; border-radius: 4px; margin: 15px 0;">
    <h4 style="margin-top: 0; color: #388E3C;">💡 INSIGHT: Viabilidade Financeira</h4>
    <ul>
        <li><b>FATO:</b> {insight['fato']}</li>
        <li><b>CAUSA:</b> {insight['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight['implicacao']}</li>
        <li><b>AÇÃO:</b> {insight['acao']}</li>
    </ul>
</div>
"""))
    
    plt.close(fig)
    return {'mes_breakeven_real': mes_breakeven_real, 'caixa_final': caixa_final, 'insight': insight}


# ============================================================================
#     VIZ 3.2: ESTRUTURA DE CUSTOS + DECOMPOSIÇÃO DETALHADA
# ============================================================================
def gerar_viz_3_2_estrutura_custos(df_real, df_ideal, premissas, report_mode=False):
    """
    Visualização completa da estrutura de custos:
    1. Tabela de decomposição ANTES do gráfico
    2. Waterfall DRE
    3. Tabela de breakdown detalhado
    4. Gráfico de composição de custos (pizza/barras)
    """
    if not report_mode:
        print("\n🔹 VIZ 3.2: Estrutura de Custos + Decomposição")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.2: Estrutura de Custos"))
        display(Markdown("**Pergunta:** Onde esta o dinheiro? A estrutura de custos e saudavel?"))
    
    m36 = df_real.iloc[-1]
    
    # Extrair valores do motor
    receita_bruta = m36['receita_bruta']
    receita_liquida = m36['receita_liquida']
    total_deducoes = m36.get('total_deducoes', receita_bruta - receita_liquida)
    total_cogs = m36['total_cogs']
    total_opex = m36['total_opex']
    ebitda = m36['ebitda']
    margem_bruta = m36['margem_bruta']
    margem_bruta_pct = m36['margem_bruta_pct']
    ebitda_pct = m36['ebitda_margin']
    
    # =========================================
    # BREAKDOWN DETALHADO DE CUSTOS
    # =========================================
    
    # COGS Breakdown
    custo_ia_total = m36.get('custo_ia_total', 0)
    custo_ia_lite = m36.get('custo_ia_lite', 0)
    custo_ia_trader = m36.get('custo_ia_trader', 0)
    custo_ia_pro = m36.get('custo_ia_pro', 0)
    comissao_afiliados = m36.get('comissao_afiliados', 0)
    custo_suporte = m36.get('custo_suporte_variavel', 0)
    
    # OPEX Breakdown - Marketing
    gasto_marketing = m36.get('gasto_marketing', 0)
    gasto_instagram = m36.get('gasto_instagram', 0)
    gasto_facebook = m36.get('gasto_facebook', 0)
    gasto_youtube = m36.get('gasto_youtube', 0)
    gasto_google = m36.get('gasto_google', 0)
    
    # OPEX Breakdown - Operacional
    custo_pessoal = m36.get('custo_pessoal', 0)
    custo_infra = m36.get('custo_infra_fixo', 0)
    custo_escritorio = m36.get('custo_escritorio', 0)
    custo_contabilidade = m36.get('custo_contabilidade', 0)
    despesas_viagens = m36.get('despesas_viagens', 0)
    despesas_freelancer = m36.get('despesas_freelancer', 0)
    
    # Benchmarks SaaS
    BENCH_MARGEM_BRUTA = 80.0
    BENCH_OPEX_PCT = 50.0
    BENCH_EBITDA = 20.0
    
    # Cálculos de %
    cogs_pct = (total_cogs / receita_bruta) * 100 if receita_bruta > 0 else 0
    opex_pct = (total_opex / receita_bruta) * 100 if receita_bruta > 0 else 0
    
    # =========================================
    # TABELA 1: DECOMPOSIÇÃO GERAL (ANTES DO GRÁFICO)
    # =========================================
    tabela_geral = [
        {'Categoria': '📈 Receita Bruta', 'Valor': formata_moeda(receita_bruta), '% Receita': '100%', 'Status': '—'},
        {'Categoria': '  (-) Impostos & Taxas', 'Valor': formata_moeda(total_deducoes), '% Receita': f'{(total_deducoes/receita_bruta*100):.1f}%', 'Status': '—'},
        {'Categoria': '= Receita Líquida', 'Valor': formata_moeda(receita_liquida), '% Receita': f'{(receita_liquida/receita_bruta*100):.1f}%', 'Status': '—'},
        {'Categoria': '  (-) COGS Total', 'Valor': formata_moeda(total_cogs), '% Receita': f'{cogs_pct:.1f}%', 'Status': '🟢' if cogs_pct < 20 else '🟡'},
        {'Categoria': '= Margem Bruta', 'Valor': formata_moeda(margem_bruta), '% Receita': f'{margem_bruta_pct:.1f}%', 'Status': '🟢' if margem_bruta_pct > 80 else '🟡'},
        {'Categoria': '  (-) OPEX Total', 'Valor': formata_moeda(total_opex), '% Receita': f'{opex_pct:.1f}%', 'Status': '🟢' if opex_pct < 50 else '🟡'},
        {'Categoria': '= EBITDA', 'Valor': formata_moeda(ebitda), '% Receita': f'{ebitda_pct:.1f}%', 'Status': '🟢' if ebitda > 0 else '🔴'},
    ]
    df_tabela_geral = pd.DataFrame(tabela_geral)
    
    # =========================================
    # RENDERIZAÇÃO ATÔMICA (V7.0)
    # =========================================
    render_atomic_block(
        chart_id="pg3_viz1_dre_breakdown",
        title_colloquial="De onde vem e para onde vai o dinheiro?",
        title_technical="VIZ 3.0: Decomposição da DRE (M36)",
        fig=None,
        legend_md=None,
        table_title="📊 DADOS TABULADOS:",
        df_tabela=df_tabela_geral,
        insight_dict={
            "fato": "Estrutura de custos analisada.", 
            "causa": "Breakdown de M36.", 
            "implicacao": "Entendimento da eficiência.", 
            "acao": "Otimizar linha a linha."
        },
        report_mode=report_mode
    )
    
    # =========================================
    # GRÁFICO 1: WATERFALL DRE
    # =========================================
    figsize = (10, 5) if report_mode else (14, 6)
    fig, ax1 = plt.subplots(figsize=figsize, dpi=150)
    
    categorias = ['Receita\nBruta', 'Impostos\n& Taxas', 'COGS', 'OPEX', 'EBITDA']
    valores = [receita_bruta, -total_deducoes, -total_cogs, -total_opex, ebitda]
    cores = ['#2196F3', '#FF9800', '#E53935', '#E53935', '#4CAF50' if ebitda > 0 else '#E53935']
    
    bottoms = [0, receita_bruta, receita_liquida, margem_bruta, 0]
    
    for i, (cat, h, c, b) in enumerate(zip(categorias, valores, cores, bottoms)):
        if i == len(categorias) - 1:
            ax1.bar(cat, h, color=c, edgecolor='black', linewidth=0.5)
        else:
            ax1.bar(cat, h, bottom=b, color=c, edgecolor='black', linewidth=0.5)
        
        val_display = formata_moeda(abs(h))
        if h >= 0:
            ax1.text(i, b + h + 500, val_display, ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax1.text(i, b + h - 500, f"-{val_display}", ha='center', va='top', fontsize=9)
    
    ax1.set_title('DRE Cascata (M36)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('R$', fontsize=11)
    ax1.axhline(y=0, color='black', linewidth=0.5)
    
    # Fonte dos dados
    adicionar_fonte_dados(ax1, "Fonte: Celulas 5A/5B | df_real_m['receita_bruta', 'total_cogs', 'total_opex', 'ebitda']")
    
    fig.suptitle('📊 WATERFALL DRE - RECEITA ATÉ EBITDA', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    salvar_figura_silencioso(fig, 'outputs/figs/pg3_viz2_waterfall.png')
    
    if report_mode:
        display(fig)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Barra Azul:** Receita bruta (ponto de partida)
2. **Barras Laranja/Vermelha:** Deduções que reduzem a receita
3. **Barra Final Verde/Vermelha:** EBITDA positivo (lucro) ou negativo (prejuízo)
4. **Regra de Sucesso:** Barra final deve ser verde e representar >20% da receita
"""
        display(Markdown(como_ler))
    else:
        plt.show()
    plt.close(fig)
    
    # =========================================
    # TABELA 2: BREAKDOWN DETALHADO DE CUSTOS
    # =========================================
    tabela_breakdown = []
    
    # COGS
    tabela_breakdown.append({'Categoria': '🔧 COGS (Custo Direto)', 'Subcategoria': 'TOTAL', 'Valor': formata_moeda(total_cogs), '% Receita': f'{cogs_pct:.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  IA - Lite', 'Valor': formata_moeda(custo_ia_lite), '% Receita': f'{(custo_ia_lite/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  IA - Trader', 'Valor': formata_moeda(custo_ia_trader), '% Receita': f'{(custo_ia_trader/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  IA - Pro', 'Valor': formata_moeda(custo_ia_pro), '% Receita': f'{(custo_ia_pro/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  Afiliados', 'Valor': formata_moeda(comissao_afiliados), '% Receita': f'{(comissao_afiliados/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  Suporte', 'Valor': formata_moeda(custo_suporte), '% Receita': f'{(custo_suporte/receita_bruta*100):.1f}%'})
    
    # OPEX - Marketing (Correção de Display: Converte explícito para float)
    gasto_mkt_val = float(gasto_marketing) if gasto_marketing is not None else 0.0
    val_mkt_str = formata_moeda(gasto_mkt_val)
    
    tabela_breakdown.append({'Categoria': '📢 Marketing', 'Subcategoria': 'TOTAL', 'Valor': val_mkt_str, '% Receita': f'{(gasto_mkt_val/receita_bruta*100):.1f}%'})
    
    # Canais (mesma lógica)
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  Instagram', 'Valor': formata_moeda(float(gasto_instagram or 0)), '% Receita': f'{(float(gasto_instagram or 0)/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  Facebook', 'Valor': formata_moeda(float(gasto_facebook or 0)), '% Receita': f'{(float(gasto_facebook or 0)/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  YouTube', 'Valor': formata_moeda(float(gasto_youtube or 0)), '% Receita': f'{(float(gasto_youtube or 0)/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': '  Google', 'Valor': formata_moeda(float(gasto_google or 0)), '% Receita': f'{(float(gasto_google or 0)/receita_bruta*100):.1f}%'})
    
    # OPEX - Operacional
    tabela_breakdown.append({'Categoria': '🏢 Operacional', 'Subcategoria': 'Pessoal (RH)', 'Valor': formata_moeda(custo_pessoal), '% Receita': f'{(custo_pessoal/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': 'Infraestrutura', 'Valor': formata_moeda(custo_infra), '% Receita': f'{(custo_infra/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': 'Escritório', 'Valor': formata_moeda(custo_escritorio), '% Receita': f'{(custo_escritorio/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': 'Contabilidade', 'Valor': formata_moeda(custo_contabilidade), '% Receita': f'{(custo_contabilidade/receita_bruta*100):.1f}%'})
    tabela_breakdown.append({'Categoria': '', 'Subcategoria': 'Viagens', 'Valor': formata_moeda(despesas_viagens), '% Receita': f'{(despesas_viagens/receita_bruta*100):.1f}%'})
    
    df_breakdown = pd.DataFrame(tabela_breakdown)
    
    if report_mode:
        display(Markdown("### 💰 BREAKDOWN DETALHADO DE CUSTOS (M36)"))
        display(Markdown("*Decomposição completa de COGS e OPEX por canal/categoria.*"))
        display(Markdown(df_breakdown.to_markdown(index=False)))
        display(Markdown(""))
    else:
        display(HTML("<h3>💰 BREAKDOWN DETALHADO DE CUSTOS (M36)</h3>"))
        display(HTML(df_breakdown.to_html(index=False, escape=False)))
    
    # =========================================
    # GRÁFICO 2: COMPOSIÇÃO DE CUSTOS (PIE + BARRAS)
    # =========================================
    # PADRONIZAÇÃO: Tamanho e Margens (Match Página 1)
    figsize = (10, 6) if report_mode else (14, 8)
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=figsize, dpi=150)
    
    # Ajuste explícito de margens (GOLD STANDARD PÁGINA 1)
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.10, right=0.95)
    
    # Pie: Composição OPEX
    opex_labels = ['Marketing', 'Pessoal', 'Infra', 'Outros']
    outros_opex = total_opex - gasto_marketing - custo_pessoal - custo_infra
    opex_sizes = [gasto_marketing, custo_pessoal, custo_infra, max(outros_opex, 0)]
    opex_colors = ['#2196F3', '#4CAF50', '#FF9800', '#9E9E9E']
    
    ax2a.pie(opex_sizes, labels=opex_labels, autopct='%1.1f%%', colors=opex_colors, startangle=90)
    ax2a.set_title('Composição OPEX', fontsize=12, fontweight='bold')
    
    # Barras: Real vs Benchmark
    metricas = ['Margem Bruta', 'OPEX %', 'EBITDA %']
    real_vals = [margem_bruta_pct, opex_pct, ebitda_pct]
    bench_vals = [BENCH_MARGEM_BRUTA, BENCH_OPEX_PCT, BENCH_EBITDA]
    
    x = np.arange(len(metricas))
    width = 0.35
    
    bars1 = ax2b.bar(x - width/2, real_vals, width, label='Real', color='#1976D2')
    bars2 = ax2b.bar(x + width/2, bench_vals, width, label='Benchmark SaaS', color='#9E9E9E', alpha=0.6)
    
    # GRID E LIMITES
    ax2b.grid(True, alpha=0.4, linestyle='-', axis='y')
    ax2b.set_ylim(0, 100) # Mantém foco no 0-100%
    
    # Lógica Inteligente de Rótulos (Evita estouro de canvas em outliers POSITIVOS e NEGATIVOS)
    for bar, val in zip(bars1, real_vals):
        # Definição segura de pos_y para não estourar o bbox
        if val > 100:
            # Caso > 100%: Trava no topo
            pos_y = 92 
            text_str = f'{val:.0f}% (!)'
            font_color = '#D32F2F' # Vermelho
            fw = 'heavy'
        elif val < 0:
            # Caso NEGATIVO (ex: -500%): Trava no fundo (dentro da área visível)
            pos_y = 5 
            text_str = f'{val:.0f}% (!)'
            font_color = '#D32F2F' # Vermelho
            fw = 'heavy'
        else:
            # Caso Normal (0 a 100)
            pos_y = val + 2
            text_str = f'{val:.1f}%'
            font_color = 'black'
            fw = 'bold'
            
        ax2b.text(bar.get_x() + bar.get_width()/2, pos_y, text_str, 
                 ha='center', fontsize=9, fontweight=fw, color=font_color,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5))
    
    ax2b.set_xticks(x)
    ax2b.set_xticklabels(metricas, fontsize=10)
    ax2b.set_ylabel('%', fontsize=11)
    ax2b.set_title('Real vs Benchmark SaaS', fontsize=12, fontweight='bold')
    ax2b.legend(loc='upper right', fontsize=9)
    
    # Fonte dos dados
    adicionar_fonte_dados(ax2b, "Fonte: Celulas 5A/5B | Breakdown COGS/OPEX/Marketing")
    
    fig2.suptitle('📊 COMPOSIÇÃO DE CUSTOS & BENCHMARK', fontsize=14, fontweight='bold', y=0.98)
    # plt.tight_layout() REMOVIDO PARA MARGENS CONTROLADAS
    salvar_figura_silencioso(fig2, 'outputs/figs/pg3_viz2_composicao_custos.png')
    
    if report_mode:
        display(fig2)
        display(Markdown("\\newpage"))
    else:
        plt.show()
    plt.close(fig2)
    
    # =========================================
    # INSIGHT DINÂMICO
    # =========================================
    maior_custo = max([
        ('Marketing', gasto_marketing),
        ('Pessoal', custo_pessoal),
        ('IA', custo_ia_total),
        ('Infra', custo_infra)
    ], key=lambda x: x[1])
    
    rh_pct = (custo_pessoal / receita_bruta) * 100 if receita_bruta > 0 else 0
    margem_ebitda = ebitda / receita_bruta if receita_bruta > 0 else 0
    
    insight = {
        "fato": f"Margem Bruta de {margem_bruta_pct:.1f}% ({'+' if margem_bruta_pct > BENCH_MARGEM_BRUTA else ''}{margem_bruta_pct - BENCH_MARGEM_BRUTA:.1f}pp vs benchmark).",
        "causa": f"Maior custo: {maior_custo[0]} ({formata_moeda(maior_custo[1])}, {(maior_custo[1]/receita_bruta*100):.1f}% da receita).",
        "implicacao": f"Para cada R$ 1 faturado, R$ {margem_ebitda:.2f} vira lucro operacional.",
        "acao": f"Monitorar RH ({rh_pct:.1f}%) e Marketing ({(gasto_marketing/receita_bruta*100):.1f}%) como % da receita."
    }
    
    if report_mode:
        insight_md = f"""
::: {{.callout-tip}}
## 💡 INSIGHT: Estrutura de Custos
- **FATO:** {insight['fato']}
- **CAUSA:** {insight['causa']}
- **IMPLICAÇÃO:** {insight['implicacao']}
- **AÇÃO:** {insight['acao']}
:::
"""
        display(Markdown(insight_md))
        # Auditoria VIZ 3.2
        audit_md = f"""
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.2
**Fonte:** df_real_m.iloc[-1] (M36 da Celula 5A)

**Formulas:**
- Margem Bruta = (Receita Liquida - COGS) / Receita Bruta x 100
- OPEX pct = Total OPEX / Receita Bruta x 100
- Benchmarks: Margem maior 80%, OPEX menor 50%, EBITDA maior 20%
:::
"""
        display(Markdown(audit_md))
    else:
        display(HTML(f"""
<div style="background-color: #E8F5E9; border-left: 5px solid #388E3C; padding: 15px; border-radius: 4px; margin: 15px 0;">
    <h4 style="margin-top: 0; color: #388E3C;">💡 INSIGHT: Estrutura de Custos</h4>
    <ul>
        <li><b>FATO:</b> {insight['fato']}</li>
        <li><b>CAUSA:</b> {insight['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight['implicacao']}</li>
        <li><b>AÇÃO:</b> {insight['acao']}</li>
    </ul>
</div>
"""))
    
    return {'margem_bruta_pct': margem_bruta_pct, 'ebitda_pct': ebitda_pct, 'insight': insight}


# ============================================================================
#     VIZ 3.3: FLUXO DE CAIXA SEMANAL (Dual Y-Axis + Tabela)
# ============================================================================
def gerar_viz_3_3_fluxo_caixa_semanal(df_real_s, report_mode=False):
    """
    Gráfico semanal (0-24 semanas) mostrando:
    - Eixo Esquerdo: Caixa + Entradas/Saídas
    - Eixo Direito: Runway em semanas
    
    Identifica o vale de caixa (momento crítico).
    """
    if not report_mode:
        print("\n🔹 VIZ 3.3: Fluxo de Caixa Semanal")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.3: Fluxo de Caixa Semanal"))
        display(Markdown("**Pergunta:** O caixa sobrevive ao ramp-up? Qual o momento mais critico?"))
    
    # Se não tiver dados semanais, simular a partir do mensal
    if 'semana' not in df_real_s.columns:
        # Criar dados sintéticos semanais (aproximação)
        semanas = range(1, 25)  # 24 semanas = 6 meses
        n = len(semanas)
        
        # Usar primeiros 6 meses do mensal e interpolar
        caixa_m6 = df_real_s.iloc[:6]['caixa'].values if len(df_real_s) >= 6 else df_real_s['caixa'].values
        
        # Interpolar para semanal
        from scipy import interpolate
        f = interpolate.interp1d(np.linspace(1, 24, len(caixa_m6)), caixa_m6, kind='linear', fill_value='extrapolate')
        caixa = f(list(semanas))
        
        # Estimar entradas e saídas
        receita_m6 = df_real_s.iloc[:6]['receita_bruta'].values if len(df_real_s) >= 6 else df_real_s['receita_bruta'].values
        entradas = np.interp(list(semanas), np.linspace(1, 24, len(receita_m6)), receita_m6) / 4  # Semanal
        
        despesas_m6 = (df_real_s.iloc[:6]['total_cogs'].values + df_real_s.iloc[:6]['total_opex'].values) if len(df_real_s) >= 6 else df_real_s['total_cogs'].values + df_real_s['total_opex'].values
        saidas = np.interp(list(semanas), np.linspace(1, 24, len(despesas_m6)), despesas_m6) / 4
    else:
        semanas = df_real_s['semana'].values[:24]
        caixa = df_real_s['caixa'].values[:24]
        entradas = df_real_s.get('entradas', df_real_s['receita_bruta'] / 4).values[:24]
        saidas = df_real_s.get('saidas', (df_real_s['total_cogs'] + df_real_s['total_opex']) / 4).values[:24]
    
    # Runway em semanas
    runway_semanas = caixa / np.maximum(saidas, 1)
    
    # Encontrar vale de caixa
    idx_min = np.argmin(caixa)
    semana_crise = semanas[idx_min] if hasattr(semanas, '__getitem__') else idx_min + 1
    caixa_min = caixa[idx_min]
    runway_min = runway_semanas[idx_min]
    
    # Figura
    figsize = (10, 5) if report_mode else (14, 6)
    fig, ax1 = plt.subplots(figsize=figsize, dpi=150)
    ax2 = ax1.twinx()
    
    # Eixo Esquerdo: Caixa + Barras
    ax1.plot(semanas, caixa, color='#1976D2', linewidth=2.5, label='Saldo Caixa', zorder=3)
    ax1.fill_between(semanas, 0, caixa, alpha=0.2, color='#1976D2')
    
    # Limite crítico
    limite_critico = np.mean(saidas) * 2  # 2 semanas de despesas
    ax1.axhline(y=limite_critico, color='#D32F2F', linestyle='--', linewidth=1.5, label='Limite Crítico')
    
    # Marcar vale
    ax1.scatter([semana_crise], [caixa_min], color='#D32F2F', s=100, zorder=5)
    ax1.annotate(f'Vale: S{semana_crise}\n{formata_moeda(caixa_min)}', 
                 xy=(semana_crise, caixa_min), xytext=(semana_crise + 2, caixa_min + np.max(caixa) * 0.15),
                 fontsize=10, color='#D32F2F',
                 arrowprops=dict(arrowstyle='->', color='#D32F2F'))
    
    ax1.set_xlabel('Semana', fontsize=12)
    ax1.set_ylabel('Caixa (R$)', fontsize=12, color='#1976D2')
    ax1.tick_params(axis='y', labelcolor='#1976D2')
    
    # Eixo Direito: Runway
    ax2.plot(semanas, runway_semanas, color='#388E3C', linewidth=2, linestyle=':', label='Runway (sem)')
    ax2.set_ylabel('Runway (semanas)', fontsize=12, color='#388E3C')
    ax2.tick_params(axis='y', labelcolor='#388E3C')
    ax2.axhline(y=4, color='#FBC02D', linestyle=':', alpha=0.5)  # Meta mínima
    
    # Título
    fig.suptitle('💸 FLUXO DE CAIXA SEMANAL (0-24 Semanas)', fontsize=14, fontweight='bold', y=1.02)
    ax1.set_title('Caixa & Runway: Identificando Crises de Liquidez', fontsize=11, color='gray')
    
    # Legenda
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)
    
    # Fonte dos dados
    adicionar_fonte_dados(ax1, "Fonte: Celulas 5A/5B | df_real_m['caixa'] interpolado para semanal")
    
    plt.tight_layout()
    salvar_figura_silencioso(fig, 'outputs/figs/pg3_viz3_fluxo_caixa_semanal.png')
    
    if report_mode:
        display(fig)
        
        # COMO LER (Legenda obrigatória)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Linha Azul (Eixo Esquerdo):** Saldo de caixa semanal
2. **Linha Vermelha Tracejada:** Limite crítico (2 semanas de despesas)
3. **Linha Verde Pontilhada (Eixo Direito):** Runway em semanas
4. **Ponto Vermelho:** Vale de caixa (momento mais crítico)
5. **Linha Amarela Horizontal:** Meta mínima de 4 semanas de runway
6. **Regra de Sucesso:** Manter caixa sempre acima da linha vermelha
"""
        display(Markdown(como_ler))
    else:
        plt.show()
    
    # Tabela Semanal
    tabela_semanas = [4, 8, 12, 16, 20, 24]
    tabela_dados = []
    for s in tabela_semanas:
        idx = s - 1 if s <= len(caixa) else len(caixa) - 1
        status = '🔴 CRÍTICO' if caixa[idx] < limite_critico else ('🟡 ATENÇÃO' if runway_semanas[idx] < 4 else '🟢 OK')
        tabela_dados.append({
            'Semana': f'S{s}',
            'Caixa': formata_moeda(caixa[idx]),
            'Entradas': formata_moeda(entradas[idx]),
            'Saídas': formata_moeda(saidas[idx]),
            'Runway': f'{runway_semanas[idx]:.1f} sem',
            'Status': status
        })
    
    df_tabela = pd.DataFrame(tabela_dados)
    
    if report_mode:
        display(Markdown(df_tabela.to_markdown(index=False)))
        display(Markdown("*Fonte: Celulas 5A/5B | df_real_m interpolado para granularidade semanal*"))
        # COMO LER VIZ 3.3
        como_ler_33 = """
**📖 COMO LER ESTE GRÁFICO (FLUXO DE CAIXA SEMANAL):**

**O QUE ESTOU VENDO?**
Este grafico mostra a saude do caixa SEMANA A SEMANA nos primeiros 6 meses - periodo mais critico para startups.

**ELEMENTOS:**
- **Linha Azul (Saldo Caixa):** Quanto dinheiro temos no banco a cada semana
- **Linha Vermelha Tracejada (Limite Critico):** Se caixa cair abaixo disso, temos menos de 2 semanas de sobrevivencia
- **Ponto Vermelho (Vale):** Semana mais perigosa - caixa no nivel mais baixo
- **Linha Laranja (Runway):** Quantas semanas conseguimos sobreviver com o caixa atual

**COMO INTERPRETAR:**
- **Caixa NUNCA deve tocar a linha vermelha** - se tocar, risco de insolvencia
- **Vale muito profundo** = precisamos de capital extra ou renegociar prazos
- **Runway abaixo de 4 semanas** = ALERTA MAXIMO

**TERMOS IMPORTANTES:**
- **Runway:** "Pista de pouso" - quantas semanas/meses a empresa sobrevive sem receita nova
- **Vale de Caixa:** Momento de menor liquidez, geralmente nos primeiros meses
- **Limite Critico:** Reserva minima para emergencias (2 semanas de despesas)
"""
        display(Markdown(como_ler_33))
        display(Markdown(""))  # Espaço para desconectar insight da tabela
        display(Markdown("\\newpage"))
    else:
        display(HTML(df_tabela.to_html(index=False, escape=False)))
        display(HTML("<br/>"))  # Espaço para desconectar insight da tabela
    
    # Insight Dinâmico
    reserva_seguranca = np.mean(saidas) * 4  # 4 semanas
    
    # Lógica Dinâmica VIZ 3.3
    if caixa_min < limite_critico:
        causa_txt = "Descompasso entre CAC pago adiantado e MRR recorrente no ramp-up."
        acao_txt = "Manter sempre 4 semanas de runway. Renegociar prazos com fornecedores."
        implicacao_txt = f"Precisamos de reserva mínima de {formata_moeda(reserva_seguranca)} para absorver vales."
    else:
        causa_txt = "Gestão de caixa eficiente absorvendo o custo de aquisição inicial."
        acao_txt = "Monitorar runway para aprovar novos investimentos em marketing."
        implicacao_txt = "Liquidez saudável suporta o crescimento planejado."

    insight = {
        "fato": f"Vale de caixa na semana {semana_crise} com {formata_moeda(caixa_min)} (runway de {runway_min:.1f} semanas).",
        "causa": causa_txt,
        "implicacao": implicacao_txt,
        "acao": acao_txt
    }
    
    if report_mode:
        insight_md = f"""
::: {{.callout-warning}}
## 💡 INSIGHT: Liquidez no Ramp-up
- **FATO:** {insight['fato']}
- **CAUSA:** {insight['causa']}
- **IMPLICAÇÃO:** {insight['implicacao']}
- **AÇÃO:** {insight['acao']}
:::
"""
        display(Markdown(insight_md))
        # Auditoria VIZ 3.3
        audit_md = f"""
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.3
**Fonte:** df_real_s (granularidade semanal, Celula 5A)

**Formulas:**
- Runway = Caixa / Despesas Semanais
- Vale de Caixa = min(Caixa) nas 24 semanas
- Reserva = Media Saidas x 4 semanas
:::
"""
        display(Markdown(audit_md))
    else:
        display(HTML(f"""
<div style="background-color: #FFFDE7; border-left: 5px solid #FBC02D; padding: 15px; border-radius: 4px; margin: 15px 0;">
    <h4 style="margin-top: 0; color: #F57F17;">💡 INSIGHT: Liquidez no Ramp-up</h4>
    <ul>
        <li><b>FATO:</b> {insight['fato']}</li>
        <li><b>CAUSA:</b> {insight['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight['implicacao']}</li>
        <li><b>AÇÃO:</b> {insight['acao']}</li>
    </ul>
</div>
"""))
    
    plt.close(fig)
    return {'semana_crise': semana_crise, 'caixa_min': caixa_min, 'insight': insight}


# ============================================================================
#     VIZ 3.4: ALAVANCAGEM OPERACIONAL (Scatter + Correlação)
# ============================================================================
def gerar_viz_3_4_alavancagem_operacional(df_real, df_ideal, report_mode=False):
    """
    Scatter plot mostrando a relação Receita vs Margem EBITDA.
    Demonstra que o modelo é alavancado (lucro cresce mais que receita).
    """
    if not report_mode:
        print("\n🔹 VIZ 3.4: Alavancagem Operacional")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.4: Alavancagem Operacional"))
        display(Markdown("**Pergunta:** A empresa escala de forma eficiente?"))
    
    # Dados
    receita = df_real['receita_bruta'].values
    ebitda_pct = df_real['ebitda_margin'].values
    meses = range(1, len(df_real) + 1)
    
    receita_ideal = df_ideal['receita_bruta'].values if 'receita_bruta' in df_ideal.columns else receita * 1.2
    ebitda_pct_ideal = df_ideal['ebitda_margin'].values if 'ebitda_margin' in df_ideal.columns else ebitda_pct + 5
    
    # Calcular alavancagem (M12 vs M36)
    if len(df_real) >= 36:
        receita_m12 = df_real.iloc[11]['receita_bruta']
        receita_m36 = df_real.iloc[35]['receita_bruta']
        ebitda_m12 = df_real.iloc[11]['ebitda']
        ebitda_m36 = df_real.iloc[35]['ebitda']
        
        delta_receita = ((receita_m36 - receita_m12) / max(receita_m12, 1)) * 100
        delta_ebitda = ((ebitda_m36 - ebitda_m12) / max(abs(ebitda_m12), 1)) * 100
        alavancagem = delta_ebitda / max(delta_receita, 1) if delta_receita > 0 else 0
    else:
        delta_receita = delta_ebitda = alavancagem = 0
    
    # Figura
    figsize = (10, 5) if report_mode else (12, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Scatter com gradiente de cor por mês
    scatter = ax.scatter(receita, ebitda_pct, c=list(meses), cmap='viridis', s=80, alpha=0.8, edgecolors='black', linewidth=0.5)
    
    # Linha de tendência (regressão polinomial)
    z = np.polyfit(receita, ebitda_pct, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(receita), max(receita), 100)
    ax.plot(x_trend, p(x_trend), color='#1976D2', linewidth=2, linestyle='--', label='Tendência Real')
    
    # Linha Ideal (tracejada) - cor vibrante e traço espesso para visibilidade
    if len(receita_ideal) == len(ebitda_pct_ideal):
        ax.plot(receita_ideal, ebitda_pct_ideal, color='#7B1FA2', linewidth=2.5, linestyle='--', alpha=0.8, label='Trajetória Ideal')
    
    # Zonas de benchmark - linhas mais visíveis
    ax.axhline(y=0, color='#D32F2F', linestyle='-', linewidth=1.5, alpha=0.7)
    ax.axhline(y=20, color='#FF9800', linestyle='--', linewidth=2, alpha=0.8, label='Benchmark 20%')
    ax.axhspan(-100, 0, alpha=0.1, color='#F44336', label='Zona Prejuízo')
    ax.axhspan(0, 20, alpha=0.05, color='#FFC107')
    ax.axhspan(20, 100, alpha=0.1, color='#4CAF50')
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Mês', fontsize=10)
    
    ax.set_xlabel('Receita Bruta (R$)', fontsize=12)
    ax.set_ylabel('Margem EBITDA (%)', fontsize=12)
    ax.set_title(f'Alavancagem Operacional: {alavancagem:.2f}x', fontsize=11, color='gray')
    fig.suptitle('📈 ALAVANCAGEM OPERACIONAL', fontsize=14, fontweight='bold', y=1.02)
    ax.legend(loc='lower right', fontsize=9)
    
    # Fonte dos dados
    adicionar_fonte_dados(ax, "Fonte: Celulas 5A/5B | df_real_m['receita_bruta', 'ebitda_margin']")
    
    plt.tight_layout()
    salvar_figura_silencioso(fig, 'outputs/figs/pg3_viz4_alavancagem.png')
    
    if report_mode:
        display(fig)
        
        # COMO LER (Legenda obrigatória)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO (ALAVANCAGEM OPERACIONAL):**

**O QUE ESTOU VENDO?**
Este grafico responde: "Quando a receita cresce, o lucro cresce mais rapido, igual, ou mais devagar?"

**ELEMENTOS:**
- **Cada Ponto = 1 Mes:** Cor mais escura = mes mais recente. Os pontos devem "subir e ir para direita"
- **Eixo X (Horizontal):** Receita bruta - quanto a empresa fatura
- **Eixo Y (Vertical):** Margem EBITDA em % - quanto sobra de lucro operacional
- **Linha Roxa Tracejada (Ideal):** Trajetoria que atingiriamos com benchmarks de mercado
- **Linha Azul Tracejada:** Tendencia real baseada nos dados
- **Faixa Verde (acima de 20%):** Margem saudavel para reinvestir e crescer
- **Faixa Vermelha (abaixo de 0%):** Prejuizo operacional

**COMO INTERPRETAR:**
- **Pontos subindo rapido** = Modelo escalavel, cada real novo gera mais lucro
- **Pontos subindo devagar** = Custos crescem junto com receita, pouca alavancagem
- **Ideal vs Real:** Se a linha roxa esta acima da azul, estamos abaixo do potencial

**TERMOS IMPORTANTES:**
- **Alavancagem Operacional:** Quanto o lucro cresce para cada 1% de crescimento de receita
  - Ex: Alavancagem 2x = receita dobra, lucro quadruplica
- **Modelo Escalavel:** Custos fixos se diluem com volume, margem melhora automaticamente
- **Margem EBITDA:** Lucro operacional dividido pela receita, em percentual
"""
        display(Markdown(como_ler))
        display(Markdown("\\newpage"))
    else:
        plt.show()
    
    # Custos fixos
    m36 = df_real.iloc[-1]
    custo_pessoal = m36.get('custo_pessoal', 0)
    custo_infra = m36.get('custo_infra_fixo', 0)
    fixos = custo_pessoal + custo_infra
    fixos_pct = (fixos / m36['receita_bruta']) * 100 if m36['receita_bruta'] > 0 else 0
    
    # Insight Dinâmico de Alavancagem (Correção V1.1)
    if alavancagem > 1.2:
        analise_escala = "Modelo altamente escalável: cada R$ adicional de receita gera mais lucro marginal."
        acao_escala = "Priorizar crescimento de receita sobre corte de custos."
    elif alavancagem > 0:
        analise_escala = "Escalabilidade moderada: custos crescem quase na mesma proporção da receita."
        acao_escala = "Revisar estrutura de custos fixos para melhorar alavancagem."
    else:
        analise_escala = "Desalavancagem operacional: custos estão crescendo mais rápido que a receita (ou margens piorando)."
        acao_escala = "ALERTA: Focar urgentemente em eficiência operacional e margem bruta."

    insight = {
        "fato": f"Alavancagem operacional de {alavancagem:.2f}x (Receita +{delta_receita:.0f}% → EBITDA +{delta_ebitda:.0f}%).",
        "causa": f"Custos fixos de {formata_moeda(fixos)} representam {fixos_pct:.1f}% da receita no M36.",
        "implicacao": analise_escala,
        "acao": acao_escala
    }
    
    if report_mode:
        insight_md = f"""
::: {{.callout-tip}}
## 💡 INSIGHT: Escalabilidade do Modelo
- **FATO:** {insight['fato']}
- **CAUSA:** {insight['causa']}
- **IMPLICAÇÃO:** {insight['implicacao']}
- **AÇÃO:** {insight['acao']}
:::
"""
        display(Markdown(insight_md))
        # Auditoria VIZ 3.4
        audit_md = f"""
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.4
**Fonte:** df_real_m, df_ideal_m (Celulas 5A/5B)

**Formulas:**
- Alavancagem = Delta EBITDA / Delta Receita
- Delta = (Valor M36 - Valor M12) / Valor M12 x 100
- Interpretacao: Alavancagem maior que 1 = Modelo escalavel
:::
"""
        display(Markdown(audit_md))
    else:
        display(HTML(f"""
<div style="background-color: #E8F5E9; border-left: 5px solid #388E3C; padding: 15px; border-radius: 4px; margin: 15px 0;">
    <h4 style="margin-top: 0; color: #388E3C;">💡 INSIGHT: Escalabilidade do Modelo</h4>
    <ul>
        <li><b>FATO:</b> {insight['fato']}</li>
        <li><b>CAUSA:</b> {insight['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight['implicacao']}</li>
        <li><b>AÇÃO:</b> {insight['acao']}</li>
    </ul>
</div>
"""))
    
    plt.close(fig)
    return {'alavancagem': alavancagem, 'insight': insight}


# ============================================================================
#     VIZ 3.5: HEATMAP DRE EVOLUTIVO (Real vs Ideal)
# ============================================================================
def gerar_viz_3_5_heatmap_dre(df_real, df_ideal, report_mode=False):
    """
    Heatmap mostrando evolução das métricas DRE ao longo dos meses.
    Cores indicam a saúde (verde = bom, vermelho = ruim).
    """
    if not report_mode:
        print("\n🔹 VIZ 3.5: Heatmap DRE Evolutivo")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.5: Evolucao DRE - Real vs Ideal"))
        display(Markdown("**Pergunta:** Estamos convergindo para o cenario ideal?"))
    
    # Meses chave
    meses_key = [0, 5, 11, 17, 23, 29, 35]  # M1, M6, M12, M18, M24, M30, M36
    meses_key = [m for m in meses_key if m < len(df_real)]
    
    # Métricas a mostrar
    metricas = ['Receita Bruta', 'Margem Bruta %', 'OPEX %', 'EBITDA %']
    
    # Construir matriz
    data_real = []
    data_ideal = []
    data_delta = []
    
    for m in meses_key:
        row_real = df_real.iloc[m]
        row_ideal = df_ideal.iloc[m] if m < len(df_ideal) else row_real
        
        receita_r = row_real['receita_bruta']
        receita_i = row_ideal['receita_bruta'] if 'receita_bruta' in row_ideal else receita_r
        margem_r = row_real['margem_bruta_pct']
        margem_i = row_ideal['margem_bruta_pct'] if 'margem_bruta_pct' in row_ideal else margem_r
        opex_r = (row_real['total_opex'] / max(row_real['receita_bruta'], 1)) * 100
        opex_i = (row_ideal['total_opex'] / max(row_ideal['receita_bruta'], 1)) * 100 if 'total_opex' in row_ideal else opex_r
        ebitda_r = row_real['ebitda_margin']
        ebitda_i = row_ideal['ebitda_margin'] if 'ebitda_margin' in row_ideal else ebitda_r
        
        data_real.append([receita_r, margem_r, opex_r, ebitda_r])
        data_ideal.append([receita_i, margem_i, opex_i, ebitda_i])
        data_delta.append([
            ((receita_r - receita_i) / max(receita_i, 1)) * 100,
            margem_r - margem_i,
            opex_r - opex_i,  # Para OPEX, menor é melhor
            ebitda_r - ebitda_i
        ])
    
    # Figura
    figsize = (10, 5) if report_mode else (14, 6)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=150)
    
    # Heatmap Delta
    delta_array = np.array(data_delta).T
    
    # Normalizar para colormap
    cmap = plt.cm.RdYlGn
    vmax = np.max(np.abs(delta_array))
    
    im = ax1.imshow(delta_array, cmap=cmap, aspect='auto', vmin=-vmax, vmax=vmax)
    
    # Labels
    meses_labels = [f'M{m+1}' for m in meses_key]
    ax1.set_xticks(range(len(meses_labels)))
    ax1.set_xticklabels(meses_labels)
    ax1.set_yticks(range(len(metricas)))
    ax1.set_yticklabels(metricas)
    
    # Adicionar valores
    for i in range(len(metricas)):
        for j in range(len(meses_key)):
            val = delta_array[i, j]
            color = 'white' if abs(val) > vmax * 0.5 else 'black'
            ax1.text(j, i, f'{val:+.1f}%' if i > 0 else f'{val:+.0f}%', 
                    ha='center', va='center', fontsize=9, color=color)
    
    ax1.set_title('Δ Delta Real vs Ideal (%)', fontsize=12, fontweight='bold')
    
    # Colorbar
    cbar = fig.colorbar(im, ax=ax1, shrink=0.8)
    cbar.set_label('Delta %')
    
    # Tabela de valores absolutos
    ax2.axis('off')
    
    # Criar tabela
    cell_text = []
    for m_idx, m in enumerate(meses_key):
        row = df_real.iloc[m]
        cell_text.append([
            f'M{m+1}',
            formata_moeda(row['receita_bruta']),
            f"{row['margem_bruta_pct']:.1f}%",
            f"{(row['total_opex'] / max(row['receita_bruta'], 1)) * 100:.1f}%",
            f"{row['ebitda_margin']:.1f}%"
        ])
    
    table = ax2.table(
        cellText=cell_text,
        colLabels=['Mês', 'Receita', 'Marg. Bruta', 'OPEX %', 'EBITDA %'],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    ax2.set_title('Valores Absolutos (Real)', fontsize=12, fontweight='bold')
    
    # Fonte dos dados
    adicionar_fonte_dados(ax1, "Fonte: Celulas 5A/5B | df_real_m vs df_ideal_m (marcos M1-M36)")
    
    fig.suptitle('📊 EVOLUÇÃO DRE: REAL VS IDEAL', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    salvar_figura_silencioso(fig, 'outputs/figs/pg3_viz5_heatmap_dre.png')
    
    if report_mode:
        display(fig)
        
        # COMO LER (Legenda obrigatória) - explicação detalhada
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

**HEATMAP (ESQUERDA) - O Delta (Δ):**
- Mostra a **diferença percentual** entre Real e Ideal, NÃO os valores absolutos.
- **Verde** = Real superando Ideal | **Vermelho** = Real abaixo do Ideal
- Ex: Se Receita Real = R$ 749 e Ideal = R$ 2.135, Delta = -65% (vermelho)
- **OPEX %:** Vermelho = OPEX maior que benchmark (ruim); Verde = menor (bom)
- **EBITDA %:** Valores negativos no Delta = margem ABAIXO do ideal

**TABELA (DIREITA) - Valores Absolutos:**
- Mostra os valores REAIS da simulação, em R$ ou %.
- EBITDA de -234.8% = prejuízo 2.3x maior que receita naquele mês.
- Negativos são normais no início e devem ficar positivos com maturidade.

**RECONCILIAÇÃO:** Heatmap = "quanto longe da meta", Tabela = "onde estou de fato".
"""
        display(Markdown(como_ler))
        display(Markdown("\\newpage"))
    else:
        plt.show()
    
    # Calcular gaps
    gaps = {
        'receita': data_delta[-1][0],
        'margem_bruta': data_delta[-1][1],
        'ebitda': data_delta[-1][3]
    }
    maior_gap = max(gaps.items(), key=lambda x: abs(x[1]))
    
    # Lógica Dinâmica de Insight (Gap Positivo vs Negativo)
    gap_val = maior_gap[1]
    gap_nome = maior_gap[0]
    
    if gap_val > 0:
        # Real superou Ideal
        causa_txt = f"Performance real de {gap_nome} superando projeções otimistas."
        implicacao_txt = "O modelo mostra tração superior ao benchmark."
        acao_txt = "Revisar metas para cima e aumentar investimento em growth."
    else:
        # Real abaixo do Ideal
        causa_txt = "Gap acumulado por conservadorismo ou fricção na execução."
        implicacao_txt = "Potencial de crescimento não capturado plenamente."
        acao_txt = "Ajustar premissas ou investigar gargalos de conversão."

    insight = {
        "fato": f"Maior desvio no M36: {gap_nome} ({gap_val:+.1f}% vs Ideal).",
        "causa": causa_txt,
        "implicacao": implicacao_txt,
        "acao": acao_txt
    }
    
    if report_mode:
        insight_md = f"""
::: {{.callout-note}}
## 💡 INSIGHT: Convergência ao Ideal
- **FATO:** {insight['fato']}
- **CAUSA:** {insight['causa']}
- **IMPLICAÇÃO:** {insight['implicacao']}
- **AÇÃO:** {insight['acao']}
:::
"""
        display(Markdown(insight_md))
        # Auditoria VIZ 3.5
        audit_md = f"""
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.5
**Fonte:** df_real_m vs df_ideal_m (Celulas 5A e 5B)

**Formulas:**
- Delta = (Real - Ideal) / |Ideal| x 100
- Verde = Real superando Ideal
- Vermelho = Real abaixo do Ideal
:::
"""
        display(Markdown(audit_md))
    else:
        display(HTML(f"""
<div style="background-color: #E3F2FD; border-left: 5px solid #1976D2; padding: 15px; border-radius: 4px; margin: 15px 0;">
    <h4 style="margin-top: 0; color: #1976D2;">💡 INSIGHT: Convergência ao Ideal</h4>
    <ul>
        <li><b>FATO:</b> {insight['fato']}</li>
        <li><b>CAUSA:</b> {insight['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight['implicacao']}</li>
        <li><b>AÇÃO:</b> {insight['acao']}</li>
    </ul>
</div>
"""))
    
    plt.close(fig)
    return {'gaps': gaps, 'insight': insight}


# ============================================================================
#     VIZ 3.6: VEREDITO FINAL
# ============================================================================
def gerar_veredito_financeiro(resultados, report_mode=False):
    """
    Gera o veredito final conectando os 5 atos.
    
    Parâmetros:
        resultados: dict com outputs das 5 visualizações anteriores
    """
    if not report_mode:
        print("\n🔹 VIZ 3.6: Veredito Financeiro")
    
    # Extrair métricas dos resultados
    mes_be = resultados.get('viz1', {}).get('mes_breakeven_real', 'N/A')
    margem_bruta = resultados.get('viz2', {}).get('margem_bruta_pct', 0)
    ebitda_pct = resultados.get('viz2', {}).get('ebitda_pct', 0)
    semana_crise = resultados.get('viz3', {}).get('semana_crise', 'N/A')
    alavancagem = resultados.get('viz4', {}).get('alavancagem', 0)
    gaps = resultados.get('viz5', {}).get('gaps', {})
    
    # Determinar status geral
    if ebitda_pct > 20 and margem_bruta > 80:
        status_geral = "APROVADO"
        cor = "#388E3C"
    elif ebitda_pct > 0:
        status_geral = "APROVADO COM RESSALVAS"
        cor = "#FBC02D"
    else:
        status_geral = "ATENÇÃO REQUERIDA"
        cor = "#D32F2F"
    
    
    
    # Lógica trinitária de escala
    if alavancagem > 1.5:
        escala_str = "altamente escalável"
        escala_status = "POSITIVO"
    elif alavancagem > 0:
        escala_str = "moderada"
        escala_status = "ALERTA"
    else:
        escala_str = "crítica (desalavancagem)"
        escala_status = "NEGATIVO"

    # Construção da NARRATIVA (Diagnóstico -> Prognóstico -> Prescrição)
    
    # Parágrafo 1: Diagnóstico (Passado/Presente)
    if status_geral == "APROVADO":
        diagnostico = f"A operação demonstra solidez financeira com margem bruta de {margem_bruta:.0f}% e EBITDA positivo de {ebitda_pct:.0f}%. A alavancagem é {escala_str}, provando que a receita cresce com eficiência de custos."
    elif status_geral == "APROVADO COM RESSALVAS":
        diagnostico = f"A operação é viável, mas opera com margens abaixo do potencial máximo. Com {margem_bruta:.0f}% de margem bruta e {ebitda_pct:.0f}% de EBITDA, o modelo para em pé, mas deixa dinheiro na mesa devido a ineficiências pontuais ou escala {escala_str}."
    else:
        diagnostico = f"A operação enfrenta desafios estruturais severos. Com margem bruta de {margem_bruta:.0f}% (abaixo do benchmark) e alavancagem {escala_str}, a estrutura de custos atual consome mais recursos do que a receita é capaz de gerar."

    # Parágrafo 2: Prognóstico (Futuro)
    # Validação de tipo segura para semana_crise
    tem_crise_liquidez = isinstance(semana_crise, (int, float)) and semana_crise <= 24
    
    if tem_crise_liquidez:
        prognostico = f"O ponto crítico é a liquidez: o modelo projeta um **vale de caixa na semana {semana_crise}**. Se a queima de caixa atual persistir sem injeção de capital ou aumento de receita, o risco de insolvência no curto prazo é iminente."
    else:
        gap_medio = np.mean(list(gaps.values())) if gaps else 0
        prognostico = f"A liquidez está controlada no curto prazo, permitindo focar na convergência para o cenário ideal (gap médio de {gap_medio:.1f}%). A solvência não é um risco imediato, mas a eficiência sim."

    # Parágrafo 3: Prescrição (Ação Única)
    if tem_crise_liquidez and semana_crise <= 12:
        prescricao = f"Ataque imediato à **Liquidez**. Renegociar prazos com fornecedores e antecipar recebíveis para sobreviver ao vale da semana {semana_crise}."
    elif escala_status == "NEGATIVO":
         prescricao = "A prioridade absoluta é **Estancar a Desalavancagem**. Não escalonar marketing antes de sanear a margem bruta (cortar custos fixos ou aumentar pricing)."
    else:
        prescricao = "Foco total em **Growth e Otimização**. O modelo está validado e solvente; a prioridade agora é melhorar as margens via CAC mais baixo ou LTV mais alto."
    
    veredito = f"""
**🔍 VEREDITO FINANCEIRO: {status_geral}**

**1. DIAGNÓSTICO:** {diagnostico}

**2. PROGNÓSTICO:** {prognostico}

**3. PRESCRIÇÃO:** {prescricao}
"""
    
    if report_mode:
        veredito_md = f"""
::: {{.callout-important}}
{veredito}
:::
"""
        display(Markdown(veredito_md))
    else:
        display(HTML(f"""
<div style="background-color: #f5f5f5; border: 2px solid {cor}; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <h3 style="color: {cor}; margin-top: 0;">🔍 VEREDITO FINANCEIRO</h3>
    <p>{veredito.replace(chr(10), '<br>')}</p>
</div>
"""))
    
    return {'status': status_geral, 'veredito': veredito}


# ============================================================================
# ORQUESTRAÇÃO PRINCIPAL
# ============================================================================
def executar_pagina_3_financeiro(df_real_m, df_real_s, df_ideal_m, premissas, report_mode=False):
    """
    Função principal que coordena a geração de toda a Página 3.
    
    INPUTS:
      - df_real_m: DataFrame mensal Real
      - df_real_s: DataFrame semanal Real (ou mensal se não tiver semanal)
      - df_ideal_m: DataFrame mensal Ideal
      - premissas: Dict de premissas
      - report_mode: Se True, gera saída otimizada para PDF/DOCX
    """
    import os
    os.makedirs('outputs/figs', exist_ok=True)
    
    if not report_mode:
        print("\n" + "=" * 80)
        print("💰 PÁGINA 3: ANÁLISE FINANCEIRA (DRE + FLUXO + MARGENS)")
        print("=" * 80)
    else:
        # Título removido para evitar duplicação com o Cabeçalho do Tier no QMD
        pass
    
    resultados = {}
    
    # VIZ 3.1: Evolução Financeira
    resultados['viz1'] = gerar_viz_3_1_evolucao_financeira(df_real_m, df_ideal_m, report_mode)
    
    # VIZ 3.2: Estrutura de Custos
    resultados['viz2'] = gerar_viz_3_2_estrutura_custos(df_real_m, df_ideal_m, premissas, report_mode)
    
    # VIZ 3.3: Fluxo de Caixa Semanal
    resultados['viz3'] = gerar_viz_3_3_fluxo_caixa_semanal(df_real_s, report_mode)
    
    # VIZ 3.4: Alavancagem Operacional
    resultados['viz4'] = gerar_viz_3_4_alavancagem_operacional(df_real_m, df_ideal_m, report_mode)
    
    # VIZ 3.5: Heatmap DRE
    resultados['viz5'] = gerar_viz_3_5_heatmap_dre(df_real_m, df_ideal_m, report_mode)
    
    # VIZ 3.6: Veredito
    resultados['veredito'] = gerar_veredito_financeiro(resultados, report_mode)
    
    if not report_mode:
        print("\n" + "=" * 80)
        print("✅ PÁGINA 3: ANÁLISE FINANCEIRA - GERAÇÃO COMPLETA!")
        print("=" * 80)
        return resultados
    
    # Em report_mode, não retorna nada para evitar output do dict
    return None


# ============================================================================
# EXECUÇÃO STANDALONE
# ============================================================================
if __name__ == "__main__":
    print("⚠️  Este arquivo é um módulo.")
    print("    Execute via 'loader_dados_relatorio.py' ou importe 'executar_pagina_3_financeiro'.")
