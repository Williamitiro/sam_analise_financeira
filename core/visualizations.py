"""
core/visualizations.py

Visualizações estáticas e utilitárias para o SAM Financial Model.
- Integra com core.glossary.obter_explicacao(key, estilo="layman")
- Defensive: não quebra se colunas faltam
- Gera gráficos para relatórios (matplotlib) e funções helper para Plotly
"""

from typing import Optional, Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set estilo consistente
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams["figure.figsize"] = (14, 7)
plt.rcParams["axes.titlepad"] = 12

# Tenta importar glossary; se não existir, fornece fallback
try:
    from .glossary import obter_explicacao
except Exception:
    def obter_explicacao(key: str, estilo: str = "layman") -> str:
        fallback = {
            "MRR": "MRR = receita recorrente mensal (o valor cobrado por mês nas assinaturas).",
            "LTV": "LTV = valor que um cliente gera durante seu tempo como cliente.",
            "CAC": "CAC = custo médio para conquistar um cliente.",
            "Caixa": "Saldo disponível em caixa da empresa."
        }
        return fallback.get(key.upper(), key)

# ---------------------------
# Helpers defensivos
# ---------------------------
def _has_cols(df: pd.DataFrame, cols: List[str]) -> bool:
    return all(c in df.columns for c in cols)

def _safe_get(df: pd.DataFrame, col: str, fallback=0.0):
    return df[col] if col in df.columns else pd.Series([fallback] * len(df))

