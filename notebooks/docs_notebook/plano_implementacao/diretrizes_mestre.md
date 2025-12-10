# 📐 MOCKUP MESTRE: ESTRUTURA UNIVERSAL DE PÁGINA V22.0

**Status:** GOLD STANDARD DEFINITIVO  
**Aplicação:** Todas as páginas do relatório (Jupyter Notebook & Export DOCX/HTML via Quarto)  
**Dimensões:** A4 Vertical (Print-First) & Responsivo (Web)  
**Fundamento:** Zero Hardcoding - Tudo Dinâmico e Inteligente

---

## 🚨 PRINCÍPIOS FUNDAMENTAIS (LEIA PRIMEIRO)

### A Regra de Ouro: ZERO HARDCODING
**TODO texto, número, insight e conclusão DEVE ser gerado dinamicamente a partir dos dados.**
### ** \notebooks\ypynb\celulas\celula_0_utils.py -- arquivo com funções úteis para todas as células, é obrigatorio ler e entender para implementar as células. ** ###

| ❌ PROIBIDO | ✅ OBRIGATÓRIO |
|------------|----------------|
| "O CAC subiu 20%" | `f"O CAC {direcao} {delta_pct:.1f}%"` |
| "Título: A PROVA NUMÉRICA" | `f"Tabela: {nome_especifico_da_metrica}"` |
| "Fonte: Modelo V10" | `f"Fonte: {df_usado} (cols: {colunas})"` |
| Conclusões estáticas | Conclusões que mudam com as premissas |

**TESTE DE VALIDAÇÃO:** Se você alterar uma premissa em `celula_2_premissas.py`, TODOS os textos do relatório devem se adaptar automaticamente.

---

## 1. ANATOMIA DE UMA PÁGINA (Estrutura Obrigatória)

### 1.1 Assinatura da Função (Boilerplate Canônico)

```python
# PAGINA_X_NOME.py

def executar_pagina_X_nome(df_real_m, df_real_s, df_ideal, premissas, report_mode=False):
    """
    PÁGINA X: [NOME DA ÁREA]
    
    Argumentos:
        df_real_m: DataFrame mensal do cenário conservador (Célula 5A)
        df_real_s: DataFrame semanal do cenário conservador (Célula 5A)
        df_ideal: DataFrame do cenário benchmark (Célula 5B)
        premissas: Dicionário de configuração (Célula 2)
        report_mode: True para export Quarto, False para notebook interativo
    """
    
    # BLOCO 0: Cabeçalho da Página
    if report_mode:
        display(Markdown("# PÁGINA X: [NOME DA ÁREA]"))
        display(Markdown(
            "**Objetivo:** Validar a tese de [TEMA] confrontando "
            "o cenário conservador (Real) vs benchmarks de mercado (Ideal)."
        ))
        display(Markdown("***"))  # NUNCA usar "---" (causa YAML error)
    else:
        print("="*80)
        print(f"🚀 PÁGINA X: {nome_area.upper()}")
        print("="*80)
    
    # BLOCO 1-5: Os 5 Atos Narrativos (ver seção 2)
    # ...
    
    # BLOCO 6: Veredito Final (ver seção 4)
    # ...
```

---

## 2. OS 5 ATOS NARRATIVOS (Framework Universal)

**TODA página DEVE contar uma história linear através de 5 visualizações que respondem a perguntas letais:**

| Ato | Função Narrativa | Pergunta do CEO | O Que Provar |
|-----|-----------------|-----------------|--------------|
| **Viz 1** | **A Tese (Macro)** | "O modelo sobrevive no pior caso?" | Resultado acumulado é positivo |
| **Viz 2** | **A Saúde (Unitária)** | "Cada unidade é lucrativa?" | Não perdemos dinheiro por venda |
| **Viz 3** | **O Controle (Tático)** | "Há controle na largada?" | Volatilidade corrigida rápido |
| **Viz 4** | **A Escala (Futuro)** | "Até onde podemos crescer?" | Identificar teto de saturação |
| **Viz 5** | **O Vazamento (Risco)** | "Onde está o dinheiro invisível?" | Quantificar perdas ocultas |

