### **Task: [Modelagem] Iteração 2 - Melhoria dos Modelos Preditivos**

**User Story:**
> **Como** um Cientista de Dados,
> **Eu quero** refinar a engenharia de features e experimentar algoritmos mais avançados,
> **Para que** eu possa melhorar a performance preditiva dos modelos de resultado da partida e de chutes a gol do time.

**Descrição/Contexto:**
A primeira iteração de modelagem (`initial_model_evaluation_report.md`) demonstrou que a previsão de **resultado da partida** é promissora (75% de acurácia) e a de **chutes a gol do time** é parcialmente viável (R² de 0.25). O modelo de jogador foi considerado inviável e será descontinuado por enquanto.

Esta segunda iteração focará em duas frentes principais para melhorar esses resultados:
1.  **Engenharia de Features Avançada:** As features atuais são simples agregações. A criação de features que capturem a *diferença* de performance entre os times e outras métricas mais sofisticadas pode adicionar um poder preditivo significativo.
2.  **Algoritmos Mais Potentes:** O `RandomForest` é um bom baseline, mas algoritmos de Gradient Boosting como o `XGBoost` são o estado-da-arte para dados tabulares e frequentemente oferecem maior precisão.

**Technical Tasks (Plano de Implementação Detalhado):**

1.  **Atualizar o Script de Processamento (`data_processing.py`):**
    *   **Novas Features de Diferença (para `wc2022_team_outcome.csv`):**
        *   Para cada estatística do primeiro tempo (gols, chutes, posse de bola, etc.), calcular a diferença entre o time da casa e o visitante (ex: `half_time_shots_difference = home_shots - away_shots`).
        *   Adicionar essas features de diferença ao dataset, pois elas capturam o domínio relativo de um time sobre o outro, o que pode ser mais preditivo do que os valores brutos.
    *   **Manter a Estrutura dos Outros Datasets:** Nenhuma mudança é necessária para `wc2022_team_sog.csv` e `wc2022_player_sog.csv` nesta fase, pois as features de time já são calculadas por linha.

2.  **Atualizar o Script de Treinamento (`train_models.py`):**
    *   **Adicionar Nova Dependência:** Incluir `xgboost` no arquivo `requirements.txt`.
    *   **Substituir Algoritmos:**
        *   Para o **Modelo 1 (Classificação)**, substituir `RandomForestClassifier` por `XGBClassifier`.
        *   Para o **Modelo 2 (Regressão)**, substituir `RandomForestRegressor` por `XGBRegressor`.
    *   **Implementar Hyperparameter Tuning (Opcional, mas recomendado):**
        *   Para ambos os modelos, usar `GridSearchCV` ou `RandomizedSearchCV` para encontrar a melhor combinação de hiperparâmetros (ex: `n_estimators`, `max_depth`, `learning_rate`). Isso automatiza o processo de otimização do modelo.
        *   *Nota: O tuning pode aumentar o tempo de execução do script.*
    *   **Atualizar Relatório de Performance:**
        *   Manter a impressão das métricas (Acurácia, Relatório de Classificação, MAE, R²) para os novos modelos.
        *   Adicionar uma comparação simples no log do console, mostrando a performance do modelo antigo vs. o novo (ex: "Acurácia do RandomForest: 0.75 -> Acurácia do XGBoost: X.XX").

**Acceptance Criteria (Definition of Done):**

*   [ ] O arquivo `requirements.txt` é atualizado para incluir `xgboost`.
*   [ ] O script `data_processing.py` é modificado para adicionar features de diferença ao dataset `wc2022_team_outcome.csv`.
*   [ ] O script `train_models.py` é atualizado para usar `XGBClassifier` e `XGBRegressor`.
*   [ ] O script `train_models.py` executa sem erros e imprime os relatórios de performance para os novos modelos.
*   [ ] O novo **Modelo 1 (Resultado da Partida)** demonstra uma acurácia superior à linha de base de 75%.
*   [ ] O novo **Modelo 2 (Chutes a Gol do Time)** demonstra um R² superior à linha de base de 0.25.
