# CÉLULA 0 - UTILITIES COMPARTILHADAS (GOLD STANDARD)
# ============================================================================
# OBJETIVO: Funções de visualização, formatação e IO compartilhadas entre páginas.
# ============================================================================

import pandas as pd
import numpy as np
import textwrap
print("DEBUG: LOADED celula_0_utils V7.5 (If fig check applied)")
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

try:
    from IPython.display import display, HTML, Markdown
except ImportError:
    # Fallback para ambientes sem IPython
    display = print
    HTML = str
    Markdown = str

# ============================================================================
# 1. SETUP E HELPERS VISUAIS
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

# ============================================================================
# 2. FILE SYSTEM OPERATIONS
# ============================================================================

def check_create_dir(path):
    """Cria diretório se não existir."""
    if not os.path.exists(path):
        os.makedirs(path)

def salvar_figura(fig, nome_arquivo):
    """Salva figura em 300 DPI e exibe inline no notebook."""
    path_figs = os.path.join("outputs", "figs")
    check_create_dir(path_figs)
    full_path = os.path.join(path_figs, nome_arquivo)
    
    fig.savefig(full_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"   📸 Figura salva: {full_path}")
    
    # Exibe no notebook antes de fechar
    try:
        display(fig)
    except:
        pass
        
    plt.close(fig)

def salvar_figura_silencioso(fig, nome_arquivo):
    """Salva figura sem exibir (usado pelo render_atomic_block)."""
    path_figs = os.path.join("outputs", "figs")
    check_create_dir(path_figs)
    full_path = os.path.join(path_figs, nome_arquivo)
    fig.savefig(full_path, dpi=300, bbox_inches='tight', facecolor='white')

