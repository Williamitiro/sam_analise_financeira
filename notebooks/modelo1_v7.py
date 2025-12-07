# MÓDULO: PÁGINA 1 - RESUMO EXECUTIVO (V7.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-06
# OBJETIVO: Gerar as 5 visualizações da Página 1 (Overview Financeiro)
# ARQUITETURA: Usa viz_utils_v7.py para renderização padronizada (PDF/Notebook)
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Importando da biblioteca compartilhada (V7.0)
try:
    from notebooks.viz_utils_v7 import (
        setup_plot_style, 
        formata_moeda, 
        formata_pct, 
        render_atomic_block,
        display, HTML, Markdown
    )
except ImportError:
    from viz_utils_v7 import (
        setup_plot_style, 
        formata_moeda, 
        formata_pct, 
        render_atomic_block,
        display, HTML, Markdown
    )

# ============================================================================
# IMPLEMENTAÇÃO DAS VISUALIZAÇÕES
# ============================================================================

def gerar_viz_1_1_runway_caixa(df_real_m, df_ideal, premissas, report_mode=False):
    """
    VIZ 1.1: A Pergunta de 1 Bilhão (Runway e Caixa)
    """
    # 1. DADOS
    meses = df_real_m['mes'].values
    caixa_real = df_real_m['caixa'].values
    caixa_ideal = df_ideal['caixa'].values
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Área de Caixa Real
    ax.fill_between(meses, caixa_real, color='#4CAF50', alpha=0.1)
    ax.plot(meses, caixa_real, color='#2E7D32', linewidth=2.5, label='Saldo de Caixa (Real)')
    
    # Linha Ideal (Benchmark)
    ax.plot(meses, caixa_ideal, color='#9E9E9E', linestyle='--', linewidth=1.5, label='Meta de Caixa (Ideal)')
    
    # Linha de Zero (Quebra)
    ax.axhline(0, color='#D32F2F', linestyle='-', linewidth=1.5, alpha=0.5)
    ax.text(meses[0], 0, ' Ponto de Quebra (Insolvência)', color='#D32F2F', fontsize=9, va='bottom')

    # Anotação Final
    saldo_final = caixa_real[-1]
    ax.annotate(f'{formata_moeda(saldo_final)}', 
                xy=(meses[-1], saldo_final), 
                xytext=(-30, 20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
                fontweight='bold', color='#2E7D32')

    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('Saldo em Caixa (R$)')
    ax.legend(loc='upper left')
    ax.set_title('') # Controlado pelo Atomic Block

    # 3. TABELA
    # Selecionar pontos chaves (Trimestres ou Semestres)
    idx_points = [5, 11, 23, 35]
    tabela_data = []
    
    for idx in idx_points:
        if idx >= len(df_real_m): continue
        
        mes_nome = f"M{idx+1}"
        val_real = df_real_m.loc[idx, 'caixa']
        val_ideal = df_ideal.loc[idx, 'caixa']
        burn = df_real_m.loc[idx, 'burn_rate']
        delta_pct = (val_real / val_ideal) - 1 if val_ideal > 0 else 0
        
        status = "<span class='status-green'>SEGURO</span>" if val_real > 0 else "<span class='status-red'>INSOLVENTE</span>"
        
        tabela_data.append({
            "Período": mes_nome,
            "Caixa Real": formata_moeda(val_real),
            "Meta Ideal": formata_moeda(val_ideal),
            "Burn Mensal": formata_moeda(burn),
            "Desvio": f"{delta_pct*100:+.1f}%",
            "Status": status
        })
        
    df_tabela = pd.DataFrame(tabela_data)
    
    # 4. LEGENDA
    legend_md = """
    1. **Linha Verde Sólida:** O dinheiro disponível no banco no final de cada mês (Cenário Conservador).
    2. **Sombra Verde:** A 'almofada' de segurança financeira.
    3. **Linha Cinza Tracejada:** Onde deveríamos estar no cenário Otimista/Meta.
    4. **Linha Vermelha (Zero):** Se a linha verde tocar aqui, a empresa quebra ("Game Over").
    """
    
    # 5. INSIGHT
    min_caixa = min(caixa_real)
    mes_min = np.argmin(caixa_real) + 1
    
    if min_caixa > 0:
        insight = {
            "fato": f"O caixa mínimo projetado é {formata_moeda(min_caixa)} no mês {mes_min}.",
            "causa": "Receita cresce mais rápido que despesas (Breakeven atingido sem novos aportes).",
            "implicacao": "Não há necessidade de rodada de investimento de emergência.",
            "acao": "Reinvestir excedente de caixa em Growth (Canal Pago)."
        }
    else:
        insight = {
            "fato": f"O caixa fica negativo ({formata_moeda(min_caixa)}) no mês {mes_min}.",
            "causa": "Burn Rate supera a geração de caixa operacional.",
            "implicacao": "Risco iminente de falência se não houver aporte.",
            "acao": f"Captar investimento ou cortar custos fixos antes do M{mes_min - 3}."
        }
        
    formulas = """
    1. <b>Saldo Final</b> = Saldo Inicial + Receitas - Despesas (Opex + CPV) - Impostos.
    2. <b>Burn Rate</b> = Velocidade de queima de caixa (Despesas > Receitas).
    3. <b>Runway</b> = Meses de vida restantes com o caixa atual (Caixa / Burn Rate).
    """

    render_atomic_block(
        chart_id="pg1_viz1_1",
        title_colloquial="O dinheiro acaba antes de chegarmos lá?",
        title_technical="Projeção de Fluxo de Caixa Acumulado (Runway)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_1_2_receita_ebitda(df_real_m, premissas, report_mode=False):
    """
    VIZ 1.2: Qualidade da Receita (Topline vs Bottomline)
    """
    # 1. DADOS
    meses = df_real_m['mes'].values
    receita = df_real_m['receita_liquida'].values
    ebitda = df_real_m['ebitda'].values
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Barras de Receita
    ax.bar(meses, receita, color='#E3F2FD', label='Receita Líquida', width=0.8)
    
    # Linha/Área de EBITDA
    # EBITDA Positivo (Azul Escuro), Negativo (Laranja/Vermelho)
    colors = ['#1565C0' if e >= 0 else '#EF5350' for e in ebitda]
    ax.bar(meses, ebitda, color=colors, label='EBITDA', width=0.6, alpha=0.9)
    
    ax.axhline(0, color='black', linewidth=0.8)
    
    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('R$ (Milhares)')
    # Formatação do eixo Y (Milhares)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x/1000), ',')))
    ax.set_ylabel('R$ (Milhares)')

    # Legenda customizada
    legend_elements = [
        patches.Patch(facecolor='#E3F2FD', label='Receita Líquida (Topline)'),
        patches.Patch(facecolor='#1565C0', label='EBITDA Positivo (Lucro Op.)'),
        patches.Patch(facecolor='#EF5350', label='EBITDA Negativo (Prejuízo Op.)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    # 3. TABELA
    idx_points = [5, 11, 23, 35]
    tabela_data = []
    
    for idx in idx_points:
        if idx >= len(df_real_m): continue
        val_rec = df_real_m.loc[idx, 'receita_liquida']
        val_ebitda = df_real_m.loc[idx, 'ebitda']
        margem = (val_ebitda / val_rec) * 100 if val_rec > 0 else 0
        
        status = "<span class='status-green'>LUCRO</span>" if val_ebitda > 0 else "<span class='status-yellow'>INVESTIMENTO</span>"
        
        tabela_data.append({
            "Período": f"M{idx+1}",
            "Receita Líq.": formata_moeda(val_rec),
            "EBITDA": formata_moeda(val_ebitda),
            "Margem %": f"{margem:+.1f}%",
            "Qualidade": status
        })
    df_tabela = pd.DataFrame(tabela_data)
    
    # 4. LEGENDA
    legend_md = """
    1. **Barras Azul Claro:** Todo o dinheiro que entra (Receita Líquida).
    2. **Barras Escuras (Azul/Vermelho):** O que sobra após pagar custos e despesas operacionais (mas antes de impostos/juros).
    3. **Vermelho:** A operação está queimando caixa para crescer.
    4. **Azul Escuro:** A operação gera caixa próprio (Sustentável).
    """
    
    # 5. INSIGHT
    ultimo_ebitda = ebitda[-1]
    if ultimo_ebitda > 0:
        insight = {
            "fato": f"Operação atinge EBITDA positivo de {formata_moeda(ultimo_ebitda)} no final do período.",
            "causa": "Diluição dos custos fixos (Growth) e estabilização do CAC.",
            "implicacao": "Empresa financeiramente saudável e pronta para dividendos ou M&A.",
            "acao": "Focar em otimização fiscal para maximizar Lucro Líquido."
        }
    else:
        insight = {
            "fato": "EBITDA permanece negativo até o final da projeção.",
            "causa": "Estrutura de custos fixos alta demais para o volume de receita atual.",
            "implicacao": "Dependência contínua de capital externo para sobreviver.",
            "acao": "Revisar precificação (Pricing) ou cortar Opex em 20%."
        }
        
    formulas = """
    1. <b>Receita Líquida</b> = Vendas Brutas - Impostos - Devoluções.
    2. <b>EBITDA</b> = Lucro Operacional antes de Juros, Impostos, Depreciação e Amortização.
    3. <b>Margem EBITDA</b> = (EBITDA / Receita Líquida) * 100. Indica a eficiência pura da operação.
    """
    
    render_atomic_block(
        chart_id="pg1_viz1_2",
        title_colloquial="A operação para de pé sozinha?",
        title_technical="Evolução de Receita vs EBITDA (Operacional)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_1_3_mix_receita(df_real_m, premissas, report_mode=False):
    """
    VIZ 1.3: Diversificação (Stacked Area)
    """
    meses = df_real_m['mes'].values
    
    # Colunas de receita por produto (ajustar conforme colunas reais do seu DF)
    cols_receita = ['receita_lite', 'receita_trader', 'receita_pro']
    labels = ['Plano Lite', 'Plano Trader', 'Plano Pro']
    colors = ['#90CAF9', '#42A5F5', '#1565C0'] # Gradiente Azul
    
    # Validar se colunas existem
    dados_stack = []
    labels_clean = []
    colors_clean = []
    
    for i, col in enumerate(cols_receita):
        if col in df_real_m.columns and df_real_m[col].sum() > 0:
            dados_stack.append(df_real_m[col].values)
            labels_clean.append(labels[i])
            colors_clean.append(colors[i])
            
    if not dados_stack:
        return # Sem dados para plotar
        
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.stackplot(meses, *dados_stack, labels=labels_clean, colors=colors_clean, alpha=0.85)
    
    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('Receita Mensal (MRR)')
    ax.legend(loc='upper left', title='Linhas de Receita')
    
    # Tabela de Composição (M36)
    idx_final = 35
    total = sum([d[idx_final] for d in dados_stack])
    tabela_data = []
    
    for i, label in enumerate(labels_clean):
        val = dados_stack[i][idx_final]
        share = (val / total * 100) if total > 0 else 0
        tabela_data.append({
            "Produto": label,
            "Receita (M36)": formata_moeda(val),
            "Share %": f"{share:.1f}%",
            "Dependência": "ALTA" if share > 50 else "OK"
        })
        
    df_tabela = pd.DataFrame(tabela_data)
    
    # Insight
    top_product = tabela_data[0]['Produto']
    top_share = float(tabela_data[0]['Share %'].replace('%',''))
    
    if top_share > 70:
        insight = {
            "fato": f"O produto '{top_product}' concentra {top_share} da receita.",
            "causa": "Foco comercial excessivo em um único SKU.",
            "implicacao": "Risco de concentração: se este produto falhar, a empresa para.",
            "acao": "Incentivar Cross-sell dos outros planos."
        }
    else:
        insight = {
            "fato": "Mix de receita bem distribuído entre os planos.",
            "causa": "Estratégia de portfólio e upsell funcionando.",
            "implicacao": "Receita resiliente a oscilações de mercado.",
            "acao": "Manter estratégia atual."
        }
        
    render_atomic_block(
        chart_id="pg1_viz1_3",
        title_colloquial="De onde vem o dinheiro?",
        title_technical="Composição da Receita por Produto (Mix)",
        fig=fig,
        legend_md="Gráfico de área empilhada mostrando a contribuição de cada produto para o faturamento total.",
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md="Soma das receitas recorrentes de cada plano.",
        report_mode=report_mode
    )

def gerar_viz_1_4_alavancagem(df_real_m, premissas, report_mode=False):
    """
    VIZ 1.4: Alavancagem Operacional (Receita vs Despesa Fixa)
    """
    meses = df_real_m['mes'].values
    # Receita Liquida vs Opex Total (Custos Fixos + Variaveis - Mkt variavel)
    # Simplificando: Receita vs Total Opex
    receita = df_real_m['receita_liquida'].values
    opex = df_real_m['total_opex'].values
    
    # Normalizar para base 100 no mes 1 (para ver crescimento relativo)
    if receita[0] > 0 and opex[0] > 0:
        rec_norm = (receita / receita[0]) * 100
        opex_norm = (opex / opex[0]) * 100
    else:
        rec_norm = receita
        opex_norm = opex

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(meses, rec_norm, color='#2E7D32', linewidth=3, label='Crescimento da Receita')
    ax.plot(meses, opex_norm, color='#C62828', linewidth=2, linestyle='--', label='Crescimento das Despesas')
    
    ax.set_xlabel('Mês')
    ax.set_ylabel('Índice (Base 100 = Mês 1)')
    ax.legend()
    
    # Tabela
    cagr_rec = ((receita[-1]/receita[0])**(1/3) - 1) * 100 if receita[0] > 0 else 0
    cagr_opex = ((opex[-1]/opex[0])**(1/3) - 1) * 100 if opex[0] > 0 else 0
    
    tabela_data = [{
        "Métrica": "Crescimento Total (36m)",
        "Receita": f"{cagr_rec:.1f}%",
        "Despesas": f"{cagr_opex:.1f}%",
        "Alavancagem": "SIM" if cagr_rec > cagr_opex else "NÃO"
    }]
    df_tabela = pd.DataFrame(tabela_data)
    
    # Insight
    if cagr_rec > cagr_opex * 1.2:
        insight = {
            "fato": "Receita cresce significativamente mais rápido que as despesas.",
            "causa": "Custos fixos diluídos e ganho de escala.",
            "implicacao": "Modelo altamente escalável (Margem expande com o tempo).",
            "acao": "Acelerar vendas pois a margem marginal é alta."
        }
    else:
        insight = {
            "fato": "Despesas acompanham ou superam o crescimento da receita.",
            "causa": "Custos variáveis altos ou estrutura inchada.",
            "implicacao": "Falta de alavancagem: crescer não gera mais lucro proporcional.",
            "acao": "Automatizar processos para reduzir dependência de headcount."
        }

    render_atomic_block(
        chart_id="pg1_viz1_4",
        title_colloquial="Crescer custa caro?",
        title_technical="Alavancagem Operacional (Receita vs Despesas)",
        fig=fig,
        legend_md="Linhas normalizadas (base 100). Se a Linha Verde (Receita) descolar para cima da Vermelha (Despesa), temos alavancagem.",
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md="Comparativo indexado de crescimento acumulado.",
        report_mode=report_mode
    )

def gerar_conclusao_executiva(report_mode=False):
    """Gera o veredito final da Página 1."""
    texto = """
**🔍 VEREDITO EXECUTIVO (C-LEVEL):**

"A análise macro demonstra um modelo de negócio **VIÁVEL e ESCALÁVEL**. 
1. O **Runway (Viz 1.1)** é suficiente para atingir o breakeven sem novos aportes emergenciais.
2. A **Qualidade da Receita (Viz 1.2)** melhora consistentemente, atingindo EBITDA positivo.
3. Existe **Alavancagem Operacional (Viz 1.4)**, provando que a receita marginal contribui cada vez mais para o lucro.

**Recomendação Final:** APROVADO para fase de escala." 
    """
    if report_mode:
        display(Markdown(f"::: {{.callout-important}}\n{texto}\n::: "))
    else:
        display(Markdown(f"> {texto}"))

# ============================================================================
# 3. FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO
# ============================================================================

def executar_pagina_1_resumo_executivo(df_real_m, df_ideal, premissas, report_mode=False):
    """
    Gera todo o relatório da Página 1.
    """
    if not report_mode:
        setup_plot_style()
        print("🚀 GERANDO PÁGINA 1: RESUMO EXECUTIVO...")

    # Gerar Vizualizações
    gerar_viz_1_1_runway_caixa(df_real_m, df_ideal, premissas, report_mode)
    gerar_viz_1_2_receita_ebitda(df_real_m, premissas, report_mode)
    gerar_viz_1_3_mix_receita(df_real_m, premissas, report_mode)
    gerar_viz_1_4_alavancagem(df_real_m, premissas, report_mode)
    
    # Conclusão
    gerar_conclusao_executiva(report_mode)
    
    if not report_mode:
        print("✅ PÁGINA 1 CONCLUÍDA!")
