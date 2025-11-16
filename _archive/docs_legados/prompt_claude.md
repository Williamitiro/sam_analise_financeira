> **Prompt para o Claude:**

"Atue como um Arquiteto de Software Full-Stack Sênior e especialista em UI/UX. Sua missão é analisar a arquitetura do meu backend Python, que está totalmente refatorado e independente, e com base nela, projetar uma arquitetura de frontend profissional e um plano de implementação detalhado para uma nova aplicação React.

Para otimizar o uso do contexto, vamos proceder de forma interativa.

**Fase 1: Contexto Estratégico do Backend**

Abaixo estão as informações críticas do meu projeto. O backend é responsável por todos os cálculos e análises financeiras.

**1. A Estratégia de API:**
O backend expõe sua funcionalidade através de uma única API REST (FastAPI) com um endpoint principal:
*   **`POST /projecao/`**: Este endpoint recebe um objeto JSON contendo todas as configurações da simulação, executa o motor de projeção e a camada de análise (`analytics`), e retorna um JSON completo com todos os resultados (KPIs, projeção mensal, análise de cohorts, insights, etc.).

**2. A Estrutura de Arquivos do Módulo `core/`:**
```
Listagem de caminhos de pasta para o volume Novo volume
O n·mero de sÚrie do volume Ú 5276-DB76
E:\PROJETOS\SAM_ANALISE_FINANCEIRA\CORE
ª   analysis.py
ª   config.py
ª   engine.py
ª   glossary.py
ª   visualizations.py
ª   __init__.py
ª   
+---analytics
ª   ª   cohorts.py
ª   ª   forecasting.py
ª   ª   insights_engine.py
ª   ª   montecarlo.py
ª   ª   sensitivity.py
ª   ª   __init__.py
ª   ª   
ª   +---__pycache__
ª           cohorts.cpython-314.pyc
ª           insights_engine.cpython-312.pyc
ª           insights_engine.cpython-314.pyc
ª           __init__.cpython-312.pyc
ª           __init__.cpython-314.pyc
ª           
+---builders
ª   ª   capital_builder.py
ª   ª   channels_builder.py
ª   ª   cogs_builder.py
ª   ª   ENTREGA.md
ª   ª   infra_builder.py
ª   ª   marketing_builder.py
ª   ª   README.md
ª   ª   revenue_builder.py
ª   ª   risk_builder.py
ª   ª   scenario_builder.py
ª   ª   tax_builder.py
ª   ª   team_builder.py
ª   ª   tools_builder.py
ª   ª   __init__.py
ª   ª   
ª   +---__pycache__
ª           capital_builder.cpython-312.pyc
ª           capital_builder.cpython-314.pyc
ª           channels_builder.cpython-312.pyc
ª           channels_builder.cpython-314.pyc
ª           cogs_builder.cpython-312.pyc
ª           cogs_builder.cpython-314.pyc
ª           infra_builder.cpython-312.pyc
ª           infra_builder.cpython-314.pyc
ª           marketing_builder.cpython-312.pyc
ª           marketing_builder.cpython-314.pyc
ª           revenue_builder.cpython-312.pyc
ª           revenue_builder.cpython-314.pyc
ª           risk_builder.cpython-312.pyc
ª           risk_builder.cpython-314.pyc
ª           scenario_builder.cpython-312.pyc
ª           scenario_builder.cpython-314.pyc
ª           tax_builder.cpython-312.pyc
ª           tax_builder.cpython-314.pyc
ª           team_builder.cpython-312.pyc
ª           team_builder.cpython-314.pyc
ª           tools_builder.cpython-312.pyc
ª           tools_builder.cpython-314.pyc
ª           __init__.cpython-312.pyc
ª           __init__.cpython-314.pyc
ª           
+---risk
ª       alerts.py
ª       contingency.py
ª       risk_scenarios.py
ª       __init__.py
ª       
+---__pycache__
        config.cpython-312.pyc
        config.cpython-314.pyc
        engine.cpython-312.pyc
        engine.cpython-314.pyc
        glossary.cpython-312.pyc
        __init__.cpython-312.pyc
        __init__.cpython-314.pyc
        
```

**3. O Código dos Arquivos Essenciais do Backend:**

**Arquivo: `core/config.py`**
*Este arquivo define o objeto `ConfigFinanceira`, a estrutura de dados central que será enviada como JSON para a API.*
```python
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
defuncionario:
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
    capital_inicial_caixa: float = -8000.00  # Capex inicial (negativo = saída)
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
```

