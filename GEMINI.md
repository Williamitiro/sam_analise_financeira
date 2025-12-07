---

---

## Gemini Added Memories (Updated)

### Project Status: Notebook Refactoring & "Gold Standard" PDF (Current)

This document summarizes the pivot towards a "Gold Standard" Investor Deck, generated programmatically via Jupyter Notebooks with high-fidelity PDF export output (Quarto).

### Major Achievements (Page 2 - Growth Machine):

1.  **Architecture "Atomic Analysis Cell" (V20.0):**
    *   Transitioned from monolithic code to modular "Atomic Blocks" (`render_atomic_block`).
    *   Each visualization now encapsulates: Header, Chart (Matplotlib), Legend (Markdown), Proof Table (HTML/MD), Insight (Strategic Text), and Audit Trail (Formulas).

2.  **Hybrid "Report Mode" Engine:**
    *   **Concept:** A single codebase (`modelo2_v7.py`) supports two distinct outputs:
        *   **Notebook Mode (`report_mode=False`):** Interactive, rich HTML tables, colorful badges.
        *   **PDF Mode (`report_mode=True`):** Clean Markdown tables, Quarto Callouts for text blocks, silent execution (no logs), and print-optimized figure sizes.

3.  **Auditability Layer:**
    *   Implemented a dedicated "Audit & Formulas" section in every visual block.
    *   Added metadata export (`exportar_relatorio_total_json`) for external validation.

### Current Challenges (PDF Layout):

*   **Overflow:** Graphs and tables tend to exceed A4 margins. Fixes applied:
    *   Reduced figure size to 6.0" x 3.2".
    *   Compacted table headers in Report Mode.
*   **Page Breaks:** LaTeX `minipage` caused compilation errors. Current strategy relies on `\newpage` before each block.
*   **Next Steps:** Validate visual output of PDF and refactor Page 1 (Executive Summary) using the same V7.0 pattern.

---

