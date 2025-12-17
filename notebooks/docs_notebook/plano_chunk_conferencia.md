# PLANO DE VERIFICAÇÃO FINAL: CONSISTÊNCIA VISUAL VS NARRATIVA

## 1. OBJETIVO
Garantir **ZERO ALUCINAÇÕES** no relatório final. Cada afirmação textual (markdown) deve ser corroborada matematicamente pelos gráficos (imagens) e dados brutos (`.pkl`).

## 2. METODOLOGIA: "CHUNKING AUDIT"
Dividiremos a verificação em blocos lógicos (Chunks) para isolar variáveis e evitar fadiga de contexto.

**Para cada Chunk, execute o seguinte loop de verificação:**
1.  **FATO:** O que o texto diz? (Extraído de `relatorio_completo.md`)
2.  **EVIDÊNCIA:** O que o gráfico mostra? (Verificado no arquivo da imagem e metadados `.json`)
3.  **PROVA REAL:** O que o cálculo diz? (Script Python rodando em cima do motor V13 se houver dúvida)
4.  **VEREDITO:** ✅ Consistente ou 🔴 Divergente

---

## 3. CHUNKS DE VERIFICAÇÃO (COBERTURA TOTAL)

### 🟦 CHUNK 1: PÁGINA 1 - COCKPIT (TIER 1)
**Foco:** Viabilidade Macro e KPIs Principais.

*   **Visualizações & Verificações Detalhadas:**
    *   `pg1_tabela_master_tabela.html` (Tabela Executiva)
        *   [ ] Verificar se os valores de MRR (M1, M6, M12, M36) batem com o texto de introdução.
        *   [ ] Confirmar se o status (Vermelho/Verde) dos ícones reflete os valores numéricos.
    *   `pg1_kpi_cards.png` (Painel de Controle)
        *   [ ] Conferir os 4 KPIs principais (MRR, Valuation, Runway, Cash) com o Resumo Executivo.
    *   `pg1_temporal_correlacao.png` (MRR vs Usuários)
        *   [ ] Verificar a correlação visual: As curvas crescem juntas? O texto menciona "descolamento"?
    *   `pg1_eficiencia_marketing.png` (ROI Marketing)
        *   [ ] Verificar se a barra de MRR ultrapassa a de Investimento no mês citado no texto (ex: Mês 6).

### 🟨 CHUNK 2: PÁGINA 2 - GROWTH MACHINE (TIER 2)
**Foco:** Eficiência do Funil e Canais.

*   **Visualizações & Verificações Detalhadas:**
    *   `pg2_viz2_1.png` (Funil Geral) + `_tabela.html`
        *   [ ] Comparar conversão global (Visitante -> Venda) com o benchmark citado no texto.
    *   `pg2_viz2_2.png` (Funil Conversão) + `_tabela.html`
        *   [ ] Verificar qual etapa do funil tem a maior quebra visual e se o texto identifica isso como gargalo.
    *   `pg2_viz2_3.png` (Mix Canais) + `_tabela.html`
        *   [ ] Confirma se o canal dominante no gráfico é o mesmo elogiado no texto.
    *   `pg2_viz2_4.png` (Evolução Canais)
        *   [ ] Checar se a tendência de crescimento dos canais pagos vs orgânicos condiz com a estratégia narrada.
    *   `pg2_viz2_5_cac_mix.png` (CAC Mix)
        *   [ ] Validar se o CAC Blended (médio) está visualmente abaixo do LTV.
    *   `pg2_viz2_6.png` (B2B Leads) + `_tabela.html`
        *   [ ] (Se aplicável) Verificar volume de leads qualificados.
    *   `pg2_viz2_7_tiers.png` (Growth Tiers) + `_tabela.html`
        *   [ ] Confirmar a distribuição de clientes por tier.

### 🟩 CHUNK 3: PÁGINA 3 - FINANCEIRO (TIER 3)
**Foco:** Sustentabilidade e Caixa.

*   **Visualizações & Verificações Detalhadas:**
    *   `pg3_viz1_evolucao_financeira.png` (Receita vs Despesa) + `_tabela.html`
        *   [ ] Ponto de Cruzamento: O mês visual onde Receita > Despesa bate com o "Mês de Break-even" do texto?
    *   `pg3_viz2_composicao_custos.png` (Pizza Custos)
        *   [ ] Verificar se a maior fatia da pizza corresponde ao "Maior ofensor de custos" citado.
    *   `pg3_viz2_waterfall.png` (Waterfall Custos)
        *   [ ] Analisar a decomposição dos custos variáveis vs fixos.
    *   `pg3_viz3_fluxo_caixa_semanal.png` (Caixa Semanal)
        *   [ ] Checar os "dentes de serra" (pagamentos) e se o vale mais baixo (pior caixa) bate com o texto de risco.
    *   `pg3_viz4_alavancagem.png` (Alavancagem Operacional)
        *   [ ] Confirmar se a margem operacional está expandindo no gráfico.
    *   `pg3_viz5_heatmap_dre.png` (Heatmap DRE)
        *   [ ] Cruzar números da última linha (Resultado Líquido) com o gráfico de Evolução Financeira.

