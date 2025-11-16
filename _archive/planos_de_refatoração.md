# Plano de Refatoração: `app/main.py` e Integração dos Builders

## Objetivo Principal

Evoluir a aplicação de um simulador com parâmetros simples para uma plataforma completa de modelagem de negócios com regras dinâmicas, utilizando a nova arquitetura de Builders. O objetivo é tornar a interface do usuário tão flexível e poderosa quanto o motor de projeção recém-refatorado.

## Diagnóstico do `main.py` Atual

- **Problema de Layout:** Toda a interface de configuração está atualmente na barra lateral (`sidebar`). Isso a torna longa, poluída e inadequada para as configurações complexas que os builders permitem (ex: adicionar múltiplas fases de marketing, múltiplos cargos com gatilhos).
- **Problema de Lógica:** A interface manipula diretamente os atributos do objeto `config` (ex: `config.churn_mensal = st.slider(...)`). Isso cria um acoplamento forte e não escala para regras de negócio complexas e dinâmicas.
- **Problema de Usabilidade:** Os menus laterais (as páginas do Streamlit) não são utilizados para configuração, centralizando tudo de forma ineficiente. A experiência do usuário é limitada a mover sliders e preencher campos simples, não refletindo a capacidade de modelar um negócio real.

---

## Plano de Refatoração em Fases

### Fase 1: Reestruturação da Arquitetura da UI (A Fundação)

O objetivo desta fase é preparar a estrutura da aplicação para receber a nova interface de configuração, separando as responsabilidades e limpando o código existente.

1.  **Criar a Página de Configurações (`11_Configuracoes.py`):**
    -   Criar um novo arquivo em `app/pages/11_Configuracoes.py`.
    -   Esta página se tornará o local central para **toda** a configuração do modelo financeiro. Ela conterá a UI para interagir com todos os builders.

2.  **Limpar a `sidebar` e o `main.py`:**
    -   A `sidebar` será drasticamente simplificada. Todos os `st.expander` com sliders e inputs de parâmetros de negócio (Funil, Receita, Custos, etc.) serão **removidos**.
    -   A `sidebar` manterá apenas controles **globais** da aplicação:
        -   Um seletor para carregar **cenários salvos** (Padrão, Otimista, Pessimista).
        -   O botão principal **"🚀 RODAR SIMULAÇÃO"**.
    -   O arquivo `app/main.py` se tornará principalmente a "home" da aplicação, responsável por exibir os dashboards (as abas horizontais que já funcionam). Toda a lógica de configuração de parâmetros sairá dele.

3.  **Gerenciamento de Estado Centralizado (`st.session_state`):**
    -   O objeto `st.session_state.config` continuará sendo a única fonte da verdade para a configuração.
    -   A nova página `11_Configuracoes.py` será a principal responsável por **modificar** este objeto através dos builders.
    -   As outras páginas (`main.py` e futuros dashboards) serão apenas **leitoras** dos resultados da simulação (`st.session_state.df_projecao`, `st.session_state.kpis`), que são gerados a partir do `config`.

### Fase 2: Implementação da UI dos Builders na Nova Página

Dentro de `app/pages/11_Configuracoes.py`, usaremos `st.tabs` ou `st.expander` para organizar a UI, criando uma seção para cada área do negócio, correspondendo a um builder.

1.  **UI para `TeamBuilder` (Exemplo Detalhado):**
    -   Criar um `st.expander("👥 Planejamento de Equipe")`.
    -   Dentro dele, exibir os cargos já configurados (lendo de `st.session_state.config.cargos_planejados` ou uma estrutura similar).
    -   Usar um `st.form` para "Adicionar Novo Cargo". O formulário terá:
        -   Inputs para os detalhes do cargo: `st.text_input("Nome do Cargo")`, `st.number_input("Salário Base")`, `st.selectbox("Tipo", ["CLT", "PJ"])`.
        -   Uma sub-seção para "Gatilho de Contratação" com `st.selectbox("Contratar quando", ["MRR atingir", "Nº de Usuários atingir", "Mês específico"])` e um `st.number_input` para o valor do gatilho.
    -   Quando o formulário for submetido, o código **não vai mais mexer no `config` diretamente**. Em vez disso, ele vai instanciar o `TeamBuilder`, usar seus métodos (`builder.add_clt(...)`, `builder.quando_mrr_atingir(...)`) para construir a lista de cargos e, ao final, chamar `builder.build()` para atualizar o `st.session_state.config`.

2.  **UI para `MarketingBuilder`:**
    -   Criar um `st.expander("📢 Estratégia de Marketing")`.
    -   Permitir que o usuário defina as 4 fases de marketing (Validação, Crescimento, etc.), adicionando-as a uma lista. Cada fase terá seus próprios inputs (duração, tipo de orçamento, valor).
    -   Isso chamará os métodos do `MarketingBuilder` como `.fase_validacao(...)`, `.fase_crescimento(...)`.

3.  **UI para `InfraBuilder`:**
    -   Criar um `st.expander("🏗️ Infraestrutura Escalável")`.
    -   Permitir a definição de "Tiers", onde para cada tier o usuário pode adicionar "Componentes" com seu custo (ex: Tier 1 -> Componente "VPS AWS" com custo de R$ 150).
    -   Isso chamará os métodos `.criar_tier(...)` e `.add_componente(...)` do `InfraBuilder`.

4.  **Repetir o Padrão:** O mesmo padrão será aplicado para os outros builders (Capital, Revenue, COGS), criando uma interface rica e modular que espelha a arquitetura do `README.md`.

### Fase 3: Conexão Final e Fluxo de Execução

1.  **Botão "Rodar Simulação":** Este botão, agora na `sidebar`, será o gatilho final para a projeção.
2.  **Fluxo de Execução:**
    -   Ao clicar no botão, o `app/main.py` (ou um módulo de controle) pega o objeto `st.session_state.config` (que foi totalmente configurado pela página `11_Configuracoes.py`).
    -   Instancia o motor: `motor = MotorProjecaoFinanceira(st.session_state.config)`.
    -   Executa a projeção: `df = motor.executar_projecao(...)`.
    -   Calcula os KPIs: `kpis = motor.calcular_kpis()`.
    -   Salva os resultados `df` e `kpis` no `st.session_state`.
    -   O Streamlit automaticamente recarrega a página, e os dashboards exibirão os novos resultados.
    -   Pode-se adicionar uma navegação automática para a página principal de dashboard após a conclusão da simulação.

### Mitigação de Riscos

-   **Complexidade da UI:** O problema de uma UI muito complexa será mitigado usando uma página dedicada (`11_Configuracoes.py`) e organizando cada builder em seu próprio `st.expander` ou `st.tab`, mantendo a interface limpa e organizada.
-   **Gerenciamento de Estado:** O uso de `st.form` para adicionar novas regras (como um novo cargo) evitará que a aplicação recarregue a cada interação com um widget. O estado da configuração será consolidado no objeto `st.session_state.config` e só será usado para a simulação quando o usuário explicitamente clicar no botão para rodar.
-   **Manutenibilidade:** Ao separar a UI de configuração da UI de visualização e ao fazer com que a UI chame os métodos dos builders em vez de manipular o `config` diretamente, o código se torna muito mais limpo, legível e fácil de manter.
