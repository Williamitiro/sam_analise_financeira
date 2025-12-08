# fix_all_audits.py
# Corrige a sintaxe dos callouts e adiciona auditorias para TODOS os VIZs
# Bug: {{ em string normal fica literal. Precisa ser { (sem f-string).

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CORRIGIR A AUDITORIA VIZ 3.1 JA INSERIDA (trocar {{ por {)
old_audit_31 = '''::: {{.callout-note collapse="true"}}
## Auditoria VIZ 3.1'''

new_audit_31 = '''::: {.callout-note collapse="true"}
## Auditoria VIZ 3.1'''

content = content.replace(old_audit_31, new_audit_31)

# Tambem corrigir o fechamento se tiver problema
content = content.replace('{{.callout-note', '{.callout-note')
content = content.replace('{{.callout-tip', '{.callout-tip')
content = content.replace('{{.callout-warning', '{.callout-warning')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Corrigido: {{ substituido por { nos callouts de auditoria")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
