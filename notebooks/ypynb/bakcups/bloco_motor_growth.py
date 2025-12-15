# --------------------------
# 3.1 GROWTH PARAMETRIZADO (V13.2 - ZERO HARDCODE)
# --------------------------

# 1. CÁLCULO DO BUDGET (mantém lógica original)
mkt_fixo = p_run.get('marketing_fixo_mensal', 0.0)
mkt_perc = p_run.get('marketing_perc_receita', 0.0)
mkt_hab = p_run.get('marketing_habilitado', True)

if not mkt_hab or (mkt_fixo <= 0 and mkt_perc <= 0):
    budget_mkt_desejado = 0.0
elif mes == 0:
    budget_mkt_desejado = max(1.0, mkt_fixo)
else:
    budget_calc = dados['receita_bruta'][mes - 1] * mkt_perc
    budget_mkt_desejado = np.clip(budget_calc, mkt_fixo, p_run['marketing_teto'])

# Regras de corte por caixa (mantém lógica original)
if mes > 0 and caixa_atual < 0:
    budget_mkt = 0.0
    alertas.append({
        'tipo': 'marketing_corte_total_caixa_negativa',
        'mes': mes_atual_num,
        'caixa': caixa_atual,
        'mensagem': f'⚠️ Mês {mes_atual_num}: Marketing CORTADO (100%). Caixa negativo: R$ {caixa_atual:.2f}'
    })
elif mes > 0 and caixa_atual < (CAIXA_RESERVA * 0.20):
    budget_mkt = budget_mkt_desejado * 0.50
    alertas.append({
        'tipo': 'marketing_emergencia_caixa_critico',
        'mes': mes_atual_num,
        'caixa': caixa_atual,
        'corte_pct': 50.0,
        'mensagem': f'🔴 Mês {mes_atual_num}: Marketing em EMERGÊNCIA (corte 50%). Caixa: R$ {caixa_atual:.2f}'
    })
elif mes > 0 and caixa_atual < (CAIXA_RESERVA * 0.50):
    budget_mkt = budget_mkt_desejado * 0.75
    alertas.append({
        'tipo': 'marketing_cautela',
        'mes': mes_atual_num,
        'caixa': caixa_atual,
        'corte_pct': 25.0,
        'mensagem': f'🟡 Mês {mes_atual_num}: Marketing em CAUTELA (corte 25%). Caixa: R$ {caixa_atual:.2f}'
    })
else:
    budget_mkt = budget_mkt_desejado

dados['gasto_marketing'][mes] = budget_mkt

# 2. NOVO: DETERMINA TAXA DE CRESCIMENTO ORGÂNICO BASEADO NO BUDGET
# ------------------------------------------------------------------
# Busca o tier correspondente ao budget atual nas premissas
taxa_crescimento_organico = 0.0  # Default: sem crescimento

growth_tiers = p_run.get('growth_tiers', [])
for tier in growth_tiers:
    if tier['budget_min'] <= budget_mkt < tier['budget_max']:
        taxa_crescimento_organico = tier['taxa']
        if modo_debug and mes < 3:
            print(f"Mês {mes_atual_num}: Budget R$ {budget_mkt:.2f} → Tier '{tier['nome']}' → Growth {tier['taxa']*100:.1f}%/mês")
        break

# 3. APLICA CRESCIMENTO ORGÂNICO NO TRÁFEGO BASE
if mes > 0:
    # Crescimento orgânico acontece APENAS se houver investimento
    trafego_base = trafego_base * (1 + taxa_crescimento_organico)

# 4. CALCULA CPC BLENDED E VISITAS PAGAS (lógica original)
cpc_blended = (
    p_run['cpc_instagram'] * p_run['canal_instagram_pct'] +
    p_run['cpc_facebook'] * p_run['canal_facebook_pct'] +
    p_run['cpc_google'] * p_run['canal_google_pct'] +
    p_run['cpc_youtube'] * p_run['canal_youtube_pct']
)
dados['cpc_blended'][mes] = cpc_blended

