# CÉLULA 5D - MONTE CARLO ENTERPRISE GOLD STANDARD V4.1 (COMPATÍVEL V13 + GLOSSÁRIO)
# ============================================================================
# CORREÇÕES APLICADAS:
# 1. ✅ Compatibilidade Motor V13 (simulacao_id + tratamento de runway negativo)
# 2. ✅ Output detalhado de Runway (P10/P50/P90) na tabela
# 3. ✅ Glossário Técnico adicionado ao final (explicando siglas)
# 4. ✅ Mantida estrutura completa sem otimizações destrutivas
# ============================================================================
import os
import sys
import time
import pickle
import warnings
from datetime import datetime
from collections import defaultdict
import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import cholesky
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None

# BLOCO 2: VALIDAÇÕES CRÍTICAS
# ============================================================================
# VALIDAÇÃO DE DEPENDÊNCIAS (OBRIGATÓRIO)
# ============================================================================
if 'PREMISSAS' not in globals():
    raise RuntimeError(
        "❌ ERRO CRÍTICO: PREMISSAS não carregadas!\n"
        "Execute a Célula 02 antes desta célula."
    )
# Nota: O Motor V13 usa o nome de função 'executar_motor_fintech_v10_production_ready' 
# por herança, mas contém a lógica V13.
if 'executar_motor_fintech_v10_production_ready' not in globals():
    raise RuntimeError(
        "❌ ERRO CRÍTICO: Motor V13 não encontrado!\n"
        "Execute a Célula 04 antes desta célula."
    )
MOTOR_FUNCTION = globals()['executar_motor_fintech_v10_production_ready']
MOTOR_VERSION = 'v13_stable'
if 'monte_carlo' not in PREMISSAS:
    raise RuntimeError(
        "❌ ERRO CRÍTICO: Configuração Monte Carlo não encontrada!\n"
        "Adicione o bloco PREMISSAS['monte_carlo'] na Célula 02."
    )
MC = PREMISSAS['monte_carlo']

# BLOCO 3: CONFIGURAÇÃO DE OUTPUTS
# ============================================================================
# SETUP DE OUTPUTS E LOGGING
# ============================================================================
os.makedirs(MC['save_folder'], exist_ok=True)
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_FILE = os.path.join(MC['save_folder'], f"mc_results_{TIMESTAMP}.pkl")
CHECKPOINT_FILE = os.path.join(MC['save_folder'], f"mc_checkpoint_{TIMESTAMP}.pkl")
CSV_FILE = os.path.join(MC['save_folder'], f"mc_results_{TIMESTAMP}.csv")
TXT_FILE = os.path.join(MC['save_folder'], f"mc_resumo_{TIMESTAMP}.txt")
print("="*80)
print("🎲 MONTE CARLO ENTERPRISE GOLD V4.1 - INICIALIZANDO")
print("="*80)
print(f"📅 Timestamp: {TIMESTAMP}")
print(f"🔧 Motor: {MOTOR_VERSION.upper()}")
print(f"⚙️  Config: PREMISSAS['monte_carlo']")
print(f"📁 Output: {MC['save_folder']}")
print(f"   • Pickle: {os.path.basename(OUTPUT_FILE)}")
print(f"   • CSV: {os.path.basename(CSV_FILE)}")
print(f"   • TXT: {os.path.basename(TXT_FILE)}")
print("="*80)

# BLOCO 4: HELPER FUNCTIONS
# ============================================================================
# FUNÇÕES AUXILIARES (ZERO HARDCODED)
# ============================================================================
def safe_extract(data, keys, fallback=np.nan):
    """
    Extrai valor de dict/DataFrame com tratamento robusto.
    Retorna np.nan se não encontrar ou valor for inválido.
    """
    for key in keys:
        try:
            if isinstance(data, dict) and key in data:
                val = data[key]
                if pd.isna(val) or np.isinf(val):
                    continue
                return float(val)
            if isinstance(data, pd.DataFrame) and key in data.columns:
                if len(data) == 0:
                    continue
                val = data[key].iloc[-1]
                if pd.isna(val) or np.isinf(val):
                    continue
                return float(val)
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            continue
    return fallback

