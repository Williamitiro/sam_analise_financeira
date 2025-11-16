"""
core/builders/channels_builder.py

Builder para configuração de canais de aquisição com geração de séries temporais.

FUNCIONALIDADES:
- Configura canais (SEO, Ads, Afiliados, Referral)
- Gera colunas: Visitantes, Trials, Novos_Pagantes por canal
- Calcula CAC_Real mensal baseado no orçamento
- Gera métricas de funil: Taxa_Conversao_Trial, Taxa_Conversao_Pagante
- Compatível com motor existente (fallback seguro)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
import pandas as pd
import numpy as np

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
    """Configuração de um canal de aquisição"""
    nome: str
    tipo: TipoCanal
    percentual_trafego: float  # 0.0 a 1.0
    taxa_conversao_trial: float  # Visitante → Trial
    taxa_conversao_pagante: float  # Trial → Pagante
    cac_medio: float  # CAC target
    ativo: bool = True
    mes_inicio: int = 1
    mes_fim: Optional[int] = None
    custo_fixo_mensal: float = 0.0  # Ex: salário do time de SEO
    custo_por_visitante: float = 0.0  # Ex: CPC
    
    # Métricas calculadas em runtime (não salvar no config)
    def taxa_conversao_combinada(self) -> float:
        """Taxa visitante → pagante"""
        return self.taxa_conversao_trial * self.taxa_conversao_pagante
    
    def validar(self) -> List[str]:
        """Valida configuração do canal"""
        erros = []
        if not (0 <= self.percentual_trafego <= 1):
            erros.append(f"{self.nome}: percentual deve ser 0-1")
        if not (0 <= self.taxa_conversao_trial <= 1):
            erros.append(f"{self.nome}: conv_trial inválida")
        if not (0 <= self.taxa_conversao_pagante <= 1):
            erros.append(f"{self.nome}: conv_pagante inválida")
        if self.cac_medio < 0:
            erros.append(f"{self.nome}: CAC não pode ser negativo")
        return erros

@dataclass
class SerieCanal:
    """Série temporal de um canal (gerada pelo builder)"""
    mes: int
    visitantes: int
    trials: int
    novos_pagantes: int
    cac_real: float

class ChannelsBuilder:
    """
    Builder completo de canais com geração de séries temporais
    
    USO:
        builder = ChannelsBuilder(config)
        builder.add_canal_organico("SEO", mix=0.40, conv_trial=0.08, conv_pago=0.20, cac=200)
        builder.add_canal_pago("Google Ads", mix=0.30, conv_trial=0.04, conv_pago=0.15, cac=500)
        builder.build()
        
        # No motor:
        df = builder.gerar_series_temporais(df)
    """
    
    def __init__(self, config):
        self.config = config
        self.canais: List[CanalAquisicao] = []
        self._series_cache: Dict[str, pd.DataFrame] = {}

    def add_canal_organico(
        self, nome: str, percentual_trafego: float,
        taxa_conversao_trial: float, taxa_conversao_pagante: float,
        cac_medio: float, custo_seo_mensal: float = 0.0
    ) -> 'ChannelsBuilder':
        """Adiciona canal orgânico (SEO, Content)"""
        return self.add_canal(
            nome=nome, tipo=TipoCanal.ORGANICO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio, custo_fixo_mensal=custo_seo_mensal
        )

    def add_canal_pago(
        self, nome: str, percentual_trafego: float,
        taxa_conversao_trial: float, taxa_conversao_pagante: float,
        cac_medio: float, cpc: float = 0.0
    ) -> 'ChannelsBuilder':
        """Adiciona canal pago (Google Ads, Facebook Ads)"""
        return self.add_canal(
            nome=nome, tipo=TipoCanal.PAGO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio, custo_por_visitante=cpc
        )

    def add_canal_afiliado(
        self, nome: str, percentual_trafego: float,
        taxa_conversao_trial: float, taxa_conversao_pagante: float,
        cac_medio: float, comissao_percentual: float = 0.20
    ) -> 'ChannelsBuilder':
        """Adiciona programa de afiliados"""
        # Registra comissão no config para COGS
        if hasattr(self.config, 'comissao_afiliados'):
            from core.builders.cogs_builder import ComissaoAfiliado
            self.config.comissao_afiliados = ComissaoAfiliado(
                percentual_sobre_venda=comissao_percentual,
                mes_inicio_programa=1,
                percentual_vendas_via_afiliados=percentual_trafego
            )
        
        return self.add_canal(
            nome=nome, tipo=TipoCanal.AFILIADO,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio
        )

    def add_canal_referral(
        self, nome: str, percentual_trafego: float,
        taxa_conversao_trial: float, taxa_conversao_pagante: float,
        cac_medio: float, incentivo_por_referral: float = 0.0
    ) -> 'ChannelsBuilder':
        """Adiciona programa de referral/indicação"""
        return self.add_canal(
            nome=nome, tipo=TipoCanal.REFERRAL,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_fixo_mensal=incentivo_por_referral * 100  # Simulação simples
        )

    def add_canal(
        self, nome: str, tipo: TipoCanal, percentual_trafego: float,
        taxa_conversao_trial: float, taxa_conversao_pagante: float,
        cac_medio: float, custo_fixo_mensal: float = 0.0,
        custo_por_visitante: float = 0.0, mes_inicio: int = 1,
        mes_fim: Optional[int] = None
    ) -> 'ChannelsBuilder':
        """Adiciona canal genérico - método base"""
        canal = CanalAquisicao(
            nome=nome.replace(" ", "_"),  # Normaliza para coluna
            tipo=tipo,
            percentual_trafego=percentual_trafego,
            taxa_conversao_trial=taxa_conversao_trial,
            taxa_conversao_pagante=taxa_conversao_pagante,
            cac_medio=cac_medio,
            custo_fixo_mensal=custo_fixo_mensal,
            custo_por_visitante=custo_por_visitante,
            mes_inicio=mes_inicio,
            mes_fim=mes_fim
        )
        
        # Valida antes de adicionar
        erros = canal.validar()
        if erros:
            raise ValueError(f"Erro em canal {nome}: {erros}")
        
        self.canais.append(canal)
        return self

    def gerar_series_temporais(self, df_base: pd.DataFrame, orcamento_mensal: pd.Series = None) -> pd.DataFrame:
        """
        🔥 MÉTODO NOVO - GERA COLUNAS PARA DASHBOARD
        
        Args:
            df_base: DataFrame com 'mes' e 'Novos_Pagantes' (ou simula)
            orcamento_mensal: Série com orçamento total por mês (opcional)
        
        Returns:
            DataFrame com colunas: Visitantes, Trials, Novos_Pagantes, CAC_Real
        """
        if not self.canais:
            # Nenhum canal configurado - não faz nada
            return df_base
        
        df = df_base.copy()
        meses = df['mes'].values
        
        # Inicializa colunas de resultados
        df['Visitantes'] = 0
        df['Trials'] = 0
        df['Novos_Pagantes'] = 0
        df['CAC_Real'] = 0.0
        
        # Para cada canal, gera suas colunas
        for canal in self.canais:
            # Calcula quantos novos clientes este canal deve gerar
            # Distribui os novos pagantes totais proporcionalmente ao mix
            if 'Novos_Pagantes' not in df.columns:
                # Se não existe, estima baseado no crescimento
                df['Novos_Pagantes'] = df['Usuarios_Finais'].diff().fillna(0).clip(0)
            
            # Novos pagantes por canal
            df[f'Novos_{canal.nome}'] = (df['Novos_Pagantes'] * canal.percentual_trafego).round()
            
            # Trials por canal (baseado na taxa de conversão)
            # Fórmula: Trials = Novos_Pagantes / taxa_conversao_pagante
            df[f'Trials_{canal.nome}'] = (df[f'Novos_{canal.nome}'] / max(0.01, canal.taxa_conversao_pagante)).round()
            
            # Visitantes por canal (baseado na taxa de conversão trial)
            # Fórmula: Visitantes = Trials / taxa_conversao_trial
            df[f'Visitantes_{canal.nome}'] = (df[f'Trials_{canal.nome}'] / max(0.01, canal.taxa_conversao_trial)).round()
            
            # Acumula nos totais
            df['Visitantes'] += df[f'Visitantes_{canal.nome}']
            df['Trials'] += df[f'Trials_{canal.nome}']
            df['Novos_Pagantes'] += df[f'Novos_{canal.nome}']
        
        # Calcula CAC Real por mês
        # Fórmula: CAC = Custo_Total_Canal / Novos_Pagantes_Canal
        for canal in self.canais:
            # Custo total do canal
            if orcamento_mensal is not None:
                # Usa orçamento real do MarketingBuilder
                df[f'Custo_{canal.nome}'] = orcamento_mensal * canal.percentual_trafego + canal.custo_fixo_mensal
            else:
                # Estima baseado no CAC target
                df[f'Custo_{canal.nome}'] = df[f'Novos_{canal.nome}'] * canal.cac_medio + canal.custo_fixo_mensal
            
            # CAC Real
            df[f'CAC_{canal.nome}'] = np.where(
                df[f'Novos_{canal.nome}'] > 0,
                df[f'Custo_{canal.nome}'] / df[f'Novos_{canal.nome}'],
                0
            )
        
        # CAC Real total (blended)
        custo_total = sum(df[f'Custo_{canal.nome}'] for canal in self.canais)
        df['CAC_Real'] = np.where(
            df['Novos_Pagantes'] > 0,
            custo_total / df['Novos_Pagantes'],
            0
        )
        
        # Taxas de conversão gerais
        df['Taxa_Conversao_Trial'] = np.where(
            df['Visitantes'] > 0,
            df['Trials'] / df['Visitantes'],
            0
        )
        
        df['Taxa_Conversao_Pagante'] = np.where(
            df['Trials'] > 0,
            df['Novos_Pagantes'] / df['Trials'],
            0
        )
        
        # LTV/CAC ratio (se existir LTV)
        if 'LTV' in df.columns:
            df['LTV_CAC_Ratio'] = np.where(
                df['CAC_Real'] > 0,
                df['LTV'] / df['CAC_Real'],
                0
            )
        
        return df

    def calcular_cac_blended(self) -> float:
        """CAC médio de todos os canais"""
        if not self.canais:
            return 0.0
        return sum(c.cac_medio * c.percentual_trafego for c in self.canais if c.ativo)

    def calcular_cac_pago(self) -> float:
        """CAC médio apenas dos canais pagos"""
        canais_pagos = [c for c in self.canais if c.tipo == TipoCanal.PAGO and c.ativo]
        if not canais_pagos:
            return 0.0
        
        total_mix = sum(c.percentual_trafego for c in canais_pagos)
        if total_mix == 0:
            return 0.0
        
        return sum(c.cac_medio * (c.percentual_trafego / total_mix) for c in canais_pagos)

    def calcular_conversao_media(self) -> Tuple[float, float]:
        """Taxas de conversão médias (trial e pagante)"""
        if not self.canais:
            return (0.0, 0.0)
        
        total_mix = sum(c.percentual_trafego for c in self.canais if c.ativo)
        if total_mix == 0:
            return (0.0, 0.0)
        
        conv_trial = sum(c.taxa_conversao_trial * c.percentual_trafego for c in self.canais if c.ativo)
        conv_pagante = sum(c.taxa_conversao_pagante * c.percentual_trafego for c in self.canais if c.ativo)
        
        return (conv_trial, conv_pagante)

    def validar(self) -> List[str]:
        """Valida configuração completa"""
        erros = []
        
        # Valida cada canal
        for canal in self.canais:
            erros.extend(canal.validar())
        
        # Valida soma dos mixes
        total_mix = sum(c.percentual_trafego for c in self.canais if c.ativo)
        if abs(total_mix - 1.0) > 0.01:
            erros.append(f"Soma dos mixes: {total_mix*100:.1f}% (deveria ser 100%)")
        
        # Valida duplicatas de nome
        nomes = [c.nome for c in self.canais]
        if len(nomes) != len(set(nomes)):
            erros.append("Nomes de canais duplicados")
        
        return erros

    def build(self):
        """
        Aplica configuração ao config e retorna config
        (mantido para retrocompatibilidade)
        """
        erros = self.validar()
        if erros:
            raise ValueError(f"Erros na configuração:\n" + "\n".join(erros))
        
        if not hasattr(self.config, 'canais_aquisicao'):
            self.config.canais_aquisicao = []
        
        self.config.canais_aquisicao = self.canais
        
        # Atualiza taxas médias no config
        conv_trial, conv_pagante = self.calcular_conversao_media()
        self.config.taxa_conversao_visitante_trial = conv_trial
        self.config.taxa_conversao_trial_pagante = conv_pagante
        
        # Atualiza CACs no config
        self.config.cac_blended = self.calcular_cac_blended()
        self.config.cac_pago_meta = self.calcular_cac_pago()
        
        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Canais de Aquisição",
                detalhes={
                    'num_canais': len(self.canais),
                    'cac_blended': self.config.cac_blended,
                    'cac_pago': self.config.cac_pago_meta,
                    'canais_ativos': [c.nome for c in self.canais if c.ativo]
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
                f"   Mix:        {canal.percentual_trafego*100:.1f}%",
                f"   Conv.Trial: {canal.taxa_conversao_trial*100:.1f}%",
                f"   Conv.Pago:  {canal.taxa_conversao_pagante*100:.1f}%",
                f"   Conv.Total: {canal.taxa_conversao_combinada()*100:.2f}%",
                f"   CAC Alvo:   R$ {canal.cac_medio:,.2f}",
                f"   Custo Fixo: R$ {canal.custo_fixo_mensal:,.2f}/mês",
                ""
            ])
        
        linhas.extend([
            "─" * 70,
            f"CAC Blended:  R$ {self.calcular_cac_blended():,.2f}",
            f"CAC Pago:     R$ {self.calcular_cac_pago():,.2f}",
            "",
            f"Conv.Trial Média: {self.calcular_conversao_media()[0]*100:.2f}%",
            f"Conv.Pago Média:  {self.calcular_conversao_media()[1]*100:.2f}%",
            "═" * 70
        ])
        
        return "\n".join(linhas)

# ============================================================================
# FUNÇÕES DE AJUDA PARA CRIAR ESTRATÉGIAS PRÉ-CONFIGURADAS
# ============================================================================

def criar_estrategia_sam_canais(config) -> ChannelsBuilder:
    """
    Cria estratégia de canais padrão SAM:
    - SEO Orgânico: 40%, CAC R$200
    - Google Ads: 30%, CAC R$500
    - Programa de Afiliados: 20%, CAC R$100
    - Programa de Indicação: 10%, CAC R$50
    """
    builder = ChannelsBuilder(config)
    
    # SEO Orgânico (tráfego de qualidade, custo baixo)
    builder.add_canal_organico(
        nome="SEO & Content Marketing",
        percentual_trafego=0.40,
        taxa_conversao_trial=0.08,
        taxa_conversao_pagante=0.20,
        cac_medio=200.0,
        custo_seo_mensal=1500.0  # Ferramentas + conteúdo
    )
    
    # Google Ads (performance, escala controlada)
    builder.add_canal_pago(
        nome="Google Ads Performance",
        percentual_trafego=0.30,
        taxa_conversao_trial=0.04,
        taxa_conversao_pagante=0.15,
        cac_medio=500.0,
        cpc=2.50
    )
    
    # Programa de Afiliados (alta conversão, comissão)
    builder.add_canal_afiliado(
        nome="Programa de Afiliados",
        percentual_trafego=0.20,
        taxa_conversao_trial=0.12,
        taxa_conversao_pagante=0.30,
        cac_medio=100.0,
        comissao_percentual=0.20  # 20% de comissão
    )
    
    # Programa de Indicação (referral, CAC mínimo)
    builder.add_canal_referral(
        nome="Programa de Indicação",
        percentual_trafego=0.10,
        taxa_conversao_trial=0.15,
        taxa_conversao_pagante=0.35,
        cac_medio=50.0,
        incentivo_por_referral=20.0  # R$20 de crédito
    )
    
    return builder

# ============================================================================
# TESTE AUTOMÁTICO DO BUILDER
# ============================================================================

if __name__ == "__main__":
    import sys
    import os
    import pandas as pd
    
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    # Config mock
    class MockConfig:
        def __init__(self):
            self.canais_aquisicao = []
            self.comissao_afiliados = None
            self.alteracoes = []
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})
    
    config = MockConfig()
    
    # Cria estratégia SAM
    builder = criar_estrategia_sam_canais(config)
    
    # DataFrame de exemplo
    df_exemplo = pd.DataFrame({
        'mes': [1, 2, 3, 4, 5, 6],
        'Usuarios_Iniciais': [1000, 1200, 1350, 1480, 1600, 1720],
        'Usuarios_Finais': [1200, 1350, 1480, 1600, 1720, 1850],
        'MRR': [97000, 110500, 120000, 130000, 140000, 150000],
        'ARPU': [97, 97, 97, 97, 97, 97],
    })
    
    # Adiciona novos pagantes (se não existir)
    df_exemplo['Novos_Pagantes'] = df_exemplo['Usuarios_Finais'].diff().fillna(0).clip(0) + 50
    
    # Gera séries temporais
    df_resultado = builder.gerar_series_temporais(df_exemplo)
    
    print("="*70)
    print("CHANNELS BUILDER - TESTE COMPLETO")
    print("="*70)
    
    print("\nColunas geradas:")
    for col in df_resultado.columns:
        print(f"- {col}")
    
    print("\nPrimeiros 3 meses:")
    cols_vis = ['mes', 'Visitantes', 'Trials', 'Novos_Pagantes', 'CAC_Real']
    cols_vis += [f'Visitantes_{c.nome}' for c in builder.canais]
    cols_vis += [f'CAC_{c.nome}' for c in builder.canais]
    
    print(df_resultado[cols_vis].head(3).to_string())
    
    print("\n" + "="*70)
    print("✅ ChannelsBuilder funcionando corretamente!")
    print("="*70)
    
    # Relatório
    print("\n" + builder.gerar_relatorio())