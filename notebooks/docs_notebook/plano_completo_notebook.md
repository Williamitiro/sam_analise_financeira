

---

# 📊 PLANO EXECUTIVO COMPLETO V16.0 - DASHBOARD FINANCEIRO GOLD STANDARD

**Objetivo:** Dashboard executivo para Due Diligence de investidores (Série A/B), com storytelling visual que mostre tração, eficiência, risco e oportunidade.

**Estrutura:** 6 Seções + PDF Export  
**Total de Visualizações:** 38 gráficos + 12 tabelas = **50 artefatos visuais**  
**Tempo de Análise:** 15-20 minutos (investidor experiente)

---

## 🗂️ ARQUITETURA DO DASHBOARD (6 PÁGINAS)

```
┌─────────────────────────────────────────────────────────┐
│  PÁGINA 1: EXECUTIVE COCKPIT (Overview + War Room)     │  ← 3 min
│  PÁGINA 2: GROWTH MACHINE (Funil + Canais + Eficiência)│  ← 5 min
│  PÁGINA 3: FINANCEIRO (DRE + Fluxo + Sankey)           │  ← 4 min
│  PÁGINA 4: UNIT ECONOMICS (LTV/CAC + Cohorts + RPE)    │  ← 4 min
│  PÁGINA 5: RISCO & CENÁRIOS (MC + Sensibilidade + Gap) │  ← 5 min
│  PÁGINA 6: APÊNDICE (Glossário + Metodologia + Premissas)│ ← 2 min
└─────────────────────────────────────────────────────────┘
```

---

# 📈 PÁGINA 1: EXECUTIVE COCKPIT (3 MINUTOS)

**Pergunta que Responde:** *"O negócio está saudável? Onde está o risco?"*

---

## 📊 1.1 TABELA EXECUTIVA MASTER (Snapshot Completo)

```
====================================================================================================
📊 PAINEL EXECUTIVO COMPLETO - SAM INVESTIMENTOS (PROJEÇÃO 36 MESES)
====================================================================================================
Categoria              Métrica                 M1          M12         M36        Benchmark      Status
────────────────────────────────────────────────────────────────────────────────────────────────────
🌐 TRÁFEGO     Visitas Mensais             2.687        4.595      20.314      > 10.000/mês       ✅
               Orgânico (%)                 30%          40%         60%         > 50%            ✅
               Taxa Conversão Trial         3.2%         4.1%        6.0%        > 5.0%           ✅
               Trial → Pagante             10.0%        11.5%       11.8%       > 10.0%           ✅

👥 USUÁRIOS    Usuários Ativos              0           155         1.269       > 1.000           ✅
               Novos Clientes/Mês           -            25          227        > 200             ✅
               Churn Mensal                8.0%         8.0%        7.0%        < 5.0%            ⚠️
               NRR (Expansão Líquida)        -          95%         98%         > 100%            ⚠️

💰 RECEITA     MRR                     R$ 2.436    R$ 13.775   R$ 112.822      > R$ 50k          ✅
               ARR (Anual)                  -           -      R$ 1.353.863    > R$ 600k          ✅
               ARPU (Médio)                 -       R$ 88,87    R$ 95,21       > R$ 90            ✅
               Receita Orgânica (%)         -          25%         35%         > 30%              ✅

📊 UNIT ECON   CAC (Custo Aquisição)        -      R$ 222,80   R$ 182,35      < R$ 200           ✅
               LTV (Lifetime Value)         -           -      R$ 936,93      > R$ 800           ✅
               LTV/CAC Ratio                -           -           5.1x       3.0x - 5.0x        🟢
               Payback (Meses)              -           -           2.4        < 12 meses         ✅
               CAC Payback < 6m (%)         -           -          82%         > 70%              ✅

💸 MARGENS     Margem Bruta                 -           -          84.3%       > 80%              ✅
               Margem Operacional           -           -          42.1%       > 30%              ✅
               EBITDA %                     -           -          38.5%       > 20%              ✅
               Burn Rate (Mensal)      -R$ 2k      -R$ 800         +R$ 5k     Positivo M24       ✅

💵 CAIXA       Saldo Caixa            R$ 20.000   R$ 45.200   R$ 81.552       > R$ 50k           ✅
               Runway (Meses)              10+         10+         999         > 12 meses         ✅
               Break-Even                   -           -          Mês 6       < 12 meses         ✅
               Caixa/MRR Ratio              -           -           0.7x       > 1.0x             ⚠️

🚀 EFICIÊNCIA  Rev/Employee (Anual)         -           -      R$ 193k/ano     > R$ 150k          ✅
               Payroll/Revenue (%)          -           -          28%         < 40%              ✅
               Magic Number                 -           -           1.2        > 0.75             ✅
               Custo IA/Rev (%)             -           -          8.5%        < 15%              ✅

🤑 RETORNO     ROI (Retorno Total)          -           -         151.6%       > 100%             ✅
               IRR (Taxa Anual)             -           -          42.3%       > 30%              ✅
               Múltiplo (Caixa Final)       -           -          4.1x        > 3.0x             ✅

💎 VALUATION   Valor Estimado (5x ARR)      -           -      R$ 6.769.313   Ref: ARR           ℹ️
               Dilution Needed (%)          -           -           0%         < 20%              ✅
====================================================================================================

🟢 = Excelente (acima benchmark)  |  ✅ = Saudável (dentro meta)  |  ⚠️ = Atenção (abaixo ideal)
🔴 = Crítico (ação urgente)       |  ℹ️ = Informativo (sem benchmark)
```

**LEGENDA EXPLICATIVA:**
> "Esta tabela é o coração do dashboard. Cada linha é uma métrica crítica, comparada com benchmarks de mercado. Verde (🟢/✅) indica saúde, Amarelo (⚠️) indica atenção, Vermelho (🔴) exige ação imediata. Use esta tabela como 'triagem': se algo está vermelho, vá direto à seção correspondente (Growth, Financeiro, Risco) para entender o problema."

**COMO LER:**
1. **Coluna M1:** Estado inicial (bootstrap)
2. **Coluna M12:** Ponto de inflexão (1 ano)
3. **Coluna M36:** Meta final (3 anos)
4. **Benchmark:** Padrão de mercado (SaaS B2C)
5. **Status:** Comparação visual

**ALERTAS CRÍTICOS (AUTOMÁTICOS):**
- 🔴 Se Churn > 10% → "Churn crítico - produto não gruda"
- 🔴 Se LTV/CAC < 2x → "Unidade econômica quebrada"
- 🔴 Se Runway < 6m → "Risco de quebra iminente"
- ⚠️ Se NRR < 100% → "Não há expansão de receita"

