# Plano de Ação - Ponto 1: Visualização e Análise de Dados

## Objetivo
Desenvolver métodos para visualizar as informações do dataset e identificar as features mais relevantes para cada tipo de previsão (Match Outcome, Team Performance, Player Performance), com foco inicial na análise de desempenho de jogadores.

## Tarefas Detalhadas

### 1.1. Análise e Visualização Geral do Dataset
*   **Ferramentas:** Python (Pandas, Matplotlib, Seaborn), Jupyter Notebooks.
*   **Passos:**
    *   Carregar os datasets existentes (`wc2022_player_sog.csv`, `wc2022_team_outcome.csv`, `wc2022_team_sog.csv`).
    *   Realizar uma análise exploratória de dados (EDA) para cada dataset:
        *   Verificar tipos de dados, valores ausentes.
        *   Estatísticas descritivas (média, mediana, desvio padrão, etc.).
        *   Distribuição das variáveis (histogramas, box plots).
        *   Correlação entre as features e os alvos de previsão.
    *   Criar visualizações iniciais para entender a estrutura e as relações dos dados.

### 1.1.1. Resultados da Análise Exploratória Inicial (EDA)

#### wc2022_team_outcome.csv
*   **Conteúdo:** Dados de nível de partida com estatísticas do primeiro tempo e resultado final.
*   **Variável Alvo:** `final_outcome` (categórica: Win, Loss, Draw).
*   **Features Relevantes:** `ht_goals_diff`, `ht_shots_diff`, `ht_sog_diff`, `ht_fouls_diff` são fortes candidatos a preditores.
*   **Observação Importante:** A coluna `ht_corners_diff` é uniformemente zero (desvio padrão 0, min/max 0), indicando que não há variação e, portanto, deve ser excluída como feature preditiva.

#### wc2022_team_sog.csv
*   **Conteúdo:** Dados de nível de equipe por partida, com estatísticas do primeiro tempo e total de chutes a gol.
*   **Variável Alvo:** `total_shots_on_goal` para previsão de desempenho da equipe.
*   **Features Relevantes:** `ht_goals`, `ht_shots`, `ht_sog`, `ht_corners`, `ht_fouls` são preditores relevantes do primeiro tempo.

#### wc2022_player_sog.csv
*   **Conteúdo:** Dados de nível de jogador por partida, com estatísticas do primeiro tempo e total de chutes a gol.
*   **Variável Alvo:** `total_shots_on_goal` para previsão de desempenho do jogador.
*   **Features Relevantes:** `ht_passes`, `ht_touches`, `ht_dribbles` são preditores relevantes do primeiro tempo. O `player_name` também pode ser uma feature categórica significativa.
*   **Observação Importante:** O `total_shots_on_goal` para jogadores é geralmente baixo (média de 0.16, máximo de 5), sugerindo que a maioria dos jogadores não realiza muitos chutes a gol em uma única partida.

### 1.2. Rastreamento e Avaliação de Jogadores da Copa do Mundo
*   **Objetivo:** Identificar e coletar dados de desempenho de jogadores da Copa do Mundo 2022 em suas ligas anteriores.
*   **Análise de Viabilidade com Dados Atuais:**
    *   Os datasets atualmente disponíveis (`wc2022_player_sog.csv` e os dados brutos da Copa do Mundo de 2022) contêm informações sobre jogadores e suas equipes nacionais *durante* a Copa do Mundo.
    *   Os arquivos `players_data_light-2025_2026.csv` e `players_data-2025_2026.csv` na pasta `Datasets/players-data` referem-se a temporadas *posteriores* à Copa do Mundo de 2022.
    *   **Conclusão:** Com os dados *atualmente disponíveis*, **não é possível** rastrear diretamente o desempenho dos jogadores em ligas anteriores à Copa do Mundo de 2022 para todos os jogadores. No entanto, podemos analisar ligas específicas se os dados estiverem disponíveis.
