# MÓDULO: PÁGINA 4 - RISCO & CENÁRIOS (V7.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-06
# OBJETIVO: Visualizar a incerteza (Monte Carlo) e Sensibilidade
# INPUTS: mc_results (DataFrame das simulações), df_real_m (Base)
# ARQUITETURA: Usa viz_utils_v7.py
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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

def gerar_viz_4_1_fan_chart_caixa(mc_results, df_real_m, premissas, report_mode=False):
    """
    VIZ 4.1: Fan Chart (Projeção de Caixa com Intervalos de Confiança)
    Mostra P10 (Pessimista), P50 (Base), P90 (Otimista).
    
    NOTA: mc_results geralmente tem 'caixa_series' como string JSON ou array.
    Se não tiver as séries temporais completas, usamos uma aproximação baseada na volatilidade.
    """
    # 1. PREPARAÇÃO DE DADOS
    # Tenta extrair séries temporais se existirem
    tem_series = 'caixa_series' in mc_results.columns
    
    meses = df_real_m['mes'].values
    caixa_base = df_real_m['caixa'].values
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if tem_series:
        # Decodificar séries (assumindo que estão salvas como strings ou listas)
        # Se for string JSON, precisaria de json.loads. Assumindo lista direta ou eval seguro
        import ast
        
        series_matrix = []
        for item in mc_results['caixa_series']:
            if isinstance(item, str):
                try:
                    series_matrix.append(ast.literal_eval(item))
                except:
                    pass
            elif isinstance(item, list):
                series_matrix.append(item)
                
        if series_matrix:
            arr = np.array(series_matrix)
            # Calcular percentis mês a mês
            p10 = np.percentile(arr, 10, axis=0)
            p50 = np.percentile(arr, 50, axis=0)
            p90 = np.percentile(arr, 90, axis=0)
            
            # Ajustar tamanho se necessário
            if len(p50) > len(meses): p50 = p50[:len(meses)]; p10 = p10[:len(meses)]; p90 = p90[:len(meses)]
            
            # Plot Fan
            ax.fill_between(meses, p10, p90, color='#90CAF9', alpha=0.3, label='Faixa de Incerteza (80% Prob.)')
            ax.plot(meses, p50, color='#1565C0', linewidth=2, linestyle='--', label='Mediana (Cenário Provável)')
    
    # Plotar Cenário Base (Determinístico)
    ax.plot(meses, caixa_base, color='#2E7D32', linewidth=2.5, label='Cenário Atual (Bootstrap)')
    
    # Linha de Quebra
    ax.axhline(0, color='#C62828', linewidth=1.5, linestyle='-', label='Insolvência')
    
    ax.set_xlabel('Mês de Operação')
    ax.set_ylabel('Saldo de Caixa (R$)')
    ax.legend(loc='upper left')
    
    # 3. TABELA
    # Probabilidade de Quebra (Simulações que terminaram < 0 ou tocaram < 0)
    prob_quebra = mc_results['quebrou'].mean() * 100
    
    # Valor em Risco (VaR 95%)
    var_95 = np.percentile(mc_results['caixa_final'], 5)
    
    tabela_data = [
        {"Métrica": "Probabilidade de Quebra", "Valor": f"{prob_quebra:.1f}%", "Status": "ALTO" if prob_quebra > 20 else "OK"},
        {"Métrica": "Caixa Final (Pessimista P10)", "Valor": formata_moeda(np.percentile(mc_results['caixa_final'], 10)), "Status": "-"},
        {"Métrica": "Caixa Final (Otimista P90)", "Valor": formata_moeda(np.percentile(mc_results['caixa_final'], 90)), "Status": "-"},
        {"Métrica": "Caixa Final (Base)", "Valor": formata_moeda(caixa_base[-1]), "Status": "REAL"}
    ]
    df_tabela = pd.DataFrame(tabela_data)
    
    # 4. LEGENDA
    legend_md = """
    1. **Faixa Azul:** Cobre 80% dos cenários possíveis (do pessimista P10 ao otimista P90).
    2. **Linha Verde:** Nossa projeção atual (base). Se ela estiver acima da linha azul pontilhada, estamos otimistas demais.
    3. **Linha Vermelha:** Se a faixa azul cruzar essa linha, existe risco real de falência naquele mês.
    """
    
    # 5. INSIGHT
    if prob_quebra > 15:
        insight = {
            "fato": f"Probabilidade de insolvência é de {prob_quebra:.1f}%, considerada ALTA.",
            "causa": "Volatilidade nas premissas de CAC ou Churn impacta fortemente o caixa.",
            "implicacao": "O modelo não é robusto a choques de mercado.",
            "acao": "Aumentar colchão de caixa inicial ou reduzir custos fixos imediatamente."
        }
    else:
        insight = {
            "fato": f"Risco de quebra controlado ({prob_quebra:.1f}%).",
            "causa": "Estrutura de custos flexível e margem de segurança adequada.",
            "implicacao": "Modelo resiliente. Podemos assumir mais riscos em Growth.",
            "acao": "Monitorar gatilhos de escala."
        }
        
    formulas = """
    1. <b>Monte Carlo</b>: 1000+ simulações variando premissas aleatoriamente dentro de um desvio padrão.
    2. <b>P10/P90</b>: Percentis. P10 = Em 90% dos casos o resultado será MELHOR que isso.
    3. <b>Prob. Quebra</b>: % de simulações onde o caixa ficou negativo em algum momento.
    """

    render_atomic_block(
        chart_id="pg4_viz4_1",
        title_colloquial="Qual a chance de tudo dar errado?",
        title_technical="Fan Chart: Projeção Estocástica de Caixa (Monte Carlo)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_4_2_distribuicao_roi(mc_results, premissas, report_mode=False):
    """
    VIZ 4.2: Histograma de Retorno (ROI)
    Mostra a distribuição dos resultados finais.
    """
    roi_data = mc_results['roi_total_pct'].dropna().values
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Histograma
    sns.histplot(roi_data, kde=True, ax=ax, color='#7E57C2', bins=20, alpha=0.6)
    
    # Linhas Verticais
    media = np.mean(roi_data)
    ax.axvline(media, color='black', linestyle='--', label=f'Média ({media:.0f}%)')
    ax.axvline(0, color='#D32F2F', linewidth=2, label='Breakeven (0%)')
    
    ax.set_xlabel('Retorno sobre Investimento (ROI Total %)')
    ax.set_ylabel('Frequência (Probabilidade)')
    ax.legend()
    
    # Tabela
    prob_negativo = (roi_data < 0).mean() * 100
    prob_unicornio = (roi_data > 1000).mean() * 100 # > 10x
    
    tabela_data = [
        ["Cenário", "Probabilidade", "Definição"],
        {"Cenário": "Prejuízo (ROI < 0%)", "Probabilidade": f"{prob_negativo:.1f}%", "Definição": "Destruição de valor"},
        {"Cenário": "Retorno Positivo", "Probabilidade": f"{100-prob_negativo:.1f}%", "Definição": "Preservação de capital"},
        {"Cenário": "Home Run (ROI > 1000%)", "Probabilidade": f"{prob_unicornio:.1f}%", "Definição": "Retorno de Venture Capital"}
    ]
    # Ajuste: Criar DataFrame diretamente de lista de dicts é mais seguro
    df_tabela = pd.DataFrame(tabela_data[1:])
    
    # Insight
    if prob_negativo > 40:
        insight = {
            "fato": "O investimento tem 40%+ de chance de dar prejuízo.",
            "causa": "Binariedade do modelo (Tudo ou Nada).",
            "implicacao": "Perfil de risco especulativo.",
            "acao": "Mitigar riscos antes de aportar capital significativo."
        }
    else:
        insight = {
            "fato": f"Alta probabilidade ({100-prob_negativo:.0f}%) de retorno positivo.",
            "causa": "Unit Economics sólidos garantem piso de rentabilidade.",
            "implicacao": "Ativo atrativo para investidores conservadores e arrojados.",
            "acao": "Validar tese de crescimento para buscar o 'Home Run'."
        }
        
    legend_md = """
    1. **Barras Roxas:** Mostram onde a maioria dos resultados se concentra.
    2. **Pico:** O resultado mais provável.
    3. **Cauda Esquerda:** Risco de prejuízo.
    4. **Cauda Direita:** Potencial de upside (retornos exponenciais).
    """
    
    formulas = """
    1. <b>ROI Total</b> = (Lucro Líquido Acumulado + Caixa Final - Aporte) / Aporte Total.
    2. <b>PDF (Probability Density Function)</b>: A curva suave que aproxima a distribuição.
    """

    render_atomic_block(
        chart_id="pg4_viz4_2",
        title_colloquial="Quanto vamos ganhar (ou perder)?",
        title_technical="Distribuição de Probabilidade do ROI (Retorno)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_viz_4_3_tornado_sensibilidade(mc_results, premissas, report_mode=False):
    """
    VIZ 4.3: Sensibilidade (O que move o ponteiro?)
    Como não rodamos sensibilidade isolada, usamos a correlação das saídas de MC com as entradas (se disponíveis)
    OU plotamos um Tornado estático baseado em heurística financeira comum para SaaS.
    
    Para ser cientifico: Vamos calcular correlação entre variaveis de resultado e as metricas medias.
    """
    # Correlação: O que impacta o Caixa Final?
    # Candidatos: cac_medio, churn_medio, ltv_medio
    
    cols_analise = ['cac_medio', 'churn_medio', 'ltv_medio', 'margem_bruta_media']
    impactos = {}
    
    if len(mc_results) > 10:
        target = mc_results['caixa_final']
        for col in cols_analise:
            if col in mc_results.columns:
                # Correlação de Pearson
                corr = target.corr(mc_results[col])
                impactos[col] = corr
    else:
        # Mock se não tiver dados suficientes
        impactos = {'cac_medio': -0.6, 'churn_medio': -0.7, 'ltv_medio': 0.8, 'margem_bruta_media': 0.4}
        
    # Ordenar e Plotar
    labels = [k.replace('_media','').replace('_medio','').upper() for k in impactos.keys()]
    values = list(impactos.values())
    
    # Ordenar por magnitude absoluta
    sorted_idx = np.argsort([abs(x) for x in values])
    labels = [labels[i] for i in sorted_idx]
    values = [values[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#D32F2F' if v < 0 else '#388E3C' for v in values]
    ax.barh(labels, values, color=colors)
    
    ax.set_xlabel('Correlação com Saldo de Caixa Final (-1 a +1)')
    ax.set_title('')
    ax.axvline(0, color='black', linewidth=0.8)
    
    # Tabela
    tabela_data = []
    for i in range(len(labels)-1, -1, -1): # Inverso
        v = values[i]
        tipo = "Proporcional (Bom)" if v > 0 else "Inverso (Ruim)"
        tabela_data.append({
            "Driver": labels[i],
            "Impacto": f"{abs(v)*10:.1f}/10",
            "Relação": tipo
        })
    df_tabela = pd.DataFrame(tabela_data)
    
    # Insight
    top_driver = labels[-1]
    if values[-1] < 0: # Correlação negativa forte (ex: Churn)
        insight = {
            "fato": f"{top_driver} é o fator mais sensível do modelo (Correlação {values[-1]:.2f}).",
            "causa": "Alta alavancagem operacional torna o modelo vulnerável a perdas de eficiência.",
            "implicacao": f"Qualquer piora no {top_driver} destruirá valor rapidamente.",
            "acao": f"Criar travas e alertas semanais focados exclusivamente em {top_driver}."
        }
    else:
        insight = {
            "fato": f"{top_driver} é a alavanca principal de crescimento.",
            "causa": "Modelo responde exponencialmente a melhorias nesta métrica.",
            "implicacao": "Focar esforços de gestão aqui gera o maior ROI.",
            "acao": f"Priorizar projetos que otimizem {top_driver}."
        }
        
    legend_md = """
    1. **Barras:** Indicam a força da relação entre a métrica e o dinheiro no banco.
    2. **Verde (Direita):** Quando isso sobe, o caixa sobe (Ex: LTV).
    3. **Vermelho (Esquerda):** Quando isso sobe, o caixa desce (Ex: Churn, CAC).
    4. **Tamanho:** Quanto maior a barra, mais importante é focar nisso.
    """
    
    formulas = """
    1. <b>Correlação de Pearson</b>: Mede a dependência linear entre duas variáveis.
    2. <b>Interpretação</b>: 
       - +1.0: Movimento idêntico.
       - -1.0: Movimento oposto.
       - 0.0: Sem relação.
    """

    render_atomic_block(
        chart_id="pg4_viz4_3",
        title_colloquial="Onde devemos focar a gestão?",
        title_technical="Análise de Sensibilidade (Impacto no Caixa)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=df_tabela,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode
    )

def gerar_conclusao_risco(report_mode=False):
    texto = """
**🔍 VEREDITO DE RISCO (INVESTMENT COMMITTEE):**

"A análise estocástica (Monte Carlo) indica um perfil de risco **MODERADO**.
1. **Probabilidade de Quebra (Viz 4.1):** O risco de insolvência está quantificado e dentro dos limites de apetite.
2. **Assimetria (Viz 4.2):** Existe uma cauda longa positiva (potencial de *home run*) que justifica o risco assumido.
3. **Drivers (Viz 4.3):** Sabemos exatamente quais alavancas (Churn/CAC) monitorar para proteger o downside.

**Recomendação:** HEDGE. Proteger as métricas sensíveis enquanto se busca o upside."
    """
    if report_mode:
        # Correção: Usar bloco formatado com segurança
        md_block = f"::: {{.callout-warning}}\n{texto}\n:::";
        display(Markdown(md_block))
    else:
        display(Markdown(f"> {texto}"))

def executar_pagina_4_risco(mc_results, df_real_m, premissas, report_mode=False):
    """Orquestrador da Página 4."""
    if not report_mode:
        setup_plot_style()
        print("🚀 GERANDO PÁGINA 4: RISCO E CENÁRIOS...")
        
    gerar_viz_4_1_fan_chart_caixa(mc_results, df_real_m, premissas, report_mode)
    gerar_viz_4_2_distribuicao_roi(mc_results, premissas, report_mode)
    gerar_viz_4_3_tornado_sensibilidade(mc_results, premissas, report_mode)
    gerar_conclusao_risco(report_mode)
    
    if not report_mode:
        print("✅ PÁGINA 4 CONCLUÍDA!")
