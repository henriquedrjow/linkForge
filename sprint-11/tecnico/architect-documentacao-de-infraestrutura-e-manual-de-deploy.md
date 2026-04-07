# Documentação de Infraestrutura e Manual de Deploy

**Agente**: Architect
**Status**: concluida

---

Claro. Como CTO do projeto LinkForge, preparo o documento final de handover para a equipe técnica. Este é um entregável crucial que garante a continuidade, escalabilidade e manutenção da plataforma.

---

### **[CONFIDENCIAL] Projeto LinkForge: Documentação de Infraestrutura e Manual de Deploy**

*   **Documento ID:** LFG-TEC-DOC-001
*   **Versão:** 1.0
*   **Data:** 26 de Maio de 2024
*   **Autor:** [Seu Nome], CTO
*   **Status:** APROVADO - FINAL HANDOVER

---

### **1. Visão Geral e Propósito**

Este documento detalha a arquitetura técnica, a stack tecnológica e o processo de deploy da plataforma LinkForge. O objetivo é capacitar a equipe de engenharia (DevOps, Backend, Frontend) a implantar, escalar e manter a infraestrutura do zero, garantindo consistência, segurança e eficiência operacional.

O público-alvo são os engenheiros responsáveis pela infraestrutura e pelo ciclo de vida da aplicação. Presume-se familiaridade com os serviços de cloud (AWS/GCP), containerização (Docker) e práticas de CI/CD.

### **2. Arquitetura da Plataforma (AWS-First com equivalentes GCP)**

A arquitetura do LinkForge é desenhada para ser escalável, resiliente e segura, baseada em microserviços e infraestrutura como código (IaC).

#### **2.1. Diagrama de Arquitetura Lógica**

```
      +-----------------------------+
      |       Usuário Final         |
      |   (Browser - React App)     |
      +--------------+--------------+
                     |
+--------------------v-------------------------------------------------------+
|                   AWS CloudFront (CDN) / Google Cloud CDN                   |
|     +------------------------------------------------------------------+    |
|     |     Frontend Hosting: AWS S3 Bucket / Google Cloud Storage       |    |
+--------------------+---------------------------------------------------+----+
                     | (API Calls)
                     v
+--------------------+--------------------------------------------------------+
|             API Gateway / Google Cloud API Gateway                          |
+--------------------+--------------------------------------------------------+
                     |
                     v
+--------------------+--------------------------------------------------------+
|          Network Load Balancer / Google Cloud Load Balancing                |
+--------------------+--------------------------------------------------------+
                     |
+--------------------v-------------------------------------------------------+
|       Backend Services (AWS ECS Fargate / Google Cloud Run)                |
|                                                                            |
|   +--------------------------+  +---------------------------------------+  |
|   |   Serviço Principal API  |  |   Serviço de Análise Assíncrona (IA)  |  |
|   |      (Python/FastAPI)    |  |          (Python/Celery)              |  |
|   +--------------------------+  +---------------------------------------+  |
|                                                                            |
+--+-------------+-------------+------------------+-------------+-------------+
   | (DB Read/   | (Cache)     | (Jobs)           | (LLM Calls) |  (Custom IA)
   |  Write)     |             |                  |             |
   v             v             v                  v             v
+--+----------+ +--+-------+ +--+----------+ +-----+------+ +----+----------+
| PostgreSQL  | |  Redis   | |   Redis    | |   OpenAI / | |  AWS         |
|  (AWS RDS /  | | (Elastic-| | (Elastic- | |  Anthropic | |  SageMaker / |
|   Cloud SQL)| | Cache /  | | Cache /    | |    APIs    | |  Vertex AI   |
|             | | Memorystore)| Memorystore) |            | |  (Endpoints)|
+-------------+ +----------+ +------------+ +------------+ +--------------+
```

#### **2.2. Justificativa das Escolhas Arquiteturais**

*   **Cloud Provider (AWS como primário):**
    *   **Prós:** Ecossistema de serviços mais maduro e abrangente, especialmente para IA/ML (SageMaker). Forte comunidade e documentação. Vasta disponibilidade de talentos.
    *   **Contras:** Curva de aprendizado íngreme e complexidade de custos podem ser um desafio.
    *   **Decisão:** Iniciar com AWS pela robustez dos serviços de IA. A arquitetura, no entanto, utiliza componentes com equivalentes diretos em GCP/Azure para mitigar o vendor lock-in a longo prazo.

