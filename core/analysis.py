"""
core/analysis.py

Análises numéricas: Monte Carlo simples e Análise de Sensibilidade.
Projetado para ser leve e não depender de tqdm ou libs extras.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

def rodar_montecarlo(premissas: Dict[str, Any], n: int = 500, meses: int = 36, seed: int = 42) -> Dict[str, np.ndarray]:
    """
    Executa simulações Monte Carlo simplificadas.
    Retorna dicionário com arrays: 'final_cash', 'mrr_end', 'users_end' (cada length n)
    premissas: dicionário contendo chaves básicas (trafego_inicial, crescimento_trafego_mensal, taxa_conv_trial, trial_para_pago, churn_mensal, arpu, infra, marketing_min)
    """
    rng = np.random.default_rng(seed)
    final_cash = np.zeros(n)
    mrr_end = np.zeros(n)
    users_end = np.zeros(n)

    # extrai premissas com fallback
    traf_init = float(premissas.get("trafego_inicial", premissas.get("visitantes_mes_1", 1000)))
    growth = float(premissas.get("crescimento_trafego_mensal", premissas.get("taxa_crescimento_trafego_mensal", 0.2)))
    conv_trial = float(premissas.get("taxa_conv_trial", premissas.get("taxa_conversao_visitante_trial", 0.05)))
    conv_paid = float(premissas.get("trial_para_pago", premissas.get("taxa_conversao_trial_pagante", 0.15)))
    churn = float(premissas.get("churn_mensal", premissas.get("churn_mensal", 0.04)))
    arpu = float(premissas.get("arpu", premissas.get("arpu_medio", 97.0)))
    infra = float(premissas.get("infra", premissas.get("infra_tier1_custo_fixo", 209.0)))
    marketing_min = float(premissas.get("marketing_min", premissas.get("marketing_fase1_custo_fixo", 1000.0)))
    caixa_inicial = float(premissas.get("caixa_inicial", premissas.get("capital_inicial_caixa", 50000.0)))

    for i in range(n):
        # amostra variações percentuais realistas (normal truncada)
        g = growth * rng.normal(1.0, 0.15)
        c = max(0.001, churn * rng.normal(1.0, 0.2))
        # simula crescimento de usuários via tráfego acumulado (simplificado)
        traf = traf_init
        users = 0.0
        caixa = caixa_inicial

        for m in range(1, meses+1):
            traf = traf * (1 + g)
            novos_trials = traf * conv_trial
            novos_pagantes = novos_trials * conv_paid
            # cartas de churn aplicadas
            users = max(0.0, users + novos_pagantes - users * c)
            mrr = users * arpu
            # custos simplificados
            custo_ia = users * premissas.get("custo_ia", premissas.get("custo_ia_por_usuario", 5.0))
            impostos = mrr * premissas.get("aliquota_impostos", premissas.get("aliquota_impostos", 0.06))
            marketing = marketing_min if m <= 3 else max(0, mrr * premissas.get("marketing_pct", 0.15))
            opex = infra + marketing + custo_ia
            resultado = mrr - impostos - opex
            caixa = caixa + resultado + premissas.get("aporte_mensal_fixo", 0.0)
        final_cash[i] = caixa
        mrr_end[i] = mrr
        users_end[i] = users

    return {"final_cash": final_cash, "mrr_end": mrr_end, "users_end": users_end}

def sensibilidade_univariada(base_premissas: Dict[str, Any], parametro: str, valores: np.ndarray, meses: int = 36) -> pd.DataFrame:
    """
    Roda sensibilidade univariada para 'parametro' variando pelos 'valores'.
    Retorna DataFrame com colunas: parametro, caixa_final, mrr_final, usuarios_final
    """
    results = []
    for v in valores:
        prem = base_premissas.copy()
        prem[parametro] = v
        out = rodar_montecarlo(prem, n=50, meses=meses)  # 50 runs por ponto
        results.append({
            parametro: v,
            "media_caixa_final": float(out["final_cash"].mean()),
            "p50_caixa_final": float(np.percentile(out["final_cash"], 50)),
            "media_mrr_end": float(out["mrr_end"].mean()),
            "media_users_end": float(out["users_end"].mean())
        })
    return pd.DataFrame(results)