*   **Análise de Caso: Lionel Messi (Ligue 1 2021/2022 vs. FIFA World Cup 2022)**
    *   **Identificação da Liga Anterior:** Lionel Messi jogou pelo Paris Saint-Germain (PSG) na Ligue 1 (França) durante a temporada 2021/2022, imediatamente antes da Copa do Mundo de 2022.
    *   **Disponibilidade de Dados:** Dados para a Ligue 1 2021/2022 estão disponíveis no dataset (`competition_id: 7`, `season_id: 108`).
    *   **Processamento de Dados:** O script `data_processing.py` foi adaptado e executado para gerar os CSVs processados para a Ligue 1 2021/2022.
    *   **Comparação de Desempenho (Chutes a Gol):**
        *   **FIFA World Cup 2022 (7 partidas):**
            *   Total de Chutes a Gol: 20
            *   Média de Chutes a Gol por partida: 2.86
        *   **Ligue 1 2021/2022 (26 partidas):**
            *   Total de Chutes a Gol: 27
            *   Média de Chutes a Gol por partida: 1.04
    *   **Correlação/Insights:** Messi demonstrou uma média significativamente maior de chutes a gol por partida na Copa do Mundo de 2022 em comparação com sua temporada na Ligue 1 2021/2022. Isso pode indicar uma maior agressividade ofensiva ou um papel tático diferente na seleção nacional, possivelmente influenciado pelas altas apostas do torneio.
*   **O que podemos prever com dados anteriores do jogador (Ligue 1 2021/2022 para prever WC 2022):**
    *   **Para Desempenho do Jogador (e.g., `total_shots_on_goal` na WC 2022):**
        *   **Features Diretas da Ligue 1:** Média de `total_shots_on_goal`, `ht_passes`, `ht_touches`, `ht_dribbles` por partida na Ligue 1. Total de `total_shots_on_goal` na Ligue 1. Métricas de consistência (e.g., desvio padrão de `total_shots_on_goal`).
        *   **Hipótese:** O desempenho de jogadores em ligas anteriores pode servir como uma linha de base. A diferença observada em Messi sugere um "fator de intensidade" ou "impulso de torneio" em competições de alto nível.
        *   **Valor Preditivo:** O desempenho em ligas anteriores pode ser um preditor, mas com a ressalva de que o contexto do torneio (como a Copa do Mundo) pode levar a uma elevação no desempenho de métricas específicas como chutes a gol.
    *   **Para Desempenho da Equipe (e.g., `total_shots_on_goal` para a Argentina na WC 2022):**
        *   As estatísticas individuais dos jogadores de uma seleção (agregadas de suas ligas de clubes) podem ser usadas para criar features de nível de equipe. Por exemplo, a soma ou média dos `total_shots_on_goal` dos jogadores de uma equipe em suas ligas pode predizer o `total_shots_on_goal` da equipe na Copa do Mundo.
    *   **Para Resultado da Partida (e.g., Vitória/Derrota/Empate para a Argentina na WC 2022):**
        *   O desempenho individual de jogadores-chave em suas ligas pode ser um indicador indireto da força geral da equipe e, consequentemente, da probabilidade de vitória.
*   **Limitações e Próximos Passos para Robustez:**
    *   A análise atual é um estudo de caso de um único jogador. É crucial verificar se os padrões observados são generalizáveis para outros jogadores.
    *   Expandir as métricas de desempenho para incluir xG, xA, passes-chave, desarmes, etc., forneceria uma visão mais completa.
    *   Coletar dados de mais jogadores de suas respectivas ligas de clubes e da Copa do Mundo.
    *   **Aquisição de Dados Históricos Adicionais (Geral):** Para uma análise mais abrangente de outros jogadores, será necessário buscar e integrar fontes de dados externas que contenham o histórico de clubes e estatísticas de desempenho de jogadores em ligas anteriores a 2022.
    *   **Mapeamento de Jogadores:** Desenvolver uma metodologia robusta para mapear os jogadores da Copa do Mundo com seus registros históricos em outras ligas (via IDs de jogadores ou correspondência de nomes).
    *   **Métricas de Desempenho:** Definir quais métricas são mais relevantes para avaliar o desempenho de um jogador em ligas anteriores que possam impactar seu desempenho na Copa do Mundo (Gols, Assistências, Passes Completos, Dribles, Desarmes, xG, xA, etc.).
    *   Visualizar o desempenho dos jogadores antes da Copa do Mundo.

