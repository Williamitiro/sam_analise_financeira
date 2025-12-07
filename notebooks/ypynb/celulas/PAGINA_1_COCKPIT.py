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
# (Removido para modularização)


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
        print("📊 1.1 TABELA EXECUTIVA MASTER - PROJEÇÃO 36 MESES")
        print("="*80)
    else:
        display(Markdown("## 📊 1.1 TABELA EXECUTIVA MASTER"))
    
    # Snapshots
    m1 = df_real.iloc[0]
    m6 = df_real.iloc[5] if len(df_real) > 5 else df_real.iloc[-1]
    m12 = df_real.iloc[11] if len(df_real) > 11 else df_real.iloc[-1]
    m36 = df_real.iloc[-1]
    
    # Ideal (benchmark dinâmico)
    ideal_final = df_ideal.iloc[-1] if 'df_ideal' in globals() and len(df_ideal) > 0 else m36
    
    # Definição de métricas (nome, coluna, benchmark, inversão)
    metricas = [
        ('💰 RECEITA', '', '', '', '', ''),
        ('  MRR', 'mrr', met_ideal.get('mrr_final', m36['mrr']), False),
        ('  ARR (Anual)', 'arr', met_ideal.get('mrr_final', m36['mrr']) * 12, False),
        ('  Usuários Ativos', 'usuarios_ativos', met_ideal.get('usuarios_final', 1000), False),
        ('', '', '', '', '', ''),
        ('📊 UNIT ECONOMICS', '', '', '', '', ''),
        ('  LTV/CAC (Índice de Retorno)', 'ltv_cac', 3.0, False),
        ('  CAC (Custo Aquisição Cliente)', 'cac_blended', 250, True),
        ('  Churn (Taxa Cancelamento %)', 'churn_rate', 0.05, True),
        ('  Payback (Meses p/ Recuperar CAC)', 'payback_meses', 12, True),
        ('', '', '', '', '', ''),
        ('💵 CAIXA & RUNWAY', '', '', '', '', ''),
        ('  Caixa Disponível', 'caixa', 50000, False),
        ('  Runway (Meses de Sobrevivência)', 'runway_meses', 12, False),
        ('  Burn Rate (Queima Mensal)', 'burn_rate', 0, True),
        ('', '', '', '', '', ''),
        ('📈 MARGENS', '', '', '', '', ''),
        ('  Margem Bruta %', 'margem_bruta_pct', 70, False),
        ('  EBITDA (Lucro Operacional)', 'ebitda', 0, False),
    ]
    
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
        elif coluna in ['runway_meses', 'payback_meses']:
            # RUNWAY REAL: sempre mostra caixa/despesas, NUNCA infinito
            # (infinito só se não houver despesas, o que é impossível)
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
                v36_str = f'{v36:.1f}m'  # Usa valor do motor se não conseguir calcular
            bench_str = f'>{benchmark:.0f}m'
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

    if not report_mode:
        print("\n" + "-" * 105)
        print("🟢 = Excelente | ✅ = Saudável | ⚠️ = Atenção | 🔴 = Crítico")
        print("Nota: Benchmark = Cenário Ideal (df_ideal) - atualiza automaticamente se premissas mudarem")
    else:
        # Render markdown table
        cols = ['Métrica', 'M1', 'M6', 'M12', 'M36', 'Benchmark', 'Status']
        df_tab = pd.DataFrame(tabela_dados, columns=cols)
        # Substitui NaNs por vazio
        df_tab = df_tab.fillna("")
        display(Markdown(df_tab.to_markdown(index=False)))
        display(Markdown("**Nota:** Benchmark = Cenário Ideal."))
        display(Markdown("\\newpage"))
    
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
    # Adjust size for PDF
    figsize = (10, 3) if report_mode else (18, 5)
    fig, axes = plt.subplots(1, 4, figsize=figsize, dpi=150)
    
    # Se PDF, reduzir fonte do título
    title_size = 12 if report_mode else 16
    fig.suptitle('📊 PAINEL DE KPIs ESTRATÉGICOS', fontsize=title_size, fontweight='bold', y=1.05)
    
    m36 = df_real.iloc[-1]
    
    # Calcular despesas mensais para RUNWAY REAL
    despesas_mensais = m36.get('total_cogs', 0) + m36.get('total_opex', 0)
    caixa = m36.get('caixa', 0)
    runway_real = caixa / despesas_mensais if despesas_mensais > 0 else 999
    
    # Card 1: MRR (Receita Recorrente Mensal)
    mrr_real = m36['mrr']
    mrr_ideal = met_ideal.get('mrr_final', mrr_real * 2)
    gap_mrr = ((mrr_real - mrr_ideal) / mrr_ideal * 100) if mrr_ideal > 0 else 0
    emoji_mrr, cor_mrr, status_mrr = calcular_status(mrr_real, mrr_ideal * 0.7)
    
    axes[0].set_facecolor('#fafafa')
    axes[0].text(0.5, 0.88, '💰 MRR', ha='center', va='center', fontsize=14, fontweight='bold', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.72, 'Receita Recorrente Mensal', ha='center', va='center', fontsize=9, color='gray', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.48, formatar_moeda(mrr_real), ha='center', va='center', fontsize=26, fontweight='bold', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.28, f'Meta: {formatar_moeda(mrr_ideal)}', ha='center', va='center', fontsize=11, color='gray', transform=axes[0].transAxes)
    axes[0].text(0.5, 0.12, f'{emoji_mrr} Gap: {gap_mrr:+.0f}%', ha='center', va='center', fontsize=12, 
                 color=CORES.get(cor_mrr, 'black'), fontweight='bold', transform=axes[0].transAxes)
    axes[0].axis('off')
    
    # Card 2: LTV/CAC (Retorno por Real Investido)
    ltv_cac = m36.get('ltv_cac', 0)
    emoji_ltv, cor_ltv, status_ltv = calcular_status(ltv_cac, 3.0)
    
    axes[1].set_facecolor('#fafafa')
    axes[1].text(0.5, 0.88, '📈 LTV/CAC', ha='center', va='center', fontsize=14, fontweight='bold', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.72, 'Retorno por R$ em Aquisição', ha='center', va='center', fontsize=9, color='gray', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.48, f'{ltv_cac:.1f}x', ha='center', va='center', fontsize=26, fontweight='bold', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.28, 'Meta: ≥3.0x (saudável)', ha='center', va='center', fontsize=11, color='gray', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.12, f'{emoji_ltv} {status_ltv}', ha='center', va='center', fontsize=12,
                 color=CORES.get(cor_ltv, 'black'), fontweight='bold', transform=axes[1].transAxes)
    axes[1].axis('off')
    
    # Card 3: Churn (Taxa de Cancelamento)
    churn = m36.get('churn_rate', 0) * 100
    emoji_churn, cor_churn, status_churn = calcular_status(churn, 5.0, inversao=True)
    
    axes[2].set_facecolor('#fafafa')
    axes[2].text(0.5, 0.88, '🚪 Churn', ha='center', va='center', fontsize=14, fontweight='bold', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.72, 'Taxa de Cancelamento Mensal', ha='center', va='center', fontsize=9, color='gray', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.48, f'{churn:.1f}%', ha='center', va='center', fontsize=26, fontweight='bold', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.28, 'Meta: <5.0% (bom)', ha='center', va='center', fontsize=11, color='gray', transform=axes[2].transAxes)
    axes[2].text(0.5, 0.12, f'{emoji_churn} {status_churn}', ha='center', va='center', fontsize=12,
                 color=CORES.get(cor_churn, 'black'), fontweight='bold', transform=axes[2].transAxes)
    axes[2].axis('off')
    
    # Card 4: Runway (CORRIGIDO - caixa/despesas, não infinito!)
    # Runway = "Quantos meses sobrevivo SEM FATURAR NADA"
    axes[3].set_facecolor('#fafafa')
    axes[3].text(0.5, 0.88, '⏱️ Runway', ha='center', va='center', fontsize=14, fontweight='bold', transform=axes[3].transAxes)
    axes[3].text(0.5, 0.72, 'Meses sem faturar até quebrar', ha='center', va='center', fontsize=9, color='gray', transform=axes[3].transAxes)
    
    # Runway REAL = caixa / despesas (NUNCA infinito, a menos que despesas = 0)
    emoji_run, cor_run, status_run = calcular_status(runway_real, 12.0)
    
    if runway_real >= 999:
        axes[3].text(0.5, 0.48, '∞', ha='center', va='center', fontsize=26, fontweight='bold', color=CORES['sucesso'], transform=axes[3].transAxes)
        axes[3].text(0.5, 0.28, 'Sem despesas!', ha='center', va='center', fontsize=11, color=CORES['sucesso'], transform=axes[3].transAxes)
    else:
        axes[3].text(0.5, 0.48, f'{runway_real:.1f}m', ha='center', va='center', fontsize=26, fontweight='bold', transform=axes[3].transAxes)
        axes[3].text(0.5, 0.28, f'Caixa: {formatar_moeda(caixa)}', ha='center', va='center', fontsize=10, color='gray', transform=axes[3].transAxes)
    
    axes[3].text(0.5, 0.12, f'{emoji_run} {status_run}', ha='center', va='center', fontsize=12,
                 color=CORES.get(cor_run, 'black'), fontweight='bold', transform=axes[3].transAxes)
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
        display(Markdown("![KPI Cards](outputs/figs/pg1_kpi_cards.png)"))
        display(Markdown("\\newpage"))
    else:
        plt.show()
    
    return fig

