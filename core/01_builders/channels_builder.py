"""
core/builders/channels_builder.py

Builder para configuração de canais de aquisição com CAC diferenciado.
Baseado na estratégia: SEO Orgânico + Performance Ads + Afiliados.

Características:
- CAC diferente por canal
- Conversão diferente por canal
- Mix de tráfego configurável
- CAC Pago vs. CAC Blended
- Payback period por canal
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TipoCanal(Enum):
    """Tipos de canal de aquisição"""
    ORGANICO = "organico"
    PAGO = "pago"
    REFERRAL = "referral"
    DIRETO = "direto"
    AFILIADO = "afiliado"
    PARCERIA = "parceria"

@dataclass
class CanalAquisicao:
    """
    Representa um canal de aquisição com suas métricas específicas.
    
    Exemplo:
        SEO Orgânico: mix=40%, conv_trial=8%, conv_pago=20%, cac=R$200
        Google Ads: mix=30%, conv_trial=4%, conv_pago=15%, cac=R$500
    """
    nome: str
    tipo: TipoCanal
    percentual_trafego: float  # 0.0 a 1.0 (ex: 0.40 = 40%)
    taxa_conversao_trial: float  # Conversão visitante → trial
    taxa_conversao_pagante: float  # Conversão trial → pagante
    cac_medio: float  # Custo de aquisição por cliente
    ativo: bool = True
    mes_inicio: int = 1
    mes_fim: Optional[int] = None
    
    # Custos de operação do canal (opcional)
    custo_fixo_mensal: float = 0.0  # Ex: salário de especialista
    custo_por_visitante: float = 0.0  # Ex: CPC no Google Ads
    
    # Métricas derivadas (calculadas)
    @property
    def taxa_conversao_combinada(self) -> float:
        """Taxa de conversão total: visitante → pagante"""
        return self.taxa_conversao_trial * self.taxa_conversao_pagante
    
    @property
    def ltv_cac_ratio(self) -> float:
        """Estimativa de LTV/CAC (precisa do LTV do config)"""
        # Será calculado pelo engine com LTV real
        return 0.0
    
    def validar(self) -> List[str]:
        """Valida consistência dos dados"""
        erros = []
        
        if not 0 <= self.percentual_trafego <= 1:
            erros.append(f"{self.nome}: percentual_trafego deve estar entre 0 e 1")
        
        if not 0 <= self.taxa_conversao_trial <= 1:
            erros.append(f"{self.nome}: taxa_conversao_trial deve estar entre 0 e 1")
        
        if not 0 <= self.taxa_conversao_pagante <= 1:
            erros.append(f"{self.nome}: taxa_conversao_pagante deve estar entre 0 e 1")
        
        if self.cac_medio < 0:
            erros.append(f"{self.nome}: cac_medio não pode ser negativo")
        
        return erros


class ChannelsBuilder:
    """
    Builder para configurar canais de aquisição.
    
    Uso:
        builder = ChannelsBuilder(config)
        builder.add_canal_organico("SEO", mix=0.40, conv_trial=0.08, conv_pago=0.20, cac=200)
        builder.add_canal_pago("Google Ads", mix=0.30, conv_trial=0.04, conv_pago=0.15, cac=500)
        builder.add_canal_afiliado("Programa Afiliados", mix=0.20, conv_trial=0.12, conv_pago=0.30, cac=100, comissao=0.20)
        builder.build()
    """
    
    def __init__(self, config):
        """
        Args:
            config: Instância de ConfigFinanceira
        """
        self.config = config
        self.canais: List[CanalAquisicao] = []
    
    def add_canal(
        self,
        nome: str,
        tipo: TipoCanal,
        percentual_trafego: float,
        taxa_conversao_trial: float,
        taxa_conversao_pagante: float,
        cac_medio: float,
        custo_fixo_mensal: float = 0.0,
        custo_por_visitante: float = 0.0,
        mes_inicio: int = 1
    ) -> 'ChannelsBuilder':
        """Adiciona canal genérico (fluent interface)"""
        canal = CanalAquisicao(
            nome=nome,
            tipo=tipo,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_fixo_mensal=custo_fixo_mensal,
            custo_por_visitante=custo_por_visitante,
            mes_inicio=mes_inicio
        )
        self.canais.append(canal)
        return self
    
    def add_canal_organico(
        self,
        nome: str,
        percentual_trafego: float,
        taxa_conversao_trial: float,
        taxa_conversao_pagante: float,
        cac_medio: float,
        custo_seo_mensal: float = 0.0
    ) -> 'ChannelsBuilder':
        """
        Adiciona canal orgânico (SEO, Content Marketing).
        
        Exemplo:
            builder.add_canal_organico(
                "SEO Orgânico",
                percentual_trafego=0.40,
                taxa_conversao_trial=0.08,
                taxa_conversao_pagante=0.20,
                cac_medio=200,
                custo_seo_mensal=1500  # Ferramentas + tempo
            )
        """
        return self.add_canal(
            nome=nome,
            tipo=TipoCanal.ORGANICO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_fixo_mensal=custo_seo_mensal
        )
    
    def add_canal_pago(
        self,
        nome: str,
        percentual_trafego: float,
        taxa_conversao_trial: float,
        taxa_conversao_pagante: float,
        cac_medio: float,
        cpc: float = 0.0
    ) -> 'ChannelsBuilder':
        """
        Adiciona canal pago (Google Ads, Facebook Ads).
        
        Exemplo:
            builder.add_canal_pago(
                "Google Ads",
                percentual_trafego=0.30,
                taxa_conversao_trial=0.04,
                taxa_conversao_pagante=0.15,
                cac_medio=500,
                cpc=2.50
            )
        """
        return self.add_canal(
            nome=nome,
            tipo=TipoCanal.PAGO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_por_visitante=cpc
        )
    
    def add_canal_afiliado(
        self,
        nome: str,
        percentual_trafego: float,
        taxa_conversao_trial: float,
        taxa_conversao_pagante: float,
        cac_medio: float,
        comissao_percentual: float = 0.20
    ) -> 'ChannelsBuilder':
        """
        Adiciona programa de afiliados.
        
        Exemplo:
            builder.add_canal_afiliado(
                "Programa de Afiliados",
                percentual_trafego=0.20,
                taxa_conversao_trial=0.12,
                taxa_conversao_pagante=0.30,
                cac_medio=100,
                comissao_percentual=0.20
            )
        
        Nota: A comissão será adicionada ao COGS via COGSBuilder
        """
        # Registra comissão no COGS
        if hasattr(self.config, 'comissao_afiliados'):
            from .cogs_builder import ComissaoAfiliado
            self.config.comissao_afiliados = ComissaoAfiliado(
                percentual_sobre_venda=comissao_percentual,
                mes_inicio_programa=1,
                percentual_vendas_via_afiliados=percentual_trafego
            )
        
        return self.add_canal(
            nome=nome,
            tipo=TipoCanal.AFILIADO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio
        )
    
    def add_canal_referral(
        self,
        nome: str,
        percentual_trafego: float,
        taxa_conversao_trial: float,
        taxa_conversao_pagante: float,
        cac_medio: float,
        incentivo_por_referral: float = 0.0
    ) -> 'ChannelsBuilder':
        """
        Adiciona programa de referral (indicação).
        
        Exemplo:
            builder.add_canal_referral(
                "Programa de Indicação",
                percentual_trafego=0.10,
                taxa_conversao_trial=0.15,
                taxa_conversao_pagante=0.35,
                cac_medio=50,
                incentivo_por_referral=20  # R$20 de crédito para quem indica
            )
        """
        return self.add_canal(
            nome=nome,
            tipo=TipoCanal.REFERRAL,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_fixo_mensal=0.0  # Custo de incentivo é proporcional
        )
    
    def calcular_cac_blended(self) -> float:
        """
        Calcula CAC Blended (média ponderada de todos os canais).
        
        Fórmula:
            CAC_Blended = Σ(CAC_canal × %_trafego_canal)
        """
        if not self.canais:
            return 0.0
        
        cac_blended = sum(
            canal.cac_medio * canal.percentual_trafego
            for canal in self.canais
            if canal.ativo
        )
        return cac_blended
    
    def calcular_cac_pago(self) -> float:
        """
        Calcula CAC Pago (média apenas dos canais pagos).
        """
        canais_pagos = [c for c in self.canais if c.tipo == TipoCanal.PAGO and c.ativo]
        
        if not canais_pagos:
            return 0.0
        
        total_trafego_pago = sum(c.percentual_trafego for c in canais_pagos)
        
        if total_trafego_pago == 0:
            return 0.0
        
        cac_pago = sum(
            c.cac_medio * (c.percentual_trafego / total_trafego_pago)
            for c in canais_pagos
        )
        return cac_pago
    
    def calcular_conversao_media(self) -> tuple:
        """
        Retorna (conv_trial_media, conv_pagante_media) ponderadas.
        """
        if not self.canais:
            return (0.0, 0.0)
        
        total_peso = sum(c.percentual_trafego for c in self.canais if c.ativo)
        
        if total_peso == 0:
            return (0.0, 0.0)
        
        conv_trial_media = sum(
            c.taxa_conversao_trial * (c.percentual_trafego / total_peso)
            for c in self.canais
            if c.ativo
        )
        
        conv_pagante_media = sum(
            c.taxa_conversao_pagante * (c.percentual_trafego / total_peso)
            for c in self.canais
            if c.ativo
        )
        
        return (conv_trial_media, conv_pagante_media)
    
    def validar(self) -> List[str]:
        """Valida configuração de canais"""
        erros = []
        
        # Valida cada canal
        for canal in self.canais:
            erros.extend(canal.validar())
        
        # Valida soma de percentuais (deve ser ~1.0)
        total_mix = sum(c.percentual_trafego for c in self.canais if c.ativo)
        if abs(total_mix - 1.0) > 0.01:
            erros.append(f"Soma dos percentuais de tráfego é {total_mix*100:.1f}% (deveria ser 100%)")
        
        return erros
    
    def build(self):
        """
        Aplica configuração ao config e retorna.
        Atualiza taxas de conversão médias no config.
        """
        # Valida antes de aplicar
        erros = self.validar()
        if erros:
            raise ValueError(f"Erros na configuração de canais:\n" + "\n".join(erros))
        
        # Salva canais no config
        if not hasattr(self.config, 'canais_aquisicao'):
            self.config.canais_aquisicao = []
        self.config.canais_aquisicao = self.canais
        
        # Atualiza taxas de conversão médias no config
        conv_trial, conv_pagante = self.calcular_conversao_media()
        self.config.taxa_conversao_visitante_trial = conv_trial
        self.config.taxa_conversao_trial_pagante = conv_pagante
        
        # Atualiza CACs no config
        self.config.cac_blended = self.calcular_cac_blended()
        self.config.cac_pago_meta = self.calcular_cac_pago()
        
        # Registra alteração
        self.config.registrar_alteracao(
            "Configuração de canais de aquisição",
            detalhes={
                'num_canais': len(self.canais),
                'cac_blended': self.config.cac_blended,
                'cac_pago': self.config.cac_pago_meta,
                'conv_trial_media': conv_trial,
                'conv_pagante_media': conv_pagante
            }
        )
        
        return self.config
    
    def gerar_relatorio(self) -> str:
        """Gera relatório textual da configuração"""
        if not self.canais:
            return "Nenhum canal configurado."
        
        linhas = [
            "═" * 70,
            "CONFIGURAÇÃO DE CANAIS DE AQUISIÇÃO",
            "═" * 70,
            ""
        ]
        
        for canal in self.canais:
            linhas.extend([
                f"📢 {canal.nome} ({canal.tipo.value.upper()})",
                f"   Mix de Tráfego:      {canal.percentual_trafego*100:.1f}%",
                f"   Conv. Trial:         {canal.taxa_conversao_trial*100:.1f}%",
                f"   Conv. Pagante:       {canal.taxa_conversao_pagante*100:.1f}%",
                f"   Conv. Combinada:     {canal.taxa_conversao_combinada*100:.2f}%",
                f"   CAC Médio:           R$ {canal.cac_medio:,.2f}",
                ""
            ])
        
        linhas.extend([
            "─" * 70,
            f"CAC BLENDED (Todos os canais):  R$ {self.calcular_cac_blended():,.2f}",
            f"CAC PAGO (Apenas pagos):        R$ {self.calcular_cac_pago():,.2f}",
            "",
            f"Conversão Média Trial:          {self.calcular_conversao_media()[0]*100:.2f}%",
            f"Conversão Média Pagante:        {self.calcular_conversao_media()[1]*100:.2f}%",
            "═" * 70
        ])
        
        return "\n".join(linhas)


# ============================================================================
# EXEMPLO DE USO - Estratégia SAM
# ============================================================================

def criar_estrategia_sam_canais(config):
    """
    Cria a estratégia de canais conforme documento SAM:
    - SEO Orgânico (40%)
    - Google Ads (30%)
    - Programa de Afiliados (20%)
    - Referral (10%)
    """
    builder = ChannelsBuilder(config)
    
    # SEO Orgânico: melhor conversão, CAC baixo
    builder.add_canal_organico(
        nome="SEO & Content Marketing",
        percentual_trafego=0.40,
        taxa_conversao_trial=0.08,
        taxa_conversao_pagante=0.20,
        cac_medio=200,
        custo_seo_mensal=1000  # Ferramentas + tempo
    )
    
    # Google Ads: conversão média, CAC meta R$500
    builder.add_canal_pago(
        nome="Google Ads (Performance)",
        percentual_trafego=0.30,
        taxa_conversao_trial=0.04,
        taxa_conversao_pagante=0.15,
        cac_medio=500,
        cpc=2.50
    )
    
    # Programa de Afiliados: alta conversão, CAC baixo
    builder.add_canal_afiliado(
        nome="Programa de Afiliados",
        percentual_trafego=0.20,
        taxa_conversao_trial=0.12,
        taxa_conversao_pagante=0.30,
        cac_medio=100,
        comissao_percentual=0.20  # 20% de comissão
    )
    
    # Referral: melhor conversão, CAC mínimo
    builder.add_canal_referral(
        nome="Programa de Indicação",
        percentual_trafego=0.10,
        taxa_conversao_trial=0.15,
        taxa_conversao_pagante=0.35,
        cac_medio=50,
        incentivo_por_referral=20  # R$20 de crédito
    )
    
    return builder.build()


if __name__ == "__main__":
    # Teste do builder
    from core.config import ConfigFinanceira
    
    config = ConfigFinanceira()
    config_atualizado = criar_estrategia_sam_canais(config)
    
    # Gera relatório
    builder = ChannelsBuilder(config)
    builder.canais = config_atualizado.canais_aquisicao
    print(builder.gerar_relatorio())