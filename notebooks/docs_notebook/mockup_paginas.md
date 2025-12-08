

---

# 📐 MOCKUP MESTRE: ESTRUTURA UNIVERSAL DE PÁGINA (A4 PRINT)

**Dimensões:** A4 Vertical ou Slide 16:9 (Otimizado para PDF)
**Fundo:** 100% Branco
**Fontes:** Helvetica/Arial (Títulos), Courier New (Tabelas)

---

## 1. O CABEÇALHO DA PÁGINA (HEADER)
*Objetivo: Situar o leitor e definir as premissas macro.*

```text
+-----------------------------------------------------------------------+
|  PÁGINA [X]: [NOME DA ÁREA - ex: UNIT ECONOMICS]                      |
|  STATUS: VALIDAÇÃO DE TESE (SIMULAÇÃO CONSERVADORA vs IDEAL)          |
|  -------------------------------------------------------------------  |
|  RESUMO EXECUTIVO (Big Numbers):                                      |
|  [KPI 1: Real vs Meta]    [KPI 2: Real vs Meta]    [KPI 3: Runway]    |
|  (Ex: LTV: R$ 900 (-10%)) (Ex: CAC: R$ 180 (OK))   (Ex: Caixa: 18m)   |
+-----------------------------------------------------------------------+
```

---

## 2. A CÉLULA DE ANÁLISE (O BLOCO ATÔMICO)
*Esta estrutura se repete de 2 a 3 vezes por página. É a "unidade de verdade".*

### **BLOCO A: A PERGUNTA (Titles)**
```text
TITULO COLOQUIAL (H2): "Uma pergunta direta de negócio?"
(Ex: "O lucro por cliente paga a aquisição rápido o suficiente?")

TITULO TÉCNICO (H3): [Métrica] - [Cenário] vs [Benchmark] ([Período])
(Ex: "LTV/CAC Ratio & Payback Period: Real vs Ideal (M0-M36)")
```

### **BLOCO B: O VISUAL (The Chart)**
*Regra: Sempre Comparativo.*
```text
+-----------------------------------------------------------------------+
|                                                                       |
|      [ EIXO Y ]                                                       |
|          |                                                            |
|          |       / (Linha Tracejada = META IDEAL)                     |
|          |      /                                                     |
|          |     /   _______ (Callout: "Desvio de -15%")                |
|          |    /   /                                                   |
|          |___/___/ (Linha Sólida/Barra = REAL CONSERVADOR)            |
|          |____________________________________ [ EIXO X ]             |
|                                                                       |
|   LEGENDA (Texto corrido abaixo do eixo):                             |
|   "A linha sólida preta é o cenário conservador. A tracejada é a      |
|    meta. A zona vermelha indica risco de insolvência."                |
+-----------------------------------------------------------------------+
```

### **BLOCO C: A PROVA (The Table)**
*Regra: Obrigatório ter Delta e Contexto.*
```text
CONTEXTO DA TABELA: "Detalhamento dos desvios mensais e impacto financeiro."
+-----------------------------------------------------------------------+
| PERÍODO |   REAL (R$)  |  META (R$)   |    Δ (DELTA)    | STATUS      |
|---------|--------------|--------------|-----------------|-------------|
|   M06   |     150      |     200      |   -50 (-25%)    | 🔴 ALERTA   |
|   M12   |     180      |     200      |   -20 (-10%)    | 🟡 ATENÇÃO  |
|   M36   |     210      |     200      |   +10 (+5%)     | 🟢 OK       |
+-----------------------------------------------------------------------+
```

### **BLOCO D: O DIAGNÓSTICO (The Insight)** DINAMICO
*Regra: Fato $\to$ Causa $\to$ Ação.*
```text
INSIGHT ESTRATÉGICO: 'nunca hardcoded'
1. FATO: O LTV Real está 25% abaixo da meta nos primeiros 6 meses.
2. CAUSA: Alta taxa de Churn (5%) no onboarding inicial puxou a curva para baixo.
3. AÇÃO: Implementar CS Dedicado na semana 1. Impacto est.: +R$ 30k/mês.
```

### **BLOCO E: COMO LER (Obrigatório)**
*Regra: Explicar para qualquer pessoa entender, incluindo termos técnicos.*

