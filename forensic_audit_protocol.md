# Protocolo Mestre de Auditoria Forense: SAM Análise Financeira (V22.0)

**Versão da Auditoria:** 3.0 (Definitiva)
**Escopo:** Código (Lógica), Dados (Input) e Visualização (Output).

## 🎯 Objetivo da Auditoria
Garantir que o artefato final (`Pitch Deck Financeiro`) seja **1. Matematicamente Preciso**, **2. Logicamente Consistente** e **3. Visualmente Coerente**.
O auditor (IA ou Humano) deve seguir este roteiro sequencial, sem pular etapas.

**Diretórios Alvo:**
*   Gráficos: `e:\Projetos\sam_analise_financeira\notebooks\ypynb\outputs\figs`
*   Tabelas: `e:\Projetos\sam_analise_financeira\notebooks\ypynb\outputs\tables`
*   Logs: `e:\Projetos\sam_analise_financeira\notebooks\ypynb\outputs\metadata`
*   **Arquivo de Saída da Auditoria:** `e:\Projetos\sam_analise_financeira\auditoria_forense_resultado.md`

---

## 📂 PARTE 1: Manifesto de Integridade (Checklist de Arquivos)
**Verificação Binária:** O arquivo existe? (Sim/Não). Se "Não", a auditoria falha imediatamente.

### 1.1 Gráficos Essenciais (A Prova Visual)
| ID | Arquivo Esperado | Descrição |
|----|------------------|-----------|
| **P1** | `pg1_kpi_cards.png` | KPIs de Topo |
| **P1** | `pg1_temporal_correlacao.png` | Evolução Temporal |
| **P1** | `pg1_eficiencia_marketing.png` | Eficiência de Growth |
| **P2** | `pg2_viz2_canais.png` | Mix de Canais |
| **P2** | `pg2_viz3_unit_econ_ltv.png` | LTV Unitário |
| **P3** | `pg3_viz1_evolucao_financeira.png` | Caixa vs EBITDA (Dual Axis) |
| **P3** | `pg3_viz1_dre_breakdown.png` | Tabela DRE (Imagem suporte, ou HTML) |
| **P3** | `pg3_viz2_waterfall.png` | Cascata de Lucro |
| **P3** | `pg3_viz2_composicao_custos.png` | Barras Real vs Benchmark |
| **P3** | `pg3_viz3_fluxo_caixa_semanal.png` | Entradas vs Saídas |
| **P3** | `pg3_viz4_alavancagem.png` | Scatter Margem vs Receita |
| **P3** | `pg3_viz5_heatmap_dre.png` | Real vs Ideal |
| **P4** | `pg4_viz1_ltv_cac.png` | LTV/CAC Ratio |
| **P4** | `pg4_viz2_cohorts.png` | Retention Heatmap |
| **P4** | `pg4_viz3_churn_spc.png` | Controle de Churn |
| **P4** | `pg4_viz4_escala.png` | Economia de Escala |
| **P4** | `pg4_viz5_waterfall.png` | Margem Contribuição |
| **P5** | `pag5_survival_curve.png` | Curva de Sobrevivência |
| **P5** | `pg5_viz_funds.png` | Use of Funds |
| **P5** | `pg6_valuation.png` | Valuation Probabilístico |

### 1.2 Tabelas de Dados (A Prova Analítica)
| ID | Arquivo HTML Esperado | Conteúdo |
|----|-----------------------|----------|
| **T1** | `pg1_viz1_exec_table_tabela.html` | Resumo Executivo |
| **T2** | `pg2_viz2_1_tabela.html` | Detalhe Canais 1 |
| **T2** | `pg2_viz2_7_tiers_tabela.html` | Growth Tiers |
| **T5** | `pg5_viz2_tornado_tabela.html` | Sensibilidade (Tornado) |
| **T5** | `pg5_viz4_breakeven_tabela.html` | Ponto de Equilíbrio |
| **T5** | `pg5_viz5_gap_tabela.html` | Gaps Real vs Ideal |
| **--** | *(Outras tabelas pg2_viz2_X conforme mix)* | Tabelas auxiliares de canais |

---

## ⚙️ PARTE 2: Auditoria de Lógica (Motor & Premissas)
**Objetivo:** Caçar bugs silenciosos que o Python não pega (erros de regra de negócio).

