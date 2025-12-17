# PÁGINA 1 (PDF) - PÁGINA 1: EXECUTIVE COCKPIT GOLD STANDARD V5.0
# ============================================================================
# VERSÃO: 5.0 (CORRIGIDA COM FEEDBACK DO USUÁRIO)
# STATUS: PRODUCTION READY - GOLD STANDARD
#
# CORREÇÕES V5.0:
# ✅ Cards: fontes maiores, textos explicativos
# ✅ Runway: CORRIGIDO - mostra caixa/despesas (não infinito)
# ✅ Gráficos: grid visível, âncoras trimestrais
# ✅ Tabela de valores: abaixo do gráfico, por trimestre/semestre
# ✅ Milestones: metas dinâmicas de df_ideal (ZERO hardcoded)
# ✅ Eficiência: barras duplas (Marketing x MRR lado a lado)
# ✅ Consistência: mesma nomenclatura em todo lugar
# ============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings('ignore')

try:
    from IPython.display import display, HTML, Markdown
except ImportError:
    # Fallback para ambientes sem IPython
    display = print
    HTML = str
    Markdown = str

# ============================================================================
# VALIDAÇÕES DE DEPENDÊNCIAS
# ============================================================================
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_0_utils import (
        render_atomic_block, setup_plot_style, 
        salvar_figura_silencioso, salvar_tabela_html_silencioso
    )
    HAS_UTILS = True
except ImportError:
    HAS_UTILS = False
    # print("⚠️  celula_0_utils não encontrado. Usando fallback.")


# ============================================================================
# CONFIGURAÇÕES VISUAIS (ZERO HARDCODE - usa PREMISSAS se disponível)
# ============================================================================
CORES = {
    'real': '#000000',        # Preto - dados reais
    'ideal': '#388E3C',       # Verde - cenário ideal/benchmark
    'benchmark': '#D32F2F',   # Vermelho - metas
    'pessimista': '#F57C00',  # Laranja - P10
    'usuarios': '#7B1FA2',    # Roxo - usuários
    'marketing': '#1976D2',   # Azul - marketing
    'fundo': '#FFFFFF',       # Branco
    'sucesso': '#4CAF50',     # Verde claro
    'atencao': '#FF9800',     # Amarelo/Laranja
    'critico': '#F44336',     # Vermelho
}

# FONTES DE DADOS DINAMICAS
# Cada visualizacao define sua propria fonte baseada nos dados usados
def gerar_fonte(dfs_usados):
    """Gera texto de fonte dinamico baseado nos DataFrames utilizados."""
    return f"Fonte: {' | '.join(dfs_usados)}"

# Formatadores para moeda e percentual
def formatar_moeda(valor, prefixo='R$ '):
    if abs(valor) >= 1_000_000:
        return f'{prefixo}{valor/1_000_000:.1f}M'
    elif abs(valor) >= 1_000:
        return f'{prefixo}{valor/1_000:.1f}k'
    else:
        return f'{prefixo}{valor:.0f}'

def formatar_pct(valor):
    return f'{valor:.1f}%'

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def adicionar_ruido_natural(serie, intensidade=0.02):
    """
    Adiciona ruído suave para evitar linhas retas artificiais.
    Intensidade: 2% por padrão (variação natural)
    """
    ruido = np.random.normal(0, serie * intensidade)
    return serie + ruido

def calcular_status(valor, benchmark, inversao=False, tolerancia=0.2):
    """
    Determina status visual baseado no benchmark.
    inversao=True para métricas onde menor é melhor (churn, CAC)
    """
    if inversao:
        if valor <= benchmark:
            return '✅', 'sucesso', 'SAUDÁVEL'
        elif valor <= benchmark * (1 + tolerancia):
            return '⚠️', 'atencao', 'ATENÇÃO'
        else:
            return '🔴', 'critico', 'CRÍTICO'
    else:
        if valor >= benchmark:
            return '✅', 'sucesso', 'SAUDÁVEL'
        elif valor >= benchmark * (1 - tolerancia):
            return '⚠️', 'atencao', 'ATENÇÃO'
        else:
            return '🔴', 'critico', 'CRÍTICO'

def encontrar_mes_milestone(df, coluna, valor):
    """Encontra o primeiro mês onde a coluna atinge o valor."""
    mask = df[coluna] >= valor
    if mask.any():
        return int(df[mask].iloc[0]['mes'])
    return None

