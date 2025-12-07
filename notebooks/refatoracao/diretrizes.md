# DIRETRIZES MASTER - Visualização & Outputs Investor-Grade

**Versão**: 2.0.0 (Corrigida)  
**Data**: 30/11/2025  
**Status**: ✅ Aprovado para Implementação

---

## ❌ FALHAS IDENTIFICADAS E CORRIGIDAS

**Motivo desta atualização**: Feedback crítico do usuário - diretrizes anteriores NÃO foram aplicadas corretamente na primeira implementação.

### Problemas Corrigidos:

1. ❌ **Jargões sem tradução** (runway, burn rate, LTV/CAC, payback)
2. ❌ **Benchmarks irrealistas** (churn 5%, LTV/CAC 5x para fintech traders INICIANTE)
3. ❌ **Falta insights acionáveis** (só "falhou" sem plano de mitigação)
4. ❌ **Granularidade mensal** (deveria ser SEMANAL em M0-M6)
5. ❌ **Outputs cinza** sem necessidade
6. ❌ **Tabelas sem descrição/interpretação**
7. ❌ **Metas fixas** (500/1000 hardcoded) em vez de progressivas
8. ❌ **CAC R$141 M1** = irrealista (fintech pago real: R$500+)

---

## 🎯 Princípio Fundamental CORRIGIDO

> **Todo gráfico/tabela é uma ferramenta de DECISÃO, não apenas visualização.**

### Cada gráfico/tabela DEVE ter obrigatoriamente:

1. **Tradução português** de TODOS jargões técnicos
2. **3 insights acionáveis** (O QUE + POR QUÊ + AÇÃO concreta)
3. **Benchmarks realistas** para fintech B2C traders (produto NOVO, não maduro)
4. **Granularidade adequada**:
   - M0-M6: **SEMANAL** (26 semanas)
   - M7-M36: Mensal OK
5. **Interpretação clara** (como ler + exemplo prático numérico)

---

## 📊 DIRETRIZES VISUAIS OBRIGATÓRIAS

### D0. TRADUÇÕES OBRIGATÓRIAS ⭐ NOVA

**REGRA CRÍTICA**: TODO termo técnico em inglês ou jargão DEVE ter tradução em português.

| Termo Técnico | Tradução Brasileiro | Explicação Para Leigo |
|---------------|---------------------|----------------------|
| **Runway** | **Sobrevivência / Pista de Pouso** | Quantos meses a empresa sobrevive com caixa atual |
| **Burn Rate** | **Taxa de Queima / Queima de Caixa** | Quanto dinheiro gasta por mês |
| **Churn** | **Cancelamento / Evasão** | % de clientes que cancelam por mês |
| **LTV** | **Valor Vitalício do Cliente** | Quanto 1 cliente vale durante toda sua vida |
| **CAC** | **Custo de Aquisição** | Quanto custa conseguir 1 cliente novo |
| **Payback** | **Tempo de Retorno** | Meses para recuperar investimento em cliente |
| **Margem Contrib** | **Margem de Contribuição** | Quanto sobra depois de pagar custos variáveis |
| **MRR** | **Receita Recorrente Mensal** | Faturamento mensal de assinaturas |
| **ARR** | **Receita Anual Recorrente** | MRR × 12 |
| **ARPU** | **Receita Média por Usuário** | Quanto cada cliente paga em média |

**Formato obrigatório nos gráficos**:
- ✅ "Runway (Sobrevivência)" 
- ✅ "Burn Rate - Queima de Caixa Mensal"
- ✅ "LTV/CAC (Valor Cliente ÷ Custo Aquisição)"

❌ **NUNCA**: "Runway", "Burn Rate", "LTV/CAC" sozinhos

---

### D0.1 GRANULARIDADE SEMANAL ⭐ CRÍTICO NOVO

**REGRA**: Gráficos de M0-M6 (validação de modelo) DEVEM ser SEMANAIS!

#### Por que semanal?

- **Gestão operacional**: Meta mensal chega tarde demais para corrigir
- **Exemplo real**: Semana 9 (segunda-feira) → preciso ver meta DESSA semana
- **Decisões rápidas**: Traders abandonam rápido (churn alto), não dá pra esperar fim do mês

#### Onde aplicar:

