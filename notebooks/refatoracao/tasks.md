# Task Master - Refatoração Notebook Investor-Grade

**Versão**: 2.0.0 (Corrigida)  
**Data**: 01/12/2025  
**Status**: ✅ Pronto para Implementação

---

## 🎯 Objetivo Principal

Transformar notebook de projeção financeira em **ferramenta operacional diária** + **documento investor-grade** com foco nos **primeiros 6 meses** (validação crítica de modelo).

### O Que Mudou (Lições Aprendidas):

- ✅ **Benchmarks realistas** fintech traders (não SaaS Enterprise maduro)
- ✅ **Granularidade semanal** em M0-M6 (não mensal!)
- ✅ **Traduções obrigatórias** de TODOS jargões
- ✅ **Insights acionáveis** (não só "falhou")
- ✅ **Metas progressivas** (não fixas 500/1000)
- ✅ **CAC realista** M0=R$500 (não R$150!)

---

## 📋 FASE 1: Fundação & Diretrizes (CONCLUÍDA ✅)

### 1.1 Diretrizes Master

- [x] Criar diretrizes master investor-grade
- [x] Adicionar seção traduções obrigatórias (D0)
- [x] Adicionar seção granularidade semanal (D0.1) ⭐ NOVO
- [x] Benchmarks realistas fintech B2C traders
- [x] Framework 5C completo
- [x] Templates código Python/Plotly

**Arquivo**: `diretrizes.md` (v2.0.0)  
**Tempo**: 6h (concluído)

### 1.2 Análise de Imagens

- [x] Analisar 14 imagens gráficos atuais
- [x] Catalogar problemas (sombras, jargões, hardcoded)
- [x] Mapear soluções específicas

**Tempo**: 3h (concluído)

---

## 📋 FASE 2: Validações & Motor (Células 03-04)

### 2.1 Célula 03 - Auditoria de Premissas ⭐ PRIORIDADE P0

**Problemas Identificados**:
- LTV/CAC 18.54x = muito alto (validar)
- Falta validação metas progressivas
- Não trava erros críticos
- Benchmarks genéricos (não específicos fintech traders)

**Tarefas**:

- [ ] **Validar LTV/CAC** alto (> 15x)
  - Adicionar warning se > 10x
  - Verificar se CAC está subestimado
  - **Tempo**: 1h

- [ ] **Implementar metas progressivas SEMANAIS** ⭐ CRÍTICO
  - Função `gerar_metas_semanais(inicial=20, taxa=0.035, semanas=26)`
  - S1: 20 usuários → S26: 62 usuários
  - Validar alcançabilidade com recursos
  - **Tempo**: 2h

- [ ] **Validar recursos necessários vs disponíveis**
  - Para cada semana S1-S26
  - CAC × novos usuários ≤ budget marketing
  - **Tempo**: 1.5h

- [ ] **Sistema de travas OBRIGATÓRIAS**
  - Erro fatal se meta inalcançável
  - Não propagar dados ruins
  - **Código**:
    ```python
    if recursos_necessarios > budget_disponivel:
        raise ValueError(f"❌ Meta S{semana} inalcançável")
    ```
  - **Tempo**: 1h

- [ ] **Benchmarks fintech traders específicos**
  - Carregar de `docs/benchmarks_da_industria.md`
  - Validar: Churn 10-12%, CAC R$400-600, LTV/CAC 2-4x
  - **Tempo**: 1h

**Tempo Total Célula 03**: 6.5h

---

### 2.2 Célula 04 - Motor Financeiro ⭐ PRIORIDADE P0

**Decisão Arquitetural**: ✅ Alerts **NO MOTOR** (detecção precoce)

**Tarefas**:

- [ ] **Sistema alertas inteligentes embutido**
  - Alert: OPEX zero após M1
  - Alert: Margem contrib negativa
  - Alert: Burn rate > 50% receita
  - Alert: Runway < 6 meses
  - **Tempo**: 3h

- [ ] **Validar cálculo OPEX** (verificado zero em alguns meses)
  - Investigar por que OPEX = 0
  - Corrigir fórmula se necessário
  - **Tempo**: 2h

