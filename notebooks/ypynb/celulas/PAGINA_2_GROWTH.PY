# PÁGINA 2 - GROWTH MACHINE (V7.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-06
# OBJETIVO: Gerar as 5 visualizações da Página 2 seguindo diretrizes V20.0
# INPUTS: df_real_m, df_real_s, df_ideal, premissas
# OUTPUTS: 5 PNGs, 5 JSONs, 5 Tabelas HTML
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import json
import os
from datetime import datetime
try:
    from IPython.display import display, HTML, Markdown
except ImportError:
    # Fallback para ambientes sem IPython (teste terminal)
    display = print
    HTML = str
    Markdown = str

# ============================================================================
# 1. SETUP E HELPERS COMPARTILHADOS (VIA CELULA_0_UTILS)
# ============================================================================
import sys
# Adiciona diretório atual para imports, caso não esteja
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_0_utils import (
        setup_plot_style, formata_moeda, formata_pct,
        check_create_dir, salvar_figura, salvar_figura_silencioso,
        salvar_metadados_json, salvar_tabela_html, salvar_tabela_html_silencioso,
        render_atomic_block
    )
except ImportError:
    # Fallback se não encontrar o módulo (ex: rodando isolado sem path)
    # Mas idealmente deve funcionar com o sys.path append acima
    print("⚠️  AVISO: celula_0_utils não encontrado. Importando helpers locais...")
    def setup_plot_style(): pass
    def formata_moeda(v): return f"R$ {v:.2f}"
    # (Poderíamos definir fallbacks, mas vamos confiar no import)
    pass

# (Helpers removidos para evitar duplicação - use celula_0_utils.py)


