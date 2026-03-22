### **Task: [Processamento de Dados] Criar Datasets Estruturados para Modelos Preditivos da Copa do Mundo 2022**

**User Story:**
> **Como** um Cientista de Dados,
> **Eu quero** processar os arquivos JSON brutos do StatsBomb e gerar datasets estruturados em CSV,
> **Para que** eu possa treinar e avaliar modelos de classificação e regressão de forma eficiente.

**Descrição/Contexto:**
Este é o primeiro passo técnico para alcançar três objetivos de negócio: prever o vencedor de uma partida, o total de chutes a gol de um time e o total de chutes a gol de um jogador.

Para garantir um ciclo de desenvolvimento rápido e validar a viabilidade do projeto (Fail Fast), esta tarefa se concentrará **exclusivamente nos dados da Copa do Mundo de 2022**. Esta redução deliberada do escopo (de ~11GB de JSONs para apenas os 64 jogos do torneio) permitirá a criação de um pipeline de ponta-a-ponta em poucas horas.

O script a ser criado será responsável por ler os dados brutos, realizar a engenharia de features e exportar três datasets limpos e prontos para modelagem.

**Technical Tasks (Plano de Implementação Detalhado):**

1.  **Identificação dos Dados da Copa do Mundo 2022:**
    *   Ler o arquivo `Datasets/data/competitions.json`.
    *   Filtrar o JSON para encontrar o objeto correspondente a "FIFA World Cup" com a `season_name` "2022".
    *   Extrair e armazenar o `competition_id` (ex: 43) e `season_id` (ex: 106).
    *   Usar esses IDs para ler o arquivo `Datasets/data/matches/{competition_id}/{season_id}.json` e obter a lista completa de todos os `match_id`s do torneio.

2.  **Criação do Script de Processamento (`data_processing.py`):**
    *   O script irá iterar sobre a lista de `match_id`s obtida no passo anterior.
    *   Para cada `match_id`, o script carregará em memória os arquivos `Datasets/data/events/{match_id}.json` e `Datasets/data/lineups/{match_id}.json`.

3.  **Engenharia de Features e Geração dos Datasets:**
    *   Dentro do loop, para cada jogo, o script irá calcular features e alvos para os três datasets distintos:

    *   **Dataset 1: `wc2022_team_outcome.csv` (Classificação)**
        *   **Alvo (y):** Com base nos `home_score` e `away_score` do arquivo de jogo, determinar o resultado para o time da casa: 'Win', 'Draw', 'Loss'.
        *   **Features (X):** Calcular estatísticas agregadas para cada time usando apenas os eventos do **primeiro tempo** (`period == 1`):
            *   `half_time_goals`
            *   `half_time_shots`
            *   `half_time_shots_on_goal`
            *   `half_time_possession` (requer cálculo a partir dos eventos)
            *   `half_time_corners`
            *   `half_time_fouls`
        *   Cada linha no CSV representará um jogo, contendo as features do time da casa, as features do time visitante e a classe alvo.

    *   **Dataset 2: `wc2022_team_sog.csv` (Regressão)**
        *   **Alvo (y):** Para cada time no jogo, contar o número total de chutes a gol (`shot.outcome.name` em ['Goal', 'Saved']) durante a partida inteira.
        *   **Features (X):** Reutilizar as mesmas features do primeiro tempo calculadas para o Dataset 1.
        *   Cada linha no CSV representará um time em um jogo (resultando em 128 linhas para 64 jogos).

    *   **Dataset 3: `wc2022_player_sog.csv` (Regressão)**
        *   **Alvo (y):** Para cada jogador na partida (obtido do arquivo de `lineups`), contar o número total de chutes a gol durante o jogo inteiro.
        *   **Features (X):** Calcular estatísticas agregadas para cada jogador usando apenas os eventos do **primeiro tempo**:
            *   `half_time_touches`
            *   `half_time_passes`
            *   `half_time_dribbles`
        *   Cada linha no CSV representará um jogador em um jogo.

4.  **Exportação dos Resultados:**
    *   Ao final do processamento de todos os jogos, o script irá converter os dados coletados em DataFrames do Pandas.
    *   Salvar os três DataFrames como arquivos CSV na raiz do projeto: `wc2022_team_outcome.csv`, `wc2022_team_sog.csv`, e `wc2022_player_sog.csv`.

**Acceptance Criteria (Definition of Done):**

*   [ ] Um script Python chamado `data_processing.py` existe no repositório.
*   [ ] O script executa do início ao fim sem erros.
*   [ ] O script processa **apenas** os jogos da Copa do Mundo de 2022.
*   [ ] Três arquivos são gerados na raiz do projeto: `wc2022_team_outcome.csv`, `wc2022_team_sog.csv`, `wc2022_player_sog.csv`.
*   [ ] O arquivo `wc2022_team_outcome.csv` contém 64 linhas, com colunas de features do 1º tempo e uma coluna 'outcome'.
*   [ ] O arquivo `wc2022_team_sog.csv` contém 128 linhas, com colunas de features do 1º tempo e uma coluna 'total_shots_on_goal'.
*   [ ] O arquivo `wc2022_player_sog.csv` contém múltiplas linhas por jogo, com colunas de features do jogador no 1º tempo e uma coluna 'total_shots_on_goal'.
