"""
examples/configurar_sam_completo.py

Exemplo completo de configuração do SAM Financial Model usando todos os builders.

Este script mostra como usar cada builder para criar uma configuração completa
baseada na especificação real do projeto SAM (plataforma de trading).

Execute: python examples/configurar_sam_completo.py
"""

import sys
from pathlib import Path

# Adiciona raiz do projeto ao path
RAIZ = Path(__file__).parent.parent
sys.path.insert(0, str(RAIZ))

from core.config import ConfigFinanceira
from core.builders.channels_builder import ChannelsBuilder, TipoCanal
from core.builders.infra_builder import InfraBuilder, TipoComponente
from core.builders.team_builder import TeamBuilder
from core.builders.scenario_builder import ScenarioBuilder, GerenciadorCenarios


# ============================================================================
# CONFIGURAÇÃO COMPLETA DO SAM
# ============================================================================

def configurar_sam_completo():
    """
    Configura o SAM Financial Model com TODOS os builders.
    
    Baseado na especificação:
    - CAPEX: R$8.000 (estação de trabalho P&D)
    - OPEX Fase 1: R$1.709/mês (sem salários)
    - Infraestrutura: MT5 + AWS + Hostinger em tiers
    - Canais: SEO (40%) + Ads (30%) + Afiliados (20%) + Referral (10%)
    - Equipe: Fundador (fases salariais) + contratações futuras
    - Ferramentas: Cursor, Copilot, Claude, etc.
    """
    
    print("\n" + "="*70)
    print("CONFIGURANDO SAM FINANCIAL MODEL - VERSÃO COMPLETA")
    print("="*70 + "\n")
    
    # Cria scenario builder
    scenario = ScenarioBuilder(
        nome="SAM - Trading Platform",
        descricao="Projeção financeira completa para plataforma SaaS de trading"
    )
    
    # ========================================================================
    # 1. CAPITAL E FINANCIAMENTO
    # ========================================================================
    print("📊 1/8 - Configurando Capital e Financiamento...")
    
    scenario.configurar_capital_basico(
        capex_inicial=8000,  # Estação de trabalho
        aporte_mensal=1800,
        meses_aporte=12
    )
    
    # ========================================================================
    # 2. CANAIS DE AQUISIÇÃO
    # ========================================================================
    print("📊 2/8 - Configurando Canais de Aquisição...")
    
    def configurar_canais_sam(config):
        builder = ChannelsBuilder(config)
        
        # SEO Orgânico: 40% do tráfego, melhor conversão
        builder.add_canal_organico(
            nome="SEO & Content Marketing",
            percentual_trafego=0.40,
            taxa_conversao_trial=0.08,
            taxa_conversao_pagante=0.20,
            cac_medio=200,
            custo_seo_mensal=1000
        )
        
        # Google Ads: 30% do tráfego, CAC meta R$500
        builder.add_canal_pago(
            nome="Google Ads (Performance)",
            percentual_trafego=0.30,
            taxa_conversao_trial=0.04,
            taxa_conversao_pagante=0.15,
            cac_medio=500,
            cpc=2.50
        )
        
        # Programa de Afiliados: 20% do tráfego
        builder.add_canal_afiliado(
            nome="Programa de Afiliados",
            percentual_trafego=0.20,
            taxa_conversao_trial=0.12,
            taxa_conversao_pagante=0.30,
            cac_medio=100,
            comissao_percentual=0.20
        )
        
        # Referral: 10% do tráfego, melhor conversão
        builder.add_canal_referral(
            nome="Programa de Indicação",
            percentual_trafego=0.10,
            taxa_conversao_trial=0.15,
            taxa_conversao_pagante=0.35,
            cac_medio=50,
            incentivo_por_referral=20
        )
        
        return builder.build()
    
    scenario.usar_canais(configurar_canais_sam)
    
    # ========================================================================
    # 3. INFRAESTRUTURA ESCALÁVEL
    # ========================================================================
    print("📊 3/8 - Configurando Infraestrutura em Tiers...")
    
    def configurar_infra_sam(config):
        builder = InfraBuilder(config)
        
        # TIER 1: Validação (0-100 usuários) - R$209/mês
        builder.criar_tier(1, "Validação com MT5", 0, 100,
                          descricao="Infraestrutura inicial para MVP")
        
        builder.add_componente(
            "VPS Principal (Backend SAM)",
            TipoComponente.VPS,
            55.00,
            descricao="Hostinger KVM 4 - Docker Stack",
            provider="Hostinger",
            specs={"CPU": "4 vCPU", "RAM": "16 GB", "Disk": "200 GB NVMe"}
        )
        
        builder.add_componente(
            "VPS Coleta MT5 (Windows)",
            TipoComponente.VPS,
            150.00,
            descricao="AWS t2.small - MetaTrader 5 24/7",
            provider="AWS",
            specs={"Instance": "t2.small", "OS": "Windows Server", "RAM": "2 GB"}
        )
        
        builder.add_componente(
            "Domínio",
            TipoComponente.DOMINIO,
            4.00,
            descricao="Registro.br (.com.br) - R$40/ano",
            provider="Registro.br"
        )
        
        # TIER 2: Escala (101-500 usuários) - R$5.650/mês
        builder.criar_tier(2, "Escala com API Cedro", 101, 500,
                          descricao="API profissional de dados B3")
        
        builder.add_componente(
            "API Cedro (Feed Profissional)",
            TipoComponente.API_EXTERNA,
            5000.00,
            descricao="Dados de mercado em tempo real",
            provider="Cedro",
            specs={"Delay": "Real-time", "Cobertura": "B3 completa"}
        )
        
        builder.add_componente(
            "VPS Robusta (Upgrade)",
            TipoComponente.VPS,
            500.00,
            descricao="Servidor dedicado ou VPS grande",
            provider="AWS/Hostinger",
            specs={"CPU": "8 vCPU", "RAM": "32 GB", "Disk": "500 GB SSD"}
        )
        
        builder.add_componente(
            "Backup S3",
            TipoComponente.BACKUP,
            50.00,
            provider="AWS S3",
            essencial=False
        )
        
        builder.add_componente(
            "CDN Cloudflare Pro",
            TipoComponente.CDN,
            100.00,
            provider="Cloudflare",
            essencial=False
        )
        
        # TIER 3: Hiperescala (501+ usuários)
        builder.criar_tier(3, "Hiperescala", 501, 999999,
                          custo_por_usuario=1.50,
                          descricao="Custo variável por usuário adicional")
        
        return builder.build()
    
    scenario.usar_infra(configurar_infra_sam)
    
    # ========================================================================
    # 4. EQUIPE COM GATILHOS
    # ========================================================================
    print("📊 4/8 - Configurando Planejamento de Equipe...")
    
    def configurar_equipe_sam(config):
        builder = TeamBuilder(config)
        
        # FUNDADOR/CEO com fases salariais
        builder.add_fundador("Fundador", "CEO/CTO", equity=0.70) \
            .fase_sem_salario(1, 6) \
            .fase_salario_minimo(7, 12, 3000) \
            .fase_salario_pleno(13, None, 8000, gatilho_mrr=30000) \
            .com_pro_labore(0.10, gatilho_lucro=10000, minimo=1000, maximo=20000)
        
        # DEV BACKEND (contratar quando MRR > R$50k)
        builder.add_clt("Dev Backend Pleno", "Engenheiro de Software", 8000) \
            .quando_mrr_atingir(50000) \
            .com_beneficios(vr=500, vt=300, plano=400) \
            .com_reajuste_anual(0.08)
        
        # COMMUNITY MANAGER (contratar quando usuários > 1000)
        builder.add_clt("Community Manager", "Sucesso do Cliente", 5000) \
            .quando_usuarios_atingir(1000) \
            .com_beneficios(vr=500, vt=300, plano=300) \
            .com_reajuste_anual(0.08)
        
        # DESIGNER PJ (contratar no mês 6)
        builder.add_pj("Designer UI/UX", "Designer", 3000) \
            .no_mes(6)
        
        # CFO (contratar quando MRR > R$200k)
        builder.add_clt("CFO", "Chief Financial Officer", 12000) \
            .quando_mrr_atingir(200000) \
            .com_beneficios(vr=800, plano=800) \
            .com_reajuste_anual(0.10)
        
        return builder.build()
    
    scenario.usar_equipe(configurar_equipe_sam)
    
    # ========================================================================
    # 5. FERRAMENTAS SAAS
    # ========================================================================
    print("📊 5/8 - Configurando Stack de Ferramentas...")
    
    def configurar_tools_sam(config):
        from core.builders.tools_builder import ToolsBuilder, CategoriaFerramenta
        
        builder = ToolsBuilder(config)
        
        # Desenvolvimento
        builder.add_ferramenta_dev("Cursor IDE", 200, "Cursor")
        builder.add_ferramenta_dev("GitHub Copilot", 100, "GitHub")
        builder.add_ferramenta_dev("Firecrawl", 100, "Firecrawl")
        
        # IA & APIs
        builder.add_ferramenta_ia("Claude Pro (3 usuários)", 400, "Anthropic")
        builder.add_ferramenta_ia("OpenAI API", 100, "OpenAI")
        
        # Segurança
        builder.add_ferramenta("Sentry", CategoriaFerramenta.SEGURANCA, 0, 
                              "Sentry", essencial=True)
        
        # Gestão
        builder.add_ferramenta_gestao("Notion", 50, "Notion", custo_por_usuario=8)
        
        return builder.build()
    
    scenario.usar_tools(configurar_tools_sam)
    
    # ========================================================================
    # 6. MARKETING EM FASES
    # ========================================================================
    print("📊 6/8 - Configurando Estratégia de Marketing...")
    
    def configurar_marketing_sam(config):
        from core.builders.marketing_builder import MarketingBuilder
        
        builder = MarketingBuilder(config)
        
        # Fase 1: Validação (meses 1-6) - R$1.000/mês fixo
        builder.fase_validacao(1, 6, 1000, canais=["SEO", "Content"])
        
        # Fase 2: Crescimento (meses 7-18) - 25% do lucro bruto
        builder.fase_crescimento(7, 18, 0.25, 'percentual_lucro', 
                                canais=["Ads", "SEO", "Referral"])
        
        # Fase 3: Escala (meses 19-36) - 20% da receita
        builder.fase_escala(19, 36, 0.20, 
                           canais=["Ads", "Eventos", "Parceiros"])
        
        # Fase 4: Maturidade (mês 37+) - CAC target R$300
        builder.fase_maturidade(37, 300, 
                               canais=["Organic", "Referral", "Brand"])
        
        return builder.build()
    
    scenario.usar_marketing(configurar_marketing_sam)
    
    # ========================================================================
    # 7. COGS COMPLETO
    # ========================================================================
    print("📊 7/8 - Configurando COGS (Custos Variáveis)...")
    
    def configurar_cogs_sam(config):
        from core.builders.cogs_builder import COGSBuilder
        
        builder = COGSBuilder(config)
        
        builder \
            .taxa_pagamento(0.0349, 0.39, "Stripe") \
            .comissao_afiliados(0.20, percentual_vendas=0.20) \
            .comissao_parceiros(0.15, percentual_vendas=0.10) \
            .custo_ia_por_usuario(5.00) \
            .cashback_usuarios(0.05)
        
        return builder.build()
    
    scenario.usar_cogs(configurar_cogs_sam)
    
    # ========================================================================
    # 8. FUNIL E RECEITA
    # ========================================================================
    print("📊 8/8 - Configurando Funil e Modelo de Receita...")
    
    scenario.configurar_funil(
        visitantes_mes_1=1000,
        crescimento_mensal=0.20,
        conv_trial=0.05,  # Médias ponderadas dos canais
        conv_pagante=0.15,
        churn=0.04
    )
    
    scenario.configurar_receita(
        planos=[
            ("Lite", 70, 0.50),
            ("Trader", 105, 0.30),
            ("Pro", 159, 0.20)
        ]
    )
    
    # ========================================================================
    # BUILD FINAL
    # ========================================================================
    print("\n✅ Configuração completa! Construindo cenário...")
    config = scenario.build()
    
    # Exibe relatório
    print("\n" + scenario.gerar_relatorio())
    
    # Exibe detalhes dos builders
    print("\n" + "="*70)
    print("DETALHES DA CONFIGURAÇÃO")
    print("="*70 + "\n")
    
    # Canais
    if hasattr(config, 'canais_aquisicao') and config.canais_aquisicao:
        from core.builders.channels_builder import ChannelsBuilder
        cb = ChannelsBuilder(config)
        cb.canais = config.canais_aquisicao
        print(cb.gerar_relatorio())
    
    # Infraestrutura
    if hasattr(config, 'tiers_infraestrutura') and config.tiers_infraestrutura:
        from core.builders.infra_builder import InfraBuilder
        ib = InfraBuilder(config)
        ib.tiers = config.tiers_infraestrutura
        print("\n" + ib.gerar_relatorio())
    
    # Equipe
    if hasattr(config, 'cargos_planejados') and config.cargos_planejados:
        tb = TeamBuilder(config)
        tb.cargos = config.cargos_planejados
        print("\n" + tb.gerar_relatorio())
    
    return scenario


