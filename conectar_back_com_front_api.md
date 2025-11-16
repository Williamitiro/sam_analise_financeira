# Manual Passo a Passo: Conectando um Backend Python (FastAPI) a um Frontend React Profissional

Este documento detalha o processo completo para configurar um ambiente de frontend moderno e robusto, baseado em uma arquitetura profissional, para consumir uma API de backend. O objetivo é criar uma base de projeto escalável, manutenível e com as melhores práticas do mercado.

## Fase 1: Preparação e Limpeza do Ambiente

Um bom projeto começa com um espaço de trabalho organizado. Antes de iniciar o novo frontend, realizamos uma limpeza para arquivar artefatos antigos e remover a estrutura anterior.

### 1.1. Arquivamento de Documentos Antigos

Documentos de sessões de desenvolvimento anteriores, rascunhos e relatórios foram movidos para uma pasta `_archive` para não poluir o diretório raiz.

**Comando utilizado (PowerShell):**
```powershell
Move-Item -Path @("arquitetura_frontend.md", "cli_gemini.md", "context.md", "CONTEXTO_E_DIARIO.md", "decisoes_tecnicas.md", "modelo_negocio_SAM.md", "planos_de_refatoração.md", "project_structure.txt", "prompt_claude.md", "relatorio_inicial.md", "roadmap.md", "scripts_completos.md") -Destination "_archive/"
```

### 1.2. Remoção do Frontend Antigo

A pasta `frontend` antiga, que serviu como prova de conceito, foi removida manualmente pelo usuário. Este passo é crucial para garantir que não haja conflitos com a nova estrutura.

**Ação manual:** Apagar a pasta `frontend` existente.

## Fase 2: Criação do Novo Projeto Frontend (Vite + React + TS)

Utilizamos o Vite para criar um projeto React com TypeScript. O Vite é uma ferramenta de build extremamente rápida que oferece uma experiência de desenvolvimento superior.

**Ação do usuário:** No terminal, na raiz do projeto, execute o comando:
```bash
# Este comando cria uma nova pasta 'frontend' com a estrutura base do projeto
npm create vite@latest frontend -- --template react-ts
```

## Fase 3: Definição das Dependências do Projeto

O coração de um projeto Node.js está no seu arquivo `package.json`. Em vez de instalar as dependências uma a uma, nós geramos este arquivo já com todas as bibliotecas da nossa arquitetura-alvo.

### 3.1. Conteúdo do `package.json`

Este arquivo foi criado em `frontend/package.json`:
```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@hookform/resolvers": "^3.3.4",
    "@radix-ui/react-slot": "^1.0.2",
    "@tanstack/react-query": "^5.29.2",
    "axios": "^1.6.8",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "date-fns": "^3.6.0",
    "framer-motion": "^11.0.28",
    "lucide-react": "^0.368.0",
    "plotly.js": "^2.31.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.51.3",
    "react-plotly.js": "^2.6.0",
    "recharts": "^2.12.4",
    "tailwind-merge": "^2.2.2",
    "zod": "^3.22.4",
    "zustand": "^4.5.2"
  },
  "devDependencies": {
    "@tanstack/react-query-devtools": "^5.29.2",
    "@types/node": "^20.12.7",
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@types/react-plotly.js": "^2.6.3",
    "@typescript-eslint/eslint-plugin": "^7.2.0",
    "@typescript-eslint/parser": "^7.2.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "eslint": "^8.57.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.6",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.2.2",
    "vite": "^5.2.0"
  }
}
```

**Principais Tecnologias:**
- **`@tanstack/react-query`**: Para comunicação com a API, gerenciamento de cache, e estados de loading/erro.
- **`zustand`**: Para gerenciamento de estado global de forma simples e eficiente.
- **`react-hook-form`** e **`zod`**: Para criação e validação de formulários complexos com alta performance.
- **`tailwindcss`**: Para estilização via classes utilitárias, permitindo criar interfaces customizadas rapidamente.
- **`recharts`** e **`plotly.js`**: Para visualização de dados e gráficos.

### 3.2. Instalação das Dependências

**Ação do usuário:** Navegue até a nova pasta e instale as dependências.
```bash
# 1. Entre na pasta do frontend
cd frontend

# 2. Instale todas as dependências listadas no package.json
npm install
```

## Fase 4: Configuração do Tailwind CSS

Para que o Tailwind funcione, precisamos de 3 arquivos de configuração.

1.  **`frontend/tailwind.config.js`**: Diz ao Tailwind onde encontrar os arquivos que usam suas classes.
    ```javascript
    /** @type {import('tailwindcss').Config} */
    export default {
      content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    }
    ```
2.  **`frontend/postcss.config.js`**: Configura os plugins do PostCSS, que processa o CSS.
    ```javascript
    export default {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    }
    ```
3.  **`frontend/src/index.css`**: Importa as camadas base do Tailwind. O conteúdo deste arquivo deve ser apenas:
    ```css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    ```

## Fase 5: Implementação da Arquitetura de Pastas

Uma estrutura de pastas bem definida é a espinha dorsal de um projeto escalável. Criamos a seguinte estrutura para separar responsabilidades e facilitar a localização de código.

**Comando executado (PowerShell):**
```powershell
$folders = @(
    "frontend/src/app", "frontend/src/assets", "frontend/src/components/ui", "frontend/src/components/layout", "frontend/src/components/forms", "frontend/src/components/metrics", "frontend/src/components/charts", "frontend/src/components/tables", "frontend/src/components/drill-down", "frontend/src/components/insights", "frontend/src/components/filters", "frontend/src/components/loading", "frontend/src/features/configuration/hooks", "frontend/src/features/configuration/stores", "frontend/src/features/configuration/types", "frontend/src/features/configuration/utils", "frontend/src/features/projection/hooks", "frontend/src/features/projection/stores", "frontend/src/features/projection/types", "frontend/src/features/projection/utils", "frontend/src/features/scenarios/hooks", "frontend/src/features/scenarios/stores", "frontend/src/features/scenarios/types", "frontend/src/features/analytics/hooks", "frontend/src/features/analytics/types", "frontend/src/hooks", "frontend/src/lib/api", "frontend/src/lib/utils", "frontend/src/lib/theme", "frontend/src/pages/ConfigurationPage/sections", "frontend/src/pages/ResultsPage/dashboards", "frontend/src/styles", "frontend/src/types"
)
$folders | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force }
```

**Principais Diretórios:**
- `src/components`: Para componentes de UI reutilizáveis (botões, cards, etc.), seguindo o Atomic Design.
- `src/pages`: Cada página principal da aplicação (Configuração, Resultados).
- `src/features`: Lógica de negócio, hooks e stores específicos de uma funcionalidade (Configuração, Projeção).
- `src/lib`: Código compartilhado e utilitários (cliente API, formatação, etc.).
- `src/hooks`: Hooks React globais e reutilizáveis.

## Fase 6: Verificação e Próximos Passos

Com a estrutura pronta e as dependências instaladas, o ambiente de desenvolvimento está completo.

**Ação do usuário:** Inicie o servidor de desenvolvimento.
```bash
# Dentro da pasta 'frontend'
npm run dev
```

Ao acessar o endereço `http://localhost:5173` no seu navegador, você deverá ver a página inicial padrão do Vite. Embora pareça simples, toda a arquitetura profissional já está configurada e pronta para receber os componentes da aplicação.

O próximo passo é começar a desenvolver a lógica de conexão com a API em `src/lib/api/client.ts` e construir os componentes de layout em `src/components/layout`.
