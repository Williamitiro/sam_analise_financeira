import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/Dialog';
import { Badge } from '../ui/badge';
import { KPIs } from '@/types/api.types';
import { formatCurrency, formatNumber } from '@/lib/utils/formatters';
import { Lightbulb } from 'lucide-react';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

interface GlossaryModalProps {
  term: MetricId | null;
  isOpen: boolean;
  onClose: () => void;
  kpis: KPIs;
}

const GLOSSARY_CONTENT: Record<MetricId, { title: string; definition: string; formula?: string; interpretation: React.ReactNode; getValue: (kpis: KPIs) => string; getRecommendation: (kpis: KPIs) => string; }> = {
  mrr: {
    title: 'MRR (Monthly Recurring Revenue)',
    definition: 'A receita recorrente mensal é a medida mais importante para empresas de assinatura. Ela representa a receita previsível que a empresa espera receber a cada mês.',
    formula: 'MRR = (Soma da receita mensal de todos os clientes)',
    interpretation: <p className="text-sm">O MRR é o batimento cardíaco de um negócio SaaS. O crescimento consistente do MRR é o principal indicador de saúde e da trajetória do negócio.</p>,
    getValue: (kpis) => formatCurrency(kpis.MRR_Final),
    getRecommendation: (kpis) => 'Foque em estratégias de aquisição e retenção para aumentar o MRR consistentemente.',
  },
  arr: {
    title: 'ARR (Annual Recurring Revenue)',
    definition: 'A receita recorrente anualizada. É simplesmente o MRR multiplicado por 12.',
    formula: 'ARR = MRR × 12',
    interpretation: <p className="text-sm">O ARR oferece uma perspectiva de longo prazo da escala do negócio.</p>,
    getValue: (kpis) => formatCurrency(kpis.MRR_Final * 12),
    getRecommendation: (kpis) => 'Use o ARR para comunicar a escala do seu negócio a investidores e para planejamento de longo prazo.',
  },
  churn: {
    title: 'Taxa de Churn',
    definition: 'A porcentagem de clientes ou receita que cancelaram suas assinaturas em um determinado período.',
    formula: 'Churn de Receita = (MRR perdido no mês / MRR no início do mês) %',
    interpretation: (
       <ul className="space-y-2 text-sm">
        <li><Badge className="mr-2 bg-green-100 text-green-800">{'< 3%'}</Badge>Excelente para B2B SaaS.</li>
        <li><Badge variant="secondary" className="mr-2">{'3% - 7%'}</Badge>Aceitável, mas com espaço para melhorias.</li>
        <li><Badge variant="destructive" className="mr-2">{'> 7%'}</Badge>Pode indicar problemas sérios.</li>
      </ul>
    ),
    getValue: (kpis) => `${(kpis.Taxa_Churn_Media * 100).toFixed(1)}%`,
    getRecommendation: (kpis) => kpis.Taxa_Churn_Media > 0.05 ? 'Churn alto é um vazamento no seu balde. Foque em entender os motivos de cancelamento e em melhorar a retenção.' : 'Seu churn está saudável. Continue monitorando e engajando seus clientes.',
  },
  ltv_cac: {
    title: 'Relação LTV/CAC',
    definition: 'Compara o valor de um cliente (LTV) com o custo para adquiri-lo (CAC).',
    formula: 'LTV / CAC',
    interpretation: (
      <ul className="space-y-2 text-sm">
        <li><Badge variant="destructive" className="mr-2">{'< 1x'}</Badge>Insustentável.</li>
        <li><Badge variant="secondary" className="mr-2">{'1x - 3x'}</Badge>Pouca margem para escalar.</li>
        <li><Badge className="mr-2 bg-green-100 text-green-800">{'3x - 5x'}</Badge>Modelo de negócio saudável.</li>
        <li><Badge className="mr-2 bg-blue-100 text-blue-800">{'> 5x'}</Badge>Excelente. Reinvista em marketing.</li>
      </ul>
    ),
    getValue: (kpis) => `${kpis.LTV_CAC_Ratio_Final.toFixed(1)}x`,
    getRecommendation: (kpis) => kpis.LTV_CAC_Ratio_Final < 3 ? 'A relação LTV/CAC está baixa. Otimize seus canais de aquisição ou trabalhe para aumentar o LTV.' : 'Ótima eficiência de aquisição. Considere escalar os investimentos em canais com bom desempenho.',
  },
  // ... (outras métricas com getValue e getRecommendation)
  ltv: { title: 'LTV', definition: 'O valor total que um cliente gera.', formula: 'LTV = ARPU / Taxa de Churn', interpretation: <p>Ajuda a determinar quanto você pode gastar para adquirir um cliente.</p>, getValue: (kpis) => formatCurrency(kpis.LTV_Final), getRecommendation: (kpis) => 'Aumente o LTV melhorando o produto, aumentando o ARPU com upsells ou reduzindo o churn.' },
  cac: { title: 'CAC', definition: 'O custo para adquirir um novo cliente.', formula: 'CAC = (Custo de Vendas & Marketing) / (Novos Clientes)', interpretation: <p>Deve ser sempre analisado em conjunto com o LTV.</p>, getValue: (kpis) => formatCurrency(kpis.CAC_Medio_Periodo), getRecommendation: (kpis) => 'Otimize seus canais de marketing e funil de vendas para reduzir o CAC.' },
  gross_margin: { title: 'Margem Bruta', definition: 'A porcentagem da receita que resta após subtrair o COGS.', formula: 'Margem Bruta = (Receita Total - COGS) / Receita Total', interpretation: <ul className="space-y-2 text-sm"><li><Badge className="mr-2 bg-green-100 text-green-800">{'> 80%'}</Badge>Típico de SaaS.</li><li><Badge variant="secondary" className="mr-2">{'60% - 80%'}</Badge>Saudável.</li><li><Badge variant="destructive" className="mr-2">{'< 60%'}</Badge>Pode indicar altos custos.</li></ul>, getValue: (kpis) => 'N/A', getRecommendation: (kpis) => 'Reduza custos de infraestrutura ou suporte para aumentar a margem.' },
  runway: { title: 'Runway', definition: 'O número de meses que a empresa pode operar antes de ficar sem dinheiro.', formula: 'Runway = Saldo de Caixa / Burn Rate Mensal', interpretation: <ul className="space-y-2 text-sm"><li><Badge variant="destructive" className="mr-2">{'< 6 meses'}</Badge>Zona de perigo.</li><li><Badge variant="secondary" className="mr-2">{'6 - 12 meses'}</Badge>Atenção.</li><li><Badge className="mr-2 bg-green-100 text-green-800">{'> 18 meses'}</Badge>Posição segura.</li></ul>, getValue: (kpis) => `${kpis.Runway_Meses} meses`, getRecommendation: (kpis) => kpis.Runway_Meses < 12 ? 'Seu runway está curto. É hora de focar em lucratividade ou buscar novo investimento.' : 'Com um runway saudável, você tem flexibilidade para focar no crescimento de longo prazo.' },
  ebitda: { title: 'EBITDA', definition: 'Lucro antes de Juros, Impostos, Depreciação e Amortização.', formula: 'EBITDA = Lucro Líquido + Juros + Impostos + Depreciação + Amortização', interpretation: <p>Aproximação do fluxo de caixa operacional.</p>, getValue: (kpis) => 'N/A', getRecommendation: (kpis) => 'Um EBITDA positivo e crescente indica uma operação principal saudável e lucrativa.' },
  users: { title: 'Usuários', definition: 'O número total de clientes pagantes ativos.', interpretation: <p>O crescimento da base de usuários é um indicador chave da tração do produto.</p>, getValue: (kpis) => formatNumber(kpis.Usuarios_Final), getRecommendation: (kpis) => 'Analise os canais que trazem os melhores clientes e otimize o funil de conversão.' },
  break_even: { title: 'Break-Even Point', definition: 'O ponto em que a receita total se iguala aos custos totais.', interpretation: <p>Alcançar o break-even é um marco crucial para a sustentabilidade.</p>, getValue: (kpis) => `Mês ${kpis.Breakeven_Month}`, getRecommendation: (kpis) => 'Após o break-even, o foco muda de sobrevivência para crescimento lucrativo.' },
  avg_cac: { title: 'CAC Médio', definition: 'O custo médio para adquirir um único cliente novo.', formula: 'CAC = (Custo de Vendas & Marketing) / (Novos Clientes)', interpretation: <p>Monitorar o CAC médio ajuda a entender a eficiência dos canais de aquisição.</p>, getValue: (kpis) => formatCurrency(kpis.CAC_Medio_Periodo), getRecommendation: (kpis) => 'Teste novos canais e otimize os existentes para manter o CAC sob controle enquanto escala.' },
};

