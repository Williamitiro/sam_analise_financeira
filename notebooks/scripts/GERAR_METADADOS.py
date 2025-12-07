#!/usr/bin/env python3
# =============================================================================
# GERADOR DE METADADOS - EXECUTE APÓS AS CÉLULAS 5, 6, 7
# =============================================================================
# Uso: Cole este arquivo como uma célula no final do seu notebook
# Ele extrai TODAS as colunas, valores e estrutura das variáveis
#
# Gera 3 arquivos JSON:
#   1. METADADOS_NOTEBOOK_COMPLETO.json
#   2. COLUNAS_DETALHADAS.json
#   3. ESTRUTURA_NOTEBOOK_ATUALIZADO.json (atualiza o arquivo original)
# =============================================================================

import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

class GeradorMetadadosNotebook:
    """Extrai metadados completos do notebook e gera JSONs estruturados"""
    
    def __init__(self):
        self.metadata_completo = {
            "data_extracao": datetime.now().isoformat(),
            "versao": "3.0",
            "notebook": "real_vs_ideal.ipynb",
            "variaveis_encontradas": {},
            "dataframes_detalhados": {},
            "dicionarios_detalhados": {},
            "resumo_executivo": {},
            "timestamp_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.colunas_por_celula = {
            "metadata": {
                "data": datetime.now().isoformat(),
                "notebook": "real_vs_ideal.ipynb",
                "objetivo": "Mapa de todas as colunas geradas por cada célula"
            },
            "celulas": {}
        }
        
        self.erros = []
    
    def safe_to_json(self, obj):
        """Converte objetos não-serializáveis para tipos JSON"""
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        elif isinstance(obj, bool):
            return bool(obj)
        elif isinstance(obj, (list, dict)):
            return obj
        return str(obj)
    
    def extrair_dataframe(self, df_name, df, celula_num, celula_nome):
        """Extrai metadados de um DataFrame"""
        try:
            if df is None or not isinstance(df, pd.DataFrame):
                self.erros.append(f"{df_name} não é um DataFrame válido")
                return None
            
            resultado = {
                "celula": celula_num,
                "celula_nome": celula_nome,
                "tipo": "DataFrame",
                "shape": list(df.shape),
                "num_linhas": len(df),
                "num_colunas": len(df.columns),
                "colunas": list(df.columns),
                "tipos_colunas": {col: str(df[col].dtype) for col in df.columns},
                "memoria_mb": float(df.memory_usage(deep=True).sum() / 1024**2),
                "nulos_por_coluna": {col: int(df[col].isna().sum()) for col in df.columns}
            }
            
            # Snapshots de valores
            if len(df) > 0:
                resultado["valores_primeira_linha"] = {col: self.safe_to_json(df.iloc[0][col]) for col in df.columns}
                resultado["valores_ultima_linha"] = {col: self.safe_to_json(df.iloc[-1][col]) for col in df.columns}
            
            # Estatísticas básicas
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                resultado["stats"] = {
                    col: {
                        "min": self.safe_to_json(df[col].min()),
                        "max": self.safe_to_json(df[col].max()),
                        "mean": self.safe_to_json(df[col].mean()),
                        "std": self.safe_to_json(df[col].std())
                    } for col in numeric_cols
                }
            
            return resultado
        except Exception as e:
            self.erros.append(f"Erro ao extrair {df_name}: {str(e)}")
            return None
    
    def executar(self, globals_dict):
        """Executa a extração completa"""
        print("=" * 80)
        print("🔍 INICIANDO EXTRAÇÃO DE METADADOS NOTEBOOK...")
        print("=" * 80)
        
        # Mapeamento de variáveis esperadas
        variaveis_esperadas = {
            'df_real_m': (5, 'Execução Cenário Real'),
            'df_real_a': (5, 'Execução Cenário Real - Anual'),
            'df_ideal': (6, 'Cenário Ideal'),
            'df_ideal_anual': (6, 'Cenário Ideal - Anual'),
            'mc_results': (7, 'Monte Carlo Enterprise'),
            'df_audit': (9, 'Auditoria Forense')
        }
        
        # ===================================================================
        # 1. EXTRAIR DATAFRAMES
        # ===================================================================
        print("\n📊 Extraindo DataFrames...")
        for var_name, (celula_num, celula_nome) in variaveis_esperadas.items():
            if var_name in globals_dict:
                print(f"   ✅ {var_name} (Célula {celula_num})")
                df = globals_dict[var_name]
                
                resultado = self.extrair_dataframe(var_name, df, celula_num, celula_nome)
                if resultado:
                    self.metadata_completo["dataframes_detalhados"][var_name] = resultado
                    self.metadata_completo["variaveis_encontradas"][var_name] = True
                    
                    # Adicionar ao mapa de colunas
                    self.colunas_por_celula["celulas"][f"celula_{celula_num}_{var_name}"] = {
                        "celula_numero": celula_num,
                        "celula_nome": celula_nome,
                        "variavel_saida": var_name,
                        "num_colunas": len(df.columns),
                        "colunas": list(df.columns)
                    }
            else:
                self.metadata_completo["variaveis_encontradas"][var_name] = False
                print(f"   ❌ {var_name} (não encontrada)")
        
        # ===================================================================
        # 2. EXTRAIR DICIONÁRIOS
        # ===================================================================
        print("\n📚 Extraindo Dicionários...")
        dicts_esperados = {
            'met_real': (5, 'Execução Cenário Real'),
            'met_ideal': (6, 'Cenário Ideal'),
            'mc_data': (7, 'Monte Carlo'),
            'alertas_real': (5, 'Execução Cenário Real'),
            'alertas_ideal': (6, 'Cenário Ideal')
        }
        
        for dict_name, (celula_num, celula_nome) in dicts_esperados.items():
            if dict_name in globals_dict:
                print(f"   ✅ {dict_name} (Célula {celula_num})")
                obj = globals_dict[dict_name]
                
                if isinstance(obj, dict):
                    self.metadata_completo["dicionarios_detalhados"][dict_name] = {
                        "tipo": "dict",
                        "celula": celula_num,
                        "num_chaves": len(obj.keys()),
                        "chaves": list(obj.keys())[:20],  # Primeiras 20 chaves
                        "exemplo_valores": {k: self.safe_to_json(obj[k]) for k in list(obj.keys())[:3]}
                    }
                    self.metadata_completo["variaveis_encontradas"][dict_name] = True
                elif isinstance(obj, list):
                    self.metadata_completo["dicionarios_detalhados"][dict_name] = {
                        "tipo": "list",
                        "celula": celula_num,
                        "num_items": len(obj),
                        "exemplo_items": obj[:5] if len(obj) > 0 else []
                    }
                    self.metadata_completo["variaveis_encontradas"][dict_name] = True
            else:
                self.metadata_completo["variaveis_encontradas"][dict_name] = False
        
        # ===================================================================
        # 3. EXTRAIR PREMISSAS
        # ===================================================================
        print("\n⚙️ Extraindo PREMISSAS...")
        if 'PREMISSAS' in globals_dict:
            print("   ✅ PREMISSAS (Célula 2)")
            p = globals_dict['PREMISSAS']
            
            chaves_importantes = [
                'meses_projecao', 'usuarios_pagos_iniciais', 'caixa_inicial',
                'preco_lite', 'preco_trader', 'preco_pro',
                'mix_lite', 'mix_trader', 'mix_pro',
                'churn_base', 'churn_maturidade',
                'marketing_fixo_mensal', 'trafego_inicial',
                'threshold_caixa_quebra', 'caixa_reserva_operacional'
            ]
            
            self.metadata_completo["dicionarios_detalhados"]["PREMISSAS"] = {
                "tipo": "dict",
                "celula": 2,
                "num_chaves_total": len(p.keys()),
                "chaves_importantes": {}
            }
            
            for chave in chaves_importantes:
                if chave in p:
                    self.metadata_completo["dicionarios_detalhados"]["PREMISSAS"]["chaves_importantes"][chave] = self.safe_to_json(p[chave])
            
            self.metadata_completo["variaveis_encontradas"]["PREMISSAS"] = True
        else:
            self.metadata_completo["variaveis_encontradas"]["PREMISSAS"] = False
        
        # ===================================================================
        # 4. GERAR RESUMO EXECUTIVO
        # ===================================================================
        print("\n📈 Gerando Resumo Executivo...")
        if 'df_real_m' in globals_dict and isinstance(globals_dict['df_real_m'], pd.DataFrame):
            df = globals_dict['df_real_m']
            if len(df) > 0:
                m1 = df.iloc[0]
                m36 = df.iloc[-1]
                
                self.metadata_completo["resumo_executivo"] = {
                    "cenario": "Real (Bootstrap)",
                    "periodo_meses": len(df),
                    "metricas_m1": {},
                    "metricas_m36": {}
                }
                
                metricas_chave = ['mrr', 'usuarios_ativos', 'caixa', 'churn_rate', 'ltv_cac', 'runway_meses', 'burn_rate']
                
                for metrica in metricas_chave:
                    if metrica in df.columns:
                        self.metadata_completo["resumo_executivo"]["metricas_m1"][metrica] = self.safe_to_json(m1[metrica])
                        self.metadata_completo["resumo_executivo"]["metricas_m36"][metrica] = self.safe_to_json(m36[metrica])
                
                print("   ✅ Resumo gerado com sucesso")
        
        # ===================================================================
        # 5. SALVAR ARQUIVOS JSON
        # ===================================================================
        print("\n💾 Salvando arquivos JSON...")
        
        # JSON 1: Metadados completos
        with open('METADADOS_NOTEBOOK_COMPLETO.json', 'w', encoding='utf-8') as f:
            json.dump(self.metadata_completo, f, indent=2, ensure_ascii=False, default=str)
        print("   ✅ METADADOS_NOTEBOOK_COMPLETO.json")
        
        # JSON 2: Apenas colunas por célula
        with open('COLUNAS_DETALHADAS.json', 'w', encoding='utf-8') as f:
            json.dump(self.colunas_por_celula, f, indent=2, ensure_ascii=False, default=str)
        print("   ✅ COLUNAS_DETALHADAS.json")
        
        # ===================================================================
        # 6. EXIBIR RESUMO
        # ===================================================================
        print("\n" + "=" * 80)
        print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        
        print("\n📊 Resumo de Variáveis Encontradas:")
        for var, encontrada in self.metadata_completo["variaveis_encontradas"].items():
            status = "✅" if encontrada else "❌"
            print(f"   {status} {var}")
        
        if "metricas_m36" in self.metadata_completo.get("resumo_executivo", {}):
            print("\n📈 Métricas Finais (M36):")
            m = self.metadata_completo["resumo_executivo"]["metricas_m36"]
            for metrica, valor in m.items():
                print(f"   {metrica:20} = {valor}")
        
        if self.erros:
            print("\n⚠️  Erros Detectados:")
            for erro in self.erros:
                print(f"   • {erro}")
        
        print("\n" + "=" * 80)
        print("📁 Arquivos gerados (no diretório do notebook):")
        print("   1. METADADOS_NOTEBOOK_COMPLETO.json")
        print("   2. COLUNAS_DETALHADAS.json")
        print("=" * 80)

# EXECUTAR
if __name__ == "__main__":
    print("Cole este código como uma célula Python no fim do seu notebook")
    print("DEPOIS de executar as células 5, 6 e 7.")
else:
    # Quando executado como célula do notebook
    gerador = GeradorMetadadosNotebook()
    gerador.executar(globals())
