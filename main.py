# DENTRO DE: main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
from typing import List, Optional, Dict, Any
from enum import Enum

# Importa os componentes do seu backend
from core.config import ConfigFinanceira, Funcionario, FerramentaSaaS, AtivoDepreciavel, DespesaAnual, ComissaoAfiliado
from core.builders.tools_builder import CategoriaFerramenta
from core.engine import MotorProjecaoFinanceira
from core.analytics.cohorts import gerar_cohort_matrix
from core.analytics.insights_engine import InsightsEngine

# Adiciona o path do projeto para garantir que as importações funcionem
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

app = FastAPI(
    title="SAM Financial Model API",
    description="API para executar projeções financeiras e análises avançadas.",
    version="1.0.0"
)

# Configuração do CORS para permitir que o frontend acesse a API
origins = [
    "http://localhost:5173",  # Endereço do frontend Vite
    "http://127.0.0.1:5173",   # Adicionado para garantir
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],      # Permite todos os cabeçalhos
)

# Cria um modelo Pydantic para validar os dados de entrada.
# Ele deve espelhar a estrutura da sua classe ConfigFinanceira.

class FerramentaSaaSModel(BaseModel):
    nome: str
    categoria: CategoriaFerramenta
    custo_mensal: float
    provider: str = ""
    descricao: str = ""
    essencial: bool = True
    custo_por_usuario: float = 0.0
    mes_inicio: int = 1
    mes_fim: Optional[int] = None
    ativa: bool = True

class FuncionarioModel(BaseModel):
    nome: str
    cargo: str
    salario_bruto: float
    mes_inicio: int
    tipo: str = "CLT"
    encargos_percentual: float = 0.68
    ativo: bool = True
    mes_fim: Optional[int] = None

class AtivoDepreciavelModel(BaseModel):
    nome: str
    valor_aquisicao: float
    meses_depreciacao: int
    mes_aquisicao: int = 0
    ativo: bool = True
    mes_fim: Optional[int] = None

class DespesaAnualModel(BaseModel):
    nome: str
    valor_anual: float
    mes_pagamento: int = 1
    ativo: bool = True
    mes_inicio: int = 1
    mes_fim: Optional[int] = None

class ComissaoAfiliadoModel(BaseModel):
    percentual_sobre_venda: float
    mes_inicio_programa: int = 1
    percentual_vendas_via_afiliados: float = 0.0