def salvar_metadados_json(chart_id, titulo, data_source, insight_dict, filename):
    """Gera arquivo JSON para integração com Quarto/Markdown."""
    path_meta = os.path.join("outputs", "metadata")
    check_create_dir(path_meta)
    
    metadata = {
        "chart_id": chart_id,
        "section": "growth_machine",
        "page_number": 2,
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

def salvar_tabela_html(df_tabela, filename):
    """Exporta DataFrame da tabela auxiliar para HTML e exibe inline."""
    path_tables = os.path.join("outputs", "tables")
    check_create_dir(path_tables)
    
    # Estilização básica CSS inline para garantir consistência
    style = """
    <style>
        table { border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 12px; }
        th { text-align: left; padding: 8px; border-bottom: 2px solid #333; background-color: #f8f9fa; }
        td { padding: 8px; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f5f5f5; }
        .status-red { color: #d32f2f; font-weight: bold; }
        .status-yellow { color: #fbc02d; font-weight: bold; }
        .status-green { color: #388e3c; font-weight: bold; }
    </style>
    """
    
    html_content = style + df_tabela.to_html(index=False, escape=False)
    
    full_path = os.path.join(path_tables, f"{filename}_tabela.html")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   📋 Tabela salva: {full_path}")

def salvar_tabela_html_silencioso(df_tabela, filename):
    """Salva HTML sem exibir (usado pelo render_atomic_block)."""
    path_tables = os.path.join("outputs", "tables")
    check_create_dir(path_tables)
    html_content = df_tabela.to_html(index=False, escape=False)
    full_path = os.path.join(path_tables, f"{filename}_tabela.html")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# ============================================================================
# 3. RENDERING ENGINE (ATOMIC BLOCK V20.0)
# ============================================================================

def render_atomic_block(chart_id, title_colloquial, title_technical, fig, legend_md, df_tabela, insight_dict, formulas_md=None, report_mode=False, table_title=None, data_source_text=None):
    """
    Renderiza um Bloco de Análise Atômica completo no Notebook (Padrão V21.1).
    Se report_mode=True: 
      - Redimensiona figuras para caber em A4 (10x4.5).
      - Converte HTML tags (<b>) para Markdown (**).
      - Usa Callouts do Quarto.
    Se report_mode=False: 
      - Usa HTML/CSS rico.
    """
    # 0. AJUSTE DE FIGURA PARA PDF (CRÍTICO)
    if report_mode and fig:
        # Força redimensionamento para evitar overflow no A4 (Widescreen Compacto)
        fig.set_size_inches(10, 4.5) 
    
    # 1. BLOCO A: TÍTULOS
    display(Markdown(f"## {title_colloquial}"))
    display(Markdown(f"### 📉 {title_technical}"))
    
    # 2. BLOCO B: GRÁFICO (Opcional)
    if fig:
        display(fig)
        if data_source_text:
            display(Markdown(f"*{data_source_text}*"))
        plt.close(fig) 
    else:
        # Se não tem figura, apenas exibe a fonte se houver
        if data_source_text:
            display(Markdown(f"*{data_source_text}*"))

    # 3. BLOCO C: LEGENDA "COMO LER" (Opcional)
    if legend_md:
        display(Markdown("***")) 
        
        if report_mode:
            # Modo PDF/Quarto: Callout Note Simple (Igual Tier 1)
            como_ler_block = f"""
::: {{.callout-note appearance="simple"}}
### 📖 COMO LER ESTE GRÁFICO
{legend_md}
:::
"""
            display(Markdown(como_ler_block))
        else:
            # Modo Notebook HTML
            display(Markdown(f"#### 📖 COMO LER ESTE GRÁFICO:\n{legend_md}"))
    
    # 4. BLOCO D: TABELA AUXILIAR
    # Título Customizado ou Default
    titulo_tabela = table_title if table_title else "📋 A PROVA NUMÉRICA:"
    display(Markdown(f"#### {titulo_tabela}"))
    
    if isinstance(df_tabela, str):
        # CASO ESPECIAL: Tabela passada como String Markdown pura (Manual)
        # Útil para casos onde pandas.to_markdown quebra a formatação
        display(Markdown(f"\n\n{df_tabela}\n\n"))
        
        # Em modo notebook, se quisermos salvar HTML, precisaríamos parsear ou ignorar.
        # Aqui vamos salvar apenas o arquivo texto se for string.
        if not report_mode:
            pass # Não salva HTML se for string manual
        
        # CORREÇÃO V7.6: Espaçamento após tabela string
        display(Markdown(""))
            
    elif report_mode:
        # Modo Relatório: Markdown Puro e Limpo via Pandas
        df_clean = df_tabela.fillna('')
        
        # 1. Remove tags HTML de colunas de texto (mas mantém conteúdo)
        # Ex: <span class='status-green'>SUPEROU</span> -> SUPEROU
        df_clean = df_clean.replace(to_replace=r'<[^>]+>', value='', regex=True)
        
        # 2. Converte para Markdown (Força formato pipe padrão e sanitiza)
        # remove_index=False se quiser index, mas aqui é False
        markdown_table = df_clean.to_markdown(index=False, tablefmt="pipe")
        
        # Correção ROBUSTA de caracteres de separação (long-dashes e em-dashes)
        # Substitui travessões longos que o tabulate ou copy-paste podem ter gerado
        markdown_table = markdown_table.replace('—', '-').replace('–', '-')
        
        # Garante quebras de linha para o processador Markdown do Quarto
        markdown_table = f"\n\n{markdown_table}\n\n"
        
        display(Markdown(markdown_table))
    else:
        # Modo Notebook: HTML Rico com CSS
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
        
        # CORREÇÃO V7.6: Espaçamento após tabela HTML
        display(Markdown(""))
    
    # 5. BLOCO E: INSIGHT ESTRATÉGICO
    # CORREÇÃO V7.6: Separador visual antes do insight
    display(Markdown(""))  # Espaçamento extra
    display(Markdown("***"))  # Linha horizontal (*** evita conflito YAML do Quarto)
    
    if report_mode:
        # Quarto Callout para Insight (Tip/Important)
        insight_class = "tip" # ou important
        insight_md = f"""
::: {{.callout-{insight_class}}}
## 💡 INSIGHT ESTRATÉGICO
- **FATO:** {insight_dict['fato']}
- **CAUSA:** {insight_dict['causa']}
- **IMPLICAÇÃO:** {insight_dict['implicacao']}
- **AÇÃO RECOMENDADA:** {insight_dict['acao']}
:::
        """
        display(Markdown(insight_md))
    else:
        # HTML Rico para Notebook
        def clean_text_for_html(text):
             if pd.isna(text): return ""
             return str(text).replace("'", "&#39;").replace('"', "&quot;")
        
        fato = clean_text_for_html(insight_dict['fato'])
        causa = clean_text_for_html(insight_dict['causa'])
        implicacao = clean_text_for_html(insight_dict['implicacao'])
        acao = clean_text_for_html(insight_dict['acao'])

        insight_md = f"""
<div style="background-color: #F3F4F6; border-left: 5px solid #2563EB; padding: 15px; border-radius: 4px;">
    <h4 style="margin-top: 0; color: #1E3A8A;">💡 INSIGHT ESTRATÉGICO</h4>
    <ul style="margin-bottom: 0;">
        <li><b>FATO:</b> {fato}</li>
        <li><b>CAUSA:</b> {causa}</li>
        <li><b>IMPLICAÇÃO:</b> {implicacao}</li>
        <li><b>AÇÃO RECOMENDADA:</b> {acao}</li>
    </ul>
</div>
        """
        display(HTML(insight_md))

    # 6. BLOCO F: AUDITORIA & FÓRMULAS
    if formulas_md:
        if report_mode:
            # SANITIZAÇÃO DE HTML PARA MARKDOWN (CORREÇÃO V21.1)
            # Remove qualquer tag HTML restante (<...>) e converte basics
            import re
            
            # Remove indentação excessiva para evitar Code Block no Markdown
            audit_clean = textwrap.dedent(formulas_md).strip()
            
            audit_clean = audit_clean\
                .replace("<b>", "**").replace("</b>", "**")\
                .replace("<i>", "*").replace("</i>", "*")\
                .replace("<br>", "\n")
            
            audit_clean = re.sub(r'<[^>]+>', '', audit_clean)
            
            # Quarto Callout para Auditoria
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

    if report_mode:
        # Quebra de página no PDF após cada bloco
        display(Markdown("\\newpage"))
    
    # 6. Salvar arquivos
    if fig:
        salvar_figura_silencioso(fig, f"{chart_id}.png")
    if not isinstance(df_tabela, str):
        salvar_tabela_html_silencioso(df_tabela, f"{chart_id}")
    salvar_metadados_json(chart_id, title_technical, "df_real vs df_ideal", insight_dict, chart_id)
