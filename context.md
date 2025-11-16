

---

### **Plano de Ação: Montando a Documentação Perfeita**

#### **Passo 1: Criar o Arquivo Mestre**

Crie um novo arquivo na raiz do seu projeto chamado `contexto_para_claude.md`. Todo o conteúdo a seguir será colado dentro deste arquivo.

#### **Passo 2: A Introdução e o Objetivo**

Comece o arquivo com um resumo claro para a IA.

**(Copie e cole isso no seu arquivo)**
```markdown
# Dossiê de Arquitetura: Sistema SAM Análises Financeiras

**Para:** Arquiteto de Software Sênior (IA Claude)

**De:** [william itiro]

**Missão:** Analisar a arquitetura de backend Python existente deste projeto e, com base nela, projetar uma arquitetura de frontend profissional e um plano de implementação detalhado. O objetivo é substituir a UI atual (prototipada em Streamlit) por uma solução mais robusta e escalável.

---
```

#### **Passo 3: A Estrutura de Arquivos (O Mapa)**

Dê à IA o mapa do tesouro primeiro.

**(Execute `tree /F core` no terminal e cole o resultado aqui)**
```markdown
## 1. Estrutura de Arquivos do Módulo `core/`

Esta é a organização atual dos nossos módulos de lógica de negócio.

```
[COLE AQUI A SAÍDA DO COMANDO 'tree /F core']
```

---
```

#### **Passo 4: O Coração do Sistema (Os Arquivos Essenciais)**

Agora, vamos colar o conteúdo dos arquivos mais importantes, um por um, em seções bem definidas. Isso é crucial.

**(Copie o conteúdo de cada arquivo e cole nas seções abaixo)**
```markdown
## 2. Código-Fonte dos Módulos Principais

A seguir estão os conteúdos completos dos arquivos que definem a lógica central do sistema.

### 2.1. `core/config.py` - A Estrutura de Dados Central

Este arquivo define o objeto `ConfigFinanceira`, que serve como o contêiner para todas as premissas e configurações de uma simulação.

```python
# Conteúdo completo de core/config.py
[COLE AQUI O CONTEÚDO COMPLETO DO SEU core/config.py]
```

### 2.2. `core/engine.py` - O Motor de Projeção

Este arquivo contém a classe `MotorProjecaoFinanceira`, que recebe um objeto `ConfigFinanceira` e executa todos os cálculos para gerar o DataFrame de resultados.

```python
# Conteúdo completo de core/engine.py
[COLE AQUI O CONTEÚDO COMPLETO DO SEU core/engine.py]
```

### 2.3. `core/builders/` - Exemplos da Lógica de Negócio

Os "Builders" são responsáveis por popular o objeto `ConfigFinanceira` com dados estruturados. Abaixo estão os exemplos mais representativos.

**`core/builders/team_builder.py`**
```python
# Conteúdo completo de core/builders/team_builder.py
[COLE AQUI O CONTEÚDO COMPLETO DO SEU team_builder.py]
```

**`core/builders/revenue_builder.py`**
```python
# Conteúdo completo de core/builders/revenue_builder.py
[COLE AQUI O CONTEÚDO COMPLETO DO SEU revenue_builder.py]
```

---
```

#### **Passo 5: A Lógica de Análise e Visualização (Consolidando o Conhecimento)**

Como as pastas `analytics` e o arquivo `visualizations.py` estão vazios, vamos extrair a lógica que **deveria** estar neles diretamente do seu dashboard mais completo.

**(Copie as funções relevantes do seu `01_Dashboard_Receita.py` e cole-as aqui)**
```markdown
## 3. Lógica de Análise e Visualização (Extraída do Protótipo)

A lógica analítica e de visualização foi prototipada diretamente nos arquivos de interface do Streamlit. Abaixo estão as funções mais importantes que demonstram a capacidade de análise do sistema. No futuro, elas serão movidas para os módulos `core/analytics` e `core/visualizations`.

### 3.1. Lógica Analítica (Ex: Geração de Cohorts)

Esta função, extraída do dashboard de receita, demonstra como a análise de cohorts é calculada a partir do DataFrame de resultados.

```python
# Função extraída de app/pages/01_Dashboard_Receita.py
@st.cache_data
def gerar_cohort_matrix(df):
    """Gera matriz de cohorts (otimizada)"""
    # [COLE AQUI O CONTEÚDO DA FUNÇÃO gerar_cohort_matrix]
```

### 3.2. Lógica de Visualização (Ex: Gráfico Waterfall)

Esta função, também do dashboard de receita, mostra como um gráfico complexo como o Waterfall de MRR é construído usando Plotly.

```python
# Lógica de criação do gráfico Waterfall extraída de app/pages/01_Dashboard_Receita.py
def criar_grafico_waterfall(mes_atual, mes_anterior):
    # [COLE AQUI O BLOCO DE CÓDIGO QUE GERA A go.Figure(go.Waterfall(...))]
```

---
```

#### **Passo 6: O Prompt Final (As Instruções para a IA)**

Termine o documento com as instruções claras que já elaboramos.

**(Copie e cole o texto final)**
```markdown
## 4. Sua Missão: Projetar a Próxima Geração

Com base em todo o contexto de backend fornecido acima:

Sua primeira tarefa é analisar o material e me apresentar uma **Proposta de Arquitetura de Frontend**. Esta proposta deve incluir:

1.  **Recomendação de Tecnologia (O "Stack"):** Justifique qual seria o stack de frontend ideal (React, Vue, etc.) para esta aplicação.
2.  **Arquitetura de Componentes:** Descreva como você quebraria a UI em componentes reutilizáveis.
3.  **Estratégia de Gerenciamento de Estado:** Recomende uma abordagem para gerenciar os dados da simulação na interface.
4.  **Integração com o Backend:** Proponha a estrutura de uma API REST (usando FastAPI) que serviria como a "ponte" entre o `core/` e o novo frontend.

Após eu aprovar sua proposta de arquitetura, sua segunda tarefa será gerar um **Plano de Implementação Detalhado e Sequencial**, que usarei para guiar a construção do frontend.

Por favor, comece com a Proposta de Arquitetura.
```

---

### **Resultado Final**

Ao final, você terá um único arquivo `contexto_para_claude.md` que é um dossiê completo, profissional e perfeitamente estruturado. Ele:

1.  **Respeita o limite de contexto** focando apenas no código essencial.
2.  **Dá à IA o mapa** antes de mostrar o território.
3.  **Consolida o conhecimento** que estava espalhado, mesmo que os arquivos estivessem vazios.
4.  **Termina com uma instrução clara e profissional**, guiando a IA para o próximo passo lógico.

Esta é a maneira mais eficiente e robusta de delegar uma tarefa de arquitetura complexa a uma IA.