| Gráfico | Granularidade M0-M6 | Granularidade M7-M36 |
|---------|---------------------|----------------------|
| Usuários vs Meta | **SEMANAL** (26 pontos) | Mensal (30 pontos) |
| Churn Evolution | **SEMANAL** | Mensal |
| CAC vs LTV | **SEMANAL** | Mensal |
| Burn Rate | **SEMANAL** | Mensal |
| MRR | **SEMANAL** | Mensal |

#### Como implementar:

```python
# ❌ ERRADO (mensal)
meses_m0_m6 = list(range(7))  # [0, 1, 2, 3, 4, 5, 6]

# ✅ CORRETO (semanal)
semanas_m0_m6 = list(range(1, 27))  # [1, 2, 3, ..., 26]

# Gráfico
fig.add_trace(go.Scatter(
    x=semanas_m0_m6,  # ← SEMANAL
    y=metas_semanais,
    name='Meta Semanal',
    ...
))

# Eixo X
fig.update_xaxes(
    title_text="Semana (S1-S26 = M0-M6)",
    tickvals=[1, 4, 8, 13, 17, 21, 26],  # Marcar semanas importantes
    ticktext=['S1', 'S4 (M1)', 'S8', 'S13 (M3)', 'S17', 'S21', 'S26 (M6)']
)
```

---

### D1. Estrutura Mínima (Framework 5C)

Todo gráfico DEVE ter:

1. **Contexto** (Título Duplo):
   - Técnico: "LTV/CAC Ratio Evolution"
   - + Coloquial: "Quanto cada cliente vale comparado ao custo para adquiri-lo"

2. **Clareza** (Subtítulo Explicativo):
   - Meta específica: "Meta M6: Cliente deve valer 4x o custo (benchmark fintech novo)"

3. **Comparação** (Legenda Auto-Explicativa):
   - ❌ "P50", "P90"
   - ✅ "Cenário Base (50% probabilidade)", "Cenário Otimista (90% probabilidade)"

4. **Comunicação** (Dados Numéricos Visíveis):
   - Mínimo: Semanas 1, 4, 13, 26 (M0-M6) + Meses 12, 24, 36
   - Obrigatório: Tabela dados abaixo do gráfico

5. **Call-to-Action** (Guia de Interpretação):
   - 2-3 frases: como ler
   - 1 exemplo prático com números reais
   - 1 ação se meta não atingida

---

### D2. Estilo Visual

#### ❌ Proibido:

