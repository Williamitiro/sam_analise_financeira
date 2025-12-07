import sys
import os
import pandas as pd
import numpy as np

# Adiciona o diretório notebooks ao path para importar o módulo
sys.path.append(os.path.abspath("notebooks"))

try:
    from modelo2_v7 import executar_pagina_2_growth_machine
except ImportError:
    # Se rodar de dentro de notebooks/
    sys.path.append(os.path.abspath("."))
    from modelo2_v7 import executar_pagina_2_growth_machine

def criar_dados_mock():
    """Cria DataFrames falsos para teste de plotagem."""
    print("🛠️ Criando dados mock...")
    
    # Premissas
    premissas = {}
    
    # 1. Mensal (36 meses)
    meses = list(range(1, 37))
    df_m = pd.DataFrame({
        'mes': meses,
        'trafego_total': np.linspace(1000, 50000, 36),
        'trials_total': np.linspace(100, 5000, 36),
        'novos_pagantes_total': np.linspace(10, 500, 36),
        'usuarios_ativos': np.linspace(10, 10000, 36),
        'ltv_cac': np.linspace(1.5, 4.5, 36),
        'gasto_marketing': np.linspace(5000, 100000, 36),
        'cac_blended': np.linspace(300, 150, 36),
        'mrr': np.linspace(1000, 500000, 36),
        'churn_mrr': np.linspace(50, 20000, 36) * -1, # values usually negative in prompt but kept positive for logic
        'churn_rate': np.random.uniform(0.04, 0.08, 36)
    })
    # Ajuste churn logic (viz expects positive churn_rate, positive churn_mrr for calculation)
    df_m['churn_mrr'] = np.abs(df_m['churn_mrr']) 
    
    # 2. Semanal (26 semanas)
    semanas = list(range(1, 27))
    df_s = pd.DataFrame({
        'semana': semanas,
        'cac_blended': np.random.normal(200, 50, 26) # Mean 200, Std 50
    })
    
    # 3. Ideal (Benchmarks) - Clone do real com melhoria
    df_ideal = df_m.copy()
    df_ideal['novos_pagantes_total'] *= 1.2
    df_ideal['usuarios_ativos'] *= 1.2
    
    df_ideal_s = df_s.copy()
    
    return df_m, df_s, df_ideal, df_ideal_s, premissas

if __name__ == "__main__":
    print("🧪 INICIANDO TESTE DE VERIFICAÇÃO: MODELO 2 V7\n")
    
    # 1. Cria dados
    df_real_m, df_real_s, df_ideal, df_ideal_s, premissas = criar_dados_mock()
    
    # 2. Executa função principal
    try:
        print("\n\n🧪 [TESTE 1] MODO NOTEBOOK INTERATIVO (HTML/CSS):")
        executar_pagina_2_growth_machine(df_real_m, df_real_s, df_ideal, df_ideal_s, premissas)

        print("\n\n🧪 [TESTE 2] MODO RELATÓRIO PDF (MARKDOWN/CLEAN):")
        # Redireciona stdout para evitar poluição no teste, já que report_mode deve ser silencioso
        executar_pagina_2_growth_machine(df_real_m, df_real_s, df_ideal, df_ideal_s, premissas, report_mode=True)
        
        print("\n✅ SUCESSO! A função rodou sem erros em ambos os modos.")
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

    # 3. Verifica arquivos
    expected_files = [
        "outputs/figs/pg2_viz1_funil_macro.png",
        "outputs/figs/pg2_viz2_ltv_cac.png",
        "outputs/figs/pg2_viz3_controle_semanal.png",
        "outputs/figs/pg2_viz4_elasticidade.png",
        "outputs/figs/pg2_viz5_churn_custo.png"
    ]
    
    print("\n📂 Verificando arquivos gerados:")
    all_exist = True
    for f in expected_files:
        exists = os.path.exists(f)
        status = "OK" if exists else "FALTOU"
        print(f"   - {f}: {status}")
        if not exists: all_exist = False
        
    if all_exist:
        print("\n🎉 TODOS OS ARQUIVOS FORAM GERADOS!")
    else:
        print("\n⚠️ ALGUNS ARQUIVOS ESTÃO FALTANDO.")