# ============================================================================
# CRIAR VARIAÇÕES (BASE, PESSIMISTA, OTIMISTA)
# ============================================================================

def criar_cenarios_sam():
    """
    Cria os 3 cenários principais: Base, Pessimista, Otimista
    """
    print("\n" + "="*70)
    print("CRIANDO CENÁRIOS SAM (BASE + VARIAÇÕES)")
    print("="*70)
    
    # Cenário Base
    scenario_base = configurar_sam_completo()
    
    # Cenário Pessimista
    print("\n📉 Criando cenário PESSIMISTA...")
    scenario_pessimista = scenario_base.criar_pessimista()
    print(f"✅ '{scenario_pessimista.nome}' criado")
    
    # Cenário Otimista
    print("\n📈 Criando cenário OTIMISTA...")
    scenario_otimista = scenario_base.criar_otimista()
    print(f"✅ '{scenario_otimista.nome}' criado")
    
    # Salvar todos
    print("\n💾 Salvando cenários...")
    gerenciador = GerenciadorCenarios()
    
    gerenciador.salvar_cenario(scenario_base)
    gerenciador.salvar_cenario(scenario_pessimista)
    gerenciador.salvar_cenario(scenario_otimista)
    
    print("\n✅ Todos os cenários foram salvos em 'data/scenarios/'")
    
    # Listar cenários salvos
    print("\n" + "="*70)
    print("CENÁRIOS DISPONÍVEIS")
    print("="*70)
    
    cenarios = gerenciador.listar_cenarios()
    for i, cenario in enumerate(cenarios, 1):
        print(f"\n{i}. {cenario['nome']}")
        print(f"   Arquivo: {cenario['arquivo']}")
        print(f"   Descrição: {cenario['descricao']}")
        print(f"   Builders: {', '.join(cenario['builders'])}")
    
    # Comparar cenários
    print("\n" + "="*70)
    print("COMPARAÇÃO DE CENÁRIOS")
    print("="*70)
    
    gerenciador.imprimir_comparacao([
        "sam_trading_platform",
        "sam_trading_platform_pessimista",
        "sam_trading_platform_otimista"
    ])
    
    return gerenciador


# ============================================================================
# EXEMPLO DE EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    try:
        # Cria cenários completos
        gerenciador = criar_cenarios_sam()
        
        print("\n" + "="*70)
        print("PRÓXIMOS PASSOS")
        print("="*70)
        print("""
Para usar os cenários criados:

1. No Streamlit:
   from core.builders.scenario_builder import GerenciadorCenarios
   gerenciador = GerenciadorCenarios()
   scenario = gerenciador.carregar_cenario("sam_trading_platform")
   config = scenario.build()

2. Para rodar projeção:
   from core.engine import MotorProjecaoFinanceira
   motor = MotorProjecaoFinanceira(config)
   df = motor.executar_projecao(meses=36)
   kpis = motor.calcular_kpis()

3. Para comparar cenários:
   gerenciador.imprimir_comparacao([
       "sam_trading_platform",
       "sam_trading_platform_pessimista",
       "sam_trading_platform_otimista"
   ])
        """)
        
        print("\n✅ Configuração SAM completa e pronta para uso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()