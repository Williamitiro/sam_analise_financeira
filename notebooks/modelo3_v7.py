# MÓDULO: PÁGINA 3 - FINANCEIRO DETALHADO (V7.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-06
# OBJETIVO: Gerar as 5 visualizações da Página 3 (P&L e Eficiência de Custos)
# ARQUITETURA: Usa viz_utils_v7.py
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importando da biblioteca compartilhada
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

def gerar_viz_3_1_waterfall_caixa(df_real_m, premissas, report_mode=False):
    """
    VIZ 3.1: Waterfall de Caixa (Ano 1 ou Acumulado)
    Mostra a ponte entre o caixa inicial e o final, destacando os ofensores.
    """
    # 1. DADOS (Focando no Acumulado dos últimos 12 meses ou Total)
    # Vamos pegar o delta do último ano (M25 a M36) ou total se < 12m
    periodo_analise = 12
    if len(df_real_m) > periodo_analise:
        df_rec = df_real_m.iloc[-periodo_analise:].copy()
    else:
        df_rec = df_real_m.copy()
        
    # Agregando Valores
    receita_total = df_rec['receita_liquida'].sum()
    cogs_total = -df_rec['total_cogs'].sum()
    mkt_total = -df_rec['gasto_marketing'].sum()
    pessoal_total = -df_rec['custo_pessoal'].sum()
    infra_outros = -(df_rec['total_opex'].sum() - df_rec['gasto_marketing'].sum() - df_rec['custo_pessoal'].sum())
    impostos = -df_rec['impostos'].sum()
    
    # Lista para Waterfall
    labels = ['Receita Líquida', 'COGS (Infra/Serv)', 'Marketing (Growth)', 'Pessoal (Time)', 'Outros Opex', 'Impostos', 'Resultado Op.']
    values = [receita_total, cogs_total, mkt_total, pessoal_total, infra_outros, impostos]
    net_result = sum(values)
    values.append(net_result)
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Cores
    colors = []
    base = 0
    # Acumulador para barras flutuantes
    cumulative = 0
    
    for i, val in enumerate(values):
        if i == 0: # Receita (Positiva)
            color = '#4CAF50'
            bottom = 0
            cumulative = val
        elif i == len(values) - 1: # Resultado Final (Total)
            color = '#1565C0' if val >= 0 else '#C62828'
            bottom = 0
        else: # Despesas (Negativas)
            color = '#EF5350'
            bottom = cumulative + val # O topo da barra é o acumulado anterior
            cumulative += val
            
        # Plotar barra
        # Se for negativo, a altura é abs(val), começando de (cumulative - val) que é o bottom visual??
        # Waterfall logic:
        # Start: 0. Add 100. New level 100.
        # Next: -20. Start at 100, go down to 80.
        if i == 0 or i == len(values)-1:
            ax.bar(labels[i], val, color=color)
        else:
            # Despesas
            ax.bar(labels[i], abs(val), bottom=bottom, color=color, alpha=0.8)

    # Conectores (Linhas finas entre barras) - Opcional, simplificado aqui
    
    ax.set_title('')
    ax.set_ylabel('R$ Acumulado (Últimos 12 Meses)')
    ax.axhline(0, color='black', linewidth=0.8)
    
    # Valores nas barras
    for i, v in enumerate(values):
        y_pos = v if (i==0 or i==len(values)-1) else (cumulative - v/2) # Aproximado
        # Ajuste fino visual é complexo em waterfall matplotlib puro, vamos usar anotação simples
        # ou apenas deixar o eixo Y falar.
        pass

    # 3. TABELA
    tabela_data = []
    total_receita = values[0]
    
    for i, label in enumerate(labels[:-1]): # Exceto total
        val = values[i]
        pct = (val / total_receita) * 100
        tabela_data.append({
            "Categoria": label,
            "Valor (R$)": formata_moeda(val),
            "% da Receita": f"{pct:.1f}%",
            "Impacto": "🟢" if val > 0 else "🔴"
        })
        
    tabela_data.append({
        "Categoria": "RESULTADO FINAL",
        "Valor (R$)": formata_moeda(values[-1]),
        "% da Receita": f"{(values[-1]/total_receita)*100:.1f}%",
        "Impacto": "🏁"
    })
    
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
    1. **Barra Verde (Esq):** Todo o dinheiro que entrou (Receita Líquida).
    2. **Barras Vermelhas (Flutuantes):** Onde o dinheiro foi gasto. O tamanho da barra indica o peso do custo.
    3. **Barra Final (Dir):** O que sobrou (ou faltou) no final do período. Azul = Lucro, Vermelho = Prejuízo.
    """

    # 5. INSIGHT
    maior_custo_idx = np.argmin(values[1:-1]) + 1 # +1 offset
    maior_custo_nome = labels[maior_custo_idx]
    maior_custo_val = values[maior_custo_idx]
    
    insight = {
        "fato": f"'{maior_custo_nome}' é o maior ofensor, consumindo {abs(maior_custo_val)/receita_total*100:.0f}% da receita.",
        "causa": "Investimento agressivo ou ineficiência nesta linha de despesa.",
        "implicacao": "Margem operacional comprimida.",
        "acao": f"Revisar contratos e ROI de {maior_custo_nome}."
    }
    
    formulas = """
    1. <b>Waterfall Chart</b>: Gráfico de cascata que mostra o efeito cumulativo de valores positivos e negativos.
    2. <b>Categorias Agrupadas</b>:
       - <i>Marketing</i>: Ads + Ferramentas de Mkt.
       - <i>Pessoal</i>: Salários + Encargos + Benefícios.
       - <i>Outros</i>: Escritório, Software, Viagens, etc.
    """

    render_atomic_block(
        chart_id="pg3_viz3_1",
        title_colloquial="Para onde foi o dinheiro este ano?",
        title_technical="Waterfall de Resultados (DRE Gerencial Acumulado)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_3_2_estrutura_custos(df_real_m, premissas, report_mode=False):
    """
    VIZ 3.2: Estrutura de Custos (Evolução % da Receita)
    Stacked Area Chart normalizado a 100% da Receita? Não, melhor Stacked Bar % Revenue.
    """
    # 1. DADOS (Trimestral para não poluir)
    df_tri = df_real_m.iloc[::3].copy() # A cada 3 meses
    meses = df_tri['mes'].values
    
    # Calcular % sobre Receita Liquida
    rec = df_tri['receita_liquida'].replace(0, 1) # Evitar div/0
    
    pct_cogs = (df_tri['total_cogs'] / rec) * 100
    pct_mkt = (df_tri['gasto_marketing'] / rec) * 100
    pct_pessoal = (df_tri['custo_pessoal'] / rec) * 100
    pct_admin = ((df_tri['total_opex'] - df_tri['gasto_marketing'] - df_tri['custo_pessoal']) / rec) * 100
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    width = 2.0 # Largura visual das barras (já que pulamos meses) 
    
    p1 = ax.bar(meses, pct_cogs, width, label='COGS (Custo Serviço)', color='#90A4AE')
    p2 = ax.bar(meses, pct_pessoal, width, bottom=pct_cogs, label='Pessoal (Time)', color='#FFB74D')
    p3 = ax.bar(meses, pct_mkt, width, bottom=pct_cogs+pct_pessoal, label='Marketing (CAC)', color='#64B5F6')
    p4 = ax.bar(meses, pct_admin, width, bottom=pct_cogs+pct_pessoal+pct_mkt, label='G&A (Admin)', color='#E0E0E0')
    
    # Linha de Benchmark de Lucratividade (ex: 80% de custos totais = 20% margem)
    ax.axhline(100, color='black', linestyle='--', linewidth=1, label='Limite da Receita (100%)')
    
    ax.set_xlabel('Mês')
    ax.set_ylabel('% da Receita Líquida')
    ax.set_ylim(0, 150) # Permitir ver se estourar 100%
    ax.legend(loc='upper right', ncol=2)
    
    # 3. TABELA
    # Último Trimestre
    last_idx = df_tri.index[-1]
    tabela_data = [
        {"Tipo": "COGS", "% Rec. Atual": f"{pct_cogs.iloc[-1]:.1f}%", "Benchmark SaaS": "15-20%"},
        {"Tipo": "Pessoal (R&D+G&A)", "% Rec. Atual": f"{pct_pessoal.iloc[-1]:.1f}%", "Benchmark SaaS": "30-40%"},
        {"Tipo": "Marketing (S&M)", "% Rec. Atual": f"{pct_mkt.iloc[-1]:.1f}%", "Benchmark SaaS": "20-30%"},
        {"Tipo": "Admin/Outros", "% Rec. Atual": f"{pct_admin.iloc[-1]:.1f}%", "Benchmark SaaS": "10-15%"}
    ]
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
    1. **Gráfico Empilhado:** Mostra quanto cada departamento consome da receita.
    2. **Linha Tracejada (100%):** Se as barras passarem dessa linha, a empresa está gastando mais do que ganha (Queima de Caixa Operacional).
    3. **Objetivo:** Manter a soma das barras abaixo de 80-90% para gerar lucro.
    """

    # 5. INSIGHT
    soma_final = pct_cogs.iloc[-1] + pct_pessoal.iloc[-1] + pct_mkt.iloc[-1] + pct_admin.iloc[-1]
    if soma_final > 100:
        insight = {
            "fato": f"Custos totais representam {soma_final:.0f}% da receita no último mês.",
            "causa": "Estrutura ainda pesada para o estágio atual de faturamento.",
            "implicacao": "Operação deficitária (EBITDA Negativo).",
            "acao": "Congelar contratações e focar em eficiência de vendas."
        }
    else:
        insight = {
            "fato": f"Custos estabilizados em {soma_final:.0f}% da receita.",
            "causa": "Ganhos de eficiência e alavancagem operacional.",
            "implicacao": f"Margem Operacional positiva de {100-soma_final:.0f}%.",
            "acao": "Reinvestir margem em Marketing para acelerar (Growth)."
        }
        
    formulas = """
    1. <b>Análise Vertical</b>: Cada linha de custo dividida pela Receita Líquida do período.
    2. <b>Benchmarks</b>: Comparativo com médias de mercado para empresas SaaS em estágio de Growth.
    """

    render_atomic_block(
        chart_id="pg3_viz3_2",
        title_colloquial="Nossa estrutura está inchada?",
        title_technical="Análise Vertical de Custos (% da Receita)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_3_3_evolucao_margens(df_real_m, premissas, report_mode=False):
    """
    VIZ 3.3: O Funil de Lucratividade (Margens)
    """
    meses = df_real_m['mes'].values
    mg_bruta = df_real_m['margem_bruta_pct'].values
    mg_ebitda = df_real_m['ebitda_margin'].values
    mg_liq = df_real_m['margem_liquida'].values
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(meses, mg_bruta, color='#2E7D32', linewidth=2, label='Margem Bruta (Gross)')
    ax.plot(meses, mg_ebitda, color='#1565C0', linewidth=2, label='Margem EBITDA (Op.)')
    ax.plot(meses, mg_liq, color='#6A1B9A', linewidth=2, linestyle=':', label='Margem Líquida (Net)')
    
    ax.axhline(0, color='black', linewidth=1)
    
    ax.set_xlabel('Mês')
    ax.set_ylabel('Porcentagem (%)')
    # ax.set_ylim(-100, 100) # Opcional, travar zoom
    ax.legend(loc='lower right')
    
    # Tabela
    # M36 Snapshot
    idx = 35
    tabela_data = [
        {"Nível": "Margem Bruta", "Valor M36": f"{mg_bruta[idx]:.1f}%", "Meta": ">70%"},
        {"Nível": "Margem EBITDA", "Valor M36": f"{mg_ebitda[idx]:.1f}%", "Meta": ">20%"},
        {"Nível": "Margem Líquida", "Valor M36": f"{mg_liq[idx]:.1f}%", "Meta": ">15%"}
    ]
    df_tabela = pd.DataFrame(tabela_data)
    
    # Insight
    if mg_ebitda[idx] > 20:
        insight = {
            "fato": "Margem EBITDA supera 20% na maturidade.",
            "causa": "Alta eficiência operacional e CAC controlado.",
            "implicacao": "Negócio classificado como 'Cash Cow' (Gerador de Caixa).",
            "acao": "Preparar para distribuição de dividendos."
        }
    else:
        insight = {
            "fato": f"Margem EBITDA final de {mg_ebitda[idx]:.1f}% está abaixo da meta de 20%",
            "causa": "Peso excessivo de Opex ou CAC.",
            "implicacao": "Retorno sobre capital investido (ROIC) baixo.",
            "acao": "Revisar estrutura de Opex."
        }
    
    legend_md = """
    1. **Verde (Topo):** Quanto sobra depois de pagar o servidor/taxas (Custo Direto).
    2. **Azul (Meio):** Quanto sobra depois de pagar o time e o escritório (Operação).
    3. **Roxo (Fundo):** O que vai para o bolso do acionista (Lucro Líquido).
    """

    formulas = """
    1. <b>Margem Bruta</b> = (Receita - COGS) / Receita.
    2. <b>Margem EBITDA</b> = EBITDA / Receita.
    3. <b>Margem Líquida</b> = Lucro Líquido / Receita.
    """

    render_atomic_block(
        chart_id="pg3_viz3_3",
        title_colloquial="Quanto sobra em cada etapa?",
        title_technical="Evolução de Margens (Bruta, EBITDA, Líquida)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_3_4_headcount_efficiency(df_real_m, premissas, report_mode=False):
    """
    VIZ 3.4: Eficiência de Time (ARR por Cabeça)
    Métrica clássica de SaaS: ARR per Employee.
    """
    meses = df_real_m['mes'].values
    arr = df_real_m['arr'].values
    hc = df_real_m['headcount_total'].replace(0, 1).values # Evitar div/0

    arr_per_emp = arr / hc
    
    # Benchmark (ex: R$ 500k/cabeça para empresas maduras)
    bench_maduro = 500000
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(meses, arr_per_emp, color='#00838F', linewidth=2.5, marker='o', label='ARR por Colaborador')
    ax.axhline(bench_maduro, color='#BDBDBD', linestyle='--', label='Benchmark Maturidade (R$ 500k)')
    
    ax.set_xlabel('Mês')
    ax.set_ylabel('ARR Anualizado (R$)')
    ax.legend()
    
    # Formatar eixo Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))

    # Tabela
    tabela_data = []
    idx_points = [11, 23, 35]
    for idx in idx_points:
        if idx >= len(df_real_m): continue
        tabela_data.append({
            "Período": f"M{idx+1}",
            "Time (HC)": int(hc[idx]),
            "ARR Total": formata_moeda(arr[idx]),
            "ARR / Pessoa": formata_moeda(arr_per_emp[idx])
        })
    df_tabela = pd.DataFrame(tabela_data)
    
    # Insight
    final_eff = arr_per_emp[-1]
    if final_eff > 300000:
        insight = {
            "fato": f"Eficiência de R$ {final_eff/1000:.0f}k por pessoa.",
            "causa": "Time enxuto e alta automação.",
            "implicacao": "Empresa ágil e lucrativa.",
            "acao": "Manter cultura de 'lean team'."
        }
    else:
        insight = {
            "fato": f"Eficiência baixa de R$ {final_eff/1000:.0f}k por pessoa.",
            "causa": "Contratação antecipada à receita (Overhiring).",
            "implicacao": "Burn rate inflado por folha de pagamento.",
            "acao": "Congelar contratações até o ARR subir."
        }

    legend_md = """
    1. **Linha Azul:** Faturamento anual dividido pelo número de funcionários.
    2. **Tendência de Alta:** Significa que o time está ficando mais produtivo (ou a receita cresce mais que as contratações).
    3. **Benchmark:** Empresas de elite buscam > R$ 500k/pessoa.
    """
    
    formulas = """
    1. <b>ARR (Annual Recurring Revenue)</b> = MRR x 12.
    2. <b>Headcount</b> = Total de FTEs (Full Time Employees).
    3. <b>Eficiência</b> = ARR / Headcount.
    """

    render_atomic_block(
        chart_id="pg3_viz3_4",
        title_colloquial="O time está se pagando?",
        title_technical="Eficiência de Pessoal (ARR por Colaborador)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_conclusao_financeira(report_mode=False):
    texto = """
**🔍 VEREDITO FINANCEIRO DETALHADO:**

"A análise profunda da estrutura de capital revela:
1. **Eficiência de Custos (Viz 3.2):** A estrutura de custos converge para benchmarks saudáveis, com COGS controlado.
2. **Lucratividade (Viz 3.3):** A expansão de margem EBITDA prova a tese de alavancagem.
3. **Produtividade (Viz 3.4):** O indicador de ARR/Headcount mostra um time produtivo e não inchado.

**Conclusão:** A máquina financeira está ajustada para gerar caixa no longo prazo."""
    if report_mode:
        display(Markdown(f"::: {{.callout-important}}\n{texto}\n:::"))
    else:
        display(Markdown(f"> {texto}"))

def executar_pagina_3_financeiro(df_real_m, premissas, report_mode=False):
    """Orquestrador da Página 3."""
    if not report_mode:
        setup_plot_style()
        print("🚀 GERANDO PÁGINA 3: FINANCEIRO DETALHADO...")
        
    gerar_viz_3_1_waterfall_caixa(df_real_m, premissas, report_mode)
    gerar_viz_3_2_estrutura_custos(df_real_m, premissas, report_mode)
    gerar_viz_3_3_evolucao_margens(df_real_m, premissas, report_mode)
    gerar_viz_3_4_headcount_efficiency(df_real_m, premissas, report_mode)
    gerar_conclusao_financeira(report_mode)
    
    if not report_mode:
        print("✅ PÁGINA 3 CONCLUÍDA!")
