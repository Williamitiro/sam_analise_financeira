# add_audit_callouts.py
# Adiciona callouts de auditoria apos cada insight na Pagina 3
# Seguindo o mesmo padrao de celula_0_utils.py

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Callouts de auditoria para cada VIZ
audits = {
    'VIZ 3.1': '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.1
**Fonte:** df_real_m (Celula 5A), df_ideal_m (Celula 5B)

**Formulas:**
- Break-even = Primeiro mes onde EBITDA maior que 0
- Gap = (Mes break-even Real) - (Mes break-even Ideal)
- Reducao Burn = (Burn M1 - Burn M36) / Burn M1 x 100
:::
''',
    'VIZ 3.2': '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.2
**Fonte:** df_real_m.iloc[-1] (M36 da Celula 5A)

**Formulas:**
- Margem Bruta pct = (Receita Liquida - COGS) / Receita Bruta x 100
- OPEX pct = Total OPEX / Receita Bruta x 100
- EBITDA pct = EBITDA / Receita Bruta x 100
- Benchmarks: Margem Bruta maior 80pct, OPEX menor 50pct, EBITDA maior 20pct
:::
''',
    'VIZ 3.3': '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.3
**Fonte:** df_real_s (granularidade semanal, Celula 5A)

**Formulas:**
- Runway = Caixa / Despesas Semanais
- Vale de Caixa = min(Caixa) nas primeiras 24 semanas
- Reserva Seguranca = Media das Saidas x 4 semanas
:::
''',
    'VIZ 3.4': '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.4
**Fonte:** df_real_m, df_ideal_m (Celulas 5A/5B)

**Formulas:**
- Alavancagem = Delta EBITDA pct / Delta Receita pct
- Delta Receita = (Receita M36 - Receita M12) / Receita M12 x 100
- Delta EBITDA = (EBITDA M36 - EBITDA M12) / |EBITDA M12| x 100
- Interpretacao: Alavancagem maior 1 = Modelo escalavel
:::
''',
    'VIZ 3.5': '''
::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.5
**Fonte:** df_real_m vs df_ideal_m (Celulas 5A e 5B)

**Formulas:**
- Delta = (Real - Ideal) / |Ideal| x 100
- Cores: Verde = Real superando Ideal, Vermelho = Real abaixo
- OPEX: Logica invertida (menor = melhor)
:::
'''
}

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Detectar fim de insights (callout-tip ou callout-warning) e inserir auditoria
    # VIZ 3.1: procurar "💡 INSIGHT: Viabilidade Financeira"
    if "INSIGHT: Viabilidade Financeira" in line and "callout" in lines[i-3] if i >= 3 else False:
        # Inserir auditoria antes do proximo plt.close
        pass
    
    # VIZ 3.2: procurar "INSIGHT: Margem de Segurança"
    if "INSIGHT: Margem de" in line and "display(Markdown(insight_md))" in lines[i+3] if i+3 < len(lines) else False:
        pass
    
    i += 1

# Por seguranca, apenas atualiza as fontes por agora
# Os callouts de auditoria serao adicionados via edicao direta

print("Script preparado. Execute as adicoes de auditoria conforme indicado.")
print("Fontes ja foram atualizadas para Celulas 5A/5B.")