### 2.1 Exemplo: Aplicação no Financeiro

| Ato | Métrica Concreta | Visual Esperado |
|-----|-----------------|-----------------|
| Viz 1 | Runway (Caixa Acumulado) | Linha do tempo até Breakeven |
| Viz 2 | Burn Multiple | Barras comparativas Real vs Ideal |
| Viz 3 | Fluxo de Caixa Semanal | Linha temporal 0-24 semanas |
| Viz 4 | Alavancagem Operacional | Scatter plot Receita vs Custos |
| Viz 5 | Impostos + Inadimplência | Waterfall de destruição de margem |

---

## 3. A CÉLULA DE ANÁLISE (Bloco Atômico - Padrão Obrigatório)

**TODA visualização DEVE seguir esta estrutura de 6 elementos, nesta ordem:**

### 3.1 Template Completo

```python
# ============================================================================
# VIZ X.Y: [NOME TÉCNICO DA MÉTRICA]
# ============================================================================

# --- ELEMENTO 1: TÍTULOS (Coloquial + Técnico) ---
title_colloquial = "Uma pergunta direta que o CEO faria?"
# Ex: "O lucro por cliente paga a aquisição rápido suficiente?"

title_technical = f"VIZ {pagina}.{numero}: {metrica} - {cenario} vs {benchmark}"
# Ex: "VIZ 4.1: LTV/CAC Ratio - Evolução M0-M36 (Real vs Ideal)"

# --- ELEMENTO 2: PREPARAÇÃO DOS DADOS (Dinâmico) ---
# Calcular TODAS as métricas necessárias
cac_inicial = df_real_m.iloc[0]['cac']
cac_final = df_real_m.iloc[-1]['cac']
delta_cac = (cac_final - cac_inicial) / cac_inicial
direcao = "subiu" if delta_cac > 0 else "caiu"

# --- ELEMENTO 3: O GRÁFICO (Matplotlib) ---
fig, ax = plt.subplots(figsize=(10, 5))  # SEMPRE (10,5) para HTML

# Plot Real (Foco)
ax.plot(df_real_m['mes'], df_real_m['cac'], 
        color='#000000', linewidth=2, label='Real')

# Plot Ideal (Referência)
ax.plot(df_ideal['mes'], df_ideal['cac'], 
        color='#9E9E9E', linewidth=1, linestyle='--', label='Ideal')

# Configurações obrigatórias
ax.set_xlabel("Mês")
ax.set_ylabel("CAC (R$)")
ax.set_title(title_technical, pad=20, fontweight='bold')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
plt.tight_layout()

# Salvar figura (sem exibir duplicado)
from celulas.celula_0_utils import salvar_figura_silencioso
caminho_fig = salvar_figura_silencioso(
    fig, f"viz_{pagina}_{numero}_cac_evolucao", report_mode
)

# --- ELEMENTO 3-A: Fonte Primária --- ** SEMPRE INSERIR A FONTE PRIMARIA NO GRAFICO **
**Fonte Primária:** df_real_m (Célula 5A - Bootstrap Conservador) vs df_ideal (Célula 5B - Benchmark)



# --- ELEMENTO 4: LEGENDA "COMO LER" (Texto Corrido) ---
legend_md = f"""
**📖 COMO LER ESTE GRÁFICO:**

Este gráfico mostra a evolução do Custo de Aquisição de Cliente (CAC) ao longo de 36 meses. 
A **linha preta sólida** representa o cenário conservador (Real), enquanto a **linha cinza 
tracejada** mostra o benchmark de mercado (Ideal). Quanto mais baixa a linha, melhor a 
eficiência de marketing. O CAC Real {direcao} {abs(delta_cac)*100:.1f}% no período, 
{("ficando abaixo" if delta_cac < 0 else "superando")} a meta ideal.

**GLOSSÁRIO:**
- **CAC:** Custo de Aquisição de Cliente = Gasto Marketing ÷ Novos Clientes
- **Benchmark:** Média do mercado SaaS B2B (~R$ 1.500 para nosso segmento)
"""

if report_mode:
    display(Markdown(legend_md))
else:
    display(Markdown(legend_md))

# --- ELEMENTO 5: TABELA DE PROVA (Auditável) ---
# Preparar dados da tabela
periodos_chave = [0, 6, 12, 24, 36]
tabela_data = []

for mes in periodos_chave:
    if mes < len(df_real_m):
        real_val = df_real_m.iloc[mes]['cac']
        ideal_val = df_ideal.iloc[mes]['cac']
        delta = real_val - ideal_val
        delta_pct = (delta / ideal_val) * 100
        
        # Status com emoji
        if delta_pct <= -10:
            status = "🟢 EXCELENTE"
        elif delta_pct <= 10:
            status = "🟡 ACEITÁVEL"
        else:
            status = "🔴 ALERTA"
        
        tabela_data.append({
            'Período': f'M{mes:02d}',
            'Real (R$)': f'{real_val:,.0f}',
            'Ideal (R$)': f'{ideal_val:,.0f}',
            'Δ (Delta)': f'{delta:+,.0f} ({delta_pct:+.1f}%)',
            'Status': status
        })

df_tabela = pd.DataFrame(tabela_data)

# Título específico da tabela (NUNCA "A PROVA NUMÉRICA")
table_title = f"**Tabela {pagina}.{numero}: Evolução do CAC - Marcos Temporais**"

if report_mode:
    display(Markdown(table_title))
    display(Markdown(df_tabela.to_markdown(index=False)))
    display(Markdown(
        f"_Fonte: df_real_m vs df_ideal | "
        f"Colunas: 'mes', 'cac', 'gasto_marketing', 'novos_clientes'_"
    ))
else:
    display(Markdown(table_title))
    display(df_tabela)

# --- ELEMENTO 5-A: descrição da tabela ---

# --- ELEMENTO 6: INSIGHT DINÂMICO (FATO + CAUSA + IMPLICAÇÃO + AÇÃO) ---
# Calcular métricas para o insight
delta_mkt = df_real_m.iloc[-1]['gasto_marketing'] - df_real_m.iloc[0]['gasto_marketing']
delta_conversao = (
    df_real_m.iloc[-1]['taxa_conversao'] - df_real_m.iloc[0]['taxa_conversao']
) * 100

insight_md = f"""
::: {{.callout-tip}}
## 💡 INSIGHT ESTRATÉGICO

**FATO:** O CAC {direcao} {abs(delta_cac)*100:.1f}% no período analisado, 
terminando em R$ {cac_final:,.0f} (vs meta de R$ {df_ideal.iloc[-1]['cac']:,.0f}).

**CAUSA:** Aumento de {formata_moeda(delta_mkt)} no investimento de marketing 
({delta_mkt/df_real_m.iloc[0]['gasto_marketing']*100:.0f}%) sem melhoria proporcional 
na conversão (apenas {delta_conversao:+.1f} p.p.).

**IMPLICAÇÃO:** Cada novo cliente está custando R$ {cac_final - df_ideal.iloc[-1]['cac']:,.0f} 
acima do ideal, reduzindo a margem de contribuição e aumentando o payback period de 
{df_real_m.iloc[-1]['payback_months']:.1f} para {df_real_m.iloc[-1]['payback_months']:.1f} meses.

**AÇÃO RECOMENDADA:** Revisar campanhas de tráfego pago, testar novos canais orgânicos 
e otimizar taxa de conversão do funil (meta: aumentar de 
{df_real_m.iloc[-1]['taxa_conversao']*100:.1f}% para {df_ideal.iloc[-1]['taxa_conversao']*100:.1f}%).
:::
"""

display(Markdown(insight_md))

# --- ELEMENTO 7: AUDITORIA (Fórmulas e Fonte) ---
audit_md = """
::: {.callout-note collapse="true"}
## 🔍 AUDITORIA TÉCNICA

**Fonte Primária:** df_real_m (Célula 5A - Bootstrap Conservador) vs df_ideal (Célula 5B - Benchmark)

**Fórmulas Utilizadas:**
1. **CAC** = `gasto_marketing` ÷ `novos_clientes`
2. **Delta %** = ((Valor Final - Valor Inicial) ÷ Valor Inicial) × 100
3. **Status**: Verde (≤-10%), Amarelo (±10%), Vermelho (>10%)

**Premissas Utilizadas:**
- Taxa de conversão base: `premissas['taxa_conversao_inicial']`
- Gasto marketing inicial: `premissas['gasto_marketing_m0']`
- Crescimento mensal de marketing: `premissas['crescimento_mkt_mensal']`

**Validação Cruzada:** Os valores de CAC foram cruzados com a métrica LTV/CAC 
(Viz 4.2) para garantir consistência.
:::
"""

display(Markdown(audit_md))
```

