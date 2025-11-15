"""
core/builders/remaining_builders.py

Builders restantes do sistema SAM Financial Model.
Este arquivo contém 8 builders adicionais.

INSTRUÇÕES: Separar cada builder em seu próprio arquivo:
- tools_builder.py
- marketing_builder.py
- cogs_builder.py
- revenue_builder.py
- capital_builder.py
- risk_builder.py
- tax_builder.py
- scenario_builder.py
"""

# ============================================================================
# 1. TOOLS_BUILDER.PY - Stack de Ferramentas SaaS
# ============================================================================

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class CategoriaFerramenta(Enum):
    DEV = "desenvolvimento"
    IA = "ia_apis"
    INFRA = "infraestrutura"
    GESTAO = "gestao"
    COMUNICACAO = "comunicacao"
    DESIGN = "design"
    SEGURANCA = "seguranca"
    ANALYTICS = "analytics"
    MARKETING = "marketing"

@dataclass
class FerramentaSaaS:
    """Ferramenta SaaS com custo mensal"""
    nome: str
    categoria: CategoriaFerramenta
    custo_mensal: float
    provider: str = ""
    descricao: str = ""
    essencial: bool = True
    custo_por_usuario: float = 0.0  # Se escala com usuários
    mes_inicio: int = 1
    mes_fim: Optional[int] = None
    ativa: bool = True

