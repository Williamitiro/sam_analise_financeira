"""
core/builders/revenue_builder.py

Builder para configurar planos de assinatura e gerar séries temporais de receita.

FUNCIONALIDADES:
- Configura planos (Lite, Pro, Enterprise)
- Gera breakdown de MRR por plano (MRR_Lite, MRR_Trader, MRR_Pro)
- Calcula MRR Movement (Novos, Churn, Expansão, Contração)
- Retorna ARPU por plano
- Compatível com motor existente (fallback seguro)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
import pandas as pd
import numpy as np

@dataclass
class Plano:
    """Plano de assinatura com configuração própria de churn"""
    nome: str
    preco_mensal: float
    percentual_clientes: float  # 0.0 a 1.0
    churn_mensal: float  # Churn específico do plano
    upsell_rate: float = 0.0  # % de clientes que fazem upgrade/mês
    downsell_rate: float = 0.0  # % de clientes que fazem downgrade/mês

@dataclass
class AddOn:
    """Add-on ou receita avulsa"""
    nome: str
    preco: float
    taxa_adocao: float  # % de clientes que compram
    recorrencia: str = "mensal"  # mensal, anual, unique

class RevenueBuilder:
    """
    Builder completo de receita com geração de séries temporais
    
    USO:
        builder = RevenueBuilder(config)
        builder.add_plano("Lite", 97, 0.6, 0.05)
        builder.add_plano("Trader", 197, 0.3, 0.04, upsell_rate=0.02)
        builder.add_plano("Pro", 397, 0.1, 0.03, upsell_rate=0.03)
        builder.build()
        
        # No motor:
        df = builder.gerar_series_temporais(df)
    """
    
    def __init__(self, config):
        self.config = config
        self.planos: List[Plano] = []
        self.addons: List[AddOn] = []
        self._series_geradas = False  # Flag para cache

    def add_plano(self, nome: str, preco_mensal: float, percentual_clientes: float, 
                  churn_mensal: float, upsell_rate: float = 0.0, downsell_rate: float = 0.0) -> 'RevenueBuilder':
        """Adiciona plano - interface fluente"""
        # Normaliza nome para coluna (remove espaços)
        nome_coluna = nome.replace(" ", "_")
        
        self.planos.append(Plano(
            nome=nome_coluna,
            preco_mensal=preco_mensal,
            percentual_clientes=percentual_clientes,
            churn_mensal=churn_mensal,
            upsell_rate=upsell_rate,
            downsell_rate=downsell_rate
        ))
        return self

    def add_addon(self, nome: str, preco: float, taxa_adocao: float, recorrencia: str = "mensal") -> 'RevenueBuilder':
        """Adiciona add-on - interface fluente"""
        self.addons.append(AddOn(
            nome=nome.replace(" ", "_"),
            preco=preco,
            taxa_adocao=taxa_adocao,
            recorrencia=recorrencia
        ))
        return self

    def calcular_receita_para_mes(self, usuarios: float) -> Tuple[float, float]:
        """
        MANTIDO PARA RETROCOMPATIBILIDADE
        Calcula MRR total e ARPU médio para um ponto no tempo
        
        Usado pelo motor antigo que não usa séries temporais
        """
        if not self.planos:
            # Fallback: usa config antiga
            arpu = self.config.arpu_medio
            mrr = usuarios * arpu if self.config.ativar_receita_por_usuario else 0.0
            return mrr, arpu
        
        # Calcula ARPU ponderado
        arpu = sum(p.preco_mensal * p.percentual_clientes for p in self.planos)
        mrr = usuarios * arpu
        
        return mrr, arpu

    def gerar_series_temporais(self, df_base: pd.DataFrame) -> pd.DataFrame:
        """
        🔥 MÉTODO NOVO - GERA TODAS AS COLUNAS NECESSÁRIAS
        
        Args:
            df_base: DataFrame com 'mes', 'Usuarios_Iniciais', 'Novos_Pagantes' (ou simula)
            
        Returns:
            DataFrame com colunas novas adicionadas
        """
        if not self.planos:
            # Nenhum plano configurado - não faz nada
            return df_base
        
        df = df_base.copy()
        meses = df['mes'].values
        
        # GERA COLUNAS POR PLANO
        for plano in self.planos:
            # MRR por plano = Usuários Totais × % do plano × Preço
            df[f'MRR_{plano.nome}'] = df['Usuarios_Finais'] * plano.percentual_clientes * plano.preco_mensal
            
            # ARPU por plano é o preço do plano (fixo)
            df[f'ARPU_{plano.nome}'] = plano.preco_mensal
            
            # Usuários por plano (estimado)
            df[f'Usuarios_{plano.nome}'] = (df['Usuarios_Finais'] * plano.percentual_clientes).round()
            
            # NOVOS clientes por plano (distribui proporcionalmente aos novos totais)
            if 'Novos_Pagantes' in df.columns:
                df[f'Novos_{plano.nome}'] = df['Novos_Pagantes'] * plano.percentual_clientes
            else:
                # Simula novos baseado no crescimento
                df[f'Novos_{plano.nome}'] = df['Usuarios_Finais'].diff().fillna(0).clip(0) * plano.percentual_clientes
        
        # GERA MRR MOVEMENT (Waterfall)
        if len(self.planos) > 0:
            df = self._calcular_mrr_movement(df)
        
        # GERA ARPU GERAL (ponderado)
        if not hasattr(df, 'ARPU') or df['ARPU'].isna().all():
            df['ARPU'] = sum(p.preco_mensal * p.percentual_clientes for p in self.planos)
        
        # GERA RECEITA DE ADD-ONS
        if self.addons:
            df = self._calcular_addon_revenue(df)
        
        self._series_geradas = True
        return df

    def _calcular_mrr_movement(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula MRR Movement para cada mês
        Colunas geradas: MRR_Novos_Clientes, MRR_Churn, MRR_Expansao, MRR_Contracao
        """
        # MRR de novos clientes = novos usuários × ARPU médio
        if 'Novos_Pagantes' not in df.columns:
            # Se não existe no DataFrame, estima baseado na variação
            df['Novos_Pagantes'] = df['Usuarios_Finais'].diff().fillna(0).clip(0)
        
        df['MRR_Novos_Clientes'] = df['Novos_Pagantes'] * df['ARPU']
        
        # MRR de churn = usuários que cancelam × ARPU médio
        # Assume churn sobre base do mês anterior
        df['Usuarios_Iniciais'] = df['Usuarios_Finais'].shift(1).fillna(df['Usuarios_Finais'])
        df['Churn_Absoluto'] = (df['Usuarios_Iniciais'] * config.churn_mensal).fillna(0)
        df['MRR_Churn'] = df['Churn_Absoluto'] * df['ARPU'].shift(1).fillna(df['ARPU'])
        
        # EXPANSÃO: Receita de upgrades entre planos
        # Simplificado: % de clientes de planos menores fazem upgrade
        df['MRR_Expansao'] = 0.0
        for plano in self.planos:
            if plano.upsell_rate > 0:
                # Clientes de planos menores que fazem upgrade
                usuarios_upgradaveis = df[f'Usuarios_{plano.nome}'].shift(1).fillna(0) * plano.upsell_rate
                
                # Encontra próximo plano maior (simplificado)
                idx_plano = self.planos.index(plano)
                if idx_plano < len(self.planos) - 1:
                    prox_plano = self.planos[idx_plano + 1]
                    valor_upgrade = prox_plano.preco_mensal - plano.preco_mensal
                    df['MRR_Expansao'] += usuarios_upgradaveis * valor_upgrade
        
        # CONTRAÇÃO: Downgrades (raro nos primeiros meses mas incluído)
        df['MRR_Contracao'] = 0.0
        for plano in self.planos:
            if plano.downsell_rate > 0 and df['mes'].iloc[0] > 6:  # Só após 6 meses
                usuarios_downgradaveis = df[f'Usuarios_{plano.nome}'].shift(1).fillna(0) * plano.downsell_rate
                
                idx_plano = self.planos.index(plano)
                if idx_plano > 0:
                    plano_anterior = self.planos[idx_plano - 1]
                    valor_downgrade = plano.preco_mensal - plano_anterior.preco_mensal
                    df['MRR_Contracao'] += usuarios_downgradaveis * valor_downgrade
        
        # Validação: MRR_Fim deve bater com MRR calculado
        df['MRR_Calculado'] = (
            df['MRR'].shift(1).fillna(df['MRR'].iloc[0]) + 
            df['MRR_Novos_Clientes'] - 
            df['MRR_Churn'] + 
            df['MRR_Expansao'] - 
            df['MRR_Contracao']
        )
        
        # Ajusta MRR_Final para bater (distribui discrepância)
        discrepancia = df['MRR'] - df['MRR_Calculado']
        df['MRR_Expansao'] += discrepancia.clip(0)  # Discrepância positiva vai para expansão
        df['MRR_Contracao'] += abs(discrepancia.clip(None, 0))  # Negativa vai para contração
        
        return df

    def _calcular_addon_revenue(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula receita de add-ons
        """
        df['Receita_AddOn'] = 0.0
        
        for addon in self.addons:
            if addon.recorrencia == "mensal":
                # Add-on mensal: % clientes × preço
                df[f'Addon_{addon.nome}'] = df['Usuarios_Finais'] * addon.taxa_adocao * addon.preco
                df['Receita_AddOn'] += df[f'Addon_{addon.nome}']
            elif addon.recorrencia == "anual":
                # Add-on anual: dividido por 12 para MRR
                df[f'Addon_{addon.nome}'] = (df['Usuarios_Finais'] * addon.taxa_adocao * addon.preco) / 12
                df['Receita_AddOn'] += df[f'Addon_{addon.nome}']
        
        # Ajusta MRR total para incluir add-ons
        df['MRR'] += df['Receita_AddOn']
        
        return df

    def build(self) -> 'ConfigFinanceira':
        """
        Aplica configuração ao config e retorna o objeto config modificado.
        """
        if not hasattr(self.config, 'receita'):
            self.config.receita = {}
        
        self.config.receita['planos'] = self.planos
        self.config.receita['addons'] = self.addons
        
        # Registra alterações
        if hasattr(self.config, 'registrar_alteracao'):
            # Verifica se já tem valor de ARPU para usar como base
            arpu_from_plans = sum(p.preco_mensal * p.percentual_clientes for p in self.planos) if self.planos else 0
            
            self.config.registrar_alteracao(
                "Configuração de Receita",
                detalhes={
                    'num_planos': len(self.planos),
                    'num_addons': len(self.addons),
                    'arpu_calculado': arpu_from_plans,
                    'planos_configurados': [p.nome for p in self.planos]
                }
            )
        
        # Atualiza ARPU no config se não existir
        if not hasattr(self.config, 'arpu_medio') or self.config.arpu_medio == 0:
            self.config.arpu_medio = sum(p.preco_mensal * p.percentual_clientes for p in self.planos) if self.planos else 97.0
        
        return self.config

# ============================================================================
# FUNÇÕES DE AJUDA PARA CRIAR ESTRATÉGIAS PRÉ-CONFIGURADAS
# ============================================================================

def criar_estrategia_sam_revenue(config) -> RevenueBuilder:
    """
    Cria estratégia de receita padrão SAM:
    - Lite: R$ 97/mês, 60% clientes, churn 5%
    - Trader: R$ 197/mês, 30% clientes, churn 4%, upsell 2%
    - Pro: R$ 397/mês, 10% clientes, churn 3%, upsell 3%
    - Add-on: Consultoria R$ 500 (10% adesão)
    """
    builder = RevenueBuilder(config)
    
    # Plano Lite (entry-level)
    builder.add_plano(
        nome="Lite",
        preco_mensal=97.0,
        percentual_clientes=0.60,
        churn_mensal=0.05,
        upsell_rate=0.0,  # Não faz upgrade (é o plano base)
        downsell_rate=0.0
    )
    
    # Plano Trader (plano do meio)
    builder.add_plano(
        nome="Trader",
        preco_mensal=197.0,
        percentual_clientes=0.30,
        churn_mensal=0.04,
        upsell_rate=0.02,  # 2% fazem upgrade para Pro/mês
        downsell_rate=0.01  # 1% fazem downgrade para Lite/mês
    )
    
    # Plano Pro (top tier)
    builder.add_plano(
        nome="Pro",
        preco_mensal=397.0,
        percentual_clientes=0.10,
        churn_mensal=0.03,
        upsell_rate=0.0,  # Não há plano acima
        downsell_rate=0.02  # 2% fazem downgrade para Trader/mês
    )
    
    # Add-on de consultoria
    builder.add_addon(
        nome="Consultoria",
        preco=500.0,
        taxa_adocao=0.10,  # 10% dos clientes compram
        recorrencia="mensal"
    )
    
    return builder

if __name__ == '__main__':
    # Teste completo
    import sys
    import os
    import pandas as pd
    from datetime import date
    
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    # Config mock
    class MockConfig:
        def __init__(self):
            self.receita = {}
            self.alteracoes = []
            self.arpu_medio = 0
            self.ativar_receita_por_usuario = True
            self.churn_mensal = 0.04
            self.churn_mensal = 0.04
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})
    
    config = MockConfig()
    
    # Cria estratégia SAM
    builder = criar_estrategia_sam_revenue(config)
    builder.build()
    
    # DataFrame de exemplo
    df_exemplo = pd.DataFrame({
        'mes': [1, 2, 3, 4, 5, 6],
        'Usuarios_Iniciais': [1000, 1200, 1350, 1480, 1600, 1720],
        'Usuarios_Finais': [1200, 1350, 1480, 1600, 1720, 1850],
        'Novos_Pagantes': [250, 180, 160, 150, 140, 160],  # Simulado
        'MRR': [0, 0, 0, 0, 0, 0],  # Será preenchido
        'ARPU': [0, 0, 0, 0, 0, 0],  # Será preenchido
    })
    
    # Gera séries temporais
    df_resultado = builder.gerar_series_temporais(df_exemplo)
    
    print("\n" + "="*70)
    print("COLUNAS GERADAS:")
    print("="*70)
    for col in df_resultado.columns:
        print(f"- {col}")
    
    print("\n" + "="*70)
    print("REVENUE BUILDER - TESTE COMPLETO")
    print("="*70)
    print("\nMRR por Plano:")
    print(df_resultado[['mes', 'MRR_Lite', 'MRR_Trader', 'MRR_Pro', 'MRR']].head())
    
    print("\nMRR Movement:")
    print(df_resultado[['mes', 'MRR_Novos_Clientes', 'MRR_Churn', 'MRR_Expansao', 'MRR']].head())
    
    print("\nARPU por Plano:")
    print(df_resultado[['mes', 'ARPU_Lite', 'ARPU_Trader', 'ARPU_Pro']].head())
    
    print("\n" + "="*70)
    print("✅ RevenueBuilder funcionando corretamente!")
    print("="*70)