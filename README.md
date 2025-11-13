# 💰 SAM Financial Model

Sistema completo de modelagem financeira para análise de viabilidade do negócio SAM (Sistema Quantitativo para Análise de Mercado Financeiro).

## 🎯 Características

- ✅ Projeção financeira de 36 meses com lógicas complexas
- ✅ Infraestrutura escalável em tiers (0-100, 101-500, 501+ usuários)
- ✅ Marketing em fases (fixo → % do lucro bruto)
- ✅ Salário condicional baseado em saldo de caixa
- ✅ Análise de KPIs (Break-Even, Payback, LTV/CAC, etc.)
- ✅ Visualizações profissionais (Matplotlib, Plotly)
- ✅ Interface Jupyter Notebook
- ✅ Mini-app web interativo (Streamlit)
- ✅ Exportação para Excel

## 📦 Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sam-financial-model.git
cd sam-financial-model

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 🚀 Como Usar

### Opção 1: Jupyter Notebook (Recomendado)
```bash
jupyter notebook notebook.ipynb
```

Execute as células sequencialmente para:
1. Configurar o cenário
2. Executar a projeção
3. Visualizar KPIs e gráficos
4. Exportar dados

### Opção 2: Mini-App Streamlit
```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador para:
- Configurar parâmetros interativamente
- Visualizar resultados em tempo real
- Baixar projeções em CSV/Excel

### Opção 3: Script Python
```python
from config import ConfigFinanceira
from engine import MotorProjecaoFinanceira
from visualizations import DashboardFinanceiro

# Configurar
config = ConfigFinanceira(
    aporte_mensal_fixo=2000,
    salario_fundador_mes_inicio_ideal=8
)

# Executar
motor = MotorProjecaoFinanceira(config)
projecao = motor.executar_projecao(36)
kpis = motor.calcular_kpis()

# Visualizar
print(motor.gerar_relatorio_texto())

dashboard = DashboardFinanceiro(projecao, kpis)
dashboard.plot_dashboard_completo()
```

## 📊 Estrutura do Projeto
```
sam_financial_model/
├── config.py           # Configurações e premissas
├── engine.py           # Motor de cálculo
├── visualizations.py   # Gráficos profissionais
├── notebook.ipynb      # Interface Jupyter
├── app.py             # Mini-app Streamlit
├── requirements.txt   # Dependências
└── README.md          # Este arquivo
```

## 🎛️ Principais Configurações

| Categoria | Parâmetro | Valor Padrão |
|-----------|-----------|--------------|
| **Capital** | Capex Inicial | R$ -8.000 |
| | Aporte Mensal | R$ 1.800 |
| **Aquisição** | Visitantes M1 | 1.000 |
| | Crescimento Tráfego | 20%/mês |
| | Conv. Trial | 5% |
| | Conv. Pagante | 15% |
| | Churn | 4%/mês |
| **Receita** | ARPU | R$ 97 |
| **Custos** | COGS IA | R$ 5/usuário |
| **Salário** | Pró-labore | R$ 5.000 |
| | Início | Mês 6 |
| | Caixa Mínimo | R$ 10.000 |

## 📈 KPIs Calculados

- 🎯 **Break-Even**: Mês em que o resultado operacional se torna positivo
- 💰 **Payback**: Mês em que o saldo de caixa se torna positivo
- ⚠️ **Vale da Morte**: Menor saldo de caixa (necessidade máxima)
- 📊 **LTV/CAC**: Relação entre Lifetime Value e Custo de Aquisição
- 👥 **Crescimento**: Usuários e MRR ao longo de 36 meses

## 🔍 Análises Disponíveis

- Projeção detalhada mês a mês
- Comparação de cenários (Pessimista, Realista, Otimista)
- Análise de sensibilidade (impacto do churn, conversão, etc.)
- Gráficos de crescimento, receita, fluxo de caixa e custos
- Dashboard executivo completo

## 📝 Licença

Este projeto é proprietário e confidencial.