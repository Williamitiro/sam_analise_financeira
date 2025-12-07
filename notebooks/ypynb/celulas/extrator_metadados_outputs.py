# EXTRATOR DE METADADOS - COLE E EXECUTE NO NOTEBOOK
# =============================================================================
# Este script extrai TODA a estrutura de dados disponível no notebook e salva
# em um arquivo JSON para análise. Executar APÓS as células 05A, 05B e 5D.
# =============================================================================

import json
import numpy as np
import pandas as pd
from datetime import datetime

def extrair_metadados_notebook():
    """
    Extrai metadados completos de todas as variáveis disponíveis no notebook.
    Gera um arquivo JSON com estrutura, colunas, valores de exemplo, etc.
    """
    
    metadata = {
        "data_extracao": datetime.now().isoformat(),
        "versao": "1.0",
        "variaveis_encontradas": {},
        "dataframes": {},
        "dicionarios": {},
        "erros": []
    }
    
    # Lista de variáveis para verificar
    variaveis_alvo = [
        'df_real_m', 'df_real_a', 'met_real', 'alertas_real',
        'df_ideal', 'df_ideal_anual', 'met_ideal', 'alertas_ideal',
        'mc_results', 'mc_errors', 'mc_data',
        'PREMISSAS'
    ]
    
    # Verificar quais existem
    for var in variaveis_alvo:
        if var in globals():
            metadata["variaveis_encontradas"][var] = True
        else:
            metadata["variaveis_encontradas"][var] = False
    
    # ==========================================================================
    # EXTRAIR df_real_m (Principal)
    # ==========================================================================
    if 'df_real_m' in globals():
        df = df_real_m
        
        # Snapshots de meses chave
        def safe_get(df, idx, col):
            try:
                val = df.iloc[idx][col]
                if pd.isna(val):
                    return None
                if isinstance(val, (np.floating, np.integer)):
                    return float(val)
                return val
            except:
                return None
        
        # Índices: 0=M1, 5=M6, 11=M12, -1=M36
        metadata["dataframes"]["df_real_m"] = {
            "shape": list(df.shape),
            "colunas": list(df.columns),
            "tipos_colunas": {col: str(df[col].dtype) for col in df.columns},
            "indice": list(df.index) if len(df.index) <= 50 else list(df.index[:10]) + ["..."] + list(df.index[-5:]),
            "snapshots": {
                "M1": {col: safe_get(df, 0, col) for col in df.columns},
                "M6": {col: safe_get(df, min(5, len(df)-1), col) for col in df.columns},
                "M12": {col: safe_get(df, min(11, len(df)-1), col) for col in df.columns},
                "M36": {col: safe_get(df, -1, col) for col in df.columns}
            },
            "estatisticas": {
                col: {
                    "min": float(df[col].min()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    "max": float(df[col].max()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    "mean": float(df[col].mean()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    "nulos": int(df[col].isna().sum())
                } for col in df.columns
            }
        }
        
        # Métricas chave resumidas (para fácil acesso)
        colunas_chave = ['mrr', 'usuarios_ativos', 'caixa', 'churn_rate', 'cac_blended', 
                         'ltv', 'ltv_cac', 'runway_meses', 'burn_rate', 'lucro_liquido',
                         'receita_bruta', 'margem_bruta_pct', 'ebitda', 'arr']
        
        metadata["dataframes"]["df_real_m"]["valores_chave_m36"] = {}
        for col in colunas_chave:
            if col in df.columns:
                metadata["dataframes"]["df_real_m"]["valores_chave_m36"][col] = safe_get(df, -1, col)
            else:
                metadata["dataframes"]["df_real_m"]["valores_chave_m36"][col] = "COLUNA_NAO_EXISTE"
    
    # ==========================================================================
    # EXTRAIR df_ideal (se existir)
    # ==========================================================================
    if 'df_ideal' in globals():
        df = df_ideal
        metadata["dataframes"]["df_ideal"] = {
            "shape": list(df.shape),
            "colunas": list(df.columns),
            "valores_chave_m36": {}
        }
        colunas_chave = ['mrr', 'usuarios_ativos', 'caixa', 'churn_rate', 'ltv_cac']
        for col in colunas_chave:
            if col in df.columns:
                try:
                    val = df.iloc[-1][col]
                    metadata["dataframes"]["df_ideal"]["valores_chave_m36"][col] = float(val) if not pd.isna(val) else None
                except:
                    metadata["dataframes"]["df_ideal"]["valores_chave_m36"][col] = None
    
    # ==========================================================================
    # EXTRAIR mc_results (Monte Carlo)
    # ==========================================================================
    if 'mc_results' in globals():
        df = mc_results
        metadata["dataframes"]["mc_results"] = {
            "shape": list(df.shape),
            "colunas": list(df.columns),
            "tipos_colunas": {col: str(df[col].dtype) for col in df.columns},
            "exemplo_primeira_linha": {col: (float(df.iloc[0][col]) if pd.api.types.is_numeric_dtype(df[col]) else str(df.iloc[0][col])) for col in df.columns}
        }
        
        # Estatísticas por cenário (se existir coluna cenario)
        if 'cenario' in df.columns:
            metadata["dataframes"]["mc_results"]["cenarios_unicos"] = list(df['cenario'].unique())
            
            # Percentis por cenário
            for cenario in df['cenario'].unique():
                df_cen = df[df['cenario'] == cenario]
                metadata["dataframes"]["mc_results"][f"percentis_{cenario}"] = {}
                
                for col in ['mrr_final', 'caixa_final', 'usuarios_final', 'ltv_cac_medio', 'roi_total_pct']:
                    if col in df_cen.columns:
                        metadata["dataframes"]["mc_results"][f"percentis_{cenario}"][col] = {
                            "p10": float(df_cen[col].quantile(0.10)),
                            "p50": float(df_cen[col].quantile(0.50)),
                            "p90": float(df_cen[col].quantile(0.90)),
                            "media": float(df_cen[col].mean())
                        }
    
    # ==========================================================================
    # EXTRAIR met_real (dicionário de métricas)
    # ==========================================================================
    if 'met_real' in globals():
        def converter_para_serializavel(obj):
            if isinstance(obj, (np.floating, np.integer)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            return obj
        
        metadata["dicionarios"]["met_real"] = {
            k: converter_para_serializavel(v) for k, v in met_real.items()
        }
    
    # ==========================================================================
    # EXTRAIR met_ideal (se existir)
    # ==========================================================================
    if 'met_ideal' in globals():
        def converter_para_serializavel(obj):
            if isinstance(obj, (np.floating, np.integer)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            return obj
        
        metadata["dicionarios"]["met_ideal"] = {
            k: converter_para_serializavel(v) for k, v in met_ideal.items()
        }
    
    # ==========================================================================
    # EXTRAIR PREMISSAS (algumas chaves importantes)
    # ==========================================================================
    if 'PREMISSAS' in globals():
        chaves_importantes = [
            'meses_projecao', 'usuarios_pagos_iniciais', 'caixa_inicial',
            'preco_lite', 'preco_trader', 'preco_pro',
            'mix_lite', 'mix_trader', 'mix_pro',
            'churn_inicial', 'churn_maturidade', 'churn_base',
            'marketing_fixo_mensal', 'trafego_inicial',
            'benchmark_ltv_cac_excelente', 'benchmark_ltv_cac_atencao',
            'benchmark_churn_atencao_pct', 'benchmark_churn_critico_pct',
            'meta_mrr_m6', 'meta_mrr_m12', 'meta_mrr_m36',
            'growth_m1_6_base', 'growth_m7_12_base'
        ]
        
        metadata["dicionarios"]["PREMISSAS_SELECIONADAS"] = {}
        for chave in chaves_importantes:
            if chave in PREMISSAS:
                val = PREMISSAS[chave]
                if isinstance(val, (np.floating, np.integer)):
                    metadata["dicionarios"]["PREMISSAS_SELECIONADAS"][chave] = float(val)
                else:
                    metadata["dicionarios"]["PREMISSAS_SELECIONADAS"][chave] = val
            else:
                metadata["dicionarios"]["PREMISSAS_SELECIONADAS"][chave] = "NAO_EXISTE"
    
    # ==========================================================================
    # RESUMO EXECUTIVO (para fácil leitura)
    # ==========================================================================
    if 'df_real_m' in globals():
        df = df_real_m
        m36 = df.iloc[-1]
        
        metadata["resumo_executivo"] = {
            "cenario": "REAL (Bootstrap)",
            "periodo": f"{len(df)} meses",
            "mrr_final": float(m36['mrr']) if 'mrr' in m36 else None,
            "arr_final": float(m36['mrr'] * 12) if 'mrr' in m36 else None,
            "usuarios_final": int(m36['usuarios_ativos']) if 'usuarios_ativos' in m36 else None,
            "caixa_final": float(m36['caixa']) if 'caixa' in m36 else None,
            "churn_final": float(m36['churn_rate']) if 'churn_rate' in m36 else None,
            "ltv_cac_final": float(m36['ltv_cac']) if 'ltv_cac' in m36 and not pd.isna(m36['ltv_cac']) else None,
            "runway_final": float(m36['runway_meses']) if 'runway_meses' in m36 else None,
            "burn_rate_final": float(m36['burn_rate']) if 'burn_rate' in m36 else None
        }
    
    # Salvar JSON
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    caminho = 'data/METADADOS_NOTEBOOK_COMPLETO.json'
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
    
    print("=" * 70)
    print("✅ METADADOS EXTRAÍDOS COM SUCESSO!")
    print("=" * 70)
    print(f"📁 Arquivo salvo: {caminho}")
    print()
    print("📊 RESUMO RÁPIDO:")
    print("-" * 70)
    
    if "resumo_executivo" in metadata:
        r = metadata["resumo_executivo"]
        print(f"   MRR M36:        {r.get('mrr_final', 'N/A')}")
        print(f"   Usuários M36:   {r.get('usuarios_final', 'N/A')}")
        print(f"   Caixa M36:      {r.get('caixa_final', 'N/A')}")
        print(f"   Churn M36:      {r.get('churn_final', 'N/A')}")
        print(f"   LTV/CAC M36:    {r.get('ltv_cac_final', 'N/A')}")
        print(f"   Runway M36:     {r.get('runway_final', 'N/A')}")
    
    print("-" * 70)
    print()
    print("🔍 Variáveis encontradas:")
    for var, existe in metadata["variaveis_encontradas"].items():
        status = "✅" if existe else "❌"
        print(f"   {status} {var}")
    
    print()
    print("=" * 70)
    print("📋 Agora copie o arquivo METADADOS_NOTEBOOK_COMPLETO.json")
    print("   e compartilhe comigo para análise.")
    print("=" * 70)
    
    return metadata

# EXECUTAR
metadados = extrair_metadados_notebook()
