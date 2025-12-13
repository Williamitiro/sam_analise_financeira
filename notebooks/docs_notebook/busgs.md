# 🔍 ANÁLISE DE AUDITORIA - IDENTIFICAÇÃO DE FALHAS

Analisando os códigos fornecidos, identifico **MÚLTIPLAS CAMADAS DE BUGS** que explicam as anomalias reportadas. Vou categorizá-las por gravidade:

---

## 🔴 BUGS CRÍTICOS (SHOW STOPPERS)

### **BUG #1: "Ghost Marketing" - Marketing R$0 gerando visitas pagas**
**Localização:** `celula_4_motor.py` linhas 290-340

**PROBLEMA:**
```python
# Linha 305-312 (LÓGICA QUEBRADA)
if not p_run.get('marketing_habilitado', True):
    budget_mkt_desejado = 0.0
elif mes == 0:
    budget_mkt_desejado = p_run['marketing_fixo_mensal']
else:
    budget_calc = dados['receita_bruta'][mes - 1] * p_run['marketing_perc_receita']
    budget_mkt_desejado = np.clip(budget_calc, p_run['marketing_fixo_mensal'], p_run['marketing_teto'])
```

**FALHA:** No Cenário 2, você configurou:
- `marketing_fixo_mensal = 0.0`
- `marketing_perc_receita = 0.0`

Mas a lógica **NÃO ZERA** o budget porque:
1. `marketing_habilitado` está `True` por padrão (linha 305)
2. No M0, ele usa `marketing_fixo_mensal` (linha 307)
3. Nos meses seguintes, `np.clip()` usa `marketing_fixo_mensal` como **PISO**, não TETO (linha 312)

**RESULTADO:** Mesmo com R$0 configurado, a lógica de `clip()` pode pegar valores de `receita_bruta * perc` ou defaults internos.

**CORREÇÃO:**
```python
# ANTES DE QUALQUER CÁLCULO (linha 305)
mkt_hab = p_run.get('marketing_habilitado', True)
mkt_fixo = p_run.get('marketing_fixo_mensal', 0)

# Se fixo é zero E habilitado é False, FORÇA ZERO TOTAL
if mkt_fixo <= 1.0 or not mkt_hab:
    budget_mkt_desejado = 0.0
    p_run['marketing_perc_receita'] = 0.0  # Zera também % receita
    p_run['marketing_teto'] = 0.0
elif mes == 0:
    budget_mkt_desejado = mkt_fixo
else:
    # ... resto da lógica
```

---

### **BUG #2: LTV/CAC = "nanx" vs "999.00x" vs "0.0x" (4 valores para mesma métrica)**
**Localização:** Motor linha 1095-1120 + Página 1 linha 250-300

**PROBLEMA:** Tratamento inconsistente de divisão por zero:

1. **Motor (linha 1110):**
```python
if not np.isnan(ltv_val) and not np.isnan(dados['cac_blended'][mes]) and dados['cac_blended'][mes] > 0:
    dados['ltv_cac'][mes] = ltv_val / dados['cac_blended'][mes]
else:
    dados['ltv_cac'][mes] = np.nan  # RETORNA NAN
```

2. **Tabela Master (Página 1, linha 270):**
```python
v36_str = f'{v36:.2f}x'  # FORMATA NAN COMO "nanx"
```

3. **Insight Texto (linha 620):**
```python
# Hardcoded no texto
"Cada R$ 1 investido retorna R$ 999.00"  # TEXTO FIXO (HARDCODED!)
```

4. **Monte Carlo (celula_5D, linha 180):**
```python
if result['cac_medio'] == 0:
    if result['ltv_medio'] > 0:
        result['ltv_cac'] = 10000.0 # Valor simbólico
```

**RESULTADO:** 4 caminhos de código diferentes retornam 4 valores diferentes.

**CORREÇÃO ÚNICA:**
```python
# MOTOR (linha 1110) - Standardizar tratamento
if dados['cac_blended'][mes] == 0:
    if ltv_val > 0:
        dados['ltv_cac'][mes] = 10000.0  # Símbolo de infinito
    else:
        dados['ltv_cac'][mes] = 0.0  # Sem LTV e sem CAC = modelo quebrado
elif not np.isnan(ltv_val):
    dados['ltv_cac'][mes] = ltv_val / dados['cac_blended'][mes]
else:
    dados['ltv_cac'][mes] = 0.0  # Fallback conservador

# VISUALIZAÇÃO (Página 1) - Detectar infinito
if pd.isna(v36) or v36 >= 9999:
    v36_str = "∞ (Orgânico)"
elif v36 == 0:
    v36_str = "0.0x (Inviável)"
else:
    v36_str = f"{v36:.2f}x"
```

