"""
core/builders/tools_builder.py - Stack de Ferramentas SaaS
"""

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

    def calcular_custo(self, mes: int, num_usuarios: int = 0) -> float:
        """Calcula o custo da ferramenta para um mês específico."""
        if not self.ativa or mes < self.mes_inicio:
            return 0.0
        if self.mes_fim and mes > self.mes_fim:
            return 0.0
        
        custo_total = self.custo_mensal
        if self.custo_por_usuario > 0:
            custo_total += self.custo_por_usuario * num_usuarios
            
        return custo_total

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

    def calcular_custo_para_mes(self, mes: int, num_usuarios: int = 0) -> float:
        """
        Calcula o custo total de todas as ferramentas para um mês.
        Para retrocompatibilidade, itera sobre a lista de ferramentas no config.
        """
        cfg = self.config
        custo_total = 0.0
        
        if cfg.ativar_ferramentas and hasattr(cfg, 'ferramentas_saas'):
            for tool in cfg.ferramentas_saas:
                # A lógica de cálculo agora está no próprio objeto FerramentaSaaS
                # que já lida com as condições de ativação e custo.
                custo_total += tool.calcular_custo(mes, num_usuarios)

        return custo_total

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

if __name__ == '__main__':
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    from core.config import ConfigFinanceira

    config = ConfigFinanceira()
    config_com_stack = criar_stack_sam(config)

    print("--- Stack de Ferramentas SAM ---")
    total_custo = 0
    for ferramenta in config_com_stack.ferramentas_saas:
        print(f"- {ferramenta.nome} ({ferramenta.categoria.value}): R$ {ferramenta.custo_mensal:.2f}")
        total_custo += ferramenta.custo_mensal
    print(f"Custo Mensal Total: R$ {total_custo:.2f}")