# BLOCO 5: MATRIZ DE CORRELAÇÃO
def build_correlation_matrix(variaveis, correlacoes):
    """
    Constrói matriz de correlação válida (positiva definida).
    Usa Copula Gaussiana para correlações multivariadas.
    """
    n = len(variaveis)
    var_names = list(variaveis.keys())
    corr_matrix = np.eye(n)
    for (var1, var2), corr_val in correlacoes.items():
        if var1 not in var_names or var2 not in var_names:
            continue
        i = var_names.index(var1)
        j = var_names.index(var2)
        corr_val_clipped = np.clip(corr_val, -0.99, 0.99)
        corr_matrix[i, j] = corr_val_clipped
        corr_matrix[j, i] = corr_val_clipped
    try:
        cholesky(corr_matrix)
    except np.linalg.LinAlgError:
        print("⚠️  Matriz de correlação inválida. Usando identidade.")
        corr_matrix = np.eye(n)
    return corr_matrix, var_names

# BLOCO 6: PERTURBADOR DE PREMISSAS (PARTE 1)
def perturb_premissas_com_correlacao(base, sim_index, scenario='base'):
    """
    Gera premissas perturbadas com correlações e choques.
    Seed único por simulação garantido.
    """
    seed_offset = (sim_index * 9973 + hash(scenario)) % (2**31 - 1)
    seed = (MC['random_seed'] + seed_offset) % (2**31 - 1)
    rng = np.random.RandomState(seed)
    p = base.copy()
    variaveis = MC['variaveis']
    correlacoes = MC.get('correlacoes', {})
    if MC.get('enable_correlations', False) and correlacoes:
        corr_matrix, var_names = build_correlation_matrix(variaveis, correlacoes)
        n_vars = len(var_names)
        try:
            mean = np.zeros(n_vars)
            z_correlated = rng.multivariate_normal(mean, corr_matrix)
            z_correlated = np.clip(z_correlated, -6, 6)
            u_correlated = stats.norm.cdf(z_correlated)
        except (np.linalg.LinAlgError, ValueError):
            var_names = list(variaveis.keys())
            u_correlated = rng.uniform(0, 1, len(var_names))
    else:
        var_names = list(variaveis.keys())
        u_correlated = rng.uniform(0, 1, len(var_names))

# BLOCO 7: PERTURBADOR (PARTE 2 - APLICAÇÃO)
    scenario_mult = MC['cenarios'].get(scenario, {}).get('multiplicadores', {})
    for idx, var_name in enumerate(var_names):
        if var_name not in base:
            continue
        var_config = variaveis[var_name]
        base_val = base[var_name]
        base_val_adjusted = base_val * scenario_mult.get(var_name, 1.0)
        dist_type = var_config.get('dist', 'normal')
        std = var_config['std']
        vmin = var_config.get('min', 0)
        vmax = var_config.get('max', np.inf)
        try:
            if dist_type == 'normal':
                u_clipped = np.clip(u_correlated[idx], 1e-10, 1-1e-10)
                z = stats.norm.ppf(u_clipped)
                perturbed = base_val_adjusted + z * (base_val_adjusted * std)
            elif dist_type == 'lognormal':
                if base_val_adjusted <= 0:
                    perturbed = base_val_adjusted
                else:
                    mu = np.log(base_val_adjusted)
                    sigma = std
                    u_clipped = np.clip(u_correlated[idx], 1e-10, 1-1e-10)
                    z = stats.norm.ppf(u_clipped)
                    z_clipped = np.clip(z, -10, 10)
                    perturbed = np.exp(mu + sigma * z_clipped)
            elif dist_type == 'uniform':
                perturbed = vmin + u_correlated[idx] * (vmax - vmin)
            else:
                perturbed = base_val_adjusted
        except (OverflowError, ValueError, FloatingPointError):
            perturbed = base_val_adjusted
        perturbed = np.clip(perturbed, vmin, vmax)
        p[var_name] = float(perturbed)

