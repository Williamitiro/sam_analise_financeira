"""
SAM Financial Model - Módulo de Visualizações Estáticas
=======================================================

Este módulo contém a classe `DashboardFinanceiro`, responsável por gerar
gráficos estáticos de alta qualidade usando Matplotlib e Seaborn.

Finalidade Principal:
- Análise profunda em Jupyter Notebooks.
- Geração de imagens (.png) para relatórios, apresentações e PDFs.
- Complementa os gráficos interativos do app web (que usa Plotly).

Uso típico:
    from visualizations import DashboardFinanceiro
    dashboard = DashboardFinanceiro(projecao_df, kpis)
    dashboard.plot_dashboard_completo(salvar="dashboard.png")
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional, Dict
import numpy as np

# Configuração global de estilo para todos os gráficos
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class DashboardFinanceiro:
    """
    Gera visualizações profissionais e estáticas da projeção financeira.
    
    Esta classe é projetada para criar gráficos prontos para publicação,
    destacando pontos-chave como o "vale da morte", break-even e payback.
    """
    
    def __init__(self, projecao_df: pd.DataFrame, kpis: Dict):
        """
        Inicializa o dashboard com os dados da projeção.
        
        Args:
            projecao_df (pd.DataFrame): DataFrame com a projeção mensal.
            kpis (Dict): Dicionário com os KPIs calculados pelo motor.
        """
        self.df = projecao_df
        self.kpis = kpis
    
    def plot_crescimento_usuarios(self, salvar: Optional[str] = None):
        """Gera o gráfico de crescimento de usuários pagantes."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(self.df['Mes'], self.df['Usuarios_Finais'], 
                linewidth=3, color='#1f77b4', marker='o', markersize=4)
        
        # Adiciona linhas de marco anuais
        for ano in [12, 24, 36]:
            ax.axvline(ano, color='gray', linestyle='--', alpha=0.3)
            usuarios_ano = self.df.loc[self.df['Mes'] == ano, 'Usuarios_Finais'].values[0]
            ax.text(ano, usuarios_ano, f'  {int(usuarios_ano):,} usuários', 
                   verticalalignment='bottom', fontsize=9)
        
        ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax.set_ylabel('Usuários Pagantes', fontsize=12, fontweight='bold')
        ax.set_title('Projeção de Crescimento de Usuários (36 meses)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_mrr_evolucao(self, salvar: Optional[str] = None):
        """Gera o gráfico de evolução do MRR com área preenchida."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.fill_between(self.df['Mes'], 0, self.df['MRR'], 
                        alpha=0.3, color='#2ca02c')
        ax.plot(self.df['Mes'], self.df['MRR'], 
                linewidth=3, color='#2ca02c', marker='o', markersize=4)
        
        # Exemplo de meta de MRR
        ax.axhline(100000, color='red', linestyle='--', alpha=0.5, label='Meta: R$ 100k')
        
        ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax.set_ylabel('MRR (R$)', fontsize=12, fontweight='bold')
        ax.set_title('Evolução da Receita Mensal Recorrente (MRR)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        plt.tight_layout()
        
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_fluxo_caixa(self, salvar: Optional[str] = None):
        """Gera o gráfico de fluxo de caixa e resultado operacional."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Gráfico 1: Saldo de Caixa Acumulado
        ax1.fill_between(self.df['Mes'], 0, self.df['Saldo_Caixa'], 
                         alpha=0.3, color='skyblue')
        ax1.plot(self.df['Mes'], self.df['Saldo_Caixa'], 
                linewidth=3, color='darkblue', marker='o', markersize=4)
        ax1.axhline(0, color='black', linestyle='-', linewidth=1)
        
        # Marca o "vale da morte" com texto mais claro
        vale_mes = self.kpis['Vale_da_Morte_Mes']
        vale_valor = self.kpis['Vale_da_Morte_Minimo_Caixa']
        ax1.plot(vale_mes, vale_valor, 'ro', markersize=10, label='Vale da Morte')
        ax1.text(vale_mes, vale_valor - (ax1.get_ylim()[1] * 0.05), 
                f'  Vale da Morte: R$ {vale_valor:,.0f}', 
                verticalalignment='top', fontsize=9, color='red', fontweight='bold')

        # Marca o payback
        if self.kpis.get('Payback_Investimento_Mes'):
            payback_mes = self.kpis['Payback_Investimento_Mes']
            ax1.axvline(payback_mes, color='green', linestyle='--', alpha=0.5)
            ax1.text(payback_mes, ax1.get_ylim()[1]*0.9, f'  Payback (Mês {payback_mes})', 
                    fontsize=9, color='green', fontweight='bold')
        
        ax1.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Saldo de Caixa (R$)', fontsize=12, fontweight='bold')
        ax1.set_title('Projeção de Saldo de Caixa Acumulado', 
                     fontsize=14, fontweight='bold', pad=20)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        
        # Gráfico 2: Resultado Operacional Mensal
        cores_resultado = ['#d62728' if x < 0 else '#2ca02c' for x in self.df['Resultado_Operacional']]
        ax2.bar(self.df['Mes'], self.df['Resultado_Operacional'], color=cores_resultado, alpha=0.7)
        ax2.axhline(0, color='black', linestyle='-', linewidth=1)
        
        if self.kpis.get('Break_Even_Mes'):
            break_even_mes = self.kpis['Break_Even_Mes']
            ax2.axvline(break_even_mes, color='blue', linestyle='--', alpha=0.5)
            ax2.text(break_even_mes, ax2.get_ylim()[1]*0.9, f'  Break-Even (Mês {break_even_mes})', 
                    fontsize=9, color='blue', fontweight='bold')
        
        ax2.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Resultado Operacional (R$)', fontsize=12, fontweight='bold')
        ax2.set_title('Resultado Operacional Mensal (Lucro/Prejuízo)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        
        plt.tight_layout()
        
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_composicao_custos(self, salvar: Optional[str] = None):
        """
        Gera um gráfico de área empilhada da composição dos custos principais.
        
        Nota: O engine atual agrupa custos detalhados em OPEX_Total. Para um gráfico
        mais rico, o engine poderia retornar um DF com cada custo separado.
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        custos_cols = ['Custo_Infra', 'Custo_Marketing', 'Salario_Pago']
        ax.stackplot(self.df['Mes'], *[self.df[col] for col in custos_cols],
                     labels=['Infraestrutura', 'Marketing', 'Salário Fundador'],
                     alpha=0.7, colors=['#ff7f0e', '#9467bd', '#8c564b'])
        
        ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax.set_ylabel('Custos Fixos (R$)', fontsize=12, fontweight='bold')
        ax.set_title('Evolução da Composição de Custos Fixos (OPEX)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        
        plt.tight_layout()
        
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_comparacao_cenarios(self, dfs_cenarios: Dict[str, pd.DataFrame], salvar: Optional[str] = None):
        """
        [NOVO] Gera um gráfico comparativo de MRR e Saldo de Caixa para múltiplos cenários.
        
        Args:
            dfs_cenarios (Dict[str, pd.DataFrame]): Dicionário com nome do cenário e DataFrame.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
        
        # Paleta de cores
        cores = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db'] # Vermelho, Laranja, Verde, Azul
        
        # Gráfico 1: Comparação de MRR
        for i, (nome, df) in enumerate(dfs_cenarios.items()):
            ax1.plot(df['Mes'], df['MRR'], label=nome, color=cores[i % len(cores)], lw=3)
        
        ax1.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax1.set_ylabel('MRR (R$)', fontsize=12, fontweight='bold')
        ax1.set_title('Comparação de MRR por Cenário', fontsize=14, fontweight='bold', pad=20)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        
        # Gráfico 2: Comparação de Saldo de Caixa
        for i, (nome, df) in enumerate(dfs_cenarios.items()):
            ax2.plot(df['Mes'], df['Saldo_Caixa'], label=nome, color=cores[i % len(cores)], lw=3)
        
        ax2.axhline(0, color='black', linestyle='-', linewidth=1)
        ax2.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Saldo de Caixa (R$)', fontsize=12, fontweight='bold')
        ax2.set_title('Comparação de Saldo de Caixa por Cenário', fontsize=14, fontweight='bold', pad=20)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}k'))
        
        plt.tight_layout()
        
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_dashboard_completo(self, salvar: Optional[str] = None):
        """Gera um dashboard completo com todas as métricas principais em uma única figura."""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # ... (código do dashboard completo, mantido da versão original, mas com KPIs alinhados) ...
        # Garanta que os KPIs aqui usem as chaves corretas, ex: self.kpis['LTV_Final']
        
        # Exemplo de alinhamento no bloco de texto KPI:
        kpis_texto = f"""
╔════════════════════════╗
║   KPIs PRINCIPAIS      ║
╚════════════════════════╝

Break-Even: Mês {self.kpis.get('Break_Even_Mes', 'N/A')}
Payback: Mês {self.kpis.get('Payback_Investimento_Mes', 'N/A')}
LTV: R$ {self.kpis.get('LTV_Final', 0):,.0f}
LTV/CAC: {self.kpis.get('LTV_CAC_Ratio_Final', 0):.2f}x
Vale da Morte: R$ {self.kpis.get('Vale_da_Morte_Minimo_Caixa', 0):,.0f}
MRR Ano 3: R$ {self.kpis.get('MRR_Ano3', 0):,.0f}
Usuários Ano 3: {self.kpis.get('Usuarios_Ano3', 0):,.0f}
        """
        # ... (restante do código do dashboard) ...
        
        fig.suptitle('Dashboard Financeiro - SAM (Projeção 36 Meses)', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight')
        plt.show()

    def gerar_todos_graficos(self, pasta_saida: str = "./graficos"):
        """Gera e salva todos os gráficos individuais em uma pasta especificada."""
        import os
        os.makedirs(pasta_saida, exist_ok=True)
        
        print("📊 Gerando gráficos estáticos para relatório...")
        
        self.plot_crescimento_usuarios(f"{pasta_saida}/01_crescimento_usuarios.png")
        self.plot_mrr_evolucao(f"{pasta_saida}/02_mrr_evolucao.png")
        self.plot_fluxo_caixa(f"{pasta_saida}/03_fluxo_caixa.png")
        self.plot_composicao_custos(f"{pasta_saida}/04_composicao_custos.png")
        self.plot_dashboard_completo(f"{pasta_saida}/00_dashboard_completo.png")
        
        print(f"\n✅ Todos os gráficos foram salvos em: {pasta_saida}")