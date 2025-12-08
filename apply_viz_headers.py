# apply_viz_headers.py
# Script para adicionar VIZ headers ao PAGINA_3_FINANCEIRO.py
# Execute: python apply_viz_headers.py

import os

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar e modificar VIZ 3.1 (linha ~77-79)
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # VIZ 3.1 - após o print
    if 'VIZ 3.1: Evolução Financeira Correlacionada' in line and 'print' in line:
        # Próxima linha deve ser espaço vazio
        i += 1
        if i < len(lines):
            new_lines.append('    else:\n')
            new_lines.append('        display(Markdown("---"))\n')
            new_lines.append('        display(Markdown("## VIZ 3.1: Evolucao Financeira"))\n')
            new_lines.append('        display(Markdown("**Pergunta:** A empresa caminha para o break-even?"))\n')
            new_lines.append(lines[i])  # linha original (espaço vazio)
    
    # VIZ 3.2 - após o print
    elif 'VIZ 3.2: Estrutura de Custos' in line and 'print' in line:
        i += 1
        if i < len(lines):
            new_lines.append('    else:\n')
            new_lines.append('        display(Markdown("---"))\n')
            new_lines.append('        display(Markdown("## VIZ 3.2: Estrutura de Custos"))\n')
            new_lines.append('        display(Markdown("**Pergunta:** Onde esta o dinheiro? A estrutura e saudavel?"))\n')
            new_lines.append(lines[i])
    
    # VIZ 3.3 - após o print
    elif 'VIZ 3.3: Fluxo de Caixa Semanal' in line and 'print' in line:
        i += 1
        if i < len(lines):
            new_lines.append('    else:\n')
            new_lines.append('        display(Markdown("---"))\n')
            new_lines.append('        display(Markdown("## VIZ 3.3: Fluxo de Caixa Semanal"))\n')
            new_lines.append('        display(Markdown("**Pergunta:** O caixa sobrevive ao ramp-up?"))\n')
            new_lines.append(lines[i])
    
    # VIZ 3.4 - após o print
    elif 'VIZ 3.4: Alavancagem Operacional' in line and 'print' in line:
        i += 1
        if i < len(lines):
            new_lines.append('    else:\n')
            new_lines.append('        display(Markdown("---"))\n')
            new_lines.append('        display(Markdown("## VIZ 3.4: Alavancagem Operacional"))\n')
            new_lines.append('        display(Markdown("**Pergunta:** A empresa escala de forma eficiente?"))\n')
            new_lines.append('        display(Markdown(""))\n')
            new_lines.append('        display(Markdown("**O QUE E ALAVANCAGEM?** Mede quanto o lucro cresce para cada 1% de crescimento de receita."))\n')
            new_lines.append(lines[i])
    
    # VIZ 3.5 - após o print  
    elif 'VIZ 3.5: Heatmap DRE Evolutivo' in line and 'print' in line:
        i += 1
        if i < len(lines):
            new_lines.append('    else:\n')
            new_lines.append('        display(Markdown("---"))\n')
            new_lines.append('        display(Markdown("## VIZ 3.5: Evolucao DRE - Real vs Ideal"))\n')
            new_lines.append('        display(Markdown("**Pergunta:** Estamos convergindo para o cenario ideal?"))\n')
            new_lines.append(lines[i])
    
    i += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"VIZ headers adicionados! Total de linhas: {len(new_lines)}")
