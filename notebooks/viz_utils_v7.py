# MÓDULO: VISUALIZATION UTILITIES (V7.0 - GOLD STANDARD)
# ============================================================================
# DATA: 2025-12-06
# OBJETIVO: Funções compartilhadas de renderização visual (Notebook/PDF Híbrido)
# AUTOR: Agente Codebase
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import re
from datetime import datetime

try:
    from IPython.display import display, HTML, Markdown
except ImportError:
    # Fallback para ambientes sem IPython (teste terminal)
    display = print
    HTML = str
    Markdown = str

# ============================================================================
# 1. SETUP E HELPERS DE FORMATAÇÃO
# ============================================================================

def setup_plot_style():
    """Define o estilo 'Gold Standard' para matplotlib."""
    plt.style.use('default')  # Base limpa
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def formata_moeda(valor):
    """Formata float para string de moeda (R$ 1.234,56)."""
    if pd.isna(valor):
        return "N/A"
    s = f"{valor:,.2f}"
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"R$ {s}"

def formata_pct(valor):
    """Formata float para porcentagem (12.3%)."""
    if pd.isna(valor):
        return "N/A"
    return f"{valor*100:.1f}%"

def clean_html_for_markdown(text):
    """
    Remove tags HTML e converte básicos (b, i) para Markdown.
    Útil para tabelas e textos em PDF.
    """
    if not isinstance(text, str):
        return text
    
    # Substituições Simples
    text = text.replace("<b>", "**").replace("</b>", "**")
    text = text.replace("<i>", "*").replace("</i>", "*")
    text = text.replace("<br>", "\n")
    
    # Remove spans com classes (ex: badges de status)
    text = re.sub(r"<span[^>]*>(.*?)</span>", r"**\1**", text)
     
    # Remove quaisquer outras tags restantes
    text = re.sub(r"<[^>]+>", "", text)
    
    return text

# ============================================================================
# 2. GERENCIAMENTO DE ARQUIVOS
# ============================================================================

def check_create_dir(path):
    """Cria diretório se não existir."""
    if not os.path.exists(path):
        os.makedirs(path)

def salvar_figura_silencioso(fig, nome_arquivo):
    """Salva figura sem exibir (usado pelo render_atomic_block)."""
    path_figs = os.path.join("outputs", "figs")
    check_create_dir(path_figs)
    full_path = os.path.join(path_figs, nome_arquivo)
    # DPI 300 para impressão de alta qualidade
    fig.savefig(full_path, dpi=300, bbox_inches='tight', facecolor='white')

def salvar_tabela_html_silencioso(df_tabela, filename):
    """Salva HTML sem exibir (usado pelo render_atomic_block)."""
    path_tables = os.path.join("outputs", "tables")
    check_create_dir(path_tables)
    html_content = df_tabela.to_html(index=False, escape=False)
    full_path = os.path.join(path_tables, f"{filename}_tabela.html")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def salvar_metadados_json(chart_id, titulo, data_source, insight_dict, filename):
    """Gera arquivo JSON para integração com Quarto/Markdown."""
    path_meta = os.path.join("outputs", "metadata")
    check_create_dir(path_meta)
    
    metadata = {
        "chart_id": chart_id,
        "timestamp": datetime.now().isoformat(),
        "title_simple": titulo,
        "data_source": data_source,
        "insight_generated": insight_dict,
        "files": {
            "png": f"outputs/figs/{filename}.png",
            "json": f"outputs/metadata/{filename}.json",
            "table": f"outputs/tables/{filename}_tabela.html"
        },
        "validation_status": "ok"
    }
    
    full_path = os.path.join(path_meta, f"{filename}.json")
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

# ============================================================================
# 3. CORE DE RENDERIZAÇÃO (ATOMIC BLOCK)
# ============================================================================