### 🟧 CHUNK 4: PÁGINA 4 - UNIT ECONOMICS (TIER 4)
**Foco:** Unit Economics e Viabilidade por Cliente.

*   **Visualizações & Verificações Detalhadas:**
    *   `pg4_viz1_ltv_cac.png` (LTV/CAC)
        *   [ ] O valor final da curva (ex: 5.28x) está idêntico ao "Manchete" da página?
    *   `pg4_viz2_cohorts.png` (Cohorts)
        *   [ ] Verificar se as cores (retenção) melhoram ou pioram nas safras mais recentes (eixo Y para cima).
    *   `pg4_viz3_churn_spc.png` (Churn Control Chart)
        *   [ ] Confirmar se a linha de churn está dentro dos limites de controle (linhas pontilhadas).
    *   `pg4_viz4_escala.png` (Escala)
        *   [ ] Verificar ganho de eficiência com volume.
    *   `pg4_viz5_waterfall.png` (Waterfall Unitária)
        *   [ ] Validar a construção do LTV a partir do ARPU e Margem Bruta.

### 🟥 CHUNK 5: PÁGINA 5 - RISCO & CENÁRIOS (TIER 5) - **CRÍTICO**
**Foco:** Incerteza, Risco de Quebra e Runway (Prioridade Máxima).

*   **Visualizações & Verificações Detalhadas:**
    *   `pag5_monte_carlo_fan_chart.png` (Projeção Estocástica)
        *   [ ] Verificar se a faixa de confiança (sombra) engloba o cenário Real e Ideal narrados.
    *   `pag5_distribuicao_mes6.png` (Risco Curto Prazo)
        *   [ ] A probabilidade de caixa positivo corresponde à área sob a curva?
    *   `pag5_var_histogram.png` (VaR)
        *   [ ] Verificar se a linha vertical do VaR (5%) cai exatamente no valor R$ citado no texto.
    *   `pag5_survival_curve.png` (Curva Sobrevivência)
        *   [ ] **Ponto Crítico:** Verificar o valor exato de sobrevivência no Mês 6 (texto diz 90.7%).
        *   [ ] **Ponto Crítico:** Verificar o mês de menor sobrevivência (vale da curva).
    *   `pg5_viz2_tornado.png` (Sensibilidade) + `_tabela.html`
        *   [ ] O item no topo do tornado (maior barra) é o mesmo citado como "Maior Risco" no texto?
    *   `pg5_viz4_breakeven.png` (Break-Even Estresse) + `_tabela.html`
        *   [ ] Verificar o atraso (em meses) do cenário Estresse vs Real.
    *   `pg5_viz5_gap.png` (Gap Analysis) + `_tabela.html`
        *   [ ] Confirmar visualmente o tamanho do gap (diferença) entre as barras.
    *   `pg5_viz_funds.png` (Use of Funds)
        *   [ ] **Verificar:** Esta imagem deve ter sido removida ou estar vazia/invisível no relatório final.

### 🟪 CHUNK 6: PÁGINA 6 - VALUATION (TIER 6)
**Foco:** Retorno ao Investidor.

*   **Visualizações & Verificações Detalhadas:**
    *   `pg6_valuation.png` (Valuation Range) + `_tabela.html`
        *   [ ] Verificar se o Valuation Mínimo e Máximo do gráfico condizem com o intervalo narrado.

---

## 4. FERRAMENTA FORENSE (PROVA REAL)
Utilizaremos scripts Python dedicados para recalcular os valores exatos a partir do motor.

*   **Função Core:** `celula_4_motor.executar_motor_fintech_v10_production_ready`
*   **Script de Verificação:** `scripts/verify_runway_logic.py` (Adaptar para outras métricas conforme necessário).

## 5. STATUS DA EXECUÇÃO
- [ ] CHUNK 1 (Cockpit)
- [ ] CHUNK 2 (Growth)
- [ ] CHUNK 3 (Financeiro)
- [ ] CHUNK 4 (Unit Economics)
- [ ] CHUNK 5 (Risco - Prioridade)
- [ ] CHUNK 6 (Valuation)