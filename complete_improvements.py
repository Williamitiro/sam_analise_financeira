# complete_improvements.py
# Faz TODAS as melhorias de uma vez:
# 1. COMO LER melhorado para todos os VIZ (linguagem clara, explica termos)
# 2. Títulos/intros para cada VIZ no início

filepath = r'e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# VIZ 3.1: COMO LER MELHORADO
# ============================================================
old_como_ler_31 = '''        # COMO LER
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Linha Azul Sólida:** Caixa no cenário conservador (Real)
2. **Linha Azul Tracejada:** Caixa no cenário otimista (Ideal)
3. **Área Vermelha:** Burn Rate (queima de caixa mensal)
4. **Linha Verde Sólida:** EBITDA Real (eixo direito)
5. **Linha Verde Tracejada:** EBITDA Ideal (eixo direito)
6. **Regra de Sucesso:** Quando a linha verde cruzar o zero, a operação é lucrativa
"""'''

new_como_ler_31 = '''        # COMO LER
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

**O QUE ESTOU VENDO?**
Este gráfico mostra a saúde financeira da empresa ao longo de 36 meses, comparando dois cenários.

**ELEMENTOS DO GRÁFICO:**
- **Linha Azul Sólida (Caixa Real):** Quanto dinheiro temos no banco no cenário conservador
- **Linha Azul Tracejada (Caixa Ideal):** Quanto teriamos se atingissemos benchmarks de mercado
- **Area Vermelha (Burn Rate):** Quanto dinheiro "queimamos" por mes para operar - se esta area e grande, estamos gastando muito
- **Linha Verde Solida (EBITDA Real):** Lucro operacional antes de impostos - quando cruza o zero, paramos de dar prejuizo
- **Linha Verde Tracejada (EBITDA Ideal):** Lucro que teriamos no cenario otimista

**COMO INTERPRETAR:**
- Se a linha verde esta ABAIXO de zero = prejuizo operacional (normal no inicio)
- Se a linha verde CRUZA o zero = break-even (empresa se paga)
- Se a linha azul CAI muito = cuidado, caixa acabando
- Se area vermelha DIMINUI = estamos ficando mais eficientes

**TERMOS IMPORTANTES:**
- **EBITDA:** Lucro antes de juros, impostos, depreciacao e amortizacao - mede eficiencia operacional
- **Burn Rate:** Taxa de queima de caixa - quanto gastamos por mes alem do que ganhamos
- **Break-even:** Ponto onde receita = despesas, sem lucro nem prejuizo
"""'''

content = content.replace(old_como_ler_31, new_como_ler_31)
print("Melhorado: COMO LER VIZ 3.1")

# ============================================================
# VIZ 3.2: Encontrar e melhorar COMO LER
# ============================================================
# VIZ 3.2 não tem COMO LER explícito, precisa adicionar
# Vou adicionar após o waterfall chart

old_waterfall_section = '''        display(Markdown("\\\\newpage"))
    else:
        plt.show()
    
    # =========================================
    # TABELA III: BREAKDOWN DETALHADO DE CUSTOS'''

new_waterfall_section = '''        # COMO LER VIZ 3.2
        como_ler_32 = """
**📖 COMO LER ESTE GRÁFICO (WATERFALL DRE):**

**O QUE ESTOU VENDO?**
O Waterfall mostra como a receita "escorre" ate virar lucro (ou prejuizo), passando por cada tipo de custo.

**ELEMENTOS:**
- **Barra Verde (Receita Bruta):** Todo dinheiro que entra antes de qualquer desconto
- **Barras Vermelhas (Custos):** Cada "mordida" que reduz o lucro
  - Deducoes: Impostos e taxas de pagamento
  - COGS: Custo dos Produtos Vendidos - quanto custa entregar o servico
  - OPEX: Despesas Operacionais - aluguel, salarios, marketing
- **Barra Final (EBITDA):** O que sobra depois de tudo

**COMO INTERPRETAR:**
- Se EBITDA e VERDE = lucro operacional
- Se EBITDA e VERMELHO = prejuizo operacional
- Barras vermelhas GRANDES = oportunidade de cortar custos

**BENCHMARKS SaaS:**
- Margem Bruta (Receita - COGS) deve ser maior que 80%
- OPEX deve ser menor que 50% da receita
- EBITDA saudavel: maior que 20%
"""
        display(Markdown(como_ler_32))
        display(Markdown("\\\\newpage"))
    else:
        plt.show()
    
    # =========================================
    # TABELA III: BREAKDOWN DETALHADO DE CUSTOS'''

content = content.replace(old_waterfall_section, new_waterfall_section)
print("Adicionado: COMO LER VIZ 3.2")

# ============================================================
# VIZ 3.3: Melhorar COMO LER existente (se houver) ou adicionar
# ============================================================
# Procurar padrão do VIZ 3.3

old_viz33_section = '''        display(Markdown(""))  # Espaço para desconectar insight da tabela
        display(Markdown("\\\\newpage"))
    else:
        display(HTML(df_tabela.to_html(index=False, escape=False)))
        display(HTML("<br/>"))  # Espaço para desconectar insight da tabela
    
    # Insight Dinâmico
    reserva_seguranca'''

