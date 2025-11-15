"""
core/builders/scenario_builder.py

Orquestrador que combina todos os builders para criar cenários completos.
Permite salvar, carregar e comparar cenários.
"""

import json
import copy
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable

class ScenarioBuilder:
    """
    Orquestrador de cenários completos.
    
    Combina múltiplos builders para criar configurações completas e nomeadas.
    Suporta save/load de cenários em JSON.
    
    Uso:
        # Criar cenário do zero
        scenario = ScenarioBuilder("SAM - Cenário Base")
        scenario.usar_canais(criar_estrategia_sam_canais)
        scenario.usar_infra(criar_infra_sam)
        scenario.usar_equipe(criar_equipe_sam)
        scenario.usar_tools(criar_stack_sam)
        scenario.configurar_receita(
            planos=[("Lite", 70, 0.5), ("Trader", 105, 0.3), ("Pro", 159, 0.2)]
        )
        config = scenario.build()
        scenario.salvar("cenarios/sam_base.json")
        
        # Carregar cenário
        scenario_loaded = ScenarioBuilder.carregar("cenarios/sam_base.json")
        config = scenario_loaded.build()
    """
    
    def __init__(self, nome: str, descricao: str = ""):
        """
        Args:
            nome: Nome do cenário
            descricao: Descrição do cenário
        """
        from core.config import ConfigFinanceira
        self.config = ConfigFinanceira()
        self.nome = nome
        self.descricao = descricao
        self.builders_aplicados = []
        self.metadata = {
            'criado_em': datetime.now().isoformat(),
            'versao': '4.0'
        }
    
    # ========================================================================
    # APLICAÇÃO DE BUILDERS
    # ========================================================================
    
    def usar_canais(self, func_builder: Callable) -> 'ScenarioBuilder':
        """
        Aplica builder de canais.
        
        Args:
            func_builder: Função que recebe config e retorna config atualizado
                         Ex: criar_estrategia_sam_canais(config)
        """
        func_builder(self.config)
        self.builders_aplicados.append("channels")
        return self
    
    def usar_infra(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de infraestrutura"""
        func_builder(self.config)
        self.builders_aplicados.append("infra")
        return self
    
    def usar_equipe(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de equipe"""
        func_builder(self.config)
        self.builders_aplicados.append("team")
        return self
    
    def usar_tools(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de ferramentas"""
        func_builder(self.config)
        self.builders_aplicados.append("tools")
        return self
    
    def usar_marketing(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de marketing"""
        func_builder(self.config)
        self.builders_aplicados.append("marketing")
        return self
    
    def usar_cogs(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de COGS"""
        func_builder(self.config)
        self.builders_aplicados.append("cogs")
        return self
    
    def usar_capital(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de capital"""
        func_builder(self.config)
        self.builders_aplicados.append("capital")
        return self
    
    def usar_riscos(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de riscos"""
        func_builder(self.config)
        self.builders_aplicados.append("risk")
        return self
    
    def usar_impostos(self, func_builder: Callable) -> 'ScenarioBuilder':
        """Aplica builder de impostos"""
        func_builder(self.config)
        self.builders_aplicados.append("tax")
        return self
    
    # ========================================================================
    # CONFIGURAÇÕES RÁPIDAS (SEM BUILDER)
    # ========================================================================
    
    def configurar_receita(
        self,
        planos: list,  # [(nome, preco, mix), ...]
        arpu_override: Optional[float] = None
    ) -> 'ScenarioBuilder':
        """
        Configuração rápida de receita sem usar builder.
        
        Args:
            planos: Lista de tuplas (nome, preço, mix)
                   Ex: [("Lite", 70, 0.5), ("Trader", 105, 0.3), ("Pro", 159, 0.2)]
            arpu_override: ARPU manual (ignora mix de planos)
        """
        if len(planos) >= 1:
            self.config.preco_plano_lite = planos[0][1]
            self.config.mix_plano_lite = planos[0][2]
        if len(planos) >= 2:
            self.config.preco_plano_trader = planos[1][1]
            self.config.mix_plano_trader = planos[1][2]
        if len(planos) >= 3:
            self.config.preco_plano_pro = planos[2][1]
            self.config.mix_plano_pro = planos[2][2]
        
        if arpu_override:
            self.config.arpu_medio_override = arpu_override
        
        return self
    
    def configurar_funil(
        self,
        visitantes_mes_1: int,
        crescimento_mensal: float,
        conv_trial: float,
        conv_pagante: float,
        churn: float
    ) -> 'ScenarioBuilder':
        """
        Configuração rápida do funil de aquisição.
        
        Args:
            visitantes_mes_1: Visitantes no mês 1
            crescimento_mensal: Taxa de crescimento (0.20 = 20%)
            conv_trial: Conversão visitante → trial (0.05 = 5%)
            conv_pagante: Conversão trial → pagante (0.15 = 15%)
            churn: Churn mensal (0.04 = 4%)
        """
        self.config.visitantes_mes_1 = visitantes_mes_1
        self.config.taxa_crescimento_trafego_mensal = crescimento_mensal
        self.config.taxa_conversao_visitante_trial = conv_trial
        self.config.taxa_conversao_trial_pagante = conv_pagante
        self.config.churn_mensal = churn
        return self
    
    def configurar_capital_basico(
        self,
        capex_inicial: float,
        aporte_mensal: float = 0.0,
        meses_aporte: int = 0
    ) -> 'ScenarioBuilder':
        """
        Configuração básica de capital.
        
        Args:
            capex_inicial: Investimento inicial (negativo = saída)
            aporte_mensal: Aporte mensal recorrente
            meses_aporte: Por quantos meses
        """
        self.config.capital_inicial_caixa = -abs(capex_inicial)
        self.config.aporte_mensal_fixo = aporte_mensal
        self.config.meses_aporte_fixo = meses_aporte
        return self
    
    # ========================================================================
    # VARIAÇÕES DE CENÁRIO
    # ========================================================================
    
    def criar_variacao(
        self,
        nome_variacao: str,
        modificacoes: Dict[str, Any]
    ) -> 'ScenarioBuilder':
        """
        Cria variação deste cenário modificando parâmetros específicos.
        
        Args:
            nome_variacao: Sufixo para o nome (ex: "Otimista")
            modificacoes: Dict com atributos a modificar
                         Ex: {'churn_mensal': 0.02, 'taxa_crescimento_trafego_mensal': 0.30}
        
        Returns:
            Novo ScenarioBuilder com as modificações
        """
        # Clona o cenário atual
        novo_scenario = copy.deepcopy(self)
        novo_scenario.nome = f"{self.nome} - {nome_variacao}"
        novo_scenario.descricao = f"Variação {nome_variacao} de {self.nome}"
        novo_scenario.metadata['variacao_de'] = self.nome
        novo_scenario.metadata['modificacoes'] = modificacoes
        
        # Aplica modificações
        for attr, valor in modificacoes.items():
            if hasattr(novo_scenario.config, attr):
                setattr(novo_scenario.config, attr, valor)
            else:
                print(f"Aviso: atributo '{attr}' não existe em ConfigFinanceira")
        
        return novo_scenario
    
    def criar_pessimista(self) -> 'ScenarioBuilder':
        """Cria variação pessimista automática"""
        return self.criar_variacao("Pessimista", {
            'taxa_crescimento_trafego_mensal': self.config.taxa_crescimento_trafego_mensal * 0.5,
            'churn_mensal': self.config.churn_mensal * 1.5,
            'taxa_conversao_trial_pagante': self.config.taxa_conversao_trial_pagante * 0.8,
            'cac_pago_meta': self.config.cac_pago_meta * 1.3
        })
    
    def criar_otimista(self) -> 'ScenarioBuilder':
        """Cria variação otimista automática"""
        return self.criar_variacao("Otimista", {
            'taxa_crescimento_trafego_mensal': self.config.taxa_crescimento_trafego_mensal * 1.5,
            'churn_mensal': self.config.churn_mensal * 0.7,
            'taxa_conversao_trial_pagante': self.config.taxa_conversao_trial_pagante * 1.3,
            'cac_pago_meta': self.config.cac_pago_meta * 0.8
        })
    
    # ========================================================================
    # BUILD E FINALIZAÇÃO
    # ========================================================================
    
    def build(self):
        """
        Finaliza o cenário e retorna a configuração.
        
        Returns:
            ConfigFinanceira completa e validada
        """
        self.config.nome_cenario = self.nome
        self.config.descricao_cenario = self.descricao
        
        # Registra a criação do cenário
        self.config.registrar_alteracao(
            f"Cenário '{self.nome}' criado",
            detalhes={
                'builders_aplicados': self.builders_aplicados,
                'metadata': self.metadata
            }
        )
        
        return self.config
    
    # ========================================================================
    # PERSISTÊNCIA (SAVE/LOAD)
    # ========================================================================
    
    def salvar(self, caminho: str):
        """
        Salva cenário em arquivo JSON.
        
        Args:
            caminho: Caminho do arquivo (ex: "data/scenarios/sam_base.json")
        """
        # Cria diretório se não existir
        path = Path(caminho)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepara dados para serialização
        dados = {
            'nome': self.nome,
            'descricao': self.descricao,
            'metadata': self.metadata,
            'builders_aplicados': self.builders_aplicados,
            'config': self.config.to_dict()
        }
        
        # Salva
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Cenário '{self.nome}' salvo em {caminho}")
    
    @staticmethod
    def carregar(caminho: str) -> 'ScenarioBuilder':
        """
        Carrega cenário de arquivo JSON.
        
        Args:
            caminho: Caminho do arquivo
        
        Returns:
            ScenarioBuilder reconstruído
        """
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Reconstrói ScenarioBuilder
        scenario = ScenarioBuilder(dados['nome'], dados.get('descricao', ''))
        scenario.metadata = dados.get('metadata', {})
        scenario.builders_aplicados = dados.get('builders_aplicados', [])
        
        # Reconstrói ConfigFinanceira
        from core.config import ConfigFinanceira
        scenario.config = ConfigFinanceira()
        
        # Aplica dados do dict ao config
        config_dict = dados['config']
        for key, value in config_dict.items():
            if hasattr(scenario.config, key):
                try:
                    setattr(scenario.config, key, value)
                except Exception as e:
                    print(f"Aviso: não foi possível restaurar '{key}': {e}")
        
        print(f"✅ Cenário '{scenario.nome}' carregado de {caminho}")
        return scenario
    
    def gerar_relatorio(self) -> str:
        """Gera relatório textual do cenário"""
        linhas = [
            "═" * 70,
            f"CENÁRIO: {self.nome}",
            "═" * 70,
            "",
            f"Descrição: {self.descricao or 'N/A'}",
            f"Criado em: {self.metadata.get('criado_em', 'N/A')}",
            f"Versão: {self.metadata.get('versao', 'N/A')}",
            "",
            "Builders Aplicados:",
        ]
        
        if self.builders_aplicados:
            for builder in self.builders_aplicados:
                linhas.append(f"  ✓ {builder}")
        else:
            linhas.append("  (nenhum)")
        
        linhas.extend([
            "",
            "Parâmetros Principais:",
            f"  • Visitantes Mês 1: {self.config.visitantes_mes_1:,}",
            f"  • Crescimento Tráfego: {self.config.taxa_crescimento_trafego_mensal*100:.1f}%/mês",
            f"  • Churn: {self.config.churn_mensal*100:.1f}%/mês",
            f"  • ARPU Médio: R$ {self.config.arpu_medio:.2f}",
            f"  • CAC Meta: R$ {self.config.cac_pago_meta:.2f}",
            f"  • LTV: R$ {self.config.calcular_ltv():.2f}",
            f"  • LTV/CAC: {self.config.calcular_ltv_cac_ratio():.2f}x",
            "",
            "═" * 70
        ])
        
        return "\n".join(linhas)


# ============================================================================
# GERENCIADOR DE CENÁRIOS
# ============================================================================

class GerenciadorCenarios:
    """
    Gerencia múltiplos cenários (carregar, comparar, listar).
    
    Uso:
        gerenciador = GerenciadorCenarios("data/scenarios")
        gerenciador.salvar_cenario(scenario_base)
        gerenciador.salvar_cenario(scenario_pessimista)
        
        cenarios = gerenciador.listar_cenarios()
        
        scenario = gerenciador.carregar_cenario("sam_base")
        
        comparacao = gerenciador.comparar_cenarios(["sam_base", "sam_pessimista"])
    """
    
    def __init__(self, diretorio: str = "data/scenarios"):
        """
        Args:
            diretorio: Diretório onde cenários são salvos
        """
        self.diretorio = Path(diretorio)
        self.diretorio.mkdir(parents=True, exist_ok=True)
    
    def salvar_cenario(self, scenario: ScenarioBuilder) -> str:
        """
        Salva cenário no diretório gerenciado.
        
        Returns:
            Caminho do arquivo salvo
        """
        # Gera nome de arquivo seguro
        nome_arquivo = scenario.nome.lower().replace(" ", "_").replace("-", "_")
        nome_arquivo = "".join(c for c in nome_arquivo if c.isalnum() or c == "_")
        caminho = self.diretorio / f"{nome_arquivo}.json"
        
        scenario.salvar(str(caminho))
        return str(caminho)
    
    def carregar_cenario(self, nome_ou_arquivo: str) -> ScenarioBuilder:
        """
        Carrega cenário por nome ou caminho.
        
        Args:
            nome_ou_arquivo: Nome do cenário ou caminho completo
        """
        # Tenta como caminho direto
        path = Path(nome_ou_arquivo)
        if path.exists():
            return ScenarioBuilder.carregar(str(path))
        
        # Tenta no diretório gerenciado
        nome_arquivo = nome_ou_arquivo.lower().replace(" ", "_") + ".json"
        path = self.diretorio / nome_arquivo
        if path.exists():
            return ScenarioBuilder.carregar(str(path))
        
        # Tenta sem extensão
        path = self.diretorio / f"{nome_ou_arquivo}.json"
        if path.exists():
            return ScenarioBuilder.carregar(str(path))
        
        raise FileNotFoundError(f"Cenário '{nome_ou_arquivo}' não encontrado em {self.diretorio}")
    
    def listar_cenarios(self) -> list:
        """
        Lista todos os cenários salvos.
        
        Returns:
            Lista de dicts com informações dos cenários
        """
        cenarios = []
        
        for arquivo in self.diretorio.glob("*.json"):
            try:
                scenario = ScenarioBuilder.carregar(str(arquivo))
                cenarios.append({
                    'nome': scenario.nome,
                    'arquivo': arquivo.name,
                    'descricao': scenario.descricao,
                    'criado_em': scenario.metadata.get('criado_em'),
                    'builders': scenario.builders_aplicados
                })
            except Exception as e:
                print(f"Erro ao carregar {arquivo.name}: {e}")
        
        return sorted(cenarios, key=lambda x: x['criado_em'] or '', reverse=True)
    
    def comparar_cenarios(self, nomes: list) -> Dict[str, Any]:
        """
        Compara múltiplos cenários lado a lado.
        
        Args:
            nomes: Lista de nomes de cenários
        
        Returns:
            Dict com comparação de métricas principais
        """
        cenarios_carregados = []
        
        for nome in nomes:
            try:
                scenario = self.carregar_cenario(nome)
                cenarios_carregados.append(scenario)
            except Exception as e:
                print(f"Erro ao carregar '{nome}': {e}")
        
        if not cenarios_carregados:
            return {}
        
        # Compara métricas principais
        comparacao = {
            'cenarios': [s.nome for s in cenarios_carregados],
            'metricas': {}
        }
        
        metricas_comparar = [
            'visitantes_mes_1',
            'taxa_crescimento_trafego_mensal',
            'churn_mensal',
            'taxa_conversao_trial_pagante',
            'arpu_medio',
            'cac_pago_meta'
        ]
        
        for metrica in metricas_comparar:
            comparacao['metricas'][metrica] = []
            for scenario in cenarios_carregados:
                valor = getattr(scenario.config, metrica, None)
                if callable(valor):
                    valor = valor()
                comparacao['metricas'][metrica].append(valor)
        
        # Calcula métricas derivadas
        comparacao['ltv'] = [s.config.calcular_ltv() for s in cenarios_carregados]
        comparacao['ltv_cac'] = [s.config.calcular_ltv_cac_ratio() for s in cenarios_carregados]
        
        return comparacao
    
    def imprimir_comparacao(self, nomes: list):
        """Imprime comparação formatada"""
        comp = self.comparar_cenarios(nomes)
        
        if not comp:
            print("Nenhum cenário válido para comparar")
            return
        
        print("\n" + "═" * 70)
        print("COMPARAÇÃO DE CENÁRIOS")
        print("═" * 70 + "\n")
        
        # Header
        header = f"{'Métrica':<30s}"
        for nome in comp['cenarios']:
            header += f" | {nome:<20s}"
        print(header)
        print("─" * 70)
        
        # Métricas
        for metrica, valores in comp['metricas'].items():
            linha = f"{metrica:<30s}"
            for valor in valores:
                if isinstance(valor, float):
                    if valor < 1:
                        linha += f" | {valor*100:>18.2f}%"
                    else:
                        linha += f" | {valor:>20,.2f}"
                else:
                    linha += f" | {valor:>20}"
            print(linha)
        
        # LTV e LTV/CAC
        linha_ltv = f"{'LTV':<30s}"
        for ltv in comp['ltv']:
            linha_ltv += f" | R$ {ltv:>17,.2f}"
        print(linha_ltv)
        
        linha_ratio = f"{'LTV/CAC Ratio':<30s}"
        for ratio in comp['ltv_cac']:
            linha_ratio += f" | {ratio:>18.2f}x"
        print(linha_ratio)
        
        print("\n" + "═" * 70)


# ============================================================================
# EXEMPLO DE USO COMPLETO
# ============================================================================

if __name__ == "__main__":
    # Adiciona o diretório raiz do projeto ao sys.path para permitir importações diretas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    from core.config import ConfigFinanceira
    
    # Importa funções de builders (assumindo que existem)
    try:
        from core.builders.channels_builder import criar_estrategia_sam_canais
        from core.builders.infra_builder import criar_infra_sam
        from core.builders.team_builder import criar_equipe_sam
        # O tools_builder ainda não foi separado, então a função pode não existir
        # from core.builders.tools_builder import criar_stack_sam
        
        # Solução temporária: definir uma função dummy se a importação falhar
        def criar_stack_sam(config):
            print("Aviso: Usando dummy 'criar_stack_sam'. Separe o tools_builder.py.")
            return config

    except ImportError as e:
        print(f"Aviso: alguns builders não foram encontrados ({e}). Usando configuração básica.")
        criar_estrategia_sam_canais = lambda c: c
        criar_infra_sam = lambda c: c
        criar_equipe_sam = lambda c: c
        criar_stack_sam = lambda c: c
    
    # ===== CRIAR CENÁRIO BASE =====
    print("Criando cenário SAM Base...")
    scenario_base = ScenarioBuilder(
        "SAM - Cenário Base",
        "Projeção realista baseada em premissas conservadoras"
    )
    
    scenario_base \
        .configurar_capital_basico(capex_inicial=8000, aporte_mensal=1800, meses_aporte=12) \
        .configurar_funil(
            visitantes_mes_1=1000,
            crescimento_mensal=0.20,
            conv_trial=0.05,
            conv_pagante=0.15,
            churn=0.04
        ) \
        .configurar_receita(
            planos=[("Lite", 70, 0.50), ("Trader", 105, 0.30), ("Pro", 159, 0.20)]
        ) \
        .usar_canais(criar_estrategia_sam_canais) \
        .usar_infra(criar_infra_sam) \
        .usar_equipe(criar_equipe_sam) \
        .usar_tools(criar_stack_sam)
    
    config_base = scenario_base.build()
    print(scenario_base.gerar_relatorio())
    
    # ===== CRIAR VARIAÇÕES =====
    print("\nCriando variações...")
    scenario_pessimista = scenario_base.criar_pessimista()
    scenario_otimista = scenario_base.criar_otimista()
    
    # ===== SALVAR CENÁRIOS =====
    gerenciador = GerenciadorCenarios()
    gerenciador.salvar_cenario(scenario_base)
    gerenciador.salvar_cenario(scenario_pessimista)
    gerenciador.salvar_cenario(scenario_otimista)
    
    # ===== LISTAR CENÁRIOS =====
    print("\n" + "═" * 70)
    print("CENÁRIOS SALVOS")
    print("═" * 70)
    for cenario in gerenciador.listar_cenarios():
        print(f"• {cenario['nome']:40s} ({cenario['arquivo']})")
        print(f"  {cenario['descricao']}")
        print()
    
    # ===== COMPARAR CENÁRIOS =====
    gerenciador.imprimir_comparacao([
        "sam_cenario_base",
        "sam_cenario_base_pessimista",
        "sam_cenario_base_otimista"
    ])