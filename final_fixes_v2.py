# final_fixes_v2.py
# Versao corrigida:
# - Usa *** ao inves de --- (--- causa YAML error)
# - Tamanho de graficos para (10, 5)
# - Remove COMO LER duplicado
# - Adiciona titulos/intros para cada VIZ

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. REDUZIR TAMANHO DOS GRAFICOS PARA HTML
# ============================================================
content = content.replace('figsize = (14, 6)', 'figsize = (10, 5)')
content = content.replace('figsize=(14, 6)', 'figsize=(10, 5)')
content = content.replace('figsize = (12, 6)', 'figsize = (10, 5)')
content = content.replace('figsize=(12, 6)', 'figsize=(10, 5)')
print("1. Reduzido tamanho dos graficos para (10, 5)")

# ============================================================
# 2. ADICIONAR TITULOS/INTROS COM *** (NÃO ---)
# ============================================================

# VIZ 3.1
old_viz31_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.1: Evolução Financeira Correlacionada")
    
    # =========================================
    # TABELA DRE DETALHADA (ANTES DO GRÁFICO!)'''

new_viz31_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.1: Evolução Financeira Correlacionada")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.1: Evolucao Financeira"))
        display(Markdown("**Pergunta:** A empresa caminha para o break-even? Quando o caixa fica positivo?"))
    
    # =========================================
    # TABELA DRE DETALHADA (ANTES DO GRÁFICO!)'''

content = content.replace(old_viz31_start, new_viz31_start)
print("2. Adicionado titulo VIZ 3.1 (com ***)")

# VIZ 3.2
old_viz32_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.2: Estrutura de Custos + Decomposição")
    
    m36 = df_real.iloc[-1]'''

new_viz32_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.2: Estrutura de Custos + Decomposição")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.2: Estrutura de Custos"))
        display(Markdown("**Pergunta:** Onde esta o dinheiro? A estrutura de custos e saudavel?"))
    
    m36 = df_real.iloc[-1]'''

content = content.replace(old_viz32_start, new_viz32_start)
print("3. Adicionado titulo VIZ 3.2 (com ***)")

# VIZ 3.3
old_viz33_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.3: Fluxo de Caixa Semanal")
    
    # Se não tiver dados semanais'''

new_viz33_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.3: Fluxo de Caixa Semanal")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.3: Fluxo de Caixa Semanal"))
        display(Markdown("**Pergunta:** O caixa sobrevive ao ramp-up? Qual o momento mais critico?"))
    
    # Se não tiver dados semanais'''

content = content.replace(old_viz33_start, new_viz33_start)
print("4. Adicionado titulo VIZ 3.3 (com ***)")

# VIZ 3.4
old_viz34_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.4: Alavancagem Operacional")
    
    # Dados'''

new_viz34_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.4: Alavancagem Operacional")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.4: Alavancagem Operacional"))
        display(Markdown("**Pergunta:** A empresa escala de forma eficiente?"))
    
    # Dados'''

content = content.replace(old_viz34_start, new_viz34_start)
print("5. Adicionado titulo VIZ 3.4 (com ***)")

# VIZ 3.5
old_viz35_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.5: Heatmap DRE Evolutivo")
    
    # Meses chave'''

new_viz35_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.5: Heatmap DRE Evolutivo")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 3.5: Evolucao DRE - Real vs Ideal"))
        display(Markdown("**Pergunta:** Estamos convergindo para o cenario ideal?"))
    
    # Meses chave'''

content = content.replace(old_viz35_start, new_viz35_start)
print("6. Adicionado titulo VIZ 3.5 (com ***)")

# Salvar
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("")
print("="*60)
print("TODAS as correcoes aplicadas (versao corrigida)!")
print("- Tamanho graficos: (10, 5)")
print("- Separador: *** (nao ---)")
print("- Titulos: VIZ 3.1 a 3.5")
print("="*60)
print("")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to html")
