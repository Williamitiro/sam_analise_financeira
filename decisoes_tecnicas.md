# 🧠 PARTE 13: DECISÕES TÉCNICAS IMPORTANTES

## 13.1 Arquitetura de Session State

**Problema:** Streamlit recarrega tudo a cada interação

**Solução:**
```python
# Criar um "Store" centralizado
class AppStore:
    def __init__(self):
        if 'initialized' not in st.session_state:
            self._initialize()
    
    def _initialize(self):
        st.session_state.initialized = True
        st.session_state.config = criar_config_padrao()
        st.session_state.df_projecao = None
        st.session_state.kpis = None
        # ... etc
    
    @staticmethod
    def update_config(new_config):
        st.session_state.config = new_config
        # Invalida caches dependentes
        st.session_state.df_projecao = None
        st.session_state.kpis = None
    
    @staticmethod
    def run_projection():
        motor = MotorProjecaoFinanceira(st.session_state.config)
        st.session_state.df_projecao = motor.executar_projecao()
        st.session_state.kpis = motor.calcular_kpis()
        st.session_state.insights = InsightsEngine(...).generate_all()
```

---

## 13.2 Sistema de Cache Inteligente

**Problema:** Projeção é lenta, rodar toda vez é inviável

**Solução:**
```python
import hashlib
import pickle

def hash_config(config: ConfigFinanceira) -> str:
    """Cria hash da configuração para cache"""
    config_dict = config.to_dict()
    config_str = str(sorted(config_dict.items()))
    return hashlib.md5(config_str.encode()).hexdigest()

@st.cache_data(ttl=3600)
def run_projection_cached(config_hash: str, config: ConfigFinanceira, meses: int):
    """Só recalcula se config mudou"""
    motor = MotorProjecaoFinanceira(config)
    df = motor.executar_projecao(meses=meses)
    kpis = motor.calcular_kpis()
    return df, kpis

# Uso:
config_hash = hash_config(st.session_state.config)
df, kpis = run_projection_cached(config_hash, st.session_state.config, 36)
```

---

## 13.3 Drill-Down Stack

**Problema:** Como navegar entre níveis de drill-down?

**Solução:**
```python
class DrillDownNavigator:
    def __init__(self):
        if 'drill_stack' not in st.session_state:
            st.session_state.drill_stack = []
    
    def drill_into(self, label: str, data: dict):
        """Adiciona nível à pilha"""
        st.session_state.drill_stack.append({
            'label': label,
            'data': data,
            'timestamp': datetime.now()
        })
    
    def drill_up(self):
        """Remove último nível"""
        if len(st.session_state.drill_stack) > 0:
            st.session_state.drill_stack.pop()
    
    def get_breadcrumb(self) -> str:
        """Retorna breadcrumb visual"""
        if not st.session_state.drill_stack:
            return "Home"
        
        path = " → ".join([item['label'] for item in st.session_state.drill_stack])
        return f"Home → {path}"
    
    def render_breadcrumb(self):
        """Renderiza breadcrumb clicável"""
        crumbs = ["Home"] + [item['label'] for item in st.session_state.drill_stack]
        
        cols = st.columns(len(crumbs) * 2 - 1)
        for i, crumb in enumerate(crumbs):
            with cols[i * 2]:
                if st.button(crumb, key=f"crumb_{i}"):
                    # Voltar para este nível
                    st.session_state.drill_stack = st.session_state.drill_stack[:i]
                    st.rerun()
            
            if i < len(crumbs) - 1:
                with cols[i * 2 + 1]:
                    st.write("→")
```

---

## 13.4 Filtros Globais

**Problema:** Cada dashboard precisa dos mesmos filtros

