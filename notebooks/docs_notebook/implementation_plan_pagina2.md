
---

### 2. A NOVA DIRETRIZ DE CONCEITO GLOBAL (HEURÍSTICA DE PERGUNTAS)

Baseado exatamente no seu texto acima, redigi esta **"Diretriz de Validação de Valor"**. Ela serve para decidir **SE** um gráfico deve existir e **O QUE** ele deve mostrar.

Isso deve ser colado no início de qualquer prompt de criação para garantir que a IA não crie "arte", mas sim "respostas".

---

# 🧠 DIRETRIZES GLOBAIS DE CONCEITO & INTENÇÃO (O TESTE DE VALOR)
**Objetivo:** Eliminar gráficos "descritivos" ou "enfeites". Garantir que cada pixel na tela resolva uma dúvida de negócio do investidor/gestor.

## 1. A LEI DA SUBSTITUIÇÃO (Tabela vs. Gráfico)
Antes de criar qualquer gráfico, aplique este teste:
*   **Teste:** "Eu consigo explicar esse insight com uma frase ou uma linha de tabela?"
    *   **Se SIM:** 🚫 **MATE O GRÁFICO.** Use apenas uma métrica de destaque (Big Number) ou uma linha na tabela.
    *   **Se NÃO:** (Ou seja, preciso ver a tendência, a volatilidade, a correlação ou o desvio visual entre Real vs Ideal). ✅ **FAÇA O GRÁFICO.**
*   **Exemplo Prático:**
    *   *Errado:* Gráfico de Pizza mostrando "55% Homens, 45% Mulheres". (Isso cabe numa tabela).
    *   *Certo:* Gráfico de Linha mostrando que "Mulheres converteram 3x mais que Homens na semana 12 após a mudança do criativo". (Isso exige visualização).

## 2. A ESTRUTURA DE PERGUNTAS (Socrático)
Cada célula do notebook deve ser desenhada para responder a uma **"Pergunta Letal"** específica. Se o gráfico for genérico, ele está reprovado.

### **PARA A PÁGINA DE GROWTH (Growth Engine):**

**Célula 2.1: Eficiência do Funil (Substituindo o antigo)**
*   **Pergunta do Gestor:** "O processo de vendas quebrou com o aumento de volume?"
*   **Dúvida Específica:** "Eu prometi converter 5% de Lead para Pago. No cenário Real, com 10x mais leads, essa taxa se manteve ou caiu?"
*   **O que o gráfico deve mostrar:** Não o volume total, mas o **GAP de Eficiência**. Onde o "Real" ficou abaixo do "Ideal".

**Célula 2.2: Validação Tática (Semanal)**
*   **Pergunta do Gestor:** "Onde exatamente queimamos dinheiro no início?"
*   **Dúvida Específica:** "Nas primeiras 24 semanas, houve algum momento em que o Custo (CAC) explodiu e a gente demorou para perceber?"
*   **O que o gráfico deve mostrar:** A volatilidade semanal. O gráfico deve gritar o erro (semana ruim) para provar que agora sabemos corrigir.

**Célula 2.3: Saturação (Elasticidade)**
*   **Pergunta do Gestor:** "Se eu colocar R$ 1 milhão amanhã, o que acontece?"
*   **Dúvida Específica:** "O canal aguenta ou o CAC vai dobrar? Qual é o teto matemático?"
*   **O que o gráfico deve mostrar:** A curva entortando (saturando). Deve responder "Pare de gastar em R$ X" ou "Acelere até R$ Y".

**Célula 2.4: O Vazamento (Churn)**
*   **Pergunta do Gestor:** "Quanto dinheiro estamos deixando na mesa?"
*   **Dúvida Específica:** "Não me fale em % de churn. Me fale em Reais perdidos. O balde está furado a ponto de inviabilizar o crescimento?"
*   **O que o gráfico deve mostrar:** O impacto financeiro negativo acumulado vs. o esforço de vendas.

---

## 3. O VEREDITO DE STORYTELLING
O conjunto dos gráficos da página deve formar uma frase completa:
> "Nós validamos que o funil aguenta escala **(Graf 2.1)**, corrigimos a volatilidade do custo inicial nas primeiras semanas **(Graf 2.2)**, sabemos exatamente o teto de investimento antes de saturar **(Graf 2.3)** e controlamos o vazamento financeiro do churn **(Graf 2.4)**."

