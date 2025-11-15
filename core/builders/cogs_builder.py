"""
core/builders/cogs_builder.py - Custos Variáveis Completos
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class TaxaPagamento:
    """Taxa de gateway de pagamento"""
    percentual: float  # Ex: 0.0349 = 3.49%
    taxa_fixa: float  # Ex: 0.39 = R$0,39
    provider: str = "Stripe"

@dataclass
class ComissaoAfiliado:
    """Comissão de programa de afiliados"""
    percentual_sobre_venda: float  # Ex: 0.20 = 20%
    mes_inicio_programa: int = 1
    percentual_vendas_via_afiliados: float = 0.0  # Ex: 0.30 = 30% das vendas

@dataclass
class ComissaoParceiroComercial:
    """Comissão de parceiros comerciais"""
    percentual_sobre_venda: float
    mes_inicio: int = 1
    percentual_vendas_via_parceiro: float = 0.0

class COGSBuilder:
    """
    Builder para custos variáveis (COGS).
    
    Uso:
        builder = COGSBuilder(config)
        builder.taxa_pagamento(0.035, 0.39, "Stripe")
        builder.comissao_afiliados(0.20, percentual_vendas=0.30)
        builder.comissao_parceiros(0.15, percentual_vendas=0.10)
        builder.custo_ia_por_usuario(5.00)
        builder.cashback_usuarios(0.05)
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
    
    def calcular_cogs_para_mes(self, mrr: float, novos_pagantes: float, usuarios: float) -> Dict[str, float]:
        """
        Calcula todos os componentes do COGS para um determinado mês.
        Para retrocompatibilidade, replica a lógica do motor antigo.
        """
        cfg = self.config
        custos = {
            'ia': 0.0,
            'impostos': 0.0,
            'taxas': 0.0,
            'comissoes': 0.0
        }

        if cfg.ativar_custo_ia:
            custos['ia'] = usuarios * cfg.custo_ia_por_usuario
        
        if cfg.ativar_impostos:
            custos['impostos'] = mrr * cfg.aliquota_impostos
        
        if cfg.ativar_taxas_pgto:
            custos['taxas'] = (novos_pagantes * cfg.taxa_pagamento_fixa_por_transacao) + (mrr * cfg.taxa_pagamento_percentual)
            
        if cfg.ativar_comissoes_afiliado and hasattr(cfg, 'comissao_afiliados') and cfg.comissao_afiliados is not None:
            # A lógica de 'mês de início' deve ser tratada no motor ou aqui.
            # Por enquanto, replicamos a lógica simples.
            custos['comissoes'] = mrr * cfg.comissao_afiliados.percentual_sobre_venda * cfg.comissao_afiliados.percentual_vendas_via_afiliados

        return custos

    def taxa_pagamento(self, percentual: float, taxa_fixa: float, provider: str = "Stripe") -> 'COGSBuilder':
        """Configura taxa de gateway"""
        self.config.taxa_pagamento_percentual = percentual
        self.config.taxa_pagamento_fixa_por_transacao = taxa_fixa
        self.config.gateway_provider = provider
        return self
    
    def comissao_afiliados(self, percentual: float, percentual_vendas: float, mes_inicio: int = 1) -> 'COGSBuilder':
        """Configura comissão de afiliados"""
        self.config.comissao_afiliados = ComissaoAfiliado(
            percentual_sobre_venda=percentual,
            mes_inicio_programa=mes_inicio,
            percentual_vendas_via_afiliados=percentual_vendas
        )
        return self
    
    def comissao_parceiros(self, percentual: float, percentual_vendas: float, mes_inicio: int = 1) -> 'COGSBuilder':
        """Configura comissão de parceiros"""
        self.config.comissao_parceiros = ComissaoParceiroComercial(
            percentual_sobre_venda=percentual,
            mes_inicio=mes_inicio,
            percentual_vendas_via_parceiro=percentual_vendas
        )
        return self
    
    def custo_ia_por_usuario(self, custo: float) -> 'COGSBuilder':
        """Configura custo de IA por usuário"""
        self.config.custo_ia_por_usuario = custo
        return self
    
    def cashback_usuarios(self, percentual_receita: float) -> 'COGSBuilder':
        """Configura cashback/incentivos"""
        self.config.cashback_percentual = percentual_receita
        return self
    
    def build(self):
        """Aplica ao config"""
        self.config.registrar_alteracao("Configuração de COGS")
        return self.config

if __name__ == '__main__':
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    from core.config import ConfigFinanceira

    config = ConfigFinanceira()
    
    # Exemplo de uso
    builder = COGSBuilder(config)
    builder.taxa_pagamento(0.035, 0.39, "Stripe")
    builder.comissao_afiliados(0.20, percentual_vendas=0.30)
    builder.custo_ia_por_usuario(5.00)
    builder.build()

    print("--- Configuração de COGS ---")
    print(f"Gateway: {config.gateway_provider} ({config.taxa_pagamento_percentual:.3%} + R$ {config.taxa_pagamento_fixa_por_transacao:.2f})")
    if hasattr(config, 'comissao_afiliados'):
        print(f"Comissão Afiliados: {config.comissao_afiliados.percentual_sobre_venda:.1%}")
    print(f"Custo IA por usuário: R$ {config.custo_ia_por_usuario:.2f}")
