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

# ============================================================================
# CONSTANTES DE DIRETÓRIO (CENTRALIZAÇÃO)
# ============================================================================
# Garante que outputs sempre vão para notebooks/ypynb/outputs
# Independente de onde o script é executado (root ou subpasta)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
FIGS_DIR = os.path.join(OUTPUTS_DIR, "figs")
META_DIR = os.path.join(OUTPUTS_DIR, "metadata")
TABLES_DIR = os.path.join(OUTPUTS_DIR, "tables")
MC_DIR = os.path.join(OUTPUTS_DIR, "mc_data")

# Garante que existem na importação
for d in [OUTPUTS_DIR, FIGS_DIR, META_DIR, TABLES_DIR, MC_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

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
        return "R$ 0,00"
    
    # Garantir que é float
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return "R$ -,--"

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
    # check_create_dir(path_figs) -> Já garantido na inicialização
    
    # Se nome_arquivo vier com caminhos relativos antigos (outputs/figs/...), limpa
    nome_limpo = os.path.basename(nome_arquivo)
    full_path = os.path.join(FIGS_DIR, nome_limpo)
    
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
    nome_limpo = os.path.basename(nome_arquivo)
    full_path = os.path.join(FIGS_DIR, nome_limpo)
    fig.savefig(full_path, dpi=300, bbox_inches='tight', facecolor='white')

def salvar_metadados_json(chart_id, titulo, data_source, insight_dict, filename):
    """Gera arquivo JSON para integração com Quarto/Markdown."""
    # META_DIR já definido
    
    metadata = {
        "chart_id": chart_id,
        "section": "growth_machine",
        "page_number": 2,
        "timestamp": datetime.now().isoformat(),
        "title_simple": titulo,
        "data_source": data_source,
        "insight_generated": insight_dict,
        "files": {
            "png": f"outputs/figs/{os.path.basename(filename)}.png",
            "json": f"outputs/metadata/{os.path.basename(filename)}.json",
            "table": f"outputs/tables/{os.path.basename(filename)}_tabela.html"
        },
        "validation_status": "ok"
    }
    
    name_clean = os.path.basename(filename)
    if not name_clean.endswith('.json'):
        name_clean += '.json'
    
    full_path = os.path.join(META_DIR, name_clean)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def salvar_tabela_html(df_tabela, filename):
    """Exporta DataFrame da tabela auxiliar para HTML e exibe inline."""
    # TABLES_DIR já definido
    
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
    
    if isinstance(df_tabela, pd.DataFrame):
        html_content = style + df_tabela.to_html(index=False, escape=False)
    else:
        html_content = style + str(df_tabela)
    
    name_clean = os.path.basename(filename)
    full_path = os.path.join(TABLES_DIR, f"{name_clean}_tabela.html")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   📋 Tabela salva: {full_path}")

def salvar_tabela_html_silencioso(df_tabela, filename):
    """Salva HTML sem exibir (usado pelo render_atomic_block)."""
    if isinstance(df_tabela, str) or df_tabela is None:
        return
        
    html_content = df_tabela.to_html(index=False, escape=False)
    
    name_clean = os.path.basename(filename)
    full_path = os.path.join(TABLES_DIR, f"{name_clean}_tabela.html")
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
    # Título Customizado ou Default
    titulo_tabela = table_title if table_title else "📋 TABELA DE DADOS:"
    display(Markdown(f"#### {titulo_tabela}"))
    
    # ----------------------------------------------
    # RENDERIZAÇÃO DE TABELA (HTML UNIFICADO V8.0)
    # ----------------------------------------------
    if isinstance(df_tabela, str):
        # Caso Especial: Tabela já passada como string Markdown
        display(Markdown(f"\n\n{df_tabela}\n\n"))
        display(Markdown(""))
            
    elif isinstance(df_tabela, pd.DataFrame):
        if not df_tabela.empty:
            # Estilo CSS Gold Standard (Funciona no Notebook e na maioria dos exports HTML)
            style = """
            <style>
                .dataframe { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; border-collapse: collapse; width: 100%; margin-bottom: 10px; border: 1px solid #e0e0e0; }
                .dataframe th { background-color: #f8f9fa; color: #495057; font-weight: 600; border-bottom: 2px solid #dee2e6; padding: 12px; text-align: left; }
                .dataframe td { padding: 10px 12px; border-bottom: 1px solid #e9ecef; color: #212529; }
                .dataframe tr:hover { background-color: #f1f3f5; }
                .status-red { color: #c0392b; font-weight: bold; background-color: #fadbd8; padding: 2px 8px; border-radius: 12px; font-size: 0.9em; }
                .status-yellow { color: #d4ac0d; font-weight: bold; background-color: #fcf3cf; padding: 2px 8px; border-radius: 12px; font-size: 0.9em; }
                .status-green { color: #27ae60; font-weight: bold; background-color: #d5f5e3; padding: 2px 8px; border-radius: 12px; font-size: 0.9em; }
            </style>
            """
            
            # Converter para HTML (mantendo tags internas como badges)
            html_table = df_tabela.to_html(index=False, escape=False, classes='dataframe')
            
            # Exibir
            display(HTML(style + html_table))
            display(Markdown("")) # Espaço de respiro
        else:
            display(Markdown("_Sem dados tabulares para exibir._"))
            
    else:
        # Fallback para outros tipos (None, etc)
        pass
    
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
