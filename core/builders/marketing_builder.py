"""
core/builders/marketing_builder.py - Fases de Marketing
"""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class OrcamentoCanal:
    """Define o orçamento para um canal de marketing específico."""
    nome_canal: str
    percentual_orcamento: float  # 0.0 a 1.0
    cac_alvo: Optional[float] = None

@dataclass
class FaseMarketing:
    """Fase de marketing com orçamento e regras"""
    numero: int
    nome: str
    mes_inicio: int
    mes_fim: Optional[int]
    tipo_orcamento: str  # 'fixo', 'percentual_receita', 'percentual_lucro', 'cac_target'
    valor: float  # Valor fixo OU percentual OU CAC alvo
    descricao: str = ""
    canais_priorizados: List[str] = field(default_factory=list)
    
    def calcular_orcamento(self, mrr: float, lucro_bruto: float, novos_clientes: int) -> float:
        """Calcula orçamento de marketing para o mês"""
        if self.tipo_orcamento == 'fixo':
            return self.valor
        elif self.tipo_orcamento == 'percentual_receita':
            return mrr * self.valor
        elif self.tipo_orcamento == 'percentual_lucro':
            return max(0, lucro_bruto * self.valor)
        elif self.tipo_orcamento == 'cac_target':
            return novos_clientes * self.valor  # CAC alvo × clientes
        return 0.0

class MarketingBuilder:
    """
    Builder para estratégia de marketing em fases.
    
    Uso:
        builder = MarketingBuilder(config)
        builder.fase_validacao(1, 6, 1000)
        builder.fase_crescimento(7, 18, 0.25, 'percentual_lucro')
        builder.fase_escala(19, 36, 0.20, 'percentual_receita')
        builder.fase_maturidade(37, None, 300, 'cac_target')
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.fases: List[FaseMarketing] = []

    def calcular_custo_para_mes(self, mes: int, lucro_bruto: float) -> float:
        """
        Calcula o custo de marketing para um mês específico.
        Para retrocompatibilidade, replica a lógica de 2 fases do motor antigo.
        """
        cfg = self.config

        if not cfg.ativar_marketing:
            return 0.0
        
        # Futuramente, esta lógica irá iterar sobre self.fases.
        # Por enquanto, usamos a lógica antiga para não quebrar o app.
        if mes <= cfg.marketing_fase1_duracao_meses:
            return cfg.marketing_fase1_custo_fixo
        else:
            # Fase 2: percentual sobre o lucro bruto, garantindo que não seja negativo.
            return max(0.0, lucro_bruto * cfg.marketing_fase2_perc_lucro_bruto)

    def fase_validacao(
        self,
        mes_inicio: int,
        mes_fim: int,
        orcamento_fixo: float,
        canais: List[str] = None
    ) -> 'MarketingBuilder':
        """Fase 1: Validação com orçamento fixo"""
        fase = FaseMarketing(
            numero=1,
            nome="Validação",
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            tipo_orcamento='fixo',
            valor=orcamento_fixo,
            descricao="Orçamento fixo para validar canais",
            canais_priorizados=canais or ["SEO", "Content"]
        )
        self.fases.append(fase)
        return self
    
    def fase_crescimento(
        self,
        mes_inicio: int,
        mes_fim: Optional[int],
        percentual: float,
        base: str = 'percentual_lucro',
        canais: List[str] = None
    ) -> 'MarketingBuilder':
        """Fase 2: Crescimento com reinvestimento"""
        fase = FaseMarketing(
            numero=2,
            nome="Crescimento",
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            tipo_orcamento=base,
            valor=percentual,
            descricao=f"Reinvestir {percentual*100:.0f}% do {base}",
            canais_priorizados=canais or ["Ads", "SEO", "Referral"]
        )
        self.fases.append(fase)
        return self
    
    def fase_escala(
        self,
        mes_inicio: int,
        mes_fim: Optional[int],
        percentual_receita: float,
        canais: List[str] = None
    ) -> 'MarketingBuilder':
        """Fase 3: Escala agressiva"""
        fase = FaseMarketing(
            numero=3,
            nome="Escala",
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            tipo_orcamento='percentual_receita',
            valor=percentual_receita,
            descricao=f"Investir {percentual_receita*100:.0f}% da receita",
            canais_priorizados=canais or ["Ads", "Eventos", "Parceiros"]
        )
        self.fases.append(fase)
        return self
    
    def fase_maturidade(
        self,
        mes_inicio: int,
        cac_target: float,
        canais: List[str] = None
    ) -> 'MarketingBuilder':
        """Fase 4: Maturidade com CAC alvo"""
        fase = FaseMarketing(
            numero=4,
            nome="Maturidade",
            mes_inicio=mes_inicio,
            mes_fim=None,
            tipo_orcamento='cac_target',
            valor=cac_target,
            descricao=f"Otimizar para CAC = R${cac_target:.0f}",
            canais_priorizados=canais or ["Organic", "Referral", "Brand"]
        )
        self.fases.append(fase)
        return self
    
    def build(self):
        """Aplica ao config"""
        self.config.fases_marketing = self.fases
        self.config.registrar_alteracao("Estratégia de marketing em fases",
                                       detalhes={'num_fases': len(self.fases)})
        return self.config

if __name__ == '__main__':
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    from core.config import ConfigFinanceira

    config = ConfigFinanceira()
    
    # Exemplo de uso
    builder = MarketingBuilder(config)
    builder.fase_validacao(1, 6, 1000)
    builder.fase_crescimento(7, 18, 0.25, 'percentual_lucro')
    builder.fase_escala(19, 36, 0.20, 'percentual_receita')
    builder.fase_maturidade(37, 300, 'cac_target')
    builder.build()

    print("--- Fases de Marketing SAM ---")
    for fase in config.fases_marketing:
        print(f"Fase {fase.numero}: {fase.nome} (Mês {fase.mes_inicio} - {fase.mes_fim or '...'})")
        print(f"  - Orçamento: {fase.tipo_orcamento}, Valor: {fase.valor}")
        print(f"  - Descrição: {fase.descricao}")