**Arquivo: `core/engine.py`**
*Este é o motor de cálculo principal.*
```python
"""
core/engine.py
Motor de projeção financeira INTEGRADO com Builders.
Versão 4.0 - FINAL e FUNCIONAL

Processa:
- Gatilhos de contratação do TeamBuilder
- Transições de tier do InfraBuilder  
- Fases de marketing do MarketingBuilder
- Canais diferenciados do ChannelsBuilder
- Todas as colunas necessárias para o Dashboard
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np

from .config import ConfigFinanceira


def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    """Divisão segura que retorna um valor padrão em caso de erro ou divisão por zero."""
    try:
        if b == 0 or np.isnan(b) or np.isinf(b):
            return default
        result = a / b
        if np.isnan(result) or np.isinf(result):
            return default
        return result
    except (ZeroDivisionError, TypeError, ValueError):
        return default


class MotorProjecaoFinanceira:
    """
    Motor de projeção mês a mês integrado com builders. 
    
    Uso:
        motor = MotorProjecaoFinanceira(config)
        df = motor.executar_projecao(meses=36)
        kpis = motor.calcular_kpis()
    """

    def __init__(self, config: ConfigFinanceira):
        if not isinstance(config, ConfigFinanceira):
            raise TypeError("config deve ser uma instância de ConfigFinanceira")
        
        self.config = config
        self.projecao_df: Optional[pd.DataFrame] = None
        self.kpis: Optional[Dict[str, Any]] = None
        
        # Log de eventos (para auditoria/insights)
        self.eventos: List[Dict] = []

        # 🔥 NOVO: Importe os builders (só carrega se existirem)
        try:
            from .builders.revenue_builder import RevenueBuilder
            self._revenue_builder = RevenueBuilder(config)
            self._has_revenue_builder = True
        except ImportError:
            self._has_revenue_builder = False
        
        try:
            from .builders.channels_builder import ChannelsBuilder
            self._channels_builder = ChannelsBuilder(config)
            self._has_channels_builder = True
        except ImportError:
            self._has_channels_builder = False
        
        try:
            from .builders.capital_builder import CapitalBuilder
            self._capital_builder = CapitalBuilder(config)
            self._has_capital_builder = True
        except ImportError:
            self._has_capital_builder = False
        
        try:
            from .builders.marketing_builder import MarketingBuilder
            self._marketing_builder = MarketingBuilder(config)
            self._has_marketing_builder = True
        except ImportError:
            self._has_marketing_builder = False

    def _registrar_evento(self, mes: int, tipo: str, descricao: str, valor: float = 0):
        """Registra evento para auditoria"""
        self.eventos.append({
            'mes': mes,
            'tipo': tipo,
            'descricao': descricao,
            'valor': valor
        })

    def _processar_gatilhos_contratacao(self, mes: int, metricas: dict):
        """
        Processa gatilhos de contratação do TeamBuilder.
        
        Args:
            mes: Mês atual
            metricas: Dict com mrr, usuarios, lucro, caixa
        """
        if not hasattr(self.config, 'cargos_planejados'):
            return
        
        for cargo in self.config.cargos_planejados:
            if not cargo.ativo and cargo.avaliar_gatilhos(mes, metricas):
                cargo.contratar(mes)
                self._registrar_evento(
                    mes, 
                    'CONTRATACAO',
                    f"Contratado: {cargo.nome} ({cargo.cargo_funcao})",
                    cargo.salario_base
                )

    def _calcular_tier_infraestrutura(self, usuarios: int) -> tuple:
        """
        Calcula tier de infraestrutura baseado em usuários.
        
        Returns:
            (numero_tier, custo_mensal)
        """
        if not hasattr(self.config, 'tiers_infraestrutura'):
            # Fallback: usa lógica antiga
            if usuarios <= self.config.infra_tier1_limite:
                return (1, self.config.infra_tier1_custo_fixo)
            elif usuarios <= self.config.infra_tier2_limite:
                return (2, self.config.infra_tier2_custo_fixo)
            else:
                excedente = max(0, usuarios - self.config.infra_tier2_limite)
                return (3, self.config.infra_tier2_custo_fixo + excedente * self.config.infra_tier3_custo_por_usuario)
        
        # Usa InfraBuilder
        for tier in sorted(self.config.tiers_infraestrutura, key=lambda t: t.numero):
            if tier.limite_usuarios_min <= usuarios <= tier.limite_usuarios_max:
                return (tier.numero, tier.calcular_custo(usuarios))
            elif usuarios > tier.limite_usuarios_max and tier == self.config.tiers_infraestrutura[-1]:
                return (tier.numero, tier.calcular_custo(usuarios))
        
        return (1, 0.0)

    def _calcular_marketing_fase(self, mes: int, mrr: float, lucro_bruto: float, novos_pagantes: float) -> tuple:
        """
        Calcula custo de marketing baseado na fase ativa.
        
        Returns:
            (fase_numero, custo_mensal)
        """
        if not hasattr(self.config, 'fases_marketing'):
            # Fallback: usa lógica antiga
            if mes <= self.config.marketing_fase1_duracao_meses:
                return (1, self.config.marketing_fase1_custo_fixo)
            else:
                return (2, max(0.0, lucro_bruto * self.config.marketing_fase2_perc_lucro_bruto))
        
        # Usa MarketingBuilder
        for fase in self.config.fases_marketing:
            if fase.mes_inicio <= mes and (fase.mes_fim is None or mes <= fase.mes_fim):
                custo = fase.calcular_orcamento(mrr, lucro_bruto, novos_pagantes)
                return (fase.numero, custo)
        
        return (1, 0.0)

    def _calcular_custos_equipe(self, mes: int, metricas: dict) -> tuple:
        """
        Calcula custos de equipe usando TeamBuilder.
        
        Returns:
            (custo_clt, custo_pj, custo_fundador)
        """
        if not hasattr(self.config, 'cargos_planejados'):
            # Fallback: usa lógica antiga do fundador
            saldo_caixa = metricas.get('caixa', 0)
            inicio_ok = mes >= self.config.salario_fundador_mes_inicio_ideal
            caixa_ok = saldo_caixa > self.config.salario_fundador_caixa_minimo_seguranca
            salario_fundador = self.config.salario_fundador_valor if (inicio_ok and caixa_ok) else 0.0
            return (0.0, 0.0, salario_fundador)
        
        custo_clt = 0.0
        custo_pj = 0.0
        custo_fundador = 0.0
        
        for cargo in self.config.cargos_planejados:
            custo = cargo.calcular_custo_mensal(mes, metricas)
            
            if cargo.tipo.value == 'fundador':
                custo_fundador += custo
            elif cargo.tipo.value == 'clt':
                custo_clt += custo
            elif cargo.tipo.value == 'pj':
                custo_pj += custo
        
        return (custo_clt, custo_pj, custo_fundador)

    def _calcular_custos_ferramentas(self, mes: int, num_usuarios: int = 0) -> float:
        """Calcula custo total de ferramentas SaaS usando o método de cada objeto."""
        if not hasattr(self.config, 'ferramentas_saas') or not self.config.ativar_ferramentas:
            return 0.0
        
        custo_total = 0.0
        for ferramenta in self.config.ferramentas_saas:
            # A lógica de cálculo agora está encapsulada no próprio objeto FerramentaSaaS
            custo_total += ferramenta.calcular_custo(mes, num_usuarios)

        return custo_total

    def executar_projecao(self, meses: int = 36) -> pd.DataFrame:
        """
        Executa a projeção financeira mês a mês com integração total dos builders.
        
        Gera TODAS as colunas necessárias para o dashboard.
        """
        cfg = self.config
        
        # Define TODAS as colunas que o dashboard espera
        colunas = [
            # Identificação
            'mes',
            
            # Funil de Aquisição
            'Usuarios_Iniciais', 'Visitantes', 'Novos_Trials', 'Novos_Pagantes',
            'Usuarios_Perdidos', 'Usuarios_Finais',
            
            # Taxas de Conversão (para análise)
            'Taxa_Conv_Trial', 'Taxa_Conv_Pagante', 'Taxa_Conv_Geral',
            
            # Receita
            'MRR', 'ARR', 'ARPU',
            
            # COGS Detalhado
            'Custo_IA', 'Impostos', 'Taxas_Pagamento', 'Comissoes_Afiliados', 'COGS_Total',
            
            # Margens
            'Lucro_Bruto', 'Margem_Bruta_Pct',
            
            # OPEX Detalhado
            'Custo_Infra', 'Tier_Infra',
            'Custo_Marketing', 'Fase_Marketing',
            'Salario_Fundador', 'Custo_Pessoal_CLT', 'Custo_Pessoal_PJ',
            'Custo_Escritorio', 'Custo_Ferramentas', 'Custo_Servicos_Profissionais',
            'Custo_Depreciacao', 'Custo_Despesas_Anuais',
            'OPEX_Total',
            
            # Resultado
            'EBITDA', 'Resultado_Operacional',
            
            # Fluxo de Caixa
            'Aportes', 'Fluxo_Caixa', 'Saldo_Caixa',
            
            # Métricas de Análise
            'CAC_Mensal', 'LTV', 'LTV_CAC_Ratio', 'Payback_Meses',
            
            # Receita Detalhada (para tabelas)
            'Receita_Total', 'Churn_Absoluto'
        ]
        
        registros = []
        
        # Inicializações
        saldo_caixa = float(cfg.capital_inicial_caixa or 0.0)
        visitantes = float(cfg.visitantes_mes_1 or 0.0)
        usuarios = 0.0
        acum_novos_pagantes = 0.0
        acum_marketing = 0.0
        tier_atual = 1
        fase_marketing_atual = 1
        
        # Loop principal
        for mes in range(1, meses + 1):
            
            # ============================================================ 
            # AQUISIÇÃO E RETENÇÃO
            # ============================================================ 
            
            if mes > 1:
                visitantes *= (1 + cfg.taxa_crescimento_trafego_mensal)
            
            # Usa taxas médias dos canais (se configurado)
            taxa_conv_trial = cfg.taxa_conversao_visitante_trial
            taxa_conv_pagante = cfg.taxa_conversao_trial_pagante
            
            novos_trials = visitantes * taxa_conv_trial
            novos_pagantes = novos_trials * taxa_conv_pagante
            taxa_conv_geral = taxa_conv_trial * taxa_conv_pagante
            
            usuarios_iniciais = usuarios
            usuarios_perdidos = usuarios * cfg.churn_mensal
            usuarios = max(0.0, usuarios + novos_pagantes - usuarios_perdidos)
            
            # ============================================================ 
            # RECEITA
            # ============================================================ 
            
            arpu = cfg.arpu_medio
            mrr = usuarios * arpu
            arr = mrr * 12
            receita_total = mrr  # Pode incluir receita não-recorrente no futuro
            
            # ============================================================ 
            # COGS DETALHADO
            # ============================================================ 
            
            custo_ia = usuarios * cfg.custo_ia_por_usuario if cfg.ativar_custo_ia else 0.0
            impostos = mrr * cfg.aliquota_impostos if cfg.ativar_impostos else 0.0
            
            taxas_pagamento = 0.0
            if cfg.ativar_taxas_pgto:
                taxas_pagamento = (novos_pagantes * cfg.taxa_pagamento_fixa_por_transacao) + \
                                 (mrr * cfg.taxa_pagamento_percentual)
            
            comissoes_afiliados = 0.0
            if cfg.ativar_comissoes_afiliado and hasattr(cfg, 'comissao_afiliados') and cfg.comissao_afiliados:
                if mes >= cfg.comissao_afiliados.mes_inicio_programa:
                    comissoes_afiliados = mrr * cfg.comissao_afiliados.percentual_sobre_venda * \
                                         cfg.comissao_afiliados.percentual_vendas_via_afiliados
            
            cogs_total = custo_ia + impostos + taxas_pagamento + comissoes_afiliados
            lucro_bruto = mrr - cogs_total
            margem_bruta_pct = _safe_div(lucro_bruto, mrr, 0.0)
            
            # ============================================================ 
            # MÉTRICAS PARA GATILHOS
            # ============================================================ 
            
            metricas = {
                'mrr': mrr,
                'usuarios': usuarios,
                'lucro': lucro_bruto,
                'caixa': saldo_caixa,
                'mes': mes
            }
            
            # ============================================================ 
            # GATILHOS DE CONTRATAÇÃO
            # ============================================================ 
            
            self._processar_gatilhos_contratacao(mes, metricas)
            
            # ============================================================ 
            # OPEX DETALHADO
            # ============================================================ 
            
            # Infraestrutura (com transição de tier)
            tier_atual, custo_infra = self._calcular_tier_infraestrutura(int(usuarios))
            
            # Marketing (com fases)
            fase_marketing_atual, custo_marketing = self._calcular_marketing_fase(
                mes, mrr, lucro_bruto, novos_pagantes
            )
            
            # Equipe (com gatilhos)
            custo_clt, custo_pj, salario_fundador = self._calcular_custos_equipe(mes, metricas)
            
            # Ferramentas
            custo_ferramentas = self._calcular_custos_ferramentas(mes, int(usuarios))
            
            # Escritório
            custo_escritorio = 0.0
            if cfg.ativar_escritorio and mes >= cfg.escritorio_mes_inicio:
                custo_escritorio = cfg.escritorio_custo_total_mensal
            
            # Serviços Profissionais
            custo_servicos = 0.0
            if cfg.ativar_servicos_profs:
                if mes >= cfg.contabilidade_mes_inicio:
                    custo_servicos += cfg.contabilidade_mensal
                if mes >= cfg.advogado_mes_inicio:
                    custo_servicos += cfg.advogado_retainer_mensal
                custo_servicos += cfg.consultorias_outras_mensal
            
            # Depreciação
            custo_depreciacao = 0.0
            if cfg.ativar_depreciacao:
                for ativo in cfg.ativos_depreciaveis:
                    custo_depreciacao += ativo.calcular_depreciacao_mensal(mes)
            
            # Despesas Anuais
            custo_despesas_anuais = 0.0
            if cfg.ativar_despesas_anuais:
                for desp in cfg.despesas_anuais:
                    if desp.ativo and mes >= desp.mes_inicio:
                        if desp.mes_fim is None or mes <= desp.mes_fim:
                            custo_despesas_anuais += desp.valor_mensal_rateado
            
            opex_total = (
                custo_infra + custo_marketing + salario_fundador \
                + custo_clt + custo_pj + custo_escritorio \
                + custo_ferramentas + custo_servicos \
                + custo_depreciacao + custo_despesas_anuais
            )
            
            # ============================================================ 
            # RESULTADO E FLUXO DE CAIXA
            # ============================================================ 
            
            ebitda = lucro_bruto - opex_total
            resultado_operacional = ebitda - custo_depreciacao
            
            # Aportes
            aporte = cfg.aporte_mensal_fixo if mes <= cfg.meses_aporte_fixo else 0.0
            
            fluxo_caixa = resultado_operacional + aporte
            saldo_caixa += fluxo_caixa
            
            # ============================================================ 
            # MÉTRICAS DE ANÁLISE
            # ============================================================ 
            
            cac_mensal = _safe_div(custo_marketing, novos_pagantes, np.nan)
            ltv = cfg.calcular_ltv()
            ltv_cac_ratio = _safe_div(ltv, cac_mensal, np.nan)
            payback_meses = _safe_div(cac_mensal, (lucro_bruto / usuarios if usuarios > 0 else 0), np.nan)
            
            acum_novos_pagantes += novos_pagantes
            acum_marketing += custo_marketing
            
            # ============================================================ 
            # REGISTRO DO MÊS
            # ============================================================ 
            
            registros.append({
                'mes': mes,
                'Usuarios_Iniciais': round(usuarios_iniciais, 2),
                'Visitantes': round(visitantes, 0),
                'Novos_Trials': round(novos_trials, 2),
                'Novos_Pagantes': round(novos_pagantes, 2),
                'Usuarios_Perdidos': round(usuarios_perdidos, 2),
                'Usuarios_Finais': round(usuarios, 2),
                'Taxa_Conv_Trial': round(taxa_conv_trial * 100, 2),
                'Taxa_Conv_Pagante': round(taxa_conv_pagante * 100, 2),
                'Taxa_Conv_Geral': round(taxa_conv_geral * 100, 2),
                'MRR': round(mrr, 2),
                'ARR': round(arr, 2),
                'ARPU': round(arpu, 2),
                'Custo_IA': round(custo_ia, 2),
                'Impostos': round(impostos, 2),
                'Taxas_Pagamento': round(taxas_pagamento, 2),
                'Comissoes_Afiliados': round(comissoes_afiliados, 2),
                'COGS_Total': round(cogs_total, 2),
                'Lucro_Bruto': round(lucro_bruto, 2),
                'Margem_Bruta_Pct': round(margem_bruta_pct * 100, 2),
                'Custo_Infra': round(custo_infra, 2),
                'Tier_Infra': tier_atual,
                'Custo_Marketing': round(custo_marketing, 2),
                'Fase_Marketing': fase_marketing_atual,
                'Salario_Fundador': round(salario_fundador, 2),
                'Custo_Pessoal_CLT': round(custo_clt, 2),
                'Custo_Pessoal_PJ': round(custo_pj, 2),
                'Custo_Escritorio': round(custo_escritorio, 2),
                'Custo_Ferramentas': round(custo_ferramentas, 2),
                'Custo_Servicos_Profissionais': round(custo_servicos, 2),
                'Custo_Depreciacao': round(custo_depreciacao, 2),
                'Custo_Despesas_Anuais': round(custo_despesas_anuais, 2),
                'OPEX_Total': round(opex_total, 2),
                'EBITDA': round(ebitda, 2),
                'Resultado_Operacional': round(resultado_operacional, 2),
                'Aportes': round(aporte, 2),
                'Fluxo_Caixa': round(fluxo_caixa, 2),
                'Saldo_Caixa': round(saldo_caixa, 2),
                'CAC_Mensal': round(cac_mensal, 2) if not np.isnan(cac_mensal) else np.nan,
                'LTV': round(ltv, 2),
                'LTV_CAC_Ratio': round(ltv_cac_ratio, 2) if not np.isnan(ltv_cac_ratio) else np.nan,
                'Payback_Meses': round(payback_meses, 2) if not np.isnan(payback_meses) else np.nan,
                'Receita_Total': round(receita_total, 2),
                'Churn_Absoluto': round(usuarios_perdidos, 2)
            })
        
        # ============================================================ 
        # FINALIZAÇÃO
        # ============================================================ 
        
        df = pd.DataFrame.from_records(registros, columns=colunas)
        df.fillna(value=np.nan, inplace=True)

        # ===== PASSO 2: RevenueBuilder (SEMPRE PRIMEIRO) =====
        # Gera MRR_Lite, MRR_Trader, MRR_Pro, Waterfall
        if self._has_revenue_builder and hasattr(self.config, 'receita'):
            if self.config.receita.get('planos'):
                print("🔧 Aplicando RevenueBuilder...")
                df = self._revenue_builder.gerar_series_temporais(df)
                print(f"   ✅ {len(self.config.receita['planos'])} planos processados")
            else:
                print("⚠️ RevenueBuilder configurado mas sem planos")
        
        # ===== PASSO 3: MarketingBuilder (SE EXISTIR) =====
        # Gera orçamento de marketing para CAC real
        if self._has_marketing_builder:
            print("🔧 Aplicando MarketingBuilder...")
            orcamento_mensal = []
            for mes_iter in range(1, meses + 1):
                # Usa seu método existente
                custo = self._marketing_builder.calcular_custo_para_mes(
                    mes=mes_iter,
                    lucro_bruto=df.loc[mes_iter-1, 'Lucro_Bruto']
                )
                orcamento_mensal.append(custo)
            
            # Salva no DataFrame
            df['Custo_Marketing_Total'] = orcamento_mensal
            print(f"   ✅ Orçamento de marketing calculado")
        
        # ===== PASSO 4: ChannelsBuilder (APÓS MARKETING) =====
        # Gera funil de conversão usando orçamento real
        if self._has_channels_builder and hasattr(self.config, 'canais_aquisicao'):
            if self.config.canais_aquisicao:
                print("🔧 Aplicando ChannelsBuilder...")
                
                # Pegar orçamento do marketing se disponível
                orcamento_series = None
                if 'Custo_Marketing_Total' in df.columns:
                    orcamento_series = df['Custo_Marketing_Total']
                
                df = self._channels_builder.gerar_series_temporais(
                    df,
                    orcamento_mensal=orcamento_series
                )
                print(f"   ✅ {len(self.config.canais_aquisicao)} canais processados")
        
        # ===== PASSO 5: CapitalBuilder (SEMPRE POR ÚLTIMO) =====
        # Gera runway e milestones com todos os dados disponíveis
        if self._has_capital_builder:
            print("🔧 Aplicando CapitalBuilder...")
            df = self._capital_builder.gerar_series_temporais(df)
            print("   ✅ Runway e milestones calculados")
            
        self.projecao_df = df
        
        return df

    def calcular_kpis(self) -> Dict[str, Any]:
        """
        Calcula os KPIs principais a partir do DataFrame de projeção.
        """
        if self.projecao_df is None:
            raise RuntimeError("Execute executar_projecao() antes de calcular_kpis()")
        
        df = self.projecao_df.copy()
        kpis = {}

        # Break-even
        be_df = df[df['Resultado_Operacional'] > 0]
        kpis['Break_Even_Mes'] = int(be_df.iloc[0]['mes']) if not be_df.empty else None

        # Payback
        capital_inicial = abs(self.config.capital_inicial_caixa or 0.0)
        pb_df = df[df['Saldo_Caixa'] > capital_inicial]
        kpis['Payback_Investimento_Mes'] = int(pb_df.iloc[0]['mes']) if not pb_df.empty else None

        # Vale da Morte
        if not df.empty:
            kpis['Vale_da_Morte_Minimo_Caixa'] = float(df['Saldo_Caixa'].min())
            kpis['Vale_da_Morte_Mes'] = int(df.loc[df['Saldo_Caixa'].idxmin(), 'mes'])
        else:
            kpis['Vale_da_Morte_Minimo_Caixa'] = 0.0
            kpis['Vale_da_Morte_Mes'] = 0

        # Runway
        negativo_df = df[df['Saldo_Caixa'] < 0]
        if not negativo_df.empty:
            kpis['Runway_Meses'] = int(negativo_df.iloc[0]['mes'] - 1)
        else:
            kpis['Runway_Meses'] = f">= {len(df)}"

        # Unit Economics
        kpis['LTV_Final'] = float(self.config.calcular_ltv())
        total_marketing = df['Custo_Marketing'].sum()
        total_novos = df['Novos_Pagantes'].sum()
        kpis['CAC_Medio_Periodo'] = float(_safe_div(total_marketing, total_novos, np.nan))
        kpis['LTV_CAC_Ratio_Final'] = float(_safe_div(kpis['LTV_Final'], kpis['CAC_Medio_Periodo'], np.nan))
        kpis['CAC_Payback_Meses_Config'] = float(self.config.calcular_cac_payback_meses())

        # Snapshots Anuais
        for ano in [1, 2, 3]:
            mes_final_ano = ano * 12
            if len(df) >= mes_final_ano:
                kpis[f'MRR_Ano{ano}'] = float(df.iloc[mes_final_ano - 1]['MRR'])
                kpis[f'Usuarios_Ano{ano}'] = float(df.iloc[mes_final_ano - 1]['Usuarios_Finais'])

        kpis['Saldo_Caixa_Final'] = float(df.iloc[-1]['Saldo_Caixa']) if not df.empty else 0.0
        kpis['MRR_Final'] = float(df.iloc[-1]['MRR']) if not df.empty else 0.0
        kpis['Usuarios_Final'] = float(df.iloc[-1]['Usuarios_Finais']) if not df.empty else 0.0
        
        # Eventos de auditoria
        kpis['eventos'] = self.eventos
        
        self.kpis = kpis
        return kpis

    def obter_eventos_mes(self, mes: int) -> List[Dict]:
        """Retorna eventos que ocorreram em um mês específico"""
        return [e for e in self.eventos if e['mes'] == mes]

    def verificar_builders_ativos(self) -> dict:
        """
        Retorna status dos builders para o dashboard
        """
        return {
            'RevenueBuilder': self._has_revenue_builder and hasattr(self.config, 'receita') and self.config.receita.get('planos'),
            'ChannelsBuilder': self._has_channels_builder and hasattr(self.config, 'canais_aquisicao'),
            'CapitalBuilder': self._has_capital_builder,
            'MarketingBuilder': self._has_marketing_builder,
        }


# Função procedural para retrocompatibilidade
def gerar_projecao_financeira(premissas: Dict[str, Any], meses: int = 36) -> pd.DataFrame:
    """
    Função procedural para retrocompatibilidade.
    """
    cfg = ConfigFinanceira()
    for k, v in premissas.items():
        if hasattr(cfg, k):
            try:
                setattr(cfg, k, v)
            except Exception:
                pass
    
    motor = MotorProjecaoFinanceira(cfg)
    df = motor.executar_projecao(meses=meses)
    return df
```

