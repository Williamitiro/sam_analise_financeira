# final_add_audits.py
# Adiciona callouts de auditoria APOS cada insight na Pagina 3

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Auditorias para cada VIZ (formato Quarto com escape {{}})
audit_3_1 = '''        # Auditoria VIZ 3.1
        audit_md = """
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.1
**Fonte:** df_real_m (Celula 5A), df_ideal_m (Celula 5B)

**Formulas:**
- Break-even = Primeiro mes onde EBITDA maior que 0
- Gap = Mes break-even Real - Mes break-even Ideal
- Reducao Burn = (Burn M1 - Burn M36) / Burn M1 x 100
:::
"""
        display(Markdown(audit_md))
'''

audit_3_2 = '''        # Auditoria VIZ 3.2
        audit_md = """
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.2
**Fonte:** df_real_m.iloc[-1] (M36 da Celula 5A)

**Formulas:**
- Margem Bruta = (Receita Liquida - COGS) / Receita Bruta x 100
- OPEX = Total OPEX / Receita Bruta x 100
- Benchmarks SaaS: Margem maior 80%, OPEX menor 50%, EBITDA maior 20%
:::
"""
        display(Markdown(audit_md))
'''

audit_3_3 = '''        # Auditoria VIZ 3.3
        audit_md = """
::: {{.callout-note collapse="true"}}
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

audit_3_4 = '''        # Auditoria VIZ 3.4
        audit_md = """
::: {{.callout-note collapse="true"}}
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

audit_3_5 = '''        # Auditoria VIZ 3.5
        audit_md = """
::: {{.callout-note collapse="true"}}
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

new_lines = []
inserted_count = 0

for i, line in enumerate(lines):
    new_lines.append(line)
    
    # VIZ 3.1: apos "display(Markdown(insight_md))" do insight de Viabilidade Financeira
    if '💡 INSIGHT: Viabilidade Financeira' in line and inserted_count == 0:
        # Procurar o display(Markdown(insight_md)) nas proximas linhas
        pass
    
    # Detectar o padrao: display(Markdown(insight_md)) seguido de else:
    if 'display(Markdown(insight_md))' in line:
        # Verificar se a proxima linha e "else:"
        if i + 1 < len(lines) and 'else:' in lines[i + 1]:
            # Determinar qual auditoria inserir baseado no contexto
            # Verificar linhas anteriores para identificar qual VIZ
            context = ''.join(lines[max(0, i-20):i])
            
            if 'Viabilidade Financeira' in context and inserted_count == 0:
                new_lines.append(audit_3_1)
                inserted_count += 1
                print(f"Inserted audit 3.1 after line {i+1}")
            elif 'Margem de' in context and inserted_count == 1:
                new_lines.append(audit_3_2)
                inserted_count += 1
                print(f"Inserted audit 3.2 after line {i+1}")
            elif 'Liquidez no Ramp-up' in context and inserted_count == 2:
                new_lines.append(audit_3_3)
                inserted_count += 1
                print(f"Inserted audit 3.3 after line {i+1}")
            elif 'Escalabilidade' in context and inserted_count == 3:
                new_lines.append(audit_3_4)
                inserted_count += 1
                print(f"Inserted audit 3.4 after line {i+1}")
            elif 'Gap DRE' in context and inserted_count == 4:
                new_lines.append(audit_3_5)
                inserted_count += 1
                print(f"Inserted audit 3.5 after line {i+1}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nTotal de auditorias inseridas: {inserted_count}")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