class ToolsBuilder:
    """
    Builder para stack de ferramentas SaaS.
    
    Uso:
        builder = ToolsBuilder(config)
        builder.add_ferramenta_dev("Cursor IDE", 200)
        builder.add_ferramenta_ia("Claude Pro", 400)
        builder.add_ferramenta_dev("GitHub Copilot", 100)
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.ferramentas: List[FerramentaSaaS] = []
    
    def add_ferramenta(
        self,
        nome: str,
        categoria: CategoriaFerramenta,
        custo_mensal: float,
        provider: str = "",
        essencial: bool = True,
        custo_por_usuario: float = 0.0,
        mes_inicio: int = 1
    ) -> 'ToolsBuilder':
        """Adiciona ferramenta genérica"""
        ferramenta = FerramentaSaaS(
            nome=nome,
            categoria=categoria,
            custo_mensal=custo_mensal,
            provider=provider,
            essencial=essencial,
            custo_por_usuario=custo_por_usuario,
            mes_inicio=mes_inicio
        )
        self.ferramentas.append(ferramenta)
        return self
    
    def add_ferramenta_dev(self, nome: str, custo: float, provider: str = "") -> 'ToolsBuilder':
        """Adiciona ferramenta de desenvolvimento"""
        return self.add_ferramenta(nome, CategoriaFerramenta.DEV, custo, provider, True)
    
    def add_ferramenta_ia(self, nome: str, custo: float, provider: str = "") -> 'ToolsBuilder':
        """Adiciona ferramenta de IA/APIs"""
        return self.add_ferramenta(nome, CategoriaFerramenta.IA, custo, provider, True)
    
    def add_ferramenta_gestao(self, nome: str, custo: float, provider: str = "", custo_por_usuario: float = 0) -> 'ToolsBuilder':
        """Adiciona ferramenta de gestão (Notion, etc)"""
        return self.add_ferramenta(nome, CategoriaFerramenta.GESTAO, custo, provider, False, custo_por_usuario)
    
    def build(self):
        """Aplica ao config"""
        self.config.ferramentas_saas = self.ferramentas
        self.config.registrar_alteracao("Configuração de ferramentas SaaS", 
                                       detalhes={'total': len(self.ferramentas)})
        return self.config

def criar_stack_sam(config):
    """Stack de ferramentas SAM conforme especificação"""
    builder = ToolsBuilder(config)
    
    # Desenvolvimento
    builder.add_ferramenta_dev("Cursor IDE", 200, "Cursor")
    builder.add_ferramenta_dev("GitHub Copilot", 100, "GitHub")
    builder.add_ferramenta_dev("Firecrawl", 100, "Firecrawl")
    
    # IA & APIs
    builder.add_ferramenta_ia("Claude Pro (3 usuários)", 400, "Anthropic")
    builder.add_ferramenta_ia("OpenAI API", 100, "OpenAI")  # Custo inicial baixo
    
    # Segurança & Monitoramento
    builder.add_ferramenta("Sentry", CategoriaFerramenta.SEGURANCA, 0, "Sentry", True)  # Free tier
    
    # Gestão (opcional)
    builder.add_ferramenta_gestao("Notion", 50, "Notion", custo_por_usuario=8)
    
    return builder.build()


# ============================================================================
# 2. MARKETING_BUILDER.PY - Fases de Marketing
# ============================================================================

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


# ============================================================================
# 3. COGS_BUILDER.PY - Custos Variáveis Completos
# ============================================================================

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


# ============================================================================
# 4. REVENUE_BUILDER.PY - Modelo de Receita Complexo
# ============================================================================

@dataclass
class Plano:
    """Plano de assinatura"""
    nome: str
    preco: float
    mix_inicial: float  # Percentual no início
    descricao: str = ""

@dataclass
class AddOn:
    """Add-on/funcionalidade extra"""
    nome: str
    preco: float
    percentual_usuarios_que_compram: float
    mes_lancamento: int = 1

class RevenueBuilder:
    """
    Builder para modelo de receita.
    
    Uso:
        builder = RevenueBuilder(config)
        builder.add_plano("Lite", 70, 0.50)
        builder.add_plano("Trader", 105, 0.30)
        builder.add_plano("Pro", 159, 0.20)
        builder.com_upsell(0.02, "Lite", "Trader")  # 2% migra/mês
        builder.add_addon("Alertas Premium", 20, 0.15)  # 15% compram
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.planos: List[Plano] = []
        self.addons: List[AddOn] = []
    
    def add_plano(self, nome: str, preco: float, mix: float, descricao: str = "") -> 'RevenueBuilder':
        """Adiciona plano"""
        plano = Plano(nome=nome, preco=preco, mix_inicial=mix, descricao=descricao)
        self.planos.append(plano)
        return self
    
    def add_addon(self, nome: str, preco: float, percentual_compra: float, mes_lancamento: int = 1) -> 'RevenueBuilder':
        """Adiciona add-on"""
        addon = AddOn(nome=nome, preco=preco, 
                     percentual_usuarios_que_compram=percentual_compra,
                     mes_lancamento=mes_lancamento)
        self.addons.append(addon)
        return self
    
    def com_upsell(self, taxa_mensal: float, plano_origem: str, plano_destino: str) -> 'RevenueBuilder':
        """Configura taxa de upsell entre planos"""
        if not hasattr(self.config, 'upsell_rules'):
            self.config.upsell_rules = []
        self.config.upsell_rules.append({
            'taxa': taxa_mensal,
            'origem': plano_origem,
            'destino': plano_destino
        })
        return self
    
    def build(self):
        """Aplica ao config"""
        if self.planos:
            self.config.planos = self.planos
            # Atualiza preços e mix legados
            if len(self.planos) >= 1:
                self.config.preco_plano_lite = self.planos[0].preco
                self.config.mix_plano_lite = self.planos[0].mix_inicial
            if len(self.planos) >= 2:
                self.config.preco_plano_trader = self.planos[1].preco
                self.config.mix_plano_trader = self.planos[1].mix_inicial
            if len(self.planos) >= 3:
                self.config.preco_plano_pro = self.planos[2].preco
                self.config.mix_plano_pro = self.planos[2].mix_inicial
        
        if self.addons:
            self.config.addons = self.addons
        
        self.config.registrar_alteracao("Configuração de receita")
        return self.config


# ============================================================================
# 5. CAPITAL_BUILDER.PY - Aportes e Financiamento
# ============================================================================

@dataclass
class Aporte:
    """Aporte de capital"""
    valor: float
    mes: int
    tipo: str = "equity"  # 'equity', 'debt', 'grant'
    diluicao: float = 0.0  # Se equity
    juros_anual: float = 0.0  # Se debt
    carencia_meses: int = 0  # Se debt
    nome_investidor: str = ""

@dataclass
class Emprestimo:
    """Empréstimo com juros"""
    valor: float
    mes_desembolso: int
    juros_anual: float
    prazo_meses: int
    carencia_meses: int = 0
    banco: str = ""

