# 🏆 God Level Coder Challenge

## O Problema

Donos de restaurantes gerenciam operações complexas através de múltiplos canais (presencial, iFood, Rappi, app próprio). Eles têm dados de **vendas, produtos, clientes e operações**, mas não conseguem extrair insights personalizados para tomar decisões de negócio.

Ferramentas como Power BI são genéricas demais. Dashboards fixos não respondem perguntas específicas. **Como empoderar donos de restaurantes a explorarem seus próprios dados?**

## Seu Desafio

Construa uma solução que permita donos de restaurantes **criarem suas próprias análises** sobre seus dados operacionais. Pense: "Power BI para restaurantes" ou "Metabase específico para food service".

### O que esperamos

Uma plataforma onde um dono de restaurante possa:
- Visualizar métricas relevantes (faturamento, produtos mais vendidos, horários de pico)
- Criar dashboards personalizados sem escrever código
- Comparar períodos e identificar tendências
- Extrair valor de dados complexos de forma intuitiva

### O que você recebe

- Script para geração de **500.000 vendas** de 6 meses (50 lojas, múltiplos canais)
- Schema PostgreSQL com dados realistas de operação
- Liberdade total de tecnologias e arquitetura
- Liberdade total no uso de AI e ferramentas de geração de código

### O que você entrega

1. Uma solução funcionando (deployed ou local) - com frontend e backend adequados ao banco fornecido
2. Documentação de decisões arquiteturais
3. Demo em vídeo (5-10 min) explicando sua abordagem - mostrando a solução funcional e deployada / rodando na sua máquina, apresentando-a no nível de detalhes que julgar relevante
4. Código bem escrito e testável

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [PROBLEMA.md](./PROBLEMA.md) | Contexto detalhado, persona Maria, dores do usuário |
| [DADOS.md](./DADOS.md) | Schema completo, padrões, volume de dados |
| [AVALIACAO.md](./AVALIACAO.md) | Como avaliaremos sua solução |
| [FAQ.md](./FAQ.md) | Perguntas frequentes |
| [QUICKSTART.md](./QUICKSTART.md) | Tutorial rápido para começar o desafio |

## Avaliação

**Não** estamos avaliando se você seguiu instruções específicas.  
**Sim** estamos avaliando:
- Pensamento arquitetural e decisões técnicas
- Qualidade da solução para o problema do usuário
- Performance e escala
- UX e usabilidade
- Metodologia de trabalho e entrega


## Prazo

Até 03/11/2025 às 23:59.

## Submissão

Mande um email para gsilvestre@arcca.io

Com:
- Link do repositório (público ou nos dê acesso)
- Link do vídeo demo (5-10 min)
- Link do deploy (opcional mas valorizado)
- Documento de decisões arquiteturais



## 🚀 Minha Solução

Esta seção detalha a abordagem técnica e as decisões de arquitetura tomadas para resolver o desafio "God Level Coder".

### Arquitetura e Tecnologias

A solução foi desenvolvida seguindo uma arquitetura desacoplada, com um backend robusto e um frontend interativo, priorizando a manutenibilidade e escalabilidade.

-   **Backend:**
    -   A API foi construída em Python (utilizando um framework como FastAPI/Flask).
    -   **Princípios de Design:** Foram aplicados conceitos de **Domain-Driven Design (DDD)** para modelar o domínio complexo do negócio e os princípios **SOLID** para refatorar as classes, resultando em um código mais limpo, coeso e extensível.

-   **Frontend:**
    -   A interface do usuário foi desenvolvida para ser intuitiva e permitir a exploração de dados de forma dinâmica.

-   **Banco de Dados:**
    -   O banco de dados PostgreSQL fornecido foi hospedado na **Supabase**, garantindo uma infraestrutura de dados gerenciada, segura e escalável.

### Deploy da Aplicação

Para garantir a disponibilidade e performance, a aplicação foi distribuída em diferentes serviços de nuvem, cada um especializado em sua função:

