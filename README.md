# ✅ **O que estamos construindo**

Estamos construindo **um Sistema Avançado de Análise Financeira e Simulação de Negócios**, chamado **SAM Financial Model** — um motor completo de projeções, simulações, análises de risco e dashboards.

Ele funciona como:

### **📌 Um simulador financeiro completo capaz de prever o futuro de uma startup, SaaS ou negócio digital.**

Inclui:

* Projeções determinísticas (36–60 meses)
* Análises de risco (Monte Carlo)
* Sensibilidade (tornado charts)
* Controle granular de custos, CAC, churn, marketing, headcount etc.
* Dashboards visuais avançados
* Relatórios financeiros completos (DRE, fluxo de caixa, MRR breakdown)
* Visualizações interativas
* Tabelas detalhadas com filtros
* Explicações técnicas e leigas integradas (glossário inteligente)

É mais avançado que um Excel tradicional, mais acessível que ferramentas corporativas e mais flexível do que modelos estáticos.

---

# 🎯 **Para qual aplicação estamos construindo**

Para:

## **📌 Fundadores, empreendedores, analistas e investidores** que precisam tomar decisões com base em projeções confiáveis e não em achismo.

Ele serve para:

* Validar viabilidade de um negócio SaaS
* Medir sustentabilidade financeira
* Testar cenários (otimista vs realista vs pessimista)
* Entender risco de caixa acabar
* Saber quando a empresa entra em equilíbrio
* Avaliar MRR, LTV, CAC, churn e crescimento
* Analisar impacto de mudanças nos custos ou marketing
* Estruturar decisões de investimento e contratação
* Criar projeções para rodadas de captação
* Demonstrar profissionalismo e maturidade analítica

É exatamente o tipo de ferramenta que um CFO usaria — mas simplificada para fundadores e analistas operacionais.

---

# 💡 **Qual é a ideia de valor (Value Proposition)**

### 🔥 **É o primeiro sistema que une:**

* **Modelagem financeira completa**
* **Simulações avançadas**
* **Explicações didáticas**
* **Interface simples**
* **Flexibilidade total (configurar tudo)**

Ou seja:

## ⭐ **Transforma dados brutos em decisões inteligentes.**

### É uma ferramenta que permite:

### **→ Entender a realidade financeira da empresa**

### **→ Simular o que acontece com mudanças estratégicas**

### **→ Controlar totalmente o crescimento e os custos**

### **→ Reduzir risco e aumentar previsibilidade**

### **→ Justificar decisões com dados (não feeling)**

---

# 🧠 **O que exatamente ela entrega ao usuário final**

### ✔ Projeção financeira completa

### ✔ Indicadores críticos (MRR, CAC, LTV, churn, ARPU…)

### ✔ Tabelas e relatórios automáticos

### ✔ Monte Carlo com 500+ simulações

### ✔ Tornado chart (impacto das variáveis)

### ✔ Painel para testar hipóteses

### ✔ Filtros avançados e visualização interativa

### ✔ Módulo completo de marketing (multi estágio)

### ✔ Módulo de folha (contratações futuras)

### ✔ Modelo vivo (não engessado como Excel)

### ✔ Entendimento profundo (explicação clara e narrativa)

---

# 🚀 **Resumo em uma frase**

### **Estamos construindo um sistema profissional de projeção, análise e tomada de decisão, que transforma um fluxo caótico de planilhas em uma plataforma inteligente para prever o futuro financeiro de um negócio.**

---


---

# 📊 PLANO ESTRATÉGICO COMPLETO - SAM FINANCIAL MODEL v4.0

## Análise da Situação Atual vs. Visão Desejada

Entendi **perfeitamente** a profundidade do que você precisa. O app atual é uma "calculadora simples" quando deveria ser um **"War Room Financeiro"** - um centro de comando estratégico onde TODAS as decisões financeiras podem ser simuladas, auditadas e visualizadas.

---

# 🎯 PARTE 1: DIAGNÓSTICO COMPLETO

## ❌ Problemas Críticos Identificados

### 1. **CAIXA PRETA** (Problema #1 mais grave)
- KPIs aparecem mas não mostram **DE ONDE VÊM**
- Break-even diz "Mês 3" mas não mostra o gráfico de resultado operacional chegando a zero
- CAC Payback diz "6 meses" mas não decompõe: (CAC R$500) ÷ (Margem mensal R$83) = 6 meses
- **SOLUÇÃO**: Cada métrica precisa de um "Drill-Down" visual

### 2. **CONFIGURAÇÃO LIMITADA** (Problema #2)
- Faltam campos para:
  - Equipe detalhada (cargo por cargo com gatilhos de contratação)
  - Infraestrutura em tiers com transição automática
  - Marketing em 4 fases com regras de transição
  - Impostos progressivos (Simples → Lucro Real)
  - Comissões de afiliados/parceiros
  - Custos imprevistos e reserva de contingência

### 3. **FALTA DE INTELIGÊNCIA** (Problema #3)
- Não há insights automáticos tipo:
  - ⚠️ "ALERTA: Vale da Morte em Mês 8 = -R$45k. Você precisa captar R$50k antes disso"
  - 💡 "INSIGHT: Se churn cair de 5% para 3%, LTV sobe 67% e você atinge break-even 4 meses antes"
  - 🎯 "META: Para atingir R$100k MRR em 18 meses, precisa crescer 12%/mês (está em 8%)"

### 4. **VISUALIZAÇÃO ESTÁTICA** (Problema #4)
- Gráficos não interagem entre si
- Não há drill-down (clicar na barra de "Infra" e ver VPS1 + VPS2 + Cedro)
- Faltam gráficos avançados:
  - Waterfall (como a receita vira lucro)
  - Sankey (fluxo de dinheiro)
  - Heatmap (sensibilidade 2D)
  - Cohort retention table
  - Funnel visual (visitante → trial → pagante)

### 5. **AUDITORIA IMPOSSÍVEL** (Problema #5)
- CFO olha e pergunta: "De onde veio esse R$45k de OPEX?"
- Resposta atual: "Está na tabela" ❌
- Resposta necessária: Gráfico de pizza mostrando: Pessoal 60%, Infra 20%, Marketing 15%, Ferramentas 5% + drill-down em cada fatia ✅

---

# 🏗️ PARTE 2: ARQUITETURA DA SOLUÇÃO

## Estrutura de 3 Camadas

```
CAMADA 1: CONFIGURAÇÃO AVANÇADA (Config Builder)
├── Sistema de "Builders" para cada categoria
├── Validação em tempo real
├── Templates salvos (cenários nomeados)
└── Import/Export JSON

CAMADA 2: ENGINE INTELIGENTE (Analytics Engine)
├── Cálculos base (já existe)
├── Detecção de anomalias
├── Geração de insights
├── Simulação de "E se...?" em tempo real
└── Cálculos de decomposição (cada valor sabe sua origem)

CAMADA 3: VISUALIZAÇÃO INTERATIVA (Smart Dashboard)
├── Dashboards temáticos (Receita, Custos, Caixa, Equipe)
├── Gráficos com drill-down
├── Filtros globais + filtros específicos
├── Exportação de cada visual
└── Modo "Apresentação" (para investidores)
```

---

# 📋 PARTE 3: LISTA DETALHADA DE FEATURES

## 🔧 CATEGORIA 1: CONFIGURAÇÃO AVANÇADA

### 1.1 Capital & Financiamento
**Status Atual:** ✅ Básico OK  
**Adicionar:**
- [ ] Múltiplos aportes programados (Mês 1: R$50k, Mês 12: R$100k, Mês 24: R$200k)
- [ ] Simulação de rodadas (Seed, Series A com diluição)
- [ ] Empréstimos com juros e carência
- [ ] Reserva de contingência (% da receita)

**Interface necessária:**
```
┌─ Aportes Programados ─────────────────┐
│ [+] Adicionar Aporte                   │
│ ┌───────────────────────────────────┐ │
│ │ Mês: [12] Valor: [100000]         │ │
│ │ Tipo: [Equity ▼] Diluição: [20%] │ │
│ │ [Remover]                         │ │
│ └───────────────────────────────────┘ │
└────────────────────────────────────────┘
```

---

### 1.2 Funil de Aquisição
**Status Atual:** ✅ Básico OK  
**Adicionar:**
- [ ] Múltiplos canais (Organic, Paid, Referral, Direct)
- [ ] Conversão diferente por canal
- [ ] CAC diferente por canal
- [ ] Sazonalidade (Jul-Dez cresce 30%, Jan-Mar cai 20%)

**Interface necessária:**
```
┌─ Canais de Aquisição ─────────────────┐
│ Canal       │ % Traffic │ Conv Trial │ Conv Pago │ CAC    │
├─────────────┼───────────┼────────────┼───────────┼────────┤
│ Organic SEO │ 40%       │ 8%         │ 20%       │ R$200  │
│ Google Ads  │ 30%       │ 4%         │ 15%       │ R$800  │
│ Referral    │ 20%       │ 12%        │ 30%       │ R$100  │
│ Direct      │ 10%       │ 10%        │ 25%       │ R$50   │
└─────────────┴───────────┴────────────┴───────────┴────────┘
```

---

### 1.3 Receita (Mix de Planos)
**Status Atual:** ✅ Básico OK  
**Adicionar:**
- [ ] Evolução do mix ao longo do tempo (Ano 1: 50% Lite, Ano 2: 30% Lite)
- [ ] Upsell/Downsell (% que migra de plano/mês)
- [ ] Add-ons (funcionalidades extras)
- [ ] Receita não-recorrente (implementação, treinamento)

**Interface necessária:**
```
┌─ Evolução do Mix de Planos ───────────┐
│ Ano 1: Lite [50%] Trader [30%] Pro [20%]
│ Ano 2: Lite [30%] Trader [40%] Pro [30%]
│ Ano 3: Lite [20%] Trader [35%] Pro [45%]
│
│ ☑ Ativar Upsell (2% Lite→Trader/mês)
│ ☑ Ativar Add-ons (15% compram extra R$20)
└────────────────────────────────────────┘
```

---

### 1.4 Custos Variáveis (COGS) - **CRÍTICO**
**Status Atual:** ⚠️ INCOMPLETO  
**Adicionar:**
- [ ] Taxa de pagamento (% + fixo por transação)
- [ ] Comissões de afiliados (% sobre vendas via afiliado)
- [ ] Comissões de parceiros (% sobre vendas via parceria)
- [ ] Custos de mídia performance (CPC, CPM) vinculados a CAC
- [ ] Cashback/Incentivos (% da receita em volta para usuário)