- [ ] **Validar margem contribuição**
  - Por que -60% em M0? (esperado: poucos users)
  - Explicar evolução -60% → +15%
  - Adicionar interpretação no output
  - **Tempo**: 1.5h

- [ ] **Documentar cálculos críticos**
  - Comentários inline para cada fórmula
  - Referências a benchmarks
  - **Tempo**: 2h

**Tempo Total Célula 04**: 8.5h

---

## 📋 FASE 3: Dashboard M0-M6 (Célula 05C) ⭐ NOVA

### 3.1 Célula 05C - Calendário Metas Semanal (CONCLUÍDA ✅)

**Criada**: Calendário imprimível S1-S26 com metas progressivas

**O que foi feito**:
- [x] Metas semanais realistas (benchmarks corretos)
- [x] Formato imprimível (colar na parede)
- [x] Gráficos SEMANAIS (não mensal)
- [x] Traduções completas português

**Arquivo**: `CELULA_05C_CALENDARIO_METAS_SEMANAL.py`  
**Tempo**: 6h (concluído)

### 3.2 Integração no Notebook

- [ ] **Copiar célula 05C para notebook**
  - Posicionar após célula 04 (motor)
  - Executar e validar
  - **Tempo**: 0.5h

- [ ] ** Ajustar se necessário**
  - Correções visuais
  - Dados faltando
  - **Tempo**: 1h

**Tempo Total Fase 3**: 7.5h (1.5h restantes)

---

## 📋 FASE 4: Executive Summary (Célula 06) ⭐ PRIORIDADE P1

### 4.1 Correções Críticas

**Problemas**:
- Meta hardcoded 500/1000 usuários
- Gráficos com sombras
- ROI 2218% sem validação
- Falta análise detalhada M0-M6

**Tarefas**:

- [ ] **Investigar origem 500/1000** ❌ HARDCODED
  - Grep no código atual
  - Substituir por metas dinâmicas
  - **Tempo**: 0.5h

- [ ] **Implementar metas progressivas**
  - Usar função `gerar_metas_usuarios()` 
  - M0: 20, M1: 23, M3: 31... M6: 47
  - Taxa 15% M-o-M
  - **Tempo**: 1h

- [ ] **Validar ROI 2218%**
  - Conferir fórmula
  - Adicionar warning se investimento baixo
  - Explicar por que tão alto
  - **Tempo**: 1h

- [ ] **Remover sombras** de TODOS gráficos
  - `fill='none'` em todos Scatter
  - Checar visual
  - **Tempo**: 0.5h

### 4.2 Gráfico: Usuários vs Meta ⭐ CRÍTICO

- [ ] **Meta PROGRESSIVA** (não fixa 500)
  - Linha tracejada com metas mensais
  - S1-S26: granularidade semanal
  - S27+: mensal
  - **Tempo**: 2h

- [ ] **Linha de alerta** (80% meta)
  - Zona amarela se cair abaixo
  - **Tempo**: 0.5h

- [ ] **Traduzir título** 
  - "Usuários Ativos vs Meta Progressiva"
  - Subtítulo: "Meta cresce 15% ao mês (validação) → 8% (consolidação) → 3% (escala)"
  - **Tempo**: 0.5h

- [ ] **Guia interpretação obrigatória**
  - 📖 Como Ler
  - Exemplo numérico
  - **Tempo**: 0.5h

### 4.3 Todos Gráficos da Célula

- [ ] **Subtítulos coloquiais** (framework 5C)
  - Técnico + tradução português
  - **Tempo**: 1h

- [ ] **Dados numéricos visíveis**
  - Mínimo semanas-chave + trimestres
  - **Tempo**: 1h

- [ ] **Marcos temporais**
  - S4 (M1), S13 (M3), S26 (M6), M12, M24, M36
  - **Tempo**: 0.5h

- [ ] **Legendas auto-explicativas**
  - "Cenário Base (50% probabilidade)"
  - Nunca "P50" sozinho
  - **Tempo**: 0.5h

### 4.4 Output Textual

