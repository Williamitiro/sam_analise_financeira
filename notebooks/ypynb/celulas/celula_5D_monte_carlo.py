# CÉLULA 5D - MONTE CARLO ENTERPRISE GOLD STANDARD V4.2 (MODULARIZADA)
# ============================================================================
# CORREÇÕES APLICADAS:
# 1. ✅ Modularização em função
# 2. ✅ Compatibilidade Motor V13
# ============================================================================
import os
import sys
import time
import pickle
import warnings
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import cholesky
import traceback

# Adiciona diretório atual para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None

try:
    from celula_4_motor import executar_motor_fintech_v10_production_ready
    from celula_2_premissas import PREMISSAS
except ImportError:
    pass

MOTOR_VERSION = 'v13_stable'

# BLOCO 4: HELPER FUNCTIONS
def safe_extract(data, keys, fallback=np.nan):
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

def build_correlation_matrix(variaveis, correlacoes):
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

def perturb_premissas_com_correlacao(base, sim_index, mc_config, scenario='base'):
    seed_offset = (sim_index * 9973 + hash(scenario)) % (2**31 - 1)
    seed = (mc_config['random_seed'] + seed_offset) % (2**31 - 1)
    rng = np.random.RandomState(seed)
    p = base.copy()
    variaveis = mc_config['variaveis']
    correlacoes = mc_config.get('correlacoes', {})
    
    if mc_config.get('enable_correlations', False) and correlacoes:
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
        
    scenario_mult = mc_config['cenarios'].get(scenario, {}).get('multiplicadores', {})
    
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
        
    for var_name, mult in scenario_mult.items():
        if var_name not in variaveis and var_name in p:
            p[var_name] = float(p[var_name] * mult)
            
    if 'mix_lite' in p and 'mix_trader' in p and 'mix_pro' in p:
        total_mix = p['mix_lite'] + p['mix_trader'] + p['mix_pro']
        if total_mix > 0:
            p['mix_lite'] /= total_mix
            p['mix_trader'] /= total_mix
            p['mix_pro'] /= total_mix
            
    choques = mc_config.get('choques', {})
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

def run_single_simulation(sim_index, premissas_base, mc_config, scenario='base', motor_func=None):
    if motor_func is None:
        raise ValueError("Função do motor não fornecida")
        
    start_time = time.time()
    timeout = mc_config.get('timeout_seconds', 300)
    
    try:
        p_var, seed_used = perturb_premissas_com_correlacao(
            premissas_base, sim_index, mc_config, scenario
        )
        
        df_m, df_a, metrics, alerts = motor_func(
            p_var,
            seed=seed_used,
            variacao_params=None,
            simulacao_id=sim_index
        )
        
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"Excedeu {timeout}s")
        
        result = {
            'sim': sim_index, 'scenario': scenario, 'seed': seed_used,
            'success': True, 'time_elapsed': elapsed,
            'caixa_final': safe_extract(metrics, ['caixa_final'], df_m['caixa'].iloc[-1] if len(df_m) > 0 else np.nan),
            'mrr_final': safe_extract(metrics, ['mrr_final'], df_m['mrr'].iloc[-1] if len(df_m) > 0 else np.nan),
            'arr_final': safe_extract(metrics, ['arr_final'], df_m['arr'].iloc[-1] if len(df_m) > 0 else np.nan),
            'usuarios_final': int(safe_extract(metrics, ['usuarios_final'], df_m['usuarios_ativos'].iloc[-1] if len(df_m) > 0 else 0)),
            'cac_medio': safe_extract(metrics, ['cac_medio'], df_m['cac_blended'].replace([0, np.inf, -np.inf], np.nan).mean()),
            'ltv_medio': safe_extract(metrics, ['ltv_medio', 'ltv_media'], df_m['ltv'].replace([0, np.inf, -np.inf], np.nan).mean()),
            'churn_medio': safe_extract(metrics, ['churn_medio'], df_m['churn_rate'].mean() if len(df_m) > 0 else np.nan),
            'margem_bruta_media': safe_extract(metrics, ['margem_bruta_media'], df_m['margem_bruta_pct'].mean() if len(df_m) > 0 else np.nan),
            'ebitda_margin_media': safe_extract(metrics, ['ebitda_margin_media'], df_m['ebitda_margin'].mean() if len(df_m) > 0 else np.nan),
            'nrr': safe_extract(metrics, ['nrr'], np.nan),
            'burn_rate_medio': safe_extract(metrics, ['burn_rate_medio'], df_m['burn_rate'].mean() if len(df_m) > 0 else np.nan),
            'runway_final': (df_m['runway_meses'].iloc[-1] if len(df_m) > 0 and df_m['runway_meses'].iloc[-1] < 999 else np.nan),
            'quebrou': bool(safe_extract(metrics, ['quebrou'], df_m['caixa'].min() < mc_config['kpis']['risco'].get('caixa_minimo_critico', 0) if len(df_m) > 0 else False)),
            'runway_critico': bool(df_m['runway_meses'].iloc[6:].min() < mc_config['kpis']['risco'].get('runway_minimo_alerta', 3) if len(df_m) > 6 else False),
            'var95_caixa': safe_extract(metrics, ['var95_caixa'], np.nan),
            'cvar95_caixa': safe_extract(metrics, ['cvar95_caixa'], np.nan),
            'roi_total_pct': safe_extract(metrics, ['roi_total_pct'], np.nan),
            'payback_meses_medio': safe_extract(metrics, ['payback_meses_medio'], np.nan)
        }
        
        ltv_cac_motor = safe_extract(metrics, ['ltv_cac_medio', 'ltv_cac'], np.nan)
        if np.isnan(ltv_cac_motor) and result['cac_medio'] > 0:
            result['ltv_cac'] = result['ltv_medio'] / result['cac_medio']
        else:
            result['ltv_cac'] = ltv_cac_motor
            
        if mc_config.get('save_timeseries', True):
            result['caixa_series'] = df_m['caixa'].values.tolist()
            result['mrr_series'] = df_m['mrr'].values.tolist()
            
        return result
        
    except (TimeoutError, OverflowError, Exception) as e:
         return {
            'sim': sim_index, 'scenario': scenario, 'success': False,
            'error': str(e)[:500], 'time_elapsed': time.time() - start_time
        }

