"""
core/builders/infra_builder.py

Builder para configuração de infraestrutura escalável em tiers.
Baseado na arquitetura SAM: MT5 + AWS + Hostinger.

Tiers:
- Tier 1: Validação (0-100 usuários) - VPS Hostinger + VPS AWS Windows
- Tier 2: Escala (101-500 usuários) - API Cedro + Infra robusta
- Tier 3: Hiperescala (501+ usuários) - Custo por usuário adicional
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TipoComponente(Enum):
    """Tipo de componente de infraestrutura"""
    VPS = "vps"
    API_EXTERNA = "api_externa"
    CDN = "cdn"
    BACKUP = "backup"
    DOMINIO = "dominio"
    MONITORAMENTO = "monitoramento"
    OUTRO = "outro"

@dataclass
class ComponenteInfra:
    """
    Representa um componente de infraestrutura.
    
    Exemplo:
        VPS Principal: R$55/mês (Hostinger KVM 4)
        VPS MT5: R50/mês (AWS t2.small Windows)
    """
    nome: str
    tipo: TipoComponente
    custo_mensal: float
    descricao: str = ""
    provider: str = ""
    specs: Dict[str, str] = field(default_factory=dict)
    ativo: bool = True
    essencial: bool = True
    
    def to_dict(self) -> dict:
        return {
            'nome': self.nome,
            'tipo': self.tipo.value,
            'custo': self.custo_mensal,
            'provider': self.provider,
            'specs': self.specs
        }

@dataclass
class TierInfra:
    """
    Representa um tier de infraestrutura.
    
    Exemplo:
        Tier 1: 0-100 usuários, R$209/mês (VPS Principal + VPS MT5 + Domínio)
    """
    numero: int
    nome: str
    limite_usuarios_min: int
    limite_usuarios_max: int
    componentes: List[ComponenteInfra] = field(default_factory=list)
    custo_fixo_total: float = 0.0
    custo_variavel_por_usuario: float = 0.0
    descricao: str = ""
    
    @property
    def custo_total_componentes(self) -> float:
        """Soma custos de todos os componentes"""
        return sum(c.custo_mensal for c in self.componentes if c.ativo)
    
    def calcular_custo(self, usuarios: int) -> float:
        """
        Calcula custo total para N usuários neste tier.
        
        Args:
            usuarios: Número de usuários ativos
        
        Returns:
            Custo mensal total
        """
        if usuarios < self.limite_usuarios_min:
            return 0.0
        
        custo_base = self.custo_total_componentes or self.custo_fixo_total
        
        if usuarios <= self.limite_usuarios_max:
            return custo_base
        else:
            # Usuários excedentes
            excedente = usuarios - self.limite_usuarios_max
            return custo_base + (excedente * self.custo_variavel_por_usuario)
    
    def to_dict(self) -> dict:
        return {
            'tier': self.numero,
            'nome': self.nome,
            'range': f"{self.limite_usuarios_min}-{self.limite_usuarios_max}",
            'custo_fixo': self.custo_fixo_total or self.custo_total_componentes,
            'custo_variavel': self.custo_variavel_por_usuario,
            'componentes': [c.to_dict() for c in self.componentes]
        }


class InfraBuilder:
    """
    Builder para configurar infraestrutura escalável em tiers.
    """
    
    def __init__(self, config):
        """
        Args:
            config: Instância de ConfigFinanceira
        """
        self.config = config
        self.tiers: List[TierInfra] = []
        self.tier_atual: Optional[TierInfra] = None

    def calcular_custo_para_mes(self, usuarios: int) -> float:
        """
        Calcula o custo de infraestrutura para um mês.
        Para retrocompatibilidade, replica a lógica de 3 tiers do motor antigo.
        """
        cfg = self.config

        # Futuramente, esta lógica usará self.tiers se estiverem definidos.
        # Por enquanto, fallback para a lógica antiga.
        if usuarios <= cfg.infra_tier1_limite:
            return cfg.infra_tier1_custo_fixo if cfg.ativar_infra_tier1 else 0.0
        elif usuarios <= cfg.infra_tier2_limite:
            return cfg.infra_tier2_custo_fixo if cfg.ativar_infra_tier2 else 0.0
        else:
            if not cfg.ativar_infra_tier3:
                return 0.0
            adicionais = max(0, usuarios - cfg.infra_tier2_limite)
            return cfg.infra_tier2_custo_fixo + adicionais * cfg.infra_tier3_custo_por_usuario

    def criar_tier(
        self,
        numero: int,
        nome: str,
        usuarios_min: int,
        usuarios_max: int,
        custo_fixo: float = 0.0,
        custo_por_usuario: float = 0.0,
        descricao: str = ""
    ) -> 'InfraBuilder':
        """
        Cria um novo tier de infraestrutura (fluent interface).
        """
        tier = TierInfra(
            numero=numero,
            nome=nome,
            limite_usuarios_min=usuarios_min,
            limite_usuarios_max=usuarios_max,
            custo_fixo_total=custo_fixo,
            custo_variavel_por_usuario=custo_por_usuario,
            descricao=descricao
        )
        self.tiers.append(tier)
        self.tier_atual = tier
        return self
    
    def add_componente(
        self,
        nome: str,
        tipo: TipoComponente,
        custo_mensal: float,
        descricao: str = "",
        provider: str = "",
        specs: Dict[str, str] = None,
        essencial: bool = True
    ) -> 'InfraBuilder':
        """
        Adiciona componente ao tier atual (fluent interface).
        """
        if not self.tier_atual:
            raise ValueError("Crie um tier antes de adicionar componentes (use criar_tier)")
        
        componente = ComponenteInfra(
            nome=nome,
            tipo=tipo,
            custo_mensal=custo_mensal,
            descricao=descricao,
            provider=provider,
            specs=specs or {},
            essencial=essencial
        )
        self.tier_atual.componentes.append(componente)
        return self
    
    def calcular_custo_para_usuarios(self, usuarios: int) -> tuple:
        """
        Calcula custo de infra para N usuários.
        
        Returns:
            (tier_ativo, custo_mensal)
        """
        for tier in sorted(self.tiers, key=lambda t: t.numero):
            if tier.limite_usuarios_min <= usuarios <= tier.limite_usuarios_max:
                return (tier.numero, tier.calcular_custo(usuarios))
            elif usuarios > tier.limite_usuarios_max:
                # Continua no último tier com custo variável
                if tier == self.tiers[-1]:
                    return (tier.numero, tier.calcular_custo(usuarios))
        
        # Fallback: tier 1
        return (1, self.tiers[0].calcular_custo(usuarios) if self.tiers else 0.0)
    
    def validar(self) -> List[str]:
        """Valida configuração de tiers"""
        erros = []
        
        if not self.tiers:
            erros.append("Nenhum tier configurado")
            return erros
        
        # Valida sobreposição de ranges
        for i, tier1 in enumerate(self.tiers):
            for tier2 in self.tiers[i+1:]:
                if not (tier1.limite_usuarios_max < tier2.limite_usuarios_min or 
                        tier2.limite_usuarios_max < tier1.limite_usuarios_min):
                    erros.append(
                        f"Tier {tier1.numero} e Tier {tier2.numero} têm ranges sobrepostos"
                    )
        
        # Valida gaps
        tiers_ordenados = sorted(self.tiers, key=lambda t: t.limite_usuarios_min)
        for i in range(len(tiers_ordenados) - 1):
            tier_atual = tiers_ordenados[i]
            tier_proximo = tiers_ordenados[i + 1]
            
            if tier_atual.limite_usuarios_max + 1 != tier_proximo.limite_usuarios_min:
                erros.append(
                    f"Gap entre Tier {tier_atual.numero} (até {tier_atual.limite_usuarios_max}) "
                    f"e Tier {tier_proximo.numero} (de {tier_proximo.limite_usuarios_min})"
                )
        
        return erros
    
    def build(self):
        """
        Aplica configuração ao config e retorna.
        """
        # Valida
        erros = self.validar()
        if erros:
            raise ValueError(f"Erros na configuração de infra:\n" + "\n".join(erros))
        
        # Salva tiers no config
        if not hasattr(self.config, 'tiers_infraestrutura'):
            self.config.tiers_infraestrutura = []
        self.config.tiers_infraestrutura = self.tiers
        
        # Atualiza valores legados no config (compatibilidade)
        if len(self.tiers) >= 1:
            tier1 = self.tiers[0]
            self.config.infra_tier1_custo_fixo = tier1.custo_total_componentes or tier1.custo_fixo_total
            self.config.infra_tier1_limite = tier1.limite_usuarios_max
            self.config.infra_tier1_detalhes = {
                c.nome: c.custo_mensal for c in tier1.componentes
            }
        
        if len(self.tiers) >= 2:
            tier2 = self.tiers[1]
            self.config.infra_tier2_custo_fixo = tier2.custo_total_componentes or tier2.custo_fixo_total
            self.config.infra_tier2_limite = tier2.limite_usuarios_max
            self.config.infra_tier2_detalhes = {
                c.nome: c.custo_mensal for c in tier2.componentes
            }
        
        if len(self.tiers) >= 3:
            tier3 = self.tiers[2]
            self.config.infra_tier3_custo_por_usuario = tier3.custo_variavel_por_usuario
        
        # Registra
        self.config.registrar_alteracao(
            "Configuração de infraestrutura em tiers",
            detalhes={
                'num_tiers': len(self.tiers),
                'tiers': [t.to_dict() for t in self.tiers]
            }
        )
        
        return self.config
    
    def gerar_relatorio(self) -> str:
        """Gera relatório textual da configuração"""
        if not self.tiers:
            return "Nenhum tier configurado."
        
        linhas = [
            "═" * 70,
            "CONFIGURAÇÃO DE INFRAESTRUTURA ESCALÁVEL",
            "═" * 70,
            ""
        ]
        
        for tier in sorted(self.tiers, key=lambda t: t.numero):
            linhas.extend([
                f"TIER {tier.numero}: {tier.nome} ({tier.limite_usuarios_min}-{tier.limite_usuarios_max} usuários)",
                "─" * 70
            ])
            
            if tier.componentes:
                for comp in tier.componentes:
                    spec_str = ", ".join(f"{k}: {v}" for k, v in comp.specs.items()) if comp.specs else ""
                    linhas.append(
                        f"  • {comp.nome:30s} R$ {comp.custo_mensal:>8,.2f}/mês  "
                        f"[{comp.provider}] {spec_str}"
                    )
                linhas.append(f"\n  TOTAL FIXO: R$ {tier.custo_total_componentes:,.2f}/mês")
            else:
                linhas.append(f"  Custo Fixo: R$ {tier.custo_fixo_total:,.2f}/mês")
            
            if tier.custo_variavel_por_usuario > 0:
                linhas.append(f"  Custo Variável: R$ {tier.custo_variavel_por_usuario:.2f}/usuário adicional")
            
            linhas.append("")
        
        linhas.append("═" * 70)
        return "\n".join(linhas)


# ============================================================================
# EXEMPLO DE USO - Infraestrutura SAM
# ============================================================================

def criar_infra_sam(config):
    """
    Cria infraestrutura conforme especificação SAM:
    
    Tier 1 (0-100): R$209/mês
        - VPS Principal (Hostinger KVM 4): R$55
        - VPS MT5 (AWS Windows): R50
        - Domínio: R$4
    
    Tier 2 (101-500): R$5.650/mês
        - API Cedro: R$5.000
        - VPS Robusta: R$500
        - Backup S3: R$50
        - CDN Cloudflare: R00
    
    Tier 3 (501+): Tier 2 + R,50/usuário
    """
    builder = InfraBuilder(config)
    
    # ===== TIER 1: Validação (0-100 usuários) =====
    builder.criar_tier(
        numero=1,
        nome="Validação com MT5",
        usuarios_min=0,
        usuarios_max=100,
        descricao="Infraestrutura inicial para MVP e primeiros clientes"
    )
    
    builder.add_componente(
        "VPS Principal (Backend SAM)",
        TipoComponente.VPS,
        55.00,
        descricao="Hostinger KVM 4 - PostgreSQL, Redis, API, Workers",
        provider="Hostinger",
        specs={
            "CPU": "4 vCPU",
            "RAM": "16 GB",
            "Disk": "200 GB NVMe",
            "Bandwidth": "Unlimited"
        },
        essencial=True
    )
    
    builder.add_componente(
        "VPS Coleta MT5 (Windows)",
        TipoComponente.VPS,
        150.00,
        descricao="AWS t2.small - MetaTrader 5 rodando 24/7",
        provider="AWS",
        specs={
            "Instance": "t2.small",
            "OS": "Windows Server",
            "CPU": "1 vCPU",
            "RAM": "2 GB"
        },
        essencial=True
    )
    
    builder.add_componente(
        "Domínio",
        TipoComponente.DOMINIO,
        4.00,
        descricao="Registro.br (.com.br) - R$40/ano diluído",
        provider="Registro.br",
        essencial=True
    )
    
    # ===== TIER 2: Escala (101-500 usuários) =====
    builder.criar_tier(
        numero=2,
        nome="Escala com API Cedro",
        usuarios_min=101,
        usuarios_max=500,
        descricao="Infraestrutura profissional com feed de dados confiável"
    )
    
    builder.add_componente(
        "API Cedro (Feed Profissional)",
        TipoComponente.API_EXTERNA,
        5000.00,
        descricao="API de dados de mercado em tempo real (B3)",
        provider="Cedro",
        specs={"Delay": "Real-time", "Cobertura": "B3 completa"},
        essencial=True
    )
    
    builder.add_componente(
        "VPS Robusta (Upgrade)",
        TipoComponente.VPS,
        500.00,
        descricao="Servidor dedicado ou VPS grande",
        provider="AWS/Hostinger",
        specs={"CPU": "8 vCPU", "RAM": "32 GB", "Disk": "500 GB SSD"},
        essencial=True
    )
    
    builder.add_componente(
        "Backup S3",
        TipoComponente.BACKUP,
        50.00,
        descricao="Armazenamento redundante de dados históricos",
        provider="AWS S3",
        essencial=False
    )
    
    builder.add_componente(
        "CDN Cloudflare Pro",
        TipoComponente.CDN,
        100.00,
        descricao="Aceleração global + proteção DDoS",
        provider="Cloudflare",
        essencial=False
    )
    
    # ===== TIER 3: Hiperescala (501+ usuários) =====
    builder.criar_tier(
        numero=3,
        nome="Hiperescala",
        usuarios_min=501,
        usuarios_max=999999,
        custo_por_usuario=1.50,
        descricao="Custo variável por usuário adicional (cloud elástico)"
    )
    
    # Tier 3 herda componentes do Tier 2 + custo variável
    # (componentes serão os mesmos, mas o engine aplica custo adicional)
    
    return builder.build()


if __name__ == "__main__":
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # Teste do builder
    from core.config import ConfigFinanceira
    
    config = ConfigFinanceira()
    config_atualizado = criar_infra_sam(config)
    
    # Gera relatório
    builder = InfraBuilder(config)
    builder.tiers = config_atualizado.tiers_infraestrutura
    print(builder.gerar_relatorio())
    
    # Testa cálculo de custos
    print("\n" + "="*70)
    print("TESTE DE CUSTOS POR NÚMERO DE USUÁRIOS")
    print("="*70)
    
    for usuarios in [50, 100, 250, 500, 750, 1000]:
        tier, custo = builder.calcular_custo_para_usuarios(usuarios)
        print(f"{usuarios:4d} usuários → Tier {tier} → R$ {custo:>10,.2f}/mês")