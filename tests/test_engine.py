"""
SAM Financial Model - Testes de Validação e Auditoria
Versão 1.0 - Testes Unitários Financeiros

Este módulo testa todos os componentes do modelo financeiro para garantir:
1. Lógica matemática correta
2. Flags de ativação funcionando
3. Cálculos contábeis consistentes

INSTRUÇÕES:
- Coloque este arquivo na pasta tests/
- Execute via: python -m tests.testes_validacao
- Ou importe no notebook: from tests.testes_validacao import executar_todos_testes
"""

import sys
import pandas as pd
import numpy as np
from typing import Dict, Any

# Importa os módulos do pacote core
try:
    from core import (
        ConfigFinanceira, 
        Funcionario, 
        FerramentaSaaS, 
        AtivoDepreciavel, 
        DespesaAnual, 
        ComissaoAfiliado,
        criar_config_padrao,
        criar_config_com_contratacoes,
        criar_config_pessimista,
        criar_config_otimista
    )
    from core.engine import MotorProjecaoFinanceira
    print("✅ Módulos importados com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)

# ============================================================================
# SEÇÃO 1: TESTES DE FLAGS DE ATIVAÇÃO
# ============================================================================

def test_flag_marketing():
    """Testa se a flag de marketing desativa o custo corretamente."""
    print("\n[Teste 1] Verificando flag de marketing...")
    
    config = ConfigFinanceira()
    config.ativar_marketing = False
    config.marketing_fase1_custo_fixo = 500.0
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(3)
    
    assert df['Custo_Marketing'].sum() == 0.0, f"Marketing não desligou! Soma: {df['Custo_Marketing'].sum()}"
    print("✅ Marketing desliga corretamente")

def test_flag_fundador():
    """Testa se a flag de fundador desativa o salário corretamente."""
    print("\n[Teste 2] Verificando flag de fundador...")
    
    config = ConfigFinanceira()
    config.ativar_fundador = False
    config.salario_fundador_valor = 5000.0
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(6)
    
    assert df['Salario_Pago'].sum() == 0.0, f"Fundador não desligou! Soma: {df['Salario_Pago'].sum()}"
    print("✅ Fundador desliga corretamente")

def test_flag_custo_ia():
    """Testa se a flag de custo IA desativa corretamente."""
    print("\n[Teste 3] Verificando flag de custo IA...")
    
    config = ConfigFinanceira()
    config.ativar_custo_ia = False
    config.custo_ia_por_usuario = 5.0
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(5)
    
    assert (df['Custo_IA'] == 0).all(), f"Custo IA não desligou! COGS: {df['Custo_IA'].sum()}"
    print("✅ Custo IA desliga corretamente")

def test_flag_infraestrutura():
    """Testa se as flags de infraestrutura desativam corretamente."""
    print("\n[Teste 4] Verificando flags de infraestrutura...")
    
    config = ConfigFinanceira()
    config.ativar_infra_tier1 = False
    config.ativar_infra_tier2 = False
    config.ativar_infra_tier3 = False
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(5)
    
    assert df['Custo_Infra'].sum() == 0.0, f"Infra não desligou! Soma: {df['Custo_Infra'].sum()}"
    print("✅ Infraestrutura desliga corretamente")

def test_flag_escritorio():
    """Testa se a flag de escritório desativa corretamente."""
    print("\n[Teste 5] Verificando flag de escritório...")
    
    config = ConfigFinanceira()
    config.ativar_escritorio = False
    config.escritorio_aluguel_mensal = 2000.0
    config.escritorio_mes_inicio = 1
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(3)
    
    assert df['Custo_Escritorio'].sum() == 0.0, f"Escritório não desligou! Soma: {df['Custo_Escritorio'].sum()}"
    print("✅ Escritório desliga corretamente")

def test_flag_ferramentas():
    """Testa se a flag de ferramentas SaaS desativa corretamente."""
    print("\n[Teste 6] Verificando flag de ferramentas...")
    
    config = ConfigFinanceira()
    config.ativar_ferramentas = False
    config.adicionar_ferramenta("Teste", "dev", 100.0, mes_inicio=1)
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(3)
    
    assert df['Custo_Ferramentas'].sum() == 0.0, f"Ferramentas não desligaram! Soma: {df['Custo_Ferramentas'].sum()}"
    print("✅ Ferramentas desligam corretamente")

# ============================================================================
# SEÇÃO 2: TESTES DE FUNCIONÁRIOS E CONTRATAÇÕES
# ============================================================================

def test_demitir_funcionario():
    """Testa se demitir funcionário reduz custos corretamente."""
    print("\n[Teste 7] Verificando demissão de funcionário...")
    
    config = criar_config_com_contratacoes()
    motor = MotorProjecaoFinanceira(config)
    df_original = motor.executar_projecao(24)
    
    # Demite o Dev Backend no mês 15
    config.equipe[0].ativo = False
    
    motor_apos = MotorProjecaoFinanceira(config)
    df_apos = motor_apos.executar_projecao(24)
    
    custo_mes_15_original = df_original[df_original['Mes'] == 15]['Custo_Pessoal_CLT'].iloc[0]
    custo_mes_15_apos = df_apos[df_apos['Mes'] == 15]['Custo_Pessoal_CLT'].iloc[0]
    
    assert custo_mes_15_apos < custo_mes_15_original, \
        f"Demissão não reduziu custos! Original: {custo_mes_15_original}, Após: {custo_mes_15_apos}"
    
    print(f"✅ Demissão reduziu custos de R${custo_mes_15_original:.2f} para R${custo_mes_15_apos:.2f}")

def test_funcionario_temporario():
    """Testa funcionário que trabalha por período limitado."""
    print("\n[Teste 8] Verificando funcionário temporário...")
    
    config = ConfigFinanceira()
    config.adicionar_funcionario(
        nome="Consultor Temporário",
        cargo="Consultor",
        salario_bruto=3000.0,
        mes_inicio=6,
        mes_fim=12,
        tipo="PJ"
    )
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(15)
    
    custo_mes_5 = df[df['Mes'] == 5]['Custo_Pessoal_PJ'].iloc[0]
    custo_mes_8 = df[df['Mes'] == 8]['Custo_Pessoal_PJ'].iloc[0]
    custo_mes_13 = df[df['Mes'] == 13]['Custo_Pessoal_PJ'].iloc[0]
    
    assert custo_mes_5 == 0.0, f"Funcionário ativo antes do início! Mês 5: {custo_mes_5}"
    assert custo_mes_8 == 3000.0, f"Funcionário não ativo no período! Mês 8: {custo_mes_8}"
    assert custo_mes_13 == 0.0, f"Funcionário ativo após término! Mês 13: {custo_mes_13}"
    
    print("✅ Funcionário temporário funciona corretamente")

# ============================================================================
# SEÇÃO 3: TESTES DE LOGICA MATEMATICA E RECEITA
# ============================================================================

def test_mrr_calculo():
    """Testa cálculo manual de MRR."""
    print("\n[Teste 9] Verificando cálculo de MRR...")
    
    config = ConfigFinanceira()
    config.visitantes_mes_1 = 1000
    config.taxa_conversao_visitante_trial = 0.05  # 5%
    config.taxa_conversao_trial_pagante = 0.20   # 20%
    config.arpu_medio_override = 100.0
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(1)
    
    # Manual: 1000 × 5% × 20% × 100 = 1000
    mrr_esperado = 1000.0
    mrr_calculado = df[df['Mes'] == 1]['MRR'].iloc[0]
    
    assert abs(mrr_calculado - mrr_esperado) < 0.01, \
        f"MRR incorreto! Esperado: {mrr_esperado}, Calculado: {mrr_calculado}"
    
    print(f"✅ MRR calculado corretamente: R${mrr_calculado:.2f}")

def test_cac_calculo():
    """Testa cálculo de CAC mensal."""
    print("\n[Teste 10] Verificando cálculo de CAC...")
    
    config = ConfigFinanceira()
    config.visitantes_mes_1 = 1000
    config.marketing_fase1_custo_fixo = 5000.0
    config.taxa_conversao_visitante_trial = 0.05
    config.taxa_conversao_trial_pagante = 0.15
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(1)
    
    novos_pagantes = df[df['Mes'] == 1]['Novos_Pagantes'].iloc[0]
    cac_calculado = df[df['Mes'] == 1]['CAC_Mensal'].iloc[0]
    
    assert novos_pagantes > 0, "Não houve novos pagantes!"
    
    # O motor usa o valor exato (7.5) para o cálculo, não o arredondado (8), para maior precisão.
    # Esperado: 1000 × 5% × 15% = 7.5 clientes
    cac_esperado = 5000.0 / (1000 * 0.05 * 0.15) # 5000 / 7.5 = 666.67
    
    assert abs(cac_calculado - cac_esperado) < 0.01, \
        f"CAC incorreto! Esperado: {cac_esperado:.2f}, Calculado: {cac_calculado:.2f}"
    
    print(f"✅ CAC calculado corretamente: R${cac_calculado:.2f} (esperado: R${cac_esperado:.2f})")

def test_ltv_calculo():
    """Testa cálculo de LTV."""
    print("\n[Teste 11] Verificando cálculo de LTV...")
    
    config = ConfigFinanceira()
    config.arpu_medio_override = 100.0
    config.churn_mensal = 0.05
    config.custo_ia_por_usuario = 20.0
    config.aliquota_impostos = 0.06
    config.taxa_pagamento_percentual = 0.0349
    
    # Calculado dinamicamente
    valor_esperado = ((100.0 * (1 - 0.06 - 0.0349)) - 20.0) / 0.05
    ltv_calculado = config.calcular_ltv()
    
    assert abs(ltv_calculado - valor_esperado) < (valor_esperado * 0.01), \
        f"LTV incorreto! Esperado: {valor_esperado:.2f}, Calculado: {ltv_calculado:.2f}"
    
    print(f"✅ LTV calculado corretamente: R${ltv_calculado:.2f}")

def test_ferramenta_temporaria():
    """Testa ferramenta SaaS com período limitado."""
    print("\n[Teste 12] Verificando ferramenta temporária...")
    
    config = ConfigFinanceira()
    ferramenta = FerramentaSaaS(
        nome="Ferramenta Temporária",
        categoria="teste",
        custo_mensal=1000.0,
        mes_inicio=3,
        mes_fim=5,
        ativa=True
    )
    config.ferramentas_saas.append(ferramenta)
    
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(6)
    
    custo_mes_2 = df[df['Mes'] == 2]['Custo_Ferramentas'].iloc[0]
    custo_mes_4 = df[df['Mes'] == 4]['Custo_Ferramentas'].iloc[0]
    custo_mes_6 = df[df['Mes'] == 6]['Custo_Ferramentas'].iloc[0]
    
    assert custo_mes_2 == 0.0, f"Ferramenta ativa antes do início! Mês 2: {custo_mes_2}"
    assert custo_mes_4 == 1000.0, f"Ferramenta não ativa no período! Mês 4: {custo_mes_4}"
    assert custo_mes_6 == 0.0, f"Ferramenta ativa após término! Mês 6: {custo_mes_6}"
    
    print("✅ Ferramenta temporária funciona corretamente")

# ============================================================================
# SEÇÃO 4: TESTES DE INTEGRIDADE CONTÁBIL
# ============================================================================

def test_consistencia_contabil():
    """Verifica se Receita - COGS - OPEX = Resultado Operacional."""
    print("\n[Teste 13] Verificando consistência contábil...")
    
    config = criar_config_com_contratacoes()
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(12)
    
    for _, row in df.iterrows():
        resultado_calculado = row['MRR'] - row['COGS_Total'] - row['OPEX_Total']
        resultado_tabela = row['Resultado_Operacional']
        
        # Tolerância aumentada para 0.05 para lidar com erros de arredondamento de ponto flutuante
        assert abs(resultado_calculado - resultado_tabela) < 0.05, \
            f"Inconsistência no mês {row['Mes']}: Calculado={resultado_calculado:.2f}, Tabela={resultado_tabela:.2f}"
    
    print("✅ Tabela contábil está consistente em todos os meses")

def test_evolucao_caixa():
    """Verifica se Saldo_Caixa(mês N) = Saldo_Caixa(mês N-1) + Fluxo_Caixa(mês N)."""
    print("\n[Teste 14] Verificando evolução de caixa...")
    
    config = ConfigFinanceira()
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(6)
    
    saldo_anterior = config.capital_inicial_caixa
    for _, row in df.iterrows():
        saldo_calculado = saldo_anterior + row['Fluxo_Caixa']
        saldo_tabela = row['Saldo_Caixa']
        
        # Tolerância aumentada para 0.05 para lidar com erros de arredondamento de ponto flutuante
        assert abs(saldo_calculado - saldo_tabela) < 0.05, \
            f"Caixa inconsistente no mês {row['Mes']}: Calculado={saldo_calculado:.2f}, Tabela={saldo_tabela:.2f}"
        
        saldo_anterior = saldo_tabela
    
    print("✅ Fluxo de caixa está matematicamente correto")

def test_colunas_nao_nulas():
    """Garante que nenhuma coluna importante retorna NaN."""
    print("\n[Teste 15] Verificando ausência de valores nulos...")
    
    config = criar_config_com_contratacoes()
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(12)
    
    colunas_criticas = ['MRR', 'Saldo_Caixa', 'Resultado_Operacional', 'CAC_Mensal']
    for coluna in colunas_criticas:
        assert not df[coluna].isna().any(), f"Coluna {coluna} contém valores NaN!"
    
    print("✅ Nenhuma coluna crítica contém valores nulos")

# ============================================================================
# EXECUTOR PRINCIPAL
# ============================================================================

def executar_todos_testes():
    """Executa todos os testes e retorna relatório."""
    print("=" * 70)
    print("🧪 INICIANDO BATERIA DE TESTES - SAM FINANCIAL MODEL")
    print("=" * 70)
    
    testes = [
        test_flag_marketing,
        test_flag_fundador,
        test_flag_custo_ia,
        test_flag_infraestrutura,
        test_flag_escritorio,
        test_flag_ferramentas,
        test_demitir_funcionario,
        test_funcionario_temporario,
        test_mrr_calculo,
        test_cac_calculo,
        test_ltv_calculo,
        test_ferramenta_temporaria,
        test_consistencia_contabil,
        test_evolucao_caixa,
        test_colunas_nao_nulas,
    ]
    
    total = len(testes)
    aprovados = 0
    reprovados = 0
    
    for i, teste in enumerate(testes, 1):
        try:
            print(f"\n{'─' * 70}")
            print(f"Teste {i}/{total}: {teste.__doc__}")
            print(f"{'─' * 70}")
            teste()
            aprovados += 1
            print("🟢 APROVADO")
        except Exception as e:
            reprovados += 1
            print(f"🔴 REPROVADO: {str(e)}")
    
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO FINAL")
    print("=" * 70)
    print(f"Total de Testes: {total}")
    print(f"✅ Aprovados: {aprovados}")
    print(f"❌ Reprovados: {reprovados}")
    print(f"Taxa de Sucesso: {aprovados/total*100:.1f}%")
    
    if reprovados == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! O MODELO ESTÁ VALIDADO.")
    else:
        print(f"\n⚠️  {reprovados} testes falharam. Revise o modelo antes de prosseguir.")
    
    return reprovados == 0

# ============================================================================
# EXECUÇÃO DIRETA
# ============================================================================

if __name__ == "__main__":
    # Executa todos os testes quando o arquivo é rodado diretamente
    sucesso = executar_todos_testes()
    sys.exit(0 if sucesso else 1)