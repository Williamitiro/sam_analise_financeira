# final_fixes.py
# Corrige:
# 1. Remove COMO LER duplicado do VIZ 3.3
# 2. Reduz tamanho dos graficos de (14, 6) para (10, 5) para HTML
# 3. Adiciona titulos/intros antes de cada VIZ

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. REMOVER COMO LER DUPLICADO DO VIZ 3.3
# ============================================================
old_como_ler_33_simples = '''    if report_mode:
        plt.show()
        
        # COMO LER (Legenda obrigatória)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Linha Azul (Eixo Esquerdo):** Saldo de caixa semanal
2. **Linha Vermelha Tracejada:** Limite crítico (2 semanas de despesas)
3. **Linha Verde Pontilhada (Eixo Direito):** Runway em semanas
4. **Ponto Vermelho:** Vale de caixa (momento mais crítico)
5. **Linha Amarela Horizontal:** Meta mínima de 4 semanas de runway
6. **Regra de Sucesso:** Manter caixa sempre acima da linha vermelha
"""
        display(Markdown(como_ler))
    else:
        plt.show()'''

new_como_ler_33_simples = '''    if report_mode:
        plt.show()
        # COMO LER movido para apos a tabela (versao completa)
    else:
        plt.show()'''

content = content.replace(old_como_ler_33_simples, new_como_ler_33_simples)
print("1. Removido COMO LER duplicado do VIZ 3.3")

# ============================================================
# 2. REDUZIR TAMANHO DOS GRAFICOS PARA HTML
# ============================================================
# Trocar (14, 6) por (10, 5) - mais compacto para HTML
content = content.replace('figsize = (14, 6)', 'figsize = (10, 5)')
content = content.replace('figsize=(14, 6)', 'figsize=(10, 5)')
content = content.replace('figsize = (12, 6)', 'figsize = (10, 5)')
content = content.replace('figsize=(12, 6)', 'figsize=(10, 5)')
print("2. Reduzido tamanho dos graficos para (10, 5)")

# ============================================================
# 3. ADICIONAR TITULOS/INTROS ANTES DE CADA VIZ
# ============================================================
# VIZ 3.1: adicionar titulo antes do grafico
old_viz31_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.1: Evolução Financeira Correlacionada")
    
    # =========================================
    # TABELA DRE DETALHADA (ANTES DO GRÁFICO!)'''

new_viz31_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.1: Evolução Financeira Correlacionada")
    else:
        # Titulo e intro para report_mode
        display(Markdown("---"))
        display(Markdown("## VIZ 3.1: Evolucao Financeira"))
        display(Markdown("**Pergunta de Negocio:** A empresa caminha para o break-even? Quando o caixa fica positivo?"))
        display(Markdown(""))
    
    # =========================================
    # TABELA DRE DETALHADA (ANTES DO GRÁFICO!)'''

content = content.replace(old_viz31_start, new_viz31_start)
print("3. Adicionado titulo/intro VIZ 3.1")

# VIZ 3.2
old_viz32_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.2: Estrutura de Custos + Decomposição")
    
    m36 = df_real.iloc[-1]'''

new_viz32_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.2: Estrutura de Custos + Decomposição")
    else:
        display(Markdown("---"))
        display(Markdown("## VIZ 3.2: Estrutura de Custos"))
        display(Markdown("**Pergunta de Negocio:** Onde esta o dinheiro? A estrutura de custos e saudavel para SaaS?"))
        display(Markdown(""))
    
    m36 = df_real.iloc[-1]'''

content = content.replace(old_viz32_start, new_viz32_start)
print("4. Adicionado titulo/intro VIZ 3.2")

# VIZ 3.3
old_viz33_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.3: Fluxo de Caixa Semanal")
    
    # Se não tiver dados semanais'''

new_viz33_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.3: Fluxo de Caixa Semanal")
    else:
        display(Markdown("---"))
        display(Markdown("## VIZ 3.3: Fluxo de Caixa Semanal"))
        display(Markdown("**Pergunta de Negocio:** O caixa sobrevive ao ramp-up? Qual o momento mais critico?"))
        display(Markdown(""))
    
    # Se não tiver dados semanais'''

content = content.replace(old_viz33_start, new_viz33_start)
print("5. Adicionado titulo/intro VIZ 3.3")

# VIZ 3.4
old_viz34_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.4: Alavancagem Operacional")
    
    # Dados'''

new_viz34_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.4: Alavancagem Operacional")
    else:
        display(Markdown("---"))
        display(Markdown("## VIZ 3.4: Alavancagem Operacional"))
        display(Markdown("**Pergunta de Negocio:** A empresa escala de forma eficiente? O lucro cresce mais rapido que a receita?"))
        display(Markdown(""))
    
    # Dados'''

content = content.replace(old_viz34_start, new_viz34_start)
print("6. Adicionado titulo/intro VIZ 3.4")

# VIZ 3.5
old_viz35_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.5: Heatmap DRE Evolutivo")
    
    # Meses chave'''

new_viz35_start = '''    if not report_mode:
        print("\\n🔹 VIZ 3.5: Heatmap DRE Evolutivo")
    else:
        display(Markdown("---"))
        display(Markdown("## VIZ 3.5: Evolucao DRE - Real vs Ideal"))
        display(Markdown("**Pergunta de Negocio:** Estamos convergindo para o cenario ideal? Quais metricas estao mais distantes?"))
        display(Markdown(""))
    
    # Meses chave'''

content = content.replace(old_viz35_start, new_viz35_start)
print("7. Adicionado titulo/intro VIZ 3.5")

# Salvar
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("")
print("="*60)
print("TODAS as correcoes aplicadas!")
print("="*60)
print("")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to html")