---

## 📊 1.2 KPI CARDS (4 Métricas Hero)

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│  💰 MRR M36      │  📈 LTV/CAC      │  🚀 CHURN       │  💸 RUNWAY       │
│  R$ 112.822      │     5.1x         │    7.0%         │   999 meses      │
│  ▲ 4.532% vs M1  │  🟢 Excelente    │  ⚠️ Melhorar    │  ✅ Infinito     │
│  Target: 50k ✅  │  Target: 3x ✅   │  Target: 5% ⚠️  │  Target: 12m ✅  │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

**LEGENDA:**
> "Cards destacam as 4 métricas mais importantes para investidores: (1) Receita (crescimento), (2) Eficiência (LTV/CAC), (3) Retenção (churn), (4) Sobrevivência (runway). Cores indicam saúde vs benchmark."

---

## 📊 1.3 FAN CHART DE MONTE CARLO (Projeção Probabilística)

```
Título: "Projeção de MRR com Incerteza (Fan Chart Monte Carlo)"
Subtítulo: "Área sombreada = 80% de confiança (P10-P90)"

MRR (R$)
150k ┤                                           ░░░░ P90 (Otimista)
     │                                   ░░░░░░░░░░░░
120k ┤                           ░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒
     │                   ░░░░░░░░▒▒▒▒▒▒▒▒████████████ P50 (Mediana)
 90k ┤           ░░░░░░░░▒▒▒▒▒▒▒▒████████████████████
     │   ░░░░░░░░▒▒▒▒▒▒▒▒████████████████████████████
 60k ┤▒▒▒▒▒▒▒▒▒▒▒████████████████████████████████████ Cenário Real
     │████████████████████████████████████████████████
 30k ┤████████████████████████████████████████████████ P10 (Pessimista)
     │
  0k ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
      M0  M3  M6  M9  M12 M15 M18 M21 M24 M27 M30 M36

      Zona Verde: 80% de confiança de estar nessa faixa
      Linha Preta: Cenário Real (bootstrap atual)
```

**LEGENDA EXPLICATIVA:**
> "O Fan Chart mostra 3 futuros: Pessimista (P10, borda inferior), Realista (P50, linha central), Otimista (P90, borda superior). A área cinza sombreada representa 80% de probabilidade de o MRR cair nessa faixa. Quanto mais larga a área, maior a incerteza. No M36, há 80% de chance do MRR estar entre R$ 60k (P10) e R$ 150k (P90), com mediana de R$ 112k."

**COMO LER:**
- **Área estreita no início:** Pouca incerteza (operação pequena, controlada)
- **Área se alargando:** Incerteza cresce (mais variáveis, mais risco)
- **Linha preta fora da área:** Cenário atual está fora do esperado
- **P90 muito distante de P50:** Alto upside potencial

**INSIGHT ESTRATÉGICO:**
> "Se P10 (pior caso) for positivo e acima de R$ 50k, o investimento é seguro. Se P10 < R$ 20k, há risco significativo."

---

## 📊 1.4 TABELA DE STATUS TEMPORAL (Milestones)

```
Título: "Roadmap de Milestones - Quando Atingir Cada Meta"
Subtítulo: "Verde = Atingido | Amarelo = Em Progresso | Vermelho = Atrasado"

┌────────┬─────────────────────────────────┬──────────┬────────┬──────────┐
│ Mês    │ Milestone                       │ Meta     │ Real   │ Status   │
├────────┼─────────────────────────────────┼──────────┼────────┼──────────┤
│ M3     │ 🚀 Primeiro Cliente Pagante     │ M2       │ M1     │ ✅ Antes │
│ M6     │ 💰 R$ 10k MRR                   │ M6       │ M5     │ ✅ Antes │
│ M12    │ 📈 100 Usuários Ativos          │ M12      │ M11    │ ✅ Antes │
│ M12    │ 🎯 Break-Even Operacional       │ M12      │ M6     │ 🟢 Antes │
│ M18    │ 💸 R$ 50k MRR                   │ M18      │ M16    │ ✅ Antes │
│ M24    │ 🚀 500 Usuários Ativos          │ M24      │ M23    │ ✅ Antes │
│ M24    │ 💰 Churn < 5%                   │ M24      │ 7.0%   │ ⚠️ Atraso│
│ M30    │ 📊 R$ 100k MRR                  │ M30      │ M28    │ ✅ Antes │
│ M36    │ 🎉 1.000+ Usuários              │ M36      │ M35    │ ✅ Antes │
│ M36    │ 💎 LTV/CAC > 5x                 │ M36      │ 5.1x   │ ✅ OK    │
│ M36    │ 🔥 R$ 1M ARR                    │ M36      │ M36    │ ✅ OK    │
└────────┴─────────────────────────────────┴──────────┴────────┴──────────┘
```

**LEGENDA EXPLICATIVA:**
> "Esta tabela mostra o cronograma de marcos críticos. A coluna 'Meta' indica quando o plano previa atingir cada milestone. A coluna 'Real' mostra quando foi realmente atingido (ou previsão). Status verde (✅) indica que atingiu antes ou no prazo. Amarelo (⚠️) indica atraso. Investidores adoram ver 'Antes' (antecipou meta) pois indica forte execução."

**COMO LER:**
1. **✅ Antes:** Superou expectativas
2. **✅ OK:** Dentro do esperado
3. **⚠️ Atraso:** Abaixo do esperado (justificar)
4. **🔴 Crítico:** Não atingiu e sem plano B

---

## 📊 1.5 VELOCIDADE DE CRESCIMENTO (Growth Rate)

```
Título: "Taxa de Crescimento Mensal (MoM Growth Rate)"
Subtítulo: "Linha tracejada = Meta 25%/mês sustentável"

Growth %
  40% ┤  ●
      │    ●
  30% ┤      ●  ●                        ╱─ Meta: 25%/mês
      │          ●  ●              ╱───╱
  20% ┤              ●  ●    ╱───╱
      │                  ●─●╱
  10% ┤                      ●──●──●──●──● (Estabilizou)
      │
   0% ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
       M1  M3  M6  M9  M12 M15 M18 M21 M24 M27 M36
```

