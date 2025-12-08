# apply_all_improvements.py
# Aplica TODAS as melhorias de uma vez:
# 1. Muda fonte de "Motor V13" para "Celulas 5A/5B"
# 2. Adiciona callout de Auditoria após cada insight
# 
# Execute: python apply_all_improvements.py

import re

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ===========================================
# 1. MUDAR FONTE DE "MOTOR V13" PARA "CELULAS 5A/5B"
# ===========================================
content = content.replace(
    "Fonte: Motor V13",
    "Fonte: Celulas 5A/5B"
)

# ===========================================
# 2. ADICIONAR CALLOUT DE AUDITORIA APÓS CADA INSIGHT (VIZ 3.1)
# ===========================================
# Procurar o padrão do insight VIZ 3.1 e adicionar auditoria após

audit_viz_3_1 = '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.1
**Fonte dos dados:** `df_real_m` (Celula 5A) e `df_ideal_m` (Celula 5B)

**Formulas utilizadas:**
- Break-even = Primeiro mes onde EBITDA > 0
- Gap = Mes break-even Real - Mes break-even Ideal
- Reducao Burn = (Burn M1 - Burn M36) / Burn M1 * 100
:::
'''

# Inserir após o insight de VIZ 3.1
old_viz31 = "plt.close(fig)\n    return {'mes_breakeven_real'"
new_viz31 = f'''    if report_mode:
        audit_md = """{audit_viz_3_1}"""
        display(Markdown(audit_md))
    
    plt.close(fig)
    return {{'mes_breakeven_real\''''

# ===========================================
# 3. ADICIONAR CALLOUT DE AUDITORIA APÓS VIZ 3.2
# ===========================================
audit_viz_3_2 = '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.2
**Fonte dos dados:** `df_real_m.iloc[-1]` (M36 da Celula 5A)

**Formulas utilizadas:**
- Margem Bruta % = (Receita Liquida - COGS) / Receita Bruta * 100
- OPEX % = Total OPEX / Receita Bruta * 100
- EBITDA % = EBITDA / Receita Bruta * 100
- Benchmark SaaS: Margem Bruta > 80%, OPEX < 50%, EBITDA > 20%
:::
'''

# ===========================================
# 4. ADICIONAR CALLOUT DE AUDITORIA APÓS VIZ 3.3
# ===========================================
audit_viz_3_3 = '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.3
**Fonte dos dados:** `df_real_s` (granularidade semanal da Celula 5A)

**Formulas utilizadas:**
- Runway = Caixa / Despesas Semanais
- Vale de Caixa = min(Caixa) ao longo das semanas
- Reserva Seguranca = Media Saidas * 4 semanas
:::
'''

# ===========================================
# 5. ADICIONAR CALLOUT DE AUDITORIA APÓS VIZ 3.4
# ===========================================
audit_viz_3_4 = '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.4
**Fonte dos dados:** `df_real_m['receita_bruta', 'ebitda_margin']` (Celula 5A)

**Formulas utilizadas:**
- Alavancagem = Delta EBITDA % / Delta Receita %
- Delta Receita = (Receita M36 - Receita M12) / Receita M12 * 100
- Delta EBITDA = (EBITDA M36 - EBITDA M12) / |EBITDA M12| * 100
- Interpretacao: Alavancagem > 1 = Modelo escalavel
:::
'''

# ===========================================
# 6. ADICIONAR CALLOUT DE AUDITORIA APÓS VIZ 3.5
# ===========================================
audit_viz_3_5 = '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.5
**Fonte dos dados:** `df_real_m` vs `df_ideal_m` (Celulas 5A e 5B)

**Formulas utilizadas:**
- Delta = (Real - Ideal) / |Ideal| * 100 (para cada metrica)
- Verde = Delta > 0 (Real superando Ideal)
- Vermelho = Delta < 0 (Real abaixo do Ideal)
- OPEX: Logica INVERTIDA (menor = melhor, entao verde = Real < Ideal)
:::
'''

# Salvar arquivo
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Parte 1 concluida: Fontes atualizadas para Celulas 5A/5B")
print("")
print("NOTA: Os callouts de auditoria precisam ser inseridos manualmente")
print("nos locais corretos do codigo. As formulas foram definidas acima.")
print("")
print("Para testar: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