# BLOCO 8: PERTURBADOR (PARTE 3 - FINALIZAÇÕES)
    for var_name, mult in scenario_mult.items():
        if var_name not in variaveis and var_name in p:
            p[var_name] = float(p[var_name] * mult)
    if 'mix_lite' in p and 'mix_trader' in p and 'mix_pro' in p:
        total_mix = p['mix_lite'] + p['mix_trader'] + p['mix_pro']
        if total_mix > 0:
            p['mix_lite'] /= total_mix
            p['mix_trader'] /= total_mix
            p['mix_pro'] /= total_mix
    choques = MC.get('choques', {})
    for choque_nome, choque_config in choques.items():
        if rng.random() < choque_config['probabilidade']:
            for param, efeito in choque_config['efeito'].items():
                if param not in p:
                    continue
                if isinstance(efeito, (int, float)) and efeito < 1:
                    p[param] *= efeito
                else:
                    p[param] = efeito
    return p, seed

# BLOCO 9: EXECUTOR DE SIMULAÇÃO
def run_single_simulation(sim_index, premissas_base, scenario='base'):
    """
    Executa uma simulação completa com timeout e error handling.
    Retorna dict com KPIs ou erro.
    """
    start_time = time.time()
    timeout = MC.get('timeout_seconds', 300)
    try:
        p_var, seed_used = perturb_premissas_com_correlacao(
            premissas_base, sim_index, scenario
        )
        # Executa o Motor V13 passando o ID da simulação
        df_m, df_a, metrics, alerts = MOTOR_FUNCTION(
            p_var,
            seed=seed_used,
            variacao_params=None,
            simulacao_id=sim_index
        )
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"Excedeu {timeout}s")
        
        result = {
            'sim': sim_index,
            'scenario': scenario,
            'seed': seed_used,
            'success': True,
            'time_elapsed': elapsed,
            'caixa_final': safe_extract(
                metrics, ['caixa_final'], 
                df_m['caixa'].iloc[-1] if len(df_m) > 0 else np.nan
            ),
            'mrr_final': safe_extract(
                metrics, ['mrr_final'],
                df_m['mrr'].iloc[-1] if len(df_m) > 0 else np.nan
            ),
            'arr_final': safe_extract(
                metrics, ['arr_final'],
                df_m['arr'].iloc[-1] if len(df_m) > 0 else np.nan
            ),
            'usuarios_final': int(safe_extract(
                metrics, ['usuarios_final'],
                df_m['usuarios_ativos'].iloc[-1] if len(df_m) > 0 else 0
            )),
            'cac_medio': safe_extract(
                metrics, ['cac_medio'],
                df_m['cac_blended'].replace([0, np.inf, -np.inf], np.nan).mean()
            ),
            'ltv_medio': safe_extract(
                metrics, ['ltv_medio', 'ltv_media'],
                df_m['ltv'].replace([0, np.inf, -np.inf], np.nan).mean()
            ),
            'churn_medio': safe_extract(
                metrics, ['churn_medio'],
                df_m['churn_rate'].mean() * 100 if len(df_m) > 0 else np.nan
            ),
            'margem_bruta_media': safe_extract(
                metrics, ['margem_bruta_media'],
                df_m['margem_bruta_pct'].mean() if len(df_m) > 0 else np.nan
            ),
            'ebitda_margin_media': safe_extract(
                metrics, ['ebitda_margin_media'],
                df_m['ebitda_margin'].mean() if len(df_m) > 0 else np.nan
            ),
            'nrr': safe_extract(metrics, ['nrr'], np.nan),
            'grr': safe_extract(metrics, ['grr'], np.nan),
            'cohort_m6_retention': safe_extract(metrics, ['cohort_m6_retention'], np.nan),
            'payback_meses_medio': safe_extract(metrics, ['payback_meses_medio'], np.nan),
            'roi_total_pct': safe_extract(metrics, ['roi_total_pct'], np.nan),
            'burn_rate_medio': safe_extract(
                metrics, ['burn_rate_medio'],
                df_m['burn_rate'].mean() if len(df_m) > 0 else np.nan
            ),
            'caixa_minimo': safe_extract(
                metrics, ['caixa_minimo'],
                df_m['caixa'].min() if len(df_m) > 0 else np.nan
            ),
            'mes_caixa_minimo': int(safe_extract(
                metrics, ['mes_caixa_minimo'],
                df_m['caixa'].idxmin() + 1 if len(df_m) > 0 else 0
            )),
            'runway_final': (
                df_m['runway_meses'].iloc[-1] 
                if len(df_m) > 0 and df_m['runway_meses'].iloc[-1] < 999 
                else np.nan
            ),
            'quebrou': bool(safe_extract(
                metrics, ['quebrou'],
                df_m['caixa'].min() < MC['kpis']['risco'].get('caixa_minimo_critico', 0)
                if len(df_m) > 0 else False
            )),
            'runway_critico': bool(
                # Pega do mês 6 em diante (.iloc[6:]) para ignorar o sufoco inicial
                df_m['runway_meses'].iloc[6:].min() < MC['kpis']['risco'].get('runway_minimo_alerta', 3)
                if len(df_m) > 6 else False
            ),
            'var95_caixa': safe_extract(metrics, ['var95_caixa'], np.nan),
            'cvar95_caixa': safe_extract(metrics, ['cvar95_caixa'], np.nan),
        }
        ltv_cac_motor = safe_extract(metrics, ['ltv_cac_medio', 'ltv_cac'], np.nan)
        if np.isnan(ltv_cac_motor) and result['cac_medio'] > 0:
            result['ltv_cac'] = result['ltv_medio'] / result['cac_medio']
        else:
            result['ltv_cac'] = ltv_cac_motor
        if MC.get('save_timeseries', False):
            result['caixa_series'] = df_m['caixa'].values.tolist()
            result['mrr_series'] = df_m['mrr'].values.tolist()
        return result
    except TimeoutError as e:
        return {
            'sim': sim_index, 'scenario': scenario, 'success': False,
            'error': f"TIMEOUT: {str(e)}", 'time_elapsed': time.time() - start_time
        }
    except OverflowError as e:
        return {
            'sim': sim_index, 'scenario': scenario, 'success': False,
            'error': "OVERFLOW: Valores numéricos excederam limites",
            'time_elapsed': time.time() - start_time
        }
    except Exception as e:
        return {
            'sim': sim_index, 'scenario': scenario, 'success': False,
            'error': str(e)[:500], 'time_elapsed': time.time() - start_time
        }