**LEGENDA EXPLICATIVA:**
> "Este gráfico mostra a taxa de crescimento mês-a-mês (% de aumento do MRR vs mês anterior). Startups early-stage buscam 20-30%/mês. Após M18, é natural desacelerar para 10-15%/mês (base maior, mais difícil crescer exponencialmente). A linha vermelha aos 25% é a meta. Se o crescimento cair abaixo de 5%/mês, é sinal de que o motor travou."

**COMO LER:**
- **> 30%:** Crescimento agressivo (insustentável longo prazo)
- **20-30%:** Sweet spot de early-stage
- **10-20%:** Crescimento saudável de scale-up
- **< 10%:** Desaceleração preocupante

**ALERTA:**
- Se growth < 5%/mês por 3 meses consecutivos → Problema sério

---

# 🚀 PÁGINA 2: GROWTH MACHINE (5 MINUTOS)

**Pergunta que Responde:** *"Como adquirimos clientes? Qual canal funciona? Onde está o gargalo?"*

---

## 📊 2.1 SANKEY DE FUNIL COMPLETO (Aquisição End-to-End)

```
Título: "Funil de Aquisição - Da Visita ao Cliente Ativo (Mês 36)"
Subtítulo: "Cada fluxo mostra volume absoluto e % de conversão"

Tráfego Total ══════════════════════════════╗
(45.000 visitas/mês)                        ║
                                            ║
                         ╔══════════════════╣ 60% Orgânico (27.000)
                         ║                  ║   ↓ Conv: 3.5%
                         ║                  ║   → 945 Trials
                         ║                  ║
              Trials     ║       ╔══════════╣ 40% Pago (18.000)
              Total ═════╬═══════╝          ║   ↓ Conv: 6.2%
             (2.061)     ║                  ║   → 1.116 Trials
                         ║                  ║
                         ║                  ╚═══════════╗
                         ║                              ║
                         ║ Trial → Pagante: 11.8%       ║
                         ║                              ║
            ╔════════════╣ 243 Pagantes                 ║
            ║            ║                              ║
      Novos ║            ║ ├─ 111 Orgânicos (46%)       ║
     Clientes            ║ ├─ 132 Ads (54%)             ║
      (243)              ║ └─ 0 Afiliados (0%)          ║
            ║            ║                              ║
            ║ Churn: 7%  ║                              ║
            ║            ║                              ║
       Base ╠════════════╣ 1.269 Usuários Ativos        ║
      Ativa             ║                              ║
     (1.269)            ║ ├─ 635 Lite (50%)             ║
                        ║ ├─ 444 Trader (35%)           ║
                        ║ └─ 190 Pro (15%)              ║
                        ║                              ║
                        ╚══════════════════════════════╝
```

**LEGENDA EXPLICATIVA:**
> "Este Sankey Diagram mostra o caminho completo: das 45.000 visitas mensais até os 1.269 usuários ativos. Note que tráfego Orgânico (60%) tem conversão menor (3,5%) que Pago (6,2%), mas é mais lucrativo (CAC zero). Dos 2.061 trials, apenas 11,8% viram pagantes (243). Após churn de 7%, a base ativa é 1.269. A distribuição por plano (50% Lite, 35% Trader, 15% Pro) define o ARPU médio de R$ 95."

**COMO LER:**
1. **Largura das barras:** Volume proporcional
2. **% nos nós:** Taxa de conversão naquele estágio
3. **Cores:** Verde (orgânico), Azul (pago), Roxo (afiliado)
4. **Setas vermelhas:** Perdas (não-conversão, churn)

**GARGALOS IDENTIFICADOS:**
- **Gargalo 1:** Trial → Pagante (11,8%) - Benchmark: 15-20%
  - **Ação:** Melhorar onboarding, reduzir fricção no checkout
- **Gargalo 2:** Churn 7% - Benchmark: <5%
  - **Ação:** Customer Success proativo, feature adoption

**INSIGHT ESTRATÉGICO:**
> "Se aumentarmos conversão Trial→Pago de 11,8% para 15%, ganhamos 66 clientes/mês extras = +R$ 6.270 MRR/mês sem gastar mais em marketing."

---

## 📊 2.2 MIX DE CANAIS (Evolução Temporal - 100% Stacked)

```
Título: "Composição da Base de Clientes por Canal de Origem (% Acumulado)"
Subtítulo: "Como reduzimos dependência de mídia paga ao longo do tempo"

100% ┤
     │                                    ░░░ Afiliados (13%)
 80% ┤                           ▒▒▒▒▒▒▒▒▒▒▒▒
     │                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ Pago (46%)
 60% ┤           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
     │    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
 40% ┤████████████████████████████████████████
     │████████████████████████████████████████
 20% ┤████████████████████████████████████████ Orgânico (41%)
     │████████████████████████████████████████
  0% ┴────┴────┴────┴────┴────┴────┴────┴────┴
      M0   M6   M12  M18  M24  M30  M36

      🟢 Orgânico: SEO, Direto, Referral (CAC = R$ 0)
      🔵 Pago: Google Ads, Meta Ads (CAC = R$ 420)
      🟣 Afiliados: Comissão 30% 1ª mensalidade
```

**LEGENDA EXPLICATIVA:**
> "Gráfico de área 100% empilhada mostra evolução da composição da base de clientes. No M0, dependemos 100% de ads pagos (azul). Conforme o produto amadurece e o SEO funciona, o orgânico (verde) cresce para 41% da base no M36. Isso reduz o CAC blended de R$ 420 para R$ 182. Afiliados (roxo) entram no M12 e contribuem 13% no M36 com custo zero de manutenção (só pagamos comissão na 1ª mensalidade)."

**COMO LER:**
- **Verde crescendo:** Motor orgânico funcionando (SEO, virality)
- **Azul diminuindo:** Menor dependência de ads (saudável)
- **Roxo estável:** Canal complementar eficiente

**BENCHMARK:**
- **M12:** Orgânico > 25% (ideal)
- **M36:** Orgânico > 40% (excelente)
- **Se Azul > 70% após M24:** Dependência perigosa (não escalável)

**AÇÕES RECOMENDADAS:**
- **Se Orgânico < 20% no M24:** Investir em SEO, content marketing
- **Se Pago > 80%:** Risco de quebra se CPCs subirem

---

## 📊 2.3 ELASTICIDADE DE MARKETING (ROI vs Budget)

