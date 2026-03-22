# Resumo Executivo  
Uma **assistente virtual local** sem GPU (CPU-only) em notebook com 9 GB de RAM exige modelos de linguagem (LLMs) compactos e otimizados. Propomos usar modelos quantizados/compromissados (por ex. LLaMA 3.1 de 8B em 4-bit ~7–8 GB【1†L161-L168】, Mistral 7B Q4_K_M ~6,9 GB【1†L189-L198】, Gemma3 4B Q4_K_M ~1,7 GB【25†L211-L218】, DeepSeek-7B Q4_K_M ~6,7 GB【25†L272-L280】 etc.) combinados com técnicas de compressão (INT4/8, GPTQ, AWQ, LoRA/PEFT) que reduzem significativamente o uso de memória【33†L78-L82】【35†L239-L247】. Indicamos uma arquitetura local leve: um serviço de inferência LLM (por ex. **LMStudio/llmster** com CPU multithread), API REST/CLI para consultas e interface web simples (p. ex. Streamlit) para usuários, e armazenamento local de logs. O pipeline de explicação inclui pré-processamento dos dados de entrada (limpeza, transformação), formatação de prompt (template de explicação com metadados, features importantes, incertezas e contexto), inferência do LLM, pós-processamento (ajustes de texto, cache de respostas) e monitoração. Devem ser usados metadados adicionais – como informações da instância, contexto de negócio, histórico do usuário e coeficientes de incerteza – para enriquecer as explicações. Para avaliar as explicações, mediremos **fidelidade** (se a explicação reflete o modelo【19†L450-L454】), **correção/factualidade** (alinhamento com fatos e lógica do modelo【19†L538-L544】), **compacidade** (concicidade da explicação【19†L543-L551】) e **utilidade ao usuário** (por exemplo, através de testes de usuário). Exemplos de prompt/template em português cobrem níveis executivos, técnicos e de recomendações práticas. Foram compilados recursos oficiais do LMStudio, repositórios de modelos (Hugging Face, TheBloke) e ferramentas de quantização (BitsAndBytes, GPTQ, AWQ), incluindo referências em português quando disponíveis【1†L159-L166】【33†L78-L82】.  

## 1. Requisitos e Dados de Entrada  
Como a tarefa preditiva e o formato dos dados não foram especificados, consideramos cenários genéricos (dados tabulares, texto livre, etc.) e listamos as informações extras necessárias além da predição bruta:

- **Dados de entrada brutos**: as características originais e pré-processadas usadas pelo modelo (valores, unidades, categorias), para contextualizar a explicação.  
- **Metadados do modelo**: identificação do modelo (tipo, versão, data de treinamento) e métricas de performance conhecidas (precisão, AUC etc.), úteis para transparência e auditoria.  
- **Incerteza/Intervalos de confiança**: quantificações da confiança na previsão (probabilidade, desvio padrão, intervalo de confiança) informam o grau de certeza do resultado.  
- **Principais features/atributos**: importância dos atributos de entrada que mais influenciaram a predição (via métodos de interpretabilidade como SHAP/LIME【12†L180-L184】), para indicar o “porquê” da decisão do modelo.  
- **Contexto do usuário e negócio**: histórico ou perfil do usuário (se houver contexto pessoal), e parâmetros de negócio (por ex. regras de custo/benefício, regimes regulatórios) que podem influenciar a explicação ou recomendações.  
- **Glossário de termos**: definições de termos técnicos/domínio usados na saída, para tornar a explicação didática; útil quando o usuário não for especialista.  
- **Exemplos contrafactuais**: “o que aconteceria se um atributo X fosse outro valor” – pequenos ajustes nos dados de entrada que alteram a previsão, mostrando cenários próximos com resultado diferente【7†L68-L70】.  
- **Limites e políticas**: avisos sobre a aplicabilidade do modelo, limites de validade e políticas de privacidade (por ex. se dados sensíveis foram usados). Esse contexto legal/regulatóro aumenta a confiabilidade da explicação.  

Esses itens formam o contexto informativo que guia o gerador de explicações. Por exemplo, saber as features mais importantes (via valores SHAP) ajuda a destacar quais variáveis motivaram a predição【12†L180-L184】, e contrafactuais (mínimas mudanças para inverter a decisão) ilustram as fronteiras da decisão【7†L68-L70】. A coleta desses dados auxilia no pós-processamento e na personalização das respostas.

