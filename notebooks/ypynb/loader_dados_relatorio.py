# ============================================================================
# LOADER DADOS RELATÓRIO - ORQUESTRADOR PRINCIPAL (V1.0)
# ============================================================================
# OBJETIVO: Importar módulos, rodar simulações e gerar outputs para o relatório.
# DATA: 2025-12-07
# ============================================================================

import os
import sys
import warnings
import pandas as pd

# Adiciona diretório 'celulas' ao path para permitir imports
current_dir = os.path.dirname(os.path.abspath(__file__))
celulas_dir = os.path.join(current_dir, 'celulas')
if celulas_dir not in sys.path:
    sys.path.append(celulas_dir)

# Imports dos Módulos Refatorados
try:
    from celula_2_premissas import PREMISSAS
    from celula_5A_bootstrap_real import executar_analise_real
    from celula_5B_cenario_ideal import executar_analise_ideal
    from celula_5D_monte_carlo import executar_monte_carlo
    from PAGINA_1_COCKPIT_V4 import executar_pagina_1
    from PAGINA_2_GROWTH import executar_pagina_2_growth_machine
    from PAGINA_3_FINANCEIRO import executar_pagina_3_financeiro
except ImportError as e:
    print(f"❌ ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
    print("Verifique se o path está correto e se os arquivos __init__.py existem se necessário (embora sys.path resolva).")
    sys.exit(1)

def main(report_mode=True, run_monte_carlo=False):
    """
    Função Mestre que gera todos os dados para o Relatório de Investidores.
    
    Args:
        report_mode (bool): Se True, gera outputs otimizados para PDF (Markdown, sem logs excessivos).
        run_monte_carlo (bool): Se True, roda a simulação de Monte Carlo (pode demorar).
    """
    print("="*80)
    print("🚀 ORQUESTADOR DE RELATÓRIO - INICIANDO GERAÇÃO")
    print(f"   Modo Relatório: {report_mode}")
    print(f"   Monte Carlo: {run_monte_carlo}")
    print("="*80)
    
    warnings.filterwarnings('ignore')
    
    # 1. CARREGAR E CONFIGURAR PREMISSAS
    # (PREMISSAS já importado, mas poderíamos recarregar ou ajustar aqui)
    print("\n📦 1. PREMISSAS CARREGADAS")
    
    # 2. CENÁRIO REAL (Bootstrap + Simulação)
    print("\n⚙️  2. EXECUTANDO CENÁRIO REAL...")
    df_real_m, _, df_real_s, _, met_real, _ = executar_analise_real(PREMISSAS)
    print("   ✅ Cenário Real concluído.")
    
    # 3. CENÁRIO IDEAL (Benchmarks)
    print("\n⚙️  3. EXECUTANDO CENÁRIO IDEAL...")
    df_ideal_m, _, df_ideal_s, _, met_ideal, _ = executar_analise_ideal(PREMISSAS)
    print("   ✅ Cenário Ideal concluído.")
    
    # 4. MONTE CARLO (Opcional - demora mais)
    if run_monte_carlo:
        print("\n⚙️  4. EXECUTANDO MONTE CARLO...")
        mc_results, df_mc = executar_monte_carlo(PREMISSAS)
        print("   ✅ Monte Carlo concluído.")
    else:
        print("\n⏭️  4. MONTE CARLO PULADO (run_monte_carlo=False)")
        mc_results = None
    
    # 5. GERAR PÁGINA 1: COCKPIT
    # Nota: executar_pagina_1 espera (df_real_m, df_ideal, met_real, met_ideal)
    # Ajuste: PAGINA_1_COCKPIT pode precisar de tratamento de argumentos se met_real for diferente do esperado.
    # Assumindo compatibilidade.
    executar_pagina_1(
        df_real_m=df_real_m, 
        df_ideal=df_ideal_m, 
        met_real=met_real, 
        met_ideal=met_ideal,
        report_mode=report_mode
    )
    
    # 6. GERAR PÁGINA 2: GROWTH MACHINE
    executar_pagina_2_growth_machine(
        df_real_m=df_real_m,
        df_real_s=df_real_s,
        df_ideal=df_ideal_m,
        df_ideal_s=df_ideal_s,
        premissas=PREMISSAS,
        report_mode=report_mode
    )
    
    # 7. GERAR PÁGINA 3: FINANCEIRO (DRE + Custos + Fluxo de Caixa)
    executar_pagina_3_financeiro(
        df_real_m=df_real_m,
        df_real_s=df_real_s,
        df_ideal_m=df_ideal_m,
        premissas=PREMISSAS,
        report_mode=report_mode
    )
    
    print("\n" + "="*80)
    print("✅ GERAÇÃO DE RELATÓRIO CONCLUÍDA COM SUCESSO!")
    print("="*80)

if __name__ == "__main__":
    # Configuração simples via argumentos de linha de comando poderia ser adicionada aqui
    # Por padrão, roda em modo relatório e SEM Monte Carlo para ser rápido.
    main(report_mode=True, run_monte_carlo=False)