# BLOCO 10: VALIDAÇÃO PRÉVIA
# ============================================================================
# VALIDAÇÃO PRÉ-EXECUÇÃO (OBRIGATÓRIA)
# ============================================================================
if MC['validacao']['rodar_teste_previo']:
    print("\n🔍 VALIDAÇÃO PRÉVIA - Testando 1 simulação...")
    print("-"*80)
    test_result = run_single_simulation(0, PREMISSAS, 'base')
    if not test_result.get('success', False):
        print("❌ ERRO NA SIMULAÇÃO DE TESTE:")
        print(f"   {test_result.get('error', 'Erro desconhecido')}")
        if MC['validacao']['abort_se_teste_falhar']:
            print("\n⚠️  Abortando Monte Carlo")
            raise RuntimeError("Simulação de teste falhou")
        else:
            print("\n⚠️  Continuando (modo debug)")
    else:
        print(f"✅ Teste bem-sucedido!")
        print(f"   Tempo: {test_result['time_elapsed']:.2f}s")
        print(f"   MRR: R$ {test_result['mrr_final']:,.2f}")
        print(f"   Usuários: {test_result['usuarios_final']}")
        print(f"   Caixa: R$ {test_result['caixa_final']:,.2f}")
        print(f"   LTV/CAC: {test_result.get('ltv_cac', np.nan):.2f}")
    print("-"*80)

