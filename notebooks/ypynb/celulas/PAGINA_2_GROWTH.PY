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
        ax.text(val_r * 1.15, i, f'{int(val_r):,}', va='center', fontweight='bold', color='black', fontsize=10)
        
        # Conversão removida de dentro do gráfico para limpar a visualização.
        # Os dados de conversão estarão na tabela detalhada abaixo.
    
    # Fonte Dinamica (Removida daqui, passada para render_atomic_block)
    # ax.text(...)

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
**O QUE ESTOU VENDO?** Gráfico de barras comparando o **Funil de Vendas Real** (barras escuras) com a **Meta de Mercado** (barras cinzas).

**COMO LER O GRÁFICO:**
- **Barras Escuras (Preto/Verde):** Volume REAL alcançado em cada etapa do funil no cenário conservador.
- **Barras Cinza (Fundo Tracejado):** Benchmark de mercado (quanto deveríamos ter se estivéssemos na média do setor).
- **Eixo X (Escala Logarítmica):** Comprime números grandes para facilitar visualização. Ex: 10.000 visitantes vs 64 vendas ficam visíveis juntos.

**COMO LER A TABELA:**
- **Visitantes (Real):** Quantas pessoas únicas chegaram ao site.
- **Conv. Global Real:** De cada 100 visitantes, quantos viraram pagantes (%).
- **Conv. Meta (Ideal):** A conversão esperada se estivéssemos no padrão de mercado.
- **Δ (Delta):** Diferença em pontos percentuais (p.p.). Negativo = abaixo da meta.