**Solução:**
```python
class GlobalFilters:
    @staticmethod
    def render_sidebar():
        """Renderiza filtros na sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.subheader("🔍 Filtros Globais")
            
            # Período
            col1, col2 = st.columns(2)
            with col1:
                mes_inicio = st.number_input("De (mês)", 1, 60, 1)
            with col2:
                mes_fim = st.number_input("Até (mês)", mes_inicio, 60, 36)
            
            st.session_state.filtro_periodo = (mes_inicio, mes_fim)
            
            # Granularidade
            st.session_state.filtro_granular = st.selectbox(
                "Granularidade",
                ["Mensal", "Trimestral", "Anual"]
            )
            
            # Cenário
            st.session_state.filtro_cenario = st.selectbox(
                "Cenário",
                list(st.session_state.cenarios.keys())
            )
    
    @staticmethod
    def apply_to_df(df: pd.DataFrame) -> pd.DataFrame:
        """Aplica filtros ao DataFrame"""
        mes_inicio, mes_fim = st.session_state.filtro_periodo
        df_filtered = df[(df['mes'] >= mes_inicio) & (df['mes'] <= mes_fim)]
        
        granular = st.session_state.filtro_granular
        if granular == "Trimestral":
            df_filtered = df_filtered.groupby(df_filtered['mes'] // 3).sum()
        elif granular == "Anual":
            df_filtered = df_filtered.groupby(df_filtered['mes'] // 12).sum()
        
        return df_filtered
```

---

## 13.5 Sistema de Temas

**Problema:** Cores consistentes em todos os gráficos

**Solução:**
```python
# .streamlit/config.toml
[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

# theme.py
COLORS = {
    'primary': '#2E86AB',
    'success': '#06A77D',
    'warning': '#F77F00',
    'danger': '#D62828',
    'info': '#4895EF',
    'secondary': '#6C757D',
    
    # Para gráficos
    'revenue': '#06A77D',
    'costs': '#D62828',
    'cash': '#2E86AB',
    'profit': '#06A77D',
    'loss': '#D62828',
    
    # Categorias de custo
    'pessoal': '#8338EC',
    'infra': '#3A86FF',
    'marketing': '#FB5607',
    'ferramentas': '#FFBE0B',
    'servicos': '#06A77D',
}

def get_plotly_template():
    """Retorna template Plotly consistente"""
    return {
        'layout': {
            'font': {'family': 'Arial, sans-serif'},
            'plot_bgcolor': '#FFFFFF',
            'paper_bgcolor': '#FFFFFF',
            'colorway': list(COLORS.values()),
        }
    }
```

---

# 📚 PARTE 14: PADRÕES DE CÓDIGO

## 14.1 Padrão de Builder

```python
# core/builders/team_builder.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class HiringTrigger:
    """Representa um gatilho de contratação"""
    type: str  # 'mrr', 'usuarios', 'mes', 'lucro'
    value: float
    operator: str = '>='  # '>=', '>', '==', '<', '<='

@dataclass
class Position:
    """Representa um cargo"""
    cargo: str
    salario_bruto: float
    tipo: str  # 'CLT', 'PJ'
    triggers: List[HiringTrigger]
    reajuste_anual_pct: float = 0.08
    beneficios: dict = None

class TeamBuilder:
    """Construtor de equipe com gatilhos"""
    
    def __init__(self, config: ConfigFinanceira):
        self.config = config
        self.positions: List[Position] = []
    
    def add_position(
        self,
        cargo: str,
        salario: float,
        tipo: str = 'CLT',
        triggers: List[HiringTrigger] = None
    ) -> 'TeamBuilder':
        """
        Adiciona cargo (fluent interface)
        
        Exemplo:
            builder.add_position(
                'Dev Backend',
                8000,
                tipo='CLT',
                triggers=[HiringTrigger('mrr', 50000)]
            )
        """
        position = Position(
            cargo=cargo,
            salario_bruto=salario,
            tipo=tipo,
            triggers=triggers or []
        )
        self.positions.append(position)
        return self  # Fluent interface
    
    def with_trigger(self, trigger_type: str, value: float) -> 'TeamBuilder':
        """Adiciona gatilho à última posição adicionada"""
        if not self.positions:
            raise ValueError("Adicione uma posição primeiro")
        
        self.positions[-1].triggers.append(
            HiringTrigger(type=trigger_type, value=value)
        )
        return self
    
    def with_benefits(self, **kwargs) -> 'TeamBuilder':
        """Adiciona benefícios à última posição"""
        if not self.positions:
            raise ValueError("Adicione uma posição primeiro")
        
        self.positions[-1].beneficios = kwargs
        return self
    
    def build(self) -> ConfigFinanceira:
        """Aplica ao config e retorna"""
        for position in self.positions:
            # Adiciona funcionário ao config com triggers
            # A lógica de quando contratar será no engine
            self.config.adicionar_funcionario_com_gatilhos(
                nome=position.cargo,
                cargo=position.cargo,
                salario_bruto=position.salario_bruto,
                tipo=position.tipo,
                gatilhos=[t.__dict__ for t in position.triggers]
            )
        
        return self.config

# Uso:
team = TeamBuilder(config) \
    .add_position('Dev Backend', 8000, 'CLT') \
        .with_trigger('mrr', 50000) \
        .with_benefits(vr=500, vt=300) \
    .add_position('Community Manager', 5000, 'CLT') \
        .with_trigger('usuarios', 1000) \
        .with_trigger('mrr', 80000) \
    .build()
```

