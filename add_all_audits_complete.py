# add_all_audits_complete.py
# Adiciona auditorias para VIZ 3.2, 3.3, 3.4 e 3.5
# VIZ 3.1 ja foi adicionado anteriormente

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Auditorias para cada VIZ (usando f-string para que {{ vire {)
audit_32 = '''        # Auditoria VIZ 3.2
        audit_md = f"""
::: {{{{.callout-note collapse="true"}}}}
## Auditoria VIZ 3.2
**Fonte:** df_real_m.iloc[-1] (M36 da Celula 5A)

**Formulas:**
- Margem Bruta = (Receita Liquida - COGS) / Receita Bruta x 100
- OPEX pct = Total OPEX / Receita Bruta x 100
- Benchmarks: Margem maior 80%, OPEX menor 50%, EBITDA maior 20%
:::
"""
        display(Markdown(audit_md))
'''

audit_33 = '''        # Auditoria VIZ 3.3
        audit_md = f"""
::: {{{{.callout-note collapse="true"}}}}
## Auditoria VIZ 3.3
**Fonte:** df_real_s (granularidade semanal, Celula 5A)

**Formulas:**
- Runway = Caixa / Despesas Semanais
- Vale de Caixa = min(Caixa) nas 24 semanas
- Reserva = Media Saidas x 4 semanas
:::
"""
        display(Markdown(audit_md))
'''

audit_34 = '''        # Auditoria VIZ 3.4
        audit_md = f"""
::: {{{{.callout-note collapse="true"}}}}
## Auditoria VIZ 3.4
**Fonte:** df_real_m, df_ideal_m (Celulas 5A/5B)

**Formulas:**
- Alavancagem = Delta EBITDA / Delta Receita
- Delta = (Valor M36 - Valor M12) / Valor M12 x 100
- Interpretacao: Alavancagem maior que 1 = Modelo escalavel
:::
"""
        display(Markdown(audit_md))
'''

audit_35 = '''        # Auditoria VIZ 3.5
        audit_md = f"""
::: {{{{.callout-note collapse="true"}}}}
## Auditoria VIZ 3.5
**Fonte:** df_real_m vs df_ideal_m (Celulas 5A e 5B)

**Formulas:**
- Delta = (Real - Ideal) / |Ideal| x 100
- Verde = Real superando Ideal
- Vermelho = Real abaixo do Ideal
:::
"""
        display(Markdown(audit_md))
'''

# Procurar as linhas especificas e inserir auditorias
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    
    # VIZ 3.2: apos "display(Markdown(insight_md))" da Estrutura de Custos
    # Linha 510 contem isso, e a proxima linha (511) e "    else:"
    if i == 509:  # Apos linha 510 (indice 509)
        new_lines.append(audit_32)
        print(f"Adicionado audit 3.2 apos linha {i+1}")
    
    # VIZ 3.3: apos "display(Markdown(insight_md))" da Liquidez no Ramp-up
    # Linha 685
    if i == 684:  # Apos linha 685
        new_lines.append(audit_33)
        print(f"Adicionado audit 3.3 apos linha {i+1}")
    
    # VIZ 3.4: apos "display(Markdown(insight_md))" da Escalabilidade
    # Linha 819
    if i == 818:  # Apos linha 819
        new_lines.append(audit_34)
        print(f"Adicionado audit 3.4 apos linha {i+1}")
    
    # VIZ 3.5: apos "display(Markdown(insight_md))" da Convergencia
    # Linha 1000
    if i == 999:  # Apos linha 1000
        new_lines.append(audit_35)
        print(f"Adicionado audit 3.5 apos linha {i+1}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("")
print("Auditorias VIZ 3.2 a 3.5 adicionadas!")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