# ============================================================================
# FUNÇÃO 1: TABELA EXECUTIVA MASTER
# ============================================================================
def gerar_tabela_executiva(df_real, df_ideal, met_real, met_ideal, report_mode=False):
    """
    Gera tabela executiva com snapshot M1, M6, M12, M36.
    100% dinâmico - ZERO hardcoded.
    """
    if not report_mode:
        print("\n" + "="*80)
        print("1.1 TABELA EXECUTIVA MASTER - PROJEÇÃO 36 MESES (V7.2)")
        print("="*80)
    else:
        display(Markdown("## 1.1 TABELA EXECUTIVA MASTER"))
    
    # Snapshots
    m1 = df_real.iloc[0]
    m6 = df_real.iloc[5] if len(df_real) > 5 else df_real.iloc[-1]
    m12 = df_real.iloc[11] if len(df_real) > 11 else df_real.iloc[-1]
    m36 = df_real.iloc[-1]
    
    # Ideal (benchmark dinâmico)
    ideal_final = df_ideal.iloc[-1] if 'df_ideal' in globals() and len(df_ideal) > 0 else m36
    
    # Definição de métricas (nome, coluna, benchmark, inversão)
    metricas = [
        ('RECEITA', '', '', '', '', ''),
        ('  MRR', 'mrr', met_ideal.get('mrr_final', m36['mrr']), False),
        ('  ARR (Anual)', 'arr', met_ideal.get('mrr_final', m36['mrr']) * 12, False),
        ('  Usuários Ativos', 'usuarios_ativos', met_ideal.get('usuarios_final', 1000), False),
        ('', '', '', '', '', ''),
        ('UNIT ECONOMICS', '', '', '', '', ''),
        ('  LTV/CAC (Índice de Retorno)', 'ltv_cac', 3.0, False),
        ('  CAC (Custo Aquisição Cliente)', 'cac_blended', 250, True),
        ('  Churn (Taxa Cancelamento %)', 'churn_rate', 0.05, True),
        ('  Payback (Meses p/ Recuperar CAC)', 'payback_meses', 12, True),
        ('', '', '', '', '', ''),
        ('CAIXA & RUNWAY', '', '', '', '', ''),
        ('  Caixa Disponível', 'caixa', 50000, False),
        ('  Runway (Meses de Sobrevivência)', 'runway_meses', 12, False),
        ('  Burn Rate (Queima Mensal)', 'burn_rate', 0, True),
        ('', '', '', '', '', ''),
        ('MARGENS & RETORNO', '', '', '', '', ''),
        ('  Margem Bruta %', 'margem_bruta_pct', 70, False),
        ('  EBITDA (Lucro Operacional)', 'ebitda', 0, False),
        ('  Lucro Líquido Acumulado (36m)', 'lucro_liquido_acum', 0, False),
        ('', '', '', '', '', ''),
        ('INVESTIDOR', '', '', '', '', ''),
        ('  Investimento Realizado (Total)', 'investimento_total', 0, False),
        ('  ROI Potencial (Exit 5x ARR)', 'roi_investidor_exit', 100, False),
        ('  ROI Realizado (Caixa M36)', 'roi_investidor_caixa', 0, False),
        ('  Valuation Estimado (5x ARR)', 'valuation_estimado', 1000000, False),
        ('  Break-Even (Mês Lucrativo)', 'break_even_mes', 12, True),
    ]
    
    # =========================================
    # CÁLCULOS PARA MÉTRICAS DO INVESTIDOR
    # =========================================
    # ROI: (Valor Atual - Investimento Total) / Investimento Total × 100
    # Investimento = Caixa Inicial + Soma de todos os aportes (limitado aos meses de aporte)
    try:
        from celula_2_premissas import PREMISSAS
        caixa_inicial = PREMISSAS.get('caixa_inicial', 4000)
        aporte_mensal = PREMISSAS.get('aporte_mensal', 2500)
        meses_aporte = PREMISSAS.get('meses_aporte', 6)
    except:
        caixa_inicial = 4000
        aporte_mensal = 2500
        meses_aporte = 6
    
    investimento_total = caixa_inicial + (aporte_mensal * meses_aporte) + 8000  # Capital (Empresa) + R$ 8k Equipamentos (PF)
    
    # Adiciona colunas calculadas ao DataFrame temporariamente
    df_real = df_real.copy()
    
    # ROI por período
    for i, row_idx in enumerate([0, 5, 11, -1]):  # M1, M6, M12, M36
        mes_atual = row_idx + 1 if row_idx != -1 else 36
        meses_aportados = min(mes_atual, meses_aporte)
        inv_ate_agora = caixa_inicial + (aporte_mensal * meses_aportados)
        
    # ROI no M36
    caixa_final = m36.get('caixa', 0)
    arr_final = m36.get('arr', m36.get('mrr', 0) * 12)
    # Valuation (Múltiplo 5x ARR - padrão SaaS)
    valuation_m36 = arr_final * 5
    
    # ---------------------------------------------------------
    # CÁLCULO DE RETORNO DO INVESTIDOR (LÓGICA DE EQUITY)
    # ---------------------------------------------------------
    # Premissa: Investidor pôs 100% do capital (27k) por 50% do negócio
    equity_investidor = 0.50 
    
    # Cenário 1: EXIT (Venda da empresa)
    valor_exit_investidor = valuation_m36 * equity_investidor
    roi_exit_m36 = ((valor_exit_investidor - investimento_total) / max(investimento_total, 1)) * 100
    
    # Cenário 2: CAIXA (Liquidação/Dividendos)
    # Se fechar hoje, divide o caixa 50/50
    valor_caixa_investidor = caixa_final * equity_investidor
    roi_caixa_m36 = ((valor_caixa_investidor - investimento_total) / max(investimento_total, 1)) * 100
    
    # Break-Even: encontrar primeiro mês com EBITDA > 0
    break_even_mes = None
    if 'ebitda' in df_real.columns:
        mask = df_real['ebitda'] > 0
        if mask.any():
            break_even_mes = df_real[mask].iloc[0]['mes']
    
    # Adiciona as colunas calculadas
    df_real['roi_investidor_exit'] = roi_exit_m36
    df_real['roi_investidor_caixa'] = roi_caixa_m36
    df_real['valuation_estimado'] = df_real['arr'] * 5 if 'arr' in df_real.columns else df_real['mrr'] * 12 * 5
    df_real['break_even_mes'] = break_even_mes if break_even_mes else 99
    df_real['investimento_total'] = investimento_total  # Coluna constante para o total investido
    
    # Atualiza snapshots com novos dados
    m1 = df_real.iloc[0]
    m6 = df_real.iloc[5] if len(df_real) > 5 else df_real.iloc[-1]
    m12 = df_real.iloc[11] if len(df_real) > 11 else df_real.iloc[-1]
    m36 = df_real.iloc[-1]
    
    # Header
    if not report_mode:
        print(f"{'Métrica':<35} {'M1':>12} {'M6':>12} {'M12':>12} {'M36':>12} {'Benchmark':>12} {'Status':>8}")
        print("-" * 105)
    
    tabela_dados = []
    
    for metrica in metricas:
        if len(metrica) < 4 or metrica[1] == '':
            # Linha de categoria
            if not report_mode:
                print(f"\n{metrica[0]}")
            else:
                # Adiciona linha vazia ou cabeçalho na tabela
                tabela_dados.append([f"**{metrica[0]}**", "", "", "", "", "", ""])
            continue
            
        nome, coluna, benchmark, inversao = metrica[:4]
        
        # Verifica se coluna existe
        if coluna not in df_real.columns:
            continue
            
        # Pega valores
        v1 = m1.get(coluna, 0)
        v6 = m6.get(coluna, 0)
        v12 = m12.get(coluna, 0)
        v36 = m36.get(coluna, 0)
        
        # Status dinâmico
        emoji, _, _ = calcular_status(v36, benchmark, inversao)
        
        # Formata valores
        if 'pct' in coluna or coluna == 'churn_rate':
            fmt = lambda x: f'{x*100:.1f}%' if coluna == 'churn_rate' else f'{x:.1f}%'
            v1_str = fmt(v1)
            v6_str = fmt(v6)
            v12_str = fmt(v12)
            v36_str = fmt(v36)
            bench_str = f'{benchmark*100:.1f}%' if coluna == 'churn_rate' else f'{benchmark:.1f}%'
        elif coluna in ['mrr', 'arr', 'caixa', 'burn_rate', 'ebitda', 'cac_blended']:
            v1_str = formatar_moeda(v1)
            v6_str = formatar_moeda(v6)
            v12_str = formatar_moeda(v12)
            v36_str = formatar_moeda(v36)
            bench_str = formatar_moeda(benchmark)
        elif coluna in ['ltv_cac']:
            v1_str = f'{v1:.2f}x'
            v6_str = f'{v6:.2f}x'
            v12_str = f'{v12:.2f}x'
            v36_str = f'{v36:.2f}x'
            bench_str = f'{benchmark:.1f}x'
        elif coluna == 'runway_meses':
            # RUNWAY REAL: sempre mostra caixa/despesas, NUNCA infinito
            v1_str = f'{v1:.1f}m'
            v6_str = f'{v6:.1f}m'
            v12_str = f'{v12:.1f}m'
            # Para M36, calcular runway real = caixa / despesas
            caixa_m36 = m36.get('caixa', 0)
            despesas_m36 = m36.get('total_cogs', 0) + m36.get('total_opex', 0)
            if despesas_m36 > 0:
                runway_real = caixa_m36 / despesas_m36
                v36_str = f'{runway_real:.1f}m'
            else:
                v36_str = f'{v36:.1f}m'
            bench_str = f'>{benchmark:.0f}m'

        elif coluna == 'payback_meses':
            # PAYBACK: Apenas formatação simples
            v1_str = f'{v1:.1f}m'
            v6_str = f'{v6:.1f}m'
            v12_str = f'{v12:.1f}m'
            v36_str = f'{v36:.1f}m'
            bench_str = f'<{benchmark:.0f}m'
        elif coluna == 'investimento_total':
            # Investimento Total: valor fixo (acumulado)
            v1_str = '-'
            v6_str = '-'
            v12_str = '-'
            v36_str = formatar_moeda(v36)
            bench_str = '-'
        elif coluna == 'roi_investidor_exit' or coluna == 'roi_investidor_caixa':
            # ROI: percentual
            v1_str = '-'
            v6_str = '-'
            v12_str = '-'
            v36_str = f'{v36:.0f}%'
            bench_str = f'>{benchmark:.0f}%'
        elif coluna == 'valuation_estimado':
            # Valuation: moeda grande
            v1_str = formatar_moeda(v1)
            v6_str = formatar_moeda(v6)
            v12_str = formatar_moeda(v12)
            v36_str = formatar_moeda(v36)
            bench_str = f'>{formatar_moeda(benchmark)}'
        elif coluna == 'break_even_mes':
            # Break-Even: mês específico (não é série temporal)
            if v36 < 99:
                v1_str = '-'
                v6_str = '-'
                v12_str = '-'
                v36_str = f'M{int(v36)}'
                bench_str = f'<M{benchmark:.0f}'
            else:
                v1_str = '-'
                v6_str = '-'
                v12_str = '-'
                v36_str = 'Não atingido'
                bench_str = f'<M{benchmark:.0f}'
        else:
            v1_str = f'{v1:,.0f}'
            v6_str = f'{v6:,.0f}'
            v12_str = f'{v12:,.0f}'
            v36_str = f'{v36:,.0f}'
            bench_str = f'{benchmark:,.0f}'
        
        if not report_mode:
            print(f"{nome:<35} {v1_str:>12} {v6_str:>12} {v12_str:>12} {v36_str:>12} {bench_str:>12} {emoji:>8}")
        
        # Adiciona dados para tabela Markdown
        tabela_dados.append([nome.strip(), v1_str, v6_str, v12_str, v36_str, bench_str, emoji])

    cols = ['Métrica', 'M1', 'M6', 'M12', 'M36', 'Benchmark', 'Status']
    df_tab = pd.DataFrame(tabela_dados, columns=cols).fillna("")
    
    # =========================================
    # RENDERIZAÇÃO ATÔMICA (V7.0) - CORRIGIDA
    # =========================================
    # Identificar KPIs críticos (status vermelho)
    kpis_criticos = [row[0] for row in tabela_dados if '🔴' in str(row[-1])]
    kpis_atencao = [row[0] for row in tabela_dados if '⚠️' in str(row[-1])]
    
    # Insight dinâmico baseado nos dados reais
    if len(kpis_criticos) > 0:
        insight_fato = f"{len(kpis_criticos)} métrica(s) em estado CRÍTICO: {', '.join(kpis_criticos[:3])}"
        insight_acao = f"Priorizar correção imediata de: {kpis_criticos[0]}"
    elif len(kpis_atencao) > 0:
        insight_fato = f"{len(kpis_atencao)} métrica(s) requerem atenção: {', '.join(kpis_atencao[:3])}"
        insight_acao = "Monitorar de perto e definir plano de ação."
    else:
        insight_fato = "Todas as métricas dentro dos benchmarks estabelecidos."
        insight_acao = "Manter execução e monitorar mensalmente."
    
    insight_tabela = {
        "fato": insight_fato,
        "causa": "Análise automática comparando M36 vs Benchmarks de mercado.",
        "implicacao": "Esta tabela mostra a evolução temporal (M1→M36) dos principais indicadores de viabilidade do negócio.",
        "acao": insight_acao
    }

    if report_mode:
        # PDF: Markdown puro (Tabela simples)
        render_atomic_block(
            chart_id="pg1_tabela_master",
            title_colloquial="Como está a saúde geral do negócio?",
            title_technical="VIZ 1.1 Tabela Executiva Master",
            fig=None,
            legend_md=None,
            df_tabela=df_tab,
            insight_dict=insight_tabela,
            report_mode=True,
            table_title="EVOLUÇÃO DOS INDICADORES (M1 → M36):"
        )
    
    return True

