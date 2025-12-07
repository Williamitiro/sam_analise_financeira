"""
SAM Financial Model - Configurações Completas
Sistema de configuração modular e extensível para projeção financeira.

VERSÃO 2.1 - Unificado com Builders
Última Atualização: 2025-11-14

O que foi feito:
1. Unificada a definição da classe FerramentaSaaS, que agora é importada do
   respectivo builder para evitar conflitos de assinatura de método.
"""

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

# Importa a definição da classe do builder para ser a única fonte da verdade
from .builders.tools_builder import FerramentaSaaS, CategoriaFerramenta

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
    ativo: bool = True
    mes_fim: Optional[int] = None
    
    def calcular_custo_mensal(self, mes_atual: int) -> float:
        """Calcula o custo mensal total incluindo encargos."""
        if not self.ativo:
            return 0.0
        if mes_atual < self.mes_inicio:
            return 0.0
        if self.mes_fim is not None and mes_atual > self.mes_fim:
            return 0.0
        
        if self.tipo == "CLT":
            return self.salario_bruto * (1 + self.encargos_percentual)
        else:  # PJ
            return self.salario_bruto

# A classe FerramentaSaaS foi removida daqui e agora é importada do tools_builder.py

@dataclass
class AtivoDepreciavel:
    """Representa um ativo que será depreciado ao longo do tempo."""
    nome: str
    valor_aquisicao: float
    meses_depreciacao: int  # Vida útil em meses
    mes_aquisicao: int = 0  # Mês 0 = antes do início
    ativo: bool = True
    mes_fim: Optional[int] = None
    
    def calcular_depreciacao_mensal(self, mes_atual: int) -> float:
        """Calcula a depreciação mensal."""
        if not self.ativo:
            return 0.0
        if mes_atual <= self.mes_aquisicao:
            return 0.0
        if self.mes_fim is not None and mes_atual > self.mes_fim:
            return 0.0
        if mes_atual > (self.mes_aquisicao + self.meses_depreciacao):
            return 0.0
        return self.valor_aquisicao / self.meses_depreciacao

