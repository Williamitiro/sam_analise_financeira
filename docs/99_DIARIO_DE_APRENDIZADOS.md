# Diário de Aprendizados e Decisões de Arquitetura

Este documento serve como um log de decisões importantes, problemas encontrados e as soluções aplicadas ao longo do desenvolvimento do projeto SAM. O objetivo é manter um registro histórico que possa ser consultado no futuro para entender o "porquê" por trás das escolhas técnicas e de arquitetura.

---

### **Data: 2025-11-18**

**Problema:** A documentação do projeto estava espalhada por múltiplos arquivos e pastas (`README.md`, `_archive/`, `plano_estrategico/`, `_checkpoints/`), tornando difícil para um novo desenvolvedor (ou para o próprio time no futuro) entender o estado atual, a visão de alto nível, a arquitetura e o roadmap. Havia redundância e informação desatualizada.

**Decisão/Solução:**
1.  **Centralizar toda a documentação:** Foi decidido criar uma única fonte de verdade na pasta `docs/` na raiz do projeto.
2.  **Estruturar a Documentação:** A nova estrutura foi organizada em arquivos temáticos para facilitar a consulta:
    -   `00_VISAO_GERAL_DO_PROJETO.md`: O "quê", o "porquê" e "para quem".
    -   `01_ARQUITETURA_E_TECNOLOGIAS.md`: O "como" técnico, detalhando o stack e a estrutura.
    -   `02_ROADMAP_DE_DESENVOLVIMENTO.md`: O "quando", consolidando os planos de implementação e o status atual.
    -   `99_DIARIO_DE_APRENDIZADOS.md`: Este próprio arquivo, para registrar o "porquê" das decisões futuras.
3.  **Arquivar o Legado:** Todos os arquivos de planejamento antigos e checkpoints foram movidos para a pasta `_archive/` para limpar a raiz do projeto, mas ainda manter o histórico se necessário.
4.  **Simplificar o `README.md`:** O `README.md` principal será simplificado para ser um ponto de entrada, direcionando os leitores para a nova pasta `docs/`.

**Racional:** Esta reorganização cria um ambiente de desenvolvimento mais limpo e profissional. Ela reduz a carga cognitiva para qualquer pessoa que interaja com o projeto, garantindo que a informação seja fácil de encontrar, consistente e atualizada.