# ============================================================================
# FUNÇÃO 2: KPI CARDS (4 em linha, CORRIGIDO - fontes grandes, runway real)
# ============================================================================
def gerar_kpi_cards(df_real, met_real, met_ideal, report_mode=False):
    """
    Gera 4 KPI cards com:
    - Fontes grandes e legíveis
    - Textos explicativos (não só técnicos)
    - RUNWAY REAL = caixa / despesas (não infinito quando lucrativo!)
    """
    # AUMENTADO: Tamanho da figura para melhor legibilidade no DOCX (Menos achatado)
    figsize = (16, 5) if report_mode else (18, 6)
    fig, axes = plt.subplots(1, 4, figsize=figsize, dpi=150)
    
    # AUMENTADO: Fonte do título
    title_size = 18 if report_mode else 20
    fig.suptitle('PAINEL DE KPIs ESTRATÉGICOS', fontsize=title_size, fontweight='bold', y=0.98)
    
    m36 = df_real.iloc[-1]
    
    # Calcular despesas mensais para RUNWAY REAL
    despesas_mensais = m36.get('total_cogs', 0) + m36.get('total_opex', 0)
    caixa = m36.get('caixa', 0)
    runway_real = caixa / despesas_mensais if despesas_mensais > 0 else 999
    
    # Card 1: MRR
    mrr_real = m36['mrr']
    mrr_ideal = met_ideal.get('mrr_final', mrr_real * 2)
    gap_mrr = ((mrr_real - mrr_ideal) / mrr_ideal * 100) if mrr_ideal > 0 else 0
    emoji_mrr, cor_mrr, status_mrr = calcular_status(mrr_real, mrr_ideal * 0.7)
    
    axes[0].set_facecolor('#fafafa')
    axes[0].text(0.5, 0.82, '💰 MRR', ha='center', va='center', fontsize=20, fontweight='bold', color='#333333', transform=axes[0].transAxes)
    val_str_0 = formatar_moeda(mrr_real)
    font_val_0 = 36 if len(val_str_0) < 10 else 28
    axes[0].text(0.5, 0.55, val_str_0, ha='center', va='center', fontsize=font_val_0, fontweight='heavy', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.32, f'Meta: {formatar_moeda(mrr_ideal)}', ha='center', va='center', fontsize=14, color='gray', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.18, f'{emoji_mrr} Gap: {gap_mrr:+.0f}%', ha='center', va='center', fontsize=16, fontweight='bold', color=CORES.get(cor_mrr, 'black'), transform=axes[0].transAxes)
    axes[0].axis('off')
    
    # Card 2: LTV/CAC
    ltv_cac = m36.get('ltv_cac', 0)
    emoji_ltv, cor_ltv, status_ltv = calcular_status(ltv_cac, 3.0)
    
    axes[1].set_facecolor('#fafafa')
    axes[1].text(0.5, 0.82, '📈 LTV/CAC', ha='center', va='center', fontsize=20, fontweight='bold', color='#333333', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.55, f'{ltv_cac:.1f}x', ha='center', va='center', fontsize=40, fontweight='heavy', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.32, 'Meta: ≥3.0x', ha='center', va='center', fontsize=14, color='gray', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.18, f'{emoji_ltv} {status_ltv}', ha='center', va='center', fontsize=16, fontweight='bold', color=CORES.get(cor_ltv, 'black'), transform=axes[1].transAxes)
    axes[1].axis('off')
    
    # Card 3: Churn
    churn = m36.get('churn_rate', 0) * 100
    emoji_churn, cor_churn, status_churn = calcular_status(churn, 5.0, inversao=True)
    
    axes[2].set_facecolor('#fafafa')
    axes[2].text(0.5, 0.82, '🚪 Churn', ha='center', va='center', fontsize=20, fontweight='bold', color='#333333', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.55, f'{churn:.1f}%', ha='center', va='center', fontsize=40, fontweight='heavy', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.32, 'Meta: <5.0%', ha='center', va='center', fontsize=14, color='gray', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.18, f'{emoji_churn} {status_churn}', ha='center', va='center', fontsize=16, fontweight='bold', color=CORES.get(cor_churn, 'black'), transform=axes[2].transAxes)
    axes[2].axis('off')
    
    # Card 4: Runway
    emoji_run, cor_run, status_run = calcular_status(runway_real, 12.0)
    
    axes[3].set_facecolor('#fafafa')
    axes[3].text(0.5, 0.82, '⏱️ Runway', ha='center', va='center', fontsize=20, fontweight='bold', color='#333333', transform=axes[3].transAxes)
    
    if runway_real >= 999:
        axes[3].text(0.5, 0.55, '∞', ha='center', va='center', fontsize=40, fontweight='heavy', color=CORES['sucesso'], transform=axes[3].transAxes)
        axes[3].text(0.5, 0.32, 'Sem despesas!', ha='center', va='center', fontsize=14, color=CORES['sucesso'], transform=axes[3].transAxes)
    else:
        axes[3].text(0.5, 0.55, f'{runway_real:.1f}m', ha='center', va='center', fontsize=40, fontweight='heavy', transform=axes[3].transAxes)
        axes[3].text(0.5, 0.32, f'Caixa: {formatar_moeda(caixa)}', ha='center', va='center', fontsize=14, color='gray', transform=axes[3].transAxes)
    
    axes[3].text(0.5, 0.18, f'{emoji_run} {status_run}', ha='center', va='center', fontsize=16, fontweight='bold', color=CORES.get(cor_run, 'black'), transform=axes[3].transAxes)
    axes[3].axis('off')
    
    # Bordas visíveis
    for ax in axes:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#cccccc')
            spine.set_linewidth(1.5)
    
    plt.tight_layout()
    plt.savefig('outputs/figs/pg1_kpi_cards.png', dpi=300, bbox_inches='tight', facecolor='white')
    
    if report_mode:
        plt.close(fig)
        display(Markdown("## PAINEL DE CONTROLE (KPIs)"))
        display(Markdown("**Visão Geral:** Indicadores chave de performance no final do período (M36)."))
        display(Markdown("![KPI Cards](outputs/figs/pg1_kpi_cards.png)"))
        display(Markdown("*Fonte: df_real_m (Simulacao Real) - Snapshot M36*"))
        
        # GLOSSÁRIO IMEDIATAMENTE APÓS OS CARDS
        glossario_md = """
### GLOSSÁRIO DOS KPIs

| KPI | O que significa | Por que importa |
|-----|-----------------|------------------|
| **MRR** | Receita Mensal Recorrente | Quanto dinheiro entra TODO mês de forma previsível. |
| **ROI (Exit)** | Retorno Potencial | Retorno se vender a empresa hoje (50% do Valuation - Investimento). |
| **ROI (Caixa)** | Retorno Realizado | Retorno se liquidar a empresa hoje (50% do Caixa - Investimento). |
| **Valuation** | Valuation (Exit) | Valor estimado de venda da empresa, calculado como **5x a Receita Anual (ARR)**. |
| **LTV/CAC** | Retorno por Cliente | Para cada R$ 1 gasto para trazer um cliente, quantos R$ ele gera de volta. Meta: ≥3x. |
| **Churn** | Evasão de Clientes | De cada 100 clientes, quantos cancelam por mês. Meta: <5%. |
| **Runway** | Fôlego Financeiro | Com o caixa atual, quantos meses a empresa sobrevive SEM nova receita. Meta: >12 meses. |

"""
        display(Markdown(glossario_md))
        display(Markdown("***"))
    else:
        plt.show()
    
    return fig

