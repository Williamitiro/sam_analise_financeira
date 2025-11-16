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
    print(builder.gerar_relatorio()
    )