export const GlossaryModal = ({ term, isOpen, onClose, kpis }: GlossaryModalProps) => {
  const content = term ? GLOSSARY_CONTENT[term] : null;
  const currentValue = term && kpis ? content?.getValue(kpis) : 'N/A';
  const recommendation = term && kpis ? content?.getRecommendation(kpis) : 'N/A';

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-lg">
        {content ? (
          <>
            <DialogHeader>
              <DialogTitle className="text-2xl">{content.title}</DialogTitle>
              <DialogDescription>{content.definition}</DialogDescription>
            </DialogHeader>
            <div className="py-4 space-y-6">
              {content.formula && (
                <div>
                  <h4 className="font-semibold text-slate-800 mb-2">Fórmula</h4>
                  <code className="text-sm bg-slate-100 p-2 rounded-md block w-full text-left">{content.formula}</code>
                </div>
              )}
              <div>
                <h4 className="font-semibold text-slate-800 mb-2">Interpretação</h4>
                {content.interpretation}
              </div>
              
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">Seu Valor Atual</h4>
                <p className="text-2xl font-bold text-blue-800 font-mono">{currentValue}</p>
              </div>

              <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                 <h4 className="font-semibold text-amber-900 mb-2 flex items-center gap-2">
                    <Lightbulb size={18} />
                    Ação Recomendada
                </h4>
                <p className="text-sm text-amber-800">{recommendation}</p>
              </div>

            </div>
          </>
        ) : (
          <DialogHeader>
            <DialogTitle>Termo não encontrado</DialogTitle>
          </DialogHeader>
        )}
      </DialogContent>
    </Dialog>
  );
};