Se os gráficos não contarem essa história conectada, eles estão errados.

---

# 📘 SPEC SHEET: PÁGINA 2 — GROWTH MACHINE (INSTITUTIONAL GRADE)
**Versão Final de Execução** | **Estilo:** Kaszek/Sequoia/a16z
**Output:** Imagem High-DPI (300dpi) ou PDF Vetorial.

---

### 🚨 1. DIRETRIZES GLOBAIS INVIOLÁVEIS (MANDAMENTOS)

1.  **DINAMICIDADE TOTAL:** Zero hardcoded. Tudo calculado em runtime (`df_real_m`, `mc_results`).
2.  **ESCALA LOGARÍTMICA OBRIGATÓRIA (Funil):** O gráfico de funil **DEVE** usar escala logarítmica no eixo X para permitir a visualização proporcional de Visitas (milhares) vs Conversão (unidades).
3.  **TABELAS EXPANDIDAS (7 Snapshots):** Todas as tabelas auxiliares devem mostrar as colunas: M0, M3, M6, M12, M18, M24, M36 (ou último mês disponível).
4.  **ZONAS DE CONTEXTO:** Gráficos de eficiência (Payback, ROI) devem ter **fundo colorido** (Background Spans) indicando zonas de Excelência (Verde), Atenção (Amarelo) e Perigo (Vermelho/Rosa), e não apenas linhas.
5.  **INSIGHTS COM CONFIANÇA:** Todo insight deve ter uma flag de confiança baseada em dados (`High` se R² > 0.9 ou Delta > 20%, `Medium` caso contrário).
6.  **CALLOUTS & ANCORAS:** Anotações devem ser "Ancoradas" em pontos de inflexão reais (ex: mês onde Orgânico cruzou Pago), não aleatórias.
7.  **Estrutura de Cada Bloco Visual:**
    *   **Topo:** Título Coloquial + Subtítulo Técnico.
    *   **Centro:** Gráfico com Anotações "Ancoradas".
    *   **Tabela:** Tabela auxiliar.
    *   **Fundo:** Bloco "Como Ler" + Bloco "Insight" (Dinâmico).

---

## 📊 VIZ 2.1: EVOLUÇÃO DO FUNIL (LOGARÍTMICO)
*Substitui o Sankey por ser matematicamente superior para comparação de escala.*

### 📝 A. Conteúdo Textual
*   **Título (Coloquial):** "Escalando o volume sem destruir a eficiência"
*   **Subtítulo (Técnico):** "Funil de Conversão Comparativo: M6 (Início) vs M36 (Atual) | Escala Logarítmica"

### 📐 B. Especificação do Gráfico (Plotagem)
*   **Tipo:** `Horizontal Bar Chart (Side-by-Side)`
*   **Eixo X:** **ESCALA LOGARÍTMICA (`symlog` ou `log`)**. *Mandatório.*
    *   *Motivo:* Permitir ver `14.000` visitas e `6` vendas no mesmo gráfico sem que a venda vire um pixel invisível.
*   **Eixo Y (Categorias):**
    1.  `Visitas` (Topo)
    2.  `Trials` (Meio)
    3.  `Novos Pagantes` (Fundo)
    4.  `Base Ativa` (Acumulado)
*   **Séries de Dados:**
    *   **Esquerda (M6):** Barras Cinza (`#B0BEC5`).
    *   **Direita (M36):** Barras Coloridas (Visitas=Cinza, Trial=Roxo, Pagantes=Verde).
*   **Data Labels (Rótulos):**
    *   Formato: `"{valor_abs}\n({taxa_conv}%)"`
    *   Posição: À direita da barra. Fonte 10pt Bold.
*   **Anotações Obrigatórias (Anchors):**
    *   **Coluna Central (Delta):** Entre o gráfico M6 e M36, inserir texto calculado:
        *   `Trial->Pago: ▲ +X p.p.` (Se melhorou, Verde. Se piorou, Vermelho).
    *   **Topo:** "Base cresceu **{delta_base}x** em 30 meses".

