# Dashboard Projeto Experts - AlfaCon

## Descrição

Dashboard completo para monitorar o engajamento dos professores do AlfaCon no projeto Experts, baseado na metodologia do livro "O Segredo de Experts" de Russell Brunson.

## Funcionalidades

### ✅ Métricas em Tempo Real
- **Total de Demandas**: Quantidade de roteiros enviados aos professores
- **Materiais Entregues**: Taxa de entrega dos materiais solicitados
- **Alcance Total**: Soma do alcance de todos os posts dos professores
- **Engajamento Médio**: Percentual de engajamento (curtidas + comentários / alcance)

### ✅ Gestão de Demandas
- **Registrar Nova Demanda**: Formulário para criar novas solicitações aos professores
- **Registrar Resultado**: Formulário para inserir métricas de engajamento dos posts
- **Histórico Completo**: Tabela com todas as demandas e seus resultados

### ✅ Análises Visuais
- **Gráfico de Demandas por Professor**: Visualização em barras das demandas por professor
- **Gráfico de Engajamento por Tipo**: Gráfico de pizza mostrando engajamento por tipo de conteúdo
- **Timeline de Entregas**: Gráfico de linha mostrando entregas ao longo do tempo

### ✅ Monitoramento de Professores
- **Cards Individuais**: Cada professor tem um card com suas estatísticas
- **Métricas Detalhadas**: Demandas, entregas e alcance por professor

## Professores Incluídos

1. **Pedro Campos** - Matemática/RLM e Estatística
2. **Pablo** - Português e Redação Oficial
3. **Rafael Araújo** - Informática
4. **Samuel** - Contabilidade
5. **Tiago Vidal** - Direito Administrativo
6. **Rogério Dalvipa** - Direito Constitucional
7. **Lucas Fávero** - Direito Penal
8. **Pedro Canezin** - Processo Penal
9. **Filipe Ávila** - Legislação Especial
10. **João Paulo** - Arquivologia
11. **Heitor** - Redação

## Como Executar

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Extrair o projeto**:
   ```bash
   # Se você recebeu o arquivo ZIP
   unzip dashboard_experts_essencial.zip
   cd dashboard_experts
   ```

2. **Criar ambiente virtual**:
   ```bash
   python -m venv venv
   ```

3. **Ativar ambiente virtual**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Executar o dashboard**:
   ```bash
   python src/main.py
   ```

6. **Acessar no navegador**:
   ```
   http://localhost:5001
   ```

## Como Usar

### 1. Gerar Dados de Exemplo
- Clique no botão **"Gerar Dados de Exemplo"** para popular o dashboard com dados fictícios
- Isso ajuda a entender como o dashboard funciona

### 2. Registrar Nova Demanda
- Selecione o **Professor**
- Escolha o **Tipo de Conteúdo** (Reels, Stories, Feed, etc.)
- Defina o **Prazo de Entrega**
- Clique em **"Registrar Demanda"**

### 3. Registrar Resultado
- Selecione a **Demanda** (apenas demandas pendentes aparecem)
- Informe se o **Material foi Entregue**
- Insira as métricas de engajamento:
  - **Alcance**: Número de contas únicas que viram o post
  - **Curtidas**: Número de curtidas
  - **Comentários**: Número de comentários
- Clique em **"Registrar Resultado"**

### 4. Visualizar Análises
- Use as **abas dos gráficos** para alternar entre diferentes visualizações
- **Demandas por Professor**: Mostra distribuição de demandas
- **Engajamento por Tipo**: Mostra qual tipo de conteúdo gera mais engajamento
- **Timeline de Entregas**: Mostra evolução das entregas ao longo do tempo

### 5. Monitorar Professores
- Visualize os **cards dos professores** para ver estatísticas individuais
- Cada card mostra: demandas, entregas e alcance total

### 6. Gerenciar Histórico
- A **tabela de histórico** mostra todas as demandas registradas
- Use o botão **"Excluir"** para remover demandas se necessário

## Estrutura de Dados

O dashboard coleta e monitora as seguintes métricas:

### Métricas de IDA (Demandas Enviadas)
- Número de roteiros enviados por professor
- Tipo de conteúdo solicitado
- Prazo de entrega estabelecido
- Data de envio da demanda

### Métricas de VOLTA (Resultados Obtidos)
- Material entregue (Sim/Não)
- Data de entrega
- Plataforma de publicação
- Métricas de engajamento:
  - Alcance
  - Impressões
  - Curtidas
  - Comentários
  - Compartilhamentos
  - Salvos
  - Visualizações (para vídeos)

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js
- **Banco de Dados**: SQLite
- **Estilo**: CSS customizado com gradientes e animações

## Arquivos Importantes

- `src/main.py`: Arquivo principal do Flask
- `src/static/index.html`: Interface do dashboard
- `src/models/demanda.py`: Modelo de dados para demandas
- `src/routes/dashboard.py`: Rotas da API do dashboard
- `src/database/app.db`: Banco de dados SQLite

## Próximos Passos para Hospedagem

Quando estiver pronto para hospedar o dashboard, você pode:

1. **Hospedar em plataformas gratuitas**:
   - Render.com (recomendado)
   - Heroku
   - PythonAnywhere

2. **Separar frontend e backend**:
   - Frontend no GitHub Pages
   - Backend em serviço de hospedagem Python

3. **Usar serviços profissionais**:
   - AWS, Google Cloud, Azure
   - DigitalOcean, Linode

## Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências foram instaladas
2. Confirme que o Python 3.11+ está sendo usado
3. Verifique se a porta 5001 não está sendo usada por outro programa

## Licença

Este projeto foi desenvolvido especificamente para o AlfaCon e o projeto Experts.