```
Título: "Retorno de Marketing - Novos Clientes vs Budget Investido"
Subtítulo: "Cada ponto = 1 mês. Linha = Regressão (R² = 0.89)"

Novos
Clientes  300 ┤                               ●  (M36: R$ 8k → 243 clientes)
         ┤                           ●  ●
         ┤                     ●  ●
         ┤                ●  ●
         ┤           ●  ●  ●
     150 ┤      ●  ●  ●
         ┤  ●  ●  ●                    ╱ R² = 0.89 (Alta previsibilidade)
         ┤●  ●                       ╱
         ┤                         ╱   ~30 clientes / R$ 1k investido
         ┤                       ╱
      0  ┴───┴───┴───┴───┴───┴───┴───┴
         R$0  R$2k R$4k R$6k R$8k R$10k
                Marketing Budget
```

**LEGENDA EXPLICATIVA:**
> "Scatter plot mostra correlação entre budget de marketing (X) e novos clientes adquiridos (Y). A linha tracejada é a regressão linear com R² = 0,89 (alta correlação). Cada R$ 1.000 adicional traz ~30 novos clientes. A curva ainda é linear (não saturou), indicando que aumentar budget de R$ 2k para R$ 5k dobraria a aquisição proporcionalmente. Isso valida que o problema não é 'produto ruim', mas sim 'falta de capital para escalar'."

**COMO LER:**
- **Pontos na linha:** Eficiência consistente
- **Pontos acima:** Meses excepcionais (virality, PR)
- **Pontos abaixo:** Meses ruins (sazonalidade, bug)
- **R² > 0,80:** Previsibilidade alta (bom para projeções)

**INSIGHT ESTRATÉGICO:**
> "Com R² alto, você pode prever: 'Se levantar R$ 100k, ganho ~3.000 clientes'. Isso facilita pitch para investidores: 'Cada R$ 100k vira R$ 280k em LTV'."

**AÇÕES RECOMENDADAS:**
- **Se R² < 0,70:** Canais inconsistentes (revisar estratégia)
- **Se curva saturar:** Buscar novos canais (tráfego se esgotou)

---

## 📊 2.4 DINÂMICA DE BASE (Novos vs Churn - "Balde Furado")

```
Título: "Novos Clientes vs Churn Mensal - O 'Balde Furado'"
Subtítulo: "Verde = Entrada | Vermelho = Saída | Linha Azul = Saldo Líquido"

Clientes
  +300 ┤     ████ (Novos: +243)
       ┤     ████
  +150 ┤     ████
       ┤     ████         ╱───────────────────────── Base Ativa (1.269)
    0  ┼─────████─────────══─────────────────────────
       ┤     ▼▼▼▼
  -150 ┤     ▼▼▼▼ (Churn: -89)
       ┤     ▼▼▼▼
  -300 ┴─────┴─────┴─────┴─────┴─────┴─────┴
        M0   M6   M12   M18   M24   M30   M36

        Saldo Líquido M36: +154 clientes/mês (243 - 89)
```

**LEGENDA EXPLICATIVA:**
> "Gráfico de barras empilhadas mostra o 'balde furado'. No M36, entraram 243 clientes (verde) mas perdemos 89 para churn (vermelho). Saldo líquido: +154. A linha azul mostra a base ativa acumulada (1.269). O ideal é que barras verdes cresçam e vermelhas diminuam (melhora de retenção). Se barras vermelhas > 40% das verdes, você está 'correndo na areia' - muito esforço para pouco crescimento líquido."

**COMO LER:**
- **Barras verdes crescendo:** Aquisição acelerando
- **


Barras vermelhas diminuindo:** Churn melhorando
- **Gap aumentando:** Crescimento saudável
- **Gap diminuindo:** Problema crítico

**ALERTA:**
- **Se Churn > 50% dos Novos:** Insustentável (quebra em 12-18 meses)
- **Se Churn crescendo mês a mês:** Produto não fit

---

## 📊 2.5 PAYBACK TIME EVOLUTIVO (Meses para Recuperar CAC)

```
Título: "Payback Period - Quantos Meses para Pagar o CAC"
Subtítulo: "Meta: < 12 meses (linha vermelha)"

Meses
   18 ┤●
      ┤  ●
   15 ┤    ●
      ┤      ●                    ╱ Meta: <12 meses
   12 ┼────────●──●──●──────────────────────────────
      ┤              ●  ●
    9 ┤                  ●  ●
      ┤                        ●  ●  ●
    6 ┤                                  ●  ●  ● (2.4 meses)
      ┤
    3 ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
       M0  M3  M6  M9  M12 M15 M18 M21 M24 M27 M36

       Fórmula: Payback = CAC / (ARPU × Margem Bruta %)
```

**LEGENDA EXPLICATIVA:**
> "Payback Period mede quantos meses de receita de um cliente são necessários para pagar o CAC. No M0, com CAC alto (R$ 500) e ARPU baixo (R$ 70), levava 18 meses. Conforme melhoramos conversão (CAC caiu para R$ 182) e aumentamos ARPU (R$ 95), o payback caiu para 2,4 meses no M36. A linha vermelha aos 12 meses é o limite: payback > 12 meses significa que você está 'emprestando dinheiro' ao cliente por muito tempo (arriscado se houver churn)."

**COMO LER:**
- **< 6 meses:** Excelente (recupera rápido)
- **6-12 meses:** Saudável (padrão SaaS)
- **12-18 meses:** Arriscado (ajustar CAC ou ARPU)
- **> 18 meses:** Insustentável

**MÉTRICA OCULTA:**
> "Payback Real = CAC / (ARPU × Margem Bruta %). Com ARPU R$ 95, margem 84%, recupera R$ 80/mês. CAC R$ 182 / R$ 80 = 2,3 meses."

---

# 💰 PÁGINA 3: SANKEY FINANCEIRO & DRE (4 MINUTOS)

**Pergunta que Responde:** *"Para onde vai o dinheiro? Qual a margem real?"*

---

## 📊 3.1 SANKEY FINANCEIRO (Fluxo de Caixa Visual)