# Visitas pagas (com limitadores de mercado - mantém lógica original)
visitas_pagas_teoricas = (budget_mkt / max(cpc_blended, 0.01))

limite_inventario = LIMITE_INVENTARIO
mercado_disponivel = max(0, MERCADO_POTENCIAL - usuarios_ativos)
taxa_conversao_pipeline = (p_run['taxa_visitante_para_trial'] * 
                           p_run['taxa_trial_para_pagante'] * 
                           eficiencia)

mercado_alcancavel_mensal = MERCADO_POTENCIAL * 0.10
penetracao_mercado = usuarios_ativos / max(1.0, mercado_alcancavel_mensal)
fator_saturacao = max(0.1, 1.0 - penetracao_mercado)
limite_mercado_realistico = mercado_alcancavel_mensal * fator_saturacao

if taxa_conversao_pipeline > 0:
    limite_mercado = min(limite_mercado_realistico, mercado_disponivel / taxa_conversao_pipeline)
else:
    limite_mercado = limite_mercado_realistico

visitas_pagas = min(visitas_pagas_teoricas, limite_inventario, limite_mercado)

if visitas_pagas < visitas_pagas_teoricas:
    dados['saturacao_mercado'][mes] = visitas_pagas_teoricas - visitas_pagas

# 5. CALCULA VISITAS ORGÂNICAS (BASE + VIRAIS)
trafego_base_ajustado = trafego_base * fator_sazon

# Visitas Virais (mantém lógica original)
elasticidade = p_run.get('elasticidade_organico', 1.0)
fator_viral_base = p_run.get('fator_visitas_organicas_por_pagante', 0.0)
penetracao = usuarios_ativos / MERCADO_POTENCIAL
fator_saturacao_viral = 1.0 / (1.0 + np.exp(10 * (penetracao - 0.5)))
visitas_virais = (usuarios_ativos * fator_viral_base * elasticidade * fator_saturacao_viral)

visitas_organicas = trafego_base_ajustado + visitas_virais

# 6. REGISTRA VETORES
dados['trafego_pago'][mes] = visitas_pagas
dados['trafego_organico'][mes] = visitas_organicas
dados['trafego_total'][mes] = visitas_pagas + visitas_organicas

# Vetores de detalhamento de MKT
dados['gasto_instagram'][mes] = budget_mkt * p_run['canal_instagram_pct']
dados['gasto_facebook'][mes] = budget_mkt * p_run['canal_facebook_pct']
dados['gasto_youtube'][mes] = budget_mkt * p_run['canal_youtube_pct']
dados['gasto_google'][mes] = budget_mkt * p_run['canal_google_pct']



## 🎯 **COMO FUNCIONA (EXEMPLO)**

### **Cenário 1: Budget R$ 0**

#growth_tiers[0]: budget_min=0, budget_max=500, taxa=0.0%
#→ Taxa de crescimento orgânico = 0%
#→ Tráfego base não cresce (fica fixo em 400)
#→ Crescimento vem APENAS de viralidade (3,5 visitas/usuário)


### **Cenário 2: Budget R$ 2.500**

#growth_tiers[2]: budget_min=1500, budget_max=3000, taxa=1.0%
#→ Taxa de crescimento orgânico = 1%/mês
#→ Tráfego base cresce 1% ao mês (400 → 404 → 408...)
#→ Crescimento vem de: orgânico (1%) + virais + ads pagas


### **Cenário 3: Budget R$ 10.000**

#growth_tiers[4]: budget_min=6000, budget_max=15000, taxa=2.5%
#→ Taxa de crescimento orgânico = 2,5%/mês
#→ Tráfego base cresce 2,5% ao mês (400 → 410 → 420...)
#→ Crescimento vem de: orgânico (2,5%) + virais + ads pagas