---

## 4. O VEREDITO FINAL (Storytelling da Página)

**TODA página DEVE terminar com um texto narrativo que conecta os 5 atos em uma conclusão jurídica.**

### 4.1 Template de Veredito

```python
def gerar_veredito_pagina_X(df_real_m, df_ideal, premissas, report_mode):
    """
    Gera o veredito narrativo final da página.
    REGRA: Texto corrido (storytelling), NÃO lista de bullets.
    """
    
    # 1. Calcular métricas para a narrativa
    status_final = "VIÁVEL" if df_real_m.iloc[-1]['caixa'] > 0 else "CRÍTICO"
    taxa_realizacao = (
        df_real_m.iloc[-1]['receita_acum'] / df_ideal.iloc[-1]['receita_acum']
    ) * 100
    
    gap_principal = identificar_maior_gap(df_real_m, df_ideal)  # Função auxiliar
    
    # 2. Construir narrativa dinâmica
    veredito_md = f"""
### 🏁 VEREDITO FINAL: {nome_area.upper()} (Status: {status_final})

A análise dos indicadores desta seção confirma uma tendência de 
**{("crescimento sustentável" if status_final == "VIÁVEL" else "risco elevado")}**. 

Começamos observando na **Viz {pagina}.1** que o modelo atinge {taxa_realizacao:.0f}% 
da meta no cenário conservador, {("garantindo viabilidade" if taxa_realizacao > 80 else "exigindo atenção")}. 
A eficiência unitária demonstrada na **Viz {pagina}.2** confirma que cada operação gera 
margem positiva, embora abaixo do benchmark ideal.

O controle tático evidenciado na **Viz {pagina}.3** mostra que a equipe conseguiu 
estabilizar a volatilidade inicial em menos de {semanas_para_estabilizar} semanas, 
um indicador de maturidade operacional. A análise de escala da **Viz {pagina}.4** 
revelou que o modelo suporta crescimento até R$ {teto_receita:,.0f}/mês antes de 
atingir retornos decrescentes.

Por fim, a **Viz {pagina}.5** quantifica o principal vazamento: **{gap_principal['nome']}** 
consome {gap_principal['valor_pct']:.1f}% da receita potencial, representando 
R$ {gap_principal['valor_abs']:,.0f} em oportunidade perdida.

**CONCLUSÃO ESTRATÉGICA:**  
O modelo provou-se {("robusto" if status_final == "VIÁVEL" else "frágil")} para 
{("escala imediata" if status_final == "VIÁVEL" else "operação controlada")}. 
O gargalo principal migrou de {gap_historico} para {gap_principal['nome']}, 
exigindo {("otimização" if status_final == "VIÁVEL" else "reestruturação")} antes da Série A.
"""
    
    # 3. Renderização condicional
    if report_mode:
        display(Markdown(f"::: {{.callout-important}}\n{veredito_md}\n:::"))
    else:
        display(Markdown(veredito_md))
```