class CapitalBuilder:
    """
    Builder para aportes e financiamento.
    
    Uso:
        builder = CapitalBuilder(config)
        builder.capex_inicial(8000)
        builder.add_aporte(50000, mes=1, tipo="equity", diluicao=0.20, investidor="Fundo XYZ")
        builder.add_aporte(100000, mes=12, tipo="equity", diluicao=0.15, investidor="Series A")
        builder.add_emprestimo(50000, mes=6, juros=0.12, prazo=24, carencia=6)
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.aportes: List[Aporte] = []
        self.emprestimos: List[Emprestimo] = []
    
    def capex_inicial(self, valor: float) -> 'CapitalBuilder':
        """Define CAPEX inicial"""
        self.config.capital_inicial_caixa = -abs(valor)  # Negativo = saída
        return self
    
    def add_aporte(
        self,
        valor: float,
        mes: int,
        tipo: str = "equity",
        diluicao: float = 0.0,
        investidor: str = "",
        juros: float = 0.0,
        carencia: int = 0
    ) -> 'CapitalBuilder':
        """Adiciona aporte"""
        aporte = Aporte(
            valor=valor,
            mes=mes,
            tipo=tipo,
            diluicao=diluicao,
            juros_anual=juros,
            carencia_meses=carencia,
            nome_investidor=investidor
        )
        self.aportes.append(aporte)
        return self
    
    def add_emprestimo(
        self,
        valor: float,
        mes: int,
        juros_anual: float,
        prazo_meses: int,
        carencia: int = 0,
        banco: str = ""
    ) -> 'CapitalBuilder':
        """Adiciona empréstimo"""
        emprestimo = Emprestimo(
            valor=valor,
            mes_desembolso=mes,
            juros_anual=juros_anual,
            prazo_meses=prazo_meses,
            carencia_meses=carencia,
            banco=banco
        )
        self.emprestimos.append(emprestimo)
        return self
    
    def build(self):
        """Aplica ao config"""
        self.config.aportes_programados = self.aportes
        self.config.emprestimos = self.emprestimos
        self.config.registrar_alteracao("Configuração de capital")
        return self.config


# ============================================================================
# 6. RISK_BUILDER.PY - Cenários de Risco
# ============================================================================

@dataclass
class CenarioRisco:
    """Cenário de risco (recessão, perda de cliente, etc)"""
    nome: str
    probabilidade: float  # 0.0 a 1.0
    mes_inicio: int
    duracao_meses: int
    impacto_receita: float = 0.0  # Percentual (ex: -0.20 = -20%)
    impacto_churn: float = 0.0  # Multiplicador (ex: 2.0 = dobra)
    impacto_cac: float = 0.0  # Multiplicador (ex: 1.3 = +30%)
    descricao: str = ""

@dataclass
class Contingencia:
    """Plano de contingência"""
    nome: str
    reserva_percentual_receita: float = 0.10  # 10% de reserva
    gatilho_ativacao: str = "caixa_abaixo_runway_6m"

class RiskBuilder:
    """
    Builder para gestão de riscos.
    
    Uso:
        builder = RiskBuilder(config)
        builder.reserva_emergencia(0.10)  # 10% da receita
        builder.cenario_recessao(mes=12, duracao=6, impacto_receita=-0.15, prob=0.30)
        builder.cenario_churn_spike(mes=8, duracao=3, impacto_churn=2.0, prob=0.20)
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.cenarios: List[CenarioRisco] = []
        self.contingencia: Optional[Contingencia] = None
    
    def reserva_emergencia(self, percentual: float) -> 'RiskBuilder':
        """Configura reserva de emergência"""
        self.contingencia = Contingencia(
            nome="Reserva de Emergência",
            reserva_percentual_receita=percentual
        )
        return self
    
    def cenario_recessao(
        self,
        mes: int,
        duracao: int,
        impacto_receita: float,
        prob: float = 0.30
    ) -> 'RiskBuilder':
        """Adiciona cenário de recessão"""
        cenario = CenarioRisco(
            nome="Recessão Econômica",
            probabilidade=prob,
            mes_inicio=mes,
            duracao_meses=duracao,
            impacto_receita=impacto_receita,
            descricao=f"Receita cai {abs(impacto_receita)*100:.0f}% por {duracao} meses"
        )
        self.cenarios.append(cenario)
        return self
    
    def cenario_churn_spike(
        self,
        mes: int,
        duracao: int,
        impacto_churn: float,
        prob: float = 0.20
    ) -> 'RiskBuilder':
        """Adiciona cenário de pico de churn"""
        cenario = CenarioRisco(
            nome="Pico de Churn",
            probabilidade=prob,
            mes_inicio=mes,
            duracao_meses=duracao,
            impacto_churn=impacto_churn,
            descricao=f"Churn {impacto_churn:.1f}x maior por {duracao} meses"
        )
        self.cenarios.append(cenario)
        return self
    
    def build(self):
        """Aplica ao config"""
        self.config.cenarios_risco = self.cenarios
        if self.contingencia:
            self.config.contingencia = self.contingencia
        self.config.registrar_alteracao("Configuração de riscos")
        return self.config