---

### **BUG #3: Runway Negativo (-22.7m) - Matematicamente Impossível**
**Localização:** Motor linha 1175-1190

**PROBLEMA:**
```python
# Linha 1180
if despesa_operacional_mensal > 0:
    if caixa_atual <= THRESHOLD_QUEBRA:
        dados['runway_meses'][mes] = 0.0
    else:
        dados['runway_meses'][mes] = caixa_atual / despesa_operacional_mensal  # PERMITE NEGATIVO!
```

**FALHA:** Se `caixa_atual = -1.7M` e `despesas = 72k`, resultado = **-22.7 meses** (absurdo).

**CORREÇÃO:**
```python
if despesa_operacional_mensal > 0:
    runway_calculado = caixa_atual / despesa_operacional_mensal
    
    # NUNCA permitir runway negativo
    if caixa_atual <= THRESHOLD_QUEBRA:
        dados['runway_meses'][mes] = 0.0
    else:
        dados['runway_meses'][mes] = max(0.0, runway_calculado)
else:
    dados['runway_meses'][mes] = 999.0  # Sem custos
```

---

### **BUG #4: Payback = Runway (Copy-Paste Error)**
**Localização:** Tabela Master (Página 1, linha 280)

**PROBLEMA:**
```python
# Linha 280 - Formatação Payback/Runway usa MESMA VARIÁVEL
v36_str = f'{v36:.1f}m'  # Runway
...
v36_str = f'{v36:.1f}m'  # Payback (MESMO CÓDIGO!)
```

**RESULTADO:** Payback mostra `-22.7m` (copiou valor do Runway quebrado).

**CORREÇÃO:**
```python
elif coluna == 'payback_meses':
    # Payback NUNCA pode ser negativo (ou é 0, ou é >0)
    if v36 < 0 or pd.isna(v36):
        v36_str = "N/A"
    else:
        v36_str = f"{v36:.1f}m"
```

---

## 🟡 BUGS MÉDIOS (Comprometem Confiança)

### **BUG #5: Gap Negativo com Texto Contraditório**
**Localização:** Página 1, linha 680

**PROBLEMA:**
```python
gap_pct = ((mrr_real - mrr_ideal) / mrr_ideal * 100)
# Se Real > Ideal, gap é NEGATIVO
# Mas texto diz: "Potencial de R$ -90k NÃO CAPTURADO" (double negative)
```

**CORREÇÃO:**
```python
if gap < 0:
    texto = f"Cenário Real SUPEROU meta em {formatar_moeda(abs(gap))}"
else:
    texto = f"Potencial de {formatar_moeda(gap)} não capturado"
```

---

### **BUG #6: Milestones Temporais Quebrados**
**Localização:** Página 1, linha 450-480

**PROBLEMA:**
```python
# Milestone: R$ 10k MRR
# MRR_M1 = R$ 9k (já maior que R$ 5k e R$ 1k)
# Mas código detecta R$ 10k só no M2
```

**CAUSA:** Função `encontrar_mes_milestone()` usa `>=` mas não valida se M0 já passou.

**CORREÇÃO:**
```python
def encontrar_mes_milestone(df, coluna, valor):
    # Se M0 já é maior, retorna M0 (não M1)
    if df.iloc[0][coluna] >= valor:
        return 0  # Já iniciou com meta batida
    
    mask = df[coluna] >= valor
    if mask.any():
        return int(df[mask].iloc[0]['mes'])
    return None
```

---

### **BUG #7: Monte Carlo - Prob. Quebra 36% quando Caixa Final = -R$1.6M**
**Localização:** `celula_5D_monte_carlo.py` linha 200-220

**PROBLEMA:** Simulação estocástica **NÃO VALIDA** cenário determinístico:
```python
# Linha 215
metricas['quebrou'] = bool(df_m['caixa'].min() < THRESHOLD_QUEBRA)
# Mas isso olha TODA a série, não o final
```

**RESULTADO:** Se caixa final é -R$1.6M, mas em algum mês ficou >0, `quebrou = False`.

**CORREÇÃO:**
```python
# Validar FINAL + SÉRIE
caixa_min_serie = df_m['caixa'].min()
caixa_final = df_m['caixa'].iloc[-1]

quebrou_serie = caixa_min_serie < THRESHOLD_QUEBRA
quebrou_final = caixa_final < THRESHOLD_QUEBRA

metricas['quebrou'] = bool(quebrou_serie or quebrou_final)  # OR lógico
```

