# fix_callouts_final.py
# Corrige os callouts VIZ 3.2-3.5 que usam {{{{ (errado) para {{ (correto)

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir {{{{ por {{ nos callouts de auditoria
# Note: isso é seguro porque {{{{ só aparece nas auditorias erradas
old = '{{{{.callout-note collapse="true"}}}}'
new = '{{.callout-note collapse="true"}}'

count = content.count(old)
content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Corrigidas {count} ocorrencias de {{{{{{{{...}}}}}}}} para {{{{...}}}}")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
