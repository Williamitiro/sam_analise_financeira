# Checkpoint: Re-arquitetura do Frontend SAM

**Data:** 16 de novembro de 2025
**Status:** Concluído

## Resumo da Sessão

Nesta sessão, tomamos uma decisão estratégica crucial: **pivotar de uma implementação incremental para uma reconstrução completa do frontend**. Essa decisão foi baseada em uma proposta de arquitetura profissional que recebemos, que nos forneceu um blueprint claro para uma aplicação de alta qualidade.

O foco foi realizar um "reset" controlado do ambiente de frontend, preparando o terreno para a nova arquitetura, configurando todas as ferramentas e criando a estrutura de pastas que guiará o desenvolvimento futuro.

## Por que a Mudança? (O "Porquê")

Continuar com a abordagem anterior (componentes simples em MUI) seria rápido a curto prazo, mas criaria dívida técnica e dificultaria a escalabilidade. A nova arquitetura, embora exija um investimento inicial maior em configuração, nos oferece:

-   **Escalabilidade:** Uma estrutura que suporta o crescimento do projeto sem se tornar caótica.
-   **Manutenibilidade:** Código organizado por funcionalidade (`features`), facilitando encontrar e modificar a lógica de negócio.
-   **Performance:** Escolha de bibliotecas focadas em performance, como `React Hook Form` e `Zustand`.
-   **Developer Experience (DX):** Ferramentas modernas como Vite e Tailwind CSS que aceleram o desenvolvimento e a estilização.

Adotar este padrão desde o início é um investimento que se paga ao longo da vida do projeto, criando um ativo de código limpo e profissional.

## A Nova Arquitetura (O "Quê")

A base do nosso novo frontend é um stack de tecnologias modernas, escolhidas especificamente para os desafios de uma aplicação rica em dados como o SAM.

### Stack Tecnológico e o Papel de Cada Peça:

-   **Vite:** Como nossa ferramenta de build, oferece um servidor de desenvolvimento quase instantâneo e um processo de build otimizado.
-   **React + TypeScript:** A base da nossa UI. React pela sua maturidade e ecossistema, e TypeScript para garantir a segurança de tipos, crucial em um projeto com modelos de dados complexos.
-   **Tailwind CSS:** Para estilização. Em vez de escrever CSS tradicional, criamos interfaces customizadas compondo classes utilitárias diretamente no HTML. Isso nos dá velocidade e consistência visual.
-   **Zustand:** Para gerenciamento de estado global. É uma alternativa mais simples e leve ao Redux, ideal para compartilhar estados como os dados da projeção ou as configurações do usuário entre componentes distantes.
-   **TanStack (React) Query:** Para comunicação com a API. Ele abstrai toda a complexidade de data fetching, gerenciando cache, estados de loading/erro e sincronização de dados em segundo plano de forma automática.
-   **React Hook Form + Zod:** Para o formulário de configuração. `React Hook Form` otimiza a performance de formulários complexos (evitando re-renders desnecessários) e `Zod` permite criar esquemas de validação robustos e seguros em TypeScript.
-   **Recharts / Plotly.js:** Uma abordagem híbrida para gráficos. `Recharts` para gráficos mais comuns e `Plotly.js` para visualizações avançadas (como Waterfall e Sankey), garantindo que tenhamos a ferramenta certa para cada tipo de dado.

## O Processo de Implementação (O "Como")

Seguimos um processo metódico e controlado para a transição:

1.  **Limpeza:** Arquivamos documentos antigos para manter o projeto organizado.
2.  **Reset:** O usuário removeu a pasta `frontend` antiga para garantir um início limpo.
3.  **Geração de Configuração:** Em vez de executar comandos de instalação, geramos diretamente os arquivos de configuração (`package.json`, `tailwind.config.js`, etc.) já com todo o setup necessário. Isso garante a reprodutibilidade do ambiente.
4.  **Instalação pelo Usuário:** O usuário assumiu a responsabilidade de executar `npm install`, baixando as dependências definidas.
5.  **Criação da Estrutura:** Criamos programaticamente toda a nova e detalhada estrutura de diretórios, estabelecendo o "esqueleto" da aplicação.

## Importância de Cada Etapa

-   **Limpeza e Reset:** Essencial para evitar conflitos e garantir que estamos construindo sobre uma base limpa, sem resquícios da implementação anterior.
-   **Definição do `package.json`:** É o "contrato" do projeto. Centraliza todas as dependências e suas versões, garantindo que qualquer desenvolvedor possa recriar o ambiente exato.
-   **Estrutura de Pastas:** É a arquitetura física do nosso código. Uma boa estrutura separa as responsabilidades, facilita a navegação e torna o projeto intuitivo para quem chega. É um dos pilares da manutenibilidade.

## Próximos Passos

Com o ambiente totalmente configurado, o caminho está livre para o desenvolvimento da aplicação em si:

1.  **Implementar o Cliente API:** Criar o serviço `axios` em `src/lib/api` para se comunicar com o backend.
2.  **Construir o Layout Principal:** Desenvolver os componentes de layout como `AppLayout`, `Sidebar` e `Header` em `src/components/layout`.
3.  **Desenvolver a Página de Configuração:** Iniciar a `ConfigurationPage`, utilizando `React Hook Form` para os campos de input e `Zustand` para gerenciar o estado do formulário de configuração.