def executar_monte_carlo(premissas, motor_func=None):
    """
    Executa o Monte Carlo Modularizado.
    """
    if 'monte_carlo' not in premissas:
        raise RuntimeError("Config 'monte_carlo' ausente nas premissas.")

    # Se motor_func não passado, tenta pegar do globals ou do import
    if motor_func is None:
        if 'executar_motor_fintech_v10_production_ready' in globals():
            motor_func = globals()['executar_motor_fintech_v10_production_ready']
        else:
             # Tenta importar dinamicamente (já deve ter sido importado pelo try/except, mas por segurança)
             try:
                 from celula_4_motor import executar_motor_fintech_v10_production_ready
                 motor_func = executar_motor_fintech_v10_production_ready
             except ImportError:
                 raise RuntimeError("Motor financeiro não disponível.")

    mc = premissas['monte_carlo']
    os.makedirs(mc['save_folder'], exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_files = {
        'pickle': os.path.join(mc['save_folder'], f"mc_results_{timestamp}.pkl"),
        'csv': os.path.join(mc['save_folder'], f"mc_results_{timestamp}.csv"),
        'txt': os.path.join(mc['save_folder'], f"mc_resumo_{timestamp}.txt")
    }

    print("="*80)
    print("🎲 MONTE CARLO ENTERPRISE V4.2 - INICIALIZANDO")
    print("="*80)
    
    # Validação Prévia
    if mc['validacao']['rodar_teste_previo']:
        print("\n🔍 VALIDAÇÃO PRÉVIA...")
        test_result = run_single_simulation(0, premissas, mc, 'base', motor_func)
        if not test_result.get('success', False):
            print(f"❌ ERRO: {test_result.get('error')}")
            if mc['validacao']['abort_se_teste_falhar']:
                raise RuntimeError("Teste falhou.")
        else:
             print("✅ Teste Ok!")
             
    # Loop Principal
    print(f"\n🚀 Rodando {mc['n_simulacoes']} simulações...")
    
    scenarios = list(mc['cenarios'].keys()) if mc['enable_scenarios'] else ['base']
    results = []
    errors = []
    
    start_time = time.time()
    
    for scenario in scenarios:
        for i in range(mc['n_simulacoes']):
            res = run_single_simulation(i, premissas, mc, scenario, motor_func)
            if res.get('success', False):
                results.append(res)
            else:
                errors.append(res)
                
    total_time = time.time() - start_time
    
    # Exportação e Reports
    df_results = pd.DataFrame(results)
    
    output_data = {
        'timestamp': timestamp,
        'config': mc,
        'results': df_results,
        'errors': errors
    }
    
    with open(output_files['pickle'], 'wb') as f:
        pickle.dump(output_data, f)
        
    print(f"\n✅ CONCLUÍDO em {total_time/60:.1f} min. Sucessos: {len(results)}")
    
    return output_data, df_results

# Execução direta
if __name__ == "__main__":
    if 'PREMISSAS' in globals():
        p = PREMISSAS
    else:
        try:
            from celula_2_premissas import PREMISSAS as p
        except:
            p = {}
            
    executar_monte_carlo(p)