- [ ] **Tabela completa M0-M36**
  - Não só resumo final
  - Exportável CSV
  - **Tempo**: 1h

- [ ] **Insights P10/P50/P90**
  - Explicar diferença
  - "Baseado em 15.000 simulações..."
  - **Tempo**: 1h

- [ ] **Cenários com interpretação**
  - Pessimista: O QUE + POR QUÊ + AÇÃO
  - Base: idem
  - Otimista: idem
  - **Tempo**: 1.5h

- [ ] **Recomendações acionáveis**
  - Específicas por cenário
  - **Tempo**: 1h

**Tempo Total Célula 06**: 14.5h

---

## 📋 FASE 5: Growth & Traction (Célula 07) ⭐ PRIORIDADE P1

### 5.1 Nota Estratégica

- [ ] **Criar notebook separado GROWTH**
  - AI-first growth strategies
  - Diferente de SaaS tradicional
  - **Arquivo**: `growth_strategy_ai_first.ipynb`
  - **Tempo**: Fase separada (40h)

### 5.2 Gráfico Sankey (Funil)

- [ ] **Reformular**: não proporcional
  - Usar % em labels
  - Blocos uniformes
  - **Tempo**: 2h

- [ ] **3 insights OBRIGATÓRIOS**
  - Maior drop-off
  - Causa raiz
  - Ação específica
  - **Tempo**: 1h

- [ ] **Visualizar como jornada**
  - Etapas compreensíveis
  - **Tempo**: 1h

### 5.3 Evolução de Usuários

- [ ] **Remover sombras** + linhas pretas
  - **Tempo**: 0.5h

- [ ] **Corrigir offset Y** (barras começam em 20)
  - Não em zero
  - **Tempo**: 0.5h

- [ ] **Churn NEGATIVO** (abaixo eixo X)
  - Visualizar perda
  - **Tempo**: 1h

- [ ] **Granularidade SEMANAL M0-M6** ⭐
  - 26 pontos (não 7)
  - **Tempo**: 1.5h

### 5.4 Mix de Aquisição

- [ ] **DESTRUIR gráfico atual** (área empilhada ruim)
  - **Tempo**: 0.5h

- [ ] **Nova viz**: linhas + meta
  - Componentes separados
  - Meta de 50% orgânico
  - **Tempo**: 2h

- [ ] **Alerta meta não atingida**
  - Se < 50% orgânico em M6
  - **Tempo**: 0.5h

- [ ] **Dados numéricos** pontos-chave
  - **Tempo**: 0.5h

### 5.5 Churn & Retention

- [ ] **Traduzir 100%** português
  - "Churn - Taxa de Cancelamento Mensal"
  - **Tempo**: 0.5h

- [ ] **Guia leitura** sob legenda
  - Exemplo prático
  - **Tempo**: 1h

- [ ] **Subtítulo coloquial**
  - "Quantos % cancelam todo mês (meta: 10% → 7.5%)"
  - **Tempo**: 0.5h

- [ ] **Granularidade SEMANAL M0-M6** ⭐
  - Churn semanal: 2.5% → 1.8%
  - **Tempo**: 1.5h

### 5.6 Cohort Heatmap

- [ ] **Traduzir** português
  - **Tempo**: 0.5h

- [ ] **TUTORIAL completo**
  - Como ler (passo a passo)
  - Exemplo: Cohort M0 vs M6
  - **Tempo**: 1.5h

- [ ] **Diminuir tamanho**
  - 70% altura atual
  - **Tempo**: 0.5h

- [ ] **Validar valores** (M0 churn 45%?)
  - Conferir lógica
  - **Tempo**: 1h

### 5.7 Output Final

- [ ] **Tabela mês a mês**
  - Não só resumo
  - **Tempo**: 0.5h

- [ ] **Insights P10/P50/P90**
  - Com interpretação
  - **Tempo**: 1h

- [ ] **Clarificar fonte**: MC ou determinístico?
  - Explícito em cada output
  - **Tempo**: 0.5h

**Tempo Total Célula 07**: 18.5h

---

## 📋 FASE 6: DRE & Financeiro (Célula 08) ⭐ PRIORIDADE P1

