
# Relatório de Avaliação dos Modelos Preditivos Iniciais

**Data:** 22 de março de 2026
**Autor:** JACKBOT
**Assunto:** Avaliação dos resultados do ciclo inicial de modelagem preditiva para partidas de futebol.

---

### 1. Sumário Executivo (TL;DR)

Este relatório detalha os resultados da primeira iteração de modelagem preditiva, que utilizou dados do primeiro tempo dos jogos da Copa do Mundo de 2022 para prever resultados finais.

*   **Previsão de Resultado da Partida (Vitória/Derrota/Empate):** **Sucesso Promissor.** O modelo alcançou 75% de acurácia, demonstrando alta viabilidade. Recomenda-se focar na melhoria deste modelo.
*   **Previsão de Chutes a Gol do Time:** **Sucesso Parcial.** O modelo demonstrou ter algum poder preditivo (R² de 0.25), mas com margem para melhorias significativas.
*   **Previsão de Chutes a Gol do Jogador:** **Inviável com a Abordagem Atual.** O modelo não demonstrou qualquer poder preditivo (R² negativo), indicando que as features utilizadas são insuficientes para a complexidade da tarefa.

**Recomendação Estratégica:** Priorizar o desenvolvimento dos modelos de previsão de **Resultado da Partida** e **Chutes a Gol do Time**. Despriorizar o modelo de previsão para jogadores individuais até que features mais ricas (ex: dados posicionais, histórico do jogador) possam ser exploradas.

---

### 2. Objetivo e Metodologia

O objetivo deste teste era validar a hipótese de que estatísticas agregadas do primeiro tempo de uma partida de futebol podem ser usadas para prever com precisão:
1.  O resultado final da partida (Classificação).
2.  O número total de chutes a gol de um time (Regressão).
3.  O número total de chutes a gol de um jogador (Regressão).

A metodologia consistiu em:
1.  **Extração de Dados:** Utilizar dados de eventos e escalações dos 64 jogos da Copa do Mundo de 2022.
2.  **Engenharia de Features:** Calcular estatísticas (gols, chutes, cantos, etc.) para times e jogadores, baseadas exclusivamente em eventos ocorridos no primeiro tempo.
3.  **Modelagem:** Treinar e avaliar três modelos distintos (`RandomForestClassifier` e `RandomForestRegressor`) usando uma divisão de 80/20 para treino e teste.

---

### 3. Avaliação Detalhada dos Modelos

#### 3.1. Modelo 1: Previsão de Resultado da Partida (Classificação)

Este modelo buscou prever se o time da casa iria Vencer, Perder ou Empatar.

**Métricas de Performance:**
*   **Acurácia Geral:** **0.75 (75%)**
*   **Relatório de Classificação:**
    ```
                  precision    recall  f1-score   support
            Draw       1.00      0.75      0.86         4
            Loss       0.75      0.60      0.67         5
             Win       0.67      0.86      0.75         7
    ```

**Interpretação:**
*   Uma acurácia de 75% é um resultado inicial muito forte, indicando que os eventos do primeiro tempo contêm um sinal preditivo claro sobre o resultado final do jogo.
*   A **precisão de 1.00 para "Draw"** é notável: quando o modelo previu um empate, ele acertou 100% das vezes no conjunto de teste. No entanto, o recall de 0.75 mostra que ele não identificou todos os empates que ocorreram.
*   O modelo teve um bom equilíbrio entre precisão e recall para "Win", sendo a classe com mais acertos.

**Conclusão:** **Altamente Viável.** O modelo já possui um desempenho útil e serve como um excelente baseline para futuras iterações.

#### 3.2. Modelo 2: Previsão de Chutes a Gol do Time (Regressão)

Este modelo buscou prever o número total de chutes a gol que um time daria na partida.

**Métricas de Performance:**
*   **Erro Médio Absoluto (MAE):** **2.23**
*   **Coeficiente de Determinação (R²):** **0.25**

**Interpretação:**
*   O MAE de 2.23 significa que, em média, as previsões do modelo estiveram erradas por aproximadamente 2 chutes. Considerando que a média de chutes a gol por time em um jogo é variável, este erro é moderado.
*   O R² de 0.25 é a métrica chave: indica que as features do primeiro tempo **explicam 25% da variabilidade** no total de chutes a gol. Isso confirma que há uma relação estatisticamente significativa, embora não seja o único fator em jogo. Fatores como mudanças táticas no segundo tempo, substituições e condicionamento físico (não medidos) provavelmente explicam os 75% restantes.

**Conclusão:** **Parcialmente Viável.** O modelo tem poder preditivo, mas não é preciso o suficiente para ser considerado confiável. Há um claro potencial para melhoria através da adição de mais features.

#### 3.3. Modelo 3: Previsão de Chutes a Gol do Jogador (Regressão)

Este modelo buscou prever o número total de chutes a gol que um jogador individualmente daria na partida.

**Métricas de Performance:**
*   **Erro Médio Absoluto (MAE):** **0.24**
*   **Coeficiente de Determinação (R²):** **-0.02**

**Interpretação:**
*   O MAE baixo é enganoso. A grande maioria dos jogadores em uma partida termina com 0 chutes a gol. Um modelo que simplesmente prevê "0" ou um valor próximo de zero para todos terá um MAE baixo, mas não oferece nenhum valor real.
*   O **R² negativo é o resultado definitivo.** Um valor de R² negativo significa que o desempenho do modelo é **pior do que um modelo ingênuo** que simplesmente previsse o valor médio de chutes a gol para todos os jogadores. Isso invalida a hipótese de que as features simples utilizadas (toques, passes, dribles no 1º tempo) são suficientes para prever uma ação tão específica e relativamente rara como um chute a gol de um jogador.

**Conclusão:** **Inviável com a Abordagem Atual.** O problema é muito complexo para as features disponíveis. O modelo falhou em encontrar qualquer padrão preditivo.

---

### 4. Recomendações e Próximos Passos

Com base nesta avaliação, as seguintes ações são recomendadas:

1.  **Prioridade Alta - Iterar no Modelo de Resultado da Partida:**
    *   **Ação:** Focar em melhorar a acurácia de 75%.
    *   **Próximos Passos:**
        *   **Engenharia de Features:** Adicionar novas features, como passes no terço final, duelos, interceptações e a diferença nas estatísticas entre o time da casa e o visitante.
        *   **Testar Novos Algoritmos:** Avaliar modelos como `GradientBoostingClassifier` e `XGBoost`, que frequentemente superam o `RandomForest`.

2.  **Prioridade Média - Iterar no Modelo de Chutes a Gol do Time:**
    *   **Ação:** Tentar aumentar o R² de 0.25.
    *   **Próximos Passos:** As mesmas ações do ponto 1 (novas features e novos algoritmos) podem ser aplicadas aqui e devem gerar melhorias.

3.  **Prioridade Baixa - Descontinuar/Pivotar o Modelo de Jogador:**
    *   **Ação:** Pausar o desenvolvimento deste modelo.
    *   **Justificativa:** A abordagem atual não funciona. Para ter sucesso, seria necessário um investimento significativamente maior em engenharia de features, potencialmente explorando os dados de "360" (posicionamento de todos os jogadores) ou integrando dados históricos de performance de cada jogador, o que foge ao escopo de um teste rápido.