**Arquivo Exemplo de Builder: `core/builders/team_builder.py`**
*Este arquivo é um bom exemplo de como a lógica de negócio é encapsulada.*
```python
"""
core/builders/team_builder.py

Builder para planejamento de equipe com gatilhos de contratação.
Suporta: CLT, PJ, fundador, sócios, pró-labore, reajustes, benefícios.

Funcionalidades:
- Gatilhos automáticos de contratação (MRR, usuários, mês, lucro)
- Salário em fases (fundador começa com R$0, depois R$3k, depois R$8k)
- Pró-labore condicional (% do lucro quando atingir meta)
- Reajustes anuais programados
- Benefícios configuráveis (VR, VT, Plano Saúde)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple
from enum import Enum

class TipoGatilho(Enum):
    """Tipo de gatilho de contratação"""
    MRR = "mrr"  # Quando MRR > valor
    USUARIOS = "usuarios"  # Quando usuários > valor
    MES = "mes"  # No mês específico
    LUCRO = "lucro"  # Quando lucro > valor
    CAIXA = "caixa"  # Quando caixa > valor

class TipoPessoa(Enum):
    """Tipo de pessoa na empresa"""
    FUNDADOR = "fundador"
    CLT = "clt"
    PJ = "pj"
    SOCIO_INVESTIDOR = "socio_investidor"
    ESTAGIARIO = "estagiario"

@dataclass
class GatilhoContratacao:
    """
    Gatilho que dispara contratação automática. 
    
    Exemplos:
        - Contratar quando MRR > R$50.000
        - Contratar quando usuários > 500
        - Contratar no mês 12
        - Contratar quando lucro > R0.000
    """
    tipo: TipoGatilho
    valor: float
    operador: str = ">="  # ">=", ">", "==", "<", "<="
    
    def avaliar(self, valor_atual: float) -> bool:
        """Verifica se gatilho foi atingido"""
        if self.operador == ">=":
            return valor_atual >= self.valor
        elif self.operador == ">":
            return valor_atual > self.valor
        elif self.operador == "==":
            return valor_atual == self.valor
        elif self.operador == "<":
            return valor_atual < self.valor
        elif self.operador == "<=":
            return valor_atual <= self.valor
        return False
    
    def __str__(self) -> str:
        tipo_label = {
            TipoGatilho.MRR: "MRR",
            TipoGatilho.USUARIOS: "usuários",
            TipoGatilho.MES: "mês",
            TipoGatilho.LUCRO: "lucro",
            TipoGatilho.CAIXA: "caixa"
        }
        return f"{tipo_label[self.tipo]} {self.operador} {self.valor:,.0f}"

@dataclass
class FaseSalarial:
    """
    Representa uma fase de remuneração (ex: fundador). 
    
    Exemplo:
        Fase 1 (mês 1-6): R$0
        Fase 2 (mês 7-12): R$3.000
        Fase 3 (mês 13+): R$8.000 quando MRR > R$30k
    """
    mes_inicio: int
    mes_fim: Optional[int]
    salario: float
    gatilhos: List[GatilhoContratacao] = field(default_factory=list)
    
    def esta_ativa(self, mes_atual: int, metricas: dict) -> bool:
        """Verifica se fase está ativa no mês atual"""
        # Verifica período
        if mes_atual < self.mes_inicio:
            return False
        if self.mes_fim and mes_atual > self.mes_fim:
            return False
        
        # Verifica gatilhos (TODOS devem estar satisfeitos)
        for gatilho in self.gatilhos:
            valor_atual = metricas.get(gatilho.tipo.value, 0)
            if not gatilho.avaliar(valor_atual):
                return False
        
        return True

@dataclass
class Beneficios:
    """Benefícios mensais do funcionário"""
    vale_refeicao: float = 0.0
    vale_transporte: float = 0.0
    plano_saude: float = 0.0
    auxilio_home_office: float = 0.0
    outros: float = 0.0
    
    @property
    def total(self) -> float:
        return (self.vale_refeicao + self.vale_transporte + 
                self.plano_saude + self.auxilio_home_office + self.outros)

@dataclass
class ProLabore:
    """Configuração de pró-labore (% do lucro)"""
    percentual_lucro: float  # Ex: 0.10 = 10% do lucro
    gatilhos: List[GatilhoContratacao] = field(default_factory=list)
    limite_minimo: float = 0.0  # Pró-labore mínimo
    limite_maximo: Optional[float] = None  # Pró-labore máximo
    
    def calcular(self, lucro_mensal: float, metricas: dict) -> float:
        """Calcula pró-labore baseado no lucro"""
        # Verifica gatilhos
        for gatilho in self.gatilhos:
            valor_atual = metricas.get(gatilho.tipo.value, 0)
            if not gatilho.avaliar(valor_atual):
                return 0.0
        
        if lucro_mensal <= 0:
            return 0.0
        
        valor = lucro_mensal * self.percentual_lucro
        
        # Aplica limites
        if valor < self.limite_minimo:
            valor = self.limite_minimo
        if self.limite_maximo and valor > self.limite_maximo:
            valor = self.limite_maximo
        
        return valor

@dataclass
class Cargo:
    """
    Representa um cargo/pessoa na empresa. 
    
    Suporta:
    - CLT/PJ com salário fixo
    - Fundador com fases salariais
    - Sócio com pró-labore
    - Gatilhos de contratação
    - Reajustes anuais
    - Benefícios
    """
    nome: str
    cargo_funcao: str
    tipo: TipoPessoa
    salario_base: float = 0.0
    encargos_percentual: float = 0.68  # 68% para CLT
    
    # Contratação
    gatilhos_contratacao: List[GatilhoContratacao] = field(default_factory=list)
    mes_contratacao_manual: Optional[int] = None  # Se não usar gatilhos
    mes_demissao: Optional[int] = None
    
    # Fases salariais (para fundador)
    fases_salariais: List[FaseSalarial] = field(default_factory=list)
    
    # Pró-labore (para sócios)
    pro_labore: Optional[ProLabore] = None
    
    # Reajustes
    reajuste_anual_percentual: float = 0.08  # 8% ao ano
    mes_primeiro_reajuste: int = 13  # Após 1 ano
    
    # Benefícios
    beneficios: Beneficios = field(default_factory=Beneficios)
    
    # Participação societária (informativo)
    equity_percentual: float = 0.0
    
    # Estado
    ativo: bool = False
    mes_inicio_real: Optional[int] = None
    
    def calcular_custo_mensal(
        self,
        mes_atual: int,
        metricas: dict
    ) -> float:
        """
        Calcula custo total no mês (salário + encargos + benefícios + pró-labore). 
        
        Args:
            mes_atual: Mês da simulação
            metricas: Dict com MRR, usuários, lucro, caixa, etc.
        
        Returns:
            Custo total mensal
        """
        if not self.ativo:
            return 0.0
        
        if self.mes_inicio_real is None or mes_atual < self.mes_inicio_real:
            return 0.0
        
        if self.mes_demissao and mes_atual > self.mes_demissao:
            return 0.0
        
        # Calcula salário base (considerando fases)
        salario = self._calcular_salario_fase(mes_atual, metricas)
        
        # Aplica reajustes
        salario = self._aplicar_reajustes(salario, mes_atual)
        
        # Calcula custo com encargos
        if self.tipo == TipoPessoa.CLT:
            custo_salario = salario * (1 + self.encargos_percentual)
        else:  # PJ, Fundador, etc
            custo_salario = salario
        
        # Adiciona benefícios
        custo_beneficios = self.beneficios.total
        
        # Adiciona pró-labore (se houver)
        custo_pro_labore = 0.0
        if self.pro_labore:
            lucro = metricas.get('lucro', 0.0)
            custo_pro_labore = self.pro_labore.calcular(lucro, metricas)
        
        return custo_salario + custo_beneficios + custo_pro_labore
    
    def _calcular_salario_fase(self, mes_atual: int, metricas: dict) -> float:
        """Calcula salário considerando fases (fundador)"""
        if not self.fases_salariais:
            return self.salario_base
        
        # Procura fase ativa
        for fase in self.fases_salariais:
            if fase.esta_ativa(mes_atual, metricas):
                return fase.salario
        
        # Fallback: salário base
        return self.salario_base
    
    def _aplicar_reajustes(self, salario: float, mes_atual: int) -> float:
        """Aplica reajustes anuais"""
        if not self.mes_inicio_real:
            return salario
        
        if mes_atual < self.mes_primeiro_reajuste:
            return salario
        
        # Calcula quantos reajustes já ocorreram
        meses_desde_inicio = mes_atual - self.mes_inicio_real
        anos_completos = meses_desde_inicio // 12
        
        if anos_completos == 0:
            return salario
        
        # Aplica reajuste composto
        return salario * ((1 + self.reajuste_anual_percentual) ** anos_completos)
    
    def avaliar_gatilhos(self, mes_atual: int, metricas: dict) -> bool:
        """Verifica se deve ser contratado neste mês"""
        if self.ativo:
            return False
        
        # Contratação manual
        if self.mes_contratacao_manual and mes_atual >= self.mes_contratacao_manual:
            return True
        
        # Gatilhos automáticos (QUALQUER um satisfeito = contratar)
        for gatilho in self.gatilhos_contratacao:
            valor_atual = metricas.get(gatilho.tipo.value, 0)
            if gatilho.avaliar(valor_atual):
                return True
        
        return False
    
    def contratar(self, mes: int):
        """Marca como contratado"""
        self.ativo = True
        self.mes_inicio_real = mes
    
    def demitir(self, mes: int):
        """Marca como demitido"""
        self.ativo = False
        self.mes_demissao = mes


class TeamBuilder:
    """
    Builder para planejamento de equipe com gatilhos.
    """
    
    def __init__(self, config):
        self.config = config
        self.cargos: List[Cargo] = []
        self.cargo_atual: Optional[Cargo] = None
        
        # Inicializa os cargos a partir do config para o cálculo
        if hasattr(config, 'cargos_planejados'):
            self.cargos = config.cargos_planejados
        elif hasattr(config, 'equipe'):
            # Lógica de compatibilidade com a estrutura antiga pode ser adicionada aqui se necessário
            pass

    def calcular_custo_para_mes(self, mes: int, mrr: float, usuarios: float, saldo_caixa: float) -> Tuple[float, float, float]:
        """
        Calcula o custo total de pessoal para um mês, gerenciando contratações.
        Retorna (custo_clt, custo_pj, salario_fundador).
        """
        cfg = self.config
        
        # Fallback para a lógica antiga se a nova estrutura não for usada
        if not hasattr(cfg, 'cargos_planejados') or not cfg.cargos_planejados:
            salario_fundador = 0.0
            if cfg.ativar_fundador:
                inicio_ok = mes >= cfg.salario_fundador_mes_inicio_ideal
                caixa_ok = saldo_caixa > cfg.salario_fundador_caixa_minimo_seguranca
                if inicio_ok and caixa_ok:
                    salario_fundador = cfg.salario_fundador_valor

            custo_clt = 0.0
            custo_pj = 0.0
            if hasattr(cfg, 'equipe') and (cfg.ativar_equipe_clt or cfg.ativar_equipe_pj):
                for f in cfg.equipe:
                    custo = f.calcular_custo_mensal(mes) # Assume que o método antigo existe
                    if f.tipo.upper() == "CLT":
                        custo_clt += custo
                    else:
                        custo_pj += custo
            return custo_clt, custo_pj, salario_fundador

        # Nova lógica usando a estrutura de Cargos
        custo_clt_total = 0.0
        custo_pj_total = 0.0
        salario_fundador_total = 0.0
        
        metricas_atuais = {
            'mrr': mrr,
            'usuarios': usuarios,
            'mes': mes,
            'caixa': saldo_caixa,
            # 'lucro' precisaria ser passado se usado em gatilhos
        }

        for cargo in self.cargos:
            # Avalia se o cargo deve ser contratado neste mês
            if not cargo.ativo and cargo.avaliar_gatilhos(mes, metricas_atuais):
                cargo.contratar(mes)
            
            # Se o cargo estiver ativo no mês, calcula seu custo
            if cargo.ativo:
                custo_cargo = cargo.calcular_custo_mensal(mes, metricas_atuais)
                if cargo.tipo == TipoPessoa.CLT:
                    custo_clt_total += custo_cargo
                elif cargo.tipo == TipoPessoa.PJ:
                    custo_pj_total += custo_cargo
                elif cargo.tipo == TipoPessoa.FUNDADOR:
                    salario_fundador_total += custo_cargo
        
        return custo_clt_total, custo_pj_total, salario_fundador_total

    def add_fundador(
        self,
        nome: str,
        cargo: str,
        equity: float = 0.0
    ) -> 'TeamBuilder':
        """Adiciona fundador (fluent interface)"""
        pessoa = Cargo(
            nome=nome,
            cargo_funcao=cargo,
            tipo=TipoPessoa.FUNDADOR,
            equity_percentual=equity,
            ativo=True,  # Fundador sempre ativo desde o início
            mes_inicio_real=1
        )
        self.cargos.append(pessoa)
        self.cargo_atual = pessoa
        return self
    
    def add_clt(
        self,
        nome: str,
        cargo: str,
        salario: float,
        encargos_pct: float = 0.68
    ) -> 'TeamBuilder':
        """Adiciona funcionário CLT"""
        pessoa = Cargo(
            nome=nome,
            cargo_funcao=cargo,
            tipo=TipoPessoa.CLT,
            salario_base=salario,
            encargos_percentual=encargos_pct
        )
        self.cargos.append(pessoa)
        self.cargo_atual = pessoa
        return self
    
    def add_pj(
        self,
        nome: str,
        cargo: str,
        valor_mensal: float
    ) -> 'TeamBuilder':
        """Adiciona prestador PJ"""
        pessoa = Cargo(
            nome=nome,
            cargo_funcao=cargo,
            tipo=TipoPessoa.PJ,
            salario_base=valor_mensal,
            encargos_percentual=0.0
        )
        self.cargos.append(pessoa)
        self.cargo_atual = pessoa
        return self
    
    def add_socio_investidor(
        self,
        nome: str,
        equity: float,
        aporte: float = 0.0,
        mes_aporte: int = 1
    ) -> 'TeamBuilder':
        """Adiciona sócio investidor"""
        pessoa = Cargo(
            nome=nome,
            cargo_funcao="Sócio Investidor",
            tipo=TipoPessoa.SOCIO_INVESTIDOR,
            equity_percentual=equity,
            ativo=True,
            mes_inicio_real=mes_aporte
        )
        self.cargos.append(pessoa)
        self.cargo_atual = pessoa
        
        # Registra aporte no config (se houver módulo de capital)
        # TODO: integrar com CapitalBuilder
        
        return self
    
    # ========== Fases Salariais (Fundador) ========== 
    
    def fase_sem_salario(self, mes_inicio: int, mes_fim: int) -> 'TeamBuilder':
        """Fase sem salário"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        fase = FaseSalarial(
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            salario=0.0
        )
        self.cargo_atual.fases_salariais.append(fase)
        return self
    
    def fase_salario_minimo(
        self,
        mes_inicio: int,
        mes_fim: Optional[int],
        salario: float
    ) -> 'TeamBuilder':
        """Fase com salário mínimo"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        fase = FaseSalarial(
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            salario=salario
        )
        self.cargo_atual.fases_salariais.append(fase)
        return self
    
    def fase_salario_pleno(
        self,
        mes_inicio: int,
        mes_fim: Optional[int],
        salario: float,
        gatilho_mrr: Optional[float] = None,
        gatilho_lucro: Optional[float] = None
    ) -> 'TeamBuilder':
        """Fase com salário pleno (condicional)"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        fase = FaseSalarial(
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            salario=salario
        )
        
        # Adiciona gatilhos opcionais
        if gatilho_mrr:
            fase.gatilhos.append(GatilhoContratacao(TipoGatilho.MRR, gatilho_mrr))
        if gatilho_lucro:
            fase.gatilhos.append(GatilhoContratacao(TipoGatilho.LUCRO, gatilho_lucro))
        
        self.cargo_atual.fases_salariais.append(fase)
        return self
    
    # ========== Pró-Labore ========== 
    
    def com_pro_labore(
        self,
        percentual: float,
        gatilho_lucro: Optional[float] = None,
        gatilho_mrr: Optional[float] = None,
        minimo: float = 0.0,
        maximo: Optional[float] = None
    ) -> 'TeamBuilder':
        """Adiciona pró-labore ao cargo atual"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        pro_labore = ProLabore(
            percentual_lucro=percentual,
            limite_minimo=minimo,
            limite_maximo=maximo
        )
        
        if gatilho_lucro:
            pro_labore.gatilhos.append(GatilhoContratacao(TipoGatilho.LUCRO, gatilho_lucro))
        if gatilho_mrr:
            pro_labore.gatilhos.append(GatilhoContratacao(TipoGatilho.MRR, gatilho_mrr))
        
        self.cargo_atual.pro_labore = pro_labore
        return self
    
    # ========== Gatilhos de Contratação ========== 
    
    def quando_mrr_atingir(self, valor: float) -> 'TeamBuilder':
        """Contratar quando MRR atingir valor"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        gatilho = GatilhoContratacao(TipoGatilho.MRR, valor)
        self.cargo_atual.gatilhos_contratacao.append(gatilho)
        return self
    
    def quando_usuarios_atingir(self, valor: float) -> 'TeamBuilder':
        """Contratar quando usuários atingir valor"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        gatilho = GatilhoContratacao(TipoGatilho.USUARIOS, valor)
        self.cargo_atual.gatilhos_contratacao.append(gatilho)
        return self
    
    def no_mes(self, mes: int) -> 'TeamBuilder':
        """Contratar em mês específico"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        self.cargo_atual.mes_contratacao_manual = mes
        return self
    
    def quando_lucro_atingir(self, valor: float) -> 'TeamBuilder':
        """Contratar quando lucro atingir valor"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        gatilho = GatilhoContratacao(TipoGatilho.LUCRO, valor)
        self.cargo_atual.gatilhos_contratacao.append(gatilho)
        return self
    
    # ========== Benefícios ========== 
    
    def com_beneficios(
        self,
        vr: float = 0.0,
        vt: float = 0.0,
        plano: float = 0.0,
        home_office: float = 0.0,
        outros: float = 0.0
    ) -> 'TeamBuilder':
        """Adiciona benefícios"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        self.cargo_atual.beneficios = Beneficios(
            vale_refeicao=vr,
            vale_transporte=vt,
            plano_saude=plano,
            auxilio_home_office=home_office,
            outros=outros
        )
        return self
    
    # ========== Reajustes ========== 
    
    def com_reajuste_anual(
        self,
        percentual: float,
        primeiro_reajuste_mes: int = 13
    ) -> 'TeamBuilder':
        """Configura reajuste anual"""
        if not self.cargo_atual:
            raise ValueError("Adicione um cargo antes")
        
        self.cargo_atual.reajuste_anual_percentual = percentual
        self.cargo_atual.mes_primeiro_reajuste = primeiro_reajuste_mes
        return self
    
    # ========== Build ========== 
    
    def build(self):
        """Aplica ao config e retorna"""
        # Salva cargos no config
        if not hasattr(self.config, 'cargos_planejados'):
            self.config.cargos_planejados = []
        self.config.cargos_planejados = self.cargos
        
        # Registra
        self.config.registrar_alteracao(
            "Planejamento de equipe",
            detalhes={
                'num_cargos': len(self.cargos),
                'tipos': [c.tipo.value for c in self.cargos]
            }
        )
        
        return self.config
    
    def gerar_relatorio(self) -> str:
        """Gera relatório de planejamento de equipe"""
        if not self.cargos:
            return "Nenhum cargo configurado."
        
        linhas = [
            "═" * 70,
            "PLANEJAMENTO DE EQUIPE",
            "═" * 70,
            ""
        ]
        
        for cargo in self.cargos:
            linhas.append(f"👤 {cargo.nome} - {cargo.cargo_funcao} ({cargo.tipo.value.upper()})")
            
            if cargo.tipo == TipoPessoa.FUNDADOR and cargo.fases_salariais:
                linhas.append("   Fases Salariais:")
                for fase in cargo.fases_salariais:
                    mes_fim_str = f"até {fase.mes_fim}" if fase.mes_fim else "em diante"
                    gatilhos_str = ", ".join(str(g) for g in fase.gatilhos) if fase.gatilhos else "sem condições"
                    linhas.append(
                        f"     • Mês {fase.mes_inicio} {mes_fim_str}: "
                        f"R$ {fase.salario:,.2f} ({gatilhos_str})"
                    )
                
                if cargo.pro_labore:
                    linhas.append(
                        f"   Pró-labore: {cargo.pro_labore.percentual_lucro*100:.1f}% do lucro "
                        f"(após {', '.join(str(g) for g in cargo.pro_labore.gatilhos)})"
                    )
            
            else:
                linhas.append(f"   Salário Base: R$ {cargo.salario_base:,.2f}")
                
                if cargo.gatilhos_contratacao:
                    linhas.append("   Contratar quando:")
                    for gatilho in cargo.gatilhos_contratacao:
                        linhas.append(f"     • {gatilho}")
                
                elif cargo.mes_contratacao_manual:
                    linhas.append(f"   Contratação: Mês {cargo.mes_contratacao_manual}")
                
                if cargo.tipo == TipoPessoa.CLT:
                    linhas.append(f"   Encargos: {cargo.encargos_percentual*100:.0f}%")
                
                if cargo.beneficios.total > 0:
                    linhas.append(f"   Benefícios: R$ {cargo.beneficios.total:,.2f}/mês")
            
            if cargo.equity_percentual > 0:
                linhas.append(f"   Equity: {cargo.equity_percentual*100:.1f}%")
            
            linhas.append("")
        
        linhas.append("═" * 70)
        return "\n".join(linhas)


# ============================================================================ 
# EXEMPLO DE USO - Equipe SAM
# ============================================================================ 

def criar_equipe_sam(config) -> 'TeamBuilder':
    """
    Cria planejamento de equipe conforme especificação SAM.
    """
    builder = TeamBuilder(config)
    
    # ===== FUNDADOR / CEO =====
    builder.add_fundador("Fundador", "CEO/CTO", equity=0.70) \
        .fase_sem_salario(1, 6) \
        .fase_salario_minimo(7, 12, 3000) \
        .fase_salario_pleno(13, None, 8000, gatilho_mrr=30000) \
        .com_pro_labore(0.10, gatilho_lucro=10000, minimo=1000, maximo=20000)
    
    # ===== DEV BACKEND (contratar quando escalar) =====
    builder.add_clt("Dev Backend Pleno", "Engenheiro de Software", 8000) \
        .quando_mrr_atingir(50000) \
        .com_beneficios(vr=500, vt=300, plano=400) \
        .com_reajuste_anual(0.08)
    
    # ===== COMMUNITY MANAGER (contratar quando tiver base) =====
    builder.add_clt("Community Manager", "Sucesso do Cliente", 5000) \
        .quando_usuarios_atingir(1000) \
        .com_beneficios(vr=500, vt=300, plano=300) \
        .com_reajuste_anual(0.08)
    
    # ===== DESIGNER PJ (contratar cedo, freelancer) =====
    builder.add_pj("Designer UI/UX", "Designer", 3000) \
        .no_mes(6)
    
    # ===== CFO (contratar quando tiver tração significativa) =====
    builder.add_clt("CFO", "Chief Financial Officer", 12000) \
        .quando_mrr_atingir(200000) \
        .com_beneficios(vr=800, plano=800) \
        .com_reajuste_anual(0.10)
    
    return builder


if __name__ == "__main__":
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    from core.config import ConfigFinanceira
    
    config = ConfigFinanceira()
    config_atualizado = criar_equipe_sam(config)
    
    builder = TeamBuilder(config)
    builder.cargos = config_atualizado.cargos_planejados
    print(builder.gerar_relatorio())
```