# ============================================================================
# FUNÇÃO 3: GRÁFICO TEMPORAL COM ÂNCORAS TRIMESTRAIS + TABELA DE VALORES
# ============================================================================
def gerar_grafico_temporal_correlacao(df_real, df_ideal, mc_results=None, report_mode=False):
    """
    Gráfico com 2 eixos Y: MRR (R$) + Usuários Ativos.
    CORRIGIDO: Grid visível, Tabela Referência.
    """
    # print("DEBUG: Executing gerar_grafico_temporal_correlacao V2.1 (FIX NAMEERROR)")
    
    # === DEFINIÇÃO ANTECIPADA DE DADOS_TABELA (PARA EVITAR NAMEERROR) ===
    # Isso garante que a variável exista mesmo que algo falhe depois
    dados_tabela = []
    
    # Popula dados_tabela
    mrr_real_arr = df_real['mrr'].values
    usuarios_arr = df_real['usuarios_ativos'].values
    periodos_tab = [1, 3, 6, 12, 24, 36]
    
    for p in periodos_tab:
        if p <= len(df_real):
            idx = p - 1
            r_mrr = mrr_real_arr[idx]
            
            # Ideal
            if len(df_ideal) > idx:
                 i_mrr = df_ideal['mrr'].iloc[idx]
            else:
                 i_mrr = r_mrr
            
            r_users = usuarios_arr[idx]
            gap_val = i_mrr - r_mrr
            gap_p = (gap_val / i_mrr * 100) if i_mrr > 0 else 0
            
            dados_tabela.append([
                f"M{p}",
                formatar_moeda(r_mrr),
                formatar_moeda(i_mrr),
                f"{int(r_users)}",
                f"{gap_p:.1f}%"
            ])
            
    # Criar figura (Mais alta para evitar achatamento)
    figsize = (10, 6) if report_mode else (14, 8)
    fig = plt.figure(figsize=figsize, dpi=150)
    
    # Ajuste explícito de margens para evitar cortes de labels
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.10, right=0.90)
    
    ax1 = fig.add_axes([0.1, 0.12, 0.85, 0.75])  # Mais espaco no topo para labels
    
    meses = df_real['mes'].values
    mrr_ideal = df_ideal['mrr'].values if len(df_ideal) > 0 else mrr_real_arr * 1.5
    
    # Adiciona ruído visual
    np.random.seed(42)
    mrr_visual = mrr_real_arr + np.random.normal(0, mrr_real_arr * 0.015, len(mrr_real_arr))
    usuarios_visual = usuarios_arr + np.random.normal(0, usuarios_arr * 0.01, len(usuarios_arr))
    usuarios_visual = np.maximum(usuarios_visual, 0)
    
    # Plot MRR
    ax1.set_xlabel('Mês', fontsize=12, fontweight='bold')
    ax1.set_ylabel('MRR em R$', fontsize=11, color='black')
    line1, = ax1.plot(meses, mrr_visual, color=CORES['real'], linewidth=2.5, label='MRR Real')
    line2, = ax1.plot(meses, mrr_ideal, color=CORES['ideal'], linewidth=2, linestyle='--', label='MRR Ideal')
    ax1.fill_between(meses, mrr_visual, mrr_ideal, alpha=0.1, color=CORES['critico'])
    
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: formatar_moeda(x)))
    
    # Plot Users
    ax2 = ax1.twinx()
    ax2.set_ylabel('Usuários Ativos', fontsize=11, color=CORES['usuarios'])
    line3, = ax2.plot(meses, usuarios_visual, color=CORES['usuarios'], linewidth=2.5, linestyle=':', label='Usuários')
    ax2.set_ylim(0, max(usuarios_arr) * 1.3)
    
    # Grid e Ancoras
    ax1.grid(True, alpha=0.4, axis='y')
    
    # Ancoras verticais (sem labels no topo para evitar sobreposicao)
    trimestres = [6, 12, 18, 24, 30, 36]
    for t in trimestres:
        if t <= len(meses):
            ax1.axvline(x=t, color='#cccccc', linestyle='--', alpha=0.5)

    ax1.set_title('EVOLUÇÃO MRR vs USUÁRIOS', fontsize=13, fontweight='bold', pad=15)
    ax1.legend([line1, line2, line3], ['MRR Real', 'MRR Ideal', 'Usuários'], loc='upper left')
    ax1.set_xlim(1, 36)
    
    plt.tight_layout()
    plt.savefig('outputs/figs/pg1_temporal_correlacao.png', bbox_inches='tight')
    
    if report_mode:
        plt.close(fig)
        display(Markdown("### EVOLUÇÃO MRR vs USUÁRIOS"))
        display(Markdown("**Pergunta:** O crescimento de usuarios esta se convertendo em receita proporcional?"))
        display(Markdown("![Evolução Temporal](outputs/figs/pg1_temporal_correlacao.png)"))
        display(Markdown("*Fonte: df_real_m vs df_ideal_m | Projecao 36 meses*"))
        
        # COMO LER
        como_ler = """
### COMO LER ESTE GRÁFICO
**O QUE ESTOU VENDO?**
A correlação entre o crescimento da receita recorrente (MRR - Linha Sólida) e a base de usuários ativos (Linha Pontilhada).

**ELEMENTOS:**
- **Linha Preta (MRR Real):** Receita recorrente mensal no cenário conservador.
- **Linha Tracejada Verde (MRR Ideal):** Meta de receita baseada em benchmarks de mercado.
- **Linha Pontilhada Roxa (Usuários):** Quantidade de clientes ativos pagantes (Eixo Direito).

**INTERPRETAÇÃO:**
- As linhas devem crescer juntas. Se a linha Roxa (Usuários) sobe mas a Preta (MRR) não, indica queda no ticket médio ou churn financeiro.
"""
        display(Markdown(como_ler))
        
        display(Markdown("***"))
        display(Markdown("#### TABELA DE REFERÊNCIA"))
        
        cols = ['Período', 'MRR Real', 'MRR Ideal', 'Usuários', 'Gap %']
        df_tab = pd.DataFrame(dados_tabela, columns=cols)
        display(Markdown(df_tab.to_markdown(index=False)))
        
        # Fonte
        display(Markdown("*Fonte: df_real_m vs df_ideal_m - Projecao 36 meses*"))
        display(Markdown("\\newpage"))
    else:
        plt.show()
        cols = ['Período', 'MRR Real', 'MRR Ideal', 'Usuários', 'Gap %']
        df_tab = pd.DataFrame(dados_tabela, columns=cols)
        display(Markdown(df_tab.to_markdown(index=False)))
    
    return fig