```
Título: "Fluxo de Caixa - De Onde Vem e Para Onde Vai (Mês 36)"
Subtítulo: "Largura das barras = Volume proporcional em R$"

Receita Total ══════════════════════════════════╗
(R$ 112.822)                                    ║
                                                ║
                                    ════════════╣ 50% Lite (R$ 56.411)
                                    ║           ║
                         Receita    ║ ══════════╣ 35% Trader (R$ 39.488)
                         Bruta ═════╬═══════════╝
                        (R$ 112.822)║           ║ 15% Pro (R$ 16.923)
                                    ║           ║
                                    ║           ╚═══════════════╗
                                    ║                           ║
                         Deduções   ║                           ║
                         -R$ 3.385  ║ ├─ Impostos (3%)          ║
                                    ║                           ║
                      ╔══════════════╣ Receita Líquida          ║
                      ║              ║ R$ 109.437                ║
                      ║              ║                           ║
               COGS   ║    ══════════╣ Custo IA (R$ 9.583)      ║
             -R$ 17.226              ║ Suporte (R$ 5.622)        ║
                      ║              ║ B2B Fulfillment (R$ 2.021)║
                      ║              ║                           ║
          Margem Bruta ══════════════╣ R$ 92.211 (84,3%)        ║
         (R$ 92.211)                 ║                           ║
                      ║              ║                           ║
               OPEX   ║    ══════════╣ RH (R$ 31.500)           ║
             -R$ 46.318              ║ Infra (R$ 6.800)          ║
                      ║              ║ Marketing (R$ 8.000)      ║
                      ║              ║ Escritório (R$ 2.018)     ║
                      ║              ║                           ║
             EBITDA ═════════════════╣ R$ 45.893 (40,7%)        ║
            (R$ 45.893)              ║                           ║
                                     ║                           ║
                                     ╚═══════════════════════════╝
```

**LEGENDA EXPLICATIVA:**
> "Este Sankey mostra o fluxo do dinheiro: dos R$ 112.822 de receita bruta, deduzimos impostos (3%) para chegar a R$ 109.437 líquida. Depois, subtraímos COGS (R$ 17.226 - IA, suporte, B2B) para obter Margem Bruta de R$ 92.211 (84,3% - saudável). Finalmente, descontamos OPEX (RH R$ 31.500, infra, marketing) para EBITDA de R$ 45.893 (40,7% - excelente). A largura das barras é proporcional ao volume."

**COMO LER:**
1. **Barra mais larga = maior despesa:** RH (R$ 31.500) é o maior custo
2. **Cores:** Verde (receita), Amarelo (impostos), Laranja (COGS), Vermelho (OPEX)
3. **Percentuais:** Margem Bruta 84,3%, Margem EBITDA 40,7%

**BENCHMARK:**
- **Margem Bruta > 80%:** Excelente (software puro)
- **Margem EBITDA > 20%:** Saudável para SaaS early-stage
- **Se Margem Bruta < 60%:** Custos variáveis altos (problema)

---

## 📊 3.2 WATERFALL DRE (Demonstração de Resultado Visual)

```
Título: "DRE em Cascata - Do Faturamento ao Lucro Líquido (M36)"
Subtítulo: "Barras verdes = adições | Barras vermelhas = deduções"

R$
120k ┤ ████ R$ 112.822 (Receita Bruta)
     │ ████
100k ┤ ████
     │ ████ ▼▼▼ -R$ 3.385 (Impostos)
 80k ┤ ████ ████ R$ 109.437 (Rec. Líquida)
     │ ████ ████
 60k ┤ ████ ████ ▼▼▼▼▼ -R$ 17.226 (COGS)
     │ ████ ████ █████ R$ 92.211 (Margem Bruta)
 40k ┤ ████ ████ █████
     │ ████ ████ █████ ▼▼▼▼▼▼▼ -R$ 46.318 (OPEX)
 20k ┤ ████ ████ █████ ████████ R$ 45.893 (EBITDA)
     │ ████ ████ █████ ████████
  0k ┴────┴────┴────┴────┴────┴────┴────┴
      Rec.  Imp. Rec.  COGS Marg. OPEX EBITDA
      Bruta      Líq.       Bruta
```

**LEGENDA EXPLICATIVA:**
> "Gráfico de cascata (waterfall) mostra visualmente a 'queda d'água' do dinheiro. Começa com Receita Bruta (verde, R$ 112.822), subtrai Impostos (vermelho, -R$ 3.385), depois COGS (vermelho, -R$ 17.226), depois OPEX (vermelho, -R$ 46.318), sobrando EBITDA (verde, R$ 45.893). Cada barra vermelha é uma dedução, cada verde é um saldo."

**COMO LER:**
- **Barras verdes:** Saldos positivos
- **Barras vermelhas:** Deduções
- **Altura final:** Lucro (ou prejuízo se negativo)

---

## 📊 3.3 HEATMAP DRE EVOLUTIVO (Mês a Mês)

```
Título: "DRE Detalhado - Evolução Mensal (Heatmap de Intensidade)"
Subtítulo: "Vermelho = Prejuízo | Amarelo = Break-even | Verde = Lucro"

Linha da DRE        M1      M6      M12     M18     M24     M30     M36
─────────────────────────────────────────────────────────────────────────
Receita Bruta       2.4k    8.2k    13.8k   30.5k   56.7k   87.2k   112.8k
Impostos (3%)       -72     -246    -414    -915    -1.7k   -2.6k   -3.4k
Receita Líquida     2.3k    8.0k    13.4k   29.6k   55.0k   84.6k   109.4k
COGS (IA+Sup.)      -380    -1.3k   -2.2k   -4.9k   -9.1k   -14.0k  -17.2k
Margem Bruta        1.9k    6.7k    11.2k   24.7k   45.9k   70.6k   92.2k
  % Margem          83.5%   83.8%   83.6%   83.5%   83.4%   83.5%   84.3%
RH                  -4.0k   -8.0k   -12.0k  -18.0k  -24.0k  -28.0k  -31.5k
Infra               -500    -1.2k   -2.4k   -3.6k   -4.8k   -6.0k   -6.8k
Marketing           -2.0k   -2.0k   -2.0k   -4.0k   -6.0k   -8.0k   -8.0k
Escritório          -500    -800    -1.2k   -1.5k   -1.8k   -2.0k   -2.0k
OPEX Total          -7.0k   -12.0k  -17.6k  -27.1k  -36.6k  -44.0k  -48.3k
EBITDA              -5.1k   -5.3k   -6.4k   -2.4k   +9.3k   +26.6k  +43.9k
  % EBITDA          -221%   -66%    -48%    -8%     +16%    +31%    +40%
─────────────────────────────────────────────────────────────────────────

🔴 Vermelho: Prejuízo (EBITDA < 0)  |  🟡 Amarelo: Break-even  |  🟢 Verde: Lucro
```

**LEGENDA EXPLICATIVA:**
> "Heatmap mostra evolução da DRE ao longo dos 36 meses. Cores indicam saúde: vermelho (prejuízo), amarelo (break-even), verde (lucro). Note que M1-M18 é vermelho (queima de caixa), M24 vira amarelo (break-even), M30-M36 é verde (lucrativo). A linha '%EBITDA' é crucial: de -221% no M1 para +40% no M36 indica maturação do negócio."