# ============================================================================
# 7. TAX_BUILDER.PY - Impostos Progressivos
# ============================================================================

@dataclass
class FaixaTributaria:
    """Faixa de tributação"""
    faturamento_min: float
    faturamento_max: float
    aliquota: float
    regime: str  # "Simples Nacional", "Lucro Presumido", "Lucro Real"

class TaxBuilder:
    """
    Builder para impostos progressivos.
    
    Uso:
        builder = TaxBuilder(config)
        builder.simples_nacional(
            faixa1=(0, 180000, 0.06),
            faixa2=(180000, 360000, 0.08),
            faixa3=(360000, 720000, 0.11)
        )
        builder.lucro_presumido_apos(720000, 0.22)
        builder.build()
    """
    
    def __init__(self, config):
        self.config = config
        self.faixas: List[FaixaTributaria] = []
    
    def simples_nacional(
        self,
        faixa1: tuple,
        faixa2: tuple,
        faixa3: tuple
    ) -> 'TaxBuilder':
        """Configura faixas do Simples Nacional"""
        for (min_val, max_val, aliq) in [faixa1, faixa2, faixa3]:
            faixa = FaixaTributaria(
                faturamento_min=min_val,
                faturamento_max=max_val,
                aliquota=aliq,
                regime="Simples Nacional"
            )
            self.faixas.append(faixa)
        return self
    
    def lucro_presumido_apos(self, faturamento: float, aliquota: float) -> 'TaxBuilder':
        """Configura Lucro Presumido após limite"""
        faixa = FaixaTributaria(
            faturamento_min=faturamento,
            faturamento_max=float('inf'),
            aliquota=aliquota,
            regime="Lucro Presumido"
        )
        self.faixas.append(faixa)
        return self
    
    def build(self):
        """Aplica ao config"""
        self.config.faixas_tributarias = sorted(self.faixas, key=lambda f: f.faturamento_min)
        self.config.registrar_alteracao("Configuração de impostos")
        return self.config


# ============================================================================
# 8. SCENARIO_BUILDER.PY - Orquestrador de Cenários Completos
# ============================================================================

class ScenarioBuilder:
    """
    Orquestrador que combina todos os builders para criar cenários completos.
    
    Uso:
        scenario = ScenarioBuilder("SAM - Cenário Base")
        scenario.usar_canais(criar_estrategia_sam_canais)
        scenario.usar_infra(criar_infra_sam)
        scenario.usar_equipe(criar_equipe_sam)
        scenario.usar_tools(criar_stack_sam)
        config = scenario.build()
    """
    
    def __init__(self, nome: str):
        from core.config import ConfigFinanceira
        self.config = ConfigFinanceira()
        self.nome = nome
        self.builders_aplicados = []
    
    def usar_canais(self, func_builder) -> 'ScenarioBuilder':
        """Aplica builder de canais"""
        func_builder(self.config)
        self.builders_aplicados.append("channels")
        return self
    
    def usar_infra(self, func_builder) -> 'ScenarioBuilder':
        """Aplica builder de infra"""
        func_builder(self.config)
        self.builders_aplicados.append("infra")
        return self
    
    def usar_equipe(self, func_builder) -> 'ScenarioBuilder':
        """Aplica builder de equipe"""
        func_builder(self.config)
        self.builders_aplicados.append("team")
        return self
    
    def usar_tools(self, func_builder) -> 'ScenarioBuilder':
        """Aplica builder de ferramentas"""
        func_builder(self.config)
        self.builders_aplicados.append("tools")
        return self
    
    def build(self):
        """Retorna config consolidado"""
        self.config.nome_cenario = self.nome
        self