**Interface necessária:**
```
┌─ COGS Detalhado ──────────────────────┐
│ ☑ Taxa Pagamento: [3.5%] + R$[0.39]/transação
│ ☑ Comissão Afiliados: [20%] (vendas via afiliado: [30%])
│ ☑ Comissão Parceiros: [15%] (vendas via parceria: [10%])
│ ☑ Cashback Usuários: [5%] da receita
│ ☐ Custo Suporte: R$[5]/usuário/mês (só se ativo)
└────────────────────────────────────────┘
```

---

### 1.5 Infraestrutura Escalável (Tiers) - **CRÍTICO**
**Status Atual:** ✅ Existe mas não configurável  
**Melhorar:**
- [ ] Interface visual para definir cada tier
- [ ] Transição automática entre tiers baseada em usuários
- [ ] Custos compostos (VPS + API + CDN + Backup)
- [ ] Alertas de transição ("Mês 8: migrar para Tier 2")

**Interface necessária:**
```
┌─ Infraestrutura por Tier ─────────────────────────────┐
│ TIER 1: Validação (0-100 usuários)
│ ├─ VPS Principal:        R$ [55]
│ ├─ VPS Coleta MT5:       R$ [150]
│ ├─ Domínio:              R$ [4]
│ └─ TOTAL TIER 1:         R$ 209
│
│ TIER 2: Escala (101-500 usuários)
│ ├─ API Cedro:            R$ [5000]
│ ├─ VPS Robusta:          R$ [500]
│ ├─ Backup S3:            R$ [50]
│ ├─ CDN Cloudflare:       R$ [100]
│ └─ TOTAL TIER 2:         R$ 5650
│
│ TIER 3: Hiperescala (501+ usuários)
│ └─ Custo por usuário:    R$ [1.50]
│
│ [+] Adicionar Item a Tier │ [Visualizar Transições]
└────────────────────────────────────────────────────────┘
```

---

### 1.6 Marketing (4 Fases) - **CRÍTICO**
**Status Atual:** ⚠️ Só 2 fases  
**Adicionar:**
- [ ] Fase 1: Validação (custo fixo R$500-2k, 3-6 meses)
- [ ] Fase 2: Crescimento (% lucro bruto, 6-18 meses)
- [ ] Fase 3: Escala (% receita, quando MRR > R$50k)
- [ ] Fase 4: Maturidade (CAC target, quando LTV/CAC > 5x)
- [ ] Orçamento por canal (SEO, Ads, Content, Eventos)

**Interface necessária:**
```
┌─ Estratégia de Marketing (4 Fases) ───────────────────┐
│ FASE 1: Validação
│ ├─ Duração: [6] meses
│ ├─ Orçamento fixo: R$ [1000]/mês
│ └─ Canais: 50% SEO, 30% Ads, 20% Content
│
│ FASE 2: Crescimento (após Fase 1)
│ ├─ Duração: [12] meses
│ ├─ Orçamento: [25%] do Lucro Bruto
│ └─ Canais: 30% SEO, 50% Ads, 20% Referral
│
│ FASE 3: Escala (quando MRR > R$[50000])
│ ├─ Orçamento: [20%] da Receita
│ └─ Canais: 20% SEO, 40% Ads, 30% Eventos, 10% Influencers
│
│ FASE 4: Maturidade (quando LTV/CAC > [5])
│ └─ CAC Target: R$[300] (otimizar para eficiência)
│
│ [Adicionar Fase Personalizada]
└────────────────────────────────────────────────────────┘
```

---

### 1.7 Salário Fundador + Sócios - **CRÍTICO**
**Status Atual:** ⚠️ Muito básico  
**Adicionar:**
- [ ] Fases de remuneração:
  - Fase 1: Sem salário (meses 1-X)
  - Fase 2: Salário mínimo (meses X-Y)
  - Fase 3: Salário cheio (após MRR > R$Z)
  - Fase 4: Salário + Pró-labore (após lucro > R$W)
- [ ] Múltiplos sócios/investidores
- [ ] Participação nos lucros (% após certo MRR)

**Interface necessária:**
```
┌─ Remuneração de Sócios ───────────────────────────────┐
│ [+] Adicionar Sócio/Fundador
│
│ SÓCIO 1: João Silva (Fundador/CEO)
│ ├─ Fase 1 (Mês 1-6):     R$ [0]
│ ├─ Fase 2 (Mês 7-12):    R$ [3000]
│ ├─ Fase 3 (Mês 13+):     R$ [8000] (quando MRR > R$[30000])
│ ├─ Pró-labore:            [10%] lucro (quando lucro > R$[10000])
│ └─ Participação acionária: [40%]
│
│ INVESTIDOR 1: Fundo XYZ
│ ├─ Aporte: R$ [200000] (Mês [12])
│ ├─ Equity: [25%]
│ └─ Cadeira no board: Sim
│
│ [Calcular Diluição] [Simular Exit]
└────────────────────────────────────────────────────────┘
```

---

### 1.8 Equipe (CLT/PJ) + Gatilhos de Contratação - **CRÍTICO**
**Status Atual:** ⚠️ Adiciona funcionário mas sem lógica  
**Adicionar:**
- [ ] Gatilhos de contratação ("Quando MRR > R$50k, contratar Dev Backend")
- [ ] Cargos pré-definidos (Dev, Marketing, CS, Financeiro, Vendas)
- [ ] Progressão salarial (reajustes anuais, promoções)
- [ ] Benefícios configuráveis (VR, VT, Plano Saúde)

**Interface necessária:**
```
┌─ Planejamento de Equipe ──────────────────────────────┐
│ CARGO: Desenvolvedor Backend
│ ├─ Tipo: [CLT ▼]
│ ├─ Salário: R$ [8000] + Encargos [68%] = R$ 13440
│ ├─ GATILHO: Contratar quando:
│ │   ☑ MRR > R$ [50000]
│ │   OU
│ │   ☑ Usuários > [500]
│ │   OU
│ │   ☐ Mês = [12]
│ └─ Reajuste: [8%] a cada [12] meses
│
│ CARGO: Community Manager
│ ├─ Tipo: [CLT ▼]
│ ├─ Salário: R$ [5000]
│ ├─ GATILHO: Contratar quando MRR > R$ [80000]
│ └─ Benefícios: VR [500], VT [300], Plano [400]
│
│ [+] Adicionar Cargo │ [Ver Timeline de Contratações]
└────────────────────────────────────────────────────────┘
```

---

### 1.9 Escritório/Operação
**Status Atual:** ⚠️ Só campos simples  
**Adicionar:**
- [ ] Decisão: Remoto vs. Híbrido vs. Presencial
- [ ] Se presencial: quando começar (gatilho por equipe size)
- [ ] Custos escaláveis (escritório pequeno → coworking → escritório próprio)

**Interface necessária:**
```
┌─ Estratégia de Espaço Físico ─────────────────────────┐
│ Modelo: ⦿ Remoto  ○ Híbrido  ○ Presencial
│
│ [Se híbrido/presencial]
│ FASE 1: Coworking (quando equipe > [3] pessoas)
│ └─ Custo: R$ [1500]/mês (Mês [6]+)
│
│ FASE 2: Escritório Pequeno (quando equipe > [10])
│ ├─ Aluguel: R$ [5000]
│ ├─ Condomínio: R$ [800]
│ ├─ Utilities: R$ [600]
│ └─ TOTAL: R$ 6400/mês (Mês [18]+)
└────────────────────────────────────────────────────────┘
```

---

### 1.10 Ferramentas SaaS - **CRÍTICO**
**Status Atual:** ✅ Sistema existe mas interface limitada  
**Melhorar:**
- [ ] Categorias visuais (Dev, Segurança, Gestão, Comunicação, Design, IA)
- [ ] Custos por usuário (ex: Notion R$8/user, GitHub R$4/dev)
- [ ] Ferramentas essenciais vs. opcionais
- [ ] Upgrade automático (ex: Notion Free → Paid quando equipe > 10)

**Interface necessária:**
```
┌─ Stack de Ferramentas SaaS ───────────────────────────┐
│ CATEGORIA: Desenvolvimento
│ ├─ GitHub Copilot:  R$ [100] (desde Mês [1])
│ ├─ Cursor IDE:      R$ [200] (desde Mês [1])
│ └─ [+] Adicionar ferramenta dev
│
│ CATEGORIA: IA & APIs
│ ├─ Claude Pro:      R$ [400] (3 usuários × R$20 × 6.5)
│ ├─ OpenAI API:      Variável (R$[5]/usuário final)
│ └─ [+] Adicionar ferramenta IA
│
│ CATEGORIA: Infraestrutura
│ ├─ VPS Windows:     R$ [150] (quando MRR > R$[20000])
│ ├─ Cloudflare Pro:  R$ [100] (Tier 2+)
│ └─ [+] Adicionar infra
│
│ [Ver Custo Total] [Otimizar Stack]
└────────────────────────────────────────────────────────┘
```

---

### 1.11 Serviços Profissionais
**Status Atual:** ⚠️ Só campos simples  
**Adicionar:**
- [ ] Contabilidade escalável (PF: R$300, PJ simples: R$500, PJ completo: R$2000)
- [ ] Advogado (retainer vs. projeto fechado)
- [ ] Consultorias específicas (Growth, Finance, Tech)

---

### 1.12 Depreciação + CAPEX
**Status Atual:** ✅ Sistema existe  
**Melhorar:**
- [ ] Interface visual para adicionar ativos
- [ ] Vida útil sugerida por categoria
- [ ] Alerta de fim de depreciação

---

### 1.13 Impostos Variáveis - **NOVO**
**Status Atual:** ❌ Não existe  
**Adicionar:**
- [ ] Simples Nacional por faixa (até R$180k: 6%, até R$360k: 8%, etc.)
- [ ] Transição automática para Lucro Presumido
- [ ] Impostos sobre folha (variável por regime)

**Interface necessária:**
```
┌─ Regime Tributário ───────────────────────────────────┐
│ FASE 1: Simples Nacional
│ ├─ Faturamento R$ 0-180k:    [6%]
│ ├─ Faturamento R$ 180-360k:  [8%]
│ └─ Faturamento R$ 360-720k:  [11%]
│
│ FASE 2: Lucro Presumido (quando faturamento > R$[720k])
│ └─ Alíquota efetiva: [22%] (IR 15% + CSLL 9% + PIS/COFINS)
│
│ [Simular Transição] [Ver Breakpoint Fiscal]
└────────────────────────────────────────────────────────┘
```

---