### 1.3. Avaliação e Agrupamento de Jogadores em "Times Parceiros"
*   **Objetivo:** Desenvolver uma metodologia para agrupar jogadores de alto desempenho em times hipotéticos ("times parceiros") para análise.
*   **Passos:**
    *   **Critérios de Seleção:** Definir critérios claros para considerar um jogador como "melhor" (e.g., top X% em xG, xA, ou uma combinação de métricas).
    *   **Metodologia de Agrupamento:**
        *   Como formar esses times? Aleatoriamente? Por posição? Por pontuação geral?
        *   Considerar a viabilidade de simular o desempenho desses times.
    *   **Visualização:** Como apresentar os resultados desses agrupamentos? (e.g., comparação de métricas agregadas dos "times parceiros" vs. times reais).

### 1.4. Análise de Viabilidade para "Campeonato Pernambucano Brasileiro de 2025"
*   **Análise de Viabilidade com Dados Atuais:**
    *   A análise do arquivo `competitions.json` (que lista todas as competições e temporadas disponíveis no dataset) **não revelou nenhuma entrada** para "Campeonato Pernambucano Brasileiro de 2025" ou qualquer competição similar no Brasil para o ano de 2025.
    *   **Conclusão:** Com os dados *atualmente disponíveis*, **não é possível** estudar o "Campeonato Pernambucano Brasileiro de 2025".
*   **Próximos Passos para Viabilizar:**
    *   **Aquisição de Novo Dataset:** Para estudar este campeonato, seria necessário adquirir um novo dataset específico para o "Campeonato Pernambucano Brasileiro de 2025" de uma fonte de dados externa.

### 1.5. Análise de Viabilidade para "Campeonato Brasileiro de 2025"
*   **Análise de Viabilidade com Dados Atuais:**
    *   A análise do arquivo `competitions.json` **não revelou nenhuma entrada** para qualquer campeonato brasileiro para o ano de 2025. Não há competições com `country_name: "Brazil"` ou `season_name` indicando "2025" para um campeonato brasileiro.
    *   **Conclusão:** Com os dados *atualmente disponíveis*, **não é possível** estudar um "Campeonato Brasileiro de 2025".
*   **Próximos Passos para Viabilizar:**
    *   **Aquisição de Novo Dataset:** Para estudar este campeonato, seria necessário adquirir um novo dataset específico para um "Campeonato Brasileiro de 2025" de uma fonte de dados externa.

## Análise da Performance de Messi e Pontos Relevantes para o Modelo:

1.  **Variável Alvo Principal:** `total_shots_on_goal` (total de chutes a gol) é a variável alvo primária para a previsão de desempenho individual do jogador. A diferença significativa na média de chutes a gol de Messi entre a Copa do Mundo (2.86) e a Ligue 1 (1.04) ressalta a importância do contexto da competição.

2.  **Estatísticas do Primeiro Tempo como Preditores:**
    *   `ht_passes` (passes no primeiro tempo), `ht_touches` (toques no primeiro tempo) e `ht_dribbles` (dribles no primeiro tempo) são fortes candidatos a features preditivas. Eles quantificam o envolvimento e as ações ofensivas do jogador no primeiro tempo, que podem correlacionar-se com seu desempenho geral na partida.

3.  **"Efeito Torneio" / Features Contextuais:**
    *   A disparidade no desempenho de Messi sugere que o *tipo de competição* é um fator altamente relevante. Uma feature binária (e.g., `is_world_cup: 1/0`) ou categórica para `competition_type` pode ser crucial para o modelo.
    *   Este "efeito torneio" pode indicar que jogadores de alto nível elevam seu desempenho em competições de alta pressão. O modelo deve ser capaz de capturar essa dinâmica.

4.  **Identidade do Jogador (`player_id`, `player_name`):**
    *   `player_id` deve ser tratado como uma feature categórica (ou incorporado via embeddings) para capturar as características únicas de cada jogador.
    *   O histórico de desempenho de um jogador (e.g., média de `total_shots_on_goal` em várias temporadas/ligas) é uma feature fundamental para estabelecer uma linha de base de seu desempenho típico.

5.  **Contexto da Equipe (`team_id`):**
    *   O `team_id` (representando a seleção nacional ou o clube) é relevante, pois o desempenho de um jogador é influenciado pela equipe e táticas. Features relacionadas à força da equipe, forma ou estilo de jogo podem ser incorporadas.

**Pontos Mais Relevantes para o Nosso Modelo (baseado na análise de Messi):**