@dataclass
class DespesaAnual:
    """Representa uma despesa paga anualmente mas rateada mensalmente."""
    nome: str
    valor_anual: float
    mes_pagamento: int = 1  # Mês do ano em que é paga
    ativo: bool = True
    mes_inicio: int = 1
    mes_fim: Optional[int] = None
    
    @property
    def valor_mensal_rateado(self) -> float:
        """Retorna o valor mensal para controle."""
        if not self.ativo:
            return 0.0
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
    """
    
    # ... (o resto das flags e seções permanece o mesmo) ...
    # ═════════════════════════════════════════════════════════
    # FLAGS DE ATIVAÇÃO GERAIS
    # ═════════════════════════════════════════════════════════
    ativar_receita_por_usuario: bool = True
    ativar_custo_ia: bool = True
    ativar_impostos: bool = True
    ativar_taxas_pgto: bool = True
    
    # Pessoal
    ativar_fundador: bool = True
    ativar_equipe_clt: bool = True
    ativar_equipe_pj: bool = True
    
    # Operação
    ativar_escritorio: bool = False
    ativar_ferramentas: bool = True
    ativar_servicos_profs: bool = True
    ativar_marketing: bool = True
    ativar_depreciacao: bool = True
    ativar_despesas_anuais: bool = True
    ativar_comissoes_afiliado: bool = False
    
    # Infraestrutura (flags adicionais para testes)
    ativar_infra_tier1: bool = True
    ativar_infra_tier2: bool = True
    ativar_infra_tier3: bool = True
    
    # ═════════════════════════════════════════════════════════
    # 1. CAPITAL E FINANCIAMENTO
    # ═════════════════════════════════════════════════════════
    capital_inicial_caixa: float = 10000.00  # Capital inicial (Bootstrapping/Pré-Seed)
    aporte_mensal_fixo: float = 1800.00
    meses_aporte_fixo: int = 12
    historico_alteracoes: List[Dict[str, Any]] = field(default_factory=list)
    
    # ═════════════════════════════════════════════════════════
    # 2. FUNIL DE AQUISIÇÃO (DETALHADO)
    # ═════════════════════════════════════════════════════════
    visitantes_mes_1: int = 1000
    taxa_crescimento_trafego_mensal: float = 0.20  # 20%
    
    # Conversões Split (para cálculo de CAC por etapa)
    taxa_conversao_visitante_trial: float = 0.05  # 5% visitantes → trial
    taxa_conversao_trial_pagante: float = 0.15  # 15% trial → pagante
    
    # Retenção
    churn_mensal: float = 0.04  # 4% cancelamento/mês
    
    # ═════════════════════════════════════════════════════════
    # 3. MODELO DE RECEITA
    # ═════════════════════════════════════════════════════════
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
    
    # ═════════════════════════════════════════════════════════
    # 4. CUSTOS VARIÁVEIS (COGS)
    # ═════════════════════════════════════════════════════════
    # Custos por usuário
    custo_ia_por_usuario: float = 5.00  # LLM API
    
    # Impostos sobre receita
    aliquota_impostos: float = 0.06  # 6% Simples Nacional
    
    # Taxas de meios de pagamento
    taxa_pagamento_percentual: float = 0.0349  # 3.49% (Stripe/Mercado Pago)
    taxa_pagamento_fixa_por_transacao: float = 0.39  # R$ 0,39 por transação
    
    # Comissões de afiliados (sistema completo)
    comissao_afiliados: Optional[ComissaoAfiliado] = None
    
    # ═════════════════════════════════════════════════════════
    # 5. INFRAESTRUTURA ESCALÁVEL (3 TIERS)
    # ═════════════════════════════════════════════════════════
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
    
    # ═════════════════════════════════════════════════════════
    # 6. MARKETING (2 FASES)
    # ═════════════════════════════════════════════════════════
    # FASE 1: Validação
    marketing_fase1_custo_fixo: float = 500.00
    marketing_fase1_duracao_meses: int = 3
    
    # FASE 2: Reinvestimento
    marketing_fase2_perc_lucro_bruto: float = 0.25  # 25% do lucro bruto
    
    # CAC Meta (para análise)
    cac_pago_meta: float = 500.00
    
    # ═════════════════════════════════════════════════════════
    # 7. SALÁRIO DO FUNDADOR (CONDICIONAL)
    # ═════════════════════════════════════════════════════════
    salario_fundador_valor: float = 5000.00
    salario_fundador_mes_inicio_ideal: int = 6
    salario_fundador_caixa_minimo_seguranca: float = 10000.00
    
    # ═════════════════════════════════════════════════════════
    # 8. EQUIPE E PESSOAL (SISTEMA COMPLETO)
    # ═════════════════════════════════════════════════════════
    equipe: List[Funcionario] = field(default_factory=list)
    
    def adicionar_funcionario(
        self,
        nome: str,
        cargo: str,
        salario_bruto: float,
        mes_inicio: int,
        tipo: str = "CLT",
        ativo: bool = True,
        mes_fim: Optional[int] = None,
        encargos_percentual: float = 0.68
    ):
        """Adiciona um funcionário à equipe."""
        funcionario = Funcionario(
            nome=nome,
            cargo=cargo,
            salario_bruto=salario_bruto,
            mes_inicio=mes_inicio,
            tipo=tipo,
            ativo=ativo,
            mes_fim=mes_fim,
            encargos_percentual=encargos_percentual
        )
        self.equipe.append(funcionario)
    
    # ═════════════════════════════════════════════════════════
    # 9. ESCRITÓRIO E OPERAÇÃO
    # ═════════════════════════════════════════════════════════
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
    
    # ═════════════════════════════════════════════════════════
    # 10. FERRAMENTAS SAAS (CATEGORIZADAS)
    # ═════════════════════════════════════════════════════════
    ferramentas_saas: List[FerramentaSaaS] = field(default_factory=list)
    
    def adicionar_ferramenta(
        self,
        nome: str,
        categoria: CategoriaFerramenta,
        custo_mensal: float,
        mes_inicio: int = 1,
        essencial: bool = True,
        ativa: bool = True,
        mes_fim: Optional[int] = None,
        custo_por_usuario: float = 0.0, # Adicionado para compatibilidade
        provider: str = "" # Adicionado para compatibilidade
    ):
        """Adiciona uma ferramenta SaaS usando a classe unificada."""
        ferramenta = FerramentaSaaS(
            nome=nome,
            categoria=categoria,
            custo_mensal=custo_mensal,
            mes_inicio=mes_inicio,
            essencial=essencial,
            ativa=ativa,
            mes_fim=mes_fim,
            custo_por_usuario=custo_por_usuario,
            provider=provider
        )
        self.ferramentas_saas.append(ferramenta)
    
    # ... (resto do arquivo permanece o mesmo) ...
    # ═════════════════════════════════════════════════════════
    # 11. SERVIÇOS PROFISSIONAIS
    # ═════════════════════════════════════════════════════════
    contabilidade_mensal: float = 0.0
    contabilidade_mes_inicio: int = 1
    
    advogado_retainer_mensal: float = 0.0
    advogado_mes_inicio: int = 999  # 999 = opcional/não usar
    
    consultorias_outras_mensal: float = 0.0
    
    # ═════════════════════════════════════════════════════════
    # 12. DEPRECIAÇÃO DE ATIVOS
    # ═════════════════════════════════════════════════════════
    ativos_depreciaveis: List[AtivoDepreciavel] = field(default_factory=list)
    
    def adicionar_ativo_depreciavel(
        self,
        nome: str,
        valor_aquisicao: float,
        meses_depreciacao: int,
        mes_aquisicao: int = 0,
        ativo: bool = True,
        mes_fim: Optional[int] = None
    ):
        """Adiciona um ativo para depreciação."""
        ativo_obj = AtivoDepreciavel(
            nome=nome,
            valor_aquisicao=valor_aquisicao,
            meses_depreciacao=meses_depreciacao,
            mes_aquisicao=mes_aquisicao,
            ativo=ativo,
            mes_fim=mes_fim
        )
        self.ativos_depreciaveis.append(ativo_obj)
    
    # ═════════════════════════════════════════════════════════
    # 13. DESPESAS ANUAIS RATEADAS
    # ═════════════════════════════════════════════════════════
    despesas_anuais: List[DespesaAnual] = field(default_factory=list)
    
    def adicionar_despesa_anual(
        self,
        nome: str,
        valor_anual: float,
        mes_pagamento: int = 1,
        ativo: bool = True,
        mes_inicio: int = 1,
        mes_fim: Optional[int] = None
    ):
        """Adiciona uma despesa anual (ex: domínio, certificados)."""
        despesa = DespesaAnual(
            nome=nome,
            valor_anual=valor_anual,
            mes_pagamento=mes_pagamento,
            ativo=ativo,
            mes_inicio=mes_inicio,
            mes_fim=mes_fim
        )
        self.despesas_anuais.append(despesa)
    
    # ═════════════════════════════════════════════════════════
    # MÉTODOS DE CÁLCULO
    # ═════════════════════════════════════════════════════════
    
    def registrar_alteracao(
        self,
        descricao: str,
        autor: str = "sistema",
        detalhes: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registra uma alteração na configuração para histórico/auditoria."""
        self.historico_alteracoes.append({
            "timestamp": datetime.utcnow().isoformat(),
            "autor": autor,
            "descricao": descricao,
            "detalhes": detalhes or {}
        })
    
    def aplicar_cenario_e_se(self, **kwargs) -> "ConfigFinanceira":
        """
        Cria um novo cenário a partir do atual, modificando apenas os parâmetros passados.
        """
        novo_config = copy.deepcopy(self)
        
        for chave, valor in kwargs.items():
            if hasattr(novo_config, chave):
                setattr(novo_config, chave, valor)
            else:
                raise AttributeError(f"ConfigFinanceira não tem o atributo '{chave}'")
        
        if kwargs:
            novo_config.registrar_alteracao(
                "Aplicação de cenário 'E se...'",
                detalhes={"alteracoes": kwargs}
            )
        
        return novo_config
    
    def alternar_componente(self, tipo: str, nome: str, ativo: bool) -> str:
        """
        Liga ou desliga qualquer componente (funcionário, ferramenta, etc).
        """
        tipo_normalizado = tipo.lower()
        estado_texto = "ativado" if ativo else "desativado"
        
        if tipo_normalizado == "funcionario":
            for funcionario in self.equipe:
                if funcionario.nome == nome:
                    funcionario.ativo = ativo
                    self.registrar_alteracao(
                        f"Funcionário {estado_texto}",
                        detalhes={"tipo": tipo_normalizado, "nome": nome, "ativo": ativo}
                    )
                    return f"{nome} {estado_texto} com sucesso!"
            raise ValueError(f"Funcionário '{nome}' não encontrado")
        
        if tipo_normalizado == "ferramenta":
            for ferramenta in self.ferramentas_saas:
                if ferramenta.nome == nome:
                    ferramenta.ativa = ativo
                    estado_texto_ferramenta = "ativada" if ativo else "desativada"
                    self.registrar_alteracao(
                        f"Ferramenta {estado_texto_ferramenta}",
                        detalhes={"tipo": tipo_normalizado, "nome": nome, "ativo": ativo}
                    )
                    return f"{nome} {estado_texto_ferramenta} com sucesso!"
            raise ValueError(f"Ferramenta '{nome}' não encontrada")
        
        if tipo_normalizado in {"ativo", "ativo_depreciavel"}:
            for ativo_depreciavel in self.ativos_depreciaveis:
                if ativo_depreciavel.nome == nome:
                    ativo_depreciavel.ativo = ativo
                    self.registrar_alteracao(
                        f"Ativo depreciável {estado_texto}",
                        detalhes={"tipo": tipo_normalizado, "nome": nome, "ativo": ativo}
                    )
                    return f"{nome} {estado_texto} com sucesso!"
            raise ValueError(f"Ativo depreciável '{nome}' não encontrado")
        
        if tipo_normalizado in {"despesa_anual", "despesa"}:
            for despesa in self.despesas_anuais:
                if despesa.nome == nome:
                    despesa.ativo = ativo
                    self.registrar_alteracao(
                        f"Despesa anual {estado_texto}",
                        detalhes={"tipo": tipo_normalizado, "nome": nome, "ativo": ativo}
                    )
                    return f"{nome} {estado_texto} com sucesso!"
            raise ValueError(f"Despesa anual '{nome}' não encontrada")
        
        raise ValueError(f"Tipo de componente '{tipo}' não suportado")
    
    def calcular_ltv(self) -> float:
        """
        Calcula o Lifetime Value (LTV) do cliente.
        """
        receita_liquida = self.arpu_medio * (
            1 - self.aliquota_impostos - self.taxa_pagamento_percentual
        )
        lucro_bruto_por_usuario = receita_liquida - self.custo_ia_por_usuario
        
        if self.churn_mensal == 0:
            return float('inf') # LTV infinito se não há churn
        return lucro_bruto_por_usuario / self.churn_mensal
    
    def calcular_ltv_cac_ratio(self) -> float:
        """Calcula a relação LTV/CAC."""
        ltv = self.calcular_ltv()
        if self.cac_pago_meta == 0:
            return float('inf') if ltv > 0 else 0.0
        return ltv / self.cac_pago_meta
    
    def calcular_cac_payback_meses(self) -> float:
        """
        Calcula o CAC Payback em meses.
        """
        margem_bruta_percentual = (
            1 - self.aliquota_impostos - 
            self.taxa_pagamento_percentual - 
            (self.custo_ia_por_usuario / self.arpu_medio if self.arpu_medio > 0 else 0)
        )
        lucro_bruto_mensal = self.arpu_medio * margem_bruta_percentual
        
        if lucro_bruto_mensal <= 0:
            return float('inf') # Payback infinito se não há lucro
        return self.cac_pago_meta / lucro_bruto_mensal
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário (útil para salvar em JSON)."""
        # ... (implementação omitida para brevidade) ...
        return {}

    def gerar_resumo_config(self) -> str:
        """Gera um resumo textual da configuração."""
        # ... (implementação omitida para brevidade) ...
        return "Resumo da configuração..."


# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES PADRÃO E CENÁRIOS
# ═══════════════════════════════════════════════════════════════

def criar_config_padrao() -> ConfigFinanceira:
    """Cria a configuração padrão do SAM."""
    config = ConfigFinanceira()
    
    config.adicionar_ativo_depreciavel(
        nome="Estação de Trabalho P&D",
        valor_aquisicao=8000.00,
        meses_depreciacao=24,
        mes_aquisicao=0
    )
    
    config.adicionar_ferramenta("GitHub Copilot", CategoriaFerramenta.DEV, 100.00, mes_inicio=1)
    config.adicionar_ferramenta("Cursor IDE", CategoriaFerramenta.DEV, 200.00, mes_inicio=1)
    config.adicionar_ferramenta("Firecrawl", CategoriaFerramenta.DEV, 100.00, mes_inicio=1)
    config.adicionar_ferramenta("Sentry", CategoriaFerramenta.SEGURANCA, 0.00, mes_inicio=1, essencial=True)
    
    config.adicionar_despesa_anual("Domínio .com.br", 40.00, mes_pagamento=1)
    
    return config

def criar_config_com_contratacoes() -> ConfigFinanceira:
    """Cria configuração com contratações planejadas."""
    config = criar_config_padrao()
    
    config.adicionar_funcionario(
        nome="Dev Backend Pleno",
        cargo="Engenheiro de Software",
        salario_bruto=8000.00,
        mes_inicio=12,
        tipo="CLT"
    )
    config.adicionar_funcionario(
        nome="Community Manager",
        cargo="Sucesso do Cliente",
        salario_bruto=4000.00,
        mes_inicio=18,
        tipo="CLT"
    )
    config.adicionar_funcionario(
        nome="Designer UI/UX",
        cargo="Designer",
        salario_bruto=3000.00,
        mes_inicio=6,
        tipo="PJ"
    )
    
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

# ... (resto do arquivo) ...
CONFIG_PADRAO = criar_config_padrao()
CONFIG_COM_CONTRATACOES = criar_config_com_contratacoes()
CONFIG_PESSIMISTA = criar_config_pessimista()
CONFIG_OTIMISTA = criar_config_otimista()

if __name__ == "__main__":
    config = criar_config_com_contratacoes()
    config.adicionar_ferramenta("Notion", CategoriaFerramenta.GESTAO, 50.00, mes_inicio=4)
    print(config.gerar_resumo_config())