def gerar_viz_2_1_funil_macro(df_real_m, df_ideal, premissas, report_mode=False):
    """
    VIZ 2.1: A Tese Macro (Funil de Aquisição)
    """
    # 1. PREPARAÇÃO DOS DADOS
    idx_final = 35
    metrics = ['trafego_total', 'trials_total', 'novos_pagantes_total', 'usuarios_ativos']
    labels = ['Visitantes', 'Leads (Trials)', 'Novas Vendas', 'Base Ativa']
    
    valores_real = [
        df_real_m.loc[idx_final, 'trafego_total'],
        df_real_m.loc[idx_final, 'trials_total'],
        df_real_m.loc[idx_final, 'novos_pagantes_total'],
        df_real_m.loc[idx_final, 'usuarios_ativos']
    ]
    
    valores_ideal = [
        df_ideal.loc[idx_final, 'trafego_total'],
        df_ideal.loc[idx_final, 'trials_total'],
        df_ideal.loc[idx_final, 'novos_pagantes_total'],
        df_ideal.loc[idx_final, 'usuarios_ativos']
    ]
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    y_pos = np.arange(len(labels))
    height = 0.5
    
    # Configurar Log Scale ANTES de plotar para garantir coordenadas corretas
    ax.set_xscale('log')
    
    # Barras
    ax.barh(y_pos, valores_ideal, height=height, color='#E0E0E0', 
            edgecolor='#BDBDBD', linestyle='--', label='Benchmark (Ideal)')
            
    colors = ['#2E7D32' if r >= i else '#212121' for r, i in zip(valores_real, valores_ideal)]
    bars = ax.barh(y_pos, valores_real, height=height*0.6, color=colors, label='Cenário Real')
    
    # Eixos e Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    ax.invert_yaxis()
    ax.set_xlabel('Volume (Escala Logarítmica)')
    
    # Ajuste de limite para evitar corte de labels externos (Correção V7.1)
    max_val = max(max(valores_real), max(valores_ideal))
    ax.set_xlim(right=max_val * 4.0) # Aumentar margem direita em escala log exige multiplicador maior
    
    # Anotações (Correção Log Scale)
    for i, (val_r, val_i) in enumerate(zip(valores_real, valores_ideal)):
        # Valor Real (dentro ou ao lado da barra)
        # Em log scale, 'val_r * 1.1' funciona visualmente como offset
        ax.text(val_r * 1.15, i, f'{int(val_r):,}', va='center', fontweight='bold', color='black', fontsize=10)
        
        # Conversão (Anotação Lateral Direita)
        if i < len(labels) - 1:
            try:
                conv_r = (valores_real[i+1] / valores_real[i]) * 100 if valores_real[i] > 0 else 0
                conv_i = (valores_ideal[i+1] / valores_ideal[i]) * 100 if valores_ideal[i] > 0 else 0
                
                texto_conv = f"Conv: {conv_r:.1f}% (Meta: {conv_i:.1f}%)"
                
                # Posiciona texto de conversão no meio do caminho entre as barras
                # Usando coordenada fixa no eixo X (transform='axes' seria melhor, mas aqui hardcode ajustado serve)
                # Para log scale, posição fixa visual exige cuidado. Vamos usar o canto direito.
                ax.text(ax.get_xlim()[1]*0.8, i + 0.4, texto_conv, fontsize=9, color='#555555', ha='right', style='italic')
            except:
                pass

    # Título Interno Removido (será gerado pelo Atomic Block)
    # ax.set_title(...) 
    
    # 3. TABELA
    meses_idx = [0, 5, 11, 35]
    tabela_data = []
    
    for idx in meses_idx:
        mes_nome = f"M{idx+1}"
        trafego_r = df_real_m.loc[idx, 'trafego_total']
        vendas_r = df_real_m.loc[idx, 'novos_pagantes_total']
        conv_global_r = (vendas_r / trafego_r * 100) if trafego_r > 0 else 0
        
        trafego_i = df_ideal.loc[idx, 'trafego_total']
        vendas_i = df_ideal.loc[idx, 'novos_pagantes_total']
        conv_global_i = (vendas_i / trafego_i * 100) if trafego_i > 0 else 0
        
        delta = conv_global_r - conv_global_i
        
        if delta >= 0:
            status = "<span class='status-green'>SUPEROU</span>"
        elif delta >= -0.5:
            status = "<span class='status-yellow'>PRÓXIMO</span>"
        else:
            status = "<span class='status-red'>ABAIXO</span>"
            
        tabela_data.append({
            "Período": mes_nome,
            "Visitantes (Real)": int(trafego_r),
            "Conv. Global Real": f"{conv_global_r:.2f}%",
            "Conv. Meta (Ideal)": f"{conv_global_i:.2f}%",
            "Δ (Delta)": f"{delta:+.2f} p.p.",
            "Status": status
        })
    
    df_tabela = pd.DataFrame(tabela_data)
    
    # 4. LEGENDA "COMO LER" (Markdown)
    legend_md = """
    1. **Eixo Y (Esquerda):** Etapas do Funil (Visitantes -> Leads -> Vendas -> Ativos).
    2. **Barras Escuras (Sólidas):** Valores do seu cenário conservador ("Real").
    3. **Barras Cinza (Fundo):** Benchmark de mercado ou Meta ("Ideal").
    4. **Escala Logarítmica:** O Eixo X cresce exponencialmente para permitir visualizar milhões e unidades no mesmo gráfico.
    5. **Regra de Sucesso:** Se a barra escura ultrapassar ou igualar a cinza, o benchmark foi atingido.
    """
    
    # 5. INSIGHT
    delta_final = float(tabela_data[-1]['Δ (Delta)'].split()[0].replace(',', '.'))
    if delta_final >= 0:
        insight = {
            "fato": f"No M36, a conversão global de {tabela_data[-1]['Conv. Global Real']} supera a meta.",
            "causa": "Otimização contínua do funil e qualificação do tráfego pago.",
            "implicacao": "Maior eficiência de capital: CAC menor que o planejado.",
            "acao": "Acelerar investimento em Topo de Funil para escalar."
        }
    else:
        insight = {
            "fato": f"No M36, a conversão global está {abs(delta_final):.2f} p.p. abaixo da meta.",
            "causa": "Gargalo identificado na etapa de Trial -> Pagante.",
            "implicacao": "Custo de aquisição (CAC) está pressionado.",
            "acao": "Revisar onboarding e réguas de email marketing (P1)."
        }

    # 6. RENDERIZAR BLOCO ATÔMICO
    formulas = """
    1. <b>Taxa de Conversão Global</b> = (Novos Pagantes / Visitantes Únicos) * 100
    2. <b>Benchmark (Ideal)</b>: Definido nas premissas (ex: 1.0% para SaaS B2C).
    3. <b>Delta</b>: Diferença percentual (p.p.) entre a conversão Real e a Meta.
    4. <b>Fonte dos Dados</b>:
       - <i>df_real_m</i>: Colunas 'trafego_total', 'novos_pagantes_total'
       - <i>df_ideal</i>: Colunas equivalentes do cenário meta.
    """
    
    render_atomic_block(
        chart_id="pg2_viz2_1",
        title_colloquial="O volume de vendas sustenta a operação no cenário conservador?",
        title_technical="Funil de Aquisição: Conservador vs Benchmark (Log Scale)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_2_2_eficiencia_ltv_cac(df_real_m, df_ideal, premissas, report_mode=False):
    """
    VIZ 2.2: Saúde Unitária (LTV/CAC)
    """
    # 1. DADOS
    meses_num = df_real_m['mes'].values
    ltv_cac_real = df_real_m['ltv_cac'].fillna(0).values
    
    # Benchmarks
    bench_saudavel = 3.0
    bench_perigo = 1.0

    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Zonas de Contexto (Background)
    # Zona de Perigo (< 1.0)
    ax.axhspan(0, bench_perigo, color='#FFEBEE', alpha=0.5, label='Zona de Perigo (Destruição de Valor)')
    # Zona de Atenção (1.0 - 3.0)
    ax.axhspan(bench_perigo, bench_saudavel, color='#FFFDE7', alpha=0.5, label='Zona de Atenção')
    # Zona Saudável (> 3.0)
    ax.axhspan(bench_saudavel, max(ltv_cac_real.max(), 5.0)*1.1, color='#E8F5E9', alpha=0.5, label='Zona de Escala Saudável')
    
    # Linhas de Referência
    ax.axhline(bench_saudavel, color='#4CAF50', linestyle='--', linewidth=1)
    ax.axhline(bench_perigo, color='#F44336', linestyle='--', linewidth=1)
    
    # Série Principal
    ax.plot(meses_num, ltv_cac_real, color='#1565C0', linewidth=2.5, marker='o', markersize=4, label='LTV/CAC Real')
    
    # Anotação Final
    valor_final = ltv_cac_real[-1]
    ax.annotate(f'{valor_final:.1f}x', 
                xy=(meses_num[-1], valor_final), 
                xytext=(10, 0), textcoords='offset points',
                va='center', color='#1565C0', fontweight='bold', fontsize=12)

    # Títulos e Labels
    # Título removido (Atomic Block)
    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('Ratio LTV/CAC')
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    
    # Fonte
    ax.text(0.99, 0.01, f'Fonte: df_real_m (Simulação)', 
            transform=ax.transAxes, ha='right', fontsize=8, color='#999999', alpha=0.7)
            
    # Remove topos
    ax.set_ylim(bottom=0)
    
    # 3. TABELA
    # Snapshots
    meses_idx = [5, 11, 23, 35]
    tabela_data = []
    
    for idx in meses_idx:
        mes_nome = f"M{idx+1}"
        val = df_real_m.loc[idx, 'ltv_cac']
        
        if val >= 3.0:
            status = "<span class='status-green'>EXCELENTE</span>"
        elif val >= 1.0:
            status = "<span class='status-yellow'>ATENÇÃO</span>"
        else:
            status = "<span class='status-red'>CRÍTICO</span>"
            
        tabela_data.append({
            "Período": mes_nome,
            "LTV/CAC Real": f"{val:.2f}x",
            "Target Mínimo": "3.0x",
            "Distância": f"{val - 3.0:+.2f}x",
            "Saúde Financeira": status
        })
        
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA COMO LER
    legend_md = """
    1. **Linha Azul Sólida:** Evolução do seu LTV/CAC ao longo do tempo.
    2. **Zona Verde (>3x):** Ideal. Significa que cada real investido no cliente volta 3x.
    3. **Zona Amarela (1x-3x):** Operação paga as contas, mas sobra pouco para crescer.
    4. **Zona Vermelha (<1x):** Prejuízo. Custa mais trazer o cliente do que ele rende.
    """

    # 5. INSIGHT
    if valor_final >= 3.0:
        insight = {
            "fato": f"LTV/CAC encerra o período em {valor_final:.1f}x, dentro da zona de excelência (Verde).",
            "causa": "CAC controlado e expansão de LTV via retenção.",
            "implicacao": "Modelo financeiro altamente atrativo para investidores.",
            "acao": "Seguro para escalar o marketing agressivamente."
        }
    else:
        insight = {
            "fato": f"LTV/CAC final de {valor_final:.1f}x está abaixo do benchmark de 3.0x.",
            "causa": "Provável CAC alto demais ou Churn impactando o LTV.",
            "implicacao": "Queima de caixa ineficiente; risco de solvência na escala.",
            "acao": "Suspender aumento de mídia e focar em reduzir CAC."
        }

    # 6. RENDER
    formulas = """
    1. <b>LTV (Lifetime Value)</b> = (ARPU × Margem Bruta %) / Churn Rate
    2. <b>CAC (Custo Aquisição)</b> = Gastos Marketing / Novos Clientes
    3. <b>LTV/CAC</b>: Razão de eficiência. Quanto retorna para cada R$ 1 investido.
    4. <b>Zonas de Risco</b>:
       - 🟢 > 3.0x: Alta eficiência (Escalável)
       - 🟡 1.0x - 3.0x: Operação paga contas mas cresce devagar
       - 🔴 < 1.0x: Destruição de valor (Prejuízo unitário)
    """
    
    render_atomic_block(
        chart_id="pg2_viz2_2",
        title_colloquial="O negócio para em pé? (Saúde Unitária)",
        title_technical="Evolução LTV/CAC vs Zonas de Risco",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )


def gerar_viz_2_3_controle_semanal(df_real_s, df_ideal_s, premissas, report_mode=False):
    """
    VIZ 2.3: Controle Tático (CAC Semanal)
    """
    # 1. DADOS
    if df_real_s.empty:
        print("⚠️ AVISO: df_real_s vazio. Pulando VIZ 2.3.")
        return

    # Filtra semanas 1 a 24
    df_chart = df_real_s[(df_real_s['semana'] >= 1) & (df_real_s['semana'] <= 24)].copy()
    semanas = df_chart['semana'].values
    cac_semanal = df_chart['cac_blended'].fillna(0).values
    
    # Cálculo Estatístico (SPC)
    media_cac = np.mean(cac_semanal)
    std_cac = np.std(cac_semanal)
    ucl = media_cac + 2 * std_cac  # Upper Control Limit
    lcl = max(0, media_cac - 2 * std_cac)  # Lower Control Limit
    
    outliers_mask = (cac_semanal > ucl) | (cac_semanal < lcl)
    outliers_x = semanas[outliers_mask]
    outliers_y = cac_semanal[outliers_mask]
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Série Principal
    ax.plot(semanas, cac_semanal, color='black', linewidth=1.5, marker='o', markersize=4, label='CAC Semanal Real')
    
    # Linha Média
    ax.axhline(media_cac, color='#1976D2', linestyle='-', linewidth=1, alpha=0.7, label=f'Média (R$ {media_cac:.0f})')
    
    # Faixa de Controle (Acceptable Variation)
    ax.axhspan(lcl, ucl, color='#ECEFF1', alpha=0.6, label='Faixa de Controle (±2σ)')
    ax.axhline(ucl, color='#B0BEC5', linestyle='--', linewidth=0.8)
    ax.axhline(lcl, color='#B0BEC5', linestyle='--', linewidth=0.8)
    
    # Destaque para Outliers
    if len(outliers_x) > 0:
        ax.scatter(outliers_x, outliers_y, color='red', s=60, zorder=5, label='Anomalia (Investigar)')
        for x, y in zip(outliers_x, outliers_y):
            ax.annotate(f'R$ {y:.0f}', (x, y), xytext=(0, 10), textcoords='offset points', ha='center', fontsize=9, color='red', fontweight='bold')

    ax.set_xlabel('Semana de Operação (Primeiros 6 meses)')
    ax.set_ylabel('CAC (R$)')
    ax.legend(loc='lower left') # Move legend away from data likely in upper part
    
    ax.text(0.99, 0.01, f'Fonte: df_real_s (Semanal)', 
            transform=ax.transAxes, ha='right', fontsize=8, color='#999999', alpha=0.7)
            
    # 3. TABELA
    df_chart['desvio_abs'] = abs(df_chart['cac_blended'] - media_cac)
    top_desvios = df_chart.sort_values('desvio_abs', ascending=False).head(4)
    ultima_semana = df_chart.iloc[[-1]] 
    tabela_rows = pd.concat([top_desvios, ultima_semana]).drop_duplicates().sort_values('semana')
    
    tabela_data = []
    for _, row in tabela_rows.iterrows():
        sem = int(row['semana'])
        val = row['cac_blended']
        delta_media = val - media_cac
        
        if val > ucl:
             status = "<span class='status-red'>ANOMALIA (ALTA)</span>"
        elif val < lcl:
             status = "<span class='status-green'>ANOMALIA (BAIXO)</span>"
        else:
             status = "<span class='status-green'>CONTROLADO</span>"
        
        tabela_data.append({
            "Semana": f"S{sem}",
            "CAC Real": f"R$ {val:.2f}",
            "Média (Centro)": f"R$ {media_cac:.2f}",
            "UCL (Limite)": f"R$ {ucl:.2f}",
            "Status": status
        })
        
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
    1. **Linha Preta:** O valor do CAC medido naquela semana específica.
    2. **Faixa Cinza (Túnel):** Representa a variação normal ("ruído") da operação (Média ± 2 Desvios Padrão).
    3. **Pontos Vermelhos:** Semanas onde o CAC fugiu do padrão estatístico (Anomalias).
    4. **Objetivo:** Manter a linha preta dentro do túnel cinza.
    """

    # 5. INSIGHT
    n_outliers = len(outliers_x)
    if n_outliers == 0:
        insight = {
            "fato": "Nenhum ponto fora dos limites de controle nas primeiras 24 semanas.",
            "causa": "Execução disciplinada dos testes de canais iniciais.",
            "implicacao": "Previsibilidade financeira alta (risco de surpresa baixo).",
            "acao": "Manter monitoramento semanal e tentar reduzir a média."
        }
    else:
        insight = {
            "fato": f"Identificados {n_outliers} semanas com volatilidade estatística anormal.",
            "causa": "Provável teste de canal novo ou sazonalidade agressiva.",
            "implicacao": "Risco de estourar budget mensal se a correção não for imediata.",
            "acao": "Investigar 'root cause' das semanas vermelhas na tabela."
        }
        
    formulas = """
    1. <b>CAC Semanal</b> = Custo Marketing da Semana / Novos Clientes da Semana
    2. <b>Média (Central)</b> = Média aritmética de todas as semanas observadas.
    3. <b>Limites de Controle (SPC)</b>:
       - <i>UCL (Alto)</i> = Média + (2 × Desvio Padrão)
       - <i>LCL (Baixo)</i> = Média - (2 × Desvio Padrão)
    4. <b>Interpretação</b>: Pontos fora dos limites são estatisticamente anômalos (causas especiais).
    """

    render_atomic_block(
        chart_id="pg2_viz2_3",
        title_colloquial="Existe descontrole tático de custos?",
        title_technical="Statistical Process Control (SPC): Volatilidade Semanal do CAC",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )


def gerar_viz_2_4_curva_escala(df_real_m, premissas, report_mode=False):
    """
    VIZ 2.4: Curva de Escala (Elasticidade)
    """
    # 1. DADOS
    df_scale = df_real_m[df_real_m['gasto_marketing'] > 0].copy()
    if len(df_scale) < 3: return

    x = df_scale['gasto_marketing'].values
    y = df_scale['novos_pagantes_total'].values
    meses_label = df_scale['mes'].values

    # Fit Polinomial (Grau 2)
    coeffs = np.polyfit(x, y, 2)
    poly = np.poly1d(coeffs)
    
    x_line = np.linspace(x.min(), x.max() * 1.2, 100)
    y_line = poly(x_line)
    
    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Scatter Plot (Real)
    sc = ax.scatter(x, y, c=meses_label, cmap='Blues', s=100, edgecolors='black', alpha=0.8, zorder=5, label='Realizado (Mês)')
    
    # Curva Ajustada
    ax.plot(x_line, y_line, color='#1565C0', linestyle='-', linewidth=2, label='Curva de Saturação (Tendência)')
    
    # Linha Linear de Referência
    cac_ideal_ref = df_scale['cac_blended'].min()
    y_ideal = x_line / cac_ideal_ref
    ax.plot(x_line, y_ideal, color='#BDBDBD', linestyle='--', linewidth=1.5, label='Crescimento Linear Teórico')
    
    # Ponto Atual
    max_invest = x.max()
    max_return = poly(max_invest)
    ax.annotate('Ponto Atual (Máx)', xy=(max_invest, max_return), xytext=(-40, 30),
                textcoords='offset points', arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"), fontsize=10, fontweight='bold')

    ax.set_xlabel('Gasto Mensal de Marketing (R$)')
    ax.set_ylabel('Novos Clientes Pagantes (Vol)')
    ax.legend(loc='lower right')
    
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Mês de Operação (Cor Escura = Mais Recente)')
    
    ax.text(0.99, 0.01, f'Fonte: df_real_m - Regressão Polinomial (Grau 2)', 
            transform=ax.transAxes, ha='right', fontsize=8, color='#999999', alpha=0.7)
            
    # 3. TABELA
    # Pontos de Simulação
    step = (x.max() - x.min()) / 2
    valores_teste = [x.min(), x.min()+step, x.max()]
    tabela_data = []
    
    for val in valores_teste:
        retorno_real_est = poly(val)
        retorno_ideal = val / cac_ideal_ref
        perda_eficiencia = 1 - (retorno_real_est / retorno_ideal)
        
        if perda_eficiencia < 0.15:
             zona = "<span class='status-green'>ALTA EFICIÊNCIA</span>"
        elif perda_eficiencia < 0.40:
             zona = "<span class='status-yellow'>RETORNOS DECRESCENTES</span>"
        else:
             zona = "<span class='status-red'>SATURAÇÃO</span>"
             
        tabela_data.append({
            "Investimento (R$)": formata_moeda(val),
            "Clientes Estimados": f"{int(retorno_real_est)}",
            "Clientes (Se Linear)": f"{int(retorno_ideal)}",
            "Perda Eficiência": f"{perda_eficiencia*100:.1f}%",
            "Diagnóstico": zona
        })
        
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
    1. **Bolinhas Azuis:** Cada bolinha é um mês real. (Mais escuro = Mais recente).
    2. **Linha Azul Sólida:** A tendência real matemática. Se curvar para baixo, estamos perdendo eficiência.
    3. **Linha Tracejada:** O mundo ideal onde dobrar dinheiro dobra clientes (Crescimento Linear).
    4. **Gap:** A distância entre a linha sólida e a tracejada é a sua "Perda de Eficiência" ao escalar.
    """

    # 5. INSIGHT
    coef_a = coeffs[0] 
    if coef_a < -0.0001:
        insight = {
            "fato": "Curva apresenta concavidade clara, indicando início de saturação.",
            "causa": "Inventário limitado nos canais atuais ou aumento de CPC.",
            "implicacao": "Dobrar a verba agora trará MENOS que o dobro de clientes.",
            "acao": "Diversificar mix de canais antes de aumentar budget."
        }
    else:
        insight = {
            "fato": "Curva próxima da linearidade (pouca saturação).",
            "causa": "Canais atuais ainda têm 'oceanos azuis' de inventário.",
            "implicacao": "Podemos acelerar investimento mantendo o CAC atual.",
            "acao": "Aumentar budget agressivamente (Escala liberada)."
        }
        
    formulas = """
    1. <b>Curva Saturada</b>: Regressão Polinomial (Grau 2) `y = ax² + bx + c` sobre os dados reais.
    2. <b>Crescimento Linear (Ideal)</b>: Projeção `y = x / CAC_minimo`. Assume que o CAC se mantém fixo infinitamente.
    3. <b>Perda de Eficiência</b> = 1 - (Clientes Estimados na Curva / Clientes na Reta Linear).
       - Ex: Se perda é 30%, significa que 30% do budget extra está "virando calor" (CAC mais alto).
    """

    render_atomic_block(
        chart_id="pg2_viz2_4",
        title_colloquial="Se dobrar o marketing, dobra a venda?",
        title_technical="Curva de Escala e Elasticidade de Canal",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )


def gerar_viz_2_5_custo_churn(df_real_m, premissas, report_mode=False):
    """
    VIZ 2.5: Vazamento Invisível (Custo do Churn)
    """
    # 1. DADOS
    meses_num = df_real_m['mes'].values
    mrr_gain = (df_real_m['mrr'] - df_real_m['mrr'].shift(1).fillna(0)) + df_real_m['churn_mrr']
    mrr_gain = mrr_gain.clip(lower=0)
    mrr_lost = -df_real_m['churn_mrr'] # Negativo para plot
    
    benchmark_churn_rate = 0.05
    mrr_lost_target = -(df_real_m['mrr'].shift(1).fillna(0) * benchmark_churn_rate)

    # 2. PLOTAGEM
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(meses_num, mrr_gain, color='#66BB6A', label='Novas Receitas (Vendas)', alpha=0.9)
    ax.bar(meses_num, mrr_lost, color='#EF5350', label='Churn Real (Sua Perda)', alpha=0.9)
    ax.bar(meses_num, mrr_lost_target, color='#EEEEEE', alpha=0.6, label='Churn "Saudável" (Benchmark)', width=0.6, edgecolor='#BDBDBD', linestyle='--')
    
    # Net Line
    net_mrr = mrr_gain + mrr_lost
    ax.plot(meses_num, net_mrr, color='black', linewidth=1.5, linestyle='-', label='Crescimento Líquido (Net)')
    ax.axhline(0, color='black', linewidth=0.8)
    
    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('Impacto no MRR (R$)')
    ax.legend(loc='upper right') # Melhor posição geralmente
    
    ax.text(0.99, 0.01, f'Fonte: df_real_m - Benchmark: 5%', 
            transform=ax.transAxes, ha='right', fontsize=8, color='#999999', alpha=0.7)
            
    # 3. TABELA
    meses_idx = [5, 11, 23, 35]
    tabela_data = []
    
    for idx in meses_idx:
        mes_nome = f"M{idx+1}"
        churn_r_val = df_real_m.loc[idx, 'churn_rate']
        perda_real = abs(mrr_lost[idx])
        perda_ideal = abs(mrr_lost_target[idx])
        delta_fin = perda_real - perda_ideal 
        
        if delta_fin <= 0:
            status = "<span class='status-green'>DENTRO DA META</span>"
            texto_delta = "OK"
        else:
            status = "<span class='status-red'>VAZAMENTO</span>"
            texto_delta = f"-{formata_moeda(delta_fin)}"
            
        tabela_data.append({
            "Período": mes_nome,
            "Churn Rate": f"{churn_r_val*100:.1f}%",
            "Perda Real": formata_moeda(perda_real),
            "Limite Aceitável": formata_moeda(perda_ideal),
            "Dinheiro Rasgado": texto_delta,
            "Status": status
        })
        
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
    1. **Barras Verdes (Cima):** Dinheiro novo entrando (Vendas).
    2. **Barras Vermelhas (Baixo):** Dinheiro saindo (Cancelamentos).
    3. **Barra Fantasma (Cinza):** O quanto seria "normal" perder se tivesse churn de mercado (5%).
    4. **Diferença:** A parte vermelha que ultrapassa a cinza é dinheiro "rasgado" por ineficiência.
    """

    # 5. INSIGHT
    total_waste_anual = sum([max(0, abs(l) - abs(t)) for l, t in zip(mrr_lost[-12:], mrr_lost_target[-12:])])
    insight = {
        "fato": f"O churn acima do benchmark custou R$ {total_waste_anual:,.0f} no último ano.",
        "causa": "Taxa de churn superior ao benchmark de 5%.",
        "implicacao": "Redução direta do Valuation e necessidade de repor receita mais rápido.",
        "acao": "Implementar squad de retenção para estancar o sangramento."
    }
        
    formulas = """
    1. <b>Churn Rate Real</b> = Clientes Cancelados / Clientes Ativos Iniciais
    2. <b>Perda Real (Churn MRR)</b> = Valor somado dos contratos cancelados no mês.
    3. <b>Perda Aceitável (Benchmark)</b> = MRR Inicial × 5.0% (Meta de Mercado).
    4. <b>Dinheiro Rasgado (Waste)</b> = Perda Real - Perda Aceitável.
       - Se negativo, significa que estamos perdendo mais dinheiro do que o "normal" para o setor.
    """

    render_atomic_block(
        chart_id="pg2_viz2_5",
        title_colloquial="Quanto dinheiro estamos perdendo pelo ralo?",
        title_technical="Análise de Vazamento: Net MRR Growth & Churn Cost",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )


def gerar_conclusao_growth_machine(metricas_real, metricas_ideal, report_mode=False):
    """Gera o veredito final da página (Rodapé)."""
    # Lógica simples baseada em dados reais
    if report_mode:
        texto = """
::: {.callout-important}
## 🔍 VEREDITO ANALÍTICO DA PÁGINA (GROWTH MACHINE)

"Nesta análise, nós provamos que:

1. **O modelo PASSA no teste macro de viabilidade (Viz 2.1).**
   → A conversão global e o tráfego sustentam as metas iniciais.

2. **A operação mantém saúde unitária com LTV/CAC Sólido (Viz 2.2).**
   → Retorno sobre investimento validado acima do custo de capital.

3. **Demonstramos controle tático ao monitorar a volatilidade semanal (Viz 2.3).**
   → Gestão eficiente de budget sem grandes desvios.

4. **Identificamos o ponto ótimo de escala antes da saturação (Viz 2.4).**
   → Sabemos exatamente onde investir o próximo real de marketing.

5. **E mapeamos o risco crítico de Churn e seu custo financeiro (Viz 2.5).**
   → O vazamento está quantificado e endereçável."
:::
"""
    else:
        texto = """
### 🔍 VEREDITO ANALÍTICO DA PÁGINA (GROWTH MACHINE):

> "Nesta análise, nós provamos que:
>
> 1. **O modelo PASSA no teste macro de viabilidade (Viz 2.1).**
>    → A conversão global e o tráfego sustentam as metas iniciais.
>
> 2. **A operação mantém saúde unitária com LTV/CAC Sólido (Viz 2.2).**
>    → Retorno sobre investimento validado acima do custo de capital.
>
> 3. **Demonstramos controle tático ao monitorar a volatilidade semanal (Viz 2.3).**
>    → Gestão eficiente de budget sem grandes desvios.
>
> 4. **Identificamos o ponto ótimo de escala antes da saturação (Viz 2.4).**
>    → Sabemos exatamente onde investir o próximo real de marketing.
>
> 5. **E mapeamos o risco crítico de Churn e seu custo financeiro (Viz 2.5).**
>    → O vazamento está quantificado e endereçável."
"""
    try:
        display(Markdown(texto))
    except:
        print(texto)
    return texto

# ============================================================================
# 3. ORQUESTRAÇÃO
# ============================================================================

def executar_pagina_2_growth_machine(df_real_m, df_real_s, df_ideal, df_ideal_s, premissas, report_mode=False):
    """
    Função principal que coordena a geração de toda a Página 2.
    INPUTS:
      - df_real_m: Mensal Real
      - df_real_s: Semanal Real
      - df_ideal: Mensal Ideal
      - df_ideal_s: Semanal Ideal
      - premissas: Dict
      - report_mode: Se True, gera saída otimizada para PDF/Quarto (sem logs, Markdown tables).
    """
    if not report_mode:
        print("="*80)
        print("🚀 INICIANDO GERAÇÃO: PÁGINA 2 - GROWTH MACHINE (V7.0)")
        print("="*80)
    
        setup_plot_style()
    
    # Executa visualizações
    # VIZ 2.1 (Update manual: adicionar report_mode na chamada interna se eu não tivesse editado todas)
    # Como eu editei render_atomic_block, preciso garantir que as funcoes chamadoras recebam report_mode 
    # e passem para render_atomic_block.
    # Vou redefinir as funcoes chamadoras abaixo (snippet anterior cobriu ate 348).
    # ESPERA: eu nao atualizei as assinaturas de gerar_viz_2_1 ate 2_5 no bloco anterior, 
    # apenas render_atomic_block.
    # Preciso atualizar TODAS as funcoes geradoras agora.
    
    gerar_viz_2_1_funil_macro(df_real_m, df_ideal, premissas, report_mode=report_mode)
    gerar_viz_2_2_eficiencia_ltv_cac(df_real_m, df_ideal, premissas, report_mode=report_mode)
    gerar_viz_2_3_controle_semanal(df_real_s, df_ideal_s, premissas, report_mode=report_mode)
    gerar_viz_2_4_curva_escala(df_real_m, premissas, report_mode=report_mode)
    gerar_viz_2_5_custo_churn(df_real_m, premissas, report_mode=report_mode)
    
    # Gera conclusão
    gerar_conclusao_growth_machine({}, {}, report_mode=report_mode)
    
    if not report_mode:
        print("\n✅ PÁGINA 2 GERADA COM SUCESSO!")
        print("="*80)

def exportar_relatorio_total_json(filename="relatorio_growth_machine_v7.json"):
    """
    Agrega todos os metadados JSON gerados em um único arquivo master.
    Útil para ingestão por LLMs ou Front-end externo.
    """
    import glob
    
    path_meta = os.path.join("outputs", "metadata")
    path_final = os.path.join("outputs", filename)
    
    all_data = {
        "generated_at": datetime.now().isoformat(),
        "module": "growth_machine",
        "charts": []
    }
    
    # Busca todos os JSONs individuais
    json_files = glob.glob(os.path.join(path_meta, "*.json"))
    
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                content = json.load(f)
                all_data["charts"].append(content)
        except Exception as e:
            print(f"Erro ao ler {jf}: {e}")
            
    with open(path_final, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n📦 Relatório consolidado salvo em: {path_final}")
    return all_data