---

## 14.2 Padrão de Component

```python
# app/components/metric_card.py

import streamlit as st
import plotly.graph_objects as go
from typing import Optional, Callable, Dict

class MetricCard:
    """
    Card de métrica com drill-down
    
    Uso:
        MetricCard(
            label="MRR",
            value=45000,
            delta=0.12,
            breakdown={'Lite': 20250, 'Trader': 15750, 'Pro': 9000}
        ).render()
    """
    
    def __init__(
        self,
        label: str,
        value: float,
        delta: Optional[float] = None,
        format_func: Callable = None,
        breakdown: Optional[Dict] = None,
        sparkline: Optional[list] = None,
        help_text: Optional[str] = None,
        target: Optional[float] = None
    ):
        self.label = label
        self.value = value
        self.delta = delta
        self.format_func = format_func or (lambda x: f"R$ {x:,.0f}")
        self.breakdown = breakdown
        self.sparkline = sparkline
        self.help_text = help_text
        self.target = target
    
    def render(self):
        """Renderiza o card"""
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Métrica principal
                formatted_value = self.format_func(self.value)
                delta_str = f"{self.delta:+.1%}" if self.delta is not None else None
                st.metric(
                    label=self.label,
                    value=formatted_value,
                    delta=delta_str,
                    help=self.help_text
                )
                
                # Target (se houver)
                if self.target:
                    progress = min(self.value / self.target, 1.0)
                    st.progress(progress)
                    st.caption(f"Meta: {self.format_func(self.target)} ({progress*100:.0f}%)")
            
            with col2:
                # Sparkline (se houver)
                if self.sparkline:
                    self._render_sparkline()
                
                # Botão drill-down (se houver breakdown)
                if self.breakdown:
                    if st.button("🔍", key=f"drill_{self.label}"):
                        self._show_breakdown()
    
    def _render_sparkline(self):
        """Renderiza mini gráfico de linha"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=self.sparkline,
            mode='lines',
            line=dict(color='#2E86AB', width=1),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))
        fig.update_layout(
            height=60,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    def _show_breakdown(self):
        """Mostra popup de breakdown"""
        with st.expander(f"📊 Composição: {self.label}", expanded=True):
            # Pizza
            fig = go.Figure(data=[go.Pie(
                labels=list(self.breakdown.keys()),
                values=list(self.breakdown.values()),
                hole=0.4
            )])
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela
            import pandas as pd
            df = pd.DataFrame({
                'Categoria': self.breakdown.keys(),
                'Valor': [self.format_func(v) for v in self.breakdown.values()],
                '%': [(v/self.value*100) for v in self.breakdown.values()]
            })
            df['%'] = df['%'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(df, use_container_width=True, hide_index=True)
```

---

## 14.3 Padrão de Insight