# BLOCO 11: SETUP EXECUÇÃO PRINCIPAL
# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================
print("\n" + "="*80)
print("🚀 INICIANDO SIMULAÇÃO MONTE CARLO")
print("="*80)
print(f"⚙️  Configuração:")
print(f"   • Simulações/cenário: {MC['n_simulacoes']}")
if MC['enable_scenarios']:
    scenarios = list(MC['cenarios'].keys())
    print(f"   • Cenários: {', '.join(scenarios)}")
else:
    scenarios = ['base']
    print(f"   • Cenário único: Base")
print(f"   • Correlações: {'Ativadas' if MC.get('enable_correlations', False) else 'Desativadas'}")
print(f"   • Choques: {len(MC.get('choques', {}))} tipos")
print(f"   • Checkpoint: cada {MC['checkpoint_every']} sims")
print(f"   • Timeout: {MC.get('timeout_seconds', 300)}s/sim")
print("="*80)
n_sims = MC['n_simulacoes']
total_tasks = len(scenarios) * n_sims
results = []
errors = []
start_time = time.time()
completed = 0
checkpoints_saved = 0
print(f"\n📊 Progresso: 0/{total_tasks} (0.0%)")
print("-"*80)

# BLOCO 12: LOOP PRINCIPAL
for scenario in scenarios:
    print(f"\n🎯 Cenário: {MC['cenarios'][scenario]['nome']}")
    print(f"   {MC['cenarios'][scenario]['descricao']}")
    for i in range(n_sims):
        result = run_single_simulation(i, PREMISSAS, scenario)
        if result.get('success', False):
            results.append(result)
        else:
            errors.append(result)
        completed += 1
        if completed % 10 == 0 or completed == total_tasks:
            elapsed = time.time() - start_time
            avg_time = elapsed / completed
            eta = avg_time * (total_tasks - completed)
            pct = (completed / total_tasks) * 100
            success_rate = (len(results) / completed) * 100
            print(f"   {completed}/{total_tasks} ({pct:.1f}%) | "
                  f"Tempo: {elapsed/60:.1f}min | ETA: {eta/60:.1f}min | "
                  f"Sucesso: {success_rate:.0f}% | Erros: {len(errors)}")
        if MC.get('output', {}).get('salvar_checkpoint', True):
            if completed % MC['checkpoint_every'] == 0:
                checkpoint_data = {
                    'completed': completed,
                    'total': total_tasks,
                    'results': results,
                    'errors': errors,
                    'timestamp': datetime.now().isoformat(),
                    'motor_version': MOTOR_VERSION,
                    'mc_config': MC
                }
                with open(CHECKPOINT_FILE, 'wb') as f:
                    pickle.dump(checkpoint_data, f)
                checkpoints_saved += 1
                print(f"   💾 Checkpoint #{checkpoints_saved} salvo")

# BLOCO 13: FINALIZAÇÃO E SUMÁRIO
total_time = time.time() - start_time
print()
print("="*80)
print("✅ SIMULAÇÃO CONCLUÍDA")
print("="*80)
print(f"⏱️  Tempo: {total_time/60:.1f} min")
print(f"✅ Sucessos: {len(results)} ({len(results)/total_tasks*100:.1f}%)")
print(f"❌ Erros: {len(errors)} ({len(errors)/total_tasks*100:.1f}%)")
print(f"💾 Checkpoints: {checkpoints_saved}")
print()

