# 🎭 FILOSOFIA DE SIMULAÇÃO: O MOTOR REAL VS IDEAL

> **LEITURA OBRIGATÓRIA PARA ENTENDER O NÚCLEO DO PROJETO.**

Este documento define a premissa fundamental de todo o relatório SAM. Se você não entender isso, não entenderá os gráficos.

## 1. O CONCEITO "ZERO HISTÓRICO"
Não existe "passado" nesta empresa. Não estamos analisando dados extraídos de um banco SQL de produção.
Todos os dados visuais são **SIMULAÇÕES PROJETIVAS (FORECAST)** baseadas em premissas de mercado e modelos matemáticos.

O objetivo do relatório não é mostrar "o que aconteceu", mas provar **"O QUE VAI ACONTECER"** com base em matemática auditável (Unit Economics).

---

## 2. OS DOIS MUNDOS PARALELOS (A vs B)
Para validar a tese de investimento, o motor (`MOTOR.PY`) roda duas simulações distintas e simultâneas para cada mês projetado:

### 🅰️ MUNDO A: O CENÁRIO "REAL" (Conservador)
*   **Código Gerador:** Célula 5A (`gerar_cenario_real`)
*   **DataFrame:** `df_real_m`
*   **Visualização Estética:** Linhas Pretas, Sólidas ou Barras Coloridas (Foco).
*   **Premissa:** "Pé no Chão". Usa taxas de conversão médias, aplica fricção de vendas, considera churn real e custos operacionais totais.
*   **Objetivo:** Provar que a empresa **para de pé (Break-Even)** e gera caixa mesmo sem uma execução perfeita. É o "Worst/Base Case".

### 🅱️ MUNDO B: O CENÁRIO "IDEAL" (Benchmark)
*   **Código Gerador:** Célula 5B (`gerar_cenario_ideal`)
*   **DataFrame:** `df_ideal_m`
*   **Visualização Estética:** Linhas Cinzas, Tracejadas, Sombras ou Faixas de Fundo.
*   **Premissa:** "Excelência Operacional". Força os KPIs para atingirem benchmarks de mercado de SaaS de Elite (ex: LTV/CAC > 3.0x, Churn < 5%/ano, Growth > 20% MoM).
*   **Objetivo:** Estabelecer a **META (TARGET)**. Onde deveríamos estar se fôssemos o Uber/Stripe do setor.

---

## 3. A LÓGICA DE AUDITORIA E COMPARAÇÃO
Cada visualização do relatório narra a batalha entre o Mundo A e o Mundo B.

### Por que existem as Células 5A e 5B?
A separação é intencional para garantir **Isolamento de Variáveis**:
1.  **Célula 5A (Real):** Permite testar "E se a conversão for ruim?".
2.  **Célula 5B (Ideal):** Permite calibrar "Qual o potencial máximo?".

**REGRA DE OURO DA NARRATIVA:**
> "Nós mostramos o **Real (A)** para provar segurança (Downside Protection), e mostramos o **Ideal (B)** para vender o sonho (Upside Potential)."

Isso explica por que a **Página 4 (Unit Economics)** usa linhas sobrepostas: para mostrar visualmente a distância entre a "Segurança" e o "Sonho".