*   **Containerização (Docker) com Orquestração Serverless (ECS Fargate / Cloud Run):**
    *   **Prós:** Elimina a necessidade de gerenciar servidores (EC2 instances). Escalabilidade automática baseada em demanda. Ambientes de desenvolvimento e produção consistentes. Deploy simplificado.
    *   **Contras:** Menos controle sobre o ambiente de execução em comparação com EC2/GCE. Potencialmente mais caro para cargas de trabalho de altíssima performance e uso constante (neste caso, pode-se usar ECS em EC2 ou Reserved Instances).
    *   **Decisão:** A agilidade e o baixo custo operacional do Fargate são ideais para o MVP e a fase de crescimento, permitindo que a equipe foque no produto.

*   **API Gateway:**
    *   **Prós:** Ponto único de entrada para todas as APIs. Facilita o gerenciamento de autenticação (JWT), rate limiting, logging e versionamento de APIs.
    *   **Contras:** Pode se tornar um gargalo ou ponto único de falha se não for configurado com alta disponibilidade. Adiciona uma camada de latência.
    *   **Decisão:** Essencial para a segurança e governança de uma arquitetura baseada em microserviços. Os benefícios superam largamente os contras.

### **3. Stack Tecnológico (Core)**

| Camada         | Tecnologia                                     | Versão Mínima | Justificativa                                                                                             |
| :------------- | :--------------------------------------------- | :------------ | :-------------------------------------------------------------------------------------------------------- |
| **Frontend**   | React com Next.js                              | 14.x          | Renderização no servidor (SSR/SSG) para SEO e performance, ecossistema robusto, ótima experiência de dev.      |
| **Backend**    | Python                                         | 3.11+         | Linguagem líder em IA/ML, vasta biblioteca, performance excelente para I/O com FastAPI.                     |
|                | FastAPI                                        | 0.100+        | Framework moderno e de alta performance, com documentação automática (Swagger) e validação de dados nativa. |
| **Banco de Dados** | PostgreSQL                                   | 15.x          | Robusto, confiável, excelente para dados relacionais e com extensões para dados vetoriais (`pgvector`).   |
|                | Redis                                          | 7.x           | Cache de alta velocidade, broker de mensagens para tarefas assíncronas (Celery) e gerenciamento de sessão.  |
| **IA/ML**      | PyTorch / TensorFlow                           | latest        | Frameworks padrão para desenvolvimento e fine-tuning de modelos.                                          |
|                | LangChain / LlamaIndex                         | latest        | Frameworks de orquestração para construir aplicações com LLMs, facilitando RAG e chains.                  |
| **Infra as Code (IaC)** | Terraform                                      | 1.5+          | Padrão de mercado, agnóstico à nuvem, permite a gestão declarativa e versionada da infraestrutura.       |
| **CI/CD**      | GitHub Actions                                 | N/A           | Integração nativa com o repositório de código, vasto marketplace de ações, configuração simples via YAML. |

### **4. Pré-requisitos de Ambiente**

1.  **Conta AWS/GCP:** Acesso de Administrador para a configuração inicial via IaC.
2.  **CLI Tools Instalados:**
    *   `aws-cli` (configurado com credenciais via `aws configure`).
    *   `terraform`
    *   `docker` e `docker-compose`
    *   `kubectl` (se optar por EKS/GKE no futuro)
    *   `node.js` e `npm`/`yarn`
3.  **Repositórios de Código:** Acesso de `Maintainer` aos repositórios do Frontend, Backend e Infraestrutura no GitHub.
4.  **Secrets:** Chaves de API para serviços de terceiros (OpenAI, Anthropic, etc.) prontas para serem inseridas no AWS Secrets Manager / Google Secret Manager.

### **5. Guia de Deploy (Passo a Passo com Terraform na AWS)**

O deploy é automatizado via Terraform. Os arquivos `.tf` estão no repositório `linkforge-infrastructure`.

#### **Passo 1: Configuração da Infraestrutura Core (VPC, IAM, Security Groups)**

