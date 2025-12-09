# ============================================================================
# VIZ 4.4 CORRIGIDA: ESCALA DE CLIENTES vs SAÚDE UNITÁRIA
# ============================================================================
def gerar_viz_4_4_escala_unit_economics(df_real_m, premissas, report_mode=False):
    """
    Scatter Plot: Base de Clientes (X) vs LTV/CAC (Y).
    
    PERGUNTA CEO: "Se dobrar a base de clientes, a unidade continua lucrativa?"
    
    TESE A PROVAR: 
    - Se LTV/CAC SOBE com escala → Economia de escala (bom!)
    - Se LTV/CAC CAI com escala → Diluição de qualidade (ruim!)
    """
    
    if not report_mode:
        print("\n🔹 VIZ 4.4: Escala de Clientes vs Saúde Unitária")
    else:
        display(Markdown("***"))
        display(Markdown("## VIZ 4.4: Escala vs Saúde Unitária"))
        display(Markdown("**Pergunta:** Se dobrar a base de clientes, a unidade continua lucrativa?"))
    
    # =========================================================================
    # 1. DADOS
    # =========================================================================
    usuarios = df_real_m['usuarios_ativos'].values
    ltv_cac = df_real_m['ltv_cac'].fillna(0).values
    meses = df_real_m['mes'].values
    cac_blended = df_real_m['cac_blended'].values
    churn_rate = df_real_m['churn_rate'].values * 100
    
    # =========================================================================
    # 2. ANÁLISE: REGRESSÃO PARA DETECTAR TENDÊNCIA
    # =========================================================================
    # Fit linear para detectar se LTV/CAC melhora ou piora com escala
    from numpy.polynomial import Polynomial
    
    # Filtrar apenas pontos onde temos dados válidos
    mask = (usuarios > 0) & (ltv_cac > 0)
    x_valid = usuarios[mask]
    y_valid = ltv_cac[mask]
    
    if len(x_valid) < 3:
        print("⚠️ AVISO: Dados insuficientes para regressão")
        return
    
    # Fit linear
    p_linear = Polynomial.fit(x_valid, y_valid, 1)
    slope = p_linear.coef[1]
    
    # Fit polinomial (grau 2) para detectar saturação
    p_poly = Polynomial.fit(x_valid, y_valid, 2)
    
    # Linha de tendência
    x_line = np.linspace(x_valid.min(), x_valid.max() * 1.2, 100)
    y_line_linear = p_linear(x_line)
    y_line_poly = p_poly(x_line)
    
    # =========================================================================
    # 3. PLOTAGEM
    # =========================================================================
    figsize = (10, 6) if report_mode else (14, 7)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.10, right=0.95)
    
    # Scatter com gradiente de cor por mês
    scatter = ax.scatter(usuarios, ltv_cac, c=meses, cmap='viridis', 
                        s=120, alpha=0.8, edgecolors='black', 
                        linewidth=0.8, zorder=3)
    
    # Linhas de tendência
    ax.plot(x_line, y_line_linear, color='#1976D2', linewidth=2.5, 
            linestyle='--', label='Tendência Linear', alpha=0.7)
    ax.plot(x_line, y_line_poly, color='#D32F2F', linewidth=2, 
            linestyle='-', label='Tendência Real (Poly)', alpha=0.8)
    
    # Zona de saúde (LTV/CAC > 3.0)
    ax.axhspan(3.0, max(ltv_cac.max(), 5.0), color='#E8F5E9', 
               alpha=0.3, label='Zona Saudável (>3x)')
    ax.axhline(3.0, color='#4CAF50', linestyle='--', linewidth=1.5, alpha=0.7)
    
    # Zona de perigo (LTV/CAC < 1.0)
    ax.axhspan(0, 1.0, color='#FFEBEE', alpha=0.3, label='Zona de Perigo (<1x)')
    ax.axhline(1.0, color='#F44336', linestyle='--', linewidth=1.5, alpha=0.7)
    
    # Anotações nos pontos-chave
    # Ponto inicial (M1)
    ax.annotate('M1 (Início)', 
                xy=(usuarios[0], ltv_cac[0]),
                xytext=(usuarios[0] * 1.1, ltv_cac[0] + 0.3),
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    
    # Ponto final (M36)
    ax.annotate('M36 (Final)', 
                xy=(usuarios[-1], ltv_cac[-1]),
                xytext=(usuarios[-1] * 0.85, ltv_cac[-1] + 0.3),
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    
    # Ponto de maior eficiência (onde LTV/CAC é máximo)
    idx_max = ltv_cac.argmax()
    if idx_max not in [0, len(ltv_cac)-1]:  # Só anota se não for início/fim
        ax.scatter([usuarios[idx_max]], [ltv_cac[idx_max]], 
                  color='gold', s=200, marker='*', zorder=4, 
                  edgecolors='black', linewidth=1.5)
        ax.annotate(f'Pico Eficiência\nM{meses[idx_max]}', 
                    xy=(usuarios[idx_max], ltv_cac[idx_max]),
                    xytext=(usuarios[idx_max] * 1.15, ltv_cac[idx_max] - 0.5),
                    fontsize=9, fontweight='bold', color='#F57F17',
                    arrowprops=dict(arrowstyle='->', color='#F57F17', lw=2))
    
    # Configurações do eixo
    ax.set_xlabel('Base de Clientes Ativos', fontsize=12, fontweight='bold')
    ax.set_ylabel('LTV/CAC (Eficiência Unitária)', fontsize=12, fontweight='bold')
    ax.set_title('Impacto da Escala na Saúde Unitária', fontsize=11, color='gray')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Mês de Operação', fontsize=10)
    
    fig.suptitle('📊 ESCALA vs SAÚDE UNITÁRIA (LTV/CAC)', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # =========================================================================
    # 4. TABELA DE ANÁLISE POR FAIXAS DE ESCALA
    # =========================================================================
    # Dividir em quartis de clientes para análise
    quartis = [0, 25, 50, 75, 100]
    tabela_md = "| Faixa de Clientes | Usuarios (Media) | LTV/CAC Medio | CAC Medio | Churn Medio | Status |\n"
    tabela_md += "|:---|---:|---:|---:|---:|:---|\n"
    
    percentis = np.percentile(usuarios, quartis)
    
    for i in range(len(percentis)-1):
        mask_faixa = (usuarios >= percentis[i]) & (usuarios < percentis[i+1])
        
        if mask_faixa.sum() == 0:
            continue
        
        usuarios_media = usuarios[mask_faixa].mean()
        ltv_cac_media = ltv_cac[mask_faixa].mean()
        cac_media = cac_blended[mask_faixa].mean()
        churn_media = churn_rate[mask_faixa].mean()
        
        if ltv_cac_media >= 3.0:
            status = "🟢 ESCALÁVEL"
        elif ltv_cac_media >= 1.5:
            status = "🟡 MODERADO"
        else:
            status = "🔴 CRÍTICO"
        
        faixa_label = f"P{quartis[i]}-P{quartis[i+1]}"
        tabela_md += f"| {faixa_label} | {int(usuarios_media)} | {ltv_cac_media:.2f}x | {formata_moeda(cac_media)} | {churn_media:.1f}% | {status} |\n"
    
    # =========================================================================
    # 5. LEGENDA "COMO LER"
    # =========================================================================
    legend_md = """
**O QUE ESTOU VENDO?**
Teste de escalabilidade: Conforme a base de clientes cresce (eixo X), a eficiência unitária (LTV/CAC, eixo Y) melhora, piora ou se mantém?

**ELEMENTOS:**
- **Bolinhas (cor = mês):** Cada ponto é um mês. Cores escuras = mais recente.
- **Linha Azul Tracejada:** Se a relação fosse perfeitamente linear.
- **Linha Vermelha Sólida:** Tendência real (pode curvar se houver saturação).
- **Zona Verde (>3x):** Alta eficiência, seguro para escalar.
- **Zona Vermelha (<1x):** Prejuízo unitário, NÃO escalar.

**INTERPRETAÇÃO:**
- **Linha SUBINDO para direita:** Economia de escala (quanto mais clientes, mais eficiente) ✅
- **Linha DESCENDO para direita:** Diluição de qualidade (escala piora o negócio) ❌
- **Linha HORIZONTAL:** Escala neutra (nem ajuda, nem atrapalha) ⚠️
"""
    
    # =========================================================================
    # 6. INSIGHT DINÂMICO
    # =========================================================================
    # Analisar a TENDÊNCIA da inclinação
    ltv_cac_inicial = ltv_cac[:6].mean()  # Média dos primeiros 6 meses
    ltv_cac_final = ltv_cac[-6:].mean()   # Média dos últimos 6 meses
    delta_ltv_cac = ltv_cac_final - ltv_cac_inicial
    
    usuarios_inicial = usuarios[:6].mean()
    usuarios_final = usuarios[-6:].mean()
    crescimento_base = ((usuarios_final - usuarios_inicial) / max(usuarios_inicial, 1)) * 100
    
    if slope > 0.0001:  # Slope positivo = melhora com escala
        insight = {
            "fato": f"LTV/CAC melhora {delta_ltv_cac:+.2f}x enquanto base cresce {crescimento_base:.0f}%.",
            "causa": f"Economia de escala: CAC cai ou LTV aumenta conforme volume sobe (slope={slope:.4f}).",
            "implicacao": "Modelo altamente escalável. Cada novo cliente MELHORA a eficiência média.",
            "acao": "Acelerar investimento em aquisição. O teto de escala ainda não foi atingido."
        }
    elif slope < -0.0001:  # Slope negativo = piora com escala
        insight = {
            "fato": f"LTV/CAC piora {delta_ltv_cac:+.2f}x enquanto base cresce {crescimento_base:.0f}%.",
            "causa": f"Diluição de qualidade: CAC sobe ou Churn aumenta com volume (slope={slope:.4f}).",
            "implicacao": "Escala está corroendo a eficiência. Crescimento pode ser autodestrutivo.",
            "acao": "PARAR crescimento. Focar em retenção e qualificação de clientes antes de escalar."
        }
    else:  # Slope ~0 = neutro
        insight = {
            "fato": f"LTV/CAC estável (~{ltv_cac_final:.2f}x) apesar de base crescer {crescimento_base:.0f}%.",
            "causa": f"Escala neutra: CAC e LTV crescem proporcionalmente (slope={slope:.4f}).",
            "implicacao": "Modelo escalável sem vantagens/desvantagens de escala.",
            "acao": "Buscar otimizações para tornar slope positivo (ex: automação, PLG)."
        }
    
    # =========================================================================
    # 7. FÓRMULAS E AUDITORIA
    # =========================================================================
    formulas = f"""
**Fonte:** df_real_m (Célula 5A)

**Fórmulas:**
1. **LTV/CAC** = (ARPU × Margem Bruta % / Churn) / CAC
2. **Slope (Inclinação)** = Coeficiente angular da regressão linear (X=Clientes, Y=LTV/CAC)
   - Valor calculado: **{slope:.6f}**
   - Interpretação: 
     - Slope > 0: Economia de escala (melhor com volume) ✅
     - Slope < 0: Diluição de qualidade (pior com volume) ❌
     - Slope ≈ 0: Escala neutra ⚠️

**Metodologia:**
- Regressão polinomial (grau 2) para detectar saturação não-linear
- Análise por quartis de base de clientes para validar consistência
- Comparação M1-M6 vs M31-M36 para medir impacto acumulado
"""
    
    # =========================================================================
    # 8. RENDERIZAR BLOCO ATÔMICO
    # =========================================================================
    render_atomic_block(
        chart_id="pg4_viz4_escala_unit",
        title_colloquial="Se dobrar a base de clientes, a unidade continua lucrativa?",
        title_technical="VIZ 4.4: Escala vs Saúde Unitária (LTV/CAC)",
        fig=fig,
        legend_md=legend_md,
        df_tabela=tabela_md,
        insight_dict=insight,
        formulas_md=formulas,
        report_mode=report_mode,
        table_title="📋 ANÁLISE POR FAIXA DE ESCALA",
        data_source_text="Fonte: df_real_m (Célula 5A) | 'usuarios_ativos' vs 'ltv_cac'"
    )
    
    plt.close(fig)
    return {'slope': slope, 'ltv_cac_final': ltv_cac_final}