### 🧠 C. Camada de Inteligência
*   **Como Ler:** "O eixo horizontal é logarítmico. Barras da esquerda mostram o início da operação; as da direita, o momento atual. A coluna central destaca o ganho de eficiência técnica (conversão) independente do aumento de volume."
*   **Insight Dinâmico (Escolher 1 via Lógica):**
    *   *(Se Conv M36 > Conv M6):* "Insight: A operação escalou 10x mantendo a qualidade. A conversão Trial→Pago subiu de {conv_m6}% para {conv_m36}%, provando Product-Market Fit."
    *   *(Se Conv M36 < Conv M6):* "Alerta: O volume cresceu, mas a eficiência caiu. Estamos comprando tráfego de pior qualidade (Conv caiu {delta} p.p.). Rever segmentação de Ads."

### 📋 D. Tabela Auxiliar (Abaixo do Gráfico)
| Mês | Visitas | Trials | Conv T→P (%) | Novos Pagantes | CAC (R$) | Benchmark T→P |
|:---|:---|:---|:---|:---|:---|:---|
| M0 | ... | ... | ... | ... | ... | 15% |
| M6 | ... | ... | ... | ... | ... | 15% |
| M12 | ... | ... | ... | ... | ... | 15% |
| M24 | ... | ... | ... | ... | ... | 15% |
| M36 | ... | ... | ... | ... | ... | 15% |

---

## 📊 VIZ 2.2: INDEPENDÊNCIA DE CANAIS (STACKED AREA)
*Visualiza a "guerra" entre o canal Pago e o Orgânico.*

### 📝 A. Conteúdo Textual
*   **Título:** "Conquistando a soberania da aquisição"
*   **Subtítulo:** "Mix de Canais (Stacked Area 100%) & Evolução do CAC Blended"

### 📐 B. Especificação do Gráfico
*   **Tipo:** `Stacked Area Chart` (Fundo) + `Line Chart` (Sobreposto).
*   **Eixo Y1 (Esquerdo - Área):** Percentual do Mix (0-100%).
*   **Eixo Y2 (Direito - Linha):** Valor Financeiro (R$).
*   **Camadas (Layers):**
    *   **Layer 0 (Fundo):** Área Verde Sólida (`#43A047`) representando **% Orgânico**.
    *   **Layer 1 (Meio):** Área Azul Translúcida (`#1E88E5`, alpha=0.7) representando **% Pago**.
    *   **Layer 2 (Frente):** Linha Vermelha Tracejada Espessa (`#D32F2F`) representando **CAC Blended**.
*   **Anotações Obrigatórias (Anchors):**
    *   **O Dia da Independência:** Identificar o mês exato (`idx`) onde `Orgânico > Pago`.
    *   Plotar uma linha vertical pontilhada nesse mês.
    *   Adicionar marcador "★" com texto: `"M{mes}: Independência (Org > 50%)"`.

### 🧠 C. Camada de Inteligência
*   **Como Ler:** "A área verde mostra o crescimento do canal orgânico (grátis) contra o pago (azul). A linha vermelha é o CAC médio. O objetivo é que a 'onda verde' suba, empurrando a linha de custo (vermelha) para baixo."
*   **Insight Dinâmico:**
    *   *(Se Orgânico > 50%):* "Independência atingida em M{mes}. Hoje o orgânico representa {pct_org}% das vendas, o que gerou uma economia estimada de R$ {economia} em Ads/ano."
    *   *(Se Orgânico < 30%):* "Dependência crítica de mídia paga ({pct_pago}%). Qualquer aumento no CPM do Google/Meta impactará diretamente a margem. Ação: Acelerar SEO."

### 📋 D. Tabela Auxiliar
| Mês | % Orgânico | % Pago | CAC Blended | Status |
|:---|:---|:---|:---|:---|
| M0 | 0% | 100% | R$ 500 | Dependente |
| M12 | 25% | 75% | R$ 220 | Transição |
| M36 | 60% | 40% | R$ 182 | Independente |

---

## 📊 VIZ 2.3: ELASTICIDADE & MEF (COLOR CODED)
*O semáforo de investimento. Responde: "Posso gastar mais?"*

