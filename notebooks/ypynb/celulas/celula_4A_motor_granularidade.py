# CELULA 4A - MOTOR DE GRANULARIDADE TEMPORAL V1.0
# ============================================================================
# OBJETIVO: Expandir dados mensais para granularidades semanal e diária
# AUTOR: [Gemini/Claude]
# DATA: 2025-12-06
# STATUS: PRODUCTION READY
# ============================================================================
# DOCUMENTAÇÃO:
# Este módulo recebe o DataFrame mensal (df_real_m) gerado pelo motor principal
# e expande para granularidades menores usando:
# 1. Interpolação linear/spline para tendência
# 2. Ruído estocástico calibrado para volatilidade realista
# 3. Preservação de totais (soma semanal/diária = valor mensal)
# ============================================================================

import pandas as pd
import numpy as np
from scipy import interpolate
from typing import Tuple, Optional


def gerar_granularidade_semanal(
    df_mensal: pd.DataFrame,
    premissas: dict,
    meses_expandir: int = 6,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Expande dados mensais para visão semanal (semanas 1-26 para M1-M6).
    
    Lógica:
    - Para FLUXOS (receita, custos, novos clientes): distribui ao longo das semanas
    - Para ESTOQUES (usuários, caixa, MRR): interpola linearmente
    - Para TAXAS (churn, CAC): replica o valor mensal com pequena variação
    
    Parâmetros:
    -----------
    df_mensal : pd.DataFrame
        DataFrame mensal gerado pelo motor principal
    premissas : dict
        Dicionário de premissas (para capturar volatilidades)
    meses_expandir : int
        Quantos meses expandir para visão semanal (padrão: 6)
    seed : int, opcional
        Seed para reprodutibilidade do ruído
        
    Retorno:
    --------
    pd.DataFrame
        DataFrame com granularidade semanal
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Configurações
    semanas_por_mes = premissas.get('semanas_por_mes', 4.33)
    total_semanas = int(meses_expandir * semanas_por_mes)
    
    # Volatilidade semanal (quanto os valores oscilam semana-a-semana)
    # Calibrado para ser realista: 10-20% de variação
    volatilidade_cac = premissas.get('volatilidade_semanal_cac', 0.15)  # 15%
    volatilidade_conversao = premissas.get('volatilidade_semanal_conversao', 0.10)  # 10%
    volatilidade_churn = premissas.get('volatilidade_semanal_churn', 0.08)  # 8%
    
    # Extrai dados dos primeiros N meses
    df_slice = df_mensal.iloc[:meses_expandir].copy()
    
    # Inicializa DataFrame semanal
    dados_semanais = {
        'semana': list(range(1, total_semanas + 1)),
        'mes_referencia': [],  # Qual mês cada semana pertence
    }
    
    # Colunas a processar
    # FLUXOS: Distribuir proporcionalmente nas semanas do mês
    colunas_fluxo = [
        'receita_bruta', 'receita_liquida', 'novos_pagantes_total', 'novos_ads', 
        'novos_organicos', 'churn_usuarios', 'churn_mrr', 'gasto_marketing',
        'trafego_total', 'trafego_pago', 'trafego_organico', 'trials_total',
        'impostos', 'taxas_pagamento', 'total_cogs', 'total_opex'
    ]
    
    # ESTOQUES: Interpolar entre valores mensais
    colunas_estoque = [
        'usuarios_ativos', 'usuarios_lite', 'usuarios_trader', 'usuarios_pro',
        'mrr', 'arr', 'caixa', 'margem_bruta'
    ]
    
    # TAXAS: Replicar com pequena variação estocástica
    colunas_taxa = [
        'cac_blended', 'cac_paid', 'ltv', 'ltv_cac', 'payback_meses',
        'churn_rate', 'retention_rate', 'arpu', 'margem_bruta_pct'
    ]
    
    # Inicializa todas as colunas
    for col in colunas_fluxo + colunas_estoque + colunas_taxa:
        if col in df_slice.columns:
            dados_semanais[col] = np.zeros(total_semanas)
    
    # --- PROCESSA CADA TIPO DE COLUNA ---
    
    # Calcula mês de referência para cada semana
    semana_atual = 0
    for mes_idx in range(meses_expandir):
        mes_num = mes_idx + 1
        semanas_no_mes = int(np.ceil(semanas_por_mes)) if mes_idx < meses_expandir - 1 else total_semanas - semana_atual
        
        # Ajusta para não ultrapassar total de semanas
        semanas_no_mes = min(semanas_no_mes, total_semanas - semana_atual)
        
        for s in range(semanas_no_mes):
            if semana_atual < total_semanas:
                dados_semanais['mes_referencia'].append(mes_num)
                semana_atual += 1
    
    # Completa se faltou
    while len(dados_semanais['mes_referencia']) < total_semanas:
        dados_semanais['mes_referencia'].append(meses_expandir)
    
    dados_semanais['mes_referencia'] = np.array(dados_semanais['mes_referencia'])
    
    # 1. FLUXOS: Distribui valor mensal nas semanas com variação
    for col in colunas_fluxo:
        if col not in df_slice.columns:
            continue
            
        for mes_idx in range(meses_expandir):
            valor_mensal = df_slice.iloc[mes_idx][col]
            semanas_do_mes = np.where(dados_semanais['mes_referencia'] == mes_idx + 1)[0]
            n_semanas = len(semanas_do_mes)
            
            if n_semanas > 0 and valor_mensal != 0:
                # Gera pesos aleatórios que somam 1 (distribuição não-uniforme)
                pesos = np.random.dirichlet(np.ones(n_semanas) * 3)  # Alpha=3 para suavizar
                
                # Distribui o valor mensal proporcionalmente
                for i, sem_idx in enumerate(semanas_do_mes):
                    dados_semanais[col][sem_idx] = valor_mensal * pesos[i]
    
    # 2. ESTOQUES: Interpolação linear entre pontos mensais
    for col in colunas_estoque:
        if col not in df_slice.columns:
            continue
        
        # Pontos mensais (semana do final de cada mês)
        valores_mensais = df_slice[col].values
        semanas_fim_mes = np.cumsum([int(np.ceil(semanas_por_mes)) if i < meses_expandir - 1 
                                      else total_semanas - sum([int(np.ceil(semanas_por_mes)) for j in range(i)])
                                      for i in range(meses_expandir)])
        semanas_fim_mes = np.clip(semanas_fim_mes, 1, total_semanas) - 1  # Índice 0-based
        
        # Cria spline para interpolação suave
        if len(valores_mensais) >= 2:
            # Adiciona ponto inicial (semana 0 = valor M0 ou projeção)
            x_pontos = np.concatenate([[0], semanas_fim_mes])
            y_pontos = np.concatenate([[valores_mensais[0] * 0.9], valores_mensais])  # Começa 10% abaixo
            
            # Interpolação cúbica
            try:
                f = interpolate.interp1d(x_pontos, y_pontos, kind='linear', fill_value='extrapolate')
                dados_semanais[col] = f(np.arange(total_semanas))
            except Exception:
                # Fallback: replica valores mensais
                for sem_idx in range(total_semanas):
                    mes_ref = int(dados_semanais['mes_referencia'][sem_idx]) - 1
                    dados_semanais[col][sem_idx] = valores_mensais[min(mes_ref, len(valores_mensais) - 1)]
        else:
            dados_semanais[col] = np.full(total_semanas, valores_mensais[0])
    
    # 3. TAXAS: Replica valor mensal + ruído estocástico
    for col in colunas_taxa:
        if col not in df_slice.columns:
            continue
        
        # Determina volatilidade baseada no tipo de métrica
        if 'cac' in col.lower():
            vol = volatilidade_cac
        elif 'churn' in col.lower():
            vol = volatilidade_churn
        else:
            vol = volatilidade_conversao
        
        for sem_idx in range(total_semanas):
            mes_ref = int(dados_semanais['mes_referencia'][sem_idx]) - 1
            valor_base = df_slice.iloc[mes_ref][col] if mes_ref < len(df_slice) else df_slice.iloc[-1][col]
            
            # Adiciona ruído (distribuição normal truncada)
            if not np.isnan(valor_base) and valor_base != 0:
                ruido = np.random.normal(0, vol)
                ruido = np.clip(ruido, -0.3, 0.3)  # Limita o ruído a ±30%
                dados_semanais[col][sem_idx] = valor_base * (1 + ruido)
            else:
                dados_semanais[col][sem_idx] = valor_base
    
    # Cria DataFrame
    df_semanal = pd.DataFrame(dados_semanais)
    
    # Adiciona colunas de contexto
    df_semanal['periodo'] = df_semanal['semana'].apply(lambda x: f'S{x:02d}')
    
    # Calcula colunas derivadas se existirem os componentes
    if 'ltv' in df_semanal.columns and 'cac_blended' in df_semanal.columns:
        df_semanal['ltv_cac_calc'] = df_semanal['ltv'] / df_semanal['cac_blended'].replace(0, np.nan)
    
    if 'cac_blended' in df_semanal.columns:
        # Payback em semanas (CAC / margem semanal)
        if 'margem_bruta' in df_semanal.columns and 'usuarios_ativos' in df_semanal.columns:
            margem_semanal_por_user = df_semanal['margem_bruta'] / df_semanal['usuarios_ativos'].replace(0, np.nan)
            df_semanal['payback_semanas'] = df_semanal['cac_blended'] / (margem_semanal_por_user * 4.33)
    
    return df_semanal


def gerar_granularidade_diaria(
    df_mensal: pd.DataFrame,
    premissas: dict,
    meses_expandir: int = 6,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Expande dados mensais para visão diária (dias 1-180 para M1-M6).
    
    Mesma lógica do semanal, mas com granularidade de 1 dia.
    
    Parâmetros:
    -----------
    df_mensal : pd.DataFrame
        DataFrame mensal gerado pelo motor principal
    premissas : dict
        Dicionário de premissas
    meses_expandir : int
        Quantos meses expandir (padrão: 6)
    seed : int, opcional
        Seed para reprodutibilidade
        
    Retorno:
    --------
    pd.DataFrame
        DataFrame com granularidade diária
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Configurações
    dias_por_mes = 30  # Simplificação
    total_dias = meses_expandir * dias_por_mes
    
    # Volatilidade diária (maior que semanal - mais ruído)
    volatilidade_cac = premissas.get('volatilidade_diaria_cac', 0.25)
    volatilidade_conversao = premissas.get('volatilidade_diaria_conversao', 0.20)
    volatilidade_churn = premissas.get('volatilidade_diaria_churn', 0.15)
    
    # Extrai dados dos primeiros N meses
    df_slice = df_mensal.iloc[:meses_expandir].copy()
    
    # Inicializa DataFrame diário
    dados_diarios = {
        'dia': list(range(1, total_dias + 1)),
        'semana': [],
        'mes_referencia': [],
    }
    
    # Calcula semana e mês de referência para cada dia
    for dia in range(1, total_dias + 1):
        semana = (dia - 1) // 7 + 1
        mes = (dia - 1) // dias_por_mes + 1
        dados_diarios['semana'].append(semana)
        dados_diarios['mes_referencia'].append(mes)
    
    dados_diarios['semana'] = np.array(dados_diarios['semana'])
    dados_diarios['mes_referencia'] = np.array(dados_diarios['mes_referencia'])
    
    # Colunas a processar (mesmas do semanal)
    colunas_fluxo = [
        'receita_bruta', 'novos_pagantes_total', 'churn_usuarios', 
        'gasto_marketing', 'trafego_total', 'trafego_pago', 'trafego_organico'
    ]
    
    colunas_estoque = [
        'usuarios_ativos', 'mrr', 'caixa'
    ]
    
    colunas_taxa = [
        'cac_blended', 'ltv', 'ltv_cac', 'churn_rate', 'arpu'
    ]
    
    # Inicializa colunas
    for col in colunas_fluxo + colunas_estoque + colunas_taxa:
        if col in df_slice.columns:
            dados_diarios[col] = np.zeros(total_dias)
    
    # 1. FLUXOS: Distribui valor mensal nos dias
    for col in colunas_fluxo:
        if col not in df_slice.columns:
            continue
            
        for mes_idx in range(meses_expandir):
            valor_mensal = df_slice.iloc[mes_idx][col]
            dias_do_mes = np.where(dados_diarios['mes_referencia'] == mes_idx + 1)[0]
            n_dias = len(dias_do_mes)
            
            if n_dias > 0 and valor_mensal != 0:
                # Gera pesos com distribuição dirichlet (mais variação que semanal)
                pesos = np.random.dirichlet(np.ones(n_dias) * 2)  # Alpha=2 para mais variação
                
                for i, dia_idx in enumerate(dias_do_mes):
                    dados_diarios[col][dia_idx] = valor_mensal * pesos[i]
    
    # 2. ESTOQUES: Interpolação linear
    for col in colunas_estoque:
        if col not in df_slice.columns:
            continue
        
        valores_mensais = df_slice[col].values
        dias_fim_mes = np.array([dias_por_mes * (i + 1) for i in range(meses_expandir)])
        dias_fim_mes = np.clip(dias_fim_mes, 1, total_dias) - 1
        
        if len(valores_mensais) >= 2:
            x_pontos = np.concatenate([[0], dias_fim_mes])
            y_pontos = np.concatenate([[valores_mensais[0] * 0.95], valores_mensais])
            
            try:
                f = interpolate.interp1d(x_pontos, y_pontos, kind='linear', fill_value='extrapolate')
                dados_diarios[col] = f(np.arange(total_dias))
            except Exception:
                for dia_idx in range(total_dias):
                    mes_ref = int(dados_diarios['mes_referencia'][dia_idx]) - 1
                    dados_diarios[col][dia_idx] = valores_mensais[min(mes_ref, len(valores_mensais) - 1)]
        else:
            dados_diarios[col] = np.full(total_dias, valores_mensais[0])
    
    # 3. TAXAS: Replica + ruído maior (diário é mais volátil)
    for col in colunas_taxa:
        if col not in df_slice.columns:
            continue
        
        if 'cac' in col.lower():
            vol = volatilidade_cac
        elif 'churn' in col.lower():
            vol = volatilidade_churn
        else:
            vol = volatilidade_conversao
        
        for dia_idx in range(total_dias):
            mes_ref = int(dados_diarios['mes_referencia'][dia_idx]) - 1
            valor_base = df_slice.iloc[mes_ref][col] if mes_ref < len(df_slice) else df_slice.iloc[-1][col]
            
            if not np.isnan(valor_base) and valor_base != 0:
                ruido = np.random.normal(0, vol)
                ruido = np.clip(ruido, -0.5, 0.5)  # Permite mais variação diária
                dados_diarios[col][dia_idx] = valor_base * (1 + ruido)
            else:
                dados_diarios[col][dia_idx] = valor_base
    
    # Cria DataFrame
    df_diario = pd.DataFrame(dados_diarios)
    
    # Adiciona colunas de contexto
    df_diario['periodo'] = df_diario['dia'].apply(lambda x: f'D{x:03d}')
    
    return df_diario


def expandir_granularidade_completa(
    df_mensal: pd.DataFrame,
    premissas: dict,
    meses_expandir: int = 6,
    seed: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Função principal: gera tanto semanal quanto diário.
    
    Parâmetros:
    -----------
    df_mensal : pd.DataFrame
        DataFrame mensal do motor principal
    premissas : dict
        Dicionário de premissas
    meses_expandir : int
        Quantos meses expandir (padrão: 6 = primeiros 6 meses)
    seed : int, opcional
        Seed para reprodutibilidade
        
    Retorno:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        (df_semanal, df_diario)
    """
    # Usa mesma seed base para ambos, mas com offset
    seed_base = seed if seed is not None else premissas.get('seed_fixa', 42)
    
    df_semanal = gerar_granularidade_semanal(
        df_mensal, premissas, meses_expandir, seed=seed_base
    )
    
    df_diario = gerar_granularidade_diaria(
        df_mensal, premissas, meses_expandir, seed=seed_base + 1000
    )
    
    return df_semanal, df_diario


# ============================================================================
# PRINT DE CONFIRMAÇÃO
# ============================================================================
if __name__ == "__main__":
    print("="*80)
    print("✅ MOTOR DE GRANULARIDADE TEMPORAL V1.0 CARREGADO")
    print("="*80)
    print("📋 FUNÇÕES DISPONÍVEIS:")
    print("   1. gerar_granularidade_semanal(df_mensal, premissas, meses=6) -> df_semanal")
    print("   2. gerar_granularidade_diaria(df_mensal, premissas, meses=6) -> df_diario")
    print("   3. expandir_granularidade_completa(df_mensal, premissas) -> (df_s, df_d)")
    print()
    print("📊 GRANULARIDADES GERADAS:")
    print("   • Semanal: Semanas 1-26 (6 meses)")
    print("   • Diário:  Dias 1-180 (6 meses)")
    print()
    print("🎯 PRONTO PARA EXPANSÃO DE DADOS MENSAIS")
    print("="*80)
