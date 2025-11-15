"""
core/builders/capital_builder.py

Builder para configurar a estrutura de capital da empresa, incluindo aportes de
sócios e empréstimos.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class Aporte:
    """Representa um aporte de capital dos sócios."""
    valor: float
    data: date
    socio: str = "Investidor Anjo"

@dataclass
class Emprestimo:
    """Representa um empréstimo ou financiamento."""
    valor_principal: float
    taxa_juros_anual: float
    prazo_meses: int
    data_inicio: date
    carencia_meses: int = 0

class CapitalBuilder:
    """
    Builder para configurar a estrutura de capital.
    """
    def __init__(self, config):
        self.config = config
        self.aportes: List[Aporte] = []
        self.emprestimos: List[Emprestimo] = []

    def calcular_aporte_para_mes(self, mes: int) -> float:
        """
        Calcula o aporte de capital para um mês específico.
        Para retrocompatibilidade, replica a lógica de aporte fixo do motor antigo.
        """
        cfg = self.config
        
        # Futuramente, esta lógica irá iterar sobre self.aportes para aportes programados.
        # Por enquanto, fallback para a lógica antiga.
        if mes <= cfg.meses_aporte_fixo:
            return cfg.aporte_mensal_fixo
        return 0.0

    def add_aporte(self, valor: float, data: date, socio: str = "Investidor Anjo") -> 'CapitalBuilder':
        """Adiciona um aporte de capital."""
        self.aportes.append(Aporte(valor=valor, data=data, socio=socio))
        return self

    def add_emprestimo(self, valor_principal: float, taxa_juros_anual: float, prazo_meses: int, data_inicio: date, carencia_meses: int = 0) -> 'CapitalBuilder':
        """Adiciona um empréstimo."""
        self.emprestimos.append(Emprestimo(
            valor_principal=valor_principal,
            taxa_juros_anual=taxa_juros_anual,
            prazo_meses=prazo_meses,
            data_inicio=data_inicio,
            carencia_meses=carencia_meses
        ))
        return self

    def build(self):
        """Aplica a configuração de capital ao config."""
        if not hasattr(self.config, 'estrutura_capital'):
            self.config.estrutura_capital = {}
        
        self.config.estrutura_capital['aportes'] = self.aportes
        self.config.estrutura_capital['emprestimos'] = self.emprestimos
        
        # Assume que o config tem um método registrar_alteracao
        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Estrutura de Capital",
                detalhes={
                    'num_aportes': len(self.aportes),
                    'num_emprestimos': len(self.emprestimos)
                }
            )
        return self.config

# Exemplo de uso
if __name__ == '__main__':
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # Para teste, usamos uma classe de configuração mock
    class MockConfig:
        def __init__(self):
            self.estrutura_capital = {}
            self.alteracoes = []
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})

    config_inicial = MockConfig()

    capital_builder = CapitalBuilder(config_inicial)
    capital_builder.add_aporte(100000, date(2024, 1, 1), "Sócio A")
    capital_builder.add_emprestimo(50000, 0.12, 24, date(2024, 6, 1))
    
    config_final = capital_builder.build()

    print("Configuração de capital aplicada:")
    print(config_final.estrutura_capital)
    print("\nAlterações registradas:")
    print(config_final.alteracoes)