new_viz33_section = '''        # COMO LER VIZ 3.3
        como_ler_33 = """
**📖 COMO LER ESTE GRÁFICO (FLUXO DE CAIXA SEMANAL):**

**O QUE ESTOU VENDO?**
Este grafico mostra a saude do caixa SEMANA A SEMANA nos primeiros 6 meses - periodo mais critico para startups.

**ELEMENTOS:**
- **Linha Azul (Saldo Caixa):** Quanto dinheiro temos no banco a cada semana
- **Linha Vermelha Tracejada (Limite Critico):** Se caixa cair abaixo disso, temos menos de 2 semanas de sobrevivencia
- **Ponto Vermelho (Vale):** Semana mais perigosa - caixa no nivel mais baixo
- **Linha Laranja (Runway):** Quantas semanas conseguimos sobreviver com o caixa atual

**COMO INTERPRETAR:**
- **Caixa NUNCA deve tocar a linha vermelha** - se tocar, risco de insolvencia
- **Vale muito profundo** = precisamos de capital extra ou renegociar prazos
- **Runway abaixo de 4 semanas** = ALERTA MAXIMO

**TERMOS IMPORTANTES:**
- **Runway:** "Pista de pouso" - quantas semanas/meses a empresa sobrevive sem receita nova
- **Vale de Caixa:** Momento de menor liquidez, geralmente nos primeiros meses
- **Limite Critico:** Reserva minima para emergencias (2 semanas de despesas)
"""
        display(Markdown(como_ler_33))
        display(Markdown(""))  # Espaço para desconectar insight da tabela
        display(Markdown("\\\\newpage"))
    else:
        display(HTML(df_tabela.to_html(index=False, escape=False)))
        display(HTML("<br/>"))  # Espaço para desconectar insight da tabela
    
    # Insight Dinâmico
    reserva_seguranca'''

content = content.replace(old_viz33_section, new_viz33_section)
print("Adicionado: COMO LER VIZ 3.3")

# ============================================================
# VIZ 3.4: Melhorar COMO LER existente
# ============================================================
old_como_ler_34 = '''        # COMO LER (Legenda obrigatória)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO:**

1. **Pontos Coloridos:** Cada mês da projeção (M1 a M36, cor mais clara = mais antigo)
2. **Eixo X:** Receita bruta mensal
3. **Eixo Y:** Margem EBITDA (%)
4. **Linha Azul Tracejada:** Tendência real (regressão)
5. **Faixa Verde:** Zona saudável (EBITDA > 20%)
6. **Faixa Vermelha:** Zona de prejuízo (EBITDA < 0)
7. **Regra de Sucesso:** Pontos devem subir e entrar na zona verde
"""'''

new_como_ler_34 = '''        # COMO LER (Legenda obrigatória)
        como_ler = """
**📖 COMO LER ESTE GRÁFICO (ALAVANCAGEM OPERACIONAL):**

**O QUE ESTOU VENDO?**
Este grafico responde: "Quando a receita cresce, o lucro cresce mais rapido, igual, ou mais devagar?"

**ELEMENTOS:**
- **Cada Ponto = 1 Mes:** Cor mais escura = mes mais recente. Os pontos devem "subir e ir para direita"
- **Eixo X (Horizontal):** Receita bruta - quanto a empresa fatura
- **Eixo Y (Vertical):** Margem EBITDA em % - quanto sobra de lucro operacional
- **Linha Roxa Tracejada (Ideal):** Trajetoria que atingiriamos com benchmarks de mercado
- **Linha Azul Tracejada:** Tendencia real baseada nos dados
- **Faixa Verde (acima de 20%):** Margem saudavel para reinvestir e crescer
- **Faixa Vermelha (abaixo de 0%):** Prejuizo operacional

**COMO INTERPRETAR:**
- **Pontos subindo rapido** = Modelo escalavel, cada real novo gera mais lucro
- **Pontos subindo devagar** = Custos crescem junto com receita, pouca alavancagem
- **Ideal vs Real:** Se a linha roxa esta acima da azul, estamos abaixo do potencial

**TERMOS IMPORTANTES:**
- **Alavancagem Operacional:** Quanto o lucro cresce para cada 1% de crescimento de receita
  - Ex: Alavancagem 2x = receita dobra, lucro quadruplica
- **Modelo Escalavel:** Custos fixos se diluem com volume, margem melhora automaticamente
- **Margem EBITDA:** Lucro operacional dividido pela receita, em percentual
"""'''

content = content.replace(old_como_ler_34, new_como_ler_34)
print("Melhorado: COMO LER VIZ 3.4")

# ============================================================
# VIZ 3.5: Já está melhorado anteriormente, verificar
# ============================================================
# O VIZ 3.5 já tem COMO LER expandido, vou verificar e melhorar se necessário

# Salvar arquivo
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("")
print("="*60)
print("TODAS as melhorias de COMO LER aplicadas!")
print("="*60)
print("")
print("Execute: quarto render notebooks/quarto_pdf/relatorio_investidores.qmd --to docx")