def render_atomic_block(chart_id, title_colloquial, title_technical, fig, legend_md, df_tabela, insight_dict, formulas_md=None, report_mode=False):
    """
    Renderiza um Bloco de Análise Atômica completo no Notebook (Padrão V20.0).
    Suporta:
    - Modo Interativo (HTML/CSS rico para Jupyter)
    - Modo Relatório (Markdown limpo + Quebras de Página para PDF via Quarto)
    """
    # A. CONFIGURAÇÃO DE QUEBRA DE PÁGINA (PDF ONLY)
    if report_mode:
        display(Markdown("\newpage"))
        
    # B. BLOCO 1: TÍTULOS
    if report_mode:
        # Adiciona {.unnumbered .unlisted} para não poluir o Sumário (TOC) no PDF
        display(Markdown(f"## {title_colloquial} {{.unnumbered .unlisted}}"))
        display(Markdown(f"### 📉 {title_technical} {{.unnumbered .unlisted}}"))
    else:
        # HTML Rico para Notebook
        display(HTML(
        f"""
        <div style="border-left: 5px solid #2563EB; padding-left: 10px; margin-bottom: 15px; margin-top: 30px;">
            <h3 style="margin: 0; color: #1E293B;">{title_technical}</h3>
            <p style="margin: 0; color: #64748B; font-style: italic;">"{title_colloquial}"</p>
        </div>
        """
        ))
    
    # C. BLOCO 2: GRÁFICO
    # Ajuste de tamanho para PDF (A4 - Margens Seguras)
    if report_mode:
        fig.set_size_inches(6.0, 3.2) 
    else:
        fig.set_size_inches(12, 6)
    
    display(fig)
    plt.close(fig) 
    
    # D. BLOCO 3: LEGENDA "COMO LER"
    if report_mode:
        display(Markdown("---")) 
        display(Markdown(f"#### 📖 COMO LER ESTE GRÁFICO:\n{legend_md}"))
    else:
        display(Markdown(f"**📖 COMO LER:** {legend_md}"))
    
    # E. BLOCO 4: TABELA AUXILIAR
    display(Markdown("#### 📋 A PROVA NUMÉRICA:"))
    
    if report_mode:
        # Markdown table limpa e COMPACTA para PDF
        df_clean = df_tabela.copy()
        
        # Encurtar nomes de colunas para caber na largura A4
        new_cols = []
        for c in df_clean.columns:
            c_new = c.replace(" (Real)", "").replace(" (Ideal)", "").replace(" (Meta)", "").replace("Global", "").replace("Estimados", "Est.")
            new_cols.append(c_new)
        df_clean.columns = new_cols

        # Limpa HTML das células (remove spans coloridos)
        for col in df_clean.columns:
            if df_clean[col].dtype == object:
                df_clean[col] = df_clean[col].apply(clean_html_for_markdown)
                
        markdown_table = df_clean.to_markdown(index=False)
        display(Markdown(markdown_table))
    else:
        # Modo Notebook: HTML Rico com CSS e Cores
        style = """
        <style>
            .dataframe { font-family: Arial, sans-serif; font-size: 13px; border-collapse: collapse; width: 100%; margin-bottom: 5px; }
            .dataframe th { background-color: #f0f0f0; color: #333; font-weight: bold; border-bottom: 2px solid #ccc; padding: 10px; text-align: left; }
            .dataframe td { padding: 10px; border-bottom: 1px solid #eee; }
            .dataframe tr:hover { background-color: #f9f9f9; }
            .status-red { color: #D32F2F; font-weight: bold; background-color: #FFEBEE; padding: 2px 6px; border-radius: 4px; }
            .status-yellow { color: #FBC02D; font-weight: bold; background-color: #FFFDE7; padding: 2px 6px; border-radius: 4px; }
            .status-green { color: #388E3C; font-weight: bold; background-color: #E8F5E9; padding: 2px 6px; border-radius: 4px; }
        </style>
        """
        html_table = style + df_tabela.to_html(index=False, escape=False, classes='dataframe')
        display(HTML(html_table))
    
    # F. BLOCO 5: AUDITORIA & FÓRMULAS
    if formulas_md:
        if report_mode:
            audit_clean = clean_html_for_markdown(formulas_md)
            audit_md = f"""
::: {{.callout-note collapse="true"}}
## 🔍 AUDITORIA & FÓRMULAS
{audit_clean}
:::
            """
            display(Markdown(audit_md))
        else:
            audit_html = f"""
            <div style="font-size: 11px; color: #555; background-color: #f9f9f9; padding: 10px; border: 1px solid #eee; margin-bottom: 20px; border-radius: 4px;">
                <b>🔍 AUDITORIA & FÓRMULAS:</b><br>
                {formulas_md.replace(chr(10), '<br>')}
            </div>
            """
            display(HTML(audit_html))

    # G. BLOCO 6: INSIGHT ESTRATÉGICO
    if report_mode:
        # Callout Quarto (PDF)
        insight_md = f"""
::: {{.callout-tip}}
## 💡 INSIGHT ESTRATÉGICO

- **FATO:** 
  {clean_html_for_markdown(insight_dict['fato'])}

- **CAUSA:** 
  {clean_html_for_markdown(insight_dict['causa'])}

- **IMPLICAÇÃO:** 
  {clean_html_for_markdown(insight_dict['implicacao'])}

- **AÇÃO RECOMENDADA:** 
  {clean_html_for_markdown(insight_dict['acao'])}
:::
        """
        display(Markdown(insight_md))
    else:
        # Card HTML (Notebook)
        insight_md = f"""
<div style="background-color: #F3F4F6; border-left: 5px solid #2563EB; padding: 15px; border-radius: 4px;">
    <h4 style="margin-top: 0; color: #1E3A8A;">💡 INSIGHT ESTRATÉGICO</h4>
    <ul style="margin-bottom: 0;">
        <li><b>FATO:</b> {insight_dict['fato']}</li>
        <li><b>CAUSA:</b> {insight_dict['causa']}</li>
        <li><b>IMPLICAÇÃO:</b> {insight_dict['implicacao']}</li>
        <li><b>AÇÃO RECOMENDADA:</b> {insight_dict['acao']}</li>
    </ul>
</div>
        """
        display(HTML(insight_md))
    
    # H. PERSISTÊNCIA (Salvar arquivos no disco para uso externo)
    # Nota: Usa o ID do gráfico como nome de arquivo base
    salvar_figura_silencioso(fig, f"{chart_id}.png")
    salvar_tabela_html_silencioso(df_tabela, f"{chart_id}")
    salvar_metadados_json(chart_id, title_technical, "Simulação V1", insight_dict, chart_id)
