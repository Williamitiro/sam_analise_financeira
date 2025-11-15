"""
core/builders/risk_builder.py

Builder para configurar cenários de risco e planos de contingência.
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CenarioRisco:
    """Representa um cenário de risco."""
    nome: str
    probabilidade: float  # 0.0 a 1.0
    impacto_financeiro: float
    descricao: str

@dataclass
class Contingencia:
    """Representa um plano de contingência."""
    risco_associado: str
    acao: str
    custo_contingencia: float

class RiskBuilder:
    """
    Builder para configurar riscos e contingências.
    """
    def __init__(self, config):
        self.config = config
        self.cenarios_risco: List[CenarioRisco] = []
        self.contingencias: List[Contingencia] = []

    def add_risco(self, nome: str, probabilidade: float, impacto_financeiro: float, descricao: str) -> 'RiskBuilder':
        """Adiciona um cenário de risco."""
        self.cenarios_risco.append(CenarioRisco(
            nome=nome,
            probabilidade=probabilidade,
            impacto_financeiro=impacto_financeiro,
            descricao=descricao
        ))
        return self

    def add_contingencia(self, risco_associado: str, acao: str, custo_contingencia: float) -> 'RiskBuilder':
        """Adiciona um plano de contingência."""
        self.contingencias.append(Contingencia(
            risco_associado=risco_associado,
            acao=acao,
            custo_contingencia=custo_contingencia
        ))
        return self

    def build(self):
        """Aplica a configuração de risco ao config."""
        if not hasattr(self.config, 'riscos'):
            self.config.riscos = {}
            
        self.config.riscos['cenarios'] = self.cenarios_risco
        self.config.riscos['contingencias'] = self.contingencias

        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Riscos e Contingências",
                detalhes={
                    'num_cenarios_risco': len(self.cenarios_risco),
                    'num_contingencias': len(self.contingencias)
                }
            )
        return self.config

# Exemplo de uso
if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    class MockConfig:
        def __init__(self):
            self.riscos = {}
            self.alteracoes = []
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})

    config_inicial = MockConfig()

    risk_builder = RiskBuilder(config_inicial)
    risk_builder.add_risco("Aumento do Churn", 0.3, 50000, "Aumento inesperado na taxa de cancelamento.")
    risk_builder.add_contingencia("Aumento do Churn", "Oferecer descontos para retenção.", 10000)
    
    config_final = risk_builder.build()

    print("Configuração de riscos aplicada:")
    print(config_final.riscos)
    print("\nAlterações registradas:")
    print(config_final.alteracoes)
