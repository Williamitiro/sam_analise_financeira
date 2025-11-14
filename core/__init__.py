 
# core/__init__.py
"""
SAM Financial Model - Core Package
Este arquivo expõe as classes e funções principais do módulo core,
permitindo imports limpos como: from core import ConfigFinanceira
"""

from .config import (
    ConfigFinanceira,
    Funcionario,
    FerramentaSaaS,
    AtivoDepreciavel,
    DespesaAnual,
    ComissaoAfiliado,
    criar_config_padrao,
    criar_config_com_contratacoes,
    criar_config_pessimista,
    criar_config_otimista,
    CONFIG_PADRAO,
    CONFIG_COM_CONTRATACOES,
    CONFIG_PESSIMISTA,
    CONFIG_OTIMISTA
)

from .engine import MotorProjecaoFinanceira

__all__ = [
    'ConfigFinanceira',
    'Funcionario',
    'FerramentaSaaS',
    'AtivoDepreciavel',
    'DespesaAnual',
    'ComissaoAfiliado',
    'criar_config_padrao',
    'criar_config_com_contratacoes',
    'criar_config_pessimista',
    'criar_config_otimista',
    'CONFIG_PADRAO',
    'CONFIG_COM_CONTRATACOES',
    'CONFIG_PESSIMISTA',
    'CONFIG_OTIMISTA',
    'MotorProjecaoFinanceira'
]