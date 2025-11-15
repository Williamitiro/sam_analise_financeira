"""
core/builders/tax_builder.py

Builder para configurar a estrutura de impostos.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class FaixaTributaria:
    """Representa uma faixa de tributação."""
    limite_superior: float
    aliquota: float

class TaxBuilder:
    """
    Builder para configurar impostos.
    """
    def __init__(self, config):
        self.config = config
        self.faixas: List[FaixaTributaria] = []

    def add_faixa(self, limite_superior: float, aliquota: float) -> 'TaxBuilder':
        """Adiciona uma faixa de tributação."""
        self.faixas.append(FaixaTributaria(limite_superior=limite_superior, aliquota=aliquota))
        return self

    def build(self):
        """Aplica a configuração de impostos ao config."""
        if not hasattr(self.config, 'impostos'):
            self.config.impostos = {}
        
        self.config.impostos['faixas'] = sorted(self.faixas, key=lambda f: f.limite_superior)

        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Impostos",
                detalhes={'num_faixas': len(self.faixas)}
            )
        return self.config

# Exemplo de uso
if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    class MockConfig:
        def __init__(self):
            self.impostos = {}
            self.alteracoes = []
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})

    config_inicial = MockConfig()

    tax_builder = TaxBuilder(config_inicial)
    tax_builder.add_faixa(180000, 0.04)
    tax_builder.add_faixa(360000, 0.073)
    
    config_final = tax_builder.build()

    print("Configuração de impostos aplicada:")
    print(config_final.impostos)
    print("\nAlterações registradas:")
    print(config_final.alteracoes)
