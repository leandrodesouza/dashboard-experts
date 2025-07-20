# Instruções de Implantação no Render.com

Este documento detalha os passos para implantar o Dashboard do Projeto Experts no Render.com. O Render.com é uma plataforma de nuvem unificada que permite hospedar aplicações web, bancos de dados e muito mais, com suporte a Python e Flask.

## Pré-requisitos

1.  **Conta no Render.com**: Certifique-se de ter uma conta ativa no Render.com. Você pode se inscrever gratuitamente.
2.  **Repositório Git**: O código do seu projeto deve estar em um repositório Git (GitHub, GitLab ou Bitbucket). Se ainda não estiver, crie um e faça o push do seu projeto.

## Passos para Implantação

Siga estes passos para implantar seu serviço web no Render.com:

### 1. Criar um Novo Serviço Web no Render.com

1.  Faça login na sua conta do Render.com.
2.  No seu Dashboard, clique em **"New"** e selecione **"Web Service"**.

### 2. Conectar seu Repositório Git

1.  Conecte sua conta Git (GitHub, GitLab ou Bitbucket) ao Render.com.
2.  Selecione o repositório onde o código do seu Dashboard está hospedado.
3.  Configure as opções de implantação:
    -   **Root Directory**: Deixe em branco se o seu projeto estiver na raiz do repositório, ou especifique o subdiretório (ex: `/dashboard_experts` se você fez o upload da pasta inteira).
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn src.main:app`

### 3. Configurar Variáveis de Ambiente (Opcional, mas recomendado)

Embora o projeto use SQLite (que não requer variáveis de ambiente para conexão com o banco de dados externo), você pode adicionar variáveis de ambiente para configurações futuras ou chaves secretas.

1.  Na seção **"Environment"**, clique em **"Add Environment Variable"**.
2.  Adicione quaisquer variáveis que seu aplicativo possa precisar.

### 4. Configurar o Banco de Dados (SQLite)

O SQLite é um banco de dados baseado em arquivo. No Render.com, o arquivo `app.db` será criado e persistirá dentro do contêiner do seu serviço web. **Importante**: Se o serviço for reiniciado ou recriado (por exemplo, após uma nova implantação), o banco de dados pode ser resetado. Para produção, considere usar um banco de dados externo como PostgreSQL (oferecido pelo Render.com) e adaptar seu código Flask para usá-lo.

Para este MVP, o SQLite funcionará bem para demonstração.

### 5. Implantar o Serviço

1.  Após configurar tudo, clique em **"Create Web Service"**.
2.  O Render.com irá clonar seu repositório, instalar as dependências e iniciar seu aplicativo.
3.  Você poderá acompanhar o progresso da implantação nos logs.

### 6. Acessar o Dashboard

1.  Uma vez que a implantação for bem-sucedida, o Render.com fornecerá uma URL pública para o seu serviço (ex: `https://your-service-name.onrender.com`).
2.  Acesse esta URL no seu navegador para ver o Dashboard funcionando.

## Solução de Problemas Comuns

-   **Erro de Build**: Verifique se todas as dependências estão listadas corretamente no `requirements.txt` e se o `Build Command` está correto.
-   **Erro de Runtime**: Verifique os logs do seu serviço no Render.com. Erros no `Start Command` ou no código Python serão exibidos aqui.
-   **Problemas de Conexão**: Certifique-se de que seu aplicativo Flask está configurado para escutar em `0.0.0.0` e na porta padrão (ou na porta que o Render.com atribui, que geralmente é a 80 ou 443, mas o Gunicorn lida com isso automaticamente).

Lembre-se que o Render.com pode levar alguns minutos para construir e implantar o aplicativo pela primeira vez. Implantações subsequentes (após pushes para o repositório Git) geralmente são mais rápidas.