---

## 5. CHECKLIST DE QUALIDADE (Critérios de Aceite)

Antes de aprovar qualquer código, verifique **TODOS** os itens:

### 5.1 Estrutura Fundamental
- [ ] Tem cabeçalho H1 + Objetivo no topo?
- [ ] Segue os 5 Atos Narrativos?
- [ ] Tem Veredito Final conectando todas as Vizes?

### 5.2 Qualidade das Visualizações
- [ ] TODAS as Vizes usam `render_atomic_block` ou seguem o template completo?
- [ ] Proibido `display(plt.show())` ou `display(fig)` soltos?
- [ ] Gráficos têm `figsize=(10, 5)` para HTML?
- [ ] Labels não sobrepõem título/legenda?

### 5.3 Zero Hardcoding
- [ ] TODOS os insights são f-strings dinâmicas?
- [ ] Tabelas têm títulos específicos (não "A PROVA NUMÉRICA")?
- [ ] Fontes citam variáveis exatas (`df_real_m` vs `df_ideal`)?
- [ ] Se alterar premissas, os textos mudam automaticamente?

### 5.4 Legibilidade e Auditoria
- [ ] "COMO LER" é texto corrido (não lista vertical)?
- [ ] Tem Glossário explicando siglas?
- [ ] Callout de Auditoria tem fórmulas matemáticas?
- [ ] Fonte dos dados está explícita (DataFrame + Colunas)?