# ---------------------------
# Classe de dashboard estático
# ---------------------------
class DashboardFinanceiro:
    def __init__(self, projecao_df: pd.DataFrame, kpis: Optional[Dict] = None):
        """
        Args:
            projecao_df: DataFrame com projeção mensal (colunas esperadas: 'mes','mrr','caixa','ebitda', etc.)
            kpis: dicionário com KPIs (opcional)
        """
        if projecao_df is None:
            raise ValueError("projecao_df não pode ser None")
        self.df = projecao_df.copy()
        # normaliza colunas para lower case para evitar KeyError
        self.df.columns = [str(c).strip().lower() for c in self.df.columns]
        self.kpis = kpis or {}

    def plot_crescimento_usuarios(self, salvar: Optional[str] = None):
        """Gráfico: usuários pagantes ao longo do tempo (fallback para colunas alternativas)."""
        # tenta colunas comuns
        users_col = None
        for cand in ["clientes_ativos", "usuarios_finais", "usuarios", "users"]:
            if cand in self.df.columns:
                users_col = cand
                break

        if users_col is None:
            print("Aviso: coluna de usuários não encontrada. Gráfico será omitido.")
            return

        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(self.df["mes"], self.df[users_col], marker='o', linewidth=2)
        ax.set_title("Crescimento de Usuários Pagantes (mês a mês)")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Usuários pagantes")
        ax.grid(alpha=0.25)

        # Legenda explicativa
        explanation = obter_explicacao("Usuários", "layman")
        ax.annotate(explanation, xy=(0.01, -0.15), xycoords='axes fraction', fontsize=9)

        plt.tight_layout()
        if salvar:
            os.makedirs(os.path.dirname(salvar) or ".", exist_ok=True)
            plt.savefig(salvar, dpi=300, bbox_inches="tight")
        plt.show()

    def plot_mrr_evolucao(self, salvar: Optional[str] = None):
        """Gráfico: MRR (linha + área)."""
        if "mrr" not in self.df.columns:
            print("Aviso: coluna 'mrr' não encontrada. O gráfico de MRR será omitido.")
            return

        fig, ax = plt.subplots(figsize=(12,6))
        ax.fill_between(self.df["mes"], 0, self.df["mrr"], alpha=0.25)
        ax.plot(self.df["mes"], self.df["mrr"], marker='o', linewidth=2)
        ax.set_title("Evolução do MRR (Receita Recorrente Mensal)")
        ax.set_xlabel("Mês")
        ax.set_ylabel("MRR (R$)")
        ax.grid(alpha=0.25)

        explanation = obter_explicacao("MRR", "layman")
        ax.annotate(explanation, xy=(0.01, -0.15), xycoords='axes fraction', fontsize=9)

        plt.tight_layout()
        if salvar:
            os.makedirs(os.path.dirname(salvar) or ".", exist_ok=True)
            plt.savefig(salvar, dpi=300, bbox_inches="tight")
        plt.show()

    def plot_fluxo_caixa(self, salvar: Optional[str] = None):
        """Gráfico: saldo de caixa acumulado e resultado operacional (barra)."""
        if "caixa" not in self.df.columns:
            print("Aviso: coluna 'caixa' não encontrada. O gráfico de fluxo de caixa será omitido.")
            return

        # Preparação
        ebitda = _safe_get(self.df, "ebitda", 0.0)

        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(14,9), gridspec_kw={'height_ratios':[2,1]})
        ax1.plot(self.df["mes"], self.df["caixa"], marker='o', linewidth=2)
        ax1.fill_between(self.df["mes"], 0, self.df["caixa"], alpha=0.12)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.set_title("Saldo de Caixa Acumulado")
        ax1.set_xlabel("Mês")
        ax1.set_ylabel("Caixa (R$)")

        # marca o vale da morte se existir no kpis
        if self.kpis and "Vale_da_Morte_Minimo_Caixa" in self.kpis and "Vale_da_Morte_Mes" in self.kpis:
            try:
                vm = self.kpis["Vale_da_Morte_Minimo_Caixa"]
                vm_mes = self.kpis["Vale_da_Morte_Mes"]
                ax1.plot(vm_mes, vm, 'ro', markersize=8)
                ax1.annotate(f"Vale da Morte: R$ {vm:,.0f}\n(Mês {vm_mes})", xy=(vm_mes, vm), xytext=(vm_mes, vm*1.1),
                             arrowprops=dict(arrowstyle="->"), fontsize=9, color='red')
            except Exception:
                pass

        # resultado operacional
        ax2.bar(self.df["mes"], ebitda, color=['#2ca02c' if x>=0 else '#d62728' for x in ebitda])
        ax2.set_title("Resultado Operacional Mensal (EBITDA)")
        ax2.set_xlabel("Mês")
        ax2.set_ylabel("R$")

        explanation = obter_explicacao("Caixa", "layman")
        ax1.annotate(explanation, xy=(0.01, -0.15), xycoords='axes fraction', fontsize=9)

        plt.tight_layout()
        if salvar:
            os.makedirs(os.path.dirname(salvar) or ".", exist_ok=True)
            plt.savefig(salvar, dpi=300, bbox_inches="tight")
        plt.show()

    def plot_composicao_custos(self, salvar: Optional[str] = None):
        """Área empilhada: composição de custos (operações)."""
        custo_cols = [c for c in ["folha","infra","marketing","custo_ia","cogs"] if c in self.df.columns]
        if not custo_cols:
            print("Aviso: nenhuma coluna de custo detalhada encontrada para composição.")
            return

        fig, ax = plt.subplots(figsize=(12,6))
        ax.stackplot(self.df["mes"], *[self.df[c] for c in custo_cols], labels=custo_cols, alpha=0.8)
        ax.set_title("Composição de Custos Operacionais (OPEX/COGS)")
        ax.set_xlabel("Mês")
        ax.set_ylabel("R$")
        ax.legend(loc='upper left')
        ax.grid(alpha=0.25)

        plt.tight_layout()
        if salvar:
            os.makedirs(os.path.dirname(salvar) or ".", exist_ok=True)
            plt.savefig(salvar, dpi=300, bbox_inches="tight")
        plt.show()

    def gerar_todos_graficos(self, pasta_saida: str = "./graficos"):
        """Gera e salva todos os gráficos disponíveis (quando possível)."""
        os.makedirs(pasta_saida, exist_ok=True)
        print("Gerando gráficos em:", pasta_saida)
        self.plot_crescimento_usuarios(os.path.join(pasta_saida, "01_crescimento_usuarios.png"))
        self.plot_mrr_evolucao(os.path.join(pasta_saida, "02_mrr_evolucao.png"))
        self.plot_fluxo_caixa(os.path.join(pasta_saida, "03_fluxo_caixa.png"))
        self.plot_composicao_custos(os.path.join(pasta_saida, "04_composicao_custos.png"))
        print("Concluído.")
