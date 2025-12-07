# 🛑 LEIA-ME PRIMEIRO (HANDOFF CONTEXT)
**Data:** 07/12/2025
**Status:** MIGRADO PARA ARQUITETURA V7 + EXPORTAÇÃO WORD

## 1. O Que Foi Feito (Última Sessão)
1.  **Padronização V7 (Gold Standard):**
    - **Página 1 (Cockpit):** Refatorada (`PAGINA_1_COCKPIT.py`). Agora usa Tabelas Markdown (não imagens) e Callouts.
    - **Página 2 (Growth):** Ajustada. Gráfico de Funil com limites corrigidos.
2.  **Pivot para Word (.docx):**
    - Abandonamos o PDF rígido. O output oficial agora é `relatorio_investidores.docx`.
    - Motivo: O usuário precisa editar layout/quebras manualmente.
3.  **Limpeza de Código:**
    - Arquivos `.py` centralizados em `notebooks/ypynb/celulas/`.
    - Logs de execução ("Iniciando motor...") silenciados via `redirect_stdout` no Quarto.

## 2. A Arquitetura Atual
- **Orquestrador:** `loader_dados_relatorio.py` (Roda tudo).
- **Control Panel:** `real_vs_ideal_v7_GOLD.ipynb` (Usa `%autoreload 2` para desenvolvimento).
- **Output:** `notebooks/quarto_pdf/relatorio_investidores.qmd` -> Gera DOCX.

## 3. PRÓXIMO PASSO (IMEDIATO)
**Iniciar a PÁGINA 3 (Financeiro).**
O arquivo `notebooks/ypynb/celulas/PAGINA_3_FINANCEIRO.py` ainda **NÃO EXISTE**.
Sua tarefa é criá-lo seguindo estritamente a estrutura da Página 2 (`PAGINA_2_GROWTH.PY`):
1.  DRE (Demonstração de Resultado).
2.  Fluxo de Caixa Semanal (0-24 semanas).
3.  Waterfalls/Sankey de Custos.

> **REGRA DE OURO:** Use `from celula_0_utils import ...` para tudo. Não duplique código. NUNCA use `plt.table`. Use `df.to_markdown()`.

## 4. Onde estão as regras?
- **Diretrizes:** `notebooks/docs_notebook/diretrizes_notebook.md` (V21.2).
- **Plano:** `implementation_plan.md` (Já detalha Page 3).