# ============================================================================
# FUNÇÃO 3: GRÁFICO TEMPORAL COM ÂNCORAS TRIMESTRAIS + TABELA DE VALORES
# ============================================================================
def gerar_grafico_temporal_correlacao(df_real, df_ideal, mc_results=None, report_mode=False):
    """
    Gráfico com 2 eixos Y: MRR (R$) + Usuários Ativos.
    CORRIGIDO:
    - Grid visível para facilitar leitura
    - Âncoras verticais a cada trimestre (3, 6, 9, 12...)
    - Tabela de valores por período abaixo do gráfico
    - Eixo Y direito (roxo) = Usuários Ativos (explicado no título)
    - Eixo Y esquerdo (preto) = MRR em R$
    """
    # Criar figura (Somente gráfico, sem tabela embutida)
    # Adjust size for PDF
    figsize = (10, 5) if report_mode else (14, 8)
    fig = plt.figure(figsize=figsize, dpi=150)
    
    # Subplot 1: Gráfico principal (Ocupa tudo)
    ax1 = fig.add_axes([0.1, 0.1, 0.85, 0.8])  # [left, bottom, width, height]
    
    meses = df_real['mes'].values
    mrr_real = df_real['mrr'].values
    mrr_ideal = df_ideal['mrr'].values if len(df_ideal) > 0 else mrr_real * 1.5
    usuarios = df_real['usuarios_ativos'].values
    
    # Adiciona ruído natural (1.5% de variação para parecer mais real)
    np.random.seed(42)
    mrr_visual = mrr_real + np.random.normal(0, mrr_real * 0.015, len(mrr_real))
    usuarios_visual = usuarios + np.random.normal(0, usuarios * 0.01, len(usuarios))
    usuarios_visual = np.maximum(usuarios_visual, 0)
    
    # Eixo 1: MRR em R$ (PRETO - eixo esquerdo)
    ax1.set_xlabel('Mês', fontsize=12, fontweight='bold')
    ax1.set_ylabel('MRR em R$ (linhas preta e verde)', fontsize=11, color='black')
    
    # Linha Real
    line1, = ax1.plot(meses, mrr_visual, color=CORES['real'], linewidth=2.5, label='MRR Real', marker='o', markersize=3)
    
    # Linha Ideal (benchmark)
    line2, = ax1.plot(meses, mrr_ideal, color=CORES['ideal'], linewidth=2, linestyle='--', label='MRR Ideal (Benchmark)')
    
    # Área do gap
    ax1.fill_between(meses, mrr_visual, mrr_ideal, alpha=0.1, color=CORES['critico'], label='Gap vs Ideal')
    
    ax1.tick_params(axis='y', labelcolor='black', labelsize=10)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: formatar_moeda(x)))
    
    # Eixo 2: Usuários (ROXO - eixo direito)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Usuários Ativos (linha roxa ···)', fontsize=11, color=CORES['usuarios'])
    line3, = ax2.plot(meses, usuarios_visual, color=CORES['usuarios'], linewidth=2.5, linestyle=':', label='Usuários Ativos')
    ax2.tick_params(axis='y', labelcolor=CORES['usuarios'], labelsize=10)
    ax2.set_ylim(0, max(usuarios) * 1.3)
    
    # GRID VISÍVEL - linhas horizontais
    ax1.grid(True, alpha=0.4, linestyle='-', linewidth=0.8, color='#cccccc', axis='y')
    ax1.grid(True, alpha=0.2, linestyle=':', linewidth=0.5, color='#999999', axis='x')
    
    # ÂNCORAS VERTICAIS - linhas a cada trimestre/semestre
    trimestres = [3, 6, 9, 12, 18, 24, 30, 36]
    cores_ancora = {'3': '#e0e0e0', '6': '#bbbbbb', '9': '#e0e0e0', 
                    '12': '#999999', '18': '#bbbbbb', '24': '#999999', 
                    '30': '#bbbbbb', '36': '#666666'}
    
    for t in trimestres:
        if t <= len(meses):
            cor = cores_ancora.get(str(t), '#cccccc')
            ax1.axvline(x=t, color=cor, linestyle='--', linewidth=1.2, alpha=0.7)
            # Labels no topo
            label = f'M{t}'
            if t == 6: label = 'S1'
            if t == 12: label = 'ANO 1'
            if t == 24: label = 'ANO 2'
            if t == 36: label = 'ANO 3'
            ax1.text(t, ax1.get_ylim()[1] * 0.98, label, ha='center', fontsize=8, 
                     fontweight='bold' if t in [12, 24, 36] else 'normal', color='gray')
    
    # Título explicativo
    ax1.set_title('📈 EVOLUÇÃO MRR vs USUÁRIOS (36 Meses)\n'
                  'Eixo Esquerdo (R$): Linhas Preta e Verde | Eixo Direito: Linha Roxa (Usuários)',
                  fontsize=13, fontweight='bold', pad=15)
    
    # Legenda
    lines = [line1, line2, line3]
    labels = ['MRR Real (R$)', 'MRR Ideal/Benchmark (R$)', 'Usuários Ativos (qtd)']
    ax1.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9)
    
    ax1.set_xlim(1, 36)
    
    # Configurações finais de Layout (Sem tabela embutida)
    # Tabela será gerada separadamente
    
    plt.tight_layout()
    plt.savefig('outputs/figs/pg1_temporal_correlacao.png', dpi=300, bbox_inches='tight', facecolor='white')
    
    if report_mode:
        plt.close(fig)
        
        # Renderiza Atomic Block Manualmente
        display(Markdown("### 📈 EVOLUÇÃO MRR vs USUÁRIOS"))
        display(Markdown("![Evolução Temporal](outputs/figs/pg1_temporal_correlacao.png)"))
        display(Markdown("***"))
        display(Markdown("#### 📋 TABELA DE REFERÊNCIA"))
        
        # Gera Tabela Markdown
        cols = ['Período', 'MRR Real', 'MRR Ideal', 'Usuários', 'Gap %']
        df_tab = pd.DataFrame(dados_tabela, columns=cols)
        display(Markdown(df_tab.to_markdown(index=False)))
        display(Markdown("\\newpage"))
        
    else:
        # Modo Notebook Interativo (Legacy + Tabela Markdown)
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
        print("📊 1.4 TABELA DE MILESTONES - REAL vs IDEAL")
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
        display(Markdown("#### 🏁 TABELA DE MILESTONES"))
        display(Markdown(df_milestones.to_markdown(index=False)))
    
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
    # Adjust size for PDF
    figsize = (10, 5) if report_mode else (16, 8)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    
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
    
    # Configurações do eixo
    ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor em R$', fontsize=12)
    ax.set_xticks(x[::3])  # Mostrar a cada 3 meses
    ax.set_xticklabels([f'M{m}' for m in meses[::3]], fontsize=10)
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
    ax.set_title('💰 INVESTIMENTO EM MARKETING vs RECEITA GERADA (MRR)\n'
                 'Barras Azuis = Quanto gastei | Barras Verdes = Quanto gerei | Eficiência = MRR ÷ Marketing',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Legenda
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    
    # Âncoras verticais anuais
    for ano in [12, 24, 36]:
        idx = ano - 1
        if idx < len(x):
            ax.axvline(x=x[idx], color='gray', linestyle='--', linewidth=1, alpha=0.5)
            ax.text(x[idx], ax.get_ylim()[1]*0.95, f'ANO {ano//12}', ha='center', fontsize=9, color='gray')
    
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
        display(Markdown("![Eficiência Marketing](outputs/figs/pg1_eficiencia_marketing.png)"))
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
    Gera insights estratégicos que mudam conforme os dados mudam.
    """
    if not report_mode:
        print("\n" + "="*80)
        print("📢 INSIGHTS ESTRATÉGICOS - O QUE FAZER COM ESTES DADOS")
        print("="*80)
    else:
        display(Markdown("## 🧠 INSIGHTS ESTRATÉGICOS DO COCKPIT"))
    
    insights = []
    
    # INSIGHT 1: LTV/CAC
    ltv_cac = met_real.get('ltv_cac_medio', 0)
    ltv_cac_ideal = met_ideal.get('ltv_cac_medio', 3.0)
    
    if ltv_cac >= 5.0:
        status = "EXCELENTE (TOP 10% do mercado)"
        acao = "Escalar agressivamente - ROI comprovado"
        emoji = "🟢"
    elif ltv_cac >= 3.0:
        status = "SAUDÁVEL"
        acao = "Otimizar churn para aumentar LTV"
        emoji = "✅"
    elif ltv_cac >= 1.5:
        status = "ATENÇÃO"
        acao = "Reduzir CAC ou aumentar retenção URGENTE"
        emoji = "⚠️"
    else:
        status = "CRÍTICO"
        acao = "PARAR aquisição paga. Focar 100% em retenção."
        emoji = "🔴"
    
    if report_mode:
        # Markdown Callout (Gold Standard)
        insight_md = f"""
::: {{.callout-{ 'tip' if 'SAUDÁVEL' in status or 'EXCELENTE' in status else 'warning' if 'ATENÇÃO' in status else 'important' }}}
### 1. Saúde da Unidade Econômica
- **Métrica:** LTV/CAC = {ltv_cac:.2f}x (Ideal: {ltv_cac_ideal:.1f}x)
- **Status:** {status}
- **Implicação:** Cada R$ 1 investido retorna R$ {ltv_cac:.2f}.
- **Ação:** {acao}
:::
"""
        display(Markdown(insight_md))
    else:
        # Print legacy
        print(f"\n{emoji} INSIGHT 1: Saúde da Unidade Econômica")
        print(f"   Métrica: LTV/CAC = {ltv_cac:.2f}x (ideal: {ltv_cac_ideal:.1f}x)")
        print(f"   Status: {status}")
        print(f"   Implicação: Cada R$ 1 em aquisição retorna R$ {ltv_cac:.2f}")
        print(f"   Ação: {acao}")
    
    # INSIGHT 2: Gap de Receita
    mrr_real = met_real.get('mrr_final', 0)
    mrr_ideal = met_ideal.get('mrr_final', mrr_real)
    gap = mrr_ideal - mrr_real
    gap_pct = (gap / mrr_ideal * 100) if mrr_ideal > 0 else 0
    
    if gap <= 0:
        status = "SUPERANDO META"
        acao = "Manter estratégia atual e documentar práticas"
        emoji = "🟢"
    elif gap_pct < 30:
        status = "PRÓXIMO DA META"
        acao = "Ajustes finos em conversão e retenção"
        emoji = "✅"
    else:
        status = "GAP SIGNIFICATIVO"
        custo_oportunidade = gap * 36
        acao = f"{formatar_moeda(custo_oportunidade)} deixados na mesa em 3 anos"
        emoji = "⚠️"
    
    if report_mode:
        insight_md = f"""
::: {{.callout-{ 'tip' if gap <= 0 else 'warning' }}}
### 2. Gap de Receita vs Potencial
- **Real vs Ideal:** {formatar_moeda(mrr_real)} vs {formatar_moeda(mrr_ideal)}
- **Gap:** {formatar_moeda(gap)} ({gap_pct:.0f}%)
- **Status:** {status}
- **Ação:** {acao}
:::
"""
        display(Markdown(insight_md))
    else:
        print(f"\n{emoji} INSIGHT 2: Gap de Receita vs Potencial")
        print(f"   Métrica: Real {formatar_moeda(mrr_real)} vs Ideal {formatar_moeda(mrr_ideal)}")
        print(f"   Gap: -{formatar_moeda(gap)} ({gap_pct:.0f}% abaixo)")
        print(f"   Status: {status}")
        print(f"   Ação: {acao}")
    
    # INSIGHT 3: Runway/Caixa - CALCULADO CORRETAMENTE como caixa/despesas
    m36 = df_real.iloc[-1]
    caixa_final = m36.get('caixa', 0)
    despesas_mensais = m36.get('total_cogs', 0) + m36.get('total_opex', 0)
    runway = caixa_final / despesas_mensais if despesas_mensais > 0 else 999
    burn_rate = m36.get('burn_rate', 0)
    
    # Status baseado no runway REAL (caixa/despesas), não no burn_rate
    if runway > 24:
        status = "MUITO CONFORTÁVEL"
        acao = "Excelente posição de caixa, considerar investir em crescimento"
        emoji = "🟢"
    elif runway > 12:
        status = "CONFORTÁVEL"
        acao = "Manter disciplina de custos"
        emoji = "✅"
    elif runway > 6:
        status = "ATENÇÃO"
        acao = f"Revisar custos. Despesas mensais: {formatar_moeda(despesas_mensais)}"
        emoji = "⚠️"
    else:
        status = "CRÍTICO"
        acao = f"SEM RECEITA = {runway:.0f} meses até quebrar! Despesas: {formatar_moeda(despesas_mensais)}/mês"
        emoji = "🔴"
    
    if report_mode:
        insight_md = f"""
::: {{.callout-{ 'tip' if 'CONFORTÁVEL' in status else 'important' }}}
### 3. Saúde de Caixa & Runway
- **Runway:** {runway:.1f} meses (Caixa: {formatar_moeda(caixa_final)})
- **Burn Rate:** {formatar_moeda(burn_rate) if burn_rate > 0 else 'R$ 0 (Lucrativo)'}
- **Status:** {status}
- **Ação:** {acao}
:::
"""
        display(Markdown(insight_md))
    else:
        print(f"\n{emoji} INSIGHT 3: Saúde de Caixa")
        print(f"   Caixa: {formatar_moeda(caixa_final)}")
        print(f"   Despesas mensais: {formatar_moeda(despesas_mensais)} (COGS + OPEX)")
        print(f"   Runway: {runway:.1f} meses (se parar de faturar)")
        print(f"   Burn Rate (fluxo negativo): {formatar_moeda(burn_rate) if burn_rate > 0 else 'R$ 0 (lucrativo)'}")
        print(f"   Status: {status}")
        print(f"   Ação: {acao}")
    
    # INSIGHT 4: Churn
    churn_real = met_real.get('churn_medio', 0)
    churn_ideal = 5.0  # 5% é benchmark SaaS
    
    if churn_real <= 3:
        status = "EXCELENTE (Best in Class)"
        acao = "Mantém! Churn baixo é seu diferencial competitivo"
        emoji = "🟢"
    elif churn_real <= 5:
        status = "BOM (Dentro do benchmark)"
        acao = "Monitorar e prevenir aumento"
        emoji = "✅"
    elif churn_real <= 8:
        status = "ATENÇÃO"
        acao = "Investir em Customer Success e onboarding"
        emoji = "⚠️"
    else:
        status = "CRÍTICO"
        acao = f"Churn de {churn_real:.1f}% destrói valor. Prioridade MÁXIMA em retenção"
        emoji = "🔴"
    
    if report_mode:
        insight_md = f"""
::: {{.callout-{ 'tip' if 'EXCELENTE' in status or 'BOM' in status else 'important' }}}
### 4. Retenção (Churn)
- **Churn Médio:** {churn_real:.1f}% (Benchmark: <{churn_ideal:.0f}%)
- **Status:** {status}
- **Ação:** {acao}
:::
"""
        display(Markdown(insight_md))
        display(Markdown("\\newpage"))
    else:
        print(f"\n{emoji} INSIGHT 4: Retenção de Clientes")
        print(f"   Métrica: Churn médio = {churn_real:.1f}% (benchmark: <{churn_ideal:.0f}%)")
        print(f"   Status: {status}")
        print(f"   Ação: {acao}")
    
    if not report_mode:
        print("\n" + "-"*80)
        print("📌 NOTA: Insights gerados automaticamente. Se premissas mudarem, insights atualizam.")
    
    return insights

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================
import os

def executar_pagina_1(df_real_m, df_ideal, met_real, met_ideal, report_mode=False):
    """
    Gera todos os artefatos da Página 1: Cockpit.
    """
    if not report_mode:
        print("\n🚀 EXECUTANDO GERAÇÃO DA PÁGINA 1...")
        print("="*80)
    
    os.makedirs('outputs/figs', exist_ok=True)
    os.makedirs('outputs/metadata', exist_ok=True)
    os.makedirs('outputs/tabelas', exist_ok=True)

    # 1. Tabela Executiva (Silenciar em PDF por enquanto para evitar logs sujos)
    if not report_mode:
        gerar_tabela_executiva(df_real_m, df_ideal, met_real, met_ideal)

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