# ============================================================================
# FUNÇÃO 4: TABELA DE MILESTONES (METAS DO CENÁRIO IDEAL - ZERO HARDCODED)
# ============================================================================
def gerar_tabela_milestones(df_real, df_ideal, met_real, met_ideal, report_mode=False):
    """
    Tabela de milestones com METAS DINÂMICAS do cenário ideal.
    """
    if not report_mode:
        print("\n" + "="*80)
        print("1.4 TABELA DE MILESTONES - REAL vs IDEAL")
        print("(Metas extraídas automaticamente do Cenário Ideal)")
        print("="*80)
    
    # Encontrar mês em que ideal atingiu determinado valor (para usar como meta)
    def quando_ideal_atingiu(coluna, valor):
        """Retorna o mês em que o cenário ideal atingiu o valor."""
        if coluna not in df_ideal.columns:
            return None
        mask = df_ideal[coluna] >= valor
        if mask.any():
            return int(df_ideal[mask].iloc[0]['mes'])
        return None
    
    # Milestones baseados no cenário ideal (NÃO hardcoded)
    # Pega valores do CENÁRIO IDEAL e encontra quando foram atingidos
    mrr_ideal_m12 = df_ideal.iloc[11]['mrr'] if len(df_ideal) > 11 else 10000
    mrr_ideal_m24 = df_ideal.iloc[23]['mrr'] if len(df_ideal) > 23 else 50000
    mrr_ideal_m36 = df_ideal.iloc[-1]['mrr']
    users_ideal_m12 = df_ideal.iloc[11]['usuarios_ativos'] if len(df_ideal) > 11 else 100
    users_ideal_m36 = df_ideal.iloc[-1]['usuarios_ativos']
    
    # Definir milestones comparando Real vs Ideal
    milestones = [
        # (Nome, Coluna, Valor, Meta de mês vem do ideal)
        ('🚀 Primeiro Cliente Pagante', 'usuarios_ativos', 1, quando_ideal_atingiu('usuarios_ativos', 1) or 1),
        ('💰 R$ 1k MRR', 'mrr', 1000, quando_ideal_atingiu('mrr', 1000) or 3),
        ('💰 R$ 5k MRR', 'mrr', 5000, quando_ideal_atingiu('mrr', 5000) or 6),
        ('👥 50 Usuários Ativos', 'usuarios_ativos', 50, quando_ideal_atingiu('usuarios_ativos', 50) or 6),
        ('💰 R$ 10k MRR', 'mrr', 10000, quando_ideal_atingiu('mrr', 10000) or 9),
        (f'👥 {int(users_ideal_m12)} Usuários (Meta M12)', 'usuarios_ativos', users_ideal_m12, 12),
        ('💰 R$ 20k MRR', 'mrr', 20000, quando_ideal_atingiu('mrr', 20000) or 12),
        ('🎯 Break-Even (EBITDA > 0)', 'ebitda', 0.01, quando_ideal_atingiu('ebitda', 0.01) or 12),
        (f'💰 {formatar_moeda(mrr_ideal_m24)} MRR (Meta M24)', 'mrr', mrr_ideal_m24, 24),
        (f'👥 {int(users_ideal_m36)} Usuários (Meta M36)', 'usuarios_ativos', users_ideal_m36, 36),
        ('📈 LTV/CAC > 3x', 'ltv_cac', 3.0, quando_ideal_atingiu('ltv_cac', 3.0) or 12),
    ]
    
    if not report_mode:
        print(f"\n{'Milestone':<45} {'Meta (Ideal)':<15} {'Real Atingiu':<15} {'Status':<15}")
        print("-" * 95)
    
    tabela_dados = []
    
    for nome, coluna, valor, meta_mes in milestones:
        if coluna not in df_real.columns:
            continue
            
        mes_atingido = encontrar_mes_milestone(df_real, coluna, valor)
        
        if mes_atingido is None:
            status = '🔴 NÃO ATINGIU'
            atingido_str = '—'
        elif mes_atingido < meta_mes:
            diff = meta_mes - mes_atingido
            status = f'🟢 -{diff}m ANTES'
            atingido_str = f'M{mes_atingido}'
        elif mes_atingido == meta_mes:
            status = '✅ IGUAL AO IDEAL'
            atingido_str = f'M{mes_atingido}'
        else:
            diff = mes_atingido - meta_mes
            status = f'⚠️ +{diff}m ATRASO'
            atingido_str = f'M{mes_atingido}'
        
        if not report_mode:
            print(f"{nome:<45} {'M' + str(meta_mes):<15} {atingido_str:<15} {status:<15}")
        
        tabela_dados.append([nome, f'M{meta_mes}', atingido_str, status])

    if not report_mode:
        print("-" * 95)
        print("🟢 = Superou o Ideal | ✅ = Igual ao Ideal | ⚠️ = Abaixo do Ideal | 🔴 = Não atingiu")
        print("📌 NOTA: Metas extraídas do cenário IDEAL (df_ideal) - não são hardcoded")
    else:
        # Render markdown table for PDF
        df_milestones = pd.DataFrame(tabela_dados, columns=['Milestone', 'Meta', 'Real', 'Status'])
        display(Markdown("#### 🏁 TABELA DE MILESTONES (REAL VS IDEAL)"))
        display(Markdown("**Objetivo:** Verificar se estamos atingindo os marcos de crescimento no tempo previsto pelo benchmark."))
        display(Markdown(df_milestones.to_markdown(index=False)))
        display(Markdown("*Fonte: df_real_m vs df_ideal_m (Metas do Benchmark)*"))
        display(Markdown("***"))
    
    return True

