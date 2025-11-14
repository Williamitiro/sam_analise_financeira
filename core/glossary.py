# 📚 SAM Financial Model - Glossary.py
# Glossário Completo de Jargões Financeiros para Investidores, CEOs e Analistas

"""
Este arquivo centraliza todas as explicações de termos financeiros usados no modelo.
Cada termo tem 4 níveis de explicação: leigo, executivo, investidor e analista.
É usado pelo app.py para gerar tooltips e ajudas contextuais.
"""

from typing import Dict, Any

# Estrutura de cada entrada do glossário
JARGOES_FINANCEIROS: Dict[str, Dict[str, Any]] = {
    
    # ============================================================================
    # 📊 RECEITA E MÉTRICAS DE RECEITA
    # ============================================================================
    
    "MRR": {
        "termo": "Monthly Recurring Revenue",
        "sigla": "MRR",
        "layman": "É a soma de todo dinheiro que entra no seu caixa todo mês, de forma recorrente. Se você tem 10 clientes pagando R$100/mês, seu MRR é R$1.000. Se você tem 100 clientes pagando R$50/mês, seu MRR é R$5.000. É a métrica mais importante de um SaaS.",
        "executive": "MRR representa a receita previsível e recorrente mensal. É o indicador principal de saúde do negócio porque mostra o tamanho real da operação recorrente, ignorando receitas eventuais. Crescimento saudável de MRR = crescimento saudável do negócio. Meta: crescer 10-15% ao mês no estágio inicial.",
        "investor": "MRR é a base para valuation de SaaS. Empresas saudáveis são vendidas por 5x a 15x o ARR (MRR × 12). Um MRR crescente com baixo churn indica viabilidade de escala. No Brasil, SaaS B2B com MRR acima de R$100k atrai Series A.",
        "analyst": "MRR = Σ(receita mensal de todos os clientes ativos). Não inclui receita one-time (implementação, treinamento). Deve ser segmentado por planos para análise de mix. Variação MRR = Novos clientes + Expansão - Churn - Contrações.",
        "formula": "MRR = Σ(ARPU de cada cliente ativo no mês)",
        "importancia": "Alta - É o indicador vital do negócio SaaS",
        "benchmark": "Early-stage SaaS: R$10k-50k MRR | Growth-stage: R$100k-500k MRR | Late-stage: >R$1M MRR"
    },
    
    "ARPU": {
        "termo": "Average Revenue Per User",
        "sigla": "ARPU",
        "layman": "É a média de quanto cada cliente te paga por mês. Se você tem R$10.000 de receita e 100 clientes, seu ARPU é R$100. Se você tem clientes em planos diferentes (R$50, R$100, R$200), o ARPU é a média ponderada de todos.",
        "executive": "ARPU mostra o poder de monetização do seu produto. ARPU baixo pode indicar que você está subprecificado ou atuando em um mercado de baixo poder aquisitivo. ARPU alto exige serviço premium e retenção forte. Meta: aumentar ARPU via upsell e planos maiores.",
        "investor": "ARPU impacta diretamente o LTV e a viabilidade do CAC. No mercado brasileiro, SaaS B2B tem ARPU médio de R$150-800. SaaS B2C tem ARPU de R$30-100. ARPU crescente >5% ao mês é sinal de product-market fit forte.",
        "analyst": "ARPU = MRR ÷ Número de Clientes Ativos. Deve ser analisado em conjunto com CAC: LTV = (ARPU × Margem Bruta) ÷ Churn. Segmentação ARPU por canal de aquisição revela eficiência.",
        "formula": "ARPU = MRR ÷ Usuários Pagantes",
        "importancia": "Alta - Diretamente impacta LTV e viabilidade do modelo",
        "benchmark": "B2B SaaS no Brasil: R$150-500 | B2C SaaS: R$30-80 | Fintech SaaS: R$200-800"
    },
    
    "ARR": {
        "termo": "Annual Recurring Revenue",
        "sigla": "ARR",
        "layman": "É seu MRR multiplicado por 12 meses. Se seu MRR é R$10.000, seu ARR é R$120.000. É usado para falar com investidores em números maiores e por isso é padrão no mercado global.",
        "executive": "ARR é a métrica de valuation primária. Investidores usam múltiplos de ARR para precificar rodadas. Um SaaS saudável cresce ARR 3x ao ano nos estágios iniciais. ARR previsível garante planejamento estratégico.",
        "investor": "Valuation padrão: 5x-15x ARR dependendo de crescimento, churn e margem. ARR R$1M+ + crescimento >100% YoY + LTV/CAC >3x = valuation premium. No Brasil, desconto de 20-30% vs. EUA por risco país.",
        "analyst": "ARR = MRR × 12. Não inclui receita não-recorrente. Para valuation, desconte churn futuro projetado. Use ARR como base para calcular run-rate e projetar valuation em rodadas.",
        "formula": "ARR = MRR × 12",
        "importancia": "Máxima - Métrica de valuation primária",
        "benchmark": "Early: R$120k-600k ARR | Series A: R$3M-6M ARR | Late: R$10M+ ARR"
    },
    
    # ============================================================================
    # 💰 CUSTOS E MARGENS
    # ============================================================================
    
    "COGS": {
        "termo": "Cost of Goods Sold",
        "sigla": "COGS",
        "layman": "É tudo que você paga DIRETAMENTE para entregar o serviço ao cliente. Se você vende um bolo, é a farinha, ovos e açúcar. No seu SaaS: taxas de pagamento (Stripe), custo da API de IA (OpenAI), e parte da infraestrutura que cresce com cada usuário novo.",
        "executive": "COGS são custos variáveis essenciais. No SaaS, include: taxas de gateway, custos de infraestrutura escalável, suporte direto ao cliente. Meta: manter COGS abaixo de 30-40% da receita. Se COGS está alto, você tem problema de eficiência técnica ou está subprecificado.",
        "investor": "COGS impacta margem bruta gross profit. SaaS saudável tem margem bruta >70-80%. COGS alto (>40% da receita) indica dependência de terceiros caros ou infraestrutura mal otimizada. Red flag para investidores.",
        "analyst": "COGS = Custo Direto de Entrega. Para SaaS: infra variável + taxas de pagamento + comissões + custos de sucesso do cliente direto. NÃO inclui marketing, salários de dev, escritório. Margem Bruta = (Receita - COGS) ÷ Receita.",
        "formula": "COGS = Custo_Infra_Var + Taxas_Pagamento + Comissões",
        "importancia": "Máxima - Define margem bruta e LTV",
        "benchmark": "Meta: <30% da receita | SaaS eficiente: 15-25% | Red flag: >40%"
    },
    
    "OPEX": {
        "termo": "Operating Expenditures",
        "sigla": "OPEX",
        "layman": "São os custos para manter a empresa funcionando: salários, aluguel, contador, ferramentas (Notion, GitHub), marketing, seu salário. São fixos (não mudam muito se você ganha mais clientes) e essenciais para a operação.",
        "executive": "OPEX inclui todos os custos operacionais: pessoal, marketing, ferramentas, serviços profissionais, escritório. Meta: OPEX deve ser coberto pelo Lucro Bruto (MRR - COGS). Se Lucro Bruto < OPEX, você está em burn mode. Planejamento de OPEX define burn rate e runway.",
        "investor": "OPEX controlado é sinal de eficiência. Early-stage SaaS deve ter OPEX baixo (lean). Ao crescer, OPEX cresce mais devagar que receita (economias de escala). CAC está incluído em OPEX (marketing), então LTV/CAC > 3x compensa OPEX saudável.",
        "analyst": "OPEX = Soma de todos custos operacionais não-diretos. Inclui: S&M (inclui CAC), R&D (salários de dev), G&A (administrativo). Efficiency Ratio = (S&M + R&D) ÷ Receita. Meta: <60% para SaaS eficiente. Burn rate = OPEX - Lucro Bruto.",
        "formula": "OPEX = Salários + Marketing + Ferramentas + Escritório + Serviços + Depreciação",
        "importancia": "Alta - Define burn rate e eficiência operacional",
        "benchmark": "Early: R$20k-80k/mês | Growth: R$100k-300k/mês | Meta: OPEX cresce <50% do crescimento de receita"
    },
    
    "CAPEX": {
        "termo": "Capital Expenditures",
        "sigla": "CAPEX",
        "layman": "É dinheiro que você gasta para comprar coisas que vão durar muito tempo: computadores, móveis, equipamentos. Não vai pro resultado do mês todo de uma vez, é 'amortizado' (dividido) ao longo dos meses. Seu 'capital inicial' é CAPEX.",
        "executive": "CAPEX são investimentos em ativos físicos ou intangíveis com vida útil >1 ano. No SaaS: equipamentos de dev, infraestrutura inicial, softwares permanentes. Impacta caixa no momento da compra, mas resultado é diluído na depreciação mensal. Planeje CAPEX para não quebrar o caixa.",
        "investor": "CAPEX baixo é característica de SaaS (modelo asset-light). Alto CAPEX pode indicar modelo não-puro de SaaS ou necessidade de infraestrutura própria. Red flag: CAPEX > 20% do ARR. Ideal: CAPEX mínimo, foco em OPEX escalável.",
        "analyst": "CAPEX é capitalizado e amortizado. Taxa de depreciação define impacto mensal no P&L. Cash Flow Statement: CAPEX é desembolso de caixa. No modelo financeiro, CAPEX inicial é saída de caixa mês 0. Meta: CAPEX < 10% do ARR anual.",
        "formula": "Depreciação Mensal = Valor CAPEX ÷ Vida Útil (meses)",
        "importancia": "Média - SaaS ideal tem CAPEX mínimo",
        "benchmark": "SaaS puro: <5% do ARR | SaaS com infra: 5-15% do ARR"
    },
    
    "Margem_Bruta": {
        "termo": "Margem Bruta",
        "sigla": "Gross Margin",
        "layman": "É a porcentagem de dinheiro que 'sobra' depois de pagar os custos diretos (COGS). Se você vende R$100 e paga R$30 de COGS, sua margem bruta é 70%. Quanto mais alta, mais dinheiro sobra para pagar salários e marketing.",
        "executive": "Margem Bruta = (Receita - COGS) ÷ Receita. Meta para SaaS: >70-80%. Margem baixa (<60%) indica problema de precificação ou custos variáveis muito altos. Margem alta dá flexibilidade para investir em crescimento via OPEX.",
        "investor": "Margem Bruta é fator de valuation. SaaS com margem >75% vale múltiplos maiores porque tem capacidade de gerar lucro operacional ao escalar. Margem <60% é red flag: modelo não-escalável ou dependência de custos externos.",
        "analyst": "Gross Margin = (Revenue - COGS) ÷ Revenue. Benchmark SaaS: 70-85%. Margem estável ou crescente com growth é ideal. Se margem cai com escala, investigate: COGS crescendo mais rápido que receita indica falha na arquitetura de custos.",
        "formula": "Margem Bruta = ((Receita - COGS) ÷ Receita) × 100",
        "importancia": "Máxima - Define capacidade de lucro",
        "benchmark": "Meta: >75% | SaaS excelente: 80-85% | Red flag: <60%"
    },
    
    # ============================================================================
    # 📈 MÉTRICAS DE AQUISIÇÃO E FUNIL
    # ============================================================================
    
    "CAC": {
        "termo": "Customer Acquisition Cost",
        "sigla": "CAC",
        "layman": "Quanto dinheiro você gasta para conquistar UM cliente novo. Se você gasta R$5.000 em anúncios e conquista 10 clientes, seu CAC é R$500. Quanto mais baixo, mais eficiente é sua máquina de vendas.",
        "executive": "CAC = Custo total de Marketing e Vendas ÷ Novos clientes no período. Meta: CAC < 1/3 do LTV. CAC alto pode ser compensado por LTV muito alto, mas retenção deve ser excelente. CAC pago via marketing vs. CAC orgânico (referral) devem ser medidos separadamente.",
        "investor": "CAC é fator crítico de investimento. SaaS B2B no Brasil: CAC ideal R$300-800. CAC > R$1.500 exige LTV > R$4.500 e churn < 3% ao mês. Se CAC está subindo ao longo do tempo, mercado está ficando saturado ou concorrência aumentou. Red flag: CAC crescendo mais rápido que ARPU.",
        "analyst": "CAC = (Marketing + Vendas) ÷ ClientesNovos. Deve ser segmentado por canal (Google Ads, Facebook, SEO). CAC Payback = CAC ÷ (ARPU × Margem Bruta). Meta: Payback < 12 meses. CAC recovery rate > 100% em 12 meses é saudável.",
        "formula": "CAC = Custo_Aquisição ÷ Novos_Clientes",
        "importancia": "Máxima - Define eficiência de crescimento",
        "benchmark": "B2B SaaS: R$300-800 | B2C SaaS: R$50-150 | Meta: CAC < 1/3 do LTV"
    },
    
    "LTV": {
        "termo": "Lifetime Value",
        "sigla": "LTV",
        "layman": "É o total de dinheiro que um cliente te paga durante toda a relação com ele. Se ele paga R$100/mês e fica 15 meses, LTV = R$1.500. Quanto maior o LTV, mais você pode gastar para conquistar clientes (CAC).",
        "executive": "LTV = (ARPU × Margem Bruta) ÷ Churn. Meta: LTV > 3x CAC. LTV alto é resultado de retenção forte e ARPU saudável. Se churn é alto, LTV destrói o modelo. Foque em retenção e expansão de receita para aumentar LTV sem aumentar CAC.",
        "investor": "LTV é a métrica de valuation mais importante. SaaS com LTV > R$3.000 e churn < 5% é altamente atrativo. LTV crescente com churn decrescente é holy grail. LTV estagnado = estagnamento do negócio. Red flag: LTV caindo enquanto ARPU sobe (churn explosivo).",
        "analyst": "LTV = (ARPU × Margem Bruta) ÷ Churn Mensal. Para análise robusta, calcule LTV com churn real, não assumido. LTV não deve exceder 3 anos de ARPU (coorte que fica >3 anos é rara). LTV/CAC ratio é derivada deste KPI.",
        "formula": "LTV = ((ARPU - COGS) × (1 ÷ Churn))",
        "importancia": "Máxima - Define valor do cliente e viabilidade do modelo",
        "benchmark": "Meta: LTV > 3x CAC | SaaS B2B: R$1.500-5.000 | SaaS B2C: R$300-800"
    },
    
    "Churn": {
        "termo": "Taxa de Cancelamento",
        "sigla": "Churn",
        "layman": "É a porcentagem de clientes que você PERDE todo mês. Se você tem 100 clientes e perde 4, seu churn é 4% ao mês. Churn é o VILÃO do SaaS. Um churn de 5% ao mês significa que você perde metade dos clientes ao ano!",
        "executive": "Churn Mensal = ClientesCancelados ÷ ClientesIniciais. Meta: <3% ao mês para B2B, <5% para B2C. Churn alto destrói LTV e torna crescimento impossível. Foque 50% do esforço em retenção e sucesso do cliente. Churn pode ser 'logo churn' (cancela rápido) ou 'maturity churn' (depois de muito tempo).",
        "investor": "Churn é o maior red flag. Investidores exigem churn <5% ao mês para SaaS B2B brasileiro. Churn >7% ao mês = modelo quebrado. Churn negativo (expansão > cancelamentos) é holy grail. Pergunte sempre: churn por coorte, churn por plano, churn por tamanho de cliente.",
        "analyst": "Churn = Cancelamentos ÷ ClientesIniciais. Deve ser calculado por coorte (clientes que entraram no mesmo mês). Churn bruto vs. líquido (incluindo expansão). Analise churn nos primeiros 90 dias vs. churn de clientes maduros. Red flag: churn crescente ao longo das coortes.",
        "formula": "Churn = (Clientes_Perdiu_Mês ÷ Clientes_Tinha_No_Início_Mês) × 100",
        "importancia": "Máxima - Maior inimigo do SaaS",
        "benchmark": "Meta B2B: <3% ao mês | Meta B2C: <5% ao mês | >7% = modelo falho"
    },
    
    "Taxa_Conversao": {
        "termo": "Taxa de Conversão",
        "sigla": "Conversion Rate",
        "layman": "É a porcentagem de pessoas que passam de uma etapa para outra no seu funil. Se 100 pessoas entram no site e 5 viram trial, sua taxa é 5%. Se 20 trials viram pagantes, sua taxa é 20%. Taxas baixas = funil ineficiente.",
        "executive": "Acompanhe duas taxas principais: Visitante→Trial e Trial→Pagante. Meta: 3-8% para primeira, 15-25% para segunda. Taxas baixas indicam problema de product-market fit, preço alto, ou comunicação confusa. Otimize o funil antes de escalar marketing.",
        "investor": "Taxa de conversão define CAC. Se pagou R$5 para atrair um visitante e taxa é 5%→20%, CAC = R$5 ÷ (0.05×0.20) = R$500. Taxas estáveis com escala indicam mercado saudável. Taxas caindo com escala = sinal de saturação.",
        "analyst": "Conversão deve ser calculada por canal. Google Ads tem conversão diferente de SEO. Analise conversão em 7, 14, 30 dias de trial. Trial→Pagante <15% é red flag. >30% é excelente. A/B teste constante nas páginas de conversão.",
        "formula": "Taxa = (Pessoas_Que_Passaram_Etapa ÷ Pessoas_Que_Tentaram) × 100",
        "importancia": "Alta - Define eficiência do funil e CAC",
        "benchmark": "Visitante→Trial: 3-8% | Trial→Pagante: 15-25%"
    },
    
    "LTV_CAC_Ratio": {
        "termo": "Relação LTV sobre CAC",
        "sigla": "LTV/CAC",
        "layman": "Divide quanto o cliente te paga (LTV) por quanto você gastou para conquistá-lo (CAC). Se LTV é R$1.500 e CAC é R$500, ratio é 3x. Meta mínima: 3x. Se for 1x, você só recupera o investimento, sem lucro.",
        "executive": "LTV/CAC = Margem bruta por cliente ÷ Custo de aquisição. Meta: >3x. <2x = modelo insustentável. >5x = oportunidade de escalar agressivamente. Mantenha este ratio estável ao escalar. Se CAC sobe, aumente retenção ou ARPU para manter ratio saudável.",
        "investor": "LTV/CAC >3x é non-negotiable para investimento. Se ratio está caindo com escala, mercado está saturando. Se ratio >4x e crescendo, invista pesado. Red flag: ratio <2.5x mesmo com otimizações de marketing.",
        "analyst": "LTV/CAC = ((ARPU × Margem Bruta) ÷ Churn) ÷ CAC. Deve ser >3x. Analise por canal: canais com ratio >4x merecem mais budget. Canais com ratio <2x devem ser cortados. Ratio estável com escala indica mercado eficiente.",
        "formula": "LTV/CAC = LTV ÷ CAC",
        "importancia": "Máxima - Métrica de saúde do modelo de negócio",
        "benchmark": "Meta mínima: 3.0x | Saudável: 3.5-5.0x | Excelente: >5.0x"
    },
    
    "CAC_Payback": {
        "termo": "Tempo de Retorno do CAC",
        "sigla": "CAC Payback",
        "layman": "Em quantos meses você recupera o dinheiro gasto para conquistar um cliente. Se CAC é R$500 e cliente paga R$100 líquido/mês, payback é 5 meses. Meta: <12 meses para SaaS B2B.",
        "executive": "CAC Payback = CAC ÷ (ARPU × Margem Bruta). Meta: 6-12 meses. >18 meses = risco de fluxo de caixa. <6 meses = oportunidade de crescer mais rápido. Payback curto + LTV/CAC alto = modelo perfeito para investir pesado.",
        "investor": "Payback >12 meses em SaaS B2B é red flag. Exige muito capital para crescer. Payback <8 meses + churn baixo = investir agressivamente. Analise payback por canal: canais com payback <6 meses são ouro.",
        "analyst": "CAC Payback = CAC ÷ ((ARPU - COGS) × (1 - Impostos)). Deve ser <12 meses. Cash flow de SaaS pode ser negativo mesmo com payback bom se churn é alto. Payback deve ser analisado com churn: payback 6 meses + churn 5% ao mês = problema.",
        "formula": "CAC Payback (meses) = CAC ÷ ((ARPU - COGS) × (1 - Taxa_Impostos))",
        "importancia": "Máxima - Define necessidade de capital e viabilidade de crescimento",
        "benchmark": "Meta: <12 meses | Ideal: 6-8 meses | Red flag: >18 meses"
    },
    
    # ============================================================================
    # 💸 FLUXO DE CAIXA E VIABILIDADE
    # ============================================================================
    
    "Break_Even": {
        "termo": "Ponto de Equilíbrio Operacional",
        "sigla": "Break-Even",
        "layman": "É o momento em que sua receita cobre todos os custos (fixos e variáveis) e você para de ter prejuízo. Antes do break-even você perde dinheiro todo mês. Depois, começa a gerar lucro operacional.",
        "executive": "Break-Even = Mês onde Resultado Operacional passa de negativo para positivo. É diferente de payback. Break-even depende de cobrir OPEX com Lucro Bruto. Se quebra-even é mês 15, você precisa capital para sobreviver 15 meses. Meta: <18 meses para SaaS.",
        "investor": "Break-even >24 meses = necessita muito capital e risco elevado. Break-even <12 meses = modelo eficiente e capital eficiente. Analise break-even vs. runway: se runway é 18 meses e break-even é mês 20, falta capital.",
        "analyst": "Break-Even Point = Fixed Costs ÷ (Price - Variable Cost per Unit). No modelo, é o primeiro mês com Resultado Operacional > 0. Deve ser analisado junto com saldo de caixa: break-even sem caixa positivo ainda requer capital. Red flag: break-even > runway.",
        "formula": "Break-Even (meses) = Primeiro mês com Resultado_Operacional > 0",
        "importancia": "Alta - Define necessidade de capital e timeline de viabilidade",
        "benchmark": "Meta: <18 meses | Ideal: 12-15 meses | Red flag: >24 meses"
    },
    
    "Runway": {
        "termo": "Prazo de Voo (até o fim do caixa)",
        "sigla": "Runway",
        "layman": "Quantos meses de dinheiro você ainda tem no banco antes que o caixa fique zero. Se tem R$100k no banco e queima R$10k/mês, seu runway é 10 meses. Meta: >12 meses de runway sempre.",
        "executive": "Runway = Saldo_Caixa_Atual ÷ Burn_Rate_Mensal. Se burn rate é R$15k/mês e saldo é R$100k, runway = 6,6 meses. Meta: manter 12-18 meses de runway. Se runway <6 meses, é hora de capitar URGENTE ou cortar custos.",
        "investor": "Runway <12 meses = red flag. Investidor quer ver capital para 18-24 meses de operação. Se runway está curto e crescimento é lento, é emergência. Se runway está curto mas crescimento é acelerado, pode valer a pena injetar mais capital.",
        "analyst": "Runway = Liquidez ÷ Burn Rate. Deve ser calculado com burn rate médio dos últimos 3 meses. Para modelagem, use burn rate projetado. Se modelo mostra saldo negativo em mês 20, runway = 19 meses. Red flag: runway <6 meses sem plano de captação.",
        "formula": "Runway = Saldo_Atual ÷ Burn_Rate",
        "importancia": "Crítica - Define sobrevivência da empresa",
        "benchmark": "Meta: 12-18 meses | Mínimo: 6 meses | Red flag: <3 meses"
    },
    
    "Vale_da_Morte": {
        "termo": "Vale da Morte (Menor Saldo de Caixa)",
        "sigla": "Vale da Morte",
        "layman": "É o momento mais crítico da empresa: quando seu saldo de caixa está no ponto mais baixo (mais negativo). É o pior momento financeiramente. Se você precisa de R$50k para sobreviver até o break-even, seu vale da morte é -R$50k.",
        "executive": "Vale da Morte = Saldo_Caixa mínimo durante a projeção. Define capital necessário. Se vale da morte é -R$200k, você precisa R$200k de capital + buffer de segurança. Meta: ter acesso a 1,3x o vale da morte em capital.",
        "investor": "Vale da morte define cheque mínimo do investidor. Se vale é -R$300k, investidor sabe que precisa investir pelo menos R$300k. Se vale é muito profundo, modelo é capital intensive e risco aumenta. Prefira modelos com vale raso (<R$500k).",
        "analyst": "Vale da Morte = MIN(Saldo_Caixa_Projetado). Deve ser acompanhado de mês onde ocorre. Se vale ocorre no mês 8 e break-even é mês 18, modelo tem 10 meses de burn pós-vale. Buffer recomendado: 30-50% acima do vale.",
        "formula": "Vale_da_Morte = MIN(projeção['Saldo_Caixa'])",
        "importancia": "Crítica - Define capital mínimo necessário",
        "benchmark": "Meta: <R$500k para startups early-stage | <R$2M para growth-stage"
    },
    
    "Burn_Rate": {
        "termo": "Taxa de Queima de Caixa",
        "sigla": "Burn Rate",
        "layman": "Quanto dinheiro você PERDE todo mês. Se começa o mês com R$100k, termina com R$90k, seu burn rate é R$10k/mês. Burn rate positivo = lucro, negativo = prejuízo.",
        "executive": "Burn Rate = Fluxo de Caixa negativo. Deve ser monitorado semanalmente. Meta: reduzir burn rate ao longo do tempo via aumento de receita, não apenas corte de custos. Se burn rate está crescente, investigue: crescimento acelerado ou ineficiência?",
        "investor": "Burn rate define capital necessário. Investidor quer ver burn rate decrescente ou estável com crescimento. Burn rate crescente sem crescimento de MRR = red flag. Burn rate >R$100k/mês em early-stage = capital intensive demais.",
        "analyst": "Burn Rate = Saldo_Final_Mês - Saldo_Inicial_Mês (negativo). Calcule burn rate médio móvel de 3 meses para suavizar variações. Gross Burn = OPEX total. Net Burn = OPEX - Receita. Meta: Net Burn < 50% do crescimento de MRR.",
        "formula": "Burn_Rate = Fluxo_Caixa (se negativo)",
        "importancia": "Crítica - Define capital e sobrevivência",
        "benchmark": "Early: R$10k-30k/mês | Growth: R$30k-100k/mês | Red flag: >R$150k/mês sem MRR proporcional"
    },
    
    # ============================================================================
    # 📉 INDICADORES DE RETENÇÃO
    # ============================================================================
    
    "Retencao": {
        "termo": "Taxa de Retenção",
        "sigla": "Retention Rate",
        "layman": "O oposto do churn. É a porcentagem de clientes que você CONSERVA. Se churn é 4%, retenção é 96%. Retenção alta = clientes amam seu produto.",
        "executive": "Retenção = 1 - Churn. Meta: >95% para B2B, >90% para B2C. Retenção por coorte é mais importante que retenção geral. Se retenção nos primeiros 90 dias é alta, product-market fit está bom. Se retenção de clientes antigos cai, seu produto está defasando.",
        "investor": "Retenção é fator de qualidade do negócio. Retenção >95% é excelente, mostra que cliente não larga. <85% é problemático. Retenção estável com coortes antigas + crescimento de novas = modelo perfeito. Red flag: retenção caindo em todas as coortes.",
        "analyst": "Retenção Mensal = 1 - Churn. Retenção Acumulada = Π(1 - Churn_Mensal). Analise retenção em dias 1, 7, 30, 90, 365. Identifique 'cliff' onde retenção cai. Meta: retenção D90 > 70%.",
        "formula": "Retenção = 1 - Churn",
        "importancia": "Máxima - Define LTV e viabilidade do modelo",
        "benchmark": "B2B: >96% = excelente | 90-95% = bom | <85% = problemático"
    },
    
    "Coorte": {
        "termo": "Análise por Coorte",
        "sigla": "Cohort Analysis",
        "layman": "É agrupar clientes pelo mês que eles entraram e ver como cada grupo se comporta ao longo do tempo. Ex: 'clientes de janeiro' vs 'clientes de fevereiro'. Mostra se sua retenção está melhorando ou piorando.",
        "executive": "Cohorts mostram evolução da qualidade do cliente. Se coorte de janeiro tinha retenção 95% e coorte de junho tem 90%, algo mudou (produto, cliente, concorrência). Cohorts permitem prever churn futuro e LTV mais acurado. Exija relatório de cohorts mensal.",
        "investor": "Cohorts são essenciais para due diligence. Investidor quer ver cohorts melhorando ao longo do tempo. Se cohorts antigas têm churn crescente, modelo está envelhecendo. Se cohorts novas têm churn menor, produto está melhorando. Red flag: todas as cohorts convergindo para churn alto.",
        "analyst": "Cohort table: linhas = mês de aquisição, colunas = meses de vida. Valor = % de clientes remanescentes. Analise curvature da linha de retenção. Meta: cohorts estabilizando >70% em 12 meses. Cohorts B2B devem ser mais estáveis que B2C.",
        "formula": "Coorte_MêsX_MêsY = (Clientes_MêsX_ainda_ativos_em_MêsY ÷ Clientes_MêsX) × 100",
        "importancia": "Alta - Detecta problemas de retenção antes que sejam aparentes",
        "benchmark": "Meta: cohorts estáveis >80% em 6 meses | >70% em 12 meses"
    },
    
    # ============================================================================
    # 💼 INDICADORES DE CAPITAL E VALUATION
    # ============================================================================
    
    "Valuation": {
        "termo": "Valuation (Precificação da Empresa)",
        "sigla": "Valuation",
        "layman": "É quanto sua empresa vale. No estágio inicial, investidor usa múltiplos do ARR. Se seu ARR é R$1M e múltiplo é 5x, valuation é R$5M. Múltiplo depende de crescimento, churn e margem.",
        "executive": "Valuation = ARR × Múltiplo. Múltiplo varia 3x-15x dependendo de: (1) Crescimento (>100% YoY = múltiplo alto), (2) Churn (<5% = múltiplo alto), (3) Margem (>70% = múltiplo alto), (4) Tamanho do mercado. Se valuation não faz sentido, captação é difícil.",
        "investor": "Valuation é negociação baseada em ARR, crescimento e qualidade. Early-stage: 3-7x ARR. Growth-stage: 7-15x ARR. No Brasil, desconto de 20-30% vs. EUA. Valuation é o que você consegue negociar, não apenas matemática. Red flag: valuation >10x ARR com churn >5%",
        "analyst": "Valuation = ARR × Revenue Multiple. Multiple = f(growth, retention, margin, TAM, SOM, SAM). Use comps de mercado para múltiplo. Desconto de país (Brazil Risk) = 20-30%. Liquidity discount para startups = 30-50%. Valuation justo = múltiplo de comps ajustado para qualidade.",
        "formula": "Valuation = ARR × Múltiplo",
        "importancia": "Crítica - Define diluição e capital levantado",
        "benchmark": "Early-stage: 3-7x ARR | Growth: 7-15x ARR | Brasil: -20% vs. EUA"
    },
    
    "Run_Rate": {
        "termo": "Run Rate (Receita Anualizada)",
        "sigla": "Run Rate",
        "layman": "É a projeção anual baseada no mês atual. Se seu MRR deste mês é R$10k, seu run rate é R$120k ao ano. Usado para falar em números maiores com investidores.",
        "executive": "Run Rate = MRR Atual × 12. Métrica para comunicação, não para gestão. Não considera crescimento ou sazonalidade. Use com cuidado: se crescimento está acelerando, run rate subestima ARR futuro. Se crescimento está desacelerando, run rate superestima.",
        "investor": "Run rate é checkpoint, não projeção. Investidor desconta run rate porque sabe que crescimento não é linear. Run rate de R$1M com churn alto vale menos que run rate de R$800k com churn baixo. Prefira falar ARR projetado com cenários.",
        "analyst": "Run Rate = Último MRR × 12. Métrica para headlines. Para valuation, use ARR projetado baseado em cohorts e taxa de crescimento. Run rate pode ser enganoso se último mês foi outlier. Sempre acompanhe de margem de erro.",
        "formula": "Run_Rate = MRR_Mês_Atual × 12",
        "importancia": "Média - Métrica de comunicação externa",
        "benchmark": "Não há benchmark - é uma derivada do MRR"
    },
    
    # ============================================================================
    # 🔧 COMPONENTES OPERACIONAIS ESPECÍFICOS
    # ============================================================================
    
    "Simples_Nacional": {
        "termo": "Simples Nacional (Impostos)",
        "sigla": "Simples",
        "layman": "É o regime de tributação que startups brasileiras usam para pagar impostos de forma simplificada. Você paga uma alíquota única sobre a receita (ex: 6% para SaaS). Não precisa pagar separado ISS, ICMS, etc.",
        "executive": "Simples Nacional para SaaS: alíquota de 5.5% a 17% dependendo da receita. Até R$180k ano: 5.5%. Até R$360k: 7.87%. Até R$720k: 10.73%. Acima disso, muda para Lucro Presumido com alíquota efetiva maior. Planeje migração tributária com 6 meses de antecedência.",
        "investor": "Imposto no Brasil é 2-3x maior que nos EUA. Simples Nacional é vantajoso até R$720k de receita. Depois, alíquota efetiva sobe para 20-30%. Modelo deve suportar carga tributária crescente. Red flag: modelo que só é lucrativo no Simples.",
        "analyst": "Alíquota Simples é progressiva. Modele escalada tributária: 6% → 8% → 11% → 20% ao sair do Simples. Prazo de migração: 6-12 meses. Considere abrir holding para otimizar. Taxa efetiva brasileira é 2x vs. Delaware LLC.",
        "formula": "Alíquota = f(Faturamento_Anual, Tabela_Simples)",
        "importancia": "Alta - Impacta margem diretamente",
        "benchmark": "Até R$180k: 5.5% | R$180k-360k: 7.87% | R$360k-720k: 10.73% | >R$720k: 20-30%"
    },
    
    "Depreciacao": {
        "termo": "Depreciação",
        "sigla": "Depreciation",
        "layman": "É dividir o custo de algo durável (computador, móvel) ao longo da vida dele. Se comprou um PC por R$2.400 e vai usar 24 meses, deprecia R$100/mês. É uma despesa contábil, não sai do caixa todo mês.",
        "executive": "Depreciação é custo contábil que reconhece desgaste de ativos fixos. No modelo, CAPEX é gasto no mês 0, mas depreciação vai para P&L mensal. Afeta resultado contábil, mas não fluxo de caixa. Meta: manter CAPEX baixo para não distorcer resultado.",
        "investor": "Depreciação é 'non-cash expense'. Investidor foca em fluxo de caixa, não resultado contábil. Mas depreciação afere valuation se empresa for vendida baseada em EBITDA. Keep CAPEX minimal. Depreciation não afere SaaS valuation múltiplo.",
        "analyst": "Depreciação Mensal = Valor_Ativo ÷ Vida_Útil_Meses. Usada para P&L. Para valuation, focar em cash flow (EBITDA + Capex). Vida útil padrão: equipamentos 24-36 meses, móveis 60 meses. Depreciação acelerada pode ser usada para redução fiscal.",
        "formula": "Depreciação = Valor_Bem ÷ Vida_Útil (em meses)",
        "importancia": "Média - Afere resultado contábil, mas não fluxo de caixa",
        "benchmark": "Vida útil: CPU 24-36 meses | Móveis 60 meses | Veículos 60 meses"
    },
    
    "Retainer": {
        "termo": "Retainer (Serviços Profissionais)",
        "sigla": "Retainer",
        "layman": "É uma taxa mensal fixa que você paga para um advogado, contador ou consultor para ter acesso a ele quando precisar. Diferente de projeto fechado, é um custo recorrente fixo.",
        "executive": "Retainer é OPEX fixo para serviços profissionais. Contador (R$500-2k/mês), advogado (R$1k-5k/mês), consultor (R$2k-10k/mês). Use retainer para serviços regulares. Para projetos pontuais, use projeto fechado para não inflar OPEX.",
        "investor": "Retainers fixos são passivos recorrentes. Investidor prefere OPEX variável. Minimize retainer alto. Retainer >R$5k/mês em early-stage é red flag. Considere usar equity + retainer reduzido para serviços iniciais.",
        "analyst": "Retainer é despesa operacional recorrente. Inclui em OPEX. Considere diferenciar retainer essencial (contador) vs. retainer estratégico (consultor). Para projeções, assume retainer crescente com inflação + serviços adicionais.",
        "formula": "Retainer_Mensal = Valor_Fixo_Contratado",
        "importancia": "Média - Parte dos custos fixos operacionais",
        "benchmark": "Contador: R$500-2k/mês | Advogado: R$1k-3k/mês | Consultor: R$2k-8k/mês"
    },
    
    # ============================================================================
    # 📊 TERMOS GERAIS DE NEGÓCIOS E FINANÇAS
    # ============================================================================
    
    "KPI": {
        "termo": "Key Performance Indicator",
        "sigla": "KPI",
        "layman": "É um número que você escolhe para medir se está indo bem ou mal. Exemplos: MRR, churn, CAC. KPIs são seus painéis de controle. Você não pode gerenciar o que não mede.",
        "executive": "KPIs são métricas de saúde do negócio. Escolha 3-5 KPIs primários (MRR, Churn, LTV/CAC) e acompanhe semanalmente. KPIs devem ser 'SMART': específicos, mensuráveis, alcançáveis, relevantes, temporais. Reveja KPIs a cada 6 meses.",
        "investor": "Investidor foca em KPIs primários: MRR growth, churn, LTV/CAC, burn rate, runway. Se você não tem KPIs claros, não está pronto para investimento. KPIs devem ser auditáveis e não-biased. Fake KPIs = red flag instantâneo.",
        "analyst": "KPIs devem ser leading (preveem futuro) e lagging (mostram resultado). Ex: CAC é leading (prevê despesas), churn é lagging (mostra resultado). Crie dashboard de KPIs com targets e alerts. Use estatística de controle para identificar variações significativas.",
        "formula": "KPI = Métrica_Escolhida (ex: MRR, Churn, CAC)",
        "importancia": "Máxima - Base da gestão",
        "benchmark": "KPIs primários do SaaS: MRR Growth >10% m/m, Churn <5% m/m, LTV/CAC >3x"
    },
    
    "TAM_SAM_SOM": {
        "termo": "Mercado Total/Endereçável/Serviceable",
        "sigla": "TAM/SAM/SOM",
        "layman": "TAM = todo o mercado do mundo (ex: US$10B). SAM = parte que seu produto atende (ex: US$2B). SOM = parte que você consegue pegar (ex: US$200M). Usado para convencer investidor que mercado é grande.",
        "executive": "TAM/SAM/SOM define tamanho da oportunidade. TAM deve ser >R$1B para atrair VC. SAM deve ser >R$100M. SOM deve ser >R$10M para 3 anos. Se SOM é muito pequeno, modelo não é venture scale. Use dados de pesquisa para validar.",
        "investor": "TAM é irrelevante se SOM é pequeno. Investidor quer ver SOM realista baseado em CAC e capacidade de vendas. SOM = Sua capacidade de aquisição × ARPU × Clientes. Red flag: TAM enorme mas SOM não justifica investimento.",
        "analyst": "TAM = Total Addressable Market (top-down). SAM = Serviceable Addressable Market (seu segmento). SOM = Serviceable Obtainable Market (sua capacidade). Calcule SOM bottom-up: quantos clientes consegue fechar × ARPU. SOM realista é 1-5% do SAM.",
        "formula": "SOM = Capacidade_Venda_Mensal × ARPU × 12 × %_Mercado_que_consegue",
        "importancia": "Alta - Para captação e estratégia",
        "benchmark": "Meta VC: TAM >R$1B, SAM >R$100M, SOM >R$10M (3 anos)"
    },
    
    "SaaS": {
        "termo": "Software as a Service",
        "sigla": "SaaS",
        "layman": "É o modelo de negócio onde você vende acesso a um software via assinatura mensal/anual, não vende licença definitiva. Exemplos: Netflix, Spotify, Salesforce. Vantagem: receita recorrente previsível.",
        "executive": "SaaS é modelo de entrega de software via cloud com assinatura recorrente. Características: receita recorrente, baixo CAPEX, escalabilidade, churn como métrica crítica. Meta: atingir R$100k MRR e LTV/CAC >3x para provar viabilidade. SaaS é asset-light e venture-fundable.",
        "investor": "SaaS é modelo de investimento favorito por recorrência e margem alta. SaaS B2B > B2C por retenção e ARPU maiores. Investidor busca: (1) MRR growth >10% m/m, (2) Churn <5%, (3) LTV/CAC >3x, (4) Margem >70%, (5) TAM >R$1B. Red flag: SaaS com churn >7% ou margem <60%.",
        "analyst": "SaaS = Software delivered as a service, priced via subscription. Key metrics: MRR, ARR, Churn, LTV, CAC, Net Dollar Retention. SaaS puro tem gross margin >75% e CAPEX <5% ARR. SaaS é modelável e previsível vs. software tradicional.",
        "formula": "Modelo SaaS: Venda_Subscrição_Recorrente + Entrega_Cloud + Atualização_Contínua",
        "importancia": "Máxima - Define modelo de negócio",
        "benchmark": "Meta early-stage: R$10k-100k MRR | Growth: R$100k-1M MRR | Late: >R$1M MRR"
    }
}

