# fix_tier1_sources.py
# Corrige:
# 1. Remove FONTE_PADRAO estatico
# 2. Torna fontes dinamicas por visualizacao
# 3. Corrige labels cortados no topo (add_axes)

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_1_COCKPIT_V4.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. REMOVER FONTE_PADRAO ESTATICO
# ============================================================
old_fonte = '''# CONFIGURAÇÃO DE FONTE DE DADOS (DINÂMICA)
# O texto abaixo será usado em todos os rodapés de gráficos
FONTE_PADRAO = "Modelo Financeiro V10 | Cenários: Real (Bootstrap) vs Ideal (Benchmark)"'''

new_fonte = '''# FONTES DE DADOS DINAMICAS
# Cada visualizacao define sua propria fonte baseada nos dados usados
def gerar_fonte(dfs_usados):
    """Gera texto de fonte dinamico baseado nos DataFrames utilizados."""
    return f"Fonte: {' | '.join(dfs_usados)}"'''

content = content.replace(old_fonte, new_fonte)
print("1. Removido FONTE_PADRAO estatico, criado gerar_fonte() dinamico")

# ============================================================
# 2. SUBSTITUIR f"**Fonte:** {FONTE_PADRAO}" POR FONTE ESPECIFICA
# ============================================================

# Tabela Executiva - usa df_real_m e df_ideal_m
content = content.replace(
    'display(Markdown(f"**Fonte:** {FONTE_PADRAO}"))\n        display(Markdown("\\\\newpage"))\n    \n    return True',
    'display(Markdown("*Fonte: df_real_m (Simulacao Real) vs df_ideal_m (Benchmark)*"))\n        display(Markdown("\\\\newpage"))\n    \n    return True'
)

# KPI Cards - usa df_real_m
content = content.replace(
    'display(Markdown(f"**Fonte:** {FONTE_PADRAO}"))\n        display(Markdown("***"))',
    'display(Markdown("*Fonte: df_real_m (Simulacao Real) - Snapshot M36*"))\n        display(Markdown("***"))'
)

# Grafico Temporal - usa df_real_m e df_ideal_m
content = content.replace(
    'display(Markdown(f"**Fonte:** {FONTE_PADRAO}"))\n        display(Markdown("\\\\newpage"))\n    else:',
    'display(Markdown("*Fonte: df_real_m vs df_ideal_m - Projecao 36 meses*"))\n        display(Markdown("\\\\newpage"))\n    else:'
)

# Milestones - usa df_real_m e df_ideal_m
content = content.replace(
    'display(Markdown(f"**Fonte:** {FONTE_PADRAO}"))\n        display(Markdown("***"))\n    \n    return True',
    'display(Markdown("*Fonte: df_real_m vs df_ideal_m - Metas dinamicas*"))\n        display(Markdown("***"))\n    \n    return True'
)

# Eficiencia Marketing - usa df_real_m
content = content.replace(
    'display(Markdown(f"**Fonte:** {FONTE_PADRAO}"))\n        display(Markdown("\\\\newpage"))\n    else:\n        plt.show()\n    \n    return fig',
    'display(Markdown("*Fonte: df_real_m - gasto_marketing vs mrr*"))\n        display(Markdown("\\\\newpage"))\n    else:\n        plt.show()\n    \n    return fig'
)

print("2. Substituido FONTE_PADRAO por fontes especificas em cada visualizacao")

# ============================================================
# 3. CORRIGIR LABELS CORTADOS NO TOPO (add_axes)
# ============================================================
# O problema e que add_axes([0.1, 0.1, 0.85, 0.8]) usa 80% da altura
# Precisamos reduzir para dar espaco no topo

content = content.replace(
    "ax1 = fig.add_axes([0.1, 0.1, 0.85, 0.8])",
    "ax1 = fig.add_axes([0.1, 0.12, 0.85, 0.75])  # Mais espaco no topo para labels"
)
print("3. Ajustado add_axes para mais espaco no topo")

# Salvar
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("")
print("="*60)
print("CORRECOES APLICADAS!")
print("- Fontes agora sao dinamicas por visualizacao")
print("- Labels no topo terao mais espaco")
print("="*60)
print("")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_completo.qmd --to html")
