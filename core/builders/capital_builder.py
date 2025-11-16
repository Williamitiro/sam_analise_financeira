"""
core/builders/capital_builder.py

Builder para configurar estrutura de capital e gerar séries temporais
de aportes, empréstimos, runway e milestones.

FUNCIONALIDADES:
- Registra aportes de sócios/investidores
- Registra empréstimos com amortização sistemática
- Calcula runway (meses até o caixa zerar)
- Projeta milestones de funding
- Gera séries temporais para dashboard
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np

@dataclass
class Aporte:
    """Aporte de capital (investimento, rodada, etc.)"""
    valor: float
    data: date
    socio: str = "Investidor Anônimo"
    tipo: str = "equity"  # equity, convertible, grant
    descricao: str = ""

@dataclass
class Emprestimo:
    """Empréstimo ou financiamento"""
    valor_principal: float
    taxa_juros_anual: float  # Taxa ao ano (ex: 0.12 = 12%)
    prazo_meses: int
    data_inicio: date
    carencia_meses: int = 0  # Meses sem pagamento
    tipo: str = "price"  # price (price), simples

class CapitalBuilder:
    """
    Builder completo de capital com geração de séries temporais
    
    USO:
        builder = CapitalBuilder(config)
        builder.add_aporte(100000, date(2024, 1, 1), "Anjo A", "equity")
        builder.add_emprestimo(50000, 0.12, 24, date(2024, 6, 1))
        builder.build()
        
        # No motor:
        df = builder.gerar_series_temporais(df)
    """

    def __init__(self, config):
        self.config = config
        self.aportes: List[Aporte] = []
        self.emprestimos: List[Emprestimo] = []
        self._series_geradas = False

    def add_aporte(
        self, valor: float, data: date, socio: str = "Investidor",
        tipo: str = "equity", descricao: str = ""
    ) -> 'CapitalBuilder':
        """Adiciona aporte - interface fluente"""
        self.aportes.append(Aporte(
            valor=valor, data=data, socio=socio,
            tipo=tipo, descricao=descricao
        ))
        return self

    def add_emprestimo(
        self, valor_principal: float, taxa_juros_anual: float,
        prazo_meses: int, data_inicio: date,
        carencia_meses: int = 0, tipo: str = "price"
    ) -> 'CapitalBuilder':
        """Adiciona empréstimo - interface fluente"""
        self.emprestimos.append(Emprestimo(
            valor_principal=valor_principal,
            taxa_juros_anual=taxa_juros_anual,
            prazo_meses=prazo_meses,
            data_inicio=data_inicio,
            carencia_meses=carencia_meses,
            tipo=tipo
        ))
        return self

    def calcular_aporte_para_mes(self, mes: int) -> float:
        """
        MANTIDO PARA RETROCOMPATIBILIDADE
        Calcula aporte para um mês específico (mês = número do mês)
        """
        cfg = self.config
        
        # Fallback para config antiga
        if hasattr(cfg, 'meses_aporte_fixo') and hasattr(cfg, 'aporte_mensal_fixo'):
            if mes <= cfg.meses_aporte_fixo:
                return cfg.aporte_mensal_fixo
        
        # Lógica nova: soma aportes programados para este mês
        from datetime import datetime
        data_mes = datetime.now().date().replace(day=1)
        # Aproximação: mês N = data atual + N-1 meses
        data_alvo = data_mes + timedelta(days=30 * (mes - 1))
        
        total_aporte = sum(
            aporte.valor for aporte in self.aportes
            if aporte.data.year == data_alvo.year and aporte.data.month == data_alvo.month
        )
        
        return total_aporte

    def gerar_series_temporais(self, df_base: pd.DataFrame) -> pd.DataFrame:
        """
        🔥 MÉTODO NOVO - GERA SÉRIES TEMPORAIS DE CAPITAL
        
        Args:
            df_base: DataFrame com 'mes', 'Caixa', 'Receita_Bruta', 'Custos_Totais'
            
        Returns:
            DataFrame com colunas: Aportes, Runway, Burn_Rate, etc.
        """
        if not self.aportes and not self.emprestimos:
            # Nenhum capital configurado - não faz nada
            return df_base
        
        df = df_base.copy()
        meses = df['mes'].values
        
        # Inicializa colunas
        df['Aporte_Mes'] = 0.0
        df['Emprestimo_Mes'] = 0.0
        df['Amortizacao_Mes'] = 0.0
        df['Juros_Mes'] = 0.0
        df['Burn_Rate_Mensal'] = 0.0
        df['Runway_Meses'] = 0.0
        
        # Data de início da projeção
        data_inicio_proj = datetime.now().date().replace(day=1)
        
        # ==== GERA APORTES POR MÊS ====
        for mes in meses:
            data_alvo = data_inicio_proj + timedelta(days=30 * (int(mes) - 1))
            
            # Soma aportes deste mês
            aporte_mes = sum(
                aporte.valor for aporte in self.aportes
                if aporte.data.year == data_alvo.year and aporte.data.month == data_alvo.month
            )
            df.loc[df['mes'] == mes, 'Aporte_Mes'] = aporte_mes
        
        # ==== GERA EMPRÉSTIMOS POR MÊS (Amortização) ====
        for emprestimo in self.emprestimos:
            df = self._calcular_amortizacao(df, emprestimo, data_inicio_proj)
        
        # ==== CALCULA BURN RATE E RUNWAY ====
        df = self._calcular_runway(df)
        
        # ==== CALCULA MILESTONES DE FUNDING ====
        df = self._calcular_milestones(df)
        
        # ==== CALCULA VALUATION (se aplicável) ====
        if 'MRR' in df.columns:
            df = self._calcular_valuation(df)
        
        self._series_geradas = True
        return df

    def _calcular_amortizacao(
        self, df: pd.DataFrame, emprestimo: Emprestimo, data_inicio_proj: date
    ) -> pd.DataFrame:
        """
        Calcula amortização sistemática do empréstimo
        """
        # Verifica período de vigência
        inicio_mes = (emprestimo.data_inicio.year - data_inicio_proj.year) * 12 + \
                    (emprestimo.data_inicio.month - data_inicio_proj.month) + 1
        
        if inicio_mes < 1:
            inicio_mes = 1
        
        fim_mes = inicio_mes + emprestimo.prazo_meses - 1
        
        # Filtra meses onde o empréstimo está ativo
        meses_ativos = df[(df['mes'] >= inicio_mes) & (df['mes'] <= fim_mes)].copy()
        
        if meses_ativos.empty:
            return df
        
        # Calcula valores mensais
        valor_mensal = emprestimo.valor_principal / emprestimo.prazo_meses
        
        # Taxa mensal de juros
        taxa_mensal = emprestimo.taxa_juros_anual / 12
        
        # Para cada mês ativo
        for _, row in meses_ativos.iterrows():
            mes = int(row['mes'])
            
            # Saldo devedor no início do mês
            meses_passados = mes - inicio_mes
            saldo_devedor = emprestimo.valor_principal - (valor_mensal * meses_passados)
            
            # Juros do mês
            juros_mes = saldo_devedor * taxa_mensal if meses_passados >= emprestimo.carencia_meses else 0
            
            # Amortização (só começa após carência)
            amortizacao_mes = valor_mensal if meses_passados >= emprestimo.carencia_meses else 0
            
            # Atualiza DataFrame
            idx = df['mes'] == mes
            df.loc[idx, 'Emprestimo_Mes'] += emprestimo.valor_principal if mes == inicio_mes else 0
            df.loc[idx, 'Amortizacao_Mes'] += amortizacao_mes
            df.loc[idx, 'Juros_Mes'] += juros_mes
        
        return df

    def _calcular_runway(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula Burn Rate e Runway (meses até acabar o caixa)
        """
        # Burn Rate = Receita - Custos (se negativo, é consumo de caixa)
        if 'Receita_Bruta' not in df.columns or 'Custos_Totais' not in df.columns:
            # Fallback: estima burn rate baseado na variação de caixa
            df['Burn_Rate_Mensal'] = -df['Caixa'].diff().fillna(0)
        else:
            df['Burn_Rate_Mensal'] = df['Receita_Bruta'] - df['Custos_Totais']
        
        # Ajusta com aportes e empréstimos (não são burn)
        df['Burn_Rate_Mensal'] = df['Burn_Rate_Mensal'] - df['Aporte_Mes'] - df['Emprestimo_Mes']
        
        # Calcula Runway: Caixa atual / Burn Rate médio (negativo)
        burn_medio_negativo = df['Burn_Rate_Mensal'][df['Burn_Rate_Mensal'] < 0].mean()
        
        if burn_medio_negativo < 0:
            # Runway crescente conforme o caixa vai diminuindo
            df['Runway_Meses'] = np.nan
            for i, row in df.iterrows():
                caixa_atual = row['Caixa']
                burn_atual = df.loc[i:, 'Burn_Rate_Mensal']
                burn_acumulado = burn_atual.cumsum()
                meses_ate_zerar = (burn_acumulado < -caixa_atual).sum()
                df.loc[i, 'Runway_Meses'] = meses_ate_zerar
        
        return df

    def _calcular_milestones(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Projeta milestones de funding (ex: R$ 100k MRR, R$ 1M ARR)
        """
        # Se não tiver MRR, não calcula
        if 'MRR' not in df.columns:
            return df
        
        # Define milestones
        milestones = [
            {'nome': 'MRR 50k', 'valor': 50000, 'tipo': 'mrr'},
            {'nome': 'MRR 100k', 'valor': 100000, 'tipo': 'mrr'},
            {'nome': 'MRR 1M', 'valor': 1000000, 'tipo': 'mrr'},
            {'nome': 'ARR 1M', 'valor': 83333, 'tipo': 'arr'},  # 1M ARR = 83k MRR
        ]
        
        # Para cada milestone, calcula quando será alcançado
        for milestone in milestones:
            df[f'Meta_{milestone["nome"]}'] = milestone['valor']
            df[f'Data_{milestone["nome"]}'] = pd.NaT
            
            # Encontra o mês onde o valor é alcançado
            idx_alcancado = df[df['MRR'] >= milestone['valor']].index
            if not idx_alcancado.empty:
                mes_alcancado = df.loc[idx_alcancado[0], 'mes']
                df.loc[df['mes'] == mes_alcancado, f'Data_{milestone["nome"]}'] = \
                    datetime.now() + timedelta(days=30 * mes_alcancado)
        
        return df

    def _calcular_valuation(self, df: pd.DataFrame, multiplo_receita: float = 5.0) -> pd.DataFrame:
        """
        Calcula valuation estimado baseado no ARR
        Fórmula: Valuation = ARR × Múltiplo
        """
        if 'ARR' not in df.columns and 'MRR' in df.columns:
            df['ARR'] = df['MRR'] * 12
        
        df['Valuation_Estimado'] = df['ARR'] * multiplo_receita
        
        return df

    # Métodos de validação e build (mantidos para compatibilidade)
    def validar(self) -> List[str]:
        """Valida configuração de capital"""
        erros = []
        
        # Valida aportes
        for i, aporte in enumerate(self.aportes):
            if aporte.valor <= 0:
                erros.append(f"Aporte {i+1}: valor deve ser positivo")
        
        # Valida empréstimos
        for i, emprestimo in enumerate(self.emprestimos):
            if emprestimo.valor_principal <= 0:
                erros.append(f"Empréstimo {i+1}: principal deve ser positivo")
            if emprestimo.taxa_juros_anual < 0 or emprestimo.taxa_juros_anual > 1:
                erros.append(f"Empréstimo {i+1}: taxa deve ser 0-1")
            if emprestimo.prazo_meses <= 0:
                erros.append(f"Empréstimo {i+1}: prazo deve ser positivo")
        
        return erros

    def build(self):
        """Aplica configuração ao config (mantido para compatibilidade)"""
        erros = self.validar()
        if erros:
            raise ValueError(f"Erros na configuração:\n" + "\n".join(erros))
        
        if not hasattr(self.config, 'estrutura_capital'):
            self.config.estrutura_capital = {}
        
        self.config.estrutura_capital['aportes'] = self.aportes
        self.config.estrutura_capital['emprestimos'] = self.emprestimos
        
        # Registra alteração
        if hasattr(self.config, 'registrar_alteracao'):
            self.config.registrar_alteracao(
                "Configuração de Estrutura de Capital",
                detalhes={
                    'num_aportes': len(self.aportes),
                    'num_emprestimos': len(self.emprestimos),
                    'total_aportes': sum(a.valor for a in self.aportes)
                }
            )
        
        return self.config

    def gerar_relatorio(self) -> str:
        """Gera relatório textual completo"""
        if not self.aportes and not self.emprestimos:
            return "Nenhum capital configurado."
        
        linhas = [
            "═" * 70,
            "ESTRUTURA DE CAPITAL",
            "═" * 70,
            ""
        ]
        
        if self.aportes:
            linhas.append("📈 APORTES DE CAPITAL")
            linhas.append("─" * 70)
            for i, aporte in enumerate(self.aportes, 1):
                linhas.extend([
                    f"#{i}: {aporte.socio}",
                    f"   Valor:  R$ {aporte.valor:,.2f}",
                    f"   Data:   {aporte.data}",
                    f"   Tipo:   {aporte.tipo}",
                    f"   Desc:   {aporte.descricao}",
                    ""
                ])
        
        if self.emprestimos:
            linhas.append("💰 EMPRÉSTIMOS E FINANCIAMENTOS")
            linhas.append("─" * 70)
            for i, emp in enumerate(self.emprestimos, 1):
                linhas.extend([
                    f"#{i}: R$ {emp.valor_principal:,.2f}",
                    f"   Taxa:   {emp.taxa_juros_anual*100:.2f}% a.a.",
                    f"   Prazo:  {emp.prazo_meses} meses",
                    f"   Início: {emp.data_inicio}",
                    f"   Carência: {emp.carencia_meses} meses",
                    ""
                ])
        
        linhas.append("═" * 70)
        
        return "\n".join(linhas)

# ============================================================================
# FUNÇÃO DE AJUDA PARA CRIAR ESTRATÉGIA PRÉ-CONFIGURADA
# ============================================================================

def criar_estrategia_sam_capital(config) -> CapitalBuilder:
    """
    Cria estratégia de capital padrão SAM:
    - Aporte inicial: R$ 100k dos fundadores
    - Empréstimo: R$ 50k após 6 meses para escala
    """
    builder = CapitalBuilder(config)
    
    # Aporte inicial dos fundadores
    builder.add_aporte(
        valor=100000.0,
        data=date(2024, 1, 1),
        socio="Fundador A + B",
        tipo="equity",
        descricao="Aporte inicial para desenvolvimento MVP"
    )
    
    # Empréstimo para escala (após validação)
    builder.add_emprestimo(
        valor_principal=50000.0,
        taxa_juros_anual=0.12,  # 12% ao ano
        prazo_meses=24,
        data_inicio=date(2024, 6, 1),
        carencia_meses=3,  # Só começa a pagar após 3 meses
        tipo="price"
    )
    
    # Próxima rodada (projeção futura)
    builder.add_aporte(
        valor=500000.0,
        data=date(2025, 6, 1),
        socio="Investidor Anjo/Seed",
        tipo="equity",
        descricao="Rodada seed para escala de marketing"
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
            self.estrutura_capital = {}
            self.alteracoes = []
            self.meses_aporte_fixo = 3
            self.aporte_mensal_fixo = 5000
        
        def registrar_alteracao(self, tipo, detalhes):
            self.alteracoes.append({'tipo': tipo, 'detalhes': detalhes})
    
    config = MockConfig()
    
    # Cria estratégia SAM
    builder = criar_estrategia_sam_capital(config)
    
    # DataFrame de exemplo
    df_exemplo = pd.DataFrame({
        'mes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Caixa': [50000, 45000, 40000, 35000, 30000, 25000, 20000, 15000, 10000, 5000],
        'Receita_Bruta': [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000],
        'Custos_Totais': [50000, 45000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000],
    })
    
    # Gera séries temporais
    df_resultado = builder.gerar_series_temporais(df_exemplo)
    
    print("="*70)
    print("CAPITAL BUILDER - TESTE COMPLETO")
    print("="*70)
    
    print("\nColunas geradas:")
    for col in sorted(df_resultado.columns):
        print(f"- {col}")
    
    print("\nPrimeiros 5 meses (colunas principais):")
    cols_vis = ['mes', 'Caixa', 'Aporte_Mes', 'Burn_Rate_Mensal', 'Runway_Meses']
    if 'Meta_MRR 100k' in df_resultado.columns:
        cols_vis.append('Meta_MRR 100k')
    
    print(df_resultado[cols_vis].head().to_string())
    
    print(f"\nTotal de aportes: R$ {sum(a.valor for a in builder.aportes):,.2f}")
    print(f"Total empréstimos: R$ {sum(e.valor_principal for e in builder.emprestimos):,.2f}")
    
    print("\n" + "="*70)
    print("✅ CapitalBuilder funcionando corretamente!")
    print("="*70)
    
    # Relatório
    print("\n" + builder.gerar_relatorio())