- Sombras (`fill='tozeroy'`, `fill='tonexty'`)
- Linhas pretas (#000000)
- Área empilhada sem dados numéricos
- Gauge/medidores (usar barra horizontal com benchmarks)
- Gráficos "linha reta" ou vazios

#### ✅ Obrigatório:

- Linhas sólidas, cores contrastantes
- Grid sutil (#F1F5F9)
- Background branco puro
- Fonte: Inter ou Roboto (10-12pt)
- Palette consistente (ver D3)

---

### D3. Cores Semânticas

| Conceito | Cor Hex | Uso |
|----------|---------|-----|
| Meta/Objetivo | `#6366F1` (Indigo) | Linha de referência |
| Alcançado | `#10B981` (Green) | Acima da meta |
| Alerta | `#F59E0B` (Amber) | 80-100% da meta |
| Crítico | `#EF4444` (Red) | < 80% da meta |
| Projeção Base | `#3B82F6` (Blue) | P50 Monte Carlo |
| Otimista | `#10B981` (Green) | P90 |
| Pessimista | `#EF4444` (Red) | P10 |

---

### D4. Marcos Temporais

Todo gráfico deve marcar:

- **S1** (Semana 1): Lançamento
- **S4** (M1): Checkpoint precoce
- **S13** (M3): Validação inicial crítica
- **S26** (M6): Decisão GO/NO-GO
- **M12**: Fim consolidação
- **M24**: Fim escala inicial
- **M36**: Projeção final

Usar `add_vline()` + `add_annotation()`.

---

## 📈 DIRETRIZES DE INSIGHTS (Storytelling)

### D5. Insights Obrigatórios (Mínimo 3 por Gráfico)

**FORMATO OBRIGATÓRIO**:

1. **O QUE** (Fato numérico):
   - Ex: "Churn caindo de 10% (S1) para 7.5% (S26)"

2. **POR QUE** (Contexto + impacto):
   - Ex: "Redução 2.5pp no churn aumenta LTV de R$800 para R$1.100 (+37.5%)"

3. **E DAÍ / AÇÃO** (Decisão concreta):
   - Ex: "Manter onboarding D0 atual + adicionar vídeo tutorial D3 (teste S14-S18)"

❌ **NUNCA**: "Métrica X falhou. Revisar estratégia." (vago!)
✅ **SEMPRE**: "CAC S9 = R$450 (meta R$400). Ação: Pausar Instagram (CAC R$600), focar Facebook (CAC R$350)"

---

### D6. Comparação com Meta PROGRESSIVA

**CRÍTICO**: Metas NÃO são fixas!

❌ **ERRADO**: Meta fixa 500 usuários M6
✅ **CERTO**: Metas progressivas semanais:
- S1: 20 usuários
- S4 (M1): 25
- S13 (M3): 38
- S26 (M6): 62

**Cálculo**: Taxa crescimento 3.5% semanal (15% M-o-M)

```python
def gerar_metas_semanais(inicial=20, taxa_semanal=0.035, semanas=26):
    return [int(inicial * (1 + taxa_semanal) ** s) for s in range(semanas)]
```

---

## 🔍 VALIDAÇÕES & QUALIDADE

### D13. Checklist Pré-Publicação

Antes de considerar gráfico "pronto":

- [ ] Título compreensível para NÃO-técnicos?
- [ ] Tem guia interpretação (📖 Como Ler)?
- [ ] Mostra dados numéricos (labels)?
- [ ] Compara com meta PROGRESSIVA?
- [ ] Tem 3 insights (O QUE + POR QUÊ + AÇÃO)?
- [ ] 100% português (zero inglês/jargão sem tradução)?
- [ ] Cores seguem palette semântica?
- [ ] Sem sombras/fills?
- [ ] Granularidade correta (semanal M0-M6)?
- [ ] Funciona standalone?
- [ ] Tabela dados abaixo?

### D14. Teste da Avó

> "Se mostrar para minha avó, ela entende o básico em 10 segundos?"

- ✅ Sim → Publicar
- ❌ Não → Refazer

---

## 📚 BENCHMARKS REALISTAS POR FASE

### ⭐ D18. BENCHMARKS FINTECH B2C TRADERS (Produto NOVO)

> **ATUALIZAÇÃO CRÍTICA**: Benchmarks anteriores eram para SaaS Enterprise MADURO.  
> Valores abaixo são para **fintech B2C de TRADERS em fase de LANÇAMENTO** (produto novo < 1 ano).

#### Fase 1: Validação (M0-M6 / S1-S26)

| Métrica | Excelente | Bom | Atenção | Crítico | Justificativa |
|---------|-----------|-----|---------|---------|---------------|
| **Churn Mensal** | **< 8%** | **8-10%** | **10-12%** | **> 12%** | Traders testam várias plataformas constantemente |
| **CAC (M0)** | **< R$400** | **R$400-600** | **R$600-800** | **> R$800** | Marketing pago início = caro (não há brand) |
| **CAC (M6)** | **< R$200** | **R$200-300** | **R$300-400** | **> R$400** | Otimização + orgânico reduz CAC |
| **LTV/CAC** | **> 4x** | **3-4x** | **2-3x** | **< 2x** | Produto novo = expectativa baixa |
| **CAC Payback** | **< 6 meses** | **6-9 meses** | **9-12 meses** | **> 12 meses** | Validação rápida essencial |
| **Conv Trial→Pago** | **> 10%** | **7-10%** | **5-7%** | **< 5%** | Freemium dificulta (TradingView grátis) |
| **Margem Bruta** | **> 75%** | **65-75%** | **55-65%** | **< 55%** | IA/Compute reduz margem vs SaaS puro |

**Por que R$500 CAC M0?**
- Sem brand/SEO = 100% tráfego pago
- CPC fintech Brasil: R$3-8
- Conversão baixa (produto novo)
- Benchmark: TradingView M0 ~$150 (R$750)

#### Fase 2: Consolidação (M7-M12)

| Métrica | Excelente | Bom |
|---------|-----------|-----|
| Churn Mensal | < 6% | 6-8% |
| LTV/CAC | > 5x | 4-5x |
| CAC | < R$180 | R$180-250 |
| CAC Payback | < 5 meses | 5-7 meses |

#### Fase 3: Escala (M13-M36)

| Métrica | Excelente | Bom |
|---------|-----------|-----|
| Churn Mensal | < 5% | 5-6% |
| LTV/CAC | > 6x | 5-6x |
| CAC | < R$150 | R$150-200 |
| Regra dos 40 | > 40% | 25-40% |

**Fontes** (2024):
- QED Investors - Fintech Benchmarks
- Robinhood, eToro, TradingView (análise pública)
- OpenView Partners - SaaS B2C
- `docs/benchmarks_da_industria.md` (completo)

---

## 🚀 TEMPLATE PADRÃO (Python/Plotly)

### Exemplo: Gráfico Semanal M0-M6

```python
def plot_meta_semanal_m0_m6(df_semanal, metas_semanais, metrica='usuarios'):
    """
    Template para gráficos SEMANAIS M0-M6
    
    Args:
        df_semanal: DataFrame com coluna 'semana' (1-26)
        metas_semanais: Dict {semana: valor_meta}
        metrica: 'usuarios', 'mrr', 'churn', 'cac'
    """
    
    traduções = {
        'usuarios': 'Usuários Pagantes',
        'mrr': 'MRR - Receita Recorrente Mensal', 
        'churn': 'Churn - Taxa de Cancelamento Semanal',
        'cac': 'CAC - Custo de Aquisição'
    }
    
    fig = go.Figure()
    
    # Meta (linha tracejada)
    fig.add_trace(go.Scatter(
        x=list(metas_semanais.keys()),
        y=list(metas_semanais.values()),
        name=f'Meta {traduções[metrica]}',
        line=dict(color='#6366F1', width=2, dash='dash'),
        mode='lines+markers'
    ))
    
    # Projeção (linha sólida)
    fig.add_trace(go.Scatter(
        x=df_semanal['semana'],
        y=df_semanal[metrica],
        name=f'Projeção {traduções[metrica]}',
        line=dict(color='#3B82F6', width=3),
        mode='lines+markers'
    ))
    
    # Checkpoints
    for semana, label in [(4, 'M1'), (13, 'M3'), (26, 'M6')]:
        fig.add_vline(
            x=semana,
            line_dash='dot',
            line_color='#F59E0B',
            annotation_text=label,
            annotation_position='top'
        )
    
    # Dados numéricos em pontos-chave
    for s in [1, 4, 13, 26]:
        valor = df_semanal.loc[df_semanal['semana']==s, metrica].iloc[0]
        fig.add_annotation(
            x=s, y=valor,
            text=f"{int(valor)}",
            showarrow=False,
            yshift=10
        )
    
    fig.update_layout(
        title=dict(
            text=f"<b>{traduções[metrica]} - Meta Semanal (S1-S26)</b><br>" +
                 f"<sub>Granularidade semanal para gestão operacional diária</sub>",
            x=0.5
        ),
        xaxis_title="Semana",
        yaxis_title=traduções[metrica],
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    fig.show()
    
    # Tabela dados
    display(Markdown("### 📊 Dados do Gráfico"))
    display(df_semanal[['semana', metrica, 'meta']].head(26))
    
    # Guia interpretação
    display(Markdown(f"""
    ### 📖 Como Ler
    - **Linha tracejada roxa**: Meta semanal progressiva
    - ** Linha azul sólida**: Projeção baseada em premissas
    - **Linhas verticais**: Checkpoints (M1, M3, M6)
    
    **Exemplo**: Semana 13 (M3) → preciso {int(metas_semanais[13])} {metrica}
    """))
```

---

## ✅ CHECKLIST FINAL GRÁFICO INVESTOR-GRADE

Um gráfico está aprovado quando:

- [ ] Passa "teste da avó" (< 10seg compreensão)
- [ ] Título técnico + coloquial
- [ ] ZERO jargões sem tradução português
- [ ] Dados numéricos visíveis
- [ ] Meta PROGRESSIVA (não fixa)
- [ ] 3 insights (O QUE + POR QUÊ + AÇÃO)
- [ ] Guia interpretação (📖 Como Ler)
- [ ] Granularidade correta (semanal M0-M6)
- [ ] Cores semânticas
- [ ] Sem sombras/fills
- [ ] Marcos temporais marcados
- [ ] Tabela dados abaixo
- [ ] Funciona standalone
- [ ] Exportável HD

---

**Versão**: 2.0.0 (Corrigida com lições aprendidas)  
**Próximo**: Aplicar em refatoração células 03-11  
**Status**: ✅ APROVADO - Pronto para implementação