### 6.1 Validações Críticas

- [ ] **Investigar OPEX zero**
  - Por que em alguns meses?
  - **Tempo**: 2h

- [ ] **EBITDA muito alta?**
  - Conferir cálculo  
  - EBITDA = Receita - COGS - OPEX
  - **Tempo**: 1.5h

- [ ] **Validar cascata waterfall**
  - Cada etapa soma corretamente
  - **Tempo**: 1.5h

### 6.2 Composição de Custos

- [ ] **3 Sankeys**: M6, M18, M36
  - Não pizza (ruim para muitas categorias)
  - Decomposição: Marketing → Ads, Afiliados, Orgânico
  - **Tempo**: 3h

- [ ] **Insights acionáveis**
  - Onde cortar custos
  - Onde investir mais
  - **Tempo**: 1h

### 6.3 Evolução das Margens

- [ ] **Margem Bruta aparece** (linha verde)
  - Confirmar visível
  - **Tempo**: 0.5h

- [ ] **Margem Contrib -60%** validar
  - Por que negativa M0-M2?
  - Explicar: custos fixos > receita
  - Mostrar quando fica positiva
  - **Tempo**: 1.5h

- [ ] **Explicação interpretação**
  - Como margem melhora com escala
  - **Tempo**: 1h

- [ ] **Meta de margem**
  - Linha referência
  - **Tempo**: 0.5h

### 6.4 Output Textual

- [ ] **DRE completo** mês a mês
  - Não só tabela simples
  - **Tempo**: 2h

- [ ] **Insights acionáveis** por linha DRE
  - **Tempo**: 1.5h

- [ ] **Alertas desvios**
  - Se margem < meta
  - **Tempo**: 1h

**Tempo Total Célula 08**: 17h

---

## 📋 FASE 7: Unit Economics (Célula 09) ⭐ PRIORIDADE P2

### 7.1 LTV/CAC Evolution

- [ ] **Explicar picos** (693 → 1878)
  - Monte Carlo ou determinístico?
  - **Tempo**: 1h

- [ ] **Correlação com outros KPIs**
  - vs Churn
  - vs CAC
  - **Tempo**: 1h

- [ ] **Guia interpretação completo**
  - **Tempo**: 1h

### 7.2 Gauge LTV/CAC

- [ ] **DESTRUIR gauge atual**
  - Substituir por barra horizontal
  - Benchmarks: 2x, 3x, 4x, 5x, 6x
  - **Tempo**: 2h

- [ ] **Subtítulo SEM jargões**
  - "Quanto Cliente Vale ÷ Custo Aquisição"
  - **Tempo**: 0.5h

### 7.3 Payback

- [ ] **DESTRUIR gráfico atual**
  - Redesenhar do zero
  - **Tempo**: 1.5h

- [ ] **Explicar eixos X e Y**
  - Tutorial completo
  - **Tempo**: 1h

- [ ] **Guia leitura**
  - Exemplo: Payback 6.9 meses = quanto?
  - **Tempo**: 1h

- [ ] **Remover jargões** sem contexto
  - "Regra dos 40" → explicar antes
  - **Tempo**: 0.5h

**Tempo Total Célula 09**: 9.5h

---

## 📋 FASE 8: Monte Carlo & Risk (Célula 10) ⭐ PRIORIDADE P2

### 8.1 Fan Chart

- [ ] **Traduzir** português
  - Todos labels
  - **Tempo**: 0.5h

- [ ] **Remover linhas pretas**
  - Cores semânticas
  - **Tempo**: 0.5h

- [ ] **Teste densidade pontos**
  - Alternativa a área
  - **Tempo**: 1.5h

- [ ] **Concentração resultados** destacada
  - P50 mais visível
  - **Tempo**: 1h

### 8.2 Distribuição Probabilidade

- [ ] **15k simulações padrão** (não 5k)
  - Atualizar todos gráficos
  - **Tempo**: 0.5h

- [ ] **Melhorar impacto visual**
  - Densidade + histograma
  - **Tempo**: 2h

