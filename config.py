"""
SAM Financial Model - Configurações Completas
Sistema de configuração modular e extensível para projeção financeira.

VERSÃO 2.0 - COMPLETA E FINALIZADA
Última Atualização: 2025-11-13

O que foi feito:
1. Estruturado em classes dataclasses para clareza e facilidade de uso.
2. Adicionado sistema completo para gestão de pessoal (CLT/PJ) com meses de início.
3. Implementado controle de despesas de escritório e operações.
4. Criado sistema para ferramentas SaaS categorizadas.
5. Adicionado módulo para serviços profissionais (contabilidade, advogado).
6. Implementado sistema completo de depreciação de ativos (CAPEX).
7. Incluído sistema para despesas anuais rateadas (domínios, etc.).
8. Adicionado cálculo automático de KPIs cruciais (LTV, LTV/CAC, CAC Payback).
9. Criado funções para gerar cenários (padrão, com contratações, pessimista, otimista).
10. Adicionado método para gerar um resumo legível da configuração.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CLASSES AUXILIARES PARA ESTRUTURAS COMPLEXAS
# ═══════════════════════════════════════════════════════════════

@dataclass
class Funcionario:
    """Representa um funcionário CLT ou prestador de serviço."""
    nome: str
    cargo: str
    salario_bruto: float
    mes_inicio: int
    tipo: str = "CLT"  # "CLT" ou "PJ"
    encargos_percentual: float = 0.68  # 68% para CLT (INSS, FGTS, férias, 13º)
    
    def calcular_custo_mensal(self, mes_atual: int) -> float:
        """Calcula o custo mensal total incluindo encargos."""
        if mes_atual < self.mes_inicio:
            return 0.0
        
        if self.tipo == "CLT":
            return self.salario_bruto * (1 + self.encargos_percentual)
        else:  # PJ
            return self.salario_bruto

@dataclass
class FerramentaSaaS:
    """Representa uma ferramenta SaaS com custo mensal."""
    nome: str
    categoria: str  # "dev", "seguranca", "gestao", "comunicacao", "design"
    custo_mensal: float
    mes_inicio: int = 1
    essencial: bool = True  # Se é essencial desde o início
    
    def calcular_custo(self, mes_atual: int) -> float:
        """Retorna o custo se o mês atual >= mês de início."""
        if mes_atual >= self.mes_inicio:
            return self.custo_mensal
        return 0.0

@dataclass
class AtivoDepreciavel:
    """Representa um ativo que será depreciado ao longo do tempo."""
    nome: str
    valor_aquisicao: float
    meses_depreciacao: int  # Vida útil em meses
    mes_aquisicao: int = 0  # Mês 0 = antes do início
    
    def calcular_depreciacao_mensal(self, mes_atual: int) -> float:
        """Calcula a depreciação mensal."""
        # Só deprecia se já foi adquirido e ainda está no período
        if mes_atual > self.mes_aquisicao and mes_atual <= (self.mes_aquisicao + self.meses_depreciacao):
            return self.valor_aquisicao / self.meses_depreciacao
        return 0.0

@dataclass
class DespesaAnual:
    """Representa uma despesa paga anualmente mas rateada mensalmente."""
    nome: str
    valor_anual: float
    mes_pagamento: int = 1  # Mês do ano em que é paga
    
    @property
    def valor_mensal_rateado(self) -> float:
        """Retorna o valor mensal para controle."""
        return self.valor_anual / 12

@dataclass
class ComissaoAfiliado:
    """Configura comissões de afiliados/parceiros."""
    percentual_sobre_venda: float  # Ex: 0.20 = 20%
    mes_inicio_programa: int = 1
    percentual_vendas_via_afiliados: float = 0.0  # Ex: 0.30 = 30% das vendas vêm de afiliados

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════

@dataclass
class ConfigFinanceira:
    """
    Configuração centralizada e completa do modelo financeiro SAM.
    
    Esta classe contém TODAS as premissas do negócio, desde capital inicial
    até custos operacionais detalhados, permitindo simulações precisas.
    """
    
    # ═══════════════════════════════════════════════════════════
    # 1. CAPITAL E FINANCIAMENTO
    # ═══════════════════════════════════════════════════════════
    capital_inicial_caixa: float = -8000.00  # Capex inicial (negativo = saída)
    aporte_mensal_fixo: float = 1800.00
    meses_aporte_fixo: int = 12
    
    # ═══════════════════════════════════════════════════════════
    # 2. FUNIL DE AQUISIÇÃO (DETALHADO)
    # ═══════════════════════════════════════════════════════════
    visitantes_mes_1: int = 1000
    taxa_crescimento_trafego_mensal: float = 0.20  # 20%
    
    # Conversões Split (para cálculo de CAC por etapa)
    taxa_conversao_visitante_trial: float = 0.05  # 5% visitantes → trial
    taxa_conversao_trial_pagante: float = 0.15  # 15% trial → pagante
    
    # Retenção
    churn_mensal: float = 0.04  # 4% cancelamento/mês
    
    # ═══════════════════════════════════════════════════════════
    # 3. MODELO DE RECEITA
    # ═══════════════════════════════════════════════════════════
    # Preços por plano
    preco_plano_lite: float = 69.90
    preco_plano_trader: float = 99.00
    preco_plano_pro: float = 159.00
    
    # Mix de distribuição (deve somar 1.0)
    mix_plano_lite: float = 0.50
    mix_plano_trader: float = 0.30
    mix_plano_pro: float = 0.20
    
    # ARPU calculado automaticamente ou override manual
    arpu_medio_override: Optional[float] = None
    
    @property
    def arpu_medio(self) -> float:
        """Calcula ARPU baseado no mix de planos ou usa override."""
        if self.arpu_medio_override:
            return self.arpu_medio_override
        
        return (
            self.preco_plano_lite * self.mix_plano_lite +
            self.preco_plano_trader * self.mix_plano_trader +
            self.preco_plano_pro * self.mix_plano_pro
        )
    
    # ═══════════════════════════════════════════════════════════
    # 4. CUSTOS VARIÁVEIS (COGS)
    # ═══════════════════════════════════════════════════════════
    # Custos por usuário
    custo_ia_por_usuario: float = 5.00  # LLM API
    
    # Impostos sobre receita
    aliquota_impostos: float = 0.06  # 6% Simples Nacional
    
    # Taxas de meios de pagamento
    taxa_pagamento_percentual: float = 0.0349  # 3.49% (Stripe/Mercado Pago)
    taxa_pagamento_fixa_por_transacao: float = 0.39  # R$ 0,39 por transação
    
    # Comissões de afiliados (sistema completo)
    comissao_afiliados: Optional[ComissaoAfiliado] = None
    
    # ═══════════════════════════════════════════════════════════
    # 5. INFRAESTRUTURA ESCALÁVEL (3 TIERS)
    # ═══════════════════════════════════════════════════════════
    # TIER 1: Validação (0-100 usuários)
    infra_tier1_custo_fixo: float = 209.00
    infra_tier1_limite: int = 100
    infra_tier1_detalhes: Dict[str, float] = field(default_factory=lambda: {
        'vps_principal': 55.00,
        'vps_coleta_mt5': 150.00,
        'dominio': 4.00
    })
    
    # TIER 2: Escala (101-500 usuários)
    infra_tier2_custo_fixo: float = 5559.00
    infra_tier2_limite: int = 500
    infra_tier2_detalhes: Dict[str, float] = field(default_factory=lambda: {
        'api_cedro': 5000.00,
        'vps_robusta': 500.00,
        'ferramentas_infra': 59.00
    })
    
    # TIER 3: Hiperescala (501+ usuários)
    infra_tier3_custo_por_usuario: float = 1.50
    
    # Custos excedentes de cloud (variável)
    cloud_custo_excedente_por_gb: float = 0.10  # R$ 0,10/GB além do plano
    cloud_gb_inclusos_tier: int = 1000  # GB inclusos no tier
    cloud_gb_estimado_por_usuario: float = 0.5  # GB/usuário/mês
    
    # ═══════════════════════════════════════════════════════════
    # 6. MARKETING (2 FASES)
    # ═══════════════════════════════════════════════════════════
    # FASE 1: Validação
    marketing_fase1_custo_fixo: float = 500.00
    marketing_fase1_duracao_meses: int = 3
    
    # FASE 2: Reinvestimento
    marketing_fase2_perc_lucro_bruto: float = 0.25  # 25% do lucro bruto
    
    # CAC Meta (para análise)
    cac_pago_meta: float = 500.00
    
    # ═══════════════════════════════════════════════════════════
    # 7. SALÁRIO DO FUNDADOR (CONDICIONAL)
    # ═══════════════════════════════════════════════════════════
    salario_fundador_valor: float = 5000.00
    salario_fundador_mes_inicio_ideal: int = 6
    salario_fundador_caixa_minimo_seguranca: float = 10000.00
    
    # ═══════════════════════════════════════════════════════════
    # 8. EQUIPE E PESSOAL (SISTEMA COMPLETO)
    # ═══════════════════════════════════════════════════════════
    equipe: List[Funcionario] = field(default_factory=list)
    
    def adicionar_funcionario(
        self,
        nome: str,
        cargo: str,
        salario_bruto: float,
        mes_inicio: int,
        tipo: str = "CLT"
    ):
        """Adiciona um funcionário à equipe."""
        funcionario = Funcionario(
            nome=nome,
            cargo=cargo,
            salario_bruto=salario_bruto,
            mes_inicio=mes_inicio,
            tipo=tipo
        )
        self.equipe.append(funcionario)
    
    # ═══════════════════════════════════════════════════════════
    # 9. ESCRITÓRIO E OPERAÇÃO
    # ═══════════════════════════════════════════════════════════
    # Despesas de escritório/operação
    escritorio_aluguel_mensal: float = 0.0
    escritorio_condominio_mensal: float = 0.0
    escritorio_agua_luz_mensal: float = 0.0
    escritorio_internet_mensal: float = 0.0
    escritorio_outros_mensal: float = 0.0
    escritorio_mes_inicio: int = 999  # 999 = nunca inicia (para empresas remotas)
    
    @property
    def escritorio_custo_total_mensal(self) -> float:
        """Calcula o custo total do escritório."""
        return (
            self.escritorio_aluguel_mensal +
            self.escritorio_condominio_mensal +
            self.escritorio_agua_luz_mensal +
            self.escritorio_internet_mensal +
            self.escritorio_outros_mensal
        )
    
    # ═══════════════════════════════════════════════════════════
    # 10. FERRAMENTAS SAAS (CATEGORIZADAS)
    # ═══════════════════════════════════════════════════════════
    ferramentas_saas: List[FerramentaSaaS] = field(default_factory=list)
    
    def adicionar_ferramenta(
        self,
        nome: str,
        categoria: str,
        custo_mensal: float,
        mes_inicio: int = 1,
        essencial: bool = True
    ):
        """Adiciona uma ferramenta SaaS."""
        ferramenta = FerramentaSaaS(
            nome=nome,
            categoria=categoria,
            custo_mensal=custo_mensal,
            mes_inicio=mes_inicio,
            essencial=essencial
        )
        self.ferramentas_saas.append(ferramenta)
    
    # ═══════════════════════════════════════════════════════════
    # 11. SERVIÇOS PROFISSIONAIS
    # ═══════════════════════════════════════════════════════════
    contabilidade_mensal: float = 0.0
    contabilidade_mes_inicio: int = 1
    
    advogado_retainer_mensal: float = 0.0
    advogado_mes_inicio: int = 999  # 999 = opcional/não usar
    
    consultorias_outras_mensal: float = 0.0
    
    # ═══════════════════════════════════════════════════════════
    # 12. DEPRECIAÇÃO DE ATIVOS
    # ═══════════════════════════════════════════════════════════
    ativos_depreciaveis: List[AtivoDepreciavel] = field(default_factory=list)
    
    def adicionar_ativo_depreciavel(
        self,
        nome: str,
        valor_aquisicao: float,
        meses_depreciacao: int,
        mes_aquisicao: int = 0
    ):
        """Adiciona um ativo para depreciação."""
        ativo = AtivoDepreciavel(
            nome=nome,
            valor_aquisicao=valor_aquisicao,
            meses_depreciacao=meses_depreciacao,
            mes_aquisicao=mes_aquisicao
        )
        self.ativos_depreciaveis.append(ativo)
    
    # ═══════════════════════════════════════════════════════════
    # 13. DESPESAS ANUAIS RATEADAS
    # ═══════════════════════════════════════════════════════════
    despesas_anuais: List[DespesaAnual] = field(default_factory=list)
    
    def adicionar_despesa_anual(
        self,
        nome: str,
        valor_anual: float,
        mes_pagamento: int = 1
    ):
        """Adiciona uma despesa anual (ex: domínio, certificados)."""
        despesa = DespesaAnual(
            nome=nome,
            valor_anual=valor_anual,
            mes_pagamento=mes_pagamento
        )
        self.despesas_anuais.append(despesa)
    
    # ═══════════════════════════════════════════════════════════
    # MÉTODOS DE CÁLCULO
    # ═══════════════════════════════════════════════════════════
    
    def calcular_ltv(self) -> float:
        """
        Calcula o Lifetime Value (LTV) do cliente.
        
        Fórmula:
        LTV = (ARPU × (1 - Taxa_Imposto - Taxa_Pagamento) - COGS) / Churn
        """
        # Lucro bruto por usuário (após impostos e taxas)
        receita_liquida = self.arpu_medio * (
            1 - self.aliquota_impostos - self.taxa_pagamento_percentual
        )
        lucro_bruto_por_usuario = receita_liquida - self.custo_ia_por_usuario
        
        return lucro_bruto_por_usuario / self.churn_mensal
    
    def calcular_ltv_cac_ratio(self) -> float:
        """Calcula a relação LTV/CAC."""
        return self.calcular_ltv() / self.cac_pago_meta
    
    def calcular_cac_payback_meses(self) -> float:
        """
        Calcula o CAC Payback em meses.
        
        Fórmula:
        Payback = CAC / (ARPU × Margem_Bruta)
        """
        margem_bruta_percentual = (
            1 - self.aliquota_impostos - 
            self.taxa_pagamento_percentual - 
            (self.custo_ia_por_usuario / self.arpu_medio)
        )
        lucro_bruto_mensal = self.arpu_medio * margem_bruta_percentual
        
        return self.cac_pago_meta / lucro_bruto_mensal
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário (útil para salvar em JSON)."""
        base_dict = {
            k: v for k, v in self.__dict__.items() 
            if not k.startswith('_') and not isinstance(v, list)
        }
        
        # Adiciona listas de forma estruturada
        base_dict['equipe'] = [
            {
                'nome': f.nome,
                'cargo': f.cargo,
                'salario': f.salario_bruto,
                'tipo': f.tipo,
                'mes_inicio': f.mes_inicio
            }
            for f in self.equipe
        ]
        
        base_dict['ferramentas_saas'] = [
            {
                'nome': f.nome,
                'categoria': f.categoria,
                'custo': f.custo_mensal,
                'mes_inicio': f.mes_inicio
            }
            for f in self.ferramentas_saas
        ]
        
        return base_dict
    
    def gerar_resumo_config(self) -> str:
        """Gera um resumo textual da configuração."""
        resumo = f"""
╔════════════════════════════════════════════════════════════════╗
║          RESUMO DA CONFIGURAÇÃO FINANCEIRA - SAM               ║
╚════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════
💰 CAPITAL E FINANCIAMENTO
═══════════════════════════════════════════════════════════════
Capital Inicial (CAPEX): R$ {abs(self.capital_inicial_caixa):,.2f}
Aporte Mensal: R$ {self.aporte_mensal_fixo:,.2f} ({self.meses_aporte_fixo} meses)

═══════════════════════════════════════════════════════════════
📊 FUNIL DE AQUISIÇÃO
═══════════════════════════════════════════════════════════════
Visitantes Mês 1: {self.visitantes_mes_1:,}
Crescimento Tráfego: {self.taxa_crescimento_trafego_mensal*100:.1f}%/mês
Conversão Visitante→Trial: {self.taxa_conversao_visitante_trial*100:.1f}%
Conversão Trial→Pagante: {self.taxa_conversao_trial_pagante*100:.1f}%
Churn Mensal: {self.churn_mensal*100:.1f}%

═══════════════════════════════════════════════════════════════
💵 RECEITA
═══════════════════════════════════════════════════════════════
ARPU Médio: R$ {self.arpu_medio:.2f}
  • Lite ({self.mix_plano_lite*100:.0f}%): R$ {self.preco_plano_lite:.2f}
  • Trader ({self.mix_plano_trader*100:.0f}%): R$ {self.preco_plano_trader:.2f}
  • Pro ({self.mix_plano_pro*100:.0f}%): R$ {self.preco_plano_pro:.2f}

═══════════════════════════════════════════════════════════════
💎 MÉTRICAS-CHAVE
═══════════════════════════════════════════════════════════════
LTV: R$ {self.calcular_ltv():,.2f}
LTV/CAC: {self.calcular_ltv_cac_ratio():.2f}x
CAC Payback: {self.calcular_cac_payback_meses():.1f} meses

═══════════════════════════════════════════════════════════════
👥 EQUIPE
═══════════════════════════════════════════════════════════════
"""
        if self.equipe:
            for func in self.equipe:
                resumo += f"  • {func.cargo}: R$ {func.salario_bruto:,.2f} ({func.tipo}) - A partir do mês {func.mes_inicio}\n"
        else:
            resumo += "  • Nenhum funcionário configurado ainda\n"
        
        resumo += f"""
═══════════════════════════════════════════════════════════════
🏢 ESCRITÓRIO
═══════════════════════════════════════════════════════════════
"""
        if self.escritorio_mes_inicio < 999:
            resumo += f"Custo Total: R$ {self.escritorio_custo_total_mensal:,.2f}/mês (a partir do mês {self.escritorio_mes_inicio})\n"
        else:
            resumo += "  • Operação remota (sem escritório físico)\n"
        
        return resumo


# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES PADRÃO E CENÁRIOS
# ═══════════════════════════════════════════════════════════════

def criar_config_padrao() -> ConfigFinanceira:
    """Cria a configuração padrão do SAM."""
    config = ConfigFinanceira()
    
    # Adiciona equipamentos para depreciação
    config.adicionar_ativo_depreciavel(
        nome="Estação de Trabalho P&D",
        valor_aquisicao=8000.00,
        meses_depreciacao=24,
        mes_aquisicao=0
    )
    
    # Adiciona ferramentas SaaS essenciais
    config.adicionar_ferramenta("GitHub Copilot", "dev", 100.00, mes_inicio=1)
    config.adicionar_ferramenta("Cursor IDE", "dev", 200.00, mes_inicio=1)
    config.adicionar_ferramenta("Firecrawl", "dev", 100.00, mes_inicio=1)
    config.adicionar_ferramenta("Sentry", "seguranca", 0.00, mes_inicio=1, essencial=True)
    
    # Adiciona despesas anuais
    config.adicionar_despesa_anual("Domínio .com.br", 40.00, mes_pagamento=1)
    
    return config

def criar_config_com_contratacoes() -> ConfigFinanceira:
    """Cria configuração com contratações planejadas."""
    config = criar_config_padrao()
    
    # Contratação 1: Dev Backend (Ano 1)
    config.adicionar_funcionario(
        nome="Dev Backend Pleno",
        cargo="Engenheiro de Software",
        salario_bruto=8000.00,
        mes_inicio=12,
        tipo="CLT"
    )
    
    # Contratação 2: Community Manager (Ano 2)
    config.adicionar_funcionario(
        nome="Community Manager",
        cargo="Sucesso do Cliente",
        salario_bruto=4000.00,
        mes_inicio=18,
        tipo="CLT"
    )
    
    # Freelancer: Designer (a partir do mês 6)
    config.adicionar_funcionario(
        nome="Designer UI/UX",
        cargo="Designer",
        salario_bruto=3000.00,
        mes_inicio=6,
        tipo="PJ"
    )
    
    # Adiciona contabilidade
    config.contabilidade_mensal = 500.00
    config.contabilidade_mes_inicio = 1
    
    return config

