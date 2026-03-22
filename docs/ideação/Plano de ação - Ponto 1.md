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

## Próximos Passos
*   Pesquisar fontes de dados para desempenho de jogadores em ligas anteriores.
*   Aprofundar a análise e visualização dos datasets existentes, focando nas features identificadas como relevantes.
*   Considerar a criação de novas features a partir dos dados brutos (e.g., posse de bola, passes completos, etc.) para enriquecer os modelos.