### 1.14 Comissões/Afiliados - **NOVO**
**Status Atual:** ❌ Não existe  
**Adicionar:**
- [ ] % de vendas via afiliados
- [ ] % de comissão
- [ ] Diferentes tiers de comissão (Bronze 10%, Prata 15%, Ouro 20%)

---

### 1.15 Contingência & Imprevistos - **NOVO**
**Status Atual:** ❌ Não existe  
**Adicionar:**
- [ ] Reserva de emergência (% da receita)
- [ ] Eventos de risco (perda de cliente grande, aumento de churn, queda de tráfego)
- [ ] Simulação de recessão (receita cai X% por Y meses)

**Interface necessária:**
```
┌─ Gestão de Riscos & Contingência ─────────────────────┐
│ RESERVA DE EMERGÊNCIA
│ └─ Guardar [10%] da receita como reserva
│
│ CENÁRIOS DE RISCO
│ ☑ Recessão Leve: Receita -15% por 6 meses (Prob: 30%)
│ ☑ Churn Spike: Churn dobra por 3 meses (Prob: 20%)
│ ☐ Perda Cliente Anchor: -R$5k MRR (Prob: 10%)
│
│ [Simular Pior Cenário] [Monte Carlo com Riscos]
└────────────────────────────────────────────────────────┘
```

---

# 📊 PARTE 4: DASHBOARDS INTELIGENTES

## 4.1 Dashboard Principal (Home) - **REDESIGN COMPLETO**

**Conceito:** "Sala de Controle do CEO"

```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 VISÃO GERAL - MÊS 12                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│ │ MRR      │ │ USUÁRIOS │ │ CAIXA    │ │ LTV/CAC  │       │
│ │ R$ 45k   │ │ 450      │ │ R$ 38k   │ │ 4.2x     │       │
│ │ +12% ▲   │ │ +50 ▲    │ │ -R$5k ▼  │ │ 0.2x ▲   │       │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│ ⚠️ ALERTAS CRÍTICOS:                                        │
│ • Vale da Morte em 3 meses (-R$12k). Captar R$20k URGENTE  │
│ • CAC subiu 25% no último mês. Revisar canais.             │
│                                                              │
│ 💡 INSIGHTS:                                                │
│ • Se churn cair para 3%, break-even adianta 2 meses        │
│ • Marketing Fase 2 começa mês que vem (Lucro > 0)          │
│                                                              │
│ 🎯 PRÓXIMAS METAS:                                          │
│ • Break-even: Mês 15 (faltam 3 meses)                      │
│ • Contratar Dev Backend: Quando MRR > R$50k (faltam R$5k)  │
│                                                              │
│ [Ver Detalhes] [Ajustar Metas] [Exportar Relatório]        │
└─────────────────────────────────────────────────────────────┘
```

**Gráficos nesta tela:**
1. **Funil de Saúde** (semáforo): Verde/Amarelo/Vermelho para cada categoria
2. **Timeline de Marcos** (linha do tempo visual): Break-even, Contratações, Mudanças de Tier
3. **Comparação vs. Meta** (gauge charts)

---

## 4.2 Dashboard de Receita - **NOVO**

```
┌─ RECEITA & CRESCIMENTO ────────────────────────────────────┐
│
│ [Gráfico Waterfall: Como chegamos no MRR atual]
│ Início Mês: R$40k → Novos: +R$8k → Churn: -R$3k → Fim: R$45k
│ (clicável: drill-down em cada barra)
│
│ [Gráfico de Linha: MRR por Plano]
│ (3 linhas: Lite, Trader, Pro com área empilhada)
│
│ [Cohort Retention Table]
│ Mês 0  │ Mês 1 │ Mês 2 │ Mês 3 │...
│ 100%   │ 95%   │ 91%   │ 88%   │...
│
│ [Gráfico de Funil: Visitantes → Trial → Pagantes]
│ (visual tipo funil com taxas de conversão)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.3 Dashboard de Custos - **NOVO**

```
┌─ RASTREADOR DE CUSTOS ─────────────────────────────────────┐
│
│ [Gráfico Sankey: Fluxo de Dinheiro]
│ Receita R$50k → COGS R$15k → OPEX R$30k → Lucro R$5k
│ (visual de fluxo com espessura proporcional)
│
│ [Gráfico de Pizza INTERATIVO: OPEX Breakdown]
│ Pessoal 55% (R$16.5k) ← CLIQUE AQUI
│ └─ [Popup mostra: 2 Devs R$13k + Fundador R$3.5k]
│
│ Infra 20% (R$6k)
│ Marketing 15% (R$4.5k)
│ Ferramentas 10% (R$3k)
│
│ [Tabela: Custos Fixos vs. Variáveis]
│ Fixos:     R$ 25k (83%)
│ Variáveis: R$ 5k  (17%)
│
│ [Comparação: Budget vs. Real vs. Forecast]
│ (gráfico de barras lado a lado)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.4 Dashboard de Caixa & Viabilidade - **NOVO**

```
┌─ GESTÃO DE CAIXA ──────────────────────────────────────────┐
│
│ [Gráfico: Saldo de Caixa com Zonas]
│ Verde: Zona segura (>R$20k)
│ Amarelo: Zona atenção (R$10k-20k)
│ Vermelho: Zona perigo (<R$10k)
│ [Marcador: "VALE DA MORTE Mês 8: -R$12k"]
│
│ [Gráfico: Burn Rate vs. Crescimento MRR]
│ (duas linhas: burn mensal e crescimento mrr)
│
│ [Painel de Runway]
│ Runway Atual: 8 meses
│ Com aporte R$50k: 14 meses
│ Para atingir break-even: 3 meses
│
│ [Simulador "E se...?"]
│ • E se MRR crescer 15% em vez de 12%? → +2 meses runway
│ • E se cortar R$5k de OPEX? → +3 meses runway
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.5 Dashboard de Equipe - **NOVO**

```
┌─ PLANEJAMENTO DE EQUIPE ───────────────────────────────────┐
│
│ [Timeline: Contratações Planejadas]
│ Mês 6:  ✅ Designer PJ contratado
│ Mês 12: 🔜 Dev Backend (quando MRR > R$50k)
│ Mês 18: 📅 Community Manager planejado
│
│ [Gráfico: Custo de Pessoal vs. Produtividade]
│ Custo/Funcionário vs. MRR/Funcionário
│
│ [Tabela: Projeção de Headcount]
│ Ano 1: 2 pessoas (Fundador + Designer)
│



# 📊 PARTE 4: DASHBOARDS INTELIGENTES (continuação)

## 4.5 Dashboard de Equipe - **NOVO** (continuação)

```
┌─ PLANEJAMENTO DE EQUIPE ───────────────────────────────────┐
│
│ [Timeline: Contratações Planejadas]
│ Mês 6:  ✅ Designer PJ contratado
│ Mês 12: 🔜 Dev Backend (quando MRR > R$50k - faltam R$5k)
│ Mês 18: 📅 Community Manager planejado
│ Mês 24: 📅 CFO planejado (quando MRR > R$200k)
│
│ [Gráfico: Custo de Pessoal vs. Produtividade]
│ ├─ Linha 1: Custo total pessoal
│ ├─ Linha 2: MRR/Funcionário (produtividade)
│ └─ Área sombreada: Break-even de produtividade
│
│ [Tabela: Projeção de Headcount]
│ Ano 1: 2 pessoas → Custo R$8k/mês → MRR/pessoa R$22.5k
│ Ano 2: 5 pessoas → Custo R$32k/mês → MRR/pessoa R$28k
│ Ano 3: 12 pessoas → Custo R$85k/mês → MRR/pessoa R$35k
│
│ [Drill-down: Clique em qualquer período]
│ └─ Mostra: Quem foi contratado, salário, cargo, gatilho
│
│ 💡 INSIGHT: Produtividade/funcionário crescendo 12%/ano
│ ⚠️ ALERTA: Custo pessoal = 71% da receita (meta: <60%)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.6 Dashboard de Marketing - **NOVO**

```
┌─ EFICIÊNCIA DE MARKETING ──────────────────────────────────┐
│
│ [Gráfico: CAC por Canal]
│ Organic:  R$200 (LTV/CAC: 7.5x) ✅ EXCELENTE
│ Ads:      R$800 (LTV/CAC: 1.9x) ⚠️ ABAIXO DA META
│ Referral: R$100 (LTV/CAC: 15x) 🚀 INVESTIR MAIS
│ Direct:   R$50  (LTV/CAC: 30x) 🚀 INVESTIR MAIS
│
│ [Gráfico: Evolução CAC vs. LTV]
│ (duas linhas ao longo do tempo + área entre elas)
│
│ [Tabela: ROI por Canal]
│ Canal     │ Investido │ Clientes │ MRR Gerado │ ROI    │
│ Organic   │ R$3k      │ 15       │ R$1.5k/mês │ 500%   │
│ Ads       │ R$12k     │ 15       │ R$1.5k/mês │ 125%   │
│ Referral  │ R$500     │ 5        │ R$500/mês  │ 1000%  │
│
│ [Funil Visual de Conversão]
│ Visitantes → Trial → Pagantes (com perdas visualizadas)
│
│ 💡 RECOMENDAÇÃO: Reduzir Ads 30%, aumentar Referral 50%
│ 💡 PROJEÇÃO: Com ajuste, CAC médio cai de R$450 para R$320
│
│ [Simular Rebalanceamento] [Ver Histórico de Campanhas]
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.7 Dashboard de Unit Economics - **NOVO**