*   **Variável Alvo:** `total_shots_on_goal` (para desempenho do jogador).
*   **Features Preditivas Chave:**
    *   **Atividade do Jogador no Primeiro Tempo:** `ht_passes`, `ht_touches`, `ht_dribbles`.
    *   **Tipo/Contexto da Competição:** Uma feature que indique o tipo de competição (Copa do Mundo, liga, etc.) para capturar o "efetio torneio".
    *   **Linha de Base Histórica do Jogador:** O desempenho médio do jogador em competições anteriores (e.g., média de `total_shots_on_goal` da liga de clubes).
    *   **Identidade do Jogador:** `player_id` como feature categórica.
    *   **Identidade/Contexto da Equipe:** `team_id` como feature categórica.

## Próximos Passos (Plano Revisado)

Com base nas análises anteriores e na decisão de não adquirir novos dados, o plano de ação é revisado para focar na otimização e re-treinamento de modelos com os datasets existentes.

### 1. Refinamento do Pré-processamento de Dados:
*   **Remoção de Features Irrelevantes:** Modificar `data_processing.py` para remover a feature `ht_corners_diff` do `df_team_outcome`, pois foi identificada como uniformemente zero e sem valor preditivo.
*   **Generalização do Processamento:** Garantir que `data_processing.py` possa ser facilmente executado para diferentes competições/temporadas disponíveis, facilitando a combinação de dados.

### 2. Criação de um Dataset Maior e Enriquecido:
*   **Combinação de Datasets:** Integrar os dados processados da Copa do Mundo de 2022 (`wc2022_player_sog.csv`, `wc2022_team_outcome.csv`, `wc2022_team_sog.csv`) com os dados da Ligue 1 2021/2022 (`ligue1_2021_2022_player_sog.csv`, `ligue1_2021_2022_team_outcome.csv`, `ligue1_2021_2022_team_sog.csv`) em um único conjunto de dados maior.
*   **Feature Engineering (Cross-Competição):**
    *   Para cada jogador, calcular métricas de desempenho médio de competições anteriores (e.g., média de `ht_passes`, `ht_touches`, `ht_dribbles`, `total_shots_on_goal` da Ligue 1 para prever o desempenho na Copa do Mundo).
    *   Criar uma feature `competition_type` (e.g., 'World Cup', 'Ligue 1') para capturar o "efeito torneio" identificado na análise de Messi.
    *   Considerar outras features contextuais (e.g., fase da competição, importância do jogo).

### 3. Re-treinamento e Avaliação do Modelo:
*   **Seleção do Alvo:** Focar na previsão de `total_shots_on_goal` para jogadores como um alvo principal, utilizando as features enriquecidas.
*   **Treinamento do Modelo:** Utilizar o dataset combinado e as novas features para treinar modelos preditivos (e.g., modelos de regressão para `total_shots_on_goal`).
*   **Avaliação:** Avaliar o desempenho do modelo, buscando melhorias na precisão e na capacidade de generalização.

#### Resultados da Avaliação do Modelo Inicial (RandomForestRegressor):
*   **Mean Absolute Error (MAE): 0.25** - O modelo prevê os chutes a gol com uma diferença média de 0.25, o que é razoável considerando a natureza dos dados.
*   **R-squared (R2): 0.17** - O R2 teve uma pequena melhora de 0.15 para 0.17, indicando que o modelo ainda explica uma pequena parte da variância nos chutes a gol dos jogadores. Há um espaço considerável para melhoria.

