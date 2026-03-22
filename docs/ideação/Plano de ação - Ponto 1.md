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
*   **Desafios:**
    *   **Fonte de Dados:** Onde encontrar dados de ligas anteriores? (e.g., StatsBomb, Opta, FBref, APIs de futebol).
    *   **Mapeamento de Jogadores:** Como garantir que os jogadores da Copa do Mundo sejam corretamente identificados nas ligas anteriores? (IDs de jogadores, nomes).
    *   **Métricas de Desempenho:** Quais métricas são mais relevantes para avaliar o desempenho de um jogador em ligas anteriores que possam impactar seu desempenho na Copa do Mundo? (Gols, Assistências, Passes Completos, Dribles, Desarmes, xG, xA, etc.).
*   **Passos:**
    *   Identificar uma fonte de dados confiável para ligas anteriores.
    *   Desenvolver um script para coletar e integrar esses dados com os dados da Copa do Mundo.
    *   Definir um conjunto de métricas chave para avaliação de jogadores.
    *   Visualizar o desempenho dos jogadores antes da Copa do Mundo.

### 1.3. Avaliação e Agrupamento de Jogadores em "Times Parceiros"
*   **Objetivo:** Desenvolver uma metodologia para agrupar jogadores de alto desempenho em times hipotéticos ("times parceiros") para análise.
*   **Passos:**
    *   **Critérios de Seleção:** Definir critérios claros para considerar um jogador como "melhor" (e.g., top X% em xG, xA, ou uma combinação de métricas).
    *   **Metodologia de Agrupamento:**
        *   Como formar esses times? Aleatoriamente? Por posição? Por pontuação geral?
        *   Considerar a viabilidade de simular o desempenho desses times.
    *   **Visualização:** Como apresentar os resultados desses agrupamentos? (e.g., comparação de métricas agregadas dos "times parceiros" vs. times reais).

## Próximos Passos
*   Pesquisar fontes de dados para desempenho de jogadores em ligas anteriores.
*   Aprofundar a análise e visualização dos datasets existentes, focando nas features identificadas como relevantes.
*   Considerar a criação de novas features a partir dos dados brutos (e.g., posse de bola, passes completos, etc.) para enriquecer os modelos.