```
┌─ ECONOMIA DO CLIENTE ──────────────────────────────────────┐
│
│ [Gráfico: Decomposição do LTV]
│ ┌─────────────────────────────────────────┐
│ │ ARPU R$97         ────────────────────► │
│ │ - Impostos (6%)   ─────────────────────┤ -R$5.82
│ │ - Taxa Pgto (3.5%) ────────────────────┤ -R$3.40
│ │ - Custo IA        ─────────────────────┤ -R$5.00
│ │ = Margem/mês      ─────────────────────┤ R$82.78
│ │ × Lifetime (25 meses) ─────────────────┤
│ │ = LTV             ─────────────────────┤ R$2069
│ └─────────────────────────────────────────┘
│
│ [Gráfico: CAC Payback Visual]
│ Mês 0: CAC -R$500
│ Mês 1: +R$83 (saldo: -R$417)
│ Mês 2: +R$83 (saldo: -R$334)
│ ...
│ Mês 6: +R$83 (saldo: +R$0) ← PAYBACK ATINGIDO
│
│ [Comparação por Plano]
│ Plano  │ ARPU  │ LTV    │ CAC   │ LTV/CAC │ Payback │
│ Lite   │ R$70  │ R$1450 │ R$400 │ 3.6x    │ 7 meses │
│ Trader │ R$99  │ R$2050 │ R$450 │ 4.6x    │ 6 meses │
│ Pro    │ R$159 │ R$3300 │ R$550 │ 6.0x    │ 4 meses │
│
│ 💡 INSIGHT: Plano Pro tem melhor unit economics (focar upsell)
│ ⚠️ ALERTA: Plano Lite marginalmente viável (considerar subir preço)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.8 Dashboard de Análise de Sensibilidade - **NOVO**

```
┌─ ANÁLISE "E SE...?" ───────────────────────────────────────┐
│
│ [Gráfico Tornado: Impacto no Caixa Final]
│ Churn -20%        ████████████████ +R$45k
│ Crescimento +20%  ██████████████ +R$38k
│ ARPU +10%         ██████████ +R$25k
│ CAC -20%          ████████ +R$18k
│ Marketing -30%    ██████ +R$12k
│ Salários +20%     ████ -R$8k
│
│ [Heatmap 2D: Churn vs. Crescimento]
│          │ Crescimento
│  Churn   │ 5%  │ 10% │ 15% │ 20% │ 25% │
│  ────────┼─────┼─────┼─────┼─────┼─────┤
│  2%      │ 🟢  │ 🟢  │ 🟢  │ 🟢  │ 🟢  │
│  4%      │ 🟡  │ 🟢  │ 🟢  │ 🟢  │ 🟢  │
│  6%      │ 🔴  │ 🟡  │ 🟢  │ 🟢  │ 🟢  │
│  8%      │ 🔴  │ 🔴  │ 🟡  │ 🟢  │ 🟢  │
│  10%     │ 🔴  │ 🔴  │ 🔴  │ 🟡  │ 🟢  │
│
│ [Simulador Interativo]
│ Se Churn cair para: [3%] ▼
│ E Crescimento subir para: [15%] ▼
│ Então:
│ • Break-even adianta 4 meses (Mês 11)
│ • LTV sobe 33% (R$2750)
│ • Runway aumenta 6 meses
│ • Caixa final: +R$67k
│
│ [Salvar Cenário] [Comparar 3 Cenários]
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.9 Dashboard de Análise de Cohorts - **NOVO**

```
┌─ ANÁLISE DE COHORTS (RETENÇÃO) ────────────────────────────┐
│
│ [Cohort Retention Table - Visual Heatmap]
│ Mês Entrada │ M0  │ M1  │ M2  │ M3  │ M6  │ M12 │
│ ────────────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ Jan/24      │100% │ 96% │ 92% │ 89% │ 84% │ 78% │ 🟢
│ Fev/24      │100% │ 95% │ 90% │ 86% │ 81% │ ... │ 🟢
│ Mar/24      │100% │ 94% │ 88% │ 83% │ ... │ ... │ 🟡
│ Abr/24      │100% │ 91% │ 84% │ ... │ ... │ ... │ 🔴
│ Mai/24      │100% │ 89% │ ... │ ... │ ... │ ... │ 🔴
│
│ ⚠️ ALERTA: Cohorts recentes (Abr-Mai) têm retenção pior
│ 💡 INVESTIGAR: O que mudou? Qualidade de leads? Onboarding?
│
│ [Gráfico: Curvas de Retenção por Cohort]
│ (linhas de cada cohort ao longo do tempo)
│
│ [Análise de Churn por Motivo]
│ Preço alto:       35%
│ Complexidade:     25%
│ Falta features:   20%
│ Suporte ruim:     15%
│ Outros:           5%
│
│ [Ações Recomendadas]
│ ☐ Revisar onboarding (reduzir churn M1)
│ ☐ Implementar feature X (reduzir churn "falta features")
│ ☐ Criar plano mais barato (reduzir churn "preço alto")
│
└─────────────────────────────────────────────────────────────┘
```

---

## 4.10 Dashboard de Cenários & Monte Carlo - **NOVO**

```
┌─ SIMULAÇÃO DE CENÁRIOS ────────────────────────────────────┐
│
│ [Comparação: Base vs. Pessimista vs. Otimista]
│
│ Métrica         │ Base    │ Pessimista │ Otimista │
│ ────────────────┼─────────┼────────────┼──────────┤
│ MRR (Mês 36)    │ R$250k  │ R$120k     │ R$450k   │
│ Break-even      │ Mês 15  │ Mês 22     │ Mês 11   │
│ Vale da Morte   │ -R$35k  │ -R$65k     │ -R$18k   │
│ Caixa Final     │ R$180k  │ R$25k      │ R$420k   │
│
│ [Gráfico: Fan Chart (Monte Carlo 1000 simulações)]
│ ┌────────────────────────────────────────┐
│ │         ░░░░░░░                        │ ← P95
│ │       ░░░░░░░░░░░                      │
│ │     ░░░░█████████░░░                   │ ← P50
│ │   ░░░░░░░░░░░░░░░░░░░                  │
│ │ ░░░░░░░░░░░░░░░░░░░░░░░                │ ← P5
│ └────────────────────────────────────────┘
│
│ [Distribuição de Resultados]
│ Probabilidade de:
│ • Caixa > R$100k (Mês 36): 68%
│ • Break-even < Mês 18:     82%
│ • Falência (Caixa < 0):    5%
│
│ [Análise de Risco]
│ Risco Alto:      Churn > 7% (Prob: 15%)
│ Risco Médio:     Crescimento < 8% (Prob: 25%)
│ Risco Baixo:     Perda cliente key (Prob: 10%)
│
│ [Simulador de Recessão]
│ Cenário: Crise econômica Mês 12-18
│ • Receita -20%
│ • Churn dobra
│ • CAC sobe 30%
│ Resultado: Break-even adia 6 meses, Vale -R$58k
│
└─────────────────────────────────────────────────────────────┘
```

---

# 🔧 PARTE 5: TABELAS INTELIGENTES

## 5.1 Tabela Dinâmica Master

**Conceito:** Uma única tabela poderosa com filtros pré-programados

