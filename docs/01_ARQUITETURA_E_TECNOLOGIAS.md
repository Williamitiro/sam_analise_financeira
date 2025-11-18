# Arquitetura e Tecnologias

## 1. Visão Geral da Arquitetura

O SAM Financial Model é construído sobre uma arquitetura moderna de aplicação web, separando claramente as responsabilidades entre o backend e o frontend.

-   **Backend:** Um motor de análise e projeção escrito em **Python**, exposto através de uma **API RESTful** construída com **FastAPI**. É responsável por toda a lógica de negócio, cálculos financeiros, simulações e persistência de dados.
-   **Frontend:** Uma Single-Page Application (SPA) interativa e responsiva, construída com **React (TypeScript)** e **Vite**. É responsável por toda a interface do usuário, visualização de dados e interação com o usuário.
-   **Comunicação:** A comunicação entre o frontend e o backend é feita exclusivamente através de chamadas HTTP para a API FastAPI, utilizando o formato JSON.

Este desacoplamento garante que cada parte do sistema possa evoluir de forma independente e permite que, no futuro, outros clientes (ex: um aplicativo móvel, um CLI) possam consumir a mesma API do backend.

## 2. Arquitetura de 3 Camadas do Backend

O backend segue uma arquitetura em três camadas para garantir organização, manutenibilidade e escalabilidade.

1.  **Camada de Configuração (`core/builders`):**
    -   **Responsabilidade:** Coletar e validar as entradas do usuário de forma estruturada.
    -   **Componentes:** Uma série de "Builders" (ex: `TeamBuilder`, `RevenueBuilder`) que guiam o usuário na configuração de cada aspecto do modelo financeiro.
    -   **Saída:** Um objeto de configuração (`ConfigFinanceira`) único e validado.

2.  **Camada de Processamento (`core/engine` e `core/analytics`):**
    -   **Responsabilidade:** Executar a lógica de negócio principal.
    -   **Componentes:**
        -   `MotorProjecaoFinanceira`: Recebe o objeto de configuração e gera a projeção financeira mês a mês.
        -   `InsightsEngine`: Analisa os resultados da projeção para gerar alertas, insights e recomendações automáticas.
        -   Módulos de análise avançada (`MonteCarlo`, `Sensitivity`, `Cohorts`).
    -   **Saída:** DataFrames do Pandas com os resultados completos, dicionários de KPIs e listas de insights.

3.  **Camada de Apresentação (API - `main.py`):**
    -   **Responsabilidade:** Expor os resultados do processamento para o mundo exterior.
    -   **Componentes:** Endpoints FastAPI (ex: `/projecao`) que orquestram a chamada das camadas inferiores e serializam a saída em formato JSON.

## 3. Stack de Tecnologias

### Backend
| Tecnologia | Propósito |
| :--- | :--- |
| **Python 3.10+** | Linguagem principal de desenvolvimento. |
| **FastAPI** | Framework web para construção da API RESTful, escolhido por sua performance e tipagem. |
| **Pydantic** | Validação de dados e gerenciamento de configurações da API. |
| **Pandas** | Manipulação e análise de dados em memória, a espinha dorsal do motor de projeção. |
| **NumPy** | Cálculos numéricos de alta performance. |
| **Uvicorn** | Servidor ASGI para rodar a aplicação FastAPI. |

### Frontend
| Tecnologia | Propósito |
| :--- | :--- |
| **React 18+** | Biblioteca para construção da interface do usuário. |
| **TypeScript** | Garante a segurança de tipos (type safety) e melhora a manutenibilidade. |
| **Vite** | Ferramenta de build extremamente rápida para desenvolvimento e produção. |
| **Tailwind CSS** | Framework CSS utility-first para estilização rápida e consistente. |
| **Zustand** | Gerenciamento de estado global, escolhido pela simplicidade e performance. |
| **TanStack Query** | Gerenciamento de cache e requisições à API (data fetching). |
| **React Hook Form** | Construção e validação de formulários complexos. |
| **Recharts** | Biblioteca principal para gráficos declarativos e customizáveis. |
| **Plotly.js** | Biblioteca complementar para gráficos avançados (Sankey, Waterfall, Heatmaps). |
| **shadcn/ui & Radix UI** | Componentes de UI base, acessíveis e sem estilo pré-definido. |
| **Framer Motion** | Biblioteca para animações e micro-interações. |
| **Zod** | Validação de schemas e dados no frontend. |

## 4. Estrutura de Pastas do Projeto

A estrutura de pastas do projeto é organizada para refletir a separação de responsabilidades:

```
sam_analise_financeira/
│
├── core/                 # Lógica de negócio principal (Backend)
│   ├── analytics/        # Módulos de análise avançada
│   ├── builders/         # Construtores de configuração
│   ├── config.py         # Definição do objeto de configuração
│   └── engine.py         # Motor de projeção principal
│
├── frontend/             # Aplicação da interface do usuário (Frontend)
│   └── src/
│       ├── app/          # Configuração da aplicação (router, providers)
│       ├── components/   # Componentes React reutilizáveis (UI, charts, layout)
│       ├── features/     # Lógica de features específicas (config, projeção)
│       ├── hooks/        # Hooks React globais
│       ├── lib/          # Utilitários e clientes de API
│       ├── pages/        # Componentes de página (rotas)
│       └── stores/       # Stores de estado global (Zustand)
│
├── main.py               # Ponto de entrada da API FastAPI
│
├── data/                 # Dados do usuário (cenários salvos, etc.)
├── notebooks/            # Jupyter Notebooks para pesquisa e análise
├── docs/                 # Documentação do projeto
└── tests/                # Testes automatizados
```