# BLOCO 14: ANÁLISE - SETUP
# ============================================================================
# ANÁLISE DE RESULTADOS
# ============================================================================
df_results = pd.DataFrame(results)
df_errors = pd.DataFrame(errors) if errors else pd.DataFrame()
if df_results.empty:
    print("❌ Nenhuma simulação bem-sucedida!")
else:
    print("="*80)
    print("📊 ANÁLISE POR CENÁRIO")
    print("="*80)

# BLOCO 15: ANÁLISE - LOOP CENÁRIOS
    for scenario in scenarios:
        df_scen = df_results[df_results['scenario'] == scenario]
        if df_scen.empty:
            continue
        print(f"\n🎯 {MC['cenarios'][scenario]['nome'].upper()}")
        print("-"*80)
        kpis_analise = {
            'MRR Final (R$)': 'mrr_final',
            'Usuários': 'usuarios_final',
            'Caixa Final (R$)': 'caixa_final',
            'LTV/CAC': 'ltv_cac',
            'ROI (%)': 'roi_total_pct',
            'NRR': 'nrr',
            'Payback (m)': 'payback_meses_medio',
            'Runway Final (m)': 'runway_final', # Novo KPI solicitado
        }
        print(f"{'KPI':<20} {'P10':>12} {'P50':>12} {'P90':>12} {'Média':>12}")
        print("-"*80)
        for kpi_label, kpi_col in kpis_analise.items():
            if kpi_col not in df_scen.columns:
                continue
            series = df_scen[kpi_col].replace([np.inf, -np.inf], np.nan).dropna()
            if len(series) == 0:
                continue
            p10 = np.percentile(series, 10)
            p50 = np.percentile(series, 50)
            p90 = np.percentile(series, 90)
            mean = series.mean()
            print(f"{kpi_label:<20} {p10:>12,.2f} {p50:>12,.2f} {p90:>12,.2f} {mean:>12,.2f}")

# BLOCO 16: ANÁLISE - RISCO
        print()
        print("⚠️  ANÁLISE DE RISCO")
        print("-"*80)
        prob_quebra = (df_scen['quebrou'].sum() / len(df_scen)) * 100
        prob_runway = (df_scen['runway_critico'].sum() / len(df_scen)) * 100
        status_quebra = "🟢" if prob_quebra < 5 else ("🟡" if prob_quebra < 15 else "🔴")
        status_runway = "🟢" if prob_runway < 10 else ("🟡" if prob_runway < 25 else "🔴")
        print(f"{status_quebra} Prob. Quebra:        {prob_quebra:>6.1f}%")
        print(f"{status_runway} Prob. Runway < 3m:   {prob_runway:>6.1f}%")
        var_series = df_scen['var95_caixa'].replace([np.inf, -np.inf], np.nan).dropna()
        if len(var_series) > 0:
            var_mean = var_series.mean()
            cvar_series = df_scen['cvar95_caixa'].replace([np.inf, -np.inf], np.nan).dropna()
            cvar_mean = cvar_series.mean() if len(cvar_series) > 0 else np.nan
            print(f"📉 VaR 95%:             R$ {var_mean:>10,.2f}")
            if not np.isnan(cvar_mean):
                print(f"📉 CVaR 95%:            R$ {cvar_mean:>10,.2f}")

# BLOCO 17: EXPORTAÇÃO - PICKLE
# ============================================================================
# EXPORTAÇÃO DE RESULTADOS
# ============================================================================
output_data = {
    'timestamp': TIMESTAMP,
    'motor_version': MOTOR_VERSION,
    'config': MC,
    'premissas': PREMISSAS,
    'results': df_results,
    'errors': df_errors,
    'execution_time_minutes': total_time / 60,
    'summary': {
        'total_tasks': total_tasks,
        'successful': len(results),
        'failed': len(errors),
        'success_rate_pct': (len(results) / total_tasks) * 100 if total_tasks > 0 else 0,
        'scenarios_run': scenarios,
    }
}
with open(OUTPUT_FILE, 'wb') as f:
    pickle.dump(output_data, f)