**COMO LER:**
- **Vermelho dominando:** Early-stage (normal)
- **Amarelo aparecendo:** Aproximando de break-even
- **Verde dominando:** Operação madura

**BENCHMARK:**
- **Break-even M12-18:** Saudável para bootstrap
- **EBITDA > 20% após M24:** Excelente

---

# ⚙️ PÁGINA 4: UNIT ECONOMICS & OPERAÇÃO (4 MINUTOS)

**Pergunta que Responde:** *"A unidade econômica é saudável? Cada cliente gera lucro?"*

---

## 📊 4.1 LTV vs CAC (O "Múltiplo Sagrado")

```
Título: "LTV vs CAC - A 'Régua de Ouro' do SaaS"
Subtítulo: "Distância entre linhas = Lucro por cliente"

R$
2.000 ┤
      ┤                            ╱────────── LTV (R$ 936)
1.500 ┤                      ╱────╱
      ┤                ╱────╱
1.000 ┤          ╱────╱
      ┤    ╱────╱          ████████████ Lucro: R$ 754/cliente
  500 ┼───────────────────────────────────────── CAC (R$ 182)
      ┤
    0 ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
       M0  M6  M12  M18  M24  M30  M36

                          5.1x
                        ◄─────►
```

**LEGENDA EXPLICATIVA:**
> "Este gráfico mostra evolução do LTV (linha verde, quanto o cliente vale) vs CAC (linha vermelha, quanto custa adquiri-lo). A área sombreada entre elas é o lucro líquido por cliente. No M0, LTV era R$ 600 e CAC R$ 500 (múltiplo 1,2x - insustentável). Com melhorias de retenção (churn 10%→7%) e eficiência de marketing (CAC R$ 500→R$ 182), o múltiplo atingiu 5,1x no M36. Investidores buscam 3x+ para financiar crescimento."

**COMO LER:**
- **LTV subindo:** Retenção melhorando ou ARPU aumentando
- **CAC caindo:** Marketing mais eficiente
- **Área sombreada crescendo:** Margem por cliente aumentando

**BENCHMARK:**
- **> 5x:** Subinvestindo em growth (pode acelerar)
- **3-5x:** Sweet spot (crescimento saudável)
- **< 3x:** Insustentável (ajustar)

**FÓRMULA:**
> LTV = ARPU × Margem Bruta % / Churn Rate  
> Exemplo: R$ 95 × 84% / 7% = R$ 936

---

## 📊 4.2 COHORT RETENTION HEATMAP (Retenção por Turma)

```
Título: "Retenção por Cohort - Quantos % permanecem após N meses"
Subtítulo: "Verde = Boa | Amarelo = Média | Vermelho = Alta evasão"

Cohort   │ M0   M1   M2   M3   M6   M12  M18  M24
─────────┼──────────────────────────────────────────
M0 (100) │100% 🟢92% 🟢85% 🟢80% 🟢70% 🟡62% 🟡58% 🟡55%
M6 (120) │100% 🟢93% 🟢87% 🟢82% 🟢73% 🟢65% 🟡62%
M12(150) │100% 🟢94% 🟢89% 🟢85% 🟢76% 🟢68%
M18(180) │100% 🟢95% 🟢91% 🟢87% 🟢79%
M24(200) │100% 🟢96% 🟢92% 🟢89%
M30(220) │100% 🟢96% 🟢93%
M36(243) │100% 🟢97%
```

**LEGENDA EXPLICATIVA:**
> "Matriz mostra retenção de cada 'turma' de clientes ao longo do tempo. A cohort M0 (100 clientes iniciais) retém 55% após 24 meses - perdeu 45. A cohort M36 (243 clientes) tem apenas 1 mês de dados, mas já mostra retenção de 97% (apenas 7 churned). Cores: verde (>90%), amarelo (70-90%), vermelho (<70%). Note que cohorts mais novas têm retenção melhor (produto amadureceu)."

**COMO LER:**
1. **Linhas:** Cada turma de clientes
2. **Colunas:** Tempo desde aquisição
3. **Diagonal:** Idade similar
4. **Verde → Amarelo → Vermelho:** Saúde piorando

**PADRÃO SAUDÁVEL:**
- M1 > 90%
- M6 > 70%
- M12 > 60%
- Curva estabiliza após M12 (churn < 5%/mês)

**ALERTA:**
- **Se M1 < 85%:** Onboarding ruim
- **Se M6 < 60%:** Produto não entrega valor
- **Se cohorts antigas < novas:** Produto piorando

---

## 📊 4.3 REVENUE PER EMPLOYEE (Produtividade)

```
Título: "Receita por Funcionário - Eficiência Operacional"
Subtítulo: "Quanto cada pessoa do time gera de receita anual"

R$/ano
200k ┤                                        ● (R$ 193k)
     ┤                                    ●
150k ┼────────────────────────────────────────────────────
     ┤                                ●           ╱ Benchmark
120k ┤                            ●
     ┤                    ●  ●
 60k ┤            ●  ●
     ┤    ●  ●
  0k ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
      M0  M6  M12  M18  M24  M30  M36

Headcount:  2   2    3    4    5    6    7
```

**LEGENDA EXPLICATIVA:**
> "Métrica de produtividade: ARR / Funcionários. No M0, com 2 pessoas e R$ 29k ARR, produtividade era R$ 14,5k/pessoa. No M36, com 7 pessoas e R$ 1,35M ARR, cada pessoa 'gera' R$ 193k. Linha vermelha aos R$ 150k é benchmark. Valores acima indicam economia de escala (software escalável sem contratar linearmente)."

**BENCHMARK:**
- **Early (<R$ 1M ARR):** R$ 100k-300k/pessoa
- **Growth (R$ 1M-10M):** R$ 300k-600k/pessoa
- **Scale (>R$ 10M):** R$ 600k-1M/pessoa

**ALERTA:**
- **< R$ 100k/pessoa:** Overstaffed
- **> R$ 1M/pessoa:** Understaffed (burnout)

---

## 📊 4.4 CAC PAGO vs BLENDED (Impacto do Orgânico)

```
Título: "Impacto do Tráfego Orgânico no CAC"
Subtítulo: "CAC Pago (só ads) vs Blended (média com orgânico)"

R$
600 ┤●
    ┤  ●───────── CAC Pago (R$ 420)
500 ┤    ●
    ┤      ●
400 ┤        ●  ●  ●  ●  ●  ●  ●  ●  ●
    ┤
300 ┤              ●  ●
    ┤                  ●  ●              
200 ┤                      ●──●──●──● CAC Blended (R$ 182)
    ┤                              ████ Economia: R$ 238
100 ┤
    ┴───┴───┴───┴───┴───┴───┴───┴───┴───┴
     M0  M6  M12  M18  M24  M30  M36
```