**Arquivo Exemplo de Análise: `core/analytics/cohorts.py`**
*Este arquivo é um bom exemplo da camada de análise que processa os resultados da projeção.*
```python
# DENTRO DE: core/analytics/cohorts.py
import pandas as pd
import numpy as np

def gerar_cohort_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Gera matriz de cohorts (otimizada)"""
    try:
        meses = df['mes'].unique()[:12]
        cohort_data = []
        
        for i, mes_cohort in enumerate(meses):
            linha = {'Cohort': f"Mês {mes_cohort}"}
            usuarios_cohort = df[df['mes'] == mes_cohort]['Novos_Pagantes'].iloc[0]
            
            if usuarios_cohort <= 0:
                continue
            
            for idade in range(0, min(12, len(meses) - i)):
                mes_futuro = mes_cohort + idade
                if mes_futuro in df['mes'].values:
                    try:
                        # Busca o cohort específico (aproximação)
                        df_cohort = df[df['mes'] == mes_futuro]
                        if not df_cohort.empty:
                            # Aproximação: assume que os usuários remanescentes incluem o cohort
                            total_remanescente = df_cohort['Usuarios_Finais'].iloc[0]
                            cohort_original = sum(df[(df['mes'] == mes_cohort)]['Novos_Pagantes'])
                            
                            if cohort_original > 0:
                                retencao = min(100, (total_remanescente / cohort_original) * 100)
                                linha[f"M{idade}"] = retencao
                            else:
                                linha[f"M{idade}"] = None
                        else:
                            linha[f"M{idade}"] = None
                    except:
                        linha[f"M{idade}"] = None
                else:
                    linha[f"M{idade}"] = None
            
            cohort_data.append(linha)
        
        df_cohorts = pd.DataFrame(cohort_data) if cohort_data else pd.DataFrame()
        return df_cohorts.fillna(0)
    except Exception as e:
        print(f"Erro ao gerar cohorts: {e}") # Usar print para debugging, não st.error
        return pd.DataFrame()
```