### 2.1 Validação de Premissas (`celula_2_premissas.py`)
1.  **Regra do Aporte Finito:**
    *   *Verificar:* Variável `meses_aporte = 6` (ou similar).
    *   *Erro:* Se for 36 ou None, é **Aporte Infinito** (Gráfico P3_Viz3 ficará errado).
2.  **Gatilhos de Salário:**
    *   *Verificar:* Salários não podem ser `True` desde o mês 0 se a receita for 0 (Modelo Bootstrap).
    *   *Erro:* `trigger_fundador = 0` (Significa salário desde o dia 1 sem caixa).
3.  **Impostos:**
    *   *Verificar:* `imposto_simples_inicial` vs `imposto_lucro_presumido`.
    *   *Lógica:* O sistema deve mudar de alíquota se faturamento > R$ 4.8M.

### 2.2 Validação do Motor (`celula_4_motor.py`)
1.  **Vazamento de Caixa:**
    *   *Fórmula:* `Variacao Caixa = (Receita - Deducoes - COGS - OPEX) + Aportes`.
    *   *Teste:* A conta fecha centavo a centavo no mês 36?
2.  **Lógica Growth:**
    *   *Teste:* Se `budget_marketing` for cortado (por falta de caixa), o `novos_clientes` cai proporcionalmente? (Se não cair, há "Magic Growth").
3.  **Lógica Churn:**
    *   *Teste:* O Churn é aplicado sobre a base TOTAL ou apenas novos? (Deve ser Base Total Anterior).

---

## 🧠 PARTE 3: Auditoria Semântica & Visual (Output)
**Objetivo:** Simular o olhar de um Investidor Sênior ("Cheiro de Erro").

### 3.1 Finanças (Página 3)
- [ ] **Teste do "EBITDA Impossível":** No `pg3_viz2_waterfall.png`, a barra de EBITDA é maior que a de Receita Bruta? (Se sim, ERRO CRÍTICO).
- [ ] **Teste do "Runway Infinito":** No `pg3_viz1_evolucao_financeira.png`, a linha azul (Caixa) sobe verticalmente sem parar após o mês 6? (Indica erro de aporte perpétuo).
- [ ] **Teste da Alavancagem:** No `pg3_viz4_alavancagem.png`, os pontos mais recentes (cores quentes) estão mais à direita e acima? (Crescimento saudável). Se voltarem para a esquerda, é retração.

### 3.2 Unit Economics (Página 4)
- [ ] **Teste LTV > CAC:** No `pg4_viz1_ltv_cac.png`, a curva LTV (azul) cruza o CAC (vermelho) e fica acima? Se LTV < CAC para sempre, negócio inviável.
- [ ] **Teste Cohort:** No `pg4_viz2_cohorts.png`, as cores esfriam (ficam azuis/claras) da esquerda para a direita? Se esquentarem (melhorarem) com o tempo sem explicação de "Upsell", é suspeito.

### 3.3 Risco (Página 5)
- [ ] **Teste Bootstrap:** No `pg5_viz_funds.png`, se "Equipe" for 0%, existe uma nota de rodapé explicando "Gatilho de Receita"?

---

## 📝 Formato do Relatório de Saída
A IA Auditora deve gerar o arquivo `auditoria_forense_resultado.md` com este exato padrão:

```markdown
# 🛡️ Relatório de Auditoria Forense - SAM V22.0

## 1. Integridade de Arquivos
- **Gráficos:** [18]/18 encontrados. ✅
- **Tabelas:** [11]/11 encontradas. ✅
- **Faltantes:** Nenhum.

## 2. Auditoria Lógica (Motor)
| Item | Resultado | Obs |
|------|-----------|-----|
| Aporte Finito | ✅ PASS | Corta no Mês 6 corretamente. |
| Impostos | ⚠️ ALERTA | Faturamento M36 encosta no teto do Simples. |

## 3. Auditoria Visual (Semântica)
- **Runway:** Normal (Curva J-Curve). ✅
- **LTV/CAC:** Saudável (>3x). ✅
- **Use of Funds:** Alerta (100% Marketing). Explicado por Bootstrap. 🟡

## 🚨 VEREDITO FINAL
[APROVADO / REPROVADO]
O modelo é consistente matematikamente e visualmente coerente para apresentação a investidores.
```