## 2. Modelos Leves e Técnicas de Compressão/PEFT  
Com 9 GB de RAM e sem GPU, recomendamos LLMs de 3–8B parâmetros quantizados. A tabela a seguir compara opções populares viáveis:

| **Modelo**      | **Tamanho (p)** | **Memória quant. (~)** | **Latência (CPU)** | **Precisão**      | **Integração**       |
|-----------------|-----------------|------------------------|--------------------|-------------------|----------------------|
| *LLaMA 3.1 8B*  | 8B              | Q2_K: 3,2 GB (RAM~7,2 GB)【1†L161-L168】 | média (10–20 tok/s) | Muito boa (Avaliação AlpacaEval)【1†L161-L168】 | Fácil (formato GGUF, LMStudio) |
| *Mistral 7B*    | 7B              | Q4_K_M: 4,37 GB (RAM~6,9 GB)【1†L189-L198】 | alta (15–25 tok/s) | Muito boa (conhec. geral, código)【1†L189-L198】 | Fácil (open-source) |
| *Gemma 3 4.5B*  | 4.5B            | Q4_K_M: 1,71 GB (RAM~≥2 GB)【25†L211-L218】 | muito alta (30–50 tok/s) | Boa (texto, P&R básicos)【25†L211-L218】 | Muito fácil |
| *Gemma 7B*      | 7B              | Q5_K_M: 6,14 GB; Q6_K: 7,01 GB【25†L231-L239】 | média (10–20 tok/s) | Muito boa (multi-tarefa)【25†L231-L239】 | Fácil |
| *Phi-3 Mini 3.8B*| 3.8B           | Q8_0: 4,06 GB (RAM~7,5 GB)【25†L251-L258】 | média/alta (20–30 tok/s) | Boa/Ótima (raz. lógica, código)【25†L251-L258】 | Fácil |
| *DeepSeek R1 7B* | 7B             | Q4_K_M: 4,22 GB (RAM~6,7 GB)【25†L272-L280】 | alta (15–25 tok/s) | Muito boa (raciocínio, código)【25†L272-L280】 | Fácil |
| *Qwen 7B Chat*  | 7B              | Q5_K_M: 5,53 GB (RAM~6 GB)【25†L300-L308】 | média (10–15 tok/s) | Boa (multilíngue, matem., codificação)【25†L300-L308】 | Fácil |
| *DeepSeek-coder 6.7B* | 6.7B      | 3,8 GB (RAM~6 GB)【25†L314-L323】      | alta (20–30 tok/s) | Ótima em código (geração e interpretação)【25†L314-L323】 | Fácil (especializado) |

A memória estimada considera o modelo quantizado em formato GGUF (por ex., *Q4_K_M* de Llama.cpp/LLaMA.cpp). Esses modelos comportam-se bem em CPUs modernos (AVX2/AVX-512) e são suportados pelo **LMStudio**. Os valores de *Precisão* são qualitativos baseados em benchmarks públicos (ex.: AlpacaEval, HumanEval) e relatos da comunidade【1†L161-L168】【25†L272-L280】. 

Além da quantização, mencionamos técnicas **PEFT/LoRA**: por exemplo, aplicar *LoRA* em um modelo quantizado de 4-bit (como QLoRA) reduz requisitos de treinamento e permite ajuste fino com poucos parâmetros【27†L44-L48】. Essa técnica (PEFT – *Parameter-Efficient Fine-Tuning*) adapta grandes LLMs sem re-treinar todos os pesos, tornando viável treinar localmente【27†L44-L48】. Combinado com quantização (bitsandbytes 4-bit), possibilita customizar o modelo sem estourar RAM.

**Comparação de técnicas de compressão**:

| **Técnica**    | **Tipo**       | **Uso de Memória**    | **Velocidade**      | **Qualidade (trade-off)**   | **Observações**                  |
|----------------|----------------|-----------------------|---------------------|----------------------------|----------------------------------|
| *INT8 (bnb)*   | Pós-treinamento (8-bit) | ~½ da original【33†L78-L82】 | ↑ moderate (2–4×)     | Alta (perda mínima)         | Fácil via HuggingFace/transformers |
| *INT4 (bnb)*   | Pós-treinamento (4-bit) | ~¼ da original【33†L78-L82】 | ↑ alta (3–5×)         | Boa (pequena degradação)    | Requer calibragem, via BitsAndBytes  |
| *GPTQ-4 (4-bit)* | Treinamento pós (layerwise) | ~¼ da original | ↑ muito (5×+)    | Média-alta (com reconstrução) | Melhor para inferência GPU, Python/llama.cpp       |
| *AWQ (4-bit)*  | Pós-treinamento (atividade) | ~¼ da original | ↑ muito (5×+)    | Alta (sem perda)           | Preserva pesos ativos【35†L176-L185】 |
| *QLoRA*        | Fine-tuning (4-bit) | ~¼ da original + LoRA | ↑ alta (vLLM acelera) | Alta (mantém precisão) | Ajuste fino local, baseado em 4-bit + LoRA |
| *LoRA*         | Fine-tuning (64-bit) | modelo intacto (RAM ↑) | lenta (full peso)   | Sem alteração de qualidade| Apenas treinamento eficiente, não reduz inferência |
| *binário/GGUF* | Sem mod (full)  | 100% (p=32-bit)     | lenta               | Base                       | Não recomendado em 9GB        |

Os valores de memória referem-se a modelos de 7–8B (FP32 ~28 GB, FP16 ~14 GB, INT8 ~7 GB【33†L78-L82】). **AWQ** (Activation-aware Quantization) e **GPTQ** são opções de quantização preciso: AWQ, por exemplo, preserva pesos importantes avaliando ativações【35†L176-L185】, atingindo desempenho e fidelidade elevados. A técnica recomendada depende do caso: por exemplo, para *máxima velocidade* considerar AWQ+vLLM; para *máxima qualidade* usar INT8/FP16; para *retreinamento local*, usar QLoRA【35†L311-L320】.  

## 3. Pipeline de Explicação (pré/prompts/pós/caching)  
O pipeline geral integra o modelo preditivo original e o gerador de explicações LLM. A figura abaixo ilustra esse fluxo (Mermaid):

```mermaid
graph TD
  A[Dados de entrada brutos] --> B[Pré-processamento\n(limpeza, normalização)]
  B --> C[Modelo Preditivo\n(previsão)]
  C --> D[Coleta de contexto:\nfeatures, incerteza, metadados]
  D --> E[Formatação de Prompt\n(template de explicação)]
  E --> F[LLM (LMStudio)\ngera explicação textual]
  F --> G[Pós-processamento\ne ajustes (gramática, disclaimers)]
  G --> H[Resposta explicativa gerada]
  D -->|cache| I[Caching de contexto]
  F -->|log| J[Armazenamento de logs]
```

1. **Pré-processamento**: coleta das entradas do usuário e transformação no formato esperado (tratamento de valores faltantes, codificação de categorias, normalização). Exemplo: converter datas para características, categorizar texto, etc. Também calcula estatísticas de incerteza (intervalos de predição, entropia). Esta etapa prepara os **metadados** que serão incluídos na explicação (por ex. valores de entrada padrão vs atípicos).  

2. **Predição e coleta de contextos**: o modelo preditivo (externo ao LLM) é executado, gerando a previsão. Em paralelo, computam-se informações de apoio: incerteza (probabilidade prevista ou intervalo de confiança), importâncias de feature (via explainer como SHAP【12†L180-L184】), histórico do usuário e contexto de negócio relevante (ex.: regras de negócio que afetam a interpretação). Esses dados formam a instância explicável.  

3. **Formatação de Prompt**: montamos um prompt de texto para o LLM, inserindo a previsão e todos os itens acima num template. Por exemplo:  
   > *“Nosso modelo preditivo indicou [resultado]. Os principais fatores que influenciaram essa previsão foram [lista de features importantes e valores]. Considere que a incerteza calculada é [intervalo/confiança]. Explique de forma clara o que esse resultado significa para o usuário, levando em conta [contexto do negócio].”*  

   Podem ser usados diferentes templates para cada nível de detalhe (ver seção de exemplos). O prompt deve organizar as informações didaticamente, pedindo ao LLM para explicar de acordo com o perfil do usuário.