- [ ] **Plotar menos linhas** se necessário
  - Max 100 linhas sobrepostas
  - **Tempo**: 1h

### 8.3 Burn Rate

- [ ] **Preencher gráfico vazio**
  - Investigar por que vazio
  - Explicar se for lucrativo (burn negativo)
  - **Tempo**: 2h

- [ ] **Insights acionáveis**
  - Quando burn é OK
  - Quando é crítico
  - **Tempo**: 1h

### 8.4 Product Engagement

- [ ] **Linha reta INACEITÁVEL**
  - Fazer previsão real OU remover
  - **Tempo**: 2h

- [ ] **Correlação com KPIs relevantes**
  - Engagement vs Churn
  - **Tempo**: 1h

**Tempo Total Célula 10**: 13h

---

## 📋 FASE 9: Operations (Célula 11) ⭐ PRIORIDADE P3

### 9.1 Headcount Evolution

- [ ] **Traduzir** português
  - **Tempo**: 0.5h

- [ ] **Melhorar visualização** (retângulos ruins)
  - Barras empilhadas
  - **Tempo**: 1.5h

- [ ] **Correlação relevante**
  - Headcount vs MRR
  - **Tempo**: 1h

- [ ] **Insights acionáveis**
  - Quando contratar
  - **Tempo**: 1h

### 9.2 ARR por Funcionário

- [ ] **Justificar meta R$150k**
  - Benchmark indústria
  - **Tempo**: 1h

- [ ] **Correlações**
  - vs Margem
  - **Tempo**: 0.5h

- [ ] **Valor gestão**
  - Quando métrica importa
  - **Tempo**: 0.5h

### 9.3 Custo Infraestrutura

- [ ] **Elementos obrigatórios** framework 5C
  - **Tempo**: 1h

- [ ] **Insights acionáveis**
  - Quando migrar infra
  - **Tempo**: 0.5h

**Tempo Total Célula 09**: 7.5h

---

## 📋 FASE 10: Exportações & Documentação ⭐ PRIORIDADE P2

### 10.1 Exportações

- [ ] **Verificar exports atuais**
  - O que já existe
  - **Tempo**: 0.5h

- [ ] **DRE completo CSV**
  - Todas linhas × 36 meses
  - **Tempo**: 1h

- [ ] **KPIs mensais CSV**
  - 15+ métricas × 36 meses
  - **Tempo**: 1h

- [ ] **Monte Carlo P10/P50/P90**
  - 3 cenários × métricas
  - **Tempo**: 1.5h

### 10.2 Diagramas Mermaid

- [ ] **Identificar onde usar**
  - Jornada usuário
  - Funil aquisição
  - **Tempo**: 1h

- [ ] **Criar diagramas**
  - 3-5 diagramas
  - **Tempo**: 2h

**Tempo Total Fase 10**: 7h

---

## 📋 FASE 11: Apresentação Final ⭐ PRIORIDADE P3

### 11.1 Estrutura Slides

- [ ] ** Mapa 20 slides** detalhado
  - O que vai em cada um
  - **Tempo**: 2h

- [ ] **Onde colar imagens**
  - Screenshots gráficos
  - **Tempo**: 1h

- [ ] **Onde usar Mermaid**
  - Diagramas
  - **Tempo**: 0.5h

### 11.2 Ordem Lógica

- [ ] **Slide 1-3**: Executive Summary
- [ ] **Slide 4-6**: Problema & Solução
- [ ] **Slide 7-9**: Mercado
- [ ] **Slide 10-12**: Produto & Tração
- [ ] **Slide 13-16**: Financials
- [ ] **Slide 17-18**: Time
- [ ] **Slide 19-20**: Ask & Uso

**Tempo**: 3.5h

**Tempo Total Fase 11**: 7h

---

## 📋 FASE 12: Scripts Refatoração ⭐ PRIORIDADE P0

### 12.1 Scripts por Célula

- [ ] `refactor_cel03_validacoes.py` (P0)
  - **Tempo**: 3h
  
- [ ] `refactor_cel04_motor_alerts.py` (P0)
  - **Tempo**: 2h
  