---

## 🟢 BUGS MENORES (Polimento)

### **BUG #8: ARPU não Reage ao Preço Alto**
**Localização:** Motor linha 580-600

**STATUS:** ✅ **NÃO É BUG** - Código está correto:
```python
dados['receita_trader'][mes] = base_trader * p_run['preco_trader']
mrr = dados['receita_lite'][mes] + dados['receita_trader'][mes] + dados['receita_pro'][mes]
dados['arpu'][mes] = mrr / usuarios_ativos
```

**VALIDAÇÃO:** No Cenário 2:
- M36: R$30.5k MRR / 20 usuários = **R$1.525 ARPU** ✅ (correto!)
- Preço Trader = R$1.500 ✅

**CONCLUSÃO:** ARPU **reagiu corretamente**. O bug estava na **percepção visual** da tabela.

---

### **BUG #9: Margem Bruta 45% sem Explicação**
**Localização:** Visualização (faltando narrativa)

**CAUSA:** COGS subiram de 5.5% → 40%, mas relatório não explica.

**CORREÇÃO:** Adicionar insight automático:
```python
if dados['margem_bruta_pct'][mes] < 70:
    alertas.append({
        'tipo': 'margem_baixa',
        'valor': dados['margem_bruta_pct'][mes],
        'causa': f"COGS altos: {dados['total_cogs'][mes]/dados['receita_bruta'][mes]*100:.1f}%",
        'mensagem': "Revisar estrutura de custos variáveis"
    })
```

---

## 🎯 SOBRE O STRESS TEST (High Ticket)

### **PREMISSAS DO CENÁRIO 2 - ANÁLISE CRÍTICA**

| Premissa | Valor | Realismo | Veredicto |
|---|---|---|---|
| Preço Trader | R$ 1.500 | ✅ Alto mas viável (Tiers premium SaaS) | **OK** |
| Marketing | R$ 0 | ⚠️ Possível mas extremo (growth 100% orgânico) | **STRESS OK** |
| COGS Trader | R$ 600 (40% receita) | 🔴 Margem 60% é BAIXA para SaaS | **IRREAL** |
| RH Fixo | R$ 60k/mês | 🔴 Com receita R$30k = 200% custos | **INSUSTENTÁVEL** |
| Usuários Iniciais | 5 | ✅ Bootstrap realista | **OK** |

### **RECOMENDAÇÃO DE STRESS:**
```python
# CENÁRIO STRESS REALISTA
premissas_stress = {
    'preco_trader': 1500,          # ✅ High ticket
    'marketing_fixo_mensal': 0,    # ✅ Orgânico puro
    'custo_ia_trader': 200,        # ✅ Margem 87% (SaaS típico)
    'salario_fundador': 0,         # ✅ Fundador sem salário (bootstrap real)
    'trigger_dev': 50,             # ✅ Contrata só quando tem caixa
    'churn_inicial': 0.20,         # ✅ Stress: churn alto
}
```

---

## 📊 PRIORIZAÇÃO DE CORREÇÕES

| Prioridade | Bug | Impacto | Esforço | Ordem |
|---|---|---|---|---|
| 🔥 P0 | BUG #1 (Ghost Marketing) | 🔴 ALTO | 🟢 Baixo | **1º** |
| 🔥 P0 | BUG #2 (LTV/CAC inconsistente) | 🔴 ALTO | 🟡 Médio | **2º** |
| 🔥 P0 | BUG #3 (Runway negativo) | 🔴 ALTO | 🟢 Baixo | **3º** |
| ⚡ P1 | BUG #7 (Monte Carlo prob.) | 🟡 MÉDIO | 🟡 Médio | **4º** |
| 📝 P2 | BUG #5 (Gap negativo) | 🟢 BAIXO | 🟢 Baixo | **5º** |

---

## 🛠️ PRÓXIMOS PASSOS

**VOCÊ PRECISA CORRIGIR:**
1. ✅ **Motor Financeiro** (`celula_4_motor.py`) - Bugs #1, #2, #3, #7
2. ✅ **Visualizações** (`pagina_1_cockpit.py`) - Bugs #4, #5, #6

**EU PRECISO VER:**
- ❌ Não preciso dos outros Tiers agora
- ✅ Me confirme que essas correções fazem sentido
- ✅ Depois aplique no código e rode Cenário 2 novamente

**PERGUNTA FINAL:** Quer que eu **escreva os patches** (código corrigido) ou você prefere aplicar manualmente baseado nas explicações?