print(f"\n💾 Pickle: {OUTPUT_FILE}")

# BLOCO 18: EXPORTAÇÃO - CSV
if MC.get('output', {}).get('salvar_csv', True) and not df_results.empty:
    df_results.to_csv(CSV_FILE, index=False)
    print(f"💾 CSV: {CSV_FILE}")

# BLOCO 19: EXPORTAÇÃO - TXT
if MC.get('output', {}).get('salvar_resumo_txt', True):
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("MONTE CARLO ENTERPRISE - RELATÓRIO EXECUTIVO\n")
        f.write("="*80 + "\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Motor: {MOTOR_VERSION}\n")
        f.write(f"Tempo: {total_time/60:.1f} min\n")
        f.write(f"Simulações: {len(results)}/{total_tasks}\n")
        f.write(f"Sucesso: {(len(results)/total_tasks)*100:.1f}%\n\n")
        for scenario in scenarios:
            df_s = df_results[df_results['scenario'] == scenario]
            if df_s.empty:
                continue
            f.write(f"\nCENÁRIO: {MC['cenarios'][scenario]['nome']}\n")
            f.write("-"*80 + "\n")
            f.write(f"MRR (Med): R$ {df_s['mrr_final'].median():,.2f}\n")
            f.write(f"Usuários (Med): {df_s['usuarios_final'].median():.0f}\n")
            f.write(f"Prob. Quebra: {(df_s['quebrou'].sum()/len(df_s))*100:.1f}%\n")
    print(f"💾 TXT: {TXT_FILE}")

# BLOCO 20: FINALIZAÇÃO
print()
print("="*80)
print("✅ EXPORTAÇÃO COMPLETA")
print("="*80)
print()
print("✅ Variáveis criadas:")
print("   • mc_data: Dict completo")
print("   • mc_results: DataFrame resultados")
print("   • mc_errors: DataFrame erros")
print()

# BLOCO 21: GLOSSÁRIO TÉCNICO
# ============================================================================
# GLOSSÁRIO DE TERMOS FINANCEIROS
# ============================================================================
print("📚 GLOSSÁRIO TÉCNICO (ENTENDENDO OS DADOS)")
print("="*80)
glossario = {
    "Runway (Pista de Pouso)": "Meses que a empresa sobrevive com o caixa atual e custos atuais sem nova receita. Se negativo, indica quebra.",
    "Burn Rate (Taxa de Queima)": "Quanto dinheiro a empresa perde (queima) por mês. Se positivo, a empresa está gastando caixa.",
    "VaR 95% (Value at Risk)": "O 'Pior Caso Comum'. Indica que em 95% dos casos, o caixa não será pior que este valor.",
    "CVaR 95% (Conditional VaR)": "A média dos 5% piores cenários. É o 'fundo do poço' se tudo der muito errado.",
    "MRR (Monthly Recurring Rev)": "Receita Recorrente Mensal. O valor das assinaturas ativas naquele mês.",
    "NRR (Net Revenue Retention)": "Retenção de Receita Líquida. > 1.00 significa que upgrades superam cancelamentos.",
    "LTV (Lifetime Value)": "Lucro bruto total que um cliente gera durante toda sua vida na empresa.",
    "CAC (Customer Acq Cost)": "Custo para adquirir um novo cliente pagante (Marketing + Vendas).",
    "LTV/CAC": "Índice de eficiência. Quantas vezes o lucro do cliente paga seu custo de aquisição. Ideal > 3.0.",
    "P10 / P50 / P90": "Percentis estatísticos. P10 = Cenário Pessimista (10%), P50 = Mediana (Cenário Base), P90 = Otimista (90%)."
}
for termo, definicao in glossario.items():
    print(f"🔹 {termo}:")
    print(f"   {definicao}")
print("="*80)
print("🎯 Próximo: Célula 06 (Dashboard)")
print("="*80)
mc_data = output_data
mc_results = df_results
mc_errors = df_errors