def criar_config_pessimista() -> ConfigFinanceira:
    """Cenário pessimista: crescimento lento, churn alto."""
    config = criar_config_padrao()
    config.taxa_crescimento_trafego_mensal = 0.10
    config.taxa_conversao_trial_pagante = 0.10
    config.churn_mensal = 0.06
    config.salario_fundador_mes_inicio_ideal = 12
    return config

def criar_config_otimista() -> ConfigFinanceira:
    """Cenário otimista: crescimento acelerado, boa retenção."""
    config = criar_config_padrao()
    config.taxa_crescimento_trafego_mensal = 0.30
    config.taxa_conversao_trial_pagante = 0.20
    config.churn_mensal = 0.03
    config.marketing_fase2_perc_lucro_bruto = 0.35
    return config


# ═══════════════════════════════════════════════════════════════
# CONSTANTES EXPORTADAS
# ═══════════════════════════════════════════════════════════════

CONFIG_PADRAO = criar_config_padrao()
CONFIG_COM_CONTRATACOES = criar_config_com_contratacoes()
CONFIG_PESSIMISTA = criar_config_pessimista()
CONFIG_OTIMISTA = criar_config_otimista()


# ═══════════════════════════════════════════════════════════════
# EXEMPLO DE USO E RESPOSTAS ÀS PERGUNTAS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Exemplo 1: Usar a configuração com contratações
    config = criar_config_com_contratacoes()
    
    # Adicionar uma nova ferramenta dinamicamente
    config.adicionar_ferramenta("Notion", "gestao", 50.00, mes_inicio=4)
    
    # Imprimir o resumo da configuração
    print(config.gerar_resumo_config())

    # ══════════════════════════════════════════════════════════
    # RESPOSTAS ÀS SUAS PERGUNTAS:
    # ══════════════════════════════════════════════════════════