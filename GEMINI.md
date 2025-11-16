# SAM Financial Model - Gemini Agent Context

## Core Directives & Modus Operandi

To ensure the highest quality and act as an experienced senior developer, the following principles must be adhered to at all times:

1.  **Analyze Root Cause:** Do not just fix symptoms. Before writing any code, investigate the "why" behind a bug or a feature request. Understand the underlying problem.
2.  **Holistic (Macro) View:** Before making changes, step back and analyze the entire system. Consider the macro-level impact. How does this change affect other modules, dependencies, and the overall architecture?
3.  **Dependency and Connection Awareness:** Explicitly map out the connections between components. Understand the data flow, internal and external API contracts, and the complete environment (development, testing, production).
4.  **Gold-Standard Practices:** All code, refactoring, and architectural decisions must align with current, industry-accepted "gold standards" for the technologies in use. This includes writing clean, maintainable, and testable code.
5.  **Surgical Precision:** Changes should be "surgical." They must be precise, targeted, and minimally disruptive, while still fully addressing the root cause. Avoid broad, sweeping changes unless a major refactoring is the explicitly stated goal.
6.  **Mock-First Development:** For the frontend, always prioritize building the UI and UX with mock data first. This validates the user experience and allows for parallel development, only connecting to the live API once the interface is complete and approved.

## Project Overview (Current State)

**Goal:** To build a sophisticated, enterprise-grade financial analysis and business simulation tool named "SAM Financial Model".

**Architecture:** The project has a modern, decoupled, two-part architecture:

*   **Backend (Python / FastAPI):**
    *   A robust Python backend powered by the **FastAPI** framework.
    *   All core business logic, financial calculations, and analysis are encapsulated in the `core/` directory, which functions as a pure, headless engine.
    *   It exposes its full functionality through a primary API endpoint: `POST /projecao`.

*   **Frontend (React / TypeScript / Vite):**
    *   A professional, high-performance frontend application built with **React**, **TypeScript**, and **Vite**.
    *   The UI is styled using **Tailwind CSS** for a utility-first, custom design approach.
    *   The old Streamlit application located in the `app/` directory is **deprecated** and is no longer used. All new development occurs in the `frontend/` directory.

## Key Technologies & Conventions

The project follows a professional architecture defined in `plano_estrategico/implementacao.md` and `plano_estrategico/plano_overview_dashbord.md`.

*   **State Management (`Zustand`):** A lightweight, centralized store for managing global UI state (filters, projection results).
*   **Data Fetching (`TanStack Query`):** Manages all API communication, providing caching, background refetching, and streamlined handling of loading/error states.
*   **Forms (`React Hook Form` + `Zod`):** A high-performance solution for building and validating the complex configuration forms.
*   **Data Visualization (`Recharts` + `Plotly.js`):** A hybrid strategy using Recharts for common charts (Line, Bar) and Plotly.js for advanced visualizations (Waterfall, Sankey, Heatmaps).
*   **UI Components:** A mix of custom-built components and headless primitives from **Radix UI**, styled with Tailwind CSS.
*   **Folder Structure:** A feature-sliced architecture is used within `frontend/src/`, with clear separation between `pages`, reusable `components`, business logic `features`, and shared utilities `lib`.
*   **API Client (`axios`):** A dedicated API client is implemented in `frontend/src/lib/api/` to handle all requests to the backend.