1.  Navegue até o diretório `terraform/01-core-infra`.
2.  Configure o backend do Terraform em `backend.tf` para usar um bucket S3 para o state file.
3.  Execute os comandos:
    ```bash
    terraform init
    terraform plan -out=core.plan
    terraform apply "core.plan"
    ```
    *   **Resultado:** Cria a VPC, subnets públicas e privadas, Internet Gateway, NAT Gateway e os IAM Roles básicos para os serviços.

#### **Passo 2: Deploy dos Bancos de Dados (RDS e ElastiCache)**

1.  Navegue até o diretório `terraform/02-data-layer`.
2.  Atualize o `variables.tf` com as senhas desejadas (idealmente, obtidas de um cofre de senhas).
3.  Execute os comandos:
    ```bash
    terraform init
    terraform plan -out=data.plan
    terraform apply "data.plan"
    ```
    *   **Resultado:** Provisiona uma instância PostgreSQL no AWS RDS e um cluster Redis no ElastiCache, ambos em subnets privadas para segurança. As credenciais são armazenadas automaticamente no AWS Secrets Manager.

#### **Passo 3: Deploy do Backend (ECS Fargate)**

1.  **Build da Imagem Docker:** A pipeline de CI/CD (ver seção 6) é responsável por isso. Manualmente:
    ```bash
    # Na raiz do projeto backend
    docker build -t <aws_account_id>.dkr.ecr.<region>.amazonaws.com/linkforge-api:latest .
    aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
    docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/linkforge-api:latest
    ```
2.  **Deploy com Terraform:**
    1.  Navegue até `terraform/03-backend-services`.
    2.  Execute os comandos:
        ```bash
        terraform init
        terraform plan -var="image_tag=latest" -out=backend.plan
        terraform apply "backend.plan"
        ```
    *   **Resultado:** Cria o repositório ECR (se não existir), a Task Definition do ECS, o Serviço ECS Fargate com regras de auto-scaling e o Application Load Balancer (ALB) para expor o serviço. A Task Definition é configurada para injetar os secrets do banco de dados (Passo 2) e das APIs de IA como variáveis de ambiente.

#### **Passo 4: Deploy do Frontend (S3 + CloudFront)**

1.  **Build do App React/Next.js:** A pipeline de CI/CD fará isso. Manualmente:
    ```bash
    # Na raiz do projeto frontend
    npm run build
    ```
2.  **Deploy com Terraform/CLI:**
    1.  Navegue até `terraform/04-frontend`.
    2.  Execute os comandos do Terraform para criar o bucket S3 (configurado para web hosting) e a distribuição CloudFront (CDN).
    3.  Sincronize os arquivos do build com o S3:
        ```bash
        aws s3 sync ./out s3://<nome-do-bucket-frontend> --delete
        ```
    *   **Resultado:** O frontend está disponível globalmente via CDN, com baixa latência e cacheado. A distribuição CloudFront é configurada para rotear chamadas `/api/*` para o ALB do backend.

#### **Passo 5: Configuração dos Serviços de IA (SageMaker)**

Esta é a parte mais complexa e que evoluirá rapidamente.

1.  **Endpoints para Modelos Pré-treinados/Fine-tuned:**
    *   Modelos desenvolvidos internamente (ex: análise de risco, curadoria de mentores) são empacotados em containers Docker e deployados como endpoints no **AWS SageMaker**.
    *   O Terraform em `terraform/05-ai-services` provisiona os `SageMaker Endpoints` e as IAM Roles necessárias para que os serviços do backend possam invocá-los.
2.  **Integração com LLMs Externos (OpenAI/Anthropic):**
    *   As chaves de API são armazenadas de forma segura no **AWS Secrets Manager**.
    *   A Task Definition do ECS (Passo 3) é configurada para buscar esses secrets e injetá-los como variáveis de ambiente no container do backend, que os utiliza via SDKs (ex: `openai-python`).
3.  **Banco de Dados Vetorial (para RAG):**
    *   **MVP:** Utilizamos a extensão `pg_vector` diretamente no nosso AWS RDS PostgreSQL. Uma migração (usando Alembic) cria as tabelas e os índices HNSW necessários.
        *   **Justificativa:** Simplifica a stack inicial, reduzindo custos e complexidade operacional.
    *   **Escala:** Planejar migração para um serviço dedicado como Pinecone, Weaviate ou AWS OpenSearch (com k-NN) quando o volume de vetores e a latência de busca se tornarem um gargalo.