---

**Sua Primeira Tarefa: A Proposta de Arquitetura de Frontend**

Com base em sua análise do backend e sabendo que o frontend será uma aplicação **React + TypeScript com Vite e estilização via Tailwind CSS**, apresente uma **Proposta de Arquitetura de Frontend**. A proposta deve detalhar:

1.  **Arquitetura de Componentes:** Descreva como você quebraria a UI em uma hierarquia de componentes React reutilizáveis. Pense nas duas páginas principais que precisamos: a **Página de Configuração** (onde o usuário insere os dados) e a **Página de Resultados** (onde os gráficos e KPIs são exibidos). Proponha uma estrutura de pastas para esses componentes (ex: `src/components/inputs`, `src/components/charts`, `src/pages`).

2.  **Estratégia de Gerenciamento de Estado:** A página de configuração terá um formulário complexo com muitos campos. Qual é a melhor estratégia para gerenciar o estado deste formulário? Recomende uma biblioteca (como `React Hook Form`, `Zustand`, `Redux Toolkit`) e justifique sua escolha para este caso de uso específico.

3.  **Estratégia de Comunicação com a API (Data Fetching):** Qual a melhor abordagem para o frontend se comunicar com nossa API FastAPI? Recomende uma biblioteca ou hook (como `React Query/TanStack Query`, `SWR`, ou o `fetch` nativo com `useEffect`) para lidar com o envio dos dados da simulação e o recebimento dos resultados, gerenciando estados de loading, erro e sucesso.

4.  **Biblioteca de Gráficos:** Com base nos tipos de análise (Waterfall, Cohorts, etc.), qual biblioteca de gráficos para JavaScript/React você recomenda (`Plotly.js`, `Chart.js`, `D3.js`, etc.)? Justifique em termos de poder de visualização e facilidade de integração com React.

**Próximo Passo:**

Após eu aprovar sua proposta de arquitetura, sua segunda tarefa será gerar um **Plano de Implementação Detalhado e Sequencial**. Este plano será uma série de prompts que usarei para guiar uma IA de codificação na construção da aplicação, seguindo a arquitetura que você definiu.

Por favor, comece com a Proposta de Arquitetura."