```
┌─ EXPLORADOR DE DADOS ──────────────────────────────────────┐
│
│ [Visualizações Rápidas] (tabs laterais)
│ ├─ 📊 DRE Completo
│ ├─ 💰 Fluxo de Caixa
│ ├─ 👥 Análise de Pessoal
│ ├─ 📈 Breakdown de Receita
│ ├─ 💸 Breakdown de COGS
│ ├─ 🏗️ Breakdown de OPEX
│ ├─ 🤖 Custos de IA
│ ├─ 📢 Análise de Marketing
│ ├─ 🏢 Custos de Infra
│ └─ 🎯 Métricas de Unit Economics
│
│ [Filtros Globais]
│ Período: [Mês 1] a [Mês 36] ▼
│ Cenário: [Base ▼] (pode comparar 2 cenários lado a lado)
│ Granularidade: ⦿ Mensal  ○ Trimestral  ○ Anual
│
│ [Colunas Personalizáveis] (arrastar e soltar)
│ ☑ Mês  ☑ MRR  ☑ Usuários  ☐ Trials  ☑ Churn%  ...
│
│ [Funções Avançadas]
│ • Adicionar coluna calculada
│ • Criar agrupamento
│ • Destacar células (ex: valores negativos em vermelho)
│ • Totalização (soma, média, mediana)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 5.2 Exemplo: DRE Detalhado (clicável)

```
┌─ DRE COMPLETO - MÊS 12 ────────────────────────────────────┐
│
│ RECEITA BRUTA                           R$ 45,000  [🔍]
│ ├─ MRR Plano Lite (45%)                 R$ 20,250  [🔍]
│ ├─ MRR Plano Trader (35%)               R$ 15,750  [🔍]
│ └─ MRR Plano Pro (20%)                  R$ 9,000   [🔍]
│
│ (-) COGS                                -R$ 13,500 [🔍]
│ ├─ Custo IA (450 users × R$5)          -R$ 2,250  [🔍]
│ ├─ Impostos (6%)                        -R$ 2,700  [🔍]
│ ├─ Taxa Pagamento (3.5%)                -R$ 1,575  [🔍]
│ ├─ Comissão Afiliados (30% vendas)     -R$ 2,700  [🔍]
│ └─ Outros COGS                          -R$ 4,275  [🔍]
│
│ = LUCRO BRUTO                           R$ 31,500  (70%)
│
│ (-) OPEX                                -R$ 28,800 [🔍]
│ ├─ Pessoal                              -R$ 16,800 [🔍]
│ │   ├─ Fundador                         -R$ 5,000
│ │   ├─ Dev Backend (CLT)                -R$ 13,440
│ │   └─ Designer (PJ)                    -R$ 3,000
│ ├─ Infraestrutura                       -R$ 5,650  [🔍]
│ │   ├─ Tier 2 (450 users)               -R$ 5,650
│ ├─ Marketing                             -R$ 4,500  [🔍]
│ │   ├─ Fase 2 (20% Lucro Bruto)         -R$ 4,500
│ ├─ Ferramentas SaaS                     -R$ 850    [🔍]
│ └─ Serviços Profissionais               -R$ 500    [🔍]
│
│ = EBITDA                                R$ 2,700   (6%)
│
│ (-) Depreciação                         -R$ 333    [🔍]
│
│ = RESULTADO OPERACIONAL                 R$ 2,367   (5.3%)
│
│ (+) Aportes                             R$ 1,800   [🔍]
│
│ = FLUXO DE CAIXA                        R$ 4,167
│
│ SALDO DE CAIXA ACUMULADO                R$ 38,245
│
│ [Cada 🔍 abre popup com drill-down visual]
│
└─────────────────────────────────────────────────────────────┘
```

---

## 5.3 Tabela: Breakdown de Custos (clicável)

```
┌─ RASTREADOR DE CUSTOS - MÊS 12 ────────────────────────────┐
│
│ Categoria         │ Valor    │ % Total │ Vs. Orç │ Trend │
│ ──────────────────┼──────────┼─────────┼─────────┼───────┤
│ 👥 Pessoal [🔍]   │ R$16,800 │ 58%     │ +5%     │ ▲     │
│ 🏗️ Infra [🔍]     │ R$5,650  │ 20%     │ -2%     │ ▬     │
│ 📢 Marketing [🔍] │ R$4,500  │ 16%     │ +12%    │ ▲▲    │
│ 🛠️ Ferramentas[🔍]│ R$850    │ 3%      │ 0%      │ ▬     │
│ 💼 Serviços [🔍]  │ R$500    │ 2%      │ 0%      │ ▬     │
│ 📉 Deprec. [🔍]   │ R$333    │ 1%      │ 0%      │ ▬     │
│ ──────────────────┼──────────┼─────────┼─────────┼───────┤
│ TOTAL             │ R$28,633 │ 100%    │ +3%     │       │
│
│ [Clicar em qualquer 🔍 mostra decomposição]
│
│ Exemplo: Clicando em "👥 Pessoal":
│ ┌─────────────────────────────────────┐
│ │ COMPOSIÇÃO: CUSTOS DE PESSOAL      │
│ │                                     │
│ │ [Gráfico de Pizza]                  │
│ │ • Dev Backend: R$13,440 (80%)      │
│ │ • Fundador: R$5,000 (30%)          │
│ │ • Designer PJ: R$3,000 (18%)       │
│ │                                     │
│ │ HISTÓRICO (últimos 6 meses)        │
│ │ [Gráfico de Linha por pessoa]      │
│ │                                     │
│ │ PROJEÇÃO (próximos 6 meses)        │
│ │ Mês 15: +Community Manager R$5k    │
│ │ Mês 18: +CFO R$10k                 │
│ │                                     │
│ │ [Fechar] [Exportar Detalhes]       │
│ └─────────────────────────────────────┘
│
└─────────────────────────────────────────────────────────────┘
```

---

# 🎨 PARTE 6: GRÁFICOS AVANÇADOS

## 6.1 Biblioteca de Tipos de Gráfico

**Para cada métrica, permitir escolher entre:**

1. **Linha** - Tendência ao longo do tempo
2. **Área** - Tendência com volume visual
3. **Barra** - Comparação entre períodos/categorias
4. **Barra Empilhada** - Composição ao longo do tempo
5. **Pizza/Donut** - Composição em um ponto
6. **Waterfall** - Como valores se somam/subtraem
7. **Sankey** - Fluxo de recursos
8. **Funil** - Conversão entre etapas
9. **Scatter** - Correlação entre 2 variáveis
10. **Heatmap** - Matriz 2D de valores
11. **Gauge** - Métrica vs. meta (velocímetro)
12. **Bullet Chart** - Progresso vs. target
13. **Box Plot** - Distribuição e outliers
14. **Violin Plot** - Distribuição detalhada
15. **Cohort Table** - Retenção por cohort

---

## 6.2 Gráficos Compostos (híbridos)

**Exemplos de combinações úteis:**

### A) MRR + Usuários (2 eixos)
```
┌─────────────────────────────────────┐
│     MRR (R$)                        │ ← Eixo esquerdo
│     ▲                               │
│ 50k │         ╱────                 │
│ 40k │       ╱                       │
│ 30k │     ╱                         │
│ 20k │   ╱                           │
│ 10k │ ╱                             │
│     └──────────────────────► Mês   │
│                                     │
│     ║║║║║║║║║║║║  ← Barras Usuários│ ← Eixo direito
└─────────────────────────────────────┘
```

### B) Receita vs. Custos (Stacked + Line)
```
┌─────────────────────────────────────┐
│ [Barras empilhadas: Receita]        │
│ [Linha: Total Custos]               │
│ [Área sombreada: Lucro]             │
└─────────────────────────────────────┘
```

### C) Burn Rate + Runway (Combo)
```
┌─────────────────────────────────────┐
│ [Barras: Burn mensal]               │
│ [Linha: Runway projetado]           │
│ [Zona vermelha: Runway < 6 meses]   │
└─────────────────────────────────────┘
```

---

## 6.3 Gráficos "PowerBI-Style"

### Cartões de Métricas Inteligentes

```
┌─────────────────────────┐
│ MRR                     │
│ R$ 45,000               │
│ ▲ +12% vs. mês anterior │
│ ▲ +145% vs. início      │
│                         │
│ [Mini sparkline] ╱──    │
│                         │
│ 🎯 Meta: R$50k          │
│ Faltam: R$5k (90%)      │
│                         │
│ [Ver Detalhes]          │
└─────────────────────────┘
```

### Gauge Chart (Velocímetro)

```
┌─────────────────────────┐
│   LTV/CAC RATIO         │
│                         │
│      ╱──────╲           │
│     ╱   4.2x ╲          │
│    │    👍    │         │
│    ╲          ╱         │
│     ╲────────╱          │
│                         │
│  1x    3x    5x    7x   │
│  🔴    🟡    🟢    🟢   │
│                         │
│ Status: SAUDÁVEL        │
└─────────────────────────┘
```

---

# 🏗️ PARTE 7: ARQUITETURA TÉCNICA

## 7.1 Estrutura de Arquivos (Nova)

```
SAM_Financial_Model_v4/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Home + Router
│   ├── pages/
│   │   ├── 01_📊_Dashboard_Receita.py
│   │   ├── 02_💸_Dashboard_Custos.py
│   │   ├── 03_💰_Dashboard_Caixa.py
│   │   ├── 04_👥_Dashboard_Equipe.py
│   │   ├── 05_📢_Dashboard_Marketing.py
│   │   ├── 06_🎯_Unit_Economics.py
│   │   ├── 07_📈_Analise_Sensibilidade.py
│   │   ├── 08_🔄_Cohorts.py
│   │   ├── 09_🎲_Cenarios_MonteCarlo.py
│   │   ├── 10_📋_Tabelas.py
│   │   ├── 11_⚙️_Configuracoes.py
│   │   └── 12_📚_Glossario.py
│   │
│   ├── components/                 # NOVO: Componentes reutilizáveis
│   │   ├── __init__.py
│   │   ├── metrics.py              # Cartões de métricas
│   │   ├── charts.py               # Gráficos padrão
│   │   ├── tables.py               # Tabelas interativas
│   │   ├── filters.py              # Filtros globais
│   │   ├── drill_down.py           # Popups de drill-down
│   │   └── insights.py             # Sistema de insights
│   │
│   └── utils/                      # NOVO: Utilitários
│       ├── __init__.py
│       ├── formatters.py           # Formatação de valores
│       ├── validators.py           # Validação de inputs
│       └── exporters.py            # Export PDF/Excel/PowerPoint
│
├── core/
│   ├── __init__.py
│   ├── config.py                   # ✅ Expandir
│   ├── engine.py                   # ✅ Expandir
│   ├── analysis.py                 # ✅ Criar/Expandir
│   ├── glossary.py                 # ✅ OK
│   ├── visualizations.py           # ✅ Expandir
│   │
│   ├── builders/                   # NOVO: Configuradores
│   │   ├── __init__.py
│   │   ├── capital_builder.py      # Aportes, empréstimos
│   │   ├── revenue_builder.py      # Planos, upsell, add-ons
│   │   ├── cogs_builder.py         # Taxas, comissões
│   │   ├── infra_builder.py        # Tiers de infraestrutura
│   │   ├── marketing_builder.py    # Fases, canais
│   │   ├── team_builder.py         # Equipe + gatilhos
│   │   └── scenario_builder.py     # Cenários completos
│   │
│   ├── analytics/                  # NOVO: Análises avançadas
│   │   ├── __init__.py
│   │   ├── sensitivity.py          # Análise de sensibilidade
│   │   ├── montecarlo.py           # Simulação Monte Carlo
│   │   ├── cohorts.py              # Análise de cohorts
│   │   ├── forecasting.py          # Previsões avançadas
│   │   └── insights_engine.py      # Gerador de insights
│   │
│   └── risk/                       # NOVO: Gestão de riscos
│       ├── __init__.py
│       ├── risk_scenarios.py       # Cenários de risco
│       ├── contingency.py          # Planos de contingência
│       └── alerts.py               # Sistema de alertas
│
├── data/                           # NOVO: Armazenamento
│   ├── scenarios/                  # Cenários salvos (JSON)
│   ├── exports/                    # Relatórios exportados
│   └── templates/                  # Templates de config
│
├── tests/   
│   ├── test_config.py
│   ├── test_engine.py
│   ├── test_builders.py
│   ├── test_analytics.py
│   └── test_integration.py
│
├── notebooks/                      # Jupyter notebooks
│   ├── 01_overview.ipynb
│   ├── 02_engine_deep_dive.ipynb
│   ├── 03_montecarlo.ipynb
│   ├── 04_sensibilidade.ipynb
│   └── 05_case_studies.ipynb
│
├── docs/                           # NOVO: Documentação
│   ├── user_guide.md
│   ├── technical_docs.md
│   ├── api_reference.md
│   └── screenshots/
│
├── requirements.txt
├── setup.py
├── README.md
└── .streamlit/                     # NOVO: Config Streamlit
    └── config.toml                 # Tema, cores, etc.





---

## 7.2 Módulos Principais a Criar/Expandir

### 🔴 CRÍTICO (Fazer Primeiro)

#### 1. `core/builders/` (NOVO - Prioridade #1)
**Propósito:** Interfaces de configuração avançada

**Arquivos:**
- `capital_builder.py` - Múltiplos aportes, empréstimos
- `revenue_builder.py` - Mix de planos evolutivo, upsell
- `cogs_builder.py` - Taxas, comissões, afiliados
- `infra_builder.py` - Tiers configuráveis
- `marketing_builder.py` - 4 fases + canais
- `team_builder.py` - Gatilhos de contratação
- `scenario_builder.py` - Gerenciador de cenários

**Exemplo de estrutura (`team_builder.py`):**
```python
class TeamBuilder:
    def __init__(self, config: ConfigFinanceira):
        self.config = config
        self.positions = []
    
    def add_position_with_trigger(
        self,
        cargo: str,
        salario: float,
        trigger_type: str,  # 'mrr', 'usuarios', 'mes'
        trigger_value: float,
        tipo: str = 'CLT'
    ):
        # Lógica para adicionar cargo com gatilho
        pass
    
    def calculate_hiring_timeline(self, df_projecao: pd.DataFrame):
        # Retorna DataFrame com mês de contratação de cada cargo
        pass
    
    def estimate_team_costs(self, meses: int):
        # Projeta custos de equipe considerando gatilhos
        pass
```

---

#### 2. `core/analytics/insights_engine.py` (NOVO - Prioridade #2)
**Propósito:** Geração automática de insights

