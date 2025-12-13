# ==============================================================================
# GERADOR DE SNAPSHOT DE AUDITORIA COMPLETA V7.0 (EXTRAÇÃO DIRETA)
# ==============================================================================
# VERSÃO: 7.0 - EXTRAÇÃO HÍBRIDA (DataFrames + render_atomic_block)
# 
# MUDANÇA CRÍTICA: Não depende APENAS do render_atomic_block.
# Extrai dados DIRETAMENTE dos DataFrames retornados pelo motor.
# ==============================================================================

import sys
import os
import gc
import importlib
import pandas as pd
import numpy as np
from datetime import datetime
import contextlib
import io
import json
import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==============================================================================
# 1. SETUP
# ==============================================================================
def limpar_cache():
    mods = ['celula_0_utils', 'celula_2_premissas', 'celula_2B_config_MC',
            'celula_4_motor', 'celula_5D_monte_carlo', 
            'PAGINA_1_COCKPIT_V4', 'PAGINA_2_GROWTH', 'PAGINA_3_FINANCEIRO',
            'PAGINA_4_UNIT_ECONOMICS', 'PAGINA_5_RISCO']
    for k in list(sys.modules.keys()):
        for m in mods:
            if m in k:
                del sys.modules[k]
                break
    gc.collect()

limpar_cache()
print("🧹 Cache limpo")

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, 'celulas'))

# ==============================================================================
# 2. IMPORTS
# ==============================================================================
print("📦 Carregando módulos...")

import celulas.celula_2_premissas as p_mod
importlib.reload(p_mod)
PREMISSAS = p_mod.PREMISSAS.copy()

import celulas.celula_2B_config_MC as mc_mod
importlib.reload(mc_mod)
if 'monte_carlo' in getattr(mc_mod, 'PREMISSAS', {}):
    PREMISSAS['monte_carlo'] = mc_mod.PREMISSAS['monte_carlo']

import celulas.celula_4_motor as motor
importlib.reload(motor)

import celulas.celula_5D_monte_carlo as mc
importlib.reload(mc)

print("✅ Módulos carregados")

# ==============================================================================
# 3. HELPERS
# ==============================================================================
def fmt_m(val):
    if pd.isna(val): return "R$ 0.00"
    if val == 0: return "R$ 0.00"
    # Formatação Gold Standard: R$ 1.234,56
    s = f"{val:,.2f}"
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"R$ {s}"

def fmt_p(val, ja_em_pct=True):
    if pd.isna(val): return "0.00%"
    # Se ja_em_pct=True, valor 45.11 é 45.11%. Se False, 0.4511 é 45.11%
    if not ja_em_pct:
        val = val * 100
    return f"{val:.2f}%"

def safe(df, col, idx, d=0):
    try:
        if col in df.columns and idx < len(df):
            v = df[col].iloc[idx]
            return v if pd.notna(v) else d
        return d
    except: return d

def salvar(path, conteudo):
    for i in range(5):
        p = path if i == 0 else f"{path[:-3]}_{i}.md"
        try:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            return p
        except PermissionError:
            pass
    raise PermissionError()

