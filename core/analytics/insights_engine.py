"""
core/analytics/insights_engine.py
Sistema de Geração Automática de Insights

Analisa a projeção financeira e gera:
- Alertas críticos (caixa, crescimento, custos)
- Oportunidades (onde investir, o que melhorar)
- Recomendações estratégicas
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import pandas as pd
import numpy as np


class AlertLevel(Enum):
    """Níveis de severidade de alertas"""
    CRITICAL = "CRÍTICO"
    WARNING = "ATENÇÃO"
    INFO = "INFO"
    SUCCESS = "POSITIVO"


@dataclass
class Insight:
    """
    Representa um insight/alerta gerado automaticamente.
    
    Attributes:
        level: Nível de severidade
        category: Categoria (caixa, crescimento, custos, unit_economics)
        title: Título do insight
        description: Descrição detalhada
        value: Valor numérico associado (opcional)
        action: Ação recomendada (opcional)
        impact: Impacto estimado (opcional)
    """
    level: AlertLevel
    category: str
    title: str
    description: str
    value: Optional[float] = None
    action: Optional[str] = None
    impact: Optional[str] = None


class InsightsEngine:
    """
    Motor de geração de insights automáticos.
    
    Analisa DataFrame de projeção e KPIs para detectar:
    - Problemas críticos (caixa negativo, churn alto)
    - Oportunidades (crescimento acelerando, canais eficientes)
    - Recomendações estratégicas (onde cortar custos, onde investir)
    """
    
    def __init__(self, df: pd.DataFrame, kpis: dict, config):
        """
        Args:
            df: DataFrame de projeção (saída do engine)
            kpis: Dict de KPIs calculados
            config: Instância de ConfigFinanceira
        """
        self.df = df
        self.kpis = kpis
        self.config = config
        self.insights: List[Insight] = []
    
    def generate_all(self) -> dict:
        """
        Gera todos os insights e retorna dict estruturado.
        
        Returns:
            {
                'alertas': [Insight, ...],
                'oportunidades': [Insight, ...],
                'recomendacoes': [Insight, ...]
            }
        """
        self._check_cash_health()
        self._check_growth_trajectory()
        self._check_unit_economics()
        self._check_cost_efficiency()
        self._check_milestones()
        
        # Separa por tipo
        alertas = [i for i in self.insights if i.level in [AlertLevel.CRITICAL, AlertLevel.WARNING]]
        oportunidades = [i for i in self.insights if i.level == AlertLevel.SUCCESS]
        info = [i for i in self.insights if i.level == AlertLevel.INFO]
        
        # Ordena por severidade
        severity_order = {
            AlertLevel.CRITICAL: 0,
            AlertLevel.WARNING: 1,
            AlertLevel.INFO: 2,
            AlertLevel.SUCCESS: 3
        }
        alertas.sort(key=lambda x: severity_order[x.level])
        
        return {
            'alertas': alertas,
            'oportunidades': oportunidades,
            'recomendacoes': info
        }
    
    def _check_cash_health(self):
        """Verifica saúde do caixa e runway"""
        
        # Vale da Morte
        vale_mes = self.kpis.get('Vale_da_Morte_Mes')
        vale_valor = self.kpis.get('Vale_da_Morte_Minimo_Caixa', 0)
        
        if vale_valor < 0:
            # Calcula quanto precisa captar
            buffer = 1.3  # 30% de margem de segurança
            valor_necessario = abs(vale_valor) * buffer
            
            if vale_mes <= 3:
                self.insights.append(Insight(
                    level=AlertLevel.CRITICAL,
                    category='caixa',
                    title='🚨 Vale da Morte IMINENTE',
                    description=f'Caixa ficará negativo em apenas {vale_mes} meses!',
                    value=vale_valor,
                    action=f'Captar R$ {valor_necessario:,.0f} URGENTEMENTE ou cortar custos',
                    impact='Risco de falência iminente'
                ))
            elif vale_mes <= 6:
                self.insights.append(Insight(
                    level=AlertLevel.WARNING,
                    category='caixa',
                    title='⚠️ Vale da Morte se aproximando',
                    description=f'Caixa ficará negativo no mês {vale_mes}',
                    value=vale_valor,
                    action=f'Planejar captação de R$ {valor_necessario:,.0f} nos próximos 2-3 meses',
                    impact='Risco moderado - há tempo para agir'
                ))
        
        # Runway
        runway = self.kpis.get('Runway_Meses')
        if isinstance(runway, int):
            if runway < 6:
                self.insights.append(Insight(
                    level=AlertLevel.CRITICAL,
                    category='caixa',
                    title='🚨 Runway CRÍTICO',
                    description=f'Apenas {runway} meses de caixa restantes',
                    action='Reduzir burn rate imediatamente ou captar capital',
                    impact='Empresa pode falir em menos de 6 meses'
                ))
            elif runway < 12:
                self.insights.append(Insight(
                    level=AlertLevel.WARNING,
                    category='caixa',
                    title='⚠️ Runway abaixo do ideal',
                    description=f'{runway} meses de runway (ideal: >12 meses)',
                    action='Iniciar processo de captação ou otimizar custos',
                    impact='Pressão crescente nos próximos meses'
                ))
        
        # Caixa positivo em todo período
        if self.df['Saldo_Caixa'].min() > 0:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='caixa',
                title='✅ Caixa saudável',
                description='Saldo de caixa positivo durante todo o período projetado',
                impact='Operação sustentável sem necessidade imediata de capital'
            ))
    
    def _check_growth_trajectory(self):
        """Verifica trajetória de crescimento"""
        
        if len(self.df) < 6:
            return  # Precisa de pelo menos 6 meses
        
        # Calcula crescimento recente (últimos 3 meses)
        mrr_recente = self.df['MRR'].tail(3)
        crescimento_recente = mrr_recente.pct_change().mean()
        
        # Calcula crescimento dos 3 meses anteriores
        mrr_anterior = self.df['MRR'].tail(6).head(3)
        crescimento_anterior = mrr_anterior.pct_change().mean()
        
        # Compara com meta
        crescimento_config = self.config.taxa_crescimento_trafego_mensal
        
        # Acelerando
        if crescimento_recente > crescimento_anterior * 1.2:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='crescimento',
                title='🚀 Crescimento ACELERANDO!',
                description=f'Taxa de crescimento subiu de {crescimento_anterior*100:.1f}% para {crescimento_recente*100:.1f}%',
                action='Considere investir mais em marketing para capitalizar o momentum',
                impact='Break-even pode acontecer antes do projetado'
            ))
        
        # Acima da meta
        elif crescimento_recente > crescimento_config * 1.2:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='crescimento',
                title='📈 Crescimento acima da meta',
                description=f'Crescendo {crescimento_recente*100:.1f}%/mês (meta: {crescimento_config*100:.1f}%)',
                action='Manter estratégia atual e considerar escalar investimentos',
                impact='Atingirá marcos importantes mais cedo'
            ))
        
        # Desacelerando
        elif crescimento_recente < crescimento_anterior * 0.7:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='crescimento',
                title='⚠️ Crescimento DESACELERANDO',
                description=f'Taxa caiu de {crescimento_anterior*100:.1f}% para {crescimento_recente*100:.1f}%',
                action='Investigar causas: saturação de canal? Concorrência? PMF?',
                impact='Break-even e marcos podem atrasar'
            ))
        
        # Abaixo da meta
        elif crescimento_recente < crescimento_config * 0.7:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='crescimento',
                title='⚠️ Crescimento abaixo da meta',
                description=f'Crescendo {crescimento_recente*100:.1f}%/mês (meta: {crescimento_config*100:.1f}%)',
                action='Revisar estratégia de aquisição e otimizar canais',
                impact='Objetivos podem não ser atingidos no prazo'
            ))
        
        # Churn alto
        churn_medio = self.config.churn_mensal
        if churn_medio > 0.05:  # >5%/mês
            self.insights.append(Insight(
                level=AlertLevel.CRITICAL,
                category='crescimento',
                title='🚨 Churn MUITO ALTO',
                description=f'Churn de {churn_medio*100:.1f}%/mês é insustentável',
                action='Implementar programa de retenção URGENTE: onboarding, CS, features',
                impact='Crescimento está sendo "comido" pelo churn'
            ))
        elif churn_medio > 0.03:  # >3%/mês
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='crescimento',
                title='⚠️ Churn elevado',
                description=f'Churn de {churn_medio*100:.1f}%/mês acima do ideal (2-3%)',
                action='Investigar causas de cancelamento e melhorar retenção',
                impact='Limitando potencial de crescimento'
            ))
    
    def _check_unit_economics(self):
        """Verifica unit economics (LTV/CAC, Payback)"""
        
        ltv_cac = self.kpis.get('LTV_CAC_Ratio_Final', 0)
        
        if ltv_cac < 2:
            self.insights.append(Insight(
                level=AlertLevel.CRITICAL,
                category='unit_economics',
                title='🚨 Unit Economics INVIÁVEL',
                description=f'LTV/CAC de {ltv_cac:.1f}x é muito baixo (mínimo: 3x)',
                action='Reduzir CAC drasticamente OU aumentar LTV (retenção, preço, upsell)',
                impact='Modelo de negócio não é sustentável'
            ))
        elif ltv_cac < 3:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='unit_economics',
                title='⚠️ Unit Economics no limite',
                description=f'LTV/CAC de {ltv_cac:.1f}x está no mínimo aceitável (ideal: >5x)',
                action='Otimizar canais de aquisição e melhorar retenção',
                impact='Pouca margem para erros ou investimentos'
            ))
        elif ltv_cac >= 5:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='unit_economics',
                title='✅ Unit Economics EXCELENTE',
                description=f'LTV/CAC de {ltv_cac:.1f}x está muito bom (ideal: >5x)',
                action='Considere AUMENTAR investimento em marketing para escalar',
                impact='Margem saudável permite crescimento acelerado'
            ))
        
        # Payback
        payback = self.kpis.get('CAC_Payback_Meses_Config', 0)
        if payback > 12:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='unit_economics',
                title='⚠️ Payback muito longo',
                description=f'CAC Payback de {payback:.0f} meses (ideal: <12 meses)',
                action='Reduzir CAC ou aumentar ARPU para recuperar investimento mais rápido',
                impact='Pressão sobre caixa no curto prazo'
            ))
        elif payback <= 6:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='unit_economics',
                title='✅ Payback rápido',
                description=f'CAC Payback de {payback:.0f} meses (ideal: <12 meses)',
                action='Excelente! Considere investir mais em aquisição',
                impact='Retorno rápido do investimento em marketing'
            ))
    
    def _check_cost_efficiency(self):
        """Verifica eficiência de custos"""
        
        if len(self.df) < 3:
            return
        
        # Pega último mês
        ultimo_mes = self.df.iloc[-1]
        mrr = ultimo_mes['MRR']
        opex = ultimo_mes['OPEX_Total']
        
        # Calcula %OPEX/Receita
        opex_pct = (opex / mrr * 100) if mrr > 0 else 0
        
        if opex_pct > 80:
            self.insights.append(Insight(
                level=AlertLevel.CRITICAL,
                category='custos',
                title='🚨 OPEX MUITO ALTO',
                description=f'OPEX representa {opex_pct:.0f}% da receita (ideal: <70%)',
                action='Cortar custos não-essenciais imediatamente',
                impact='Margem muito apertada, insustentável'
            ))
        elif opex_pct > 70:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='custos',
                title='⚠️ OPEX elevado',
                description=f'OPEX representa {opex_pct:.0f}% da receita',
                action='Analisar possibilidade de otimizar custos fixos',
                impact='Margem apertada limita investimentos'
            ))
        elif opex_pct < 50:
            self.insights.append(Insight(
                level=AlertLevel.SUCCESS,
                category='custos',
                title='✅ OPEX eficiente',
                description=f'OPEX representa apenas {opex_pct:.0f}% da receita',
                action='Ótimo! Margem saudável para crescer',
                impact='Eficiência operacional permite escala'
            ))
        
        # Analisa evolução de custos
        opex_serie = self.df['OPEX_Total'].tail(6)
        mrr_serie = self.df['MRR'].tail(6)
        
        crescimento_opex = opex_serie.pct_change().mean()
        crescimento_mrr = mrr_serie.pct_change().mean()
        
        if crescimento_opex > crescimento_mrr * 1.5:
            self.insights.append(Insight(
                level=AlertLevel.WARNING,
                category='custos',
                title='⚠️ Custos crescendo mais que receita',
                description='OPEX crescendo mais rápido que MRR',
                action='Revisar contratações e custos variáveis',
                impact='Margem está se deteriorando'
            ))
    
    def _check_milestones(self):
        """Verifica progresso em marcos importantes"""
        
        # Break-even
        break_even = self.kpis.get('Break_Even_Mes')
        if break_even and break_even != 'N/A':
            meses_faltam = break_even - len(self.df)
            
            if meses_faltam <= 3 and meses_faltam > 0:
                self.insights.append(Insight(
                    level=AlertLevel.SUCCESS,
                    category='marcos',
                    title='🎯 Break-even se aproximando!',
                    description=f'Faltam apenas {meses_faltam} meses para break-even',
                    action='Manter foco em crescimento e eficiência',
                    impact='Marco importante está próximo'
                ))
            elif meses_faltam <= 0:
                self.insights.append(Insight(
                    level=AlertLevel.SUCCESS,
                    category='marcos',
                    title='🎊 Break-even ATINGIDO!',
                    description='Empresa está operando com lucro operacional',
                    action='Considere reinvestir parte do lucro em crescimento',
                    impact='Sustentabilidade alcançada'
                ))
        
        # MRR de marcos (R$50k, R$100k, R$500k)
        mrr_atual = self.df.iloc[-1]['MRR']
        
        marcos_mrr = [
            (50000, 'R$50k MRR', 'Marco inicial de tração'),
            (100000, 'R$100k MRR', 'Marco importante - empresa séria'),
            (500000, 'R$500k MRR', 'Marco de escala - empresa madura')
        ]
        
        for valor_marco, nome_marco, desc in marcos_mrr:
            if mrr_atual >= valor_marco * 0.8 and mrr_atual < valor_marco:
                falta = valor_marco - mrr_atual
                self.insights.append(Insight(
                    level=AlertLevel.INFO,
                    category='marcos',
                    title=f'🎯 Próximo do marco: {nome_marco}',
                    description=f'{desc}. Faltam R$ {falta:,.0f}',
                    action='Manter ritmo de crescimento atual',
                    impact='Marco importante se aproxima'
                ))
            elif mrr_atual >= valor_marco and len([i for i in self.insights if nome_marco in i.title]) == 0:
                self.insights.append(Insight(
                    level=AlertLevel.SUCCESS,
                    category='marcos',
                    title=f'🎊 {nome_marco} ATINGIDO!',
                    description=desc,
                    impact='Próximo nível alcançado'
                ))