**Classes:**
```python
class InsightsEngine:
    def __init__(self, df_projecao, kpis, config):
        self.df = df_projecao
        self.kpis = kpis
        self.config = config
    
    def generate_all_insights(self):
        return {
            'alertas': self.detectar_alertas(),
            'oportunidades': self.detectar_oportunidades(),
            'recomendacoes': self.gerar_recomendacoes(),
            'previsoes': self.gerar_previsoes()
        }
    
    def detectar_alertas(self):
        alertas = []
        
        # Alerta: Vale da Morte próximo
        if self.kpis['Vale_da_Morte_Mes'] <= 6:
            alertas.append({
                'tipo': 'CRÍTICO',
                'mensagem': f"Vale da Morte em {self.kpis['Vale_da_Morte_Mes']} meses",
                'valor': self.kpis['Vale_da_Morte_Minimo_Caixa'],
                'acao': f"Captar {abs(self.kpis['Vale_da_Morte_Minimo_Caixa']) * 1.3:.0f} URGENTE"
            })
        
        # Alerta: LTV/CAC baixo
        if self.kpis['LTV_CAC_Ratio_Final'] < 3.0:
            alertas.append({
                'tipo': 'ATENÇÃO',
                'mensagem': 'LTV/CAC abaixo do mínimo viável',
                'valor': self.kpis['LTV_CAC_Ratio_Final'],
                'acao': 'Reduzir CAC ou aumentar retenção'
            })
        
        # Alerta: Churn alto
        churn_medio = self.df['Usuarios_Perdidos'].sum() / self.df['Usuarios_Finais'].sum()
        if churn_medio > 0.05:
            alertas.append({
                'tipo': 'CRÍTICO',
                'mensagem': f'Churn médio muito alto: {churn_medio*100:.1f}%',
                'valor': churn_medio,
                'acao': 'Investigar causas e implementar programa de retenção'
            })
        
        return alertas
    
    def detectar_oportunidades(self):
        oportunidades = []
        
        # Oportunidade: Crescimento acelerando
        crescimento_recente = self.df['MRR'].pct_change().tail(3).mean()
        if crescimento_recente > 0.15:
            oportunidades.append({
                'tipo': 'CRESCIMENTO',
                'mensagem': 'Crescimento acelerando! Considere investir mais em marketing',
                'impacto': 'Se manter ritmo, atingirá break-even 2 meses antes'
            })
        
        # Oportunidade: CAC de canal específico muito bom
        # (precisa ter dados por canal)
        
        return oportunidades
    
    def gerar_recomendacoes(self):
        recomendacoes = []
        
        # Recomendação: Otimização de custos
        if self.df['OPEX_Total'].iloc[-1] / self.df['MRR'].iloc[-1] > 0.7:
            recomendacoes.append({
                'area': 'CUSTOS',
                'mensagem': 'OPEX representa >70% da receita',
                'acao': 'Analisar possibilidade de reduzir custos fixos',
                'impacto_estimado': 'Poderia adiantar break-even em 1-2 meses'
            })
        
        return recomendacoes
    
    def gerar_previsoes(self):
        # Usar regressão simples para prever tendências
        pass
```

---

#### 3. `app/components/drill_down.py` (NOVO - Prioridade #3)
**Propósito:** Sistema de drill-down para gráficos

**Exemplo:**
```python
import streamlit as st
import plotly.graph_objects as go

class DrillDownSystem:
    def __init__(self):
        if 'drill_down_stack' not in st.session_state:
            st.session_state.drill_down_stack = []
    
    def create_drillable_metric(
        self,
        label: str,
        value: float,
        breakdown: dict,
        format_func=None
    ):
        """
        Cria métrica com drill-down
        
        Args:
            label: "OPEX Total"
            value: 28800
            breakdown: {
                'Pessoal': 16800,
                'Infra': 5650,
                'Marketing': 4500,
                ...
            }
        """
        col1, col2 = st.columns([3, 1])
        
        with col1:
            formatted_value = format_func(value) if format_func else f"R$ {value:,.0f}"
            st.metric(label, formatted_value)
        
        with col2:
            if st.button("🔍", key=f"drill_{label}"):
                self._show_breakdown_popup(label, breakdown, format_func)
    
    def _show_breakdown_popup(self, label, breakdown, format_func):
        # Modal/expander com breakdown
        with st.expander(f"📊 Composição: {label}", expanded=True):
            # Gráfico de pizza
            fig = go.Figure(data=[go.Pie(
                labels=list(breakdown.keys()),
                values=list(breakdown.values()),
                hole=0.3
            )])
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            df_breakdown = pd.DataFrame({
                'Categoria': breakdown.keys(),
                'Valor': breakdown.values()
            })
            df_breakdown['%'] = (df_breakdown['Valor'] / df_breakdown['Valor'].sum() * 100).round(1)
            df_breakdown = df_breakdown.sort_values('Valor', ascending=False)
            st.dataframe(df_breakdown, use_container_width=True)
            
            # Botão para drill mais fundo (se houver)
            if 'sub_breakdown' in breakdown:
                # Permitir drill em sub-categorias
                pass
```

---

### 🟡 IMPORTANTE (Fazer em Seguida)

#### 4. `core/analytics/montecarlo.py` (Expandir)
**Adicionar:**
- Distribuições configuráveis por variável
- Correlação entre variáveis (ex: churn ↑ quando crescimento ↑)
- Cenários de risco incluídos
- Análise de percentis detalhada (P1, P5, P10, P25, P50, P75, P90, P95, P99)

---

#### 5. `core/analytics/cohorts.py` (NOVO)
**Funcionalidade:**
- Análise de retenção por cohort
- Heatmap de retenção
- Churn por cohort
- Lifetime por cohort
- Comparação entre cohorts

---

#### 6. `app/components/charts.py` (Expandir)
**Adicionar todos os tipos de gráfico:**
```python
class ChartLibrary:
    @staticmethod
    def waterfall_chart(valores: dict, title: str):
        # Gráfico waterfall (receita → lucro)
        pass
    
    @staticmethod
    def sankey_diagram(flows: dict, title: str):
        # Diagrama Sankey (fluxo de dinheiro)
        pass
    
    @staticmethod
    def funnel_chart(stages: dict, title: str):
        # Funil de conversão
        pass
    
    @staticmethod
    def gauge_chart(value: float, min_val: float, max_val: float, target: float):
        # Velocímetro
        pass
    
    @staticmethod
    def cohort_heatmap(df_cohort: pd.DataFrame):
        # Heatmap de retenção por cohort
        pass
    
    @staticmethod
    def dual_axis_chart(df: pd.DataFrame, y1_col: str, y2_col: str):
        # Gráfico com 2 eixos Y
        pass
    
    @staticmethod
    def combo_chart(df: pd.DataFrame, bar_cols: list, line_cols: list):
        # Barras + linhas no mesmo gráfico
        pass
```

---

#### 7. `core/risk/alerts.py` (NOVO)
**Sistema de alertas automáticos:**
```python
class AlertSystem:
    def __init__(self, df_projecao, kpis, config):
        self.df = df_projecao
        self.kpis = kpis
        self.config = config
        self.alerts = []
    
    def check_all_alerts(self):
        self._check_cash_alerts()
        self._check_growth_alerts()
        self._check_unit_economics_alerts()
        self._check_team_alerts()
        return self.alerts
    
    def _check_cash_alerts(self):
        # Runway < 6 meses
        # Vale da Morte próximo
        # Caixa negativo em X meses
        pass
    
    def _check_growth_alerts(self):
        # Crescimento desacelerando
        # Churn aumentando
        # CAC subindo
        pass
    
    def _check_unit_economics_alerts(self):
        # LTV/CAC < 3
        # Payback > 12 meses
        # Margem bruta < 60%
        pass
```

---

### 🟢 DESEJÁVEL (Fazer Depois)

#### 8. `app/utils/exporters.py` (NOVO)
**Exportação avançada:**
- PDF com relatório executivo completo
- PowerPoint com slides prontos
- Excel com múltiplas abas e formatação
- JSON para integração com outras ferramentas

---

#### 9. `core/integration/` (NOVO - Futuro)
**Integrações externas:**
- Importar dados reais de CRM (Pipedrive, HubSpot)
- Importar dados de Analytics (Google Analytics, Mixpanel)
- Importar dados de Gateway (Stripe, Mercado Pago)
- API REST para alimentar o modelo com dados reais

---

# 📊 PARTE 8: LÓGICA DE CONEXÕES E FLUXOS

## 8.1 Fluxo de Dados Principal

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DE DADOS SAM v4                    │
└─────────────────────────────────────────────────────────────┘

1. CONFIGURAÇÃO (Input do Usuário)
   │
   ├─ UI Streamlit (Sidebar + Páginas de Config)
   │  └─> Builders (capital, revenue, team, etc.)
   │      └─> ConfigFinanceira (objeto consolidado)
   │
2. PROCESSAMENTO (Engine)
   │
   ├─> MotorProjecaoFinanceira.executar_projecao()
   │   ├─ Loop mês a mês (1 a N meses)
   │   ├─ Aplica regras de negócio
   │   ├─ Calcula métricas derivadas
   │   └─> DataFrame completo (36 colunas × N linhas)
   │
   ├─> MotorProjecaoFinanceira.calcular_kpis()
   │   └─> Dict de KPIs (Break-even, LTV, CAC, etc.)
   │
3. ANÁLISE AVANÇADA (Analytics)
   │
   ├─> InsightsEngine.generate_all_insights()
   │   └─> Alertas, Oportunidades, Recomendações
   │
   ├─> MonteCarloSimulator.run(n=1000)
   │   └─> Distribuição de resultados
   │
   ├─> SensitivityAnalyzer.analyze()
   │   └─> Tornado chart, Heatmaps
   │
   └─> CohortAnalyzer.analyze()
       └─> Retention tables, Churn por cohort
   │
4. VISUALIZAÇÃO (Dashboard)
   │
   ├─> Dashboards temáticos (Receita, Custos, Caixa, etc.)
   │   ├─ Gráficos interativos (Plotly)
   │   ├─ Drill-down system (popups)
   │   └─ Filtros globais
   │
   ├─> Tabelas dinâmicas
   │   └─ Filtros, sorting, agrupamento
   │
   └─> Insights automatizados
       └─ Cards de alerta/oportunidade
   │
5. EXPORTAÇÃO (Output)
   │
   └─> Exporters
       ├─ PDF (relatório executivo)
       ├─ Excel (dados + gráficos)
       ├─ PowerPoint (apresentação)
       └─ JSON (backup de cenário)
```

---

## 8.2 Correlações entre Módulos

### Mapa de Dependências

```
ConfigFinanceira (core/config.py)
    ↓
    ├─> Usado por: MotorProjecaoFinanceira
    ├─> Usado por: Builders (para construção incremental)
    ├─> Usado por: ScenarioManager (para salvar/carregar)
    └─> Usado por: Validators (para validação)