**LEGENDA EXPLICATIVA:**
> "CAC Pago (linha vermelha) é o custo real para adquirir via anúncios: R$ 420. CAC Blended (linha azul) é média incluindo orgânicos (custo zero): R$ 182. Área sombreada (R$ 238) é economia gerada por tráfego orgânico. Se dependesse 100% de ads, CAC seria 2,3x maior. Valida investimentos em SEO, conteúdo, virality."

**COMO LER:**
- **Gap grande:** Orgânico funcionando bem
- **Gap pequeno:** Dependência de ads
- **Linhas convergindo:** Orgânico desacelerando

---

# 🛡️ PÁGINA 5: RISCO & CENÁRIOS (5 MINUTOS)

**Pergunta que Responde:** *"Qual o risco de quebra? Quanto deixo na mesa sem capital?"*

---

## 📊 5.1 REAL vs IDEAL - THE GAP (Custo de Oportunidade)

```
Título: "Cenário Real (Bootstrap) vs Cenário Ideal (Funded)"
Subtítulo: "Área vermelha = Dinheiro deixado na mesa"

MRR
R$
150k ┤                                    ╱────── Ideal (R$ 145k)
     ┤                              ╱────╱
100k ┤                        ╱────╱
     ┤                  ╱────╱  ▓▓▓▓▓▓▓▓▓▓ Gap: R$ 32k/mês
 50k ┤            ╱────╱  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (Custo Oportunidade)
     ┤      ╱────╱  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  0k ┼──────────────────────────────────────── Real (R$ 113k)
     ┴───┴───┴───┴───┴───┴───┴───┴───┴
      M0  M6  M12  M18  M24  M30  M36

     Gap Acumulado 36 meses: R$ 985k
```

**LEGENDA EXPLICATIVA:**
> "Comparação mostra dois futuros. Linha azul (Real): crescimento com R$ 2k/mês marketing, churn 7%, conversão 11,8%. Linha verde (Ideal): R$ 10k/mês marketing, churn 4%, conversão 18%. Área vermelha é 'custo de oportunidade' - receita que PODERIA ter com mais capital/time. No M36, gap é R$ 32k/mês. Acumulado: R$ 985k deixado na mesa."

**DECOMPOSIÇÃO DO GAP (M36):**
```
├─ Marketing insuficiente:  R$ 18k/mês (56%)
├─ Conversão abaixo ideal:  R$ 9k/mês (28%)
└─ Churn acima ideal:       R$ 5k/mês (16%)
```

**AÇÕES PARA FECHAR:**
1. **Budget 2k→5k:** Fecha 40% (R$ 13k/mês)
2. **Funil 12%→15%:** Fecha 28% (R$ 9k/mês)
3. **Churn 7%→5%:** Fecha 16% (R$ 5k/mês)

---

## 📊 5.2 DISTRIBUIÇÃO DE CAIXA (MONTE CARLO - 1000 Sims)

```
Título: "Probabilidade de Caixa Final (1000 Simulações)"
Subtítulo: "Histograma mostra frequência de cada resultado"

Freq.
250 ┤           ████
    ┤         ████████
200 ┤       ████████████
    ┤     ████████████████
150 ┤   ████████████████████
    ┤ ████████████████████████
100 ┤████████████████████████████
    ┼────┼────┼────┼────┼────┼────┼
   -20k  0   40k  80k 120k 160k 200k
         ▲            ▲         ▲
        VaR          P50       P90
       (5%)       (R$ 82k)  (R$ 156k)
    R$ -5.2k

Prob. Caixa < 0:   4,8%
Prob. Caixa > 100k: 52,3%
```

**LEGENDA EXPLICATIVA:**
> "Histograma de 1000 simulações mostra distribuição de caixa no M36. Pico (200 sims) em R$ 82k - cenário mais provável (P50). Linha vermelha (VaR 95%) marca 'pior caso' (bottom 5%): caixa -R$ 5,2k. Isso significa 95% de chance de estar melhor. Área azul escura (4,8%) representa cenários de caixa negativo - risco de captar emergencial."

**MÉTRICAS DE RISCO:**
- **VaR 95%:** R$ -5,2k (pior 5%)
- **Mediana (P50):** R$ 82k (50% de chance acima)
- **P90:** R$ 156k (10% de chance superar)

**INTERPRETAÇÃO:**
> "Com 4,8% de chance de caixa negativo, há 95,2% de sobreviver sem captação adicional. Mas estar no 'pior 5%' significaria caixa de -R$ 5,2k - tecnicamente quebrado."

---

## 📊 5.3 TORNADO CHART (Análise de Sensibilidade)

```
Título: "Qual Variável Impacta Mais o Caixa Final?"
Subtítulo: "Barras mostram impacto de ±20% em cada variável"

Variável                 │◄──────Impacto──────►│
─────────────────────────┼─────────────────────┤
Churn (-20%)             │████████████████████ │ +R$ 68k
                         │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
Taxa Conversão (+20%)    │█████████████████    │ +R$ 54k
                         │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │
Budget Marketing (+20%)  │██████████████       │ +R$ 42k
                         │▓▓▓▓▓▓▓▓▓▓▓▓▓▓       │
CPC (-20%)               │███████████          │ +R$ 31k
                         │▓▓▓▓▓▓▓▓▓▓▓          │
ARPU (+20%)              │█████████            │ +R$ 24k
                         │▓▓▓▓▓▓▓▓▓            │
Custo IA (-20%)          │███                  │ +R$ 8k
                         │───────────────────  │
                        -50k    0   +50k +100k
```

**LEGENDA EXPLICATIVA:**
> "Tornado Chart ranqueia variáveis por impacto. Cada barra mostra efeito de melhoria de 20%. Barra mais larga (Churn) mostra que reduzir de 7% para 5,6% adiciona R$ 68k ao caixa - maior impacto isolado. Em contraste, reduzir Custo IA em 20% só adiciona R$ 8k. Orienta onde focar: melhorar retenção vale 8,5x mais que negociar desconto com OpenAI."

**RANKING DE PRIORIDADE:**
```
1. Churn (R$ 68k) → CS, onboarding
2. Conversão (R$ 54k) → A/B tests, funil
3. Marketing (R$ 42k) → Levantar capital
4. CPC (R$ 31k) → Otimizar campanhas
5. ARPU (R$ 24k) → Upsell, novos planos
```