# ============================================================================
# FUNÇÕES AUXILIARES PARA USAR NO APP
# ============================================================================

def obter_explicacao(termo: str, nivel: str = "executive") -> str:
    """
    Retorna explicação de um termo no nível adequado.
    
    Args:
        termo: Sigla ou nome do termo (ex: "LTV", "CAC", "MRR")
        nivel: "layman", "executive", "investor", "analyst"
    
    Returns:
        String com a explicação completa
    """
    if termo.upper() not in JARGOES_FINANCEIROS:
        return f"Termo '{termo}' não encontrado no glossário."
    
    entrada = JARGOES_FINANCEIROS[termo.upper()]
    
    if nivel not in ["layman", "executive", "investor", "analyst"]:
        nivel = "executive"
    
    # Monta resposta completa
    resposta = f"""
**{entrada['termo']} ({entrada['sigla']})**

**{nivel.upper()}:** {entrada[nivel]}

**Importância:** {entrada['importancia']}
**Benchmark:** {entrada['benchmark']}
"""
    
    if 'formula' in entrada:
        resposta += f"\n**Fórmula:** {entrada['formula']}"
    
    return resposta

def listar_todos_termos() -> list:
    """Retorna lista de todas as siglas disponíveis."""
    return list(JARGOES_FINANCEIROS.keys())

def obter_resumo_investidor() -> Dict[str, str]:
    """
    Retorna dicionário com apenas as explicações de nível 'investor'
    para uso rápido no app.
    """
    return {
        sigla: dados["investor"] 
        for sigla, dados in JARGOES_FINANCEIROS.items()
    }

# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # Testa algumas explicações
    print("=" * 80)
    print("TESTE DO GLOSSÁRIO")
    print("=" * 80)
    
    print("\n--- Explicação de LTV para Investidor ---")
    print(obter_explicacao("LTV", "investor"))
    
    print("\n--- Explicação de Churn para Leigo ---")
    print(obter_explicacao("CHURN", "layman"))
    
    print("\n--- Explicação de COGS para Analista ---")
    print(obter_explicacao("COGS", "analyst"))
    
    print(f"\n--- Termos Disponíveis ({len(listar_todos_termos())} termos) ---")
    print(listar_todos_termos())