MotorProjecaoFinanceira (core/engine.py)
    ↓
    ├─> Recebe: ConfigFinanceira
    ├─> Retorna: DataFrame projecao + Dict KPIs
    ├─> Usado por: Todos os dashboards
    ├─> Usado por: MonteCarloSimulator (roda N vezes)
    └─> Usado por: SensitivityAnalyzer (varia parâmetros)

InsightsEngine (core/analytics/insights_engine.py)
    ↓
    ├─> Recebe: DataFrame + KPIs + Config
    ├─> Retorna: Dict de insights
    ├─> Usado por: Dashboard principal (alertas)
    └─> Usado por: Relatórios automáticos

DrillDownSystem (app/components/drill_down.py)
    ↓
    ├─> Recebe: Métricas + Breakdown
    ├─> Retorna: Popups interativos
    └─> Usado por: Todos os dashboards

ChartLibrary (app/components/charts.py)
    ↓
    ├─> Recebe: DataFrames + Config de visualização
    ├─> Retorna: Gráficos Plotly
    └─> Usado por: Todos os dashboards
```

---

## 8.3 Session State Management

**Variáveis críticas em `st.session_state`:**

```python
# Dados principais
st.session_state.config           # ConfigFinanceira atual
st.session_state.df_projecao      # DataFrame de projeção
st.session_state.kpis             # Dict de KPIs
st.session_state.insights         # Dict de insights

# Cenários
st.session_state.cenarios         # Dict de cenários salvos
st.session_state.cenario_ativo    # Nome do cenário ativo

# Filtros globais
st.session_state.filtro_periodo   # (mes_inicio, mes_fim)
st.session_state.filtro_granular  # 'mensal', 'trimestral', 'anual'

# Drill-down
st.session_state.drill_stack      # Pilha de drill-downs
st.session_state.drill_data       # Dados do drill atual

# Análises
st.session_state.montecarlo_results  # Resultados da última simulação MC
st.session_state.sensitivity_data    # Dados da análise de sensibilidade
st.session_state.cohort_data         # Dados de cohort

# UI State
st.session_state.sidebar_expanded    # Sidebar aberto/fechado
st.session_state.dark_mode           # Modo escuro/claro
```

---

# 🎯 PARTE 9: PLANO DE IMPLEMENTAÇÃO

## Fase 1: Foundation (Semana 1-2) ⭐⭐⭐

### Objetivo: Base sólida e configuração avançada

**Tarefas:**

1. **Criar estrutura de pastas completa**
   - [ ] `core/builders/`
   - [ ] `core/analytics/`
   - [ ] `core/risk/`
   - [ ] `app/components/`
   - [ ] `app/utils/`
   - [ ] `data/scenarios/`

2. **Expandir `core/config.py`**
   - [ ] Adicionar campos para múltiplos aportes
   - [ ] Adicionar sistema de impostos progressivos
   - [ ] Adicionar comissões de afiliados/parceiros
   - [ ] Adicionar contingência/reserva

3. **Criar Builders básicos**
   - [ ] `capital_builder.py` (aportes múltiplos)
   - [ ] `team_builder.py` (gatilhos de contratação)
   - [ ] `infra_builder.py` (tiers configuráveis)
   - [ ] `marketing_builder.py` (4 fases)

4. **Expandir `core/engine.py`**
   - [ ] Adicionar cálculo de aportes múltiplos
   - [ ] Adicionar lógica de gatilhos de contratação
   - [ ] Adicionar transições de tier automáticas
   - [ ] Adicionar fases de marketing dinâmicas
   - [ ] Adicionar coluna de "decomposição" para cada valor (rastreabilidade)

**Entregável:** App funciona com configuração avançada

---

## Fase 2: Intelligence Layer (Semana 3-4) ⭐⭐⭐

### Objetivo: Insights e alertas automáticos

**Tarefas:**

1. **Criar `core/analytics/insights_engine.py`**
   - [ ] `detectar_alertas()` (5 tipos de alerta)
   - [ ] `detectar_oportunidades()` (3 tipos)
   - [ ] `gerar_recomendacoes()` (análise automatizada)
   - [ ] `gerar_previsoes()` (regressão simples)

2. **Criar `core/risk/alerts.py`**
   - [ ] Sistema de alertas com severidade (crítico, atenção, info)
   - [ ] Alertas de caixa (runway, vale da morte)
   - [ ] Alertas de crescimento (desaceleração, churn)
   - [ ] Alertas de unit economics (LTV/CAC, payback)

3. **Integrar no Dashboard Principal**
   - [ ] Seção de "Alertas Críticos" no topo
   - [ ] Seção de "Insights" logo abaixo
   - [ ] Seção de "Próximas Metas" com timeline

**Entregável:** Dashboard mostra alertas e insights inteligentes

---

## Fase 3: Visualization & Drill-Down (Semana 5-6) ⭐⭐

### Objetivo: Visualização rica e interativa

**Tarefas:**

1. **Criar `app/components/drill_down.py`**
   - [ ] Sistema de popups para drill-down
   - [ ] Decomposição de métricas em sub-componentes
   - [ ] Navegação "breadcrumb" (voltar níveis)

2. **Expandir `app/components/charts.py`**
   - [ ] Waterfall chart
   - [ ] Sankey diagram
   - [ ] Funnel chart
   - [ ] Gauge chart
   - [ ] Cohort heatmap
   - [ ] Dual-axis chart
   - [ ] Combo chart (barras + linhas)

3. **Criar Dashboards Temáticos**
   - [ ] Dashboard de Receita (breakdown, cohorts, funil)
   - [ ] Dashboard de Custos (sankey, pizza drill-down, fixos vs variáveis)
   - [ ] Dashboard de Caixa (zones, runway, simulador "e se")
   - [ ] Dashboard de Equipe (timeline, produtividade)
   - [ ] Dashboard de Marketing (ROI por canal, CAC evolution)

4. **Redesenhar Dashboard Principal**
   - [ ] Cards de métricas com mini sparklines
   - [ ] Seção de alertas destacada
   - [ ] Timeline visual de marcos
   - [ ] Comparação vs. meta (gauge charts)

**Entregável:** 6 dashboards temáticos + drill-down funcional

---

## Fase 4: Advanced Analytics (Semana 7-8) ⭐

### Objetivo: Monte Carlo, Sensibilidade, Cohorts

**Tarefas:**

1. **Expandir `core/analytics/montecarlo.py`**
   - [ ] Distribuições configuráveis
   - [ ] Correlação entre variáveis
   - [ ] Inclusão de cenários de risco
   - [ ] Fan chart visualization

2. **Criar `core/analytics/sensitivity.py`**
   - [ ] Análise univariada (tornado chart)
   - [ ] Análise bivariada (heatmap 2D)
   - [ ] Spider chart (múltiplas variáveis)

3. **Criar `core/analytics/cohorts.py`**
   - [ ] Cohort retention table
   - [ ] Heatmap de retenção
   - [ ] Análise de churn por cohort
   - [ ] LTV por cohort

4. **Criar Dashboard de Cenários**
   - [ ] Comparação Base vs. Pessimista vs. Otimista
   - [ ] Fan chart de Monte Carlo
   - [ ] Simulador "E se...?" interativo
   - [ ] Análise de risco (probabilidades)

**Entregável:** Análises avançadas completas

---

## Fase 5: Tables & Export (Semana 9) ⭐

### Objetivo: Tabelas dinâmicas e exportação

**Tarefas:**

1. **Criar sistema de tabelas dinâmicas**
   - [ ] Filtros pré-programados (DRE, Fluxo, Breakdown COGS, etc.)
   - [ ] Colunas personalizáveis (arrastar e soltar)
   - [ ] Agrupamentos configuráveis
   - [ ] Destacar células (condicional)
   - [ ] Totalização (soma, média, mediana)

2. **Criar `app/utils/exporters.py`**
   - [ ] Export PDF (relatório executivo multi-página)
   - [ ] Export Excel (múltiplas abas + formatação)
   - [ ] Export PowerPoint (slides prontos)
   - [ ] Export JSON (cenário completo)

3. **Integrar no app**
   - [ ] Botão "Exportar Relatório" no dashboard principal
   - [ ] Escolher formato (PDF/Excel/PPT)
   - [ ] Preview antes de baixar

**Entregável:** Sistema completo de tabelas e exportação

---

## Fase 6: Polish & UX (Semana 10) ⭐

### Objetivo: Refinamento de UX e performance

**Tarefas:**

1. **Melhorar UI/UX**
   - [ ] Tema customizado (`.streamlit/config.toml`)
   - [ ] Cores consistentes (palette)
   - [ ] Ícones em todos os lugares
   - [ ] Loading states elegantes
   - [ ] Empty states (quando não há dados)
   - [ ] Error messages claros

2. **Performance**
   - [ ] Cache agressivo (`@st.cache_data`)
   - [ ] Lazy loading de dashboards
   - [ ] Otimizar gráficos pesados
   - [ ] Debounce em inputs

3. **Documentação**
   - [ ] Tooltips em todos os campos
   - [ ] Help buttons com explicações
   - [ ] Tutorial interativo (primeira vez)
   - [ ] README.md completo
   - [ ] Vídeo demo

**Entregável:** App polido e rápido

---

# 📝 PARTE 10: CHECKLIST DE FEATURES

## ✅ Configuração Avançada

- [ ] Múltiplos aportes programados
- [ ] Empréstimos com juros
- [ ] Impostos progressivos (Simples → Lucro Real)
- [ ] Reserva de contingência (% receita)
- [ ] Canais de aquisição separados
- [ ] Mix de planos evolutivo
- [ ] Upsell/Downsell configurável
- [ ] Add-ons e extras
- [ ] Taxas de pagamento completas
- [ ] Comissões de afiliados
- [ ] Comissões de parceiros
- [ ] Cashback/incentivos
- [ ] Infraestrutura em tiers configurável
- [ ] Transição automática entre tiers
- [ ] Marketing em 4 fases
- [ ] Orçamento por canal de marketing
- [ ] Salário fundador em fases
- [ ] Pró-labore condicional
- [ ] Múltiplos sócios/investidores
- [ ] Participação nos lucros
- [ ] Equipe com gatilhos de contratação
- [ ] Reajustes salariais programados
- [ ] Benefícios configuráveis (VR, VT, Plano)
- [ ] Decisão de escritório (Remoto/Híbrido/Presencial)
- [ ] Ferramentas SaaS por categoria
- [ ] Custos por usuário (ex: Notion)
- [ ] Upgrade automático de ferramentas
- [ ] Contabilidade escalável
- [ ] Consultorias específicas
- [ ] Depreciação com vida útil configurável
- [ ] Cenários de risco (recessão, churn spike)

## ✅ Inteligência e Insights

- [ ] Alertas críticos automáticos
- [ ] Detecção de oportunidades
- [ ] Recomendações automatizadas
- [ ] Previsões de tendências
- [ ] Comparação vs. metas
- [ ] Timeline de marcos importantes
- [ ] "E se...?" interativo

## ✅ Dashboards

- [ ] Dashboard Principal (home)
- [ ] Dashboard de Receita
- [ ] Dashboard de Custos
- [ ] Dashboard de Caixa & Viabilidade
- [ ] Dashboard de Equipe
- [ ] Dashboard de Marketing
- [ ] Dashboard de Unit Economics
- [ ] Dashboard de Sensibilidade
- [ ] Dashboard de Cohorts
- [ ] Dashboard de Cenários & Monte Carlo

## ✅ Visualizações

- [ ] Gráficos de linha
- [ ] Gráficos de área
- [ ] Gráficos de barra
- [ ] Barras empilhadas
- [ ] Pizza/Donut
- [ ] Waterfall
- [ ] Sankey
- [ ] Funil
- [ ] Scatter plot
- [ ] Heatmap
- [ ] Gauge (velocímetro)
- [ ] Bullet chart
- [ ] Cohort table
- [ ] Fan chart (Monte Carlo)
- [ ] Tornado chart (sensibilidade)
- [ ] Spider chart
- [ ] Dual-axis charts
- [ ] Combo charts (barras + linhas)
- [ ] Mini sparklines em cards

## ✅ Drill-Down e Interatividade

- [ ] Clicar em métrica → ver breakdown
- [ ] Clicar em gráfico → drill-down
- [ ] Popup de decomposição
- [ ] Navegação breadcrumb
- [ ] Drill em múltiplos níveis
- [ ] Hover tooltips em tudo
- [ ] Filtros globais (período, cenário)
- [ ] Filtros específicos por dashboard

## ✅ Tabelas

- [ ] Tabela dinâmica master
- [ ] Filtros pré-programados
- [ ] DRE detalhado clicável
- [ ] Fluxo de caixa detalhado
- [ ] Breakdown de custos por categoria
- [ ] Análise de pessoal
- [ ] Análise de marketing
- [ ] Colunas personalizáveis
- [ ] Agrupamentos configuráveis
- [ ] Destacar células condicional
- [ ] Totalização (soma, média, mediana)
- [ ] Sorting multi-coluna
- [ ] Export individual de tabelas
- [ ] Comparação lado a lado (2 cenários)
- [ ] Granularidade ajustável (mensal/trimestral/anual)

## ✅ Análises Avançadas

- [ ] Monte Carlo com 500+ simulações
- [ ] Distribuições configuráveis por variável
- [ ] Correlação entre variáveis
- [ ] Fan chart visual
- [ ] Percentis (P5, P50, P95)
- [ ] Probabilidade de resultados
- [ ] Análise de sensibilidade univariada
- [ ] Análise de sensibilidade bivariada
- [ ] Tornado chart
- [ ] Heatmap 2D
- [ ] Spider chart
- [ ] Análise de cohorts
- [ ] Retention table
- [ ] Churn por cohort
- [ ] LTV por cohort
- [ ] Comparação entre cohorts

## ✅ Cenários

- [ ] Salvar cenários com nome
- [ ] Carregar cenários salvos
- [ ] Comparar 3 cenários lado a lado
- [ ] Base vs. Pessimista vs. Otimista
- [ ] Cenários de risco (recessão, etc.)
- [ ] Export/Import de cenários (JSON)
- [ ] Templates de cenários
- [ ] Duplicar e modificar cenário

## ✅ Exportação

- [ ] CSV simples
- [ ] Excel com múltiplas abas
- [ ] Excel com formatação rica
- [ ] PDF - Relatório Executivo
- [ ] PDF - Relatório Técnico
- [ ] PowerPoint com slides prontos
- [ ] JSON (backup completo)
- [ ] Agendamento de relatórios (futuro)

## ✅ UX/UI

- [ ] Tema customizado
- [ ] Modo escuro/claro
- [ ] Sidebar com navegação clara
- [ ] Breadcrumbs
- [ ] Loading states elegantes
- [ ] Empty states informativos
- [ ] Error messages claros
- [ ] Success feedbacks
- [ ] Tooltips em todos os campos
- [ ] Help buttons contextuais
- [ ] Tutorial interativo (primeira vez)
- [ ] Atalhos de teclado
- [ ] Responsive (mobile-friendly)

## ✅ Performance

- [ ] Cache agressivo
- [ ] Lazy loading de dashboards
- [ ] Debounce em inputs
- [ ] Otimização de gráficos
- [ ] Paginação em tabelas grandes
- [ ] Background processing (Monte Carlo)

---

# 🔄 PARTE 11: MATRIZ DE PRIORIDADES

## Prioridade CRÍTICA (Fazer AGORA) 🔴

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Builders (capital, team, infra, marketing)** | 🔥🔥🔥 | 3-4 dias | Sem isso, não há configuração avançada |
| **Insights Engine** | 🔥🔥🔥 | 2-3 dias | Transforma o app de calculadora em ferramenta estratégica |
| **Drill-Down System** | 🔥🔥🔥 | 2 dias | Resolve problema da "caixa preta" |
| **Dashboard de Custos com breakdown** | 🔥🔥 | 2 dias | Auditoria é impossível sem isso |
| **Gatilhos de contratação** | 🔥🔥 | 1 dia | Planejamento de equipe é essencial |
| **Tiers de infraestrutura configuráveis** | 🔥🔥 | 1 dia | Custos escaláveis são core do modelo |
| **4 fases de marketing** | 🔥🔥 | 1 dia | Marketing é 20-30% dos custos |

**Total estimado: 12-15 dias úteis (3 semanas)**

---

## Prioridade ALTA (Logo em seguida) 🟡

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Dashboards temáticos (Receita, Caixa, Equipe, Marketing)** | 🔥🔥 | 4-5 dias | Visibilidade segmentada |
| **Gráficos avançados (Waterfall, Sankey, Funnel)** | 🔥🔥 | 2-3 dias | Melhora muito a comunicação |
| **Sistema de alertas** | 🔥🔥 | 1-2 dias | Proatividade nas decisões |
| **Tabelas dinâmicas com filtros** | 🔥 | 2 dias | Flexibilidade de análise |
| **Monte Carlo expandido** | 🔥 | 2 dias | Análise de risco robusta |
| **Análise de sensibilidade** | 🔥 | 2 dias | Entender alavancas de negócio |

**Total estimado: 13-16 dias úteis (3 semanas)**

---

## Prioridade MÉDIA (Quando tiver tempo) 🟢

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Análise de cohorts** | 🔥 | 2 dias | Importante mas não urgente |
| **Export PDF/PowerPoint** | 🔥 | 3 dias | Nice to have para apresentações |
| **Cenários salvos** | 🔥 | 1 dia | Conveniência |
| **Tutorial interativo** | 🔥 | 2 dias | Onboarding |
| **Modo escuro** | 🔥 | 1 dia | UX |

**Total estimado: 9 dias úteis (2 semanas)**

---

## Prioridade BAIXA (Futuro) ⚪

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|---|
| **Integrações externas (Stripe, GA, CRM)** | 🔥 | 5+ dias | Futuro: dados reais |
| **API REST** | 🔥 | 3+ dias | Futuro: integração com outros sistemas |
| **Multi-usuário** | 🔥 | 5+ dias | Futuro: colaboração |
| **Agendamento de relatórios** | 🔥 | 2 dias | Automação |

---

# 🎯 PARTE 12: ROADMAP VISUAL

```
MÊS 1: FOUNDATION & INTELLIGENCE
├─ Semana 1-2: Builders + Config avançada
│  └─ Entregável: Configuração completa funcionando
│
└─ Semana 3-4: Insights Engine + Alertas
   └─ Entregável: Dashboard inteligente com alertas