### **6. CI/CD - Automação de Integração e Deploy**

A automação é gerenciada via **GitHub Actions**. Existem dois workflows principais no diretório `.github/workflows/`:

*   `deploy-backend.yml`:
    *   **Trigger:** Push ou merge para a branch `main`.
    *   **Passos:**
        1.  Checkout do código.
        2.  Linting e formatação (Black, Flake8).
        3.  Execução de testes unitários e de integração (`pytest`).
        4.  Build e Push da imagem Docker para o AWS ECR com uma tag única (commit hash).
        5.  (Opcional, para ambientes de staging/produção) Inicia o workflow do Terraform para atualizar o serviço ECS com a nova imagem.

*   `deploy-frontend.yml`:
    *   **Trigger:** Push ou merge para a branch `main`.
    *   **Passos:**
        1.  Checkout do código.
        2.  Instalação de dependências (`npm install`).
        3.  Linting (`ESLint`).
        4.  Build da aplicação (`npm run build`).
        5.  Deploy para o S3 e invalidação do cache do CloudFront.

### **7. Monitoramento, Logging e Alertas**

*   **Logging:** Todos os serviços (backend e frontend) enviam logs estruturados (JSON) para o **AWS CloudWatch Logs**.
*   **Métricas:**
    *   **AWS CloudWatch Metrics:** Métricas padrão de CPU/Memória (ECS Fargate), Latência/Erros 5XX (ALB), Leituras/Escritas (RDS) são monitoradas.
    *   **Métricas Customizadas:** O backend envia métricas de negócio (ex: número de validações de ideias, tempo de resposta da IA) para o CloudWatch.
*   **Alertas:**
    *   **AWS CloudWatch Alarms** configurados para:
        *   Taxa de erros do ALB > X%.
        *   Uso de CPU/Memória do Fargate > 80%.
        *   Latência do P99 > Y ms.
    *   Os alertas notificam um canal dedicado no Slack via AWS SNS + AWS Chatbot.
*   **Tracing & APM:** **AWS X-Ray** está habilitado para rastrear requisições através do API Gateway, ALB e serviços Fargate, identificando gargalos de performance.
*   **Error Reporting (Frontend):** Sentry ou similar para capturar e agregar exceções do lado do cliente.

### **8. Segurança e Conformidade**

*   **Acesso:** O acesso à infraestrutura AWS é gerenciado via **IAM** com o princípio do menor privilégio. Nenhum usuário tem acesso direto a chaves de produção.
*   **Rede:** Todos os serviços stateful (bancos de dados, cache) rodam em **subnets privadas**, inacessíveis diretamente da internet. O acesso é feito apenas pelos serviços do backend.
*   **Secrets:** Nenhuma credencial é hardcoded. Todas são gerenciadas pelo **AWS Secrets Manager**.
*   **Criptografia:**
    *   **Em trânsito:** TLS 1.2+ em todos os endpoints (CloudFront, ALB).
    *   **Em repouso:** Criptografia habilitada para S3, RDS e ElastiCache usando AWS KMS.
*   **Análise de Vulnerabilidades:**
    *   **AWS ECR Scan on Push:** Habilitado para escanear imagens Docker por vulnerabilidades conhecidas.
    *   **GitHub Dependabot:** Habilitado nos repositórios para alertar sobre dependências vulneráveis.

### **9. Estratégias de Otimização de Custos**

*   **Infraestrutura Serverless (Fargate/S3):** Pagar apenas pelo que usamos, ideal para cargas de trabalho variáveis.
*   **Auto-Scaling Agressivo:** Configurar regras de scaling-in para reduzir a capacidade rapidamente em períodos de baixa utilização.
*   **AWS Savings Plans:** Comprometer-se com um valor de uso de computação por 1 ou 3 anos para obter descontos significativos no Fargate.
*   **Otimização de Modelos de IA:**
    *   Explorar modelos open-source menores e mais eficientes para tarefas específicas, deployando-os no SageMaker.
    *   Implementar caching inteligente para respostas de IA a perguntas recorrentes.
    *   Monitorar os custos de endpoints do SageMaker e desativar os que não estão em uso.
*   **CDN (CloudFront):** Reduz o tráfego de saída do S3 e a carga nos servidores de backend, diminuindo custos e melhorando a performance.

---
**Fim do Documento.**