- [ ] `refactor_cel06_metas_prog.py` (P1)
  - **Tempo**: 3h
  
- [ ] `refactor_cel06_graficos.py` (P1)
  - **Tempo**: 4h
  
- [ ] `refactor_cel07_sankey.py` (P1)
  - **Tempo**: 2h
  
- [ ] `refactor_cel07_evolucao_users.py` (P1)
  - **Tempo**: 2h
  
- [ ] `refactor_cel08_dre.py` (P1)
  - **Tempo**: 3h
  
- [ ] `refactor_cel09_unit_econ.py` (P2)
  - **Tempo**: 2h
  
- [ ] `refactor_cel10_monte_carlo.py` (P2)
  - **Tempo**: 3h
  
- [ ] `refactor_cel11_ops.py` (P3)
  - **Tempo**: 2h

### 12.2 Qualidade Scripts

- [ ] **Backup automático** antes aplicar
  - **Tempo**: 1h (global)
  
- [ ] **Validação pós-aplicação**
  - Testes automáticos
  - **Tempo**: 2h (global)

**Tempo Total Fase 12**: 30h

---

## 📊 Status Geral & Estimativa

### Resumo por Fase:

| Fase | Descrição | Tempo Estimado | Prioridade | Status |
|------|-----------|----------------|------------|--------|
| **1** | Fundação & Diretrizes | 9h | P0 | ✅ CONCLUÍDA |
| **2** | Validações & Motor | 15h | P0 | ⏳ Pendente |
| **3** | Dashboard M0-M6 | 7.5h | P0 | ✅ 90% Concluída |
| **4** | Executive Summary | 14.5h | P1 | ⏳ Pendente |
| **5** | Growth & Traction | 18.5h | P1 | ⏳ Pendente |
| **6** | DRE & Financeiro | 17h | P1 | ⏳ Pendente |
| **7** | Unit Economics | 9.5h | P2 | ⏳ Pendente |
| **8** | Monte Carlo | 13h | P2 | ⏳ Pendente |
| **9** | Operations | 7.5h | P3 | ⏳ Pendente |
| **10** | Exportações | 7h | P2 | ⏳ Pendente |
| **11** | Apresentação | 7h | P3 | ⏳ Pendente |
| **12** | Scripts Refatoração | 30h | P0-P3 | ⏳ Pendente |
| **TOTAL** | | **155.5h** | | **6% Concluído** |

### Breakdown:

- **Total tarefas**: ~120
- **Concluídas**: ~8 (7%)
- **Em progresso**: 0
- **Pendentes**: ~112 (93%)

### Por Prioridade:

- **P0 (Crítico)**: 54h - Diretrizes, Validações, Scripts base
- **P1 (Alto)**: 50h - Células core investor docs
- **P2 (Médio)**: 36.5h - Unit econ, MC, Exports
- **P3 (Baixo)**: 15h - Ops, Apresentação

---

## 🎯 Recomendações de Execução

### Abordagem Incremental (Recomendada):

**Sprint 1** (1 semana - 40h):
- Fase 2: Validações & Motor (15h)
- Fase 3: Finalizar Dashboard M0-M6 (1.5h)
- Fase 4: Executive Summary (14.5h)
- Fase 12: Scripts P0 (5h)
- Testes & Ajustes (4h)

**Sprint 2** (1 semana - 40h):
- Fase 5: Growth & Traction (18.5h)
- Fase 6: DRE & Financeiro (17h)
- Fase 12: Scripts P1 (4.5h)

**Sprint 3** (1 semana - 40h):
- Fase 7: Unit Economics (9.5h)
- Fase 8: Monte Carlo (13h)
- Fase 9: Operations (7.5h)
- Fase 10: Exportações (7h)
- Fase 12: Scripts P2-P3 (3h)

**Sprint 4** (0.5 semana - 20h):
- Fase 11: Apresentação (7h)
- Testes integrados (8h)
- Documentação final (5h)

**Total**: 3.5 semanas (~140h úteis)

---

**Versão**: 2.0.0  
**Última atualização**: 01/12/2025  
**Próximo**: Documento 3/5 - plano_refa_celulas.md