### 5.5 Compatibilidade Quarto
- [ ] Usa `***` para separadores (NUNCA `---`)?
- [ ] Callouts seguem padrão `{{` em f-strings e `{` em strings normais?
- [ ] Tabelas são Markdown puro (`df.to_markdown()`)?
- [ ] Testou `quarto render ... --to docx` sem erros?

**REGRA DE REJEIÇÃO:** Se **QUALQUER** item acima for "NÃO", o código deve ser rejeitado e refeito.

---

## 6. PADRÕES VISUAIS POR TIPO DE GRÁFICO

### 6.1 Linhas Temporais (Evolução)
```python
# Real: Preto, Sólido, Destaque
ax.plot(x, y_real, color='#000000', linewidth=2, label='Real')

# Ideal: Cinza, Tracejado, Referência
ax.plot(x, y_ideal, color='#9E9E9E', linewidth=1, linestyle='--', label='Ideal')

# Benchmark Externo: Vermelho, Pontilhado
ax.axhline(y=benchmark, color='#D32F2F', linestyle=':', label='Mercado')
```

### 6.2 Barras Comparativas (Ghost Bar)
```python
# Ideal: Barra Larga, Cinza, Fundo
ax.barh(categorias, valores_ideal, height=0.8, 
        color='#E0E0E0', alpha=0.5, label='Meta')

# Real: Barra Estreita, Colorida, Frente
ax.barh(categorias, valores_real, height=0.4, 
        color='#2E7D32', label='Atual')
```

### 6.3 Tabelas (Formatação)
```python
# Status com Emojis
def obter_status_emoji(valor, limites):
    if valor < limites['verde']:
        return "🟢 EXCELENTE"
    elif valor < limites['amarelo']:
        return "🟡 ACEITÁVEL"
    else:
        return "🔴 ALERTA"

# Delta Explícito
delta_texto = f"{delta:+,.0f} ({delta_pct:+.1f}%)"
```

---

## 7. ANTI-PADRÕES (O Que NÃO Fazer)

| ❌ ERRO COMUM | 🚫 CONSEQUÊNCIA | ✅ SOLUÇÃO |
|--------------|-----------------|-----------|
| Usar `---` em Markdown | YAML parse error | Usar `***` |
| `{{` em string normal | Aparece literal `{{` | Usar `{` ou f-string |
| `figsize=(14, 6)` | Scroll horizontal | Usar `(10, 5)` |
| Título "A PROVA NUMÉRICA" | Genérico/amador | Título específico |
| `<b>` em Callout | HTML literal | Usar `**bold**` |
| Annotations dentro do gráfico | Poluição visual | Legenda externa |
| Valores hardcoded | Mentira se dados mudarem | Cálculo dinâmico |
| Bulk replace de `{{` | Quebra f-strings | NÃO FAZER |