4. **Inferência do LLM**: utiliza-se o modelo de linguagem local no LMStudio (llmster). Recomenda-se diminuir tokens máximos (p. ex. n_ctx=2048) e limitar threads para conter o uso de memória. É possível ativar *streaming* no LMStudio para visualizar a geração token a token. Opcionalmente, usar **cache de prompts/explicações** para respostas repetidas, evitando recomputar.  

5. **Pós-processamento**: a saída do LLM é revisada automaticamente: por exemplo, corrigir ortografia/gramática (biblioteca de linguagem natural) e inserir avisos de limitação (“Essa explicação é apenas para suporte…”). Também incorporar políticas de privacidade ou avisos de compliance se necessário. O texto final é então entregue ao usuário.  

6. **Caching e log**: respostas recentes podem ser armazenadas em cache (por ex. Redis ou arquivo local) para consultas repetidas. Paralelamente, registros de perguntas, respostas e métricas (tempo, tokens usados) são gravados em logs para monitoramento. Isto permite medir latência, detectar drift (mudança na distribuição de explicações) e fazer auditoria.  

**Estimativa de uso de memória/CPU**: Modelos ~7B em Q4_K_M consomem ~7–8 GB RAM【1†L161-L168】【25†L272-L280】. Considerar overhead adicional (~20% do tamanho de arquivo quantizado【1†L159-L166】) para ativações. Em CPU, velocidade típica é de dezenas de tokens/s (depende do processador). Pré/pós-processamento são leves em comparação. Se necessário, reduzir número de threads (p. ex. `n_threads=4`) ou baixar tamanho de batch de tokens.  

## 4. Arquitetura de Implantação Local  
Propõe-se uma arquitetura simples de serviço local, como mostra o diagrama:

```mermaid
graph LR
  subgraph **Servidor Local**
    LLMsvc[Serviço de Inferência (LMStudio/llmster)] 
    API[API Local (e.g. FastAPI)]
    Logs[Armazenamento de Logs (SQLite/CSV)]
  end
  User[Usuário / Cliente Web/CLI]
  
  LLMsvc <--> API : solicitações de inference
  API --> LLMsvc : respostas de texto
  User --> API : consulta via UI/CLI
  API --> Logs : grava queries & respostas
```

- **Serviço de Inferência**: roda o LLM via LMStudio. Pode ser o modo “headless” (*llmster*) sem interface gráfica【36†L189-L197】. Configurar para usar CPU (modo high performance numa máquina sem GPU).  
- **API Local**: expõe endpoints REST (compatíveis OpenAI ou customizados) em LAN. Pode usar frameworks Python (FastAPI/Flask). A API recebe solicitações do cliente, formata prompts, invoca o LLM e retorna respostas explicativas.  
- **Interface Web/CLI**: front-end leve (pode ser uma página web em Streamlit ou app CLI em Python) que chama a API. Permite conversação ou consulta de previsões e explicações.  
- **Armazenamento de Logs**: um banco de dados local (SQLite, CSV ou JSON) para logs de requests/responses, métricas de desempenho, feedback do usuário. Auxilia monitorar uso, debugging e avaliar qualidade das explicações ao longo do tempo.  

**Otimizações de memória**: use quantização (GGUF) e desative camadas GPU no LMStudio (ex. `n_gpu_layers=0`). Ajuste *n_threads* para o número de vCPU. No Windows, garanta no LMStudio Preferences > Engine: “CPU” e selecione nucleos específicos. Descarregue modelos (unload) quando não usados【36†L203-L208】, e use `lms server start` para manter serviço ativo【36†L203-L208】. O LMStudio gerencia cache de modelo próprio; evitar múltiplas instâncias simultâneas.  

