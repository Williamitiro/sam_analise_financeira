import sys
import os
import pandas as pd
import numpy as np
import importlib
from datetime import datetime
import contextlib
import io
import json

# Setup paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'celulas'))

# ============================================================================
# 1. MONKEYPATCHING INFRASTRUCTURE
# ============================================================================
CAPTURED_BLOCKS = []

def capture_atomic_block(**kwargs):
    """
    Substituta para render_atomic_block que captura os dados para auditoria.
    """
    block_data = {
        'id': kwargs.get('chart_id', 'unknown'),
        'title': kwargs.get('title_technical', 'Sem Título'),
        'colloquial': kwargs.get('title_colloquial', ''),
        'tabela': kwargs.get('df_tabela', None),
        'insight': kwargs.get('insight_dict', {}),
        'formulas': kwargs.get('formulas_md', ''),
        'legend': kwargs.get('legend_md', ''),
        'source': kwargs.get('data_source_text', '')
    }
    
    CAPTURED_BLOCKS.append(block_data)
    
    # SILENCIO ABSOLUTO: Fecha a figura se existir para não abrir popup
    if 'fig' in kwargs and kwargs['fig']:
        try:
            import matplotlib.pyplot as plt
            plt.close(kwargs['fig'])
            plt.close('all') # Garantia extra
        except:
            pass

def dummy_display(*args, **kwargs): pass
def dummy_markdown(*args, **kwargs): return ""
def dummy_html(*args, **kwargs): return ""

# ============================================================================
# 2. LOAD MODULES & APPLY PATCH
# ============================================================================
try:
    import celulas.celula_0_utils as utils
    
    # Patch base
    utils.render_atomic_block = capture_atomic_block
    
    # Load Core Modules
    import celulas.celula_4_motor as motor
    import celulas.celula_5D_monte_carlo as mc
    import celulas.celula_2B_config_MC as config_mc
    import celulas.celula_2_premissas as premissas_mod
    
    importlib.reload(premissas_mod)
    PREMISSAS = premissas_mod.PREMISSAS
    
    if hasattr(config_mc, 'PREMISSAS') and 'monte_carlo' in config_mc.PREMISSAS:
        PREMISSAS['monte_carlo'] = config_mc.PREMISSAS['monte_carlo']
    
    # Import Pages
    import celulas.PAGINA_1_COCKPIT_V4 as p1
    import celulas.PAGINA_2_GROWTH as p2
    import celulas.PAGINA_3_FINANCEIRO as p3
    import celulas.PAGINA_4_UNIT_ECONOMICS as p4
    import celulas.PAGINA_5_RISCO as p5

    # Force Reload & Inject Patch
    importlib.reload(p1)
    importlib.reload(p2)
    importlib.reload(p3)
    importlib.reload(p4)
    importlib.reload(p5)
    
    print("🩹 Injetando capture_atomic_block...")
    p1.render_atomic_block = capture_atomic_block
    p2.render_atomic_block = capture_atomic_block
    p3.render_atomic_block = capture_atomic_block
    p4.render_atomic_block = capture_atomic_block
    p5.render_atomic_block = capture_atomic_block
    
    # Try utils subgroup patch
    if hasattr(p1, 'utils'): p1.utils.render_atomic_block = capture_atomic_block
    if hasattr(p2, 'utils'): p2.utils.render_atomic_block = capture_atomic_block
    if hasattr(p3, 'utils'): p3.utils.render_atomic_block = capture_atomic_block
    if hasattr(p4, 'utils'): p4.utils.render_atomic_block = capture_atomic_block
    if hasattr(p5, 'utils'): p5.utils.render_atomic_block = capture_atomic_block

except ImportError as e:
    print(f"❌ Erro Crítico na Importação: {e}")
    sys.exit(1)