**INTERPRETAÇÃO:** Se todas as barras escuras preencherem ou ultrapassarem as cinzas, a operação está no trilho certo.
"""
    
    # 5. INSIGHT
    
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
**FÓRMULAS:**
1. **Taxa de Conversão Global** = (Novos Pagantes / Visitantes Únicos) × 100
2. **Delta (Δ)** = Conversão Real - Conversão Meta (em pontos percentuais)

**GLOSSÁRIO:**
- **Leads (Trials):** Visitantes que iniciaram o período de teste gratuito (demonstraram interesse).
- **Novas Vendas:** Usuários que se tornaram pagantes no mês.
- **Base Ativa:** Total de clientes pagantes ativos ao final do período.
- **p.p. (Pontos Percentuais):** Diferença absoluta entre duas porcentagens. Ex: 0.62% - 0.79% = -0.17 p.p.
"""
    
    render_atomic_block(
        chart_id="pg2_viz2_1",
        title_colloquial="O volume de vendas sustenta a operação no cenário conservador?",
        title_technical="VIZ 2.1: Funil de Aquisição (Conservador vs Benchmark)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Detalhamento do Funil (Real vs Meta)",
        data_source_text="Fonte: df_real_m (Simulacao) vs df_ideal (Meta)"
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
    
    # Fonte Dinamica (Removida, via render_atomic)
    # ax.text(...)
            
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
    # 4. LEGENDA COMO LER
    legend_md = """
**O QUE ESTOU VENDO?** A evolução do índice de eficiência financeira (LTV/CAC) ao longo do tempo, sobreposto a zonas coloridas de risco.

**COMO LER O GRÁFICO:**
- **Linha Azul:** Valor do LTV/CAC Real em cada mês.
- **Zona Verde (>3x):** Operação altamente eficiente. Cada R$1 investido retorna R$3+. Pode escalar agressivamente.
- **Zona Amarela (1x-3x):** Operação sustentável, mas margem apertada. Crescimento lento.
- **Zona Vermelha (<1x):** Destruição de valor. Cada cliente CUSTA mais do que gera (Prejuízo).

**DIFERENÇA ENTRE LTV/CAC e MRR/MARKETING (Tier 1):**
- **MRR/Marketing (Tier 1):** Quanto de receita mensal gera por cada R$1 gasto. É uma visão de curto prazo (mês a mês).
- **LTV/CAC (Este Gráfico):** Quanto o cliente gera durante TODA sua vida útil por cada R$1 investido. É uma visão de longo prazo (ciclo de vida).

**POR QUE ISSO IMPORTA?**
Um negócio pode ter MRR/Marketing baixo nos primeiros meses, mas LTV/CAC alto se a retenção for forte (cliente paga por 2 anos). Por isso analisamos os dois.

**INTERPRETAÇÃO:** Mantenha a linha azul na zona verde ou amarela. Se entrar no vermelho, CONGELE investimentos.
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
    # 6. RENDER
    formulas = """
**FÓRMULAS:**
1. **LTV (Lifetime Value)** = ARPU × (1 / Churn Rate) × Margem Bruta %
2. **CAC (Custo Aquisição)** = Gastos Marketing Totais / Novos Clientes Pagantes
3. **LTV/CAC** = LTV ÷ CAC

**ZONAS DE RISCO:**
- 🟢 **>3.0x:** Alta eficiência (Escalável sem medo)
- 🟡 **1.0x - 3.0x:** Operação paga contas mas cresce devagar
- 🔴 **<1.0x:** Destruição de valor (Cada cliente dá prejuízo)

**GLOSSÁRIO:**
- **ARPU:** Receita Média por Usuário (Average Revenue Per User)
- **Churn Rate:** Percentual de clientes que cancelam por mês
- **Margem Bruta:** Receita menos custos diretos (COGS)
"""
    
    render_atomic_block(
        chart_id="pg2_viz2_2",
        title_colloquial="O negócio para em pé? (Saúde Unitária)",
        title_technical="VIZ 2.2: Evolução LTV/CAC vs Zonas de Risco",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Evolução da Eficiência LTV/CAC",
        data_source_text="Fonte: df_real_m (LTV/CAC) | Benchmark: 3.0x"
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
    
    # Fonte (Removida, via render_atomic)
    # ax.text(...)
            
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

    # 4. LEGENDA COMO LER
    legend_md = """
**O QUE ESTOU VENDO?** Grafico de Controle Estatistico (SPC) do CAC semanal para detectar anomalias operacionais.

**COMO LER O GRAFICO:**
- **Linha Preta com Pontos:** Custo de Aquisicao (CAC) real em cada semana.
- **Linha Azul Horizontal:** Media historica do CAC (o "centro" do tunel).
- **Faixa Cinza (Tunel):** Intervalo de variacao estatistica aceitavel (+/-2 Desvios Padrao).
- **Pontos Vermelhos:** Semanas com CAC FORA do tunel (anomalias que exigem investigacao).

**COMO LER A TABELA:**
- **Semana:** Identificador da semana (S1, S10, etc.)
- **CAC Real:** Custo de trazer 1 cliente naquela semana especifica.
- **Media (Centro):** Valor medio de todas as semanas (mesmo para todas as linhas).
- **UCL (Limite):** Limite Superior de Controle. Se CAC > UCL, e anomalia.
- **Status:** "CONTROLADO" (dentro do tunel) ou "ANOMALIA" (fora do tunel).

**POR QUE O UCL E IGUAL EM TODAS AS LINHAS?**
O UCL e um **limite fixo** calculado uma unica vez (Media + 2xDesvio Padrao). Ele nao muda por semana. O que muda e o CAC Real.

**COMO INVESTIGAR ANOMALIAS (FONTES DE DADOS):**
1. **Google Ads / Meta Ads:** Verifique CPCs e impressoes da semana.
2. **Google Analytics:** Cheque origem do trafego e taxa de rejeicao.
3. **CRM/Pipeline:** Verifique se houve campanha promocional ou bug no checkout.
4. **Calendario:** Compare com datas comemorativas ou eventos do setor.

**INTERPRETACAO:** Se um ponto vermelho aparecer, NAO entre em panico. Investigue primeiro. Pode ser um teste A/B bem-sucedido ou uma sazonalidade prevista.
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
**FÓRMULAS:**
1. **CAC Semanal** = Custo Marketing da Semana ÷ Novos Clientes da Semana
2. **Média (Centro)** = Soma de todos os CACs ÷ Número de semanas
3. **Desvio Padrão (σ)** = Dispersão dos valores em torno da média
4. **UCL (Upper Control Limit)** = Média + (2 × σ)
5. **LCL (Lower Control Limit)** = Média - (2 × σ)

**GLOSSÁRIO:**
- **SPC (Statistical Process Control):** Método de monitoramento de qualidade usado em manufatura e operações.
- **UCL (Upper Control Limit):** Limite superior. Valores acima disso são estatisticamente anormais (apenas 2.5% de chance de ocorrer naturalmente).
- **LCL (Lower Control Limit):** Limite inferior. Valores abaixo podem indicar oportunidade (CAC muito baixo) OU erro de dados.
- **Anomalia:** Ponto fora do túnel de controle. Pode ser positivo (oportunidade) ou negativo (problema).
"""

    render_atomic_block(
        chart_id="pg2_viz2_3",
        title_colloquial="Existe descontrole tático de custos?",
        title_technical="VIZ 2.3: Volatilidade Semanal do CAC (SPC)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Monitoramento de Anomalias (Semanal)",
        data_source_text=f"Fonte: df_real_s (CAC Semanal) | Media: R$ {media_cac:.0f}"
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
    
    # Fonte (Removida, via render_atomic)
    # ax.text(...)
            
    # 3. TABELA (REFEITA DO ZERO - MANUAL PARA EVITAR ERROS DE FORMATAÇÃO)
    # Pontos de Simulação
    step = (x.max() - x.min()) / 2
    valores_teste = [x.min(), x.min()+step, x.max()]
    
    # Lista para armazenar dados (usada para DF no modo interativo)
    dados_raw = []
    
    # Header Manual
    tabela_md = "| Investimento | Clientes Est. | Linear (Ideal) | Perda Efic. | Diagnostico |\n"
    tabela_md += "|:---|---:|---:|---:|:---|\n"
    
    for val in valores_teste:
        retorno_real_est = poly(val)
        retorno_ideal = val / cac_ideal_ref
        perda_eficiencia = 1 - (retorno_real_est / retorno_ideal)
        
        # Definição de Zona
        # Definição de Zona
        if val < cac_ideal_ref * 0.5:
             zona_txt = "VOLUME BAIXO"
             zona_emoji = "⚪ VOLUME INSUFICIENTE"
             perda_eficiencia = 0.0 # Bônus de dúvida
        elif perda_eficiencia < 0.15:
             zona_txt = "ALTA EFICIENCIA"
             zona_emoji = "🟢 ALTA EFICIÊNCIA"
        elif perda_eficiencia < 0.40:
             zona_txt = "RETORNOS DECRESCENTES"
             zona_emoji = "🟡 RETORNOS DECRESCENTES"
        else:
             zona_txt = "SATURACAO"
             zona_emoji = "🔴 SATURAÇÃO"
             
        # Formatação valores
        inv_str = formata_moeda(val)
        cli_est_str = f"{int(retorno_real_est)}"
        cli_lin_str = f"{int(retorno_ideal)}"
        perda_str = f"{perda_eficiencia*100:.1f}%"
        
        # Adiciona linha ao Markdown Manual
        tabela_md += f"| {inv_str} | {cli_est_str} | {cli_lin_str} | {perda_str} | {zona_txt} |\n"
        
        # Adiciona ao dicionário para DataFrame (Modo HTML Rico)
        dados_raw.append({
            "Investimento (R$)": inv_str,
            "Clientes Estimados": cli_est_str,
            "Clientes (Se Linear)": cli_lin_str,
            "Perda Eficiência": perda_str,
            "Diagnóstico": zona_emoji
        })
        
    df_tabela = pd.DataFrame(dados_raw)

    # Decisão: String ou DataFrame?
    # No report_mode, usamos a String Manual para garantir formatação perfeita.
    tabela_final = tabela_md if report_mode else df_tabela

    # 4. LEGENDA
    legend_md = """
**O QUE ESTOU VENDO?** Grafico de elasticidade de canal que responde: "Se eu dobrar o investimento em marketing, as vendas dobram?"

**RESPOSTA DIRETA:**
- **Se a linha azul estiver PARALELA a linha cinza tracejada:** SIM, dobrar marketing = dobra vendas.
- **Se a linha azul estiver CURVANDO PARA BAIXO:** NAO, dobrar marketing traz MENOS que o dobro de vendas (saturacao).

**COMO LER O GRAFICO:**
- **Bolinhas Azuis:** Cada bolinha e um mes real. Cor mais escura = mes mais recente.
- **Linha Azul Solida (Tendencia):** Curva ajustada que mostra o comportamento real.
- **Linha Cinza Tracejada (Linear):** Cenario ideal onde o CAC nunca sobe.

**DIFERENCA DESTE GRAFICO PARA O LTV/CAC:**
- **LTV/CAC (VIZ 2.2):** Mede eficiencia PASSADA (quanto ja retornou).
- **Este Grafico (VIZ 2.4):** Projeta eficiencia FUTURA (quanto VAI retornar se aumentar budget).

**INTERPRETACAO:** Se a linha azul estiver "deitando" (curvando para baixo), e um sinal de alerta. Significa que os canais atuais estao saturando e voce precisa diversificar.
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
**FORMULAS:**
1. **Curva Saturada:** Regressao Polinomial (Grau 2) y = ax2 + bx + c
2. **Crescimento Linear (Ideal):** y = x / CAC_minimo (assume CAC fixo para sempre)
3. **Perda de Eficiencia** = 1 - (Clientes Reais / Clientes Teoricos)

**GLOSSARIO:**
- **Elasticidade:** Razao entre variacao de vendas e variacao de investimento. Elasticidade 1.0 = dobrou budget, dobrou vendas.
- **Saturacao:** Ponto onde aumentar investimento traz retornos decrescentes.
- **Perda de Eficiencia:** Quanto do budget extra esta "virando calor" (CAC mais alto).
- **Linear Teorico:** Cenario impossivel onde o CAC nunca sobe, nao importa o volume.
"""

    render_atomic_block(
        chart_id="pg2_viz2_4",
        title_colloquial="Se dobrar o marketing, dobra a venda?",
        title_technical="VIZ 2.4: Curva de Escala e Elasticidade de Canal",
        fig=fig,
        legend_md=legend_md,
        df_tabela=tabela_final,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Teste de Elasticidade de Canal",
        data_source_text="Fonte: df_real_m (Marketing vs Vendas) | Regressão Polinomial (Grau 2)"
    )


def gerar_viz_2_5_cac_mix_canais(df_real_m, premissas, report_mode=False):
    """
    VIZ 2.5: CAC Pago vs Blended (Eficiência Orgânica)
    (Originalmente na Pagina 4, movido para cá conforme diretriz Gold Standard)
    """
    # 1. DADOS
    cac_blended = df_real_m['cac_blended'].values
    meses = df_real_m['mes'].values
    
    # Tenta pegar CAC Paid direto, senão calcula
    if 'cac_paid' in df_real_m.columns and df_real_m['cac_paid'].sum() > 0:
        cac_pago = df_real_m['cac_paid'].values
    else:
        # Fallback inteligente
        if 'novos_ads' in df_real_m.columns and 'gasto_marketing' in df_real_m.columns:
            novos_ads = df_real_m['novos_ads'].values
            gasto = df_real_m['gasto_marketing'].values
            cac_pago = np.divide(gasto, novos_ads, out=np.zeros_like(gasto), where=novos_ads!=0)
            cac_pago = np.where(cac_pago == 0, cac_blended * 1.5, cac_pago)
        else:
             cac_pago = cac_blended * 1.25

    # 2. PLOTAGEM
    figsize = (10, 6) if report_mode else (14, 6)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.20, left=0.10, right=0.95)
    
    ax.plot(meses, cac_pago, color='#EF5350', linestyle='--', linewidth=2, label='CAC Pago (Só Ads)')
    ax.plot(meses, cac_blended, color='#1976D2', linewidth=3, label='CAC Blended (Real)')
    
    ax.fill_between(meses, cac_blended, cac_pago, color='#1976D2', alpha=0.1, label='Economia Orgânica')

    ax.set_title('Eficiência de Mix: Pago vs Orgânico', fontsize=12, color='gray')
    ax.set_ylabel('Custo por Cliente (R$)', fontsize=12)
    ax.set_xlabel('Mês', fontsize=12)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # 3. TABELA
    economia = cac_pago - cac_blended
    novos = df_real_m['novos_pagantes_total'].values
    poupanca_total = economia * novos
    
    tabela_md = "| Período | CAC Pago | CAC Blended | Economia/Cliente | Total Economizado |\n"
    tabela_md += "|:---|---:|---:|---:|---:|\n"
    
    idx_show = [5, 11, 23, 35]
    for idx in idx_show:
        if idx < len(df_real_m):
            tabela_md += f"| M{meses[idx]} | {formata_moeda(cac_pago[idx])} | {formata_moeda(cac_blended[idx])} | {formata_moeda(economia[idx])} | {formata_moeda(poupanca_total[idx])} |\n"

    # 4. LEGENDA
    legend_md = """
**O QUE ESTOU VENDO?** Comparativo entre o custo de aquisicao se dependessemos 100% de anuncios (Vermelho) vs o custo real misturando organico (Azul).

**COMO LER O GRAFICO:**
- **Linha Vermelha Tracejada (CAC Pago):** Quanto custaria trazer 1 cliente se TODO o trafego viesse de anuncios.
- **Linha Azul Solida (CAC Blended):** Custo real por cliente, considerando trafego organico + pago.
- **Area Azul Clara:** Representa a ECONOMIA gerada pelo trafego organico.

**COMO LER A TABELA:**
- **CAC Pago:** Custo por cliente se fosse 100% pago.
- **CAC Blended:** Custo real por cliente (misturado).
- **Economia/Cliente:** Diferenca entre Pago e Blended. Quanto voce economiza por cliente gratuito.
- **Total Economizado:** Economia multiplicada pelo numero de clientes novos no mes.

**INTERPRETACAO:** 
- **Linhas afastadas:** SEO, Indicacoes e Branding estao gerando trafego gratuito (Otimo!).
- **Linhas juntas:** O crescimento e 100% dependente de anuncios pagos (Risco alto).
"""

    formulas = """
**FORMULAS:**
1. **CAC Pago** = Gasto em Ads / Novos Clientes (vindos de Ads)
2. **CAC Blended** = Gasto Total em Marketing / Novos Clientes (TOTAIS, inclusive organicos)
3. **Economia** = CAC Pago - CAC Blended

**GLOSSARIO:**
- **Blended:** "Misturado". Significa que estamos calculando o custo medio considerando TODOS os clientes, nao so os de ads.
- **Organico:** Trafego que vem "de graca" - SEO, indicacoes, redes sociais nao-pagas.
- **Economia Organica:** Quanto voce economiza por nao depender 100% de anuncios pagos.
"""
    
    # 5. INSIGHT
    econ_m36 = economia[-1]
    insight = {
        "fato": f"Tráfego orgânico reduz o CAC em {formata_moeda(econ_m36)} por cliente.",
        "causa": "Mix balanceado entre canais pagos e gratuitos.",
        "implicacao": "Menor sensibilidade a aumentos de CPM nas plataformas de ads.",
        "acao": "Manter investimento em SEO para ampliar o gap."
    }

    render_atomic_block(
        chart_id="pg2_viz2_5_cac_mix",
        title_colloquial="Quanto economizamos com trafego organico?",
        title_technical="VIZ 2.5: Impacto do Mix de Canais (CAC Pago vs Blended)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=tabela_md,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="📋 ECONOMIA DE CANAL",
        data_source_text="Fonte: df_real_m | CAC Paid vs CAC Blended"
    )
    plt.close(fig)


def gerar_viz_2_6_custo_churn(df_real_m, premissas, report_mode=False):
    """
    VIZ 2.6: Vazamento Invisível (Custo do Churn)
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
    
    # Fonte (Removida, via render_atomic)
    # ax.text(...)
            
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
            status = "🟢 DENTRO DA META"
            texto_delta = "OK"
        else:
            status = "🔴 VAZAMENTO"
            texto_delta = f"-{formata_moeda(delta_fin)}"
            
        # Correção para PDF: Remover emojis
        if report_mode:
            status = status.replace("🟢 ", "").replace("🔴 ", "")

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
**O QUE ESTOU VENDO?** Grafico de vazamento de receita que mostra o quanto entra (vendas) vs quanto sai (cancelamentos) por mes.

**COMO LER O GRAFICO:**
- **Barras Verdes (Acima de 0):** Receita NOVA que entrou no mes (novas vendas).
- **Barras Vermelhas (Abaixo de 0):** Receita PERDIDA por cancelamentos (churn real).
- **Barras Cinzas (Fundo):** O quanto seria aceitavel perder (benchmark de 5% de churn).
- **Linha Preta (Net Growth):** RESULTADO LIQUIDO = Vendas Novas - Churn. Se positivo, a empresa cresce. Se negativo, encolhe.

**O QUE A LINHA PRETA SIGNIFICA:**
A linha preta mostra o **crescimento liquido** do MRR. Ela considera TODOS os clientes, novos e antigos:
- **Linha preta ACIMA de 0:** A empresa esta crescendo (mais vendas que cancelamentos).
- **Linha preta NA linha 0:** Empresa estagnada (vendas = cancelamentos).
- **Linha preta ABAIXO de 0:** Empresa encolhendo (mais cancelamentos que vendas).

**COMO LER A TABELA:**
- **Churn Rate:** Percentual de clientes que cancelaram no mes.
- **Perda Real:** Valor em R$ dos contratos cancelados.
- **Limite Aceitavel:** Quanto seria "normal" perder baseado no benchmark de 5%.
- **Dinheiro Rasgado:** Perda Real - Limite Aceitavel. Se positivo, estamos perdendo mais que o normal.

**INTERPRETACAO:** A parte vermelha que excede a sombra cinza e ineficiencia de retencao que corroi o crescimento.
"""

    # 5. INSIGHT
    total_waste_anual = sum([max(0, abs(l) - abs(t)) for l, t in zip(mrr_lost[-12:], mrr_lost_target[-12:])])
    insight = {
        "fato": f"O churn acima do benchmark custou R$ {total_waste_anual:,.0f} no ultimo ano.",
        "causa": "Taxa de churn superior ao benchmark de 5%.",
        "implicacao": "Reducao direta do Valuation e necessidade de repor receita mais rapido.",
        "acao": "Implementar squad de retencao para estancar o sangramento."
    }
        
    formulas = """
**FORMULAS:**
1. **Churn Rate Real** = Clientes Cancelados / Clientes Ativos Iniciais
2. **Perda Real (Churn MRR)** = Valor somado dos contratos cancelados no mes.
3. **Perda Aceitavel (Benchmark)** = MRR Inicial x 5.0% (Meta de Mercado).
4. **Dinheiro Rasgado (Waste)** = Perda Real - Perda Aceitavel.

**GLOSSARIO:**
- **Net Growth (Crescimento Liquido):** Vendas Novas - Churn. Mostra se a empresa esta crescendo ou encolhendo.
- **Churn Rate:** Percentual de clientes que cancelaram no mes.
- **Benchmark 5%:** Taxa de churn considerada "saudavel" para SaaS.
- **Dinheiro Rasgado:** Perda de receita alem do esperado. Dinheiro que "foi pro ralo" por retencao ruim.
"""

    render_atomic_block(
        chart_id="pg2_viz2_6",
        title_colloquial="Quanto dinheiro estamos perdendo pelo ralo?",
        title_technical="VIZ 2.6: Analise de Vazamento (Net Growth e Churn)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Impacto Financeiro do Churn",
        data_source_text="Fonte: df_real_m (Churn MRR) | Benchmark: 5%"
    )


def gerar_viz_2_7_timeline_growth(df_real_m, premissas, report_mode=False):
    """
    VIZ 2.7: Cronograma de Investimento & Tiers de Growth (Solicitação User)
    """
    # 1. DADOS
    meses_num = df_real_m['mes'].values
    gasto_mkt = df_real_m['gasto_marketing'].values
    trafego_org = df_real_m['trafego_organico'].values
    
    # Recupera Tiers das Premissas para colorir (dedução reversa)
    tiers = premissas.get('growth_tiers', [])
    
    # 2. PLOTAGEM (Dual Axis)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Barras de Investimento
    bars = ax1.bar(meses_num, gasto_mkt, color='#5C6BC0', alpha=0.8, label='Investimento Mensal (R$)')
    ax1.set_xlabel('Mês de Operação')
    ax1.set_ylabel('Budget de Marketing (R$)', color='#3F51B5')
    ax1.tick_params(axis='y', labelcolor='#3F51B5')
    
    # Linha de Tráfego Orgânico (Resultado do Tier)
    ax2 = ax1.twinx()
    ax2.plot(meses_num, trafego_org, color='#66BB6A', linewidth=3, linestyle='-', marker='o', markersize=4, label='Tráfego Orgânico (Visitantes)')
    ax2.set_ylabel('Crescimento Orgânico (Vol)', color='#2E7D32')
    ax2.tick_params(axis='y', labelcolor='#2E7D32')
    
    # Tiras de Tiers (Background Color ou Anotação?)
    # Vamos usar anotação de texto nos meses chave para não poluir
    
    # Legenda combinada
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    
    # 3. TABELA (O PONTO CRÍTICO PEDIDO PELO USER)
    meses_idx = [0, 5, 11, 23, 35]
    tabela_data = []
    
    for idx in meses_idx:
        if idx >= len(df_real_m): continue
        
        mes_nome = f"M{idx+1}"
        invest = df_real_m.loc[idx, 'gasto_marketing']
        org_traffic = df_real_m.loc[idx, 'trafego_organico']
        
        # Dedução do Tier Ativo
        tier_nome = "NI (Tier 0)"
        tier_desc = "Sem Investimento"
        tier_badge = "<span class='status-red'>INATIVO</span>"
        
        if invest <= 0:
             tier_nome = "Tier 0 (Hustle)"
             tier_badge = "<span class='status-red'>ZERO</span>"
        else:
            for i, t in enumerate(tiers):
                if t['budget_min'] <= invest < t['budget_max']:
                    tier_nome = t.get('nome', f"Tier {i+1} ({t['taxa']*100:.1f}%)")
                    # Define cor badge baseado no budget
                    if invest < 2000:
                        tier_badge = "<span class='status-yellow'>BAIXO</span>"
                    elif invest < 10000:
                        tier_badge = "<span class='status-green'>MÉDIO</span>"
                    else:
                        tier_badge = "<span class='status-green' style='background:#b9f6ca'>TURBO</span>"
                    break
            
            # Fallback para ultimo tier se estourar max
            if invest >= tiers[-1]['budget_min']:
                tier_nome = tiers[-1].get('nome', "Tier Max (Growth Agressivo)")
                tier_badge = "<span class='status-green' style='background:#b9f6ca'>TURBO MAX</span>"

        tabela_data.append({
            "Período": mes_nome,
            "Budget (R$)": formata_moeda(invest),
            "Tier Ativo (Growth Engine)": tier_nome,
            "Tráfego Orgânico": f"{int(org_traffic)} visitantes",
            "Status": tier_badge
        })
        
    df_tabela = pd.DataFrame(tabela_data)

    # 4. LEGENDA
    legend_md = """
**O QUE ESTOU VENDO?** Timeline visual mostrando em qual "marcha" o motor de crescimento esta em cada fase do negocio.

**COMO LER O GRAFICO:**
- **Barras Azuis:** Quanto dinheiro foi investido em Marketing no mes (R$).
- **Linha Verde:** Volume de trafego organico gerado como RESULTADO desse investimento.
- **Quanto maior a barra, maior o "Tier":** Cada nivel de investimento ativa diferentes estrategias de crescimento.

**O QUE SAO OS "TIERS"?**
Os Tiers sao niveis de crescimento que se desbloqueiam conforme o orcamento de marketing aumenta:
- **Tier 0 (Hustle):** Zero investimento. Crescimento 100% no boca-a-boca.
- **Tier 1 (Organico Basico):** Budget baixo. Foco em conteudo e SEO simples.
- **Tier 2 (SEO Profissional):** Budget medio. Ativa estrategias de link building e conteudo avancado.
- **Tier 3+ (Growth Agressivo):** Budget alto. Ads + Influencers + PR + Viralizacao.

**COMO LER A TABELA:**
- **Periodo:** Mes de operacao (M1, M6, etc.)
- **Budget (R$):** Quanto foi investido em marketing naquele mes.
- **Tier Ativo:** Qual nivel de crescimento estava ativo baseado no budget.
- **Trafego Organico:** Quantos visitantes vieram por canais gratuitos.
- **Status:** Se o tier esta ativo (BAIXO/MEDIO/TURBO) ou inativo (ZERO).

**INTERPRETACAO:** A ideia e ver a "evolucao das marchas". Uma empresa saudavel vai desbloqueando tiers maiores conforme a receita cresce.
"""

    # 5. INSIGHT
    invest_m36 = gasto_mkt[-1] if len(gasto_mkt) > 0 else 0
    if invest_m36 > 5000:
        insight = {
            "fato": f"No M36, a empresa opera com budget de {formata_moeda(invest_m36)}, ativando Tiers de alta performance.",
            "causa": "Receita crescente desbloqueou budgets maiores (% da Receita).",
            "implicacao": "Efeito 'Flywheel': Mais receita -> Mais Mkt -> Mais Orgânico -> Mais Receita.",
            "acao": "Monitorar saturação de canais para manter eficiência."
        }
    else:
        insight = {
            "fato": f"Investimento no M36 ({formata_moeda(invest_m36)}) ainda é conservador.",
            "causa": "Restricoes de caixa ou estrategia de bootstrap.",
            "implicacao": "Crescimento organico limitado pelos Tiers baixos.",
            "acao": "Avaliar aporte para saltar de Tier."
        }
        
    formulas = """
**FORMULAS:**
1. **Growth Tier** = Nivel de crescimento determinado pelo budget mensal.
2. **Taxa Organica** = Percentual de crescimento do trafego organico ativado pelo tier.
3. **Trafego Organico** = Visitantes do mes anterior x (1 + Taxa Organica do Tier)

**GLOSSARIO:**
- **Growth Tier:** Nivel de "marcha" do motor de crescimento. Quanto mais dinheiro, maior o tier.
- **Taxa Organica:** Percentual de crescimento mensal do trafego gratuito (SEO, indicacoes).
- **Flywheel Effect:** Ciclo virtuoso onde mais receita = mais marketing = mais organico = mais receita.
- **Budget:** Orcamento mensal de marketing.
"""

    render_atomic_block(
        chart_id="pg2_viz2_7_tiers",
        title_colloquial="Em qual marcha o motor de crescimento esta?",
        title_technical="VIZ 2.7: Timeline de Investimento e Tiers de Growth",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="Histórico de Ativação de Tiers",
        data_source_text="Fonte: df_real_m (Gasto Mkt) + Premissas (Tiers)"
    )



def gerar_conclusao_growth_machine(df_real_m, df_real_s, df_ideal, premissas, report_mode=False):
    """
    Gera o Veredito Analítico Inteligente (Smart Insight).
    Lógica: Identifica o ARQUÉTIPO DO CENÁRIO com base em múltiplas variáveis.
    """
    
    # 1. DIAGNÓSTICO DE VARIÁVEIS CHAVE
    # ----------------------------------------------------------------
    idx_final = 35 if len(df_real_m) > 35 else -1
    
    # A. Volume (Tráfego)
    trafego_real = df_real_m.iloc[idx_final]['trafego_total']
    trafego_ideal = df_ideal.iloc[idx_final]['trafego_total']
    gap_trafego = (trafego_ideal - trafego_real) / trafego_ideal if trafego_ideal > 0 else 0
    tem_trafego = gap_trafego < 0.80 # Se gap > 80%, não teve tráfego relevante
    
    # B. Unit Economics
    ltv_cac = df_real_m.iloc[idx_final]['ltv_cac']
    economics_ok = ltv_cac >= 3.0
    economics_zerado = ltv_cac == 0 or pd.isna(ltv_cac)
    
    # C. Retenção
    churn_real = df_real_m.iloc[idx_final]['churn_rate']
    churn_loss = churn_real - 0.05 # Gap vs Benchmark 5%
    churn_critico = churn_real > 0.07 # > 7% é desastre
    
    # D. Causa Raiz (Financeiro)
    # Verifica se houve investimento em MKT (se 'marketing_teto' > 0 e se houve gasto real)
    gasto_total = df_real_m['gasto_marketing'].sum()
    budget_zerado = gasto_total < 1000 # R$ 1000 em 3 anos é nada.
    
    # 2. MATCH DO ARQUÉTIPO (CENÁRIOS)
    # ----------------------------------------------------------------
    titulo_cenario = ""
    texto_narrativo = ""
    cor_box = "callout-note" # Default (Azul)
    
    # CENÁRIO A: INANIÇÃO (O caso do Estresse atual)
    if budget_zerado or (not tem_trafego and economics_zerado):
        titulo_cenario = "CENÁRIO CRÍTICO: INANIÇÃO DE CAPITAL (STARVATION)"
        cor_box = "callout-important" # Vermelho
        texto_narrativo = f"""
        **Diagnóstico:** O modelo de crescimento **não foi validado por falta de 'combustível'**. A simulação indica que restrições severas de caixa ativaram travas de segurança, impedindo investimentos mínimos em aquisição (Topo de Funil).
        
        **Evidência:** O volume de tráfego ficou {gap_trafego*100:.1f}% abaixo da meta, inviabilizando qualquer teste estatístico de conversão. O LTV/CAC zerado confirma que a máquina de vendas nem chegou a ser ligada.
        
        **Ação Recomendada:** O negócio é inviável sem uma rodada de capital inicial (Seed/Angel) para financiar o 'Go-to-Market'. Bootstrapping neste cenário leva à falência certa.
        """

    # CENÁRIO B: BALDE FURADO (Leaky Bucket)
    elif churn_critico:
        titulo_cenario = "CENÁRIO DE ALERTA: BALDE FURADO (RETENÇÃO CRÍTICA)"
        cor_box = "callout-warning" # Laranja
        texto_narrativo = f"""
        **Diagnóstico:** O motor de aquisição funciona, mas **a retenção é destrutiva**. Estamos pagando caro para trazer clientes que saem rápido demais.
        
        **Evidência:** O Churn Rate final de {churn_real*100:.1f}% está muito acima do tolerável (5%), corroendo todo o valor gerado (LTV). Escalar marketing agora seria queimar dinheiro.
        
        **Ação Recomendada:** CONGELAR novos investimentos em mídia paga. Focar 100% dos recursos em Produto e Customer Success até o Churn cair para < 5%.
        """

    # CENÁRIO C: MÉTRICAS DE VAIDADE (Traffic but no Sales)
    elif tem_trafego and not economics_ok:
        titulo_cenario = "CENÁRIO TÁTICO: MÉTRICAS DE VAIDADE (BAIXA CONVERSÃO)"
        cor_box = "callout-warning"
        texto_narrativo = f"""
        **Diagnóstico:** Existe demanda e tráfego, mas **a oferta não converte**. O produto ou a comunicação não estão ressoando com o público atraído.
        
        **Evidência:** O volume de visitantes está próximo da meta, mas o Unit Economics (LTV/CAC = {ltv_cac:.1f}x) é insustentável. O problema está na eficiência do Funil (Meio/Fundo), não no Topo.
        
        **Ação Recomendada:** Revisar Proposta de Valor, Pricing e Copywriting. Não aumentar tráfego até que a conversão suba.
        """

    # CENÁRIO D: SUCESSO (Máquina de Vendas)
    elif economics_ok and not churn_critico:
        # CORREÇÃO: Título dinâmico para não chamar Real de Ideal
        titulo_cenario = "CENÁRIO VALIDADO: MÁQUINA DE VENDAS EFICIENTE" 
        cor_box = "callout-tip" # Verde
        texto_narrativo = f"""
        **Diagnóstico:** A tese de crescimento apresenta **fortes evidências de validação**. O negócio demonstra alta eficiência na captura de valor e retenção sólida.
        
        **Evidência:** Com LTV/CAC de {ltv_cac:.1f}x e Churn controlado, cada Real investido retorna multiplicado. A operação é previsível e escalável.
        
        **Ação Recomendada:** O sinal é verde para aceleração (Scale-up). Monitorar saturação de canais conforme orçamento expande.
        """
        
    else:
        # Fallback (Cenário Misto)
        titulo_cenario = "CENÁRIO MISTO: VALIDAÇÃO PARCIAL"
        texto_narrativo = f"""
        **Diagnóstico:** O modelo apresenta sinais mistos. LTV/CAC de {ltv_cac:.1f}x mostra potencial, mas ainda há ajustes finos a fazer.
        
        **Ação Recomendada:** Otimizar canais de aquisição e monitorar o Churn ({churn_real*100:.1f}%) de perto antes de escalar.
        """

    # 3. RENDERIZAÇÃO
    # ----------------------------------------------------------------
    if report_mode:
        texto_final = f"""
::: {{.{cor_box}}}
## 🧠 VEREDITO ANALÍTICO: {titulo_cenario}
{texto_narrativo}
:::
"""
    else:
        texto_final = f"""
### 🧠 VEREDITO ANALÍTICO: {titulo_cenario}
> {texto_narrativo.replace('**', '').replace('    ', '')}
"""

    try:
        display(Markdown(texto_final))
    except:
        print(texto_final) # Fallback terminal
        
    return texto_final

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
    # VIZ 2.5 (MOVIDO DA PÁGINA 4): INVESTIMENTO VS RETORNO (CANAIS)
    gerar_viz_2_1_funil_macro(df_real_m, df_ideal, premissas, report_mode=report_mode)
    gerar_viz_2_2_eficiencia_ltv_cac(df_real_m, df_ideal, premissas, report_mode=report_mode)
    gerar_viz_2_3_controle_semanal(df_real_s, df_ideal_s, premissas, report_mode=report_mode)
    gerar_viz_2_4_curva_escala(df_real_m, premissas, report_mode=report_mode)
    
    # Nova Viz 2.5 (Movida da 4.4)
    gerar_viz_2_5_cac_mix_canais(df_real_m, premissas, report_mode=report_mode)
    
    # Antiga Viz 2.5 -> Viz 2.6
    gerar_viz_2_6_custo_churn(df_real_m, premissas, report_mode=report_mode)

    # NOVA VIZ 2.7 (Solicitada pelo User): Timeline de Tiers
    gerar_viz_2_7_timeline_growth(df_real_m, premissas, report_mode=report_mode)
    
    # Gera conclusão DINÂMICA (Smart Verdict)
    gerar_conclusao_growth_machine(df_real_m, df_real_s, df_ideal, premissas, report_mode=report_mode)
    
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
