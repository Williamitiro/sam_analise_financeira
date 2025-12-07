# CÉLULA DE AUDITORIA FORENSE & DIAGNÓSTICO DE PREMISSAS
# ============================================================================
# ESTA CÉLULA NÃO ALTERA NADA. ELA APENAS LÊ A VERDADE QUE ESTÁ NA MEMÓRIA.
# ============================================================================

import pandas as pd
import numpy as np

def auditoria_forense_premissas():
    print("="*80)
    print("🕵️‍♂️ RAIO-X DAS PREMISSAS (O QUE ESTÁ NA MEMÓRIA AGORA)")
    print("="*80)
    
    # 1. VERIFICAÇÃO DE CAIXA E CAPEX
    print("💰 DINHEIRO & INÍCIO:")
    print(f"   • Caixa Inicial Configurado:   R$ {PREMISSAS.get('caixa_inicial', 'N/A'):,.2f}")
    print(f"   • Aporte Mensal:               R$ {PREMISSAS.get('aporte_mensal', 'N/A'):,.2f}")
    print(f"   • CAPEX Inicial (Mês 0):       R$ {PREMISSAS.get('capex_inicial', 'N/A'):,.2f} <--- VERIFIQUE ISSO")
    print(f"   • Reserva de Segurança:        R$ {PREMISSAS.get('caixa_reserva_operacional', 'N/A'):,.2f}")
    
    # 2. VERIFICAÇÃO DE MARKETING
    print("\n📣 MARKETING & GROWTH:")
    print(f"   • Budget Fixo Mensal:          R$ {PREMISSAS.get('marketing_fixo_mensal', 'N/A'):,.2f}")
    print(f"   • Custo CPC Estimado:          R$ {PREMISSAS.get('cpc_instagram', 0)*PREMISSAS.get('canal_instagram_pct',0) + PREMISSAS.get('cpc_google', 0)*PREMISSAS.get('canal_google_pct',0):,.2f} (Aprox)")
    
    # 3. CUSTOS FIXOS
    print("\n🏢 CUSTOS FIXOS (BURN RATE BASAL):")
    infra = sum([v for k, v in PREMISSAS.items() if k.startswith('t1_') and isinstance(v, (int, float))])
    print(f"   • Infra Tier 1 (Mês 1):        R$ {infra:,.2f}")
    print(f"   • Salário Fundador:            R$ {PREMISSAS.get('salario_fundador', 0):,.2f} (Gatilho: R$ {PREMISSAS.get('trigger_fundador', 0):,.2f})")
    
    # 4. EXECUÇÃO DE PROVA (SIMULAÇÃO UNITÁRIA)
    print("\n" + "="*80)
    print("⚙️ EXECUTANDO SIMULAÇÃO DE PROVA (1 ÚNICA RODADA)...")
    
    # Roda o motor
    try:
        df_audit, _, metricas_audit, alertas_audit = executar_motor_fintech_v10_production_ready(
            PREMISSAS, seed=42, modo_debug=False
        )
        print("✅ Motor executado com sucesso.")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO RODAR MOTOR: {e}")
        return

    # 5. ANÁLISE DO MÊS 1 (ONDE TUDO ACONTECE)
    print("="*80)
    print("🧾 EXTRATO DETALHADO: MÊS 1 (A REALIDADE MATEMÁTICA)")
    print("="*80)
    
    row = df_audit.iloc[0] # Mês 1
    
    # Variáveis extraídas do resultado real
    caixa_inicio = PREMISSAS['caixa_inicial']
    entrada_aporte = row['aportes_capital']
    receita_liquida = row['receita_liquida']
    
    saida_mkt = row['gasto_marketing']
    saida_infra = row['custo_infra_fixo']
    saida_pessoal = row['custo_pessoal']
    saida_capex = row['capex'] # Deve ser negativo se houve gasto
    saida_outros = row['total_opex'] - (saida_mkt + saida_infra + saida_pessoal)
    
    total_entradas = receita_liquida + entrada_aporte
    # Capex no motor é registrado negativo no fluxo, então somamos o valor absoluto se for gasto
    total_saidas = row['total_cogs'] + row['total_opex'] - row['capex'] 
    
    caixa_fim = row['caixa']
    
    print(f"(+) SALDO INICIAL:              R$ {caixa_inicio:,.2f}")
    print(f"(+) Aportes/Investimento:       R$ {entrada_aporte:,.2f}")
    print(f"(+) Receita Líquida (Vendas):   R$ {receita_liquida:,.2f}")
    print("-" * 40)
    print(f"(-) Gasto Marketing (Real):     R$ {saida_mkt:,.2f}")
    print(f"(-) Infraestrutura:             R$ {saida_infra:,.2f}")
    print(f"(-) Pessoal/Equipe:             R$ {saida_pessoal:,.2f}")
    print(f"(-) CAPEX (Equipamentos):       R$ {abs(saida_capex):,.2f}")
    print(f"(-) Outros (Impostos/Taxas):    R$ {row['total_deducoes']:,.2f}")
    print("-" * 40)
    print(f"(=) CAIXA FINAL MÊS 1 (REAL):   R$ {caixa_fim:,.2f}")
    
    print("\n🔎 DIAGNÓSTICO DE RUNWAY:")
    burn_rate_m1 = row['burn_rate']
    print(f"   • Burn Rate (Queima Mensal): R$ {burn_rate_m1:,.2f}")
    if burn_rate_m1 > 0:
        runway_calc = caixa_fim / burn_rate_m1
        print(f"   • Conta do Runway: {caixa_fim:.2f} / {burn_rate_m1:.2f} = {runway_calc:.2f} meses")
    else:
        print("   • Burn Rate Zero ou Positivo (Empresa gera caixa).")

    print("\n🔎 DIAGNÓSTICO DE MARKETING MÊS 2:")
    mkt_m2 = df_audit.iloc[1]['gasto_marketing']
    print(f"   • Caixa no início do Mês 2:  R$ {caixa_fim:,.2f}")
    print(f"   • Gatilho Reserva (20%):     R$ {PREMISSAS['caixa_reserva_operacional']*0.2:,.2f}")
    print(f"   • Marketing Gasto Mês 2:     R$ {mkt_m2:,.2f}")
    
    if caixa_fim < 0 and mkt_m2 > 0:
        print("   🚨 ALERTA: O Marketing gastou dinheiro com caixa negativo! O MOTOR AINDA TEM BUG.")
    elif caixa_fim < 0 and mkt_m2 == 0:
        print("   ✅ CORRETO: O Marketing foi cortado para zero porque o caixa está negativo.")
    elif caixa_fim > 0:
        print("   ℹ️ Caixa positivo, marketing segue a regra da reserva.")

    # Exportar CSV para user conferir
    # Salvar na pasta notebooks/data
    filename = 'data/auditoria_forense_v12_4.csv'
    
    # Criar pasta data caso não exista
    import os
    if not os.path.exists('data'):
        os.makedirs('data')

    df_audit.to_csv(filename, index=False)
    print(f"\n📂 Arquivo completo gerado: {filename}")

# Executar a auditoria
auditoria_forense_premissas()