# ============================================================================
# 3. EXECUTION ENGINE
# ============================================================================
def run_audit_full():
    print("🚀 GERAÇÃO DE SNAPSHOT DE AUDITORIA COMPLETA (V3 - EXPANDED)")
    print("="*80)

    # 3.1 Executar Motor (Dados Reais)
    print("\n⚙️  Executando Motor Financeiro V13...")
    df_mensal, df_anual, metricas, alertas = motor.executar_motor_fintech_v10_production_ready(PREMISSAS)
    
    # 3.2 Executar Motor Ideal (Benchmarks)
    print("🌟 Executando Cenário Ideal...")
    p_ideal = PREMISSAS.copy()
    p_ideal['marketing_fixo_mensal'] = 5000 
    p_ideal['churn_inicial'] = 0.03
    df_ideal_m, df_ideal_a, met_ideal, _ = motor.executar_motor_fintech_v10_production_ready(p_ideal)
    
    # 3.2b Dados Semanais (Sintéticos/Interpolados)
    print("📅 Gerando dados semanais sintéticos (Interpolados)...")
    dates_s = pd.date_range(start=PREMISSAS['data_inicio'], periods=36*4, freq='W')
    df_real_s = pd.DataFrame({'semana': range(1, len(dates_s)+1), 'data': dates_s})
    
    colunas_interpolate = ['cac_blended', 'caixa', 'receita_bruta', 'total_cogs', 'total_opex', 'usuarios_ativos']
    x_monthly = np.linspace(0, len(df_mensal)-1, len(df_mensal))
    x_weekly = np.linspace(0, len(df_mensal)-1, len(df_real_s))
    
    for col in colunas_interpolate:
        if col in df_mensal.columns:
            df_real_s[col] = np.interp(x_weekly, x_monthly, df_mensal[col])
        else:
            df_real_s[col] = 0.0
    
    df_ideal_s = df_real_s.copy()
    
    # 3.3 Executar Monte Carlo
    print("🎲 Executando Monte Carlo (Fast: 50 sims)...")
    config_mc = PREMISSAS.get('monte_carlo', {})
    config_mc['n_simulacoes'] = 50
    _, mc_results = mc.executar_monte_carlo(PREMISSAS, motor_func=motor.executar_motor_fintech_v10_production_ready)
    
    # ========================================================================
    # 4. PAGE EXECUTION (CAPTURING ARTIFACTS)
    # ========================================================================
    print("\n📸 Executando Páginas para Captura...")
    
    with contextlib.redirect_stdout(io.StringIO()):
        p1.executar_pagina_1(df_mensal, df_ideal_m, metricas, met_ideal, report_mode=True)
        p2.executar_pagina_2_growth_machine(df_mensal, df_real_s, df_ideal_m, df_ideal_s, PREMISSAS, report_mode=True)
        p3.executar_pagina_3_financeiro(df_mensal, df_real_s, df_ideal_m, PREMISSAS, report_mode=True)
        p4.executar_pagina_4_unit_economics(df_mensal, df_real_s, df_ideal_m, PREMISSAS, report_mode=True)
        
        # P5 lida com possivel erro de tupla no mc_results internamente se nao for corrigido, 
        # mas ja corrigimos o script de chamada.
        p5.executar_pagina_5_risco(df_mensal, df_ideal_m, mc_results, PREMISSAS, 
                                   df_real_s=df_real_s, df_ideal_s=df_ideal_s, 
                                   motor_func=motor.executar_motor_fintech_v10_production_ready,
                                   report_mode=True)

    print(f"   ✅ Capturados {len(CAPTURED_BLOCKS)} blocos de inteligência.")

    # ========================================================================
    # 5. REPORT GENERATION
    # ========================================================================
    print("\n📝 Escrevendo Relatório Final...")
    buffer = []
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    buffer.append(f"# 🛡️ RELATÓRIO DE AUDITORIA ANALÍTICA COMPLETA")
    buffer.append(f"**Data:** {timestamp} | **Motor:** V13 Production | **Snapshot:** Full Coverage")
    buffer.append("\n---")
    
    # 5.1 Resumo Premissas Críticas (EXPANDIDO)
    buffer.append("## 1. CALIBRAGEM DO MODELO (PREMISSAS)")
    buffer.append("| Categoria | Variável | Valor Configurado |")
    buffer.append("|---|---|---|")
    
    # Lista expandida
    keys_audit = [
        ('Growth', 'usuarios_pagos_iniciais'),
        ('Growth', 'trafego_inicial'),
        ('Growth', 'crescimento_trafego_mes_1_6'),
        ('Growth', 'churn_inicial'),
        ('Growth', 'churn_base'),
        ('Pricing', 'preco_lite'),
        ('Pricing', 'preco_trader'),
        ('Pricing', 'preco_pro'),
        ('Custos', 'custo_ia_lite'),
        ('Custos', 'custo_ia_trader'),
        ('Custos', 'custo_ia_pro'),
        ('Marketing', 'marketing_fixo_mensal'),
        ('Marketing', 'marketing_perc_receita'),
        ('RH', 'salario_fundador'),
        ('RH', 'trigger_fundador'),
        ('RH', 'salario_dev_senior'),
        ('RH', 'trigger_dev'),
        ('RH', 'salario_cs'),
        ('RH', 'trigger_cs'),
        ('RH', 'encargos_trabalhistas'),
        ('Capital', 'caixa_inicial'),
        ('Capital', 'aporte_mensal'),
        ('Capital', 'meses_aporte'),
    ]
    
    for cat, k in keys_audit:
        val = PREMISSAS.get(k, 'N/A')
        buffer.append(f"| {cat} | `{k}` | {val} |")
    
    # 5.2 Loop Pelos Blocos Capturados
    blocks_by_page = {}
    for block in CAPTURED_BLOCKS:
        pid = block['id'].split('_')[0] if '_' in block['id'] else 'other'
        if pid not in blocks_by_page: blocks_by_page[pid] = []
        blocks_by_page[pid].append(block)
        
    page_order = ['pg1', 'pg2', 'pg3', 'pg4', 'pg5']
    page_names = {
        'pg1': 'COCKPIT EXECUTIVO',
        'pg2': 'GROWTH MACHINE',
        'pg3': 'FINANCEIRO & DRE',
        'pg4': 'UNIT ECONOMICS',
        'pg5': 'RISCO & CENÁRIOS'
    }
    
    for pid in page_order:
        if pid not in blocks_by_page: continue
        
        pname = page_names.get(pid, pid.upper())
        buffer.append(f"\n## 📑 {pname} ({len(blocks_by_page[pid])} Blocos)")
        
        for block in blocks_by_page[pid]:
            buffer.append(f"\n### {block['title']}")
            if block['colloquial']:
                buffer.append(f"> *{block['colloquial']}*")
            
            if block['insight']:
                ins = block['insight']
                buffer.append("\n**🧠 INSIGHT AUTOMÁTICO:**")
                buffer.append(f"- **Fato:** {ins.get('fato', '-')}")
                buffer.append(f"- **Causa:** {ins.get('causa', '-')}")
                buffer.append(f"- **Implicação:** {ins.get('implicacao', '-')}")
                buffer.append(f"- **Ação:** {ins.get('acao', '-')}")
            
            if block['tabela'] is not None:
                buffer.append("\n**📊 DADOS TABULADOS:**")
                df = block['tabela']
                if isinstance(df, pd.DataFrame):
                    if df.empty:
                        buffer.append("*(Tabela Vazia)*")
                    else:
                        buffer.append(df.to_markdown(index=False))
                elif isinstance(df, str):
                    buffer.append(df)
            
            if block['formulas']:
                buffer.append("\n<details><summary>🔍 Ver Fórmulas e Auditoria</summary>")
                buffer.append("\n" + block['formulas'])
                buffer.append("\n</details>")
                
            buffer.append("\n---")

    out_path = 'snapshot_auditoria.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(buffer))
        
    print(f"✅ RELATÓRIO SALVO: {os.path.abspath(out_path)}")

if __name__ == "__main__":
    run_audit_full()