-   **Backend:** O deploy da API foi realizado no **Render**, uma plataforma que facilita a publicação de serviços web e workers.
-   **Frontend:** A interface do usuário está hospedada na **Vercel**, otimizada para performance e entrega contínua de aplicações frontend.
-   **Banco de Dados:** O schema e os dados foram migrados para a **Supabase**. O processo envolveu a criação de um dump do banco de dados local (gerado via Docker) e a restauração no ambiente da Supabase, conforme os comandos abaixo:
    ```bash
    # 1. Gerar o backup do banco de dados local rodando em Docker
    docker compose exec postgres pg_dump -U challenge -d challenge_db --clean --if-exists --no-owner > backup-perfeito.sql

    # 2. Restaurar o backup no banco de dados da Supabase
    psql "SUA_CONNECTION_STRING_SUPABASE" -f backup-perfeito.sql
    ```

### Demonstração e Documentação da API

-   **🎥 Vídeo Demo (YouTube):** Uma demonstração completa da solução, explicando a arquitetura e mostrando a plataforma em funcionamento, está disponível no YouTube.
    -   **[Assista ao vídeo aqui](https://www.youtube.com/watch?v=MEU_LINK_AQUI)**

-   **📖 Documentação da API (Postman):** A documentação detalhada de todos os endpoints da API, incluindo exemplos de requisições e respostas, foi criada no Postman e pode ser acessada através do link abaixo.
    -   **[Acessar a documentação no Postman](https://documenter.getpostman.com/view/17743876/2sB3WpShAH)**

### Melhorias Futuras e Pontos de Evolução

Embora a solução atual seja funcional e robusta, existem oportunidades de melhoria contínua, especialmente no frontend.


#### 1. Organização e Escopo de Estilos (CSS)

Atualmente, os estilos CSS podem estar em arquivos globais ou com escopo pouco definido. Para melhorar a manutenibilidade e evitar conflitos em um projeto em crescimento, poderíamos adotar uma das seguintes estratégias:

-   **CSS Modules:** Isolar os estilos por componente, gerando nomes de classes únicos e evitando que um estilo afete outro componente inesperadamente.
-   **Styled-components (CSS-in-JS):** Escrever o CSS diretamente dentro dos componentes JavaScript (React/Vue), o que melhora a co-localização do código e facilita a criação de lógicas de estilo dinâmicas.
-   **Tailwind CSS:** Utilizar um framework de classes utilitárias para construir interfaces rapidamente sem sair do HTML, promovendo consistência visual e reduzindo a necessidade de escrever CSS customizado.

A implementação de uma dessas abordagens tornaria os componentes do frontend mais independentes, reutilizáveis e fáceis de manter.

#### 2. Testes de Frontend

Adicionar uma suíte de testes unitários e de integração para os componentes do frontend usando ferramentas como Jest e React Testing Library para garantir a estabilidade da interface do usuário conforme novas funcionalidades são adicionadas.

#### 3. Otimização de Performance com Elasticsearch

Explorar a integração mais profunda com **Elasticsearch** para indexação e busca de dados complexos. Isso permitiria consultas analíticas de alta performance e em tempo real, especialmente para cenários que exigem agregações e filtros dinâmicos sobre grandes volumes de dados, aliviando a carga do banco de dados transacional.

#### 4. Funcionalidades Avançadas com Inteligência Artificial

Expandir a solução com capacidades de IA para oferecer insights ainda mais acionáveis:

-   **Identificação de Clientes Inativos:** Implementar modelos de IA para analisar o histórico de compras e identificar clientes que não realizam pedidos há um determinado período. Isso permitiria que Maria e sua equipe pudessem planejar campanhas de reengajamento direcionadas.
-   **Geração de Relatórios Detalhados em PDF:** Desenvolver um serviço que, com base em análises e insights gerados por IA (por exemplo, identificação de padrões de venda, anomalias ou previsões), possa compilar e exportar relatórios personalizados em formato PDF. Esses relatórios ofereceriam uma visão aprofundada e acionável para os gestores, facilitando a tomada de decisões estratégicas.

---