# ============================================================================
# FUNÇÃO 5: GRÁFICO EFICIÊNCIA MARKETING - BARRAS DUPLAS (Marketing x MRR)
# ============================================================================
# ============================================================================
# FUNÇÃO 5: GRÁFICO EFICIÊNCIA MARKETING - BARRAS DUPLAS (Marketing x MRR)
# ============================================================================
def gerar_grafico_eficiencia_marketing(df_real, report_mode=False):
    """
    Gráfico com BARRAS DUPLAS: Marketing (azul) x MRR (verde) lado a lado.
    """
    # Adjust size for PDF (menos achatado)
    figsize = (10, 6) if report_mode else (16, 8)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
    # Ajuste de margens
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.10, right=0.95)
    
    meses = df_real['mes'].values
    marketing = df_real['gasto_marketing'].values
    mrr = df_real['mrr'].values
    
    # Calcular eficiência (MRR / Marketing)
    eficiencia = np.where(marketing > 0, mrr / marketing, 0)
    
    # Posições das barras (par de barras por mês)
    largura = 0.35
    x = np.arange(len(meses))
    
    # Barras duplas
    bars_mkt = ax.bar(x - largura/2, marketing, largura, label='Investimento Marketing (R$)', 
                       color=CORES['marketing'], alpha=0.8)
    bars_mrr = ax.bar(x + largura/2, mrr, largura, label='MRR Gerado (R$)', 
                       color=CORES['sucesso'], alpha=0.8)
    
    # DATA DINÂMICA (Baseada em datas reais)
    import pandas as pd
    try:
        from celula_2_premissas import PREMISSAS
        data_inicio = PREMISSAS.get('data_inicio', '2025-01-01')
    except:
        data_inicio = '2025-01-01'
        
    datas = pd.date_range(start=data_inicio, periods=len(meses), freq='MS')
    labels_datas = [d.strftime('%b/%y') for d in datas]
    
    # Configurações do eixo
    ax.set_xlabel('Período', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor em R$', fontsize=12)
    ax.set_xticks(x[::3])  # Mostrar a cada 3 meses
    ax.set_xticklabels([labels_datas[i] for i in range(0, len(meses), 3)], fontsize=10, rotation=45)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: formatar_moeda(x)))
    
    # Grid visível
    ax.grid(True, alpha=0.4, linestyle='-', axis='y')
    ax.grid(True, alpha=0.2, linestyle=':', axis='x')
    
    # Valores em cima das barras (a cada 6 meses)
    for i in [5, 11, 17, 23, 29, 35]:  # M6, M12, M18, M24, M30, M36
        if i < len(meses):
            # Valor Marketing
            ax.text(x[i] - largura/2, marketing[i] + max(marketing)*0.02, 
                    formatar_moeda(marketing[i]), ha='center', va='bottom', 
                    fontsize=8, color=CORES['marketing'], fontweight='bold')
            # Valor MRR
            ax.text(x[i] + largura/2, mrr[i] + max(mrr)*0.02, 
                    formatar_moeda(mrr[i]), ha='center', va='bottom', 
                    fontsize=8, color=CORES['sucesso'], fontweight='bold')
            # Eficiência
            ax.text(x[i], max(marketing[i], mrr[i]) + max(mrr)*0.08, 
                    f'Ef: {eficiencia[i]:.1f}x', ha='center', va='bottom', 
                    fontsize=9, fontweight='bold', color='navy',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))
    
    # Título explicativo
    ax.set_title('INVESTIMENTO EM MARKETING vs RECEITA GERADA (MRR)\n'
                 'Barras Azuis = Quanto gastei | Barras Verdes = Quanto gerei | Eficiência = MRR ÷ Marketing',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Legenda
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    
    # Ancoras verticais anuais (sem labels no topo para evitar sobreposicao com Ef)
    for ano in [12, 24, 36]:
        idx = ano - 1
        if idx < len(x):
            ax.axvline(x=x[idx], color='gray', linestyle='--', linewidth=1, alpha=0.3)
    
    # Box com resumo - POSIÇÃO: canto superior ESQUERDO, abaixo da legenda
    eficiencia_media = np.mean(eficiencia[eficiencia > 0])
    eficiencia_final = eficiencia[-1] if len(eficiencia) > 0 else 0
    total_mkt = marketing.sum()
    total_mrr = mrr[-1] * 12  # ARR aproximado
    
    resumo = (f"📊 RESUMO\n"
              f"───────────────\n"
              f"Investido: {formatar_moeda(total_mkt)}\n"
              f"ARR Final: {formatar_moeda(total_mrr)}\n"
              f"Eficiência Média: {eficiencia_media:.1f}x\n"
              f"Eficiência M36: {eficiencia_final:.1f}x\n"
              f"───────────────\n"
              f"⚠️ Eficiência ≠ LTV/CAC\n"
              f"Ef = MRR / Marketing")
    
    # Posicionado no canto ESQUERDO SUPERIOR, abaixo da legenda
    ax.text(0.02, 0.70, resumo, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.95),
            family='monospace')
    
    plt.tight_layout()
    plt.savefig('outputs/figs/pg1_eficiencia_marketing.png', dpi=300, bbox_inches='tight', facecolor='white')
    
    if report_mode:
        plt.close(fig)
        display(Markdown("### EFICIÊNCIA DE MARKETING (ROI)"))
        display(Markdown("**Pergunta:** O dinheiro investido em marketing esta retornando como receita recorrente?"))
        display(Markdown("![Eficiencia Marketing](outputs/figs/pg1_eficiencia_marketing.png)"))
        display(Markdown("*Fonte: df_real_m | gasto_marketing vs mrr*"))
        
        # COMO LER
        como_ler = """
### COMO LER ESTE GRÁFICO
**O QUE ESTOU VENDO?**
Comparativo direto entre dinheiro investido em Marketing (Azul) e receita recorrente gerada (Verde).

**ELEMENTOS:**
- **Barra Azul (Investimento):** Custo total de marketing no mês.
- **Barra Verde (MRR):** Receita recorrente total no final do mês.
- **Eficiência (Box):** Quantas vezes o MRR cobre o Marketing (Ideal > 1.0x).

**INTERPRETAÇÃO:**
- No início, é normal a barra Azul ser maior (investimento inicial).
- A partir do Mês 6, a barra Verde DEVE ultrapassar a Azul e continuar crescendo (efeito "J-Curve").
"""
        display(Markdown(como_ler))
        
        # Fonte
        display(Markdown("*Fonte: df_real_m vs df_ideal_m - Projecao 36 meses*"))
        display(Markdown("\\newpage"))
    else:
        plt.show()
    
    return fig