---

## 8. EXEMPLO COMPLETO: PÁGINA FINANCEIRO

### 8.1 Aplicação dos 5 Atos

```python
def executar_pagina_3_financeiro(df_real_m, df_real_s, df_ideal, premissas, report_mode=False):
    """PÁGINA 3: FINANCEIRO - Validação de Viabilidade Econômica"""
    
    # Cabeçalho
    if report_mode:
        display(Markdown("# PÁGINA 3: FINANCEIRO"))
        display(Markdown(
            "**Objetivo:** Validar a sustentabilidade financeira do modelo através "
            "da análise de DRE, fluxo de caixa e estrutura de custos."
        ))
        display(Markdown("***"))
    
    # VIZ 3.1: A TESE - Runway (Caixa sobrevive?)
    # ... [código completo do template 3.1] ...
    
    # VIZ 3.2: A SAÚDE - Burn Multiple (Unidade eficiente?)
    # ... [código completo do template 3.1] ...
    
    # VIZ 3.3: O CONTROLE - Fluxo Semanal (Volatilidade controlada?)
    # ... [código completo do template 3.1] ...
    
    # VIZ 3.4: A ESCALA - Alavancagem Operacional (Elasticidade?)
    # ... [código completo do template 3.1] ...
    
    # VIZ 3.5: O VAZAMENTO - Tax Leak (Dinheiro invisível?)
    # ... [código completo do template 3.1] ...
    
    # Veredito Final
    gerar_veredito_pagina_3(df_real_m, df_ideal, premissas, report_mode)
```

### 8.2 Métricas Concretas por Ato

| Ato | Métrica | Fórmula Dinâmica |
|-----|---------|------------------|
| Viz 3.1 | Runway | `caixa_atual / burn_rate_mensal` |
| Viz 3.2 | Burn Multiple | `(custo_total - receita) / nova_receita_mrr` |
| Viz 3.3 | Volatilidade | `std(fluxo_semanal) / mean(fluxo_semanal)` |
| Viz 3.4 | Alavancagem | `delta_receita% / delta_custo%` |
| Viz 3.5 | Tax Leak | `impostos_totais / receita_bruta` |

---

## 9. INTEGRAÇÃO COM OUTROS DOCUMENTOS

Este Mockup é o **DOCUMENTO CENTRAL** e deve ser lido em conjunto com:

| Documento | Relação com Mockup |
|-----------|-------------------|
| `diretrizes_checklist.md` | Lista de verificação pré-entrega |
| `filosofia_simulacao.md` | Contexto dos cenários Real vs Ideal |
| `DOCUMENTACAO_TECNICA_MASTER.md` | Detalhes de implementação técnica |
| `celula_0_utils.py` | Funções compartilhadas (não recriar) |

---

## 10. RESUMO EXECUTIVO (TL;DR)

1. **Toda página** segue os 5 Atos Narrativos (Tese → Saúde → Controle → Escala → Vazamento)
2. **Toda visualização** tem 7 elementos obrigatórios (Título → Gráfico → Como Ler → Tabela → descrição da tabela → Insight → Auditoria)
3. **Todo texto** é dinâmico (f-strings, ZERO hardcoding)
4. **Toda tabela** tem título específico e fonte explícita
5. **Todo gráfico** usa `figsize=(10, 5)` e `salvar_figura_silencioso()`
6. **Todo separador** usa `***` (NUNCA `---`)
7. **Todo callout** segue `{{` em f-string, `{` em string normal

**TESTE FINAL:** Altere uma premissa → Execute o notebook → Todos os textos devem se adaptar automaticamente.

---

**Versão:** V22.0 - Gold Standard Definitivo  
**Última Atualização:** 10/12/2025  
**Mantenedor:** Sistema SAM - Financial Deck Generator