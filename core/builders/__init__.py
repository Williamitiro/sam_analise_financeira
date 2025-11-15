"""
core/builders/__init__.py

Sistema completo de Builders para configuração avançada do SAM Financial Model.
Baseado no modelo de negócio: Plataforma SaaS de Trading (SAM).

Última atualização: 2025-01-15
"""

from .capital_builder import CapitalBuilder, Aporte, Emprestimo
from .revenue_builder import RevenueBuilder, Plano, AddOn
from .cogs_builder import COGSBuilder, TaxaPagamento, ComissaoAfiliado, ComissaoParceiroComercial
from .channels_builder import ChannelsBuilder, CanalAquisicao
from .infra_builder import InfraBuilder, TierInfra, ComponenteInfra
from .marketing_builder import MarketingBuilder, FaseMarketing, OrcamentoCanal
from .team_builder import TeamBuilder, Cargo, GatilhoContratacao
from .tools_builder import ToolsBuilder, FerramentaSaaS
from .risk_builder import RiskBuilder, CenarioRisco, Contingencia
from .tax_builder import TaxBuilder, FaixaTributaria
from .scenario_builder import ScenarioBuilder

__all__ = [
    # Capital
    'CapitalBuilder', 'Aporte', 'Emprestimo',
    
    # Receita
    'RevenueBuilder', 'Plano', 'AddOn',
    
    # COGS
    'COGSBuilder', 'TaxaPagamento', 'ComissaoAfiliado', 'ComissaoParceiroComercial',
    
    # Canais
    'ChannelsBuilder', 'CanalAquisicao',
    
    # Infraestrutura
    'InfraBuilder', 'TierInfra', 'ComponenteInfra',
    
    # Marketing
    'MarketingBuilder', 'FaseMarketing', 'OrcamentoCanal',
    
    # Equipe
    'TeamBuilder', 'Cargo', 'GatilhoContratacao',
    
    # Ferramentas
    'ToolsBuilder', 'FerramentaSaaS',
    
    # Risco
    'RiskBuilder', 'CenarioRisco', 'Contingencia',
    
    # Impostos
    'TaxBuilder', 'FaixaTributaria',
    
    # Cenários
    'ScenarioBuilder'
]