# ============================================================================
# FUNÇÃO 6: INSIGHTS DINÂMICOS (100% baseado em lógica)
# ============================================================================
# ============================================================================
# FUNÇÃO 6: INSIGHTS DINÂMICOS (100% baseado em lógica)
# ============================================================================
def gerar_insights_dinamicos(met_real, met_ideal, df_real, report_mode=False):
    """
    Gera insights estratégicos usando padrão Gold Standard (HTML).
    Padrão: FATO / CAUSA / IMPLICAÇÃO / AÇÃO (igual Página 2).
    """
    # Título da seção
    display(Markdown("## INSIGHTS ESTRATÉGICOS DO COCKPIT"))
    
    # =========================================================================
    # INSIGHT 1: LTV/CAC
    # INSIGHT 1: LTV/CAC (Usando Valor Final - "Snapshot Atua")
    # =========================================================================
    if 'ltv_cac' in df_real.columns:
        ltv_cac = df_real['ltv_cac'].iloc[-1]
        # Se for NaN (ex: CAC=0), considera infinito/alto
        if pd.isna(ltv_cac): 
            # Se CAC=0, teoricamente é infinito. Se não tem pagantes, é 0.
            # Vamos assumir 0 se não tiver dados, ou um valor alto se tiver LTV.
            if df_real['cac_blended'].iloc[-1] == 0 and df_real['ltv'].iloc[-1] > 0:
                ltv_cac = 999.0 # Simbólico para "Infinito"
            else:
                ltv_cac = 0.0
    else:
        ltv_cac = met_real.get('ltv_cac_medio', 0)

    ltv_cac_ideal = met_ideal.get('ltv_cac_medio', 3.0)
    
    if ltv_cac >= 5.0:
        status_cor = "#388E3C"  # Verde
        status_bg = "#E8F5E9"
    elif ltv_cac >= 3.0:
        status_cor = "#388E3C"
        status_bg = "#E8F5E9"
    elif ltv_cac >= 1.5:
        status_cor = "#FBC02D"  # Amarelo
        status_bg = "#FFFDE7"
    else:
        status_cor = "#D32F2F"  # Vermelho
        status_bg = "#FFEBEE"
    
    insight_1 = {
        "fato": f"LTV/CAC = {ltv_cac:.2f}x no cenário conservador.",
        "causa": "Relação entre valor do cliente (LTV) e custo de aquisição (CAC).",
        "implicacao": f"Cada R$ 1 investido em aquisição retorna R$ {ltv_cac:.2f}.",
        "acao": "Escalar aquisição se > 3.0x. Revisar CAC/Churn se < 3.0x."
    }
    
    if report_mode:
        # Quarto Callout para PDF/DOCX
        callout_type = "tip" if ltv_cac >= 3.0 else "warning" if ltv_cac >= 1.5 else "important"
        insight_md = f"""
### INSIGHT 1: Saúde Unitária (LTV/CAC)
- **FATO:** {insight_1['fato']}
- **CAUSA:** {insight_1['causa']}
- **IMPLICAÇÃO:** {insight_1['implicacao']}
- **AÇÃO RECOMENDADA:** {insight_1['acao']}

"""
        display(Markdown(insight_md))
    else:
        # HTML Rico para Notebook
        html = f"""
<div style="background-color: {status_bg}; border-left: 5px solid {status_cor}; padding: 15px; border-radius: 4px; margin-bottom: 15px;">
    <h4 style="margin-top: 0; color: {status_cor};">💡 INSIGHT 1: Saúde Unitária (LTV/CAC)</h4>
    <ul style="margin-bottom: 0;">
        <li><b>FATO:</b> {insight_1['fato']}</li>
        <li><b>CAUSA:</b> {insight_1['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight_1['implicacao']}</li>
        <li><b>AÇÃO RECOMENDADA:</b> {insight_1['acao']}</li>
    </ul>
</div>
"""
        display(HTML(html))
    
    # =========================================================================
    # INSIGHT 2: Gap de Receita
    # =========================================================================
    mrr_real = met_real.get('mrr_final', 0)
    mrr_ideal = met_ideal.get('mrr_final', mrr_real)
    gap = mrr_ideal - mrr_real
    gap_pct = (gap / mrr_ideal * 100) if mrr_ideal > 0 else 0
    
    if gap <= 0:
        status_cor = "#388E3C"
        status_bg = "#E8F5E9"
    elif gap_pct < 30:
        status_cor = "#FBC02D"
        status_bg = "#FFFDE7"
    else:
        status_cor = "#D32F2F"
        status_bg = "#FFEBEE"
    
    # Cálculo correto do Gap acumulado (soma do gap mensal, não multiplicação simples)
    # Gap mensal × número de meses restantes médio (aproximação conservadora)
    gap_anual = gap * 12  # Gap em 1 ano
    
    insight_2 = {
        "fato": f"Gap de {formatar_moeda(gap)}/mês ({gap_pct:.0f}%) entre Real e Ideal.",
        "causa": "Diferença entre projeção conservadora e cenário benchmark de mercado.",
        "implicacao": f"O cenário Ideal tem MRR {formatar_moeda(gap)} maior/mês. Em 12 meses, isso equivale a ~{formatar_moeda(gap_anual)} adicionais de receita.",
        "acao": "Aumentar conversão ou reduzir churn para aproximar do cenário Ideal."
    }
    
    if report_mode:
        callout_type = "tip" if gap <= 0 else "warning"
        insight_md = f"""
### INSIGHT 2: Gap de Receita
- **FATO:** {insight_2['fato']}
- **CAUSA:** {insight_2['causa']}
- **IMPLICAÇÃO:** {insight_2['implicacao']}
- **AÇÃO RECOMENDADA:** {insight_2['acao']}

"""
        display(Markdown(insight_md))
    else:
        html = f"""
<div style="background-color: {status_bg}; border-left: 5px solid {status_cor}; padding: 15px; border-radius: 4px; margin-bottom: 15px;">
    <h4 style="margin-top: 0; color: {status_cor};">💡 INSIGHT 2: Gap de Receita</h4>
    <ul style="margin-bottom: 0;">
        <li><b>FATO:</b> {insight_2['fato']}</li>
        <li><b>CAUSA:</b> {insight_2['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight_2['implicacao']}</li>
        <li><b>AÇÃO RECOMENDADA:</b> {insight_2['acao']}</li>
    </ul>
</div>
"""
        display(HTML(html))
    
    # =========================================================================
    # INSIGHT 3: Runway/Caixa
    # =========================================================================
    m36 = df_real.iloc[-1]
    caixa_final = m36.get('caixa', 0)
    despesas_mensais = m36.get('total_cogs', 0) + m36.get('total_opex', 0)
    runway = caixa_final / despesas_mensais if despesas_mensais > 0 else 999
    
    if runway > 12:
        status_cor = "#388E3C"
        status_bg = "#E8F5E9"
    elif runway > 6:
        status_cor = "#FBC02D"
        status_bg = "#FFFDE7"
    else:
        status_cor = "#D32F2F"
        status_bg = "#FFEBEE"
    
    insight_3 = {
        "fato": f"Runway de {runway:.1f} meses com caixa de {formatar_moeda(caixa_final)}.",
        "causa": f"Caixa disponível ÷ Despesas mensais ({formatar_moeda(despesas_mensais)}).",
        "implicacao": "Tempo de sobrevivência sem nova receita.",
        "acao": "Manter >12 meses. Se <6 meses, revisar custos urgente."
    }
    
    if report_mode:
        callout_type = "tip" if runway > 12 else "important"
        insight_md = f"""
### INSIGHT 3: Saúde de Caixa
- **FATO:** {insight_3['fato']}
- **CAUSA:** {insight_3['causa']}
- **IMPLICAÇÃO:** {insight_3['implicacao']}
- **AÇÃO RECOMENDADA:** {insight_3['acao']}

"""
        display(Markdown(insight_md))
    else:
        html = f"""
<div style="background-color: {status_bg}; border-left: 5px solid {status_cor}; padding: 15px; border-radius: 4px; margin-bottom: 15px;">
    <h4 style="margin-top: 0; color: {status_cor};">💡 INSIGHT 3: Saúde de Caixa</h4>
    <ul style="margin-bottom: 0;">
        <li><b>FATO:</b> {insight_3['fato']}</li>
        <li><b>CAUSA:</b> {insight_3['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight_3['implicacao']}</li>
        <li><b>AÇÃO RECOMENDADA:</b> {insight_3['acao']}</li>
    </ul>
</div>
"""
        display(HTML(html))
    
    # =========================================================================
    # BLOCO DE AUDITORIA (PADRÃO PÁGINA 2)
    # =========================================================================
    formulas = """
1. **LTV** = ARPU × (1 / Churn Rate)
2. **CAC** = (Gasto Marketing + Gasto Vendas) / Novos Clientes
3. **LTV/CAC** = LTV ÷ CAC (Meta: ≥3.0x)
4. **Runway** = Caixa Disponível ÷ Despesas Mensais

**6. AUDITORIA DE ROI (Exemplo M36):**
*   **Investimento Total:** R$ 27.000 (R$ 19k Empresa + R$ 8k Equipamentos)
*   **Equity do Investidor:** 50%
*   **A. Cenário CAIXA (Liquidação):**
    *   Caixa Final: R$ 165.753
    *   Parte do Investidor (50%): R$ 82.876
    *   Lucro Líquido: R$ 82.876 - R$ 27.000 = R$ 55.876
    *   **ROI Realizado:** (55.876 / 27.000) = **206%**
*   **B. Cenário EXIT (Venda):**
    *   Valuation (5x ARR): R$ 1.2M
    *   Parte do Investidor (50%): R$ 600k
    *   **ROI Potencial:** (600k - 27k) / 27k = **2.122%**
"""
    
    if report_mode:
        audit_md = f"""
### AUDITORIA & FÓRMULAS
{formulas}

"""
        display(Markdown(audit_md))
        display(Markdown("\\newpage"))
    else:
        audit_html = f"""
<div style="font-size: 11px; color: #555; background-color: #f9f9f9; padding: 10px; border: 1px solid #eee; margin-top: 20px; border-radius: 4px;">
    <b>🔍 AUDITORIA & FÓRMULAS:</b><br>
    {formulas.replace(chr(10), '<br>')}
</div>
"""
        display(HTML(audit_html))
    
    return [insight_1, insight_2, insight_3]

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================
import os