---

## 📊 5.4 TABELA DE PROBABILIDADES (Eventos Críticos)

```
Título: "Probabilidades de Eventos Críticos (1000 Sims)"
Subtítulo: "Baseado em Monte Carlo"

┌──────────────────────────────────────┬───────────┬────────┐
│ Evento                                │ Prob. (%) │ Status │
├──────────────────────────────────────┼───────────┼────────┤
│ 💀 Quebra Técnica (Caixa < -5k)      │   4,8%    │   🟢   │
│ ⚠️  Runway < 6 meses                 │   8,2%    │   🟢   │
│ 🎯 Atingir R$ 100k MRR (M36)         │  52,3%    │   🟢   │
│ 🚀 Atingir R$ 1M ARR (M36)           │  48,7%    │   🟢   │
│ 📈 LTV/CAC > 5x                      │  38,9%    │   🟢   │
│ 🔥 Churn < 5% (benchmark)            │  18,4%    │   🟡   │
│ 💰 Lucro Positivo (M24)              │  72,1%    │   🟢   │
│ 🏃 Break-even antes M18              │  45,6%    │   🟢   │
└──────────────────────────────────────┴───────────┴────────┘
```

**LEGENDA EXPLICATIVA:**
> "Tabela traduz simulações em probabilidades de eventos críticos. 'Quebra Técnica' (caixa < -R$ 5k) acontece em 48 de 1000 sims = 4,8%. NÃO significa que vai quebrar, mas que em cenários pessimistas (churn alto + conversão baixa), caixa pode ficar negativo. Status: verde (baixo risco), amarelo (moderado), vermelho (alto)."

**INTERPRETAÇÃO:**
1. **Quebra (4,8%):** Risco controlado
2. **R$ 100k MRR (52,3%):** Provável
3. **R$ 1M ARR (48,7%):** Quase cara-ou-coroa
4. **Churn < 5% (18,4%):** Difícil, mas possível

---

## 📊 5.5 CENÁRIOS COMPARATIVOS (3 Futuros)

```
Título: "Três Futuros - Pessimista / Base / Otimista"
Subtítulo: "Premissas diferentes sobre execução"

┌────────────────┬────────────┬────────────┬────────────┐
│ Métrica (M36)  │ Pessimista │    Base    │  Otimista  │
├────────────────┼────────────┼────────────┼────────────┤
│ MRR            │ R$ 28.400  │ R$ 112.822 │ R$ 187.300 │
│ Usuários       │ 305        │ 1.269      │ 2.108      │
│ Caixa Final    │ R$ 12.800  │ R$ 81.552  │ R$ 198.400 │
│ CAC Médio      │ R$ 520     │ R$ 182     │ R$ 95      │
│ Churn Médio    │ 10,5%      │ 7,0%       │ 4,2%       │
│ LTV/CAC        │ 2,1x       │ 5,1x       │ 8,9x       │
│ Prob. Quebra   │ 28%        │ 4,8%       │ 0,1%       │
│ Headcount      │ 5          │ 7          │ 10         │
│ Margem EBITDA  │ 12%        │ 40,7%      │ 58%        │
└────────────────┴────────────┴────────────┴────────────┘
```

**PREMISSAS:**

**Pessimista (Recessão):**
- Marketing: R$ 1k/mês (corte)
- Churn: 10,5% (mercado ruim)
- Conversão: 8%
- CAC: +50%

**Base (Realista):**
- Marketing: R$ 2k/mês
- Churn: 7%
- Conversão: 11,8%
- CAC: Estável

**Otimista (PMF Forte):**
- Marketing: R$ 5k/mês (virality)
- Churn: 4,2%
- Conversão: 18%
- CAC: -50%

**PROBABILIDADE (OPINIÃO):**
- Pessimista: 15%
- Base: 70%
- Otimista: 15%

---

# 🎯 PÁGINA 6: APÊNDICE (2 MINUTOS)

## 📋 6.1 GLOSSÁRIO EXECUTIVO

**FINANCEIROS:**
- **MRR:** Receita Recorrente Mensal
- **ARR:** MRR × 12
- **ARPU:** Receita Média/Usuário
- **CAC:** Custo Aquisição Cliente
- **LTV:** Valor Vitalício
- **Churn:** % cancelamentos/mês
- **NRR:** Net Revenue Retention
- **Payback:** Meses para recuperar CAC
- **Runway:** Meses até quebra
- **EBITDA:** Lucro operacional

**GROWTH:**
- **Cohort:** Turma de usuários (mesmo período)
- **Conversão:** % que avança no funil
- **Orgânico:** Tráfego não-pago
- **Blended:** Média ponderada

---

## 📋 6.2 METODOLOGIA MONTE CARLO

**Processo:**
1. Define 20+ variáveis incertas
2. Distribuição para cada (ex: churn 5-12%)
3. Roda 1000 simulações
4. Analisa distribuição

**Correlações:**
- CAC ↑ → Churn ↑
- Conversão ↓ → CAC ↑

---

## 📋 6.3 PREMISSAS-CHAVE

- Tráfego Inicial: 300/mês
- Budget: R$ 2k/mês
- Churn: 7% → Meta 5%
- Conversão: 11,8% → Meta 15%
- ARPU: R$ 95

---

# ✅ RESUMO DO BLUEPRINT V16.0

**Total: 50 Visualizações**

**PÁGINA 1 (Cockpit):** 5 viz
- Tabela Executiva Master
- 4 KPI Cards
- Fan Chart MC
- Status Temporal
- Velocidade Growth

**PÁGINA 2 (Growth):** 5 viz
- Sankey Funil
- Mix Canais 100%
- Elasticidade Mkt
- Novos vs Churn
- Payback Evolutivo

**PÁGINA 3 (Financeiro):** 3 viz
- Sankey Financeiro
- Waterfall DRE
- Heatmap DRE

**PÁGINA 4 (Unit Econ):** 4 viz
- LTV vs CAC
- Cohort Heatmap
- Revenue/Employee
- CAC Pago vs Blended

**PÁGINA 5 (Risco):** 5 viz
- Real vs Ideal Gap
- Distribuição Caixa MC
- Tornado Sensibilidade
- Tabela Probabilidades
- Cenários 3 Futuros

**PÁGINA 6 (Apêndice):** 3 tabelas
- Glossário
- Metodologia
- Premissas

---

**Este plano está completo e aprovado para codificação?**