#### Importância das Features (com features enriquecidas - RandomForestRegressor):
1.  `avg_total_sog_ligue1` (0.218): A média de chutes a gol na Ligue 1 continua sendo a feature mais importante.
2.  `ht_touches` (0.209): Toques no primeiro tempo permanecem muito importantes.
3.  `ht_passes` (0.153): Passes no primeiro tempo continuam significativos.
4.  `player_id_encoded` (0.102): A identidade do jogador continua crucial.
5.  `player_id_x_world_cup` (0.100): O termo de interação entre o ID do jogador e o tipo de competição "World Cup" é agora a quinta feature mais importante. Isso sugere que o modelo está capturando diferenças de desempenho específicas do jogador no contexto da Copa do Mundo, validando parcialmente o "efetio torneio" como algo individualizado.
6.  `team_id_encoded` (0.090): A identidade da equipe ainda desempenha um papel.
7.  `ht_dribbles` (0.072): Dribles no primeiro tempo contribuem.
8.  `player_id_x_ligue_1` (0.013): O termo de interação para a Ligue 1 tem menor importância, possivelmente porque as médias históricas já capturam grande parte do desempenho na Ligue 1.
9.  `avg_ht_passes_ligue1`, `avg_ht_touches_ligue1`, `avg_ht_dribbles_ligue1` (baixa importância): As médias individuais de estatísticas do primeiro tempo da Ligue 1 continuam com baixa importância.
10. `competition_type_Ligue 1` (0.002) e `competition_type_World Cup` (0.002): As features de tipo de competição one-hot encoded ainda têm importância muito baixa. Isso reforça a ideia de que o "efeito torneio" é mais sobre a interação do jogador com o torneio do que um efeito geral da competição em si.

#### Resultados da Avaliação do Modelo (GradientBoostingRegressor):
*   **Mean Absolute Error (MAE): 0.24** - Uma pequena melhora no MAE.
*   **R-squared (R2): 0.26** - Uma melhora significativa no R2 (de 0.17 para 0.26), indicando que o Gradient Boosting é mais eficaz em explicar a variância.

#### Importância das Features (com features enriquecidas - GradientBoostingRegressor):
1.  `avg_total_sog_ligue1` (0.409): A importância desta feature aumentou significativamente, reforçando o valor do desempenho histórico.
2.  `ht_passes` (0.190): Agora em segundo lugar, mostrando forte poder preditivo.
3.  `ht_touches` (0.160): Continua muito importante.
4.  `ht_dribbles` (0.078): Sua importância também aumentou.
5.  `player_id_x_world_cup` (0.067): O termo de interação com a Copa do Mundo continua importante, mas sua importância relativa diminuiu em comparação com as features de topo.
6.  `team_id_encoded` (0.037): Continua relevante.
7.  `player_id_encoded` (0.023): Sua importância diminuiu significativamente.
8.  `avg_ht_touches_ligue1`, `avg_ht_dribbles_ligue1`, `player_id_x_ligue_1`, `avg_ht_passes_ligue1` (baixa importância): Estas features mantêm baixa importância relativa.
9.  `competition_type_Ligue 1` (0.004) e `competition_type_World Cup` (0.00004): As features diretas de tipo de competição continuam com importância muito baixa, especialmente para a Copa do Mundo.

### 4. Análise de Generalização do "Efeito Torneio":
*   Estender a análise comparativa de desempenho (similar à de Messi) para outros jogadores presentes em ambos os datasets (Copa do Mundo e Ligue 1) para verificar se o "efetio torneio" é um padrão generalizável.

### 5. Visualização Aprofundada:
*   Criar visualizações que explorem as novas features e a relação entre o desempenho em diferentes competições.
*   Visualizar a distribuição do "efeito torneio" entre os jogadores.

## Próximos Passos Refinados:

1.  **Aprofundar Feature Engineering:**
    *   Explorar métodos mais sofisticados para capturar o "efeito torneio" (e.g., termos de interação, codificações mais complexas).
    *   Considerar outras features dos dados brutos de eventos (se disponíveis e relevantes, como xG, xA, passes-chave, desarmes, etc.).
    *   Criar features que representem a "forma" do jogador (e.g., desempenho médio nas últimas N partidas).
2.  **Melhoria do Modelo:**
    *   Realizar otimização de hiperparâmetros para o `GradientBoostingRegressor` para tentar melhorar ainda mais o R2.
    *   Experimentar com outros algoritmos de regressão (e.g., XGBoost, LightGBM) se o desempenho do Gradient Boosting não for satisfatório após a otimização.
3.  **Exploração de Dados Adicional:**
    *   Investigar a baixa importância das features diretas `competition_type`. O "efeito torneio" é realmente menos generalizável, ou a representação da feature precisa ser aprimorada?
    *   Analisar o desempenho de outros jogadores que participaram tanto da Ligue 1 quanto da Copa do Mundo para validar ou refutar a generalização do "efeito torneio".
    *   Realizar uma análise mais aprofundada da relação entre as features de atividade no primeiro tempo (`ht_passes`, `ht_touches`, `ht_dribbles`) e `total_shots_on_goal`.