MÊS 2: VISUALIZATION & ANALYTICS
├─ Semana 5-6: Drill-down + Dashboards temáticos
│  └─ Entregável: 6 dashboards com drill-down
│
└─ Semana 7-8: Monte Carlo + Sensibilidade + Cohorts
   └─ Entregável: Análises avançadas completas

MÊS 3: POLISH & EXPORT
├─ Semana 9: Tabelas dinâmicas + Export
│  └─ Entregável: Sistema completo de relatórios
│
└─ Semana 10: UX/UI + Performance + Docs
   └─ Entregável: App production-ready

MÊS 4+: FUTURE (Opcional)
└─ Integrações, API, Multi-usuário
```

---

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

---

# 🎯 PARTE 15: RESUMO EXECUTIVO DO PLANO

## O Que Temos Hoje

✅ Engine funcional básico  
✅ Configuração simples  
✅ Dashboard com gráficos básicos  
✅ Tabelas simples  
✅ Export CSV/Excel básico  

## O Que Falta (Crítico)

❌ Configuração avançada (builders)  
❌ Insights automáticos  
❌ Drill-down em gráficos/métricas  
❌ Dashboards temáticos  
❌ Análises avançadas (MC, Sensibilidade, Cohorts)  
❌ Tabelas dinâmicas  
❌ Auditoria de valores (rastreabilidade)  

## Impacto da Implementação

**Antes:** "Calculadora financeira simples"  
**Depois:** "Centro de comando estratégico"

**Antes:** CFO pergunta "de onde veio esse número?"  
**Depois:** CFO clica no número e vê breakdown completo

**Antes:** Decisões baseadas em feeling  
**Depois:** Decisões baseadas em simulações e insights

## Esforço Total Estimado

- **Fase 1 (Crítica):** 3 semanas
- **Fase 2 (Alta):** 3 semanas
- **Fase 3 (Média):** 2 semanas
- **Total:** 8 semanas (2 meses)

## ROI do Desenvolvimento

**Investimento:** 2 meses de desenvolvimento  
**Retorno:**
- Decisões financeiras 10x mais informadas
- Redução de 50% no tempo de análise
- Capacidade de captar investimento com apresentação profissional
- Ferramenta proprietária que pode ser comercializada

---

# ✅ PRÓXIMOS PASSOS IMEDIATOS

1. **Você confirma este plano** ✋
2. **Priorizamos juntos** o que fazer primeiro
3. **Começo a implementar** os Builders (Fase 1)
4. **Entregas incrementais** a cada 3-4 dias

**Devo começar pela Fase 1 (Builders + Insights)?** 🚀