## 5. Métricas e Testes de Qualidade das Explicações  
Para avaliar as explicações geradas, sugerimos métricas objetivas e testes manuais:  
- **Fidelidade**: mede o quão bem a explicação reflete o comportamento real do modelo. Calcula-se comparando as predições do modelo substituindo o processo de explicação e avaliando acurácia (por ex., quanto a explicação imita o modelo real)【19†L450-L454】.  
- **Precisão/Corretude (factualidade)**: verifica se as informações na explicação são consistentes com o modelo e com fatos externos. Espera-se alta *truthfulness*; explicações *honestas* não devem conter afirmações falsas. Esta métrica avalia a veracidade descritiva【19†L538-L544】.  
- **Compacidade/Concicidade**: mede o tamanho da explicação (número de palavras ou tópicos). Idealmente explicações devem ser sucintas e sem redundâncias【19†L543-L551】. Métricas como contagem de tokens ou de termos-chave (features não zero) auxiliam nesta medição.  
- **Utilidade/Entendimento**: avalia-se por usuários (experimentos humanos ou especialistas) se a explicação foi compreensível e útil para a tomada de decisão. Questões qualitativas ou pontuações (survey) podem medir clareza e relevância.  
- **Estabilidade/Reprodutibilidade**: verificar se explicações similares são geradas para inputs semelhantes (coerência). Um teste de perturbação (fazer pequenas mudanças nos dados de entrada) pode checar se a explicação muda drasticamente sem motivo.  
- **Desempenho**: latência (tempo p/ geração) e throughput são importantes para garantir interações em tempo aceitável. Métricas de monitoramento (como *tokens/s* ou tempo médio de resposta) devem ser registradas.  

**Monitoramento contínuo**: registrar métricas periódicas e feedback do usuário/operador em painel de controle local. Detectar *drift* de explicação (mudança de tendências de conteúdo) pode sinalizar necessidade de retreinamento ou ajuste de prompts. Realizar testes A/B com diferentes modelos/técnicas de explicação também ajuda a selecionar a melhor abordagem.  

## 6. Exemplos de Prompts/Templates (pt-BR)  
A seguir exemplos genéricos de prompts e templates para o LLM (adapte ao domínio específico). Usamos “PREVISÃO” como marcador do resultado do modelo e “DETALHES” como features/contexto:

- **Resumo Executivo (layman)**:  
  - Prompt: *“Nosso sistema preditivo indicou **PREVISÃO**. Em termos simples para um usuário não técnico, explique o que isso significa. Inclua apenas os pontos mais importantes e evite jargões.”*  
  - Exemplo de template gerado:  
    > “O modelo previu que a probabilidade de aprovação é **alta**, ou seja, esse caso tem boa chance de ser aprovado. Isso ocorre principalmente por causa das seguintes características: **DETALHES**. Em resumo, o resultado sugere que o usuário deve tomar a ação X. Essa previsão tem **Y%** de confiança, mas lembre-se que é apenas uma estimativa baseada nos dados atuais.”

- **Explicação Técnica (detalhada)**:  
  - Prompt: *“O modelo preditivo (XGBoost) gerou a previsão **PREVISÃO** para esta entrada. Explique detalhadamente, usando termos técnicos, quais atributos levaram a esse resultado. Cite métricas de confiança (intervalos) e destaque as features mais importantes.”*  
  - Exemplo:  
    > “A previsão **PREVISÃO** foi obtida pelo modelo XGBoost treinado em dados históricos de comportamento do cliente. As características de maior influência foram: **DETALHES**. Por exemplo, um aumento em A aumenta a probabilidade em 10%. O intervalo de confiança da previsão é [a, b], indicando [nível de incerteza]. Em termos técnicos, valores positivos de SHAP para A e negativos para B contribuíram para esta decisão【12†L180-L184】. O modelo tem precisão de 92% no conjunto de validação.”

- **Recomendações Acionáveis (nível operacional)**:  
  - Prompt: *“Com base na previsão **PREVISÃO** e nas principais razões (DETALHES), forneça recomendações práticas para o usuário ou gestor. Diga o que poderia ser feito para melhorar os resultados no futuro.”*  
  - Exemplo:  
    > “Dado que a previsão foi **PREVISÃO**, recomenda-se revisar as seguintes ações: primeiro, ajustar o parâmetro X porque **DETALHES**; segundo, coletar informações adicionais sobre Y, pois isso pode aumentar a confiança do modelo. Caso a previsão indique risco (por ex., **PREVISÃO de risco alto**), sugere-se monitorar Z de perto e reconsiderar a estratégia. Essas ações podem ajudar a alterar o cenário em estimativa futura (cenários contrafactuais) e melhorar o resultado desejado.”