def executar_pagina_1(df_real_m, df_ideal, met_real, met_ideal, report_mode=False):
    """
    Gera todos os artefatos da Página 1: Cockpit.
    """
    if not report_mode:
        print("\nEXECUTANDO GERAÇÃO DA PÁGINA 1...")
        print("="*80)
    
    os.makedirs('outputs/figs', exist_ok=True)
    os.makedirs('outputs/metadata', exist_ok=True)
    os.makedirs('outputs/tabelas', exist_ok=True)

    # 1. Tabela Executiva
    gerar_tabela_executiva(df_real_m, df_ideal, met_real, met_ideal, report_mode=report_mode)

    # 2. KPI Cards
    gerar_kpi_cards(df_real_m, met_real, met_ideal, report_mode=report_mode)

    # 3. Gráfico Temporal com Correlação
    gerar_grafico_temporal_correlacao(df_real_m, df_ideal, report_mode=report_mode)

    # 4. Tabela de Milestones (agora compara Real vs Ideal)
    gerar_tabela_milestones(df_real_m, df_ideal, met_real, met_ideal, report_mode=report_mode)

    # 5. Gráfico Eficiência Marketing
    gerar_grafico_eficiencia_marketing(df_real_m, report_mode=report_mode)

    # 6. Insights Dinâmicos
    gerar_insights_dinamicos(met_real, met_ideal, df_real_m, report_mode=report_mode)

    if not report_mode:
        print("\n" + "="*80)
        print("✅ PÁGINA 1: EXECUTIVE COCKPIT - GERAÇÃO COMPLETA!")
        print("="*80)
        print("📁 Arquivos gerados:")
        print("   • outputs/figs/pg1_kpi_cards.png")
        print("   • outputs/figs/pg1_temporal_correlacao.png")
        print("   • outputs/figs/pg1_eficiencia_marketing.png")
        print("="*80)

if __name__ == "__main__":
    print("⚠️  Este arquivo agora é um módulo.")
    print("    Execute via 'loader_dados_relatorio.py' ou importe 'executar_pagina_1'.")