```text
📖 COMO LER ESTE GRÁFICO:

**O QUE ESTOU VENDO?**
[Explicar o propósito do gráfico em 1-2 linhas simples]

**ELEMENTOS:**
- [Elemento 1]: [O que é] - [O que significa na prática]
- [Elemento 2]: [O que é] - [O que significa na prática]
- [Cores/Zonas]: Explicar o que cada área significa

**COMO INTERPRETAR:**
- [Condição A] = [O que significa para o negócio]
- [Condição B] = [O que significa para o negócio]

**TERMOS IMPORTANTES:**
- [Termo técnico 1]: [Definição em português claro]
- [Termo técnico 2]: [Definição em português claro]
```

**EXEMPLO REAL (VIZ Fluxo de Caixa):**
```text
📖 COMO LER ESTE GRÁFICO:

**O QUE ESTOU VENDO?**
Saúde do caixa semana a semana nos primeiros 6 meses.

**ELEMENTOS:**
- Linha Azul (Saldo Caixa): Quanto dinheiro temos no banco
- Linha Vermelha (Limite Crítico): Se caixa cair abaixo, menos de 2 semanas de sobrevivência
- Ponto Vermelho (Vale): Semana mais perigosa

**COMO INTERPRETAR:**
- Caixa NUNCA deve tocar a linha vermelha = risco de insolvência
- Runway abaixo de 4 semanas = ALERTA MÁXIMO

**TERMOS IMPORTANTES:**
- Runway: Quantas semanas a empresa sobrevive sem receita nova
- Vale de Caixa: Momento de menor liquidez
```

---

## 3. AS VARIAÇÕES DE CÉLULA POR PÁGINA
*O Mockup acima é o padrão, mas cada página exige um "sabor" específico de análise.*

### **PARA A PÁGINA FINANCEIRA (Financial)**
*   **Foco:** Fluxo de Caixa e Queima.
*   **Variação Visual:** Gráfico de "Waterfall" (Cascata) para mostrar onde o dinheiro entra e sai.
*   **Pergunta Chave:** "Quando o dinheiro acaba?"

### **PARA A PÁGINA DE UNIT ECONOMICS**
*   **Foco:** Margem por unidade/cliente.
*   **Variação Visual:** Gráfico de Barras Empilhadas (Receita - Custos Var - Mkt = Margem).
*   **Pergunta Chave:** "A venda é rentável antes de pagar os fixos?"

### **PARA A PÁGINA DE RISCO & CENÁRIOS**
*   **Foco:** Incerteza (Monte Carlo).
*   **Variação Visual:** Gráfico de "Fan Chart" (Leque). Linha média + Faixas de confiança (P10/P90) sombreadas.
*   **Pergunta Chave:** "Qual a chance de tudo dar errado?"

---

## 4. O RODAPÉ DA PÁGINA (VERDICT)
*Conclusão da página inteira.*

```text
+-----------------------------------------------------------------------+
|  VEREDITO DA ÁREA:                                                    |
|  O modelo [PASSA/NÃO PASSA] no teste de estresse conservador.         |
|  Maior Risco: [Citar o gargalo principal visto nos gráficos].         |
|  Próximo Passo: [Ação corretiva prioritária].                         |
+-----------------------------------------------------------------------+
```

---

## 5. CHECKLIST DE VALIDAÇÃO DO MOCKUP (O Robô deve checar isso)

Antes de dar a página como pronta, a IA deve passar este scanner:

1.  [ ] **Teste da Tinta:** Se eu imprimir em Preto e Branco, consigo distinguir o Real do Ideal? (Sim = Linhas sólidas vs Tracejadas).
2.  [ ] **Teste da Pergunta:** O Título H2 é uma pergunta que um investidor faria?
3.  [ ] **Teste do Delta:** A tabela mostra claramente o desvio (Vermelho/Verde)?
4.  [ ] **Teste da Ação:** O insight termina com uma ordem clara do que fazer?
5.  [ ] **Teste do Real:** Fica claro que "Real" é uma "Simulação Conservadora"?
6.  [ ] **Teste do HTML:** Gráficos usam `figsize=(10,5)` para evitar scroll?
7.  [ ] **Teste Quarto:** Separadores usam `***` (NUNCA `---`)? Callouts usam sintaxe correta?

---

Este Mockup serve para **qualquer** uma das 50 visualizações que você planeja. É só trocar o "assunto" (Growth, Finanças, Risco), mas a **estrutura de raciocínio** permanece a mesma.