```python
# core/analytics/insights_engine.py

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class AlertLevel(Enum):
    CRITICAL = "🔴 CRÍTICO"
    WARNING = "🟡 ATENÇÃO"
    INFO = "🔵 INFO"
    SUCCESS = "🟢 POSITIVO"

@dataclass
class Insight:
    """Representa um insight/alerta"""
    level: AlertLevel
    category: str  # 'caixa', 'crescimento', 'custos', 'unit_economics'
    title: str
    description: str
    value: Optional[float] = None
    action: Optional[str] = None
    impact: Optional[str] = None

class InsightsEngine:
    """Gerador de insights automáticos"""
    
    def __init__(self, df: pd.DataFrame, kpis: dict, config: ConfigFinanceira):
        self.df = df
        self.kpis = kpis
        self.config = config
        self.insights: List[Insight] = []
    
    def generate_all(self) -> List[Insight]:
        """Gera todos os insights"""
        self._check_cash_health()
        self._check_growth_trajectory()
        self._check_unit_economics()
        self._check_cost_efficiency()
        self._check_milestones()
        
        # Ordena por severidade
        severity_order = {
            AlertLevel.CRITICAL: 0,
            AlertLevel.WARNING: 1,
            AlertLevel.INFO: 2,
            AlertLevel.SUCCESS: 3
        }
        self.insights.sort(key=lambda x: severity_order[x.level])
        
        return self.insights
    
    def _check_cash_health(self):
        """Verifica saúde do caixa"""
        vale_mes = self.kpis.get('Vale_da_Morte_Mes')
        vale_valor = self.kpis.get('Vale_da_Morte_Minimo_Caixa')
        
        if vale_mes and vale_mes <= 3:
            self.insights.append(Insight(
                level=AlertLevel.CRITICAL,
                category='caixa',
                title='Vale da Morte iminente',
                description=f'Caixa ficará negativo em {vale_mes} meses',
                value=vale_valor,
                action=f'Captar R$ {abs(vale_valor) * 1.3:,.0f} URGENTE ou cortar custos',
                impact='Risco de falência'
            ))
        elif vale_mes and vale_mes <= 6:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='caixa',
                title='Vale da Morte se aproximando',
                description=f'Caixa ficará negativo em {vale_mes} meses',
                value=vale_valor,
                action=f'Planejar captação de R$ {abs(vale_valor) * 1.3:,.0f}',
                impact='Risco moderado'
            ))
        
        # Runway
        runway = self.kpis.get('Runway_Meses')
        if isinstance(runway, int) and runway < 6:
            self.insights.append(Insight(
                level=AlertLevel.CRITICAL,
                category='caixa',
                title='Runway crítico',
                description=f'Apenas {runway} meses de caixa restantes',
                action='Captar capital ou reduzir burn rate URGENTE'
            ))
    
    def _check_growth_trajectory(self):
        """Verifica trajetória de crescimento"""
        # Crescimento recente
        if len(self.df) >= 3:
            crescimento_recente = self.df['MRR'].pct_change().tail(3).mean()
            crescimento_config = self.config.taxa_crescimento_trafego_mensal
            
            if crescimento_recente > crescimento_config * 1.2:
                self.insights.append(Insight(
                    level=AlertLevel.SUCCESS,
                    category='crescimento',
                    title='Crescimento acelerando!',
                    description=f'Crescimento real ({crescimento_recente*100:.1f}%) > meta ({crescimento_config*100:.1f}%)',
                    action='Considere investir mais em marketing para capitalizar o momentum',
                    impact='Break-even pode acontecer antes do esperado'
                ))
            elif crescimento_recente < crescimento_config * 0.7:
                self.insights.append(Insight(
                    level=AlertLevel.WARNING,
                    category='crescimento',
                    title='Crescimento desacelerando',
                    description=f'Crescimento real ({crescimento_recente*100:.1f}%) < meta ({crescimento_config*100:.1f}%)',
                    action='Investigar causas: saturação de canal? Concorrência? PMF?',
                    impact='Break-even pode atrasar'
                ))
    
    # ... métodos similares para outras categorias
```