### 📝 A. Conteúdo Textual
*   **Título:** "Eficiência Marginal: A máquina de dinheiro tem limite?"
*   **Subtítulo:** "Curva de Retorno (MEF) com Zonas de Saturação (Color-Coded)"

### 📐 B. Especificação do Gráfico
*   **Tipo:** `Scatter Plot` + `Spline Interpolation` (Curva Suave).
*   **Eixo X:** Investimento em Marketing (R$).
*   **Eixo Y:** Novos Clientes (Qtd).
*   **Lógica de Cores (O Pulo do Gato):**
    *   A linha da curva NÃO pode ter cor única. Ela deve ser um gradiente ou segmentos coloridos baseados na **Derivada (Inclinação)**:
        *   **Verde Neon (`#00E676`):** Onde `Derivada > 1.0` (Retorno Acelerado).
        *   **Amarelo (`#FFEA00`):** Onde `0.5 < Derivada < 1.0` (Rendimentos Decrescentes).
        *   **Vermelho (`#FF1744`):** Onde `Derivada < 0.5` (Saturação/Ineficiência).
*   **Elementos Obrigatórios:**
    *   **Pontos:** Plotar cada mês como um círculo pequeno.
    *   **Big Dot:** O mês atual (M36) deve ser um círculo GRANDE com borda preta.
    *   **Linha de Tendência:** Tracejada preta (`Polyfit`) indicando o R² (Previsibilidade).

### 🧠 C. Camada de Inteligência
*   **Como Ler:** "Verde = Acelere (dinheiro traz muito retorno). Amarelo = Cuidado (retorno diminuindo). Vermelho = Pare (saturação). O ponto grande marca sua posição atual na curva."
*   **Insight Dinâmico:**
    *   *(Se Ponto Atual na Zona Verde):* "Zona de Aceleração. Cada R$ 1.000 extra traz {marginal_clientes} clientes. O ROI marginal é de {roi_marg}x. Recomendação: Aumentar budget."
    *   *(Se Ponto Atual na Zona Vermelha):* "Zona de Saturação. Aumentar o budget agora só vai encarecer o CAC. O canal saturou. Recomendação: Buscar novos canais (ex: TikTok, LinkedIn)."

### 📋 D. Tabela Auxiliar
| Investimento | Clientes Est. | CAC Marginal | ROI Marginal | Zona |
|:---|:---|:---|:---|:---|
| R$ 5k | 150 | R$ 33 | 10x | 🟢 |
| R$ 20k | 500 | R$ 40 | 8x | 🟢 |
| R$ 50k | 800 | R$ 62 | 5x | 🟡 |
| R$ 100k | 900 | R$ 111 | 2x | 🔴 |

---

## 📊 VIZ 2.4: NET GROWTH & CUSTO DO CHURN
*Mostra o dinheiro vazando do balde.*

### 📝 A. Conteúdo Textual
*   **Título:** "O custo invisível do 'balde furado'"
*   **Subtítulo:** "Crescimento Líquido vs Perda Financeira por Churn (R$)"

### 📐 B. Especificação do Gráfico
*   **Tipo:** `Diverging Bar Chart` + `Area Background`.
*   **Eixo Y1 (Esquerdo):** Quantidade de Clientes.
*   **Eixo Y2 (Direito - Invertido ou Secundário):** Valor Financeiro (R$).
*   **Séries:**
    *   **Barras Verdes (Para Cima):** Novos Clientes.
    *   **Barras Vermelhas (Para Baixo):** Churn de Clientes.
    *   **Linha Preta:** Net Growth (Novos - Churn).
*   **Elemento Especial (Financial Loss Layer):**
    *   Plotar uma área sombreada vermelha clara (`#FFEBEE`) ao fundo.
    *   Altura da área = `Churn Qtd * LTV Médio`.
    *   Isso visualiza o "Dinheiro que deixamos na mesa".
*   **Anotações:**
    *   Seta no mês de maior perda: "Queima de R$ {valor_max_perda}".