class ProjecaoRequest(BaseModel):
    # FLAGS DE ATIVAÇÃO GERAIS
    ativar_receita_por_usuario: bool = True
    ativar_custo_ia: bool = True
    ativar_impostos: bool = True
    ativar_taxas_pgto: bool = True
    ativar_fundador: bool = True
    ativar_equipe_clt: bool = True
    ativar_equipe_pj: bool = True
    ativar_escritorio: bool = False
    ativar_ferramentas: bool = True
    ativar_servicos_profs: bool = True
    ativar_marketing: bool = True
    ativar_depreciacao: bool = True
    ativar_despesas_anuais: bool = True
    ativar_comissoes_afiliado: bool = False
    ativar_infra_tier1: bool = True
    ativar_infra_tier2: bool = True
    ativar_infra_tier3: bool = True

    # 1. CAPITAL E FINANCIAMENTO
    capital_inicial_caixa: float = 10000.00  # Capital inicial (Bootstrapping/Pré-Seed)
    aporte_mensal_fixo: float = 1800.00
    meses_aporte_fixo: int = 12
    
    # 2. FUNIL DE AQUISIÇÃO (DETALHADO)
    visitantes_mes_1: int = 1000
    taxa_crescimento_trafego_mensal: float = 0.20
    taxa_conversao_visitante_trial: float = 0.05
    taxa_conversao_trial_pagante: float = 0.15
    churn_mensal: float = 0.04
    
    # 3. MODELO DE RECEITA
    preco_plano_lite: float = 69.90
    preco_plano_trader: float = 99.00
    preco_plano_pro: float = 159.00
    mix_plano_lite: float = 0.50
    mix_plano_trader: float = 0.30
    mix_plano_pro: float = 0.20
    arpu_medio_override: Optional[float] = None
    
    # 4. CUSTOS VARIÁVEIS (COGS)
    custo_ia_por_usuario: float = 5.00
    aliquota_impostos: float = 0.06
    taxa_pagamento_percentual: float = 0.0349
    taxa_pagamento_fixa_por_transacao: float = 0.39
    comissao_afiliados: Optional[ComissaoAfiliadoModel] = None
    
    # 5. INFRAESTRUTURA ESCALÁVEL (3 TIERS)
    infra_tier1_custo_fixo: float = 209.00
    infra_tier1_limite: int = 100
    infra_tier1_detalhes: Dict[str, float] = Field(default_factory=lambda: {
        'vps_principal': 55.00,
        'vps_coleta_mt5': 150.00,
        'dominio': 4.00
    })
    infra_tier2_custo_fixo: float = 5559.00
    infra_tier2_limite: int = 500
    infra_tier2_detalhes: Dict[str, float] = Field(default_factory=lambda: {
        'api_cedro': 5000.00,
        'vps_robusta': 500.00,
        'ferramentas_infra': 59.00
    })
    infra_tier3_custo_por_usuario: float = 1.50
    cloud_custo_excedente_por_gb: float = 0.10
    cloud_gb_inclusos_tier: int = 1000
    cloud_gb_estimado_por_usuario: float = 0.5
    
    # 6. MARKETING (2 FASES)
    marketing_fase1_custo_fixo: float = 500.00
    marketing_fase1_duracao_meses: int = 3
    marketing_fase2_perc_lucro_bruto: float = 0.25
    cac_pago_meta: float = 500.00
    
    # 7. SALÁRIO DO FUNDADOR (CONDICIONAL)
    salario_fundador_valor: float = 5000.00
    salario_fundador_mes_inicio_ideal: int = 6
    salario_fundador_caixa_minimo_seguranca: float = 10000.00
    
    # 8. EQUIPE E PESSOAL (SISTEMA COMPLETO)
    equipe: List[FuncionarioModel] = Field(default_factory=list)
    
    # 9. ESCRITÓRIO E OPERAÇÃO
    escritorio_aluguel_mensal: float = 0.0
    escritorio_condominio_mensal: float = 0.0
    escritorio_agua_luz_mensal: float = 0.0
    escritorio_internet_mensal: float = 0.0
    escritorio_outros_mensal: float = 0.0
    escritorio_mes_inicio: int = 999
    
    # 10. FERRAMENTAS SAAS (CATEGORIZADAS)
    ferramentas_saas: List[FerramentaSaaSModel] = Field(default_factory=list)
    
    # 11. SERVIÇOS PROFISSIONAIS
    contabilidade_mensal: float = 0.0
    contabilidade_mes_inicio: int = 1
    advogado_retainer_mensal: float = 0.0
    advogado_mes_inicio: int = 999
    consultorias_outras_mensal: float = 0.0
    
    # 12. DEPRECIAÇÃO DE ATIVOS
    ativos_depreciaveis: List[AtivoDepreciavelModel] = Field(default_factory=list)
    
    # 13. DESPESAS ANUAIS RATEADAS
    despesas_anuais: List[DespesaAnualModel] = Field(default_factory=list)


@app.post("/projecao/")
def executar_projecao_completa(request: ProjecaoRequest):
    """
    Recebe as configurações, executa a projeção completa e retorna todos os resultados.
    """
    # 1. Cria o objeto de configuração a partir dos dados recebidos
    request_data = request.model_dump()
    
    # Converte os dicionários das listas para os dataclasses correspondentes
    request_data['equipe'] = [Funcionario(**f) for f in request_data.get('equipe', [])]
    request_data['ferramentas_saas'] = [FerramentaSaaS(**f) for f in request_data.get('ferramentas_saas', [])]
    request_data['ativos_depreciaveis'] = [AtivoDepreciavel(**a) for a in request_data.get('ativos_depreciaveis', [])]
    request_data['despesas_anuais'] = [DespesaAnual(**d) for d in request_data.get('despesas_anuais', [])]
    if request_data.get('comissao_afiliados'):
        request_data['comissao_afiliados'] = ComissaoAfiliado(**request_data['comissao_afiliados'])

    config = ConfigFinanceira(**request_data)
    
    # 2. Executa o motor de projeção
    motor = MotorProjecaoFinanceira(config)
    df_projecao = motor.executar_projecao()
    kpis = motor.calcular_kpis()
    
    # 3. Executa a camada de análise
    insights_engine = InsightsEngine(df_projecao, kpis, config)
    insights = insights_engine.generate_all()
    
    df_cohorts = gerar_cohort_matrix(df_projecao)
    
    # 4. Monta e retorna a resposta completa
    # Converte DataFrames para JSON para poderem ser enviados pela rede
    return {
        "kpis": kpis,
        "insights": insights,
        "projecao_mensal": df_projecao.to_dict(orient='records'),
        "analise_cohorts": df_cohorts.to_dict(orient='records')
    }

@app.get("/")
def read_root():
    return {"status": "SAM Financial Model API está online."}