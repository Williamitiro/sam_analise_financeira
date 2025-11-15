"""
core/builders/revenue_builder.py

Builder para configurar os planos de assinatura e a estratégia de receita.
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Plano:
    """Representa um plano de assinatura."""
    nome: str
    preco_mensal: float
    percentual_clientes: float  # 0.0 a 1.0
    churn_mensal: float

@dataclass
class AddOn:
    """Representa um add-on ou compra avulsa."""
    nome: str
    preco: float
    taxa_adocao: float  # Percentual de clientes que compram

class RevenueBuilder:
    """
    Builder para configurar a receita.
    """
    def __init__(self, config):
        self.config = config
        self.planos: List[Plano] = []
        self.addons: List[AddOn] = []

    def add_plano(self, nome: str, preco_mensal: float, percentual_clientes: float, churn_mensal: float) -> 'RevenueBuilder':
        """Adiciona um plano de assinatura."""
        self.planos.append(Plano(
            nome=nome,
            preco_mensal=preco_mensal,
            percentual_clientes=percentual_clientes,
            churn_mensal=churn_mensal
        ))
        return self

    def add_addon(self, nome: str, preco: float, taxa_adocao: float) -> 'RevenueBuilder':
        """Adiciona um add-on."""
        self.addons.append(AddOn(nome=nome, preco=preco, taxa_adocao=taxa_adocao))
        return self

    def calcular_receita_para_mes(self, usuarios: float) -> tuple[float, float]:
        """
        Calcula o MRR e a ARPU para um determinado mês.
        Para retrocompatibilidade, usa a propriedade `arpu_medio` do objeto de configuração,
        que já lida com o cálculo ponderado dos planos simples.
        """
        cfg = self.config
        
        # Lógica de fallback: usa o cálculo de ARPU ponderado do config.
        # Isso garante que o app/main.py continue funcionando sem alterações.
        arpu = cfg.arpu_medio
        
        # A lógica futura aqui poderia verificar self.planos e self.addons
        # para um cálculo mais complexo se eles existirem.
        
        mrr = usuarios * arpu if cfg.ativar_receita_por_usuario else 0.0
        
        return mrr, arpu

    def build(self):
        """Aplica a configuração de receita ao config."""
        if not hasattr(self.config, 'receita'):
            self.config.receita = {}
            
        self.config.receita['planos'] = self.planos
        self.config.receita['addons'] = self.addons

        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Receita",
                detalhes={
                    'num_planos': len(self.planos),
                    'num_addons': len(self.addons)
                }
            )
        return self.config

# Exemplo de uso
if __name__ == '__main__':
    import sys
    import os
    from datetime import date
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    class MockConfig:
        def __init__(self):
            self.receita = {}
            self.alteracoes = []
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})

    config_inicial = MockConfig()

    revenue_builder = RevenueBuilder(config_inicial)
    revenue_builder.add_plano("Básico", 79.90, 0.6, 0.05)
    revenue_builder.add_plano("Profissional", 149.90, 0.4, 0.03)
    revenue_builder.add_addon("Consultoria", 500, 0.1)
    
    config_final = revenue_builder.build()

    print("Configuração de receita aplicada:")
    print(config_final.receita)
    print("\nAlterações registradas:")
    print(config_final.alteracoes)
