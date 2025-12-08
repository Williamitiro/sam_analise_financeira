# fix_audits_smart.py
# Corrige APENAS as auditorias (strings normais) sem quebrar f-strings existentes
# 
# O problema:
# - f-strings usam {{ para escapar e virar {  -> FUNCIONA
# - strings normais usam {{ e fica literal   -> BUG
#
# Solucao: Mudar auditorias de string normal para f-string

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# CORRECAO: Mudar audit_md de string para f-string (adicionar f antes das aspas)
# Procurar o padrao: audit_md = """ e mudar para audit_md = f"""

old_pattern = '        audit_md = """'
new_pattern = '        audit_md = f"""'

content = content.replace(old_pattern, new_pattern)

# Verificar quantas substituicoes foram feitas
count = content.count('audit_md = f"""')
print(f"Encontradas {count} auditorias convertidas para f-string")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Corrigido: audit_md convertido para f-string")
print("Agora {{ sera interpretado como { pelo Python")
print("")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
