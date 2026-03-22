# JACKBOT: Projeto de Análise e Previsão Esportiva

Este repositório contém o código-fonte e a pesquisa para o **JACKBOT**, um projeto focado na aplicação de técnicas de aprendizado de máquina para prever resultados em partidas de futebol. Este é um projeto orientado à pesquisa, com o objetivo de explorar a viabilidade de diferentes modelos preditivos.

## Sumário da Pesquisa

A pesquisa até o momento focou em estabelecer um pipeline de ponta a ponta para processamento de dados, treinamento e avaliação de modelos, utilizando um dataset limitado (Copa do Mundo 2022) para um ciclo de desenvolvimento rápido.

1.  **Iteração 1 (Baseline):** Utilizando um modelo `RandomForest`, alcançamos uma **acurácia de 75%** na previsão de resultados da partida e um **R² de 0.25** na previsão de chutes a gol por time. A previsão de chutes por jogador se mostrou inviável.

2.  **Iteração 2 (Aprimoramento):** Ao trocar para `XGBoost` e adicionar features de diferença de estatísticas, a acurácia do modelo de resultado caiu para **69%**, enquanto o R² do modelo de chutes a gol do time subiu para **0.32**. A queda na acurácia, mesmo com um modelo mais robusto, evidencia a alta variância e o risco de overfitting nos dados limitados.

3.  **Proposta para Próxima Etapa:** A próxima fase da pesquisa deve se concentrar em escalar a solução para o **dataset completo de 11GB**. O objetivo será adaptar o pipeline de processamento de dados para lidar com o volume e, em seguida, reavaliar os modelos `RandomForest` e `XGBoost`. Isso permitirá validar a real capacidade de generalização dos modelos e da engenharia de features desenvolvida até aqui.

## Objetivo do Projeto

O objetivo principal é construir e avaliar modelos capazes de prever vários eventos dentro de uma partida de futebol, usando dados de eventos do primeiro tempo para prever os resultados finais. As principais tarefas de previsão são:

1.  **Previsão de Resultado da Partida (Classificação):** Prever se o time da casa irá Vencer, Perder ou Empatar.
2.  **Chutes a Gol do Time (Regressão):** Prever o número total de chutes a gol de cada time.
3.  **Chutes a Gol de Jogador (Regressão):** Prever o número total de chutes a gol de cada jogador individualmente.

O escopo inicial está focado no conjunto de dados da **Copa do Mundo da FIFA 2022**, fornecido pela StatsBomb.

## Status e Resultados

### Iteração 1: Modelos de Baseline (RandomForest)

A avaliação inicial, documentada em `docs/initial_model_evaluation_report.md`, forneceu os seguintes benchmarks:

*   ✅ **Modelo de Resultado da Partida:** Altamente promissor, com uma precisão inicial de **75%**.
*   ⚠️ **Modelo de Chutes a Gol do Time:** Parcialmente viável, explicando cerca de **25%** da variância (R² = 0.25).
*   ❌ **Modelo de Chutes a Gol do Jogador:** Inviável com as features atuais (R² < 0), sendo despriorizado.

### Iteração 2: Modelos Aprimorados (XGBoost)

Na segunda iteração, foram introduzidas novas features (`_diff`) e o algoritmo foi trocado para XGBoost, com os seguintes resultados:

*   **Modelo de Resultado da Partida:** A performance diminuiu para **69% de acurácia**. A troca de algoritmo e a inclusão de novas features não resultaram em melhoria, possivelmente devido à alta variância em um dataset pequeno.
*   **Modelo de Chutes a Gol do Time:** Houve uma melhora modesta, com o R² subindo para **0.32**. O modelo agora explica 32% da variância, indicando um pequeno avanço na capacidade preditiva.

### Análise sobre Overfitting

É crucial destacar que os resultados atuais são baseados em um dataset muito pequeno e específico (Copa do Mundo 2022). Existe um **risco muito alto de overfitting**. Os modelos podem estar aprendendo padrões que não se generalizam para outros campeonatos ou temporadas.

O verdadeiro valor desta fase inicial não está nos modelos em si, mas no desenvolvimento de um pipeline de processamento e avaliação que poderá ser aplicado ao dataset completo de 11GB no futuro. Os scores de performance atuais devem ser vistos como um teto otimista.

## Tecnologias Utilizadas

*   **Linguagem:** Python
*   **Bibliotecas:**
    *   Pandas
    *   Scikit-learn
    *   XGBoost
    *   Matplotlib & Seaborn

## Configuração e Uso

### 1. Pré-requisitos

*   Python 3.x
*   Os dados abertos da StatsBomb para a Copa do Mundo da FIFA 2022. Coloque a pasta `data` (contendo `competitions.json`, `events/`, `matches/`, etc.) dentro de um diretório `Datasets/` na raiz do projeto.
    *Nota: O arquivo `.gitignore` está configurado para ignorar o diretório `Datasets/`.*

### 2. Instalação

Clone o repositório e instale as dependências necessárias:

```bash
git clone <url-do-repositorio>
cd JACKBOT
pip install -r requirements.txt
```

### 3. Executando os Pipelines

Os scripts podem ser executados para treinar e avaliar os modelos.

1.  **Processar os Dados:**
    Este script (`data_processing.py`) lê os JSONs brutos da StatsBomb e os converte nos CSVs necessários para o treinamento.
    ```bash
    python data_processing.py
    ```

2.  **Treinar Modelos de Baseline (RandomForest):**
    ```bash
    python train_baseline.py
    ```

3.  **Treinar Modelos Aprimorados (XGBoost):**
    ```bash
    python train_improved.py
    ```

### 4. Gerando Gráficos de Performance

Execute os scripts de visualização para gerar e salvar os gráficos de avaliação no diretório `charts/`.

*   **Gráficos do Baseline:**
    ```bash
    python visualize_baseline_results.py
    ```
*   **Gráficos dos Modelos Aprimorados:**
    ```bash
    python visualize_improved_results.py
    ```

## Visualização de Resultados

Os scripts de visualização geram os seguintes arquivos no diretório `charts/`:

*   `baseline_outcome_confusion_matrix.png`: Matriz de confusão para o modelo de resultado da partida (Baseline).
*   `baseline_team_sog_scatter.png`: Gráfico de dispersão para o modelo de chutes a gol do time (Baseline).
*   `improved_outcome_confusion_matrix.png`: Matriz de confusão para o modelo de resultado da partida (Aprimorado com XGBoost).
*   `improved_team_sog_scatter.png`: Gráfico de dispersão para o modelo de chutes a gol do time (Aprimorado com XGBoost).

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.