Cada template insere detalhes específicos do caso e adapta o nível de tecnicidade. É possível usar o LMStudio para armazenar esses modelos de prompt e reutilizá-los conforme necessário.

## 7. Recursos e Referências Oficiais  
- **LMStudio (local)**: Site oficial para baixar/configurar: [lmstudio.ai](https://lmstudio.ai)【20†L28-L36】. A [Documentação de Desenvolvimento](https://lmstudio.ai/docs/developer) detalha CLI (`lms daemon up`, `lms server start`, etc.)【36†L189-L197】【36†L203-L208】 e API compatível OpenAI.  
- **Catálogo de Modelos LMStudio**: modelos gratuitos em [lmstudio.ai/models](https://lmstudio.ai/models) (ex.: Qwen, Gemma, DeepSeek listados)【23†L52-L60】.  
- **Repositórios de Modelos**: Hugging Face (pesquisar por “Llama 3.1 8B”, “Mistral 7B”, etc.) e *TheBloke/LLMCPP* oferecem versões GGUF quantizadas. Exemplos: [TheBloke/Llama-3-8B-HF-GPTQ](https://huggingface.co/TheBloke/Llama-3-8B-HF-GPTQ) (GPTQ 4-bit), [mistralai/Mistral-7B-Instruct-v0.1](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1).  
- **Ferramentas de Quantização**:  
  - *BitsAndBytes* (Hugging Face) para quantização 8/4 bits (documentação: [bitsandbytes GitHub](https://github.com/huggingface/bitsandbytes)).  
  - *GPTQ* e *AutoGPTQ* (convertendo LLM a 4-bit) – código fonte em [AutoGPTQ GitHub](https://github.com/PanQiWei/AutoGPTQ).  
  - *AWQ* (Activation-aware Weight Quantization) – pacote pip `awq` (veja [Veni AI](https://veniplatform.com/pt/blog/llm-quantization-model-optimizasyonu-int8-int4) para exemplo em português)【35†L176-L185】.  
  - *llama.cpp* (inclui conversão GGUF e quantização offline): [GitHub llama.cpp](https://github.com/ggerganov/llama.cpp).  
  - *PEFT/LoRA*: biblioteca Hugging Face PEFT (texto e código: [HuggingFace PEFT](https://huggingface.co/docs/peft)), e tutoriais sobre QLoRA【27†L44-L48】.  
- **Artigos e Tutoriais** (preferência pt-BR):  
  - Apidog: “10 Melhores LLMs locais…” (pt-BR) detalha muitos modelos quantizados【1†L159-L166】【25†L211-L218】.  
  - Veni AI (pt-BR): “Quantização de LLM e Otimização de Modelos” aborda INT8/INT4, GPTQ, AWQ【33†L78-L82】【35†L176-L185】.  
  - DataCamp (pt-BR): “Introdução aos valores SHAP…” explica interpretação de features【12†L180-L184】.  
  - Microsoft Learn (pt-BR): “Análises contrafactuais e teste de hipóteses” define explicações contrafactuais【7†L68-L70】.  
- **Frameworks e SDKs**: O LMStudio fornece SDKs (JavaScript, Python). Exemplo de instalação CLI:  
  ```bash
  curl -fsSL https://lmstudio.ai/install.sh | bash   # instala llmster (Linux/Mac)【36†L189-L197】
  lms daemon up; lms get <modelo>; lms server start  # comandos básicos【36†L203-L208】
  ```  
- **Quantização e Integração**: Scripts de conversão de modelos podem ser baseados nos exemplos de `veniplatform.com`【35†L231-L239】 (GGUF Q4_K_M) e snippets de BitsAndBytes (8-bit/4-bit) mostrados em [35†L250-L258].

Estas referências orientam a configuração do ambiente local, seleção de modelos e técnicas de compressão. Em resumo, a solução usa LLMs quantizados leves, integração pelo LMStudio, pipeline estruturado de explicações e monitoramento rigoroso para garantir explicações claras, fiáveis e ajustadas ao usuário.