# ==============================================================================
# 4. EXECUÇÃO
# ==============================================================================
def run():
    print("\n" + "="*80)
    print("🔬 AUDITORIA FORENSE V7.0 - EXTRAÇÃO DIRETA DO MOTOR")
    print("="*80)
    ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # --- SIMULAÇÃO ---
    print("\n⚙️ FASE 1: Executando Motor...")
    
    df_real, df_anual, met_real, alertas = motor.executar_motor_fintech_v10_production_ready(
        PREMISSAS, seed=42, modo_debug=False
    )
    print(f"   ✓ Real: {len(df_real)} meses, {len(df_real.columns)} colunas")
    
    # Ideal
    p_ideal = PREMISSAS.copy()
    p_ideal['marketing_fixo_mensal'] = 5000
    p_ideal['churn_inicial'] = 0.03
    df_ideal, _, met_ideal, _ = motor.executar_motor_fintech_v10_production_ready(p_ideal, seed=42)
    print(f"   ✓ Ideal: {len(df_ideal)} meses")
    
    # Estresse
    p_stress = PREMISSAS.copy()
    p_stress['churn_inicial'] = PREMISSAS['churn_inicial'] * 2
    p_stress['taxa_trial_para_pagante'] = PREMISSAS['taxa_trial_para_pagante'] * 0.5
    df_stress, _, _, _ = motor.executar_motor_fintech_v10_production_ready(p_stress, seed=42)
    print(f"   ✓ Estresse: {len(df_stress)} meses")
    
    # Monte Carlo
    print("   → Monte Carlo...")
    mc_stats = {}
    df_mc = pd.DataFrame()
    
    try:
        _, df_mc = mc.executar_monte_carlo(PREMISSAS, motor_func=motor.executar_motor_fintech_v10_production_ready)
        
        if df_mc is not None and not df_mc.empty:
            for col in df_mc.columns:
                vals = df_mc[col].dropna()
                if len(vals) > 0 and vals.dtype in ['float64', 'int64']:
                    mc_stats[f'{col}_p5'] = np.percentile(vals, 5)
                    mc_stats[f'{col}_p50'] = np.percentile(vals, 50)
                    mc_stats[f'{col}_p95'] = np.percentile(vals, 95)
                    mc_stats[f'{col}_mean'] = vals.mean()
            
            if 'caixa_final' in df_mc.columns:
                mc_stats['prob_caixa_negativo'] = (df_mc['caixa_final'] < 0).mean()
            if 'quebrou' in df_mc.columns:
                mc_stats['prob_quebra'] = df_mc['quebrou'].mean()
        
        print(f"   ✓ MC: {len(df_mc)} sims, {len(mc_stats)} métricas")
    except Exception as e:
        print(f"   ⚠️ MC: {e}")
    
    # --- RELATÓRIO ---
    print("\n📝 FASE 2: Gerando Relatório Completo...")
    
    buf = []
    
    # === CAPA ===
    buf.append("# 🔬 RELATÓRIO DE AUDITORIA FORENSE V7.0")
    buf.append("")
    buf.append(f"**Gerado:** {ts}")
    buf.append(f"**Premissas:** V{PREMISSAS.get('meta_version', 'N/A')}")
    buf.append(f"**Motor:** V13 | **Colunas:** {len(df_real.columns)}")
    buf.append(f"**Monte Carlo:** {len(df_mc)} simulações")
    buf.append("")
    buf.append("> ⚠️ DOCUMENTO CONFIDENCIAL")
    buf.append("")
    buf.append("---")
    buf.append("")
    
    # === 1. PREMISSAS COMPLETAS ===
    buf.append("# 1. 📋 TODAS AS PREMISSAS")
    buf.append("")
    buf.append("| Categoria | Parâmetro | Valor |")
    buf.append("|---|---|---|")
    
    categorias = {
        'Growth': ['usuarios_pagos_iniciais', 'trafego_inicial', 'crescimento_trafego_mes_1_6',
                   'taxa_visitante_para_trial', 'taxa_trial_para_pagante'],
        'Churn': ['churn_inicial', 'churn_maturidade', 'churn_base', 'churn_decaimento_mensal'],
        'Pricing': ['preco_lite', 'preco_trader', 'preco_pro', 'mix_lite', 'mix_trader', 'mix_pro'],
        'COGS': ['custo_ia_lite', 'custo_ia_trader', 'custo_ia_pro'],
        'Marketing': ['marketing_fixo_mensal', 'marketing_perc_receita', 'marketing_teto'],
        'RH': ['salario_fundador', 'trigger_fundador', 'salario_dev_senior', 'trigger_dev', 
               'salario_cs', 'trigger_cs', 'encargos_trabalhistas'],
        'Capital': ['caixa_inicial', 'aporte_mensal', 'meses_aporte', 'caixa_reserva_operacional'],
        'Infra T1': ['t1_vps_app_api', 't1_vps_windows_mt5', 't1_database_managed', 't1_storage_s3',
                     't1_ferramentas_dev', 't1_scraping_news', 't1_email_transacional'],
    }
    
    for cat, keys in categorias.items():
        for k in keys:
            v = PREMISSAS.get(k, 'N/A')
            if isinstance(v, float):
                if v < 1 and v > 0:
                    v = fmt_p(v)
                else:
                    v = fmt_m(v) if v > 10 else f"{v:.4f}"
            buf.append(f"| {cat} | `{k}` | {v} |")
    
    buf.append("")
    buf.append("---")
    buf.append("")
    
    # === 2. EXTRATO MÊS 1 (AUDITORIA FORENSE ESTILO) ===
    buf.append("# 2. 🧾 EXTRATO DETALHADO MÊS 1 (AUDITORIA FORENSE)")
    buf.append("")
    buf.append("> Estilo `auditoria_forense.py` - Cada centavo rastreado")
    buf.append("")
    
    row1 = df_real.iloc[0]
    
    buf.append("## 2.1 Entradas Mês 1")
    buf.append("| Descrição | Valor |")
    buf.append("|---|---|")
    buf.append(f"| (+) Caixa Inicial | {fmt_m(PREMISSAS.get('caixa_inicial', 0))} |")
    buf.append(f"| (+) Aportes/Investimento | {fmt_m(safe(df_real, 'aportes_capital', 0, 0))} |")
    buf.append(f"| (+) Receita Bruta | {fmt_m(safe(df_real, 'receita_bruta', 0, 0))} |")
    buf.append(f"| (+) Receita Líquida | {fmt_m(safe(df_real, 'receita_liquida', 0, 0))} |")
    buf.append("")
    
    buf.append("## 2.2 Saídas Mês 1")
    buf.append("| Descrição | Valor |")
    buf.append("|---|---|")
    buf.append(f"| (-) Marketing | {fmt_m(safe(df_real, 'gasto_marketing', 0, 0))} |")
    buf.append(f"| (-) Infraestrutura | {fmt_m(safe(df_real, 'custo_infra_fixo', 0, 0))} |")
    buf.append(f"| (-) Pessoal/RH | {fmt_m(safe(df_real, 'custo_pessoal', 0, 0))} |")
    buf.append(f"| (-) COGS Total | {fmt_m(safe(df_real, 'total_cogs', 0, 0))} |")
    buf.append(f"| (-) OPEX Total | {fmt_m(safe(df_real, 'total_opex', 0, 0))} |")
    buf.append(f"| (-) Impostos | {fmt_m(safe(df_real, 'impostos', 0, 0))} |")
    buf.append(f"| (-) Taxas Pagamento | {fmt_m(safe(df_real, 'taxas_pagamento', 0, 0))} |")
    buf.append(f"| (-) CAPEX | {fmt_m(safe(df_real, 'capex', 0, 0))} |")
    buf.append("")
    
    buf.append("## 2.3 Resultado Mês 1")
    buf.append("| Métrica | Valor |")
    buf.append("|---|---|")
    buf.append(f"| Caixa Final | **{fmt_m(safe(df_real, 'caixa', 0, 0))}** |")
    buf.append(f"| Burn Rate | {fmt_m(safe(df_real, 'burn_rate', 0, 0))} |")
    buf.append(f"| Runway | {safe(df_real, 'runway_meses', 0, 0):.1f} meses |")
    buf.append(f"| Lucro/Prejuízo | {fmt_m(safe(df_real, 'lucro_liquido', 0, 0))} |")
    buf.append("")
    buf.append("---")
    buf.append("")
    
    # === 3. TABELA COMPLETA - TODAS AS COLUNAS DO MOTOR ===
    buf.append("# 3. 📊 TABELA COMPLETA DO MOTOR (TODAS AS COLUNAS)")
    buf.append("")
    buf.append(f"> **Total de colunas disponíveis: {len(df_real.columns)}**")
    buf.append("")
    
    # Agrupar colunas por categoria
    col_groups = {
        'Tráfego & Aquisição': ['trafego_total', 'trafego_pago', 'trafego_organico', 
                                'trials_total', 'novos_pagantes_total', 'novos_ads', 'novos_organicos'],
        'Usuários': ['usuarios_ativos', 'usuarios_lite', 'usuarios_trader', 'usuarios_pro',
                     'churn_usuarios', 'reativacoes'],
        'Receita': ['receita_bruta', 'receita_assinaturas', 'receita_lite', 'receita_trader', 
                    'receita_pro', 'mrr', 'arr', 'arpu'],
        'Custos': ['total_cogs', 'custo_ia_total', 'total_opex', 'gasto_marketing', 
                   'custo_infra_fixo', 'custo_pessoal'],
        'Margens': ['margem_bruta', 'margem_bruta_pct', 'ebitda', 'ebitda_margin', 
                    'lucro_liquido', 'margem_liquida'],
        'Caixa': ['caixa', 'burn_rate', 'runway_meses', 'aportes_capital'],
        'Unit Economics': ['ltv', 'cac_blended', 'cac_paid', 'ltv_cac', 'payback_meses'],
        'Churn': ['churn_rate', 'retention_rate', 'churn_pct']
    }
    
    meses = [0, 5, 11, 17, 23, 29, 35]  # M1, M6, M12, M18, M24, M30, M36
    labels = ['M1', 'M6', 'M12', 'M18', 'M24', 'M30', 'M36']
    
    for grupo, cols in col_groups.items():
        cols_exist = [c for c in cols if c in df_real.columns]
        if not cols_exist:
            continue
        
        buf.append(f"## 3.{list(col_groups.keys()).index(grupo)+1} {grupo}")
        buf.append("")
        buf.append(f"| Métrica | {' | '.join(labels)} |")
        buf.append(f"|---|{'---|' * len(labels)}")
        
        for col in cols_exist:
            vals = []
            for m in meses:
                v = safe(df_real, col, m, 0)
                if 'pct' in col or 'margin' in col:
                    # Valores já em percentual (ex: 45.11 = 45.11%)
                    vals.append(fmt_p(v, ja_em_pct=True) if pd.notna(v) else "N/A")
                elif 'rate' in col:
                    # Valores em fração (ex: 0.12 = 12.00%)
                    vals.append(fmt_p(v, ja_em_pct=False) if pd.notna(v) else "N/A")
                elif 'usuarios' in col or 'trafego' in col or 'trials' in col or 'novos' in col:
                    vals.append(f"{int(v):,}" if pd.notna(v) else "N/A")
                elif 'ltv_cac' in col:
                    vals.append(f"{v:.2f}x" if pd.notna(v) and v < 9999 else "∞")
                elif 'runway' in col or 'payback' in col:
                    vals.append(f"{v:.1f}" if pd.notna(v) else "N/A")
                else:
                    vals.append(fmt_m(v) if pd.notna(v) else "N/A")
            buf.append(f"| `{col}` | {' | '.join(vals)} |")
        
        buf.append("")
    
    buf.append("---")
    buf.append("")
    
    # === 4. COMPARATIVO REAL vs IDEAL vs ESTRESSE ===
    buf.append("# 4. ⚖️ COMPARATIVO: REAL vs IDEAL vs ESTRESSE")
    buf.append("")
    
    buf.append("## 4.1 Snapshot M36")
    buf.append("")
    buf.append("| Métrica | Real | Ideal | Estresse | Gap Real/Ideal |")
    buf.append("|---|---|---|---|---|")
    
    for col, nome in [
        ('mrr', 'MRR'), ('arr', 'ARR'), ('usuarios_ativos', 'Usuários'),
        ('caixa', 'Caixa'), ('receita_bruta', 'Receita'), ('lucro_liquido', 'Lucro'),
        ('ltv_cac', 'LTV/CAC'), ('churn_rate', 'Churn'), ('runway_meses', 'Runway')
    ]:
        vr = safe(df_real, col, 35, 0)
        vi = safe(df_ideal, col, 35, 0)
        vs = safe(df_stress, col, 35, 0)
        gap = ((vi - vr) / vi * 100) if vi != 0 else 0
        
        if 'usuarios' in col:
            buf.append(f"| {nome} | {int(vr):,} | {int(vi):,} | {int(vs):,} | {gap:.1f}% |")
        elif 'ltv_cac' in col:
            buf.append(f"| {nome} | {vr:.2f}x | {vi:.2f}x | {vs:.2f}x | {gap:.1f}% |")
        elif 'churn' in col or 'rate' in col:
            # churn_rate está em fração (0.12 = 12%)
            buf.append(f"| {nome} | {fmt_p(vr, ja_em_pct=False)} | {fmt_p(vi, ja_em_pct=False)} | {fmt_p(vs, ja_em_pct=False)} | {gap:.1f}% |")
        elif 'runway' in col:
            buf.append(f"| {nome} | {vr:.1f}m | {vi:.1f}m | {vs:.1f}m | {gap:.1f}% |")
        else:
            buf.append(f"| {nome} | {fmt_m(vr)} | {fmt_m(vi)} | {fmt_m(vs)} | {gap:.1f}% |")
    
    buf.append("")
    buf.append("---")
    buf.append("")
    
    # === 5. MONTE CARLO COMPLETO ===
    buf.append("# 5. 🎲 MONTE CARLO COMPLETO")
    buf.append("")
    
    buf.append("## 5.1 Configuração")
    buf.append("")
    mc_cfg = PREMISSAS.get('monte_carlo', {})
    buf.append(f"- **Simulações:** {mc_cfg.get('n_simulacoes', 'N/A')}")
    buf.append(f"- **Cenários:** {list(mc_cfg.get('cenarios', {}).keys())}")
    buf.append(f"- **Variáveis:** {list(mc_cfg.get('variaveis', {}).keys())}")
    buf.append("")
    
    buf.append("## 5.2 Estatísticas Percentis")
    buf.append("")
    
    # Monte Carlo - colunas disponíveis
    if df_mc is not None and not df_mc.empty:
        buf.append(f"> **Colunas MC disponíveis:** {list(df_mc.columns)}")
        buf.append("")
        
        buf.append("| Métrica | P5 | P50 | P95 | Média |")
        buf.append("|---|---|---|---|---|")
        
        for col in df_mc.columns:
            if f'{col}_p50' in mc_stats:
                p5 = mc_stats.get(f'{col}_p5', 0)
                p50 = mc_stats.get(f'{col}_p50', 0)
                p95 = mc_stats.get(f'{col}_p95', 0)
                mean = mc_stats.get(f'{col}_mean', 0)
                
                if 'usuarios' in col:
                    buf.append(f"| {col} | {int(p5):,} | {int(p50):,} | {int(p95):,} | {int(mean):,} |")
                elif 'ltv_cac' in col:
                    buf.append(f"| {col} | {p5:.2f}x | {p50:.2f}x | {p95:.2f}x | {mean:.2f}x |")
                elif 'prob' in col or 'pct' in col:
                    buf.append(f"| {col} | {fmt_p(p5)} | {fmt_p(p50)} | {fmt_p(p95)} | {fmt_p(mean)} |")
                else:
                    buf.append(f"| {col} | {fmt_m(p5)} | {fmt_m(p50)} | {fmt_m(p95)} | {fmt_m(mean)} |")
        
        buf.append("")
        
        buf.append("## 5.3 Probabilidades de Risco")
        buf.append("")
        buf.append("| Indicador | Valor |")
        buf.append("|---|---|")
        
        if 'prob_caixa_negativo' in mc_stats:
            p = mc_stats['prob_caixa_negativo'] * 100
            e = "🔴" if p > 50 else ("⚠️" if p > 20 else "✅")
            buf.append(f"| Prob. Caixa < 0 | {e} **{p:.1f}%** |")
        
        if 'prob_quebra' in mc_stats:
            p = mc_stats['prob_quebra'] * 100
            e = "🔴" if p > 50 else ("⚠️" if p > 20 else "✅")
            buf.append(f"| Prob. Quebra | {e} **{p:.1f}%** |")
        
        buf.append("")
    else:
        buf.append("*Monte Carlo não retornou dados.*")
        buf.append("")
    
    buf.append("---")
    buf.append("")
    
    # === 6. ALERTAS ===
    buf.append("# 6. ⚠️ ALERTAS DO MOTOR")
    buf.append("")
    
    if alertas:
        for a in alertas[:30]:
            if isinstance(a, dict):
                msg = a.get('mensagem', str(a))
                tip = a.get('tipo', 'info')
            else:
                msg = str(a)
                tip = 'info'
            e = '🔴' if tip == 'critico' else ('⚠️' if tip == 'atencao' else 'ℹ️')
            buf.append(f"- {e} {msg}")
        buf.append("")
    else:
        buf.append("*Nenhum alerta.*")
        buf.append("")
    
    buf.append("---")
    buf.append("")
    
    # === 7. LISTA COMPLETA DE COLUNAS ===
    buf.append("# 7. 📋 LISTA COMPLETA DE COLUNAS DO DataFrame")
    buf.append("")
    buf.append(f"> Total: {len(df_real.columns)} colunas")
    buf.append("")
    buf.append("```")
    for i, col in enumerate(df_real.columns):
        buf.append(f"{i+1:3}. {col}")
    buf.append("```")
    buf.append("")
    buf.append("---")
    buf.append("")
    
    # === METADADOS ===
    buf.append("# 📋 METADADOS")
    buf.append("")
    buf.append("| Campo | Valor |")
    buf.append("|---|---|")
    buf.append(f"| Timestamp | {ts} |")
    buf.append(f"| Colunas Motor | {len(df_real.columns)} |")
    buf.append(f"| Métricas MC | {len(mc_stats)} |")
    buf.append(f"| Alertas | {len(alertas) if alertas else 0} |")
    buf.append("")
    buf.append("---")
    buf.append("*Fim do Relatório*")
    
    # === SALVAR ===
    conteudo = "\n".join(buf)
    path = os.path.abspath(os.path.join(script_dir, '..', '..', 'snapshot_auditoria.md'))
    
    try:
        final = salvar(path, conteudo)
        print(f"\n✅ SALVO: {final}")
    except Exception as e:
        print(f"\n❌ {e}")
    
    # CSV completo
    try:
        csv_path = path.replace('.md', '_completo.csv')
        df_real.to_csv(csv_path, index=False)
        print(f"✅ CSV: {csv_path}")
    except Exception as e:
        print(f"⚠️ CSV: {e}")
    
    # JSON
    try:
        json_data = {
            'timestamp': ts,
            'colunas_motor': list(df_real.columns),
            'mc_stats': {k: float(v) for k, v in mc_stats.items()},
        }
        jpath = path.replace('.md', '.json')
        with open(jpath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON: {jpath}")
    except Exception as e:
        print(f"⚠️ JSON: {e}")

if __name__ == "__main__":
    run()
    plt.close('all')
