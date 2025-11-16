# DENTRO DE: core/analytics/cohorts.py
import pandas as pd
import numpy as np

def gerar_cohort_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Gera matriz de cohorts (otimizada)"""
    try:
        meses = df['mes'].unique()[:12]
        cohort_data = []
        
        for i, mes_cohort in enumerate(meses):
            linha = {'Cohort': f"Mês {mes_cohort}"}
            usuarios_cohort = df[df['mes'] == mes_cohort]['Novos_Pagantes'].iloc[0]
            
            if usuarios_cohort <= 0:
                continue
            
            for idade in range(0, min(12, len(meses) - i)):
                mes_futuro = mes_cohort + idade
                if mes_futuro in df['mes'].values:
                    try:
                        # Busca o cohort específico (aproximação)
                        df_cohort = df[df['mes'] == mes_futuro]
                        if not df_cohort.empty:
                            # Aproximação: assume que os usuários remanescentes incluem o cohort
                            total_remanescente = df_cohort['Usuarios_Finais'].iloc[0]
                            cohort_original = sum(df[(df['mes'] == mes_cohort)]['Novos_Pagantes'])
                            
                            if cohort_original > 0:
                                retencao = min(100, (total_remanescente / cohort_original) * 100)
                                linha[f"M{idade}"] = retencao
                            else:
                                linha[f"M{idade}"] = None
                        else:
                            linha[f"M{idade}"] = None
                    except:
                        linha[f"M{idade}"] = None
                else:
                    linha[f"M{idade}"] = None
            
            cohort_data.append(linha)
        
        df_cohorts = pd.DataFrame(cohort_data) if cohort_data else pd.DataFrame()
        return df_cohorts.fillna(0)
    except Exception as e:
        print(f"Erro ao gerar cohorts: {e}") # Usar print para debugging, não st.error
        return pd.DataFrame()
