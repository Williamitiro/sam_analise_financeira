import pytest
import pandas as pd

from core.config import ConfigFinanceira
from core.engine import MotorProjecaoFinanceira
from core.analytics.insights_engine import InsightsEngine
from core.analytics.cohorts import gerar_cohort_matrix

def test_full_projection_run():
    """
    Testa a execução completa da projeção financeira, desde a configuração até a análise.
    Este é um teste de integração para garantir que todos os componentes do core funcionam juntos.
    """
    # 1. Configuração: Usa a configuração padrão
    config = ConfigFinanceira()

    # 2. Execução do Motor de Projeção
    motor = MotorProjecaoFinanceira(config)
    df_projecao = motor.executar_projecao()
    kpis = motor.calcular_kpis()

    # Verifica se as saídas principais do motor não são nulas ou vazias
    assert df_projecao is not None
    assert not df_projecao.empty
    assert isinstance(df_projecao, pd.DataFrame)
    assert len(df_projecao) == 36

    assert kpis is not None
    assert isinstance(kpis, dict)
    assert "MRR_Final" in kpis
    assert kpis["MRR_Final"] > 0

    # 3. Execução da Camada de Análise
    insights_engine = InsightsEngine(df_projecao, kpis, config)
    insights = insights_engine.generate_all()

    df_cohorts = gerar_cohort_matrix(df_projecao)

    # Verifica as saídas da camada de análise
    assert insights is not None
    assert isinstance(insights, dict)
    assert "alertas" in insights

    assert df_cohorts is not None
    assert not df_cohorts.empty
    assert isinstance(df_cohorts, pd.DataFrame)
    
    # Verifica se não há valores NaN na matriz de cohorts
    assert not df_cohorts.isnull().values.any()

    print("\n✅ Teste de integração do backend concluído com sucesso!")
