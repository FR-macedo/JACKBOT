### **Task: [Modelagem] Treinar e Avaliar Modelos Preditivos**

**User Story:**
> **Como** um Cientista de Dados,
> **Eu quero** treinar e avaliar modelos preditivos usando os datasets processados,
> **Para que** eu possa medir a performance de cada previsão e determinar sua viabilidade.

**Descrição/Contexto:**
Esta tarefa utiliza os três arquivos CSV (`wc2022_team_outcome.csv`, `wc2022_team_sog.csv`, `wc2022_player_sog.csv`) gerados na fase anterior. O objetivo é criar um script que treine um modelo para cada dataset e reporte métricas de performance claras, permitindo-nos avaliar a qualidade das previsões baseadas em dados do primeiro tempo.

**Technical Tasks (Plano de Implementação Detalhado):**

1.  **Criação do Script de Treinamento (`train_models.py`):**
    *   O script precisará da biblioteca `scikit-learn`, além de `pandas`.
    *   O script será estruturado para treinar e avaliar os três modelos sequencialmente.

2.  **Modelo 1: Previsão de Resultado do Jogo (Classificação)**
    *   Carregar `wc2022_team_outcome.csv`.
    *   Definir as colunas de features (X) - todas as colunas de estatísticas do 1º tempo - e a coluna alvo (y) - `final_outcome`.
    *   Dividir os dados em conjunto de treino e teste (ex: 80/20) usando `train_test_split`.
    *   Instanciar e treinar um modelo `RandomForestClassifier`.
    *   Fazer previsões no conjunto de teste.
    *   Calcular e imprimir a **Acurácia** e o **Relatório de Classificação** (`classification_report`).

3.  **Modelo 2: Previsão de Chutes a Gol do Time (Regressão)**
    *   Carregar `wc2022_team_sog.csv`.
    *   Definir features (X) - estatísticas do 1º tempo - e o alvo (y) - `total_shots_on_goal`.
    *   Dividir os dados em treino e teste.
    *   Instanciar e treinar um modelo `RandomForestRegressor`.
    *   Fazer previsões no conjunto de teste.
    *   Calcular e imprimir o **Erro Médio Absoluto (MAE)** e o **Coeficiente de Determinação (R²)**.

4.  **Modelo 3: Previsão de Chutes a Gol do Jogador (Regressão)**
    *   Carregar `wc2022_player_sog.csv`.
    *   Definir features (X) - estatísticas do jogador no 1º tempo - e o alvo (y) - `total_shots_on_goal`.
    *   Dividir os dados em treino e teste.
    *   Instanciar e treinar um modelo `RandomForestRegressor`.
    *   Fazer previsões no conjunto de teste.
    *   Calcular e imprimir o **Erro Médio Absoluto (MAE)** e o **Coeficiente de Determinação (R²)**.

**Acceptance Criteria (Definition of Done):**

*   [ ] Um script Python chamado `train_models.py` existe no repositório.
*   [ ] O script executa do início ao fim sem erros.
*   [ ] O script imprime no console um relatório de performance claro para cada um dos três modelos.
*   [ ] O relatório do Modelo 1 (Classificação) inclui a acurácia.
*   [ ] Os relatórios dos Modelos 2 e 3 (Regressão) incluem o MAE e o R².