### 🧠 C. Camada de Inteligência
*   **Como Ler:** "Barras mostram fluxo de pessoas. A 'mancha' vermelha ao fundo mostra fluxo de dinheiro perdido (LTV destruído). Se a mancha cresce, o buraco no balde está custando caro."
*   **Insight Dinâmico:**
    *   "No M36, o churn de {churn_rate}% consumiu {share_perda}% das novas vendas. Isso representa uma perda econômica de R$ {loss_value}/mês. Reduzir o churn em 1 p.p. economizaria R$ {economy_val}/ano."

---

## 📊 VIZ 2.5: PAYBACK PERIOD (BACKGROUND ZONES)
*Contextualiza o risco com zonas de benchmark.*

### 📝 A. Conteúdo Textual
*   **Título:** "Velocidade de retorno do capital"
*   **Subtítulo:** "Payback Period Histórico sobre Zonas de Risco Global"

### 📐 B. Especificação do Gráfico
*   **Tipo:** `Line Chart` com `Background Spans` (Faixas de Fundo).
*   **Eixo X:** Meses (Temporal).
*   **Eixo Y:** Meses de Payback (0 a 24).
*   **Background Zones (Obrigatório - Hardcoded):**
    *   `ax.axhspan(0, 6, color='#E8F5E9')` -> **Zona Excelente (<6m)**
    *   `ax.axhspan(6, 12, color='#FFFDE7')` -> **Zona Saudável (6-12m)**
    *   `ax.axhspan(12, 18, color='#FFEBEE')` -> **Zona de Risco (>12m)**
*   **Série Principal:**
    *   Linha Preta Espessa (`linewidth=2.5`) com marcadores (`o`).
*   **Anotações:**
    *   **Rótulo Final:** Caixa de texto na ponta da linha: `"{payback_atual} meses"`.
    *   **Linha de Benchmark:** Linha tracejada vermelha em `y=12` com texto "Teto SaaS (12m)".

### 🧠 C. Camada de Inteligência
*   **Como Ler:** "Payback mede o risco de liquidez. Quanto mais baixo (zona verde), mais rápido o dinheiro volta. Zona vermelha exige caixa infinito."
*   **Insight Dinâmico:**
    *   "Payback atual de {payback} meses coloca a empresa na zona {zona}. Com esse ciclo, podemos reinvestir o capital {giros_ano} vezes ao ano, acelerando o crescimento composto."

---

## 📝 3. BLOCO DE CONCLUSÃO (Rodapé da Página)

**Formato:** Texto Markdown Limpo.

**Conteúdo:**
> ### 🚀 Veredito da Máquina de Crescimento
>
> 1.  **Tração:** A empresa provou que consegue escalar (Tráfego +{x}x) mantendo a eficiência de conversão estável (Gráfico 2.1).
> 2.  **Independência:** O canal orgânico já domina {pct_org}% da aquisição, blindando a operação contra inflação de mídia paga (Gráfico 2.2).
> 3.  **Eficiência:** O ROI marginal de {roi}x indica que há espaço para dobrar o investimento antes de atingir saturação (Gráfico 2.3).
> 4.  **Risco:** O principal ponto de atenção é o Churn Financeiro (Gráfico 2.4), que consome {pct_churn_loss}% da geração de valor.
>
> **Próximo Passo:** Aumentar budget em R$ {budget_rec}k para capturar a elasticidade disponível.















Com certeza. O plano V5.0 era bom, mas com as melhorias visuais (Log Scale, Stacked Area, Zonas de Cor) ele se torna **V6.0 — DEFINITIVE INSTITUTIONAL GRADE**.

Aqui está o plano **revisado, expandido e detalhado**. Não há resumos. Cada linha é uma instrução de execução para garantir que o resultado final seja técnico, visualmente perfeito e analiticamente profundo.

---

# 📊 PLANO DE IMPLEMENTAÇÃO V6.0 (DEFINITIVO + MELHORIAS VISUAIS)
**PÁGINA 2 — GROWTH ENGINE**
**Nível:** Institutional Grade (Kaszek/Sequoia) | **Estilo:** Logarítmico & Contextual
**Status:** 🔴 CRÍTICO: SEGUIR CADA DETALHE ABAIXO. NÃO RESUMIR.

---


