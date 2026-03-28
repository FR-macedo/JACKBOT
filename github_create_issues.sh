#!/usr/bin/env bash
# =============================================================================
# JackBot — Criação de Issues em 3 repositórios, cada um com seu próprio Project
# =============================================================================
# ESTRUTURA ESPERADA:
#   sua-org/Melchior  → Project #X  (Dupla 1 — Motor Preditivo)
#   sua-org/Gaspar    → Project #Y  (Dupla 2 — LLM e Chat)
#   sua-org/Baltasar  → Project #Z  (Dupla 3 — Infra, UX e Gamificação)
#
# COMO ENCONTRAR O PROJECT_NUMBER DE CADA REPO:
#   Acesse o repositório → aba "Projects" → clique no projeto
#   O número aparece na URL: github.com/orgs/ORG/projects/N
#   (Projects de repositório também têm número próprio)
#
# PRÉ-REQUISITOS:
#   1. gh auth login
#   2. Permissão de escrita em issues e projects nos 3 repositórios
#
# USO:
#   chmod +x github_create_issues.sh
#   ./github_create_issues.sh
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m';  RED='\033[0;31m'; NC='\033[0m'

if ! command -v gh &> /dev/null; then
  echo -e "${RED}Erro: GitHub CLI não encontrado. Instale em https://cli.github.com/${NC}"; exit 1
fi
if ! gh auth status &> /dev/null; then
  echo -e "${RED}Erro: execute 'gh auth login' primeiro.${NC}"; exit 1
fi

# =============================================================================
# Coleta de configuração
# =============================================================================
echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}  JackBot — Setup de Issues (3 repos + 3 projects)${NC}"
echo -e "${CYAN}================================================${NC}\n"

read -p "Nome da organização (ex: jackbot-squad): " ORG

REPO_D1="${ORG}/Melchior"
REPO_D2="${ORG}/Gaspar"
REPO_D3="${ORG}/Baltasar"

echo ""
echo -e "${CYAN}Informe o número do Project de cada repositório:${NC}"
echo -e "${YELLOW}(Encontre em: github.com/orgs/${ORG}/projects/N)${NC}\n"
read -p "Project do Melchior  (Dupla 1 — Motor Preditivo):    #" PROJECT_D1
read -p "Project do Gaspar    (Dupla 2 — LLM e Chat):         #" PROJECT_D2
read -p "Project do Baltasar  (Dupla 3 — Infra, UX e Gamif.): #" PROJECT_D3

echo ""
echo -e "${YELLOW}Organização : ${ORG}${NC}"
echo -e "${YELLOW}Melchior  → github.com/${REPO_D1}  |  Project #${PROJECT_D1}${NC}"
echo -e "${YELLOW}Gaspar    → github.com/${REPO_D2}  |  Project #${PROJECT_D2}${NC}"
echo -e "${YELLOW}Baltasar  → github.com/${REPO_D3}  |  Project #${PROJECT_D3}${NC}"
echo ""
read -p "Confirmar? (s/N): " CONFIRM
[[ "$CONFIRM" =~ ^[Ss]$ ]] || { echo "Abortado."; exit 0; }

# =============================================================================
# Funções auxiliares
# =============================================================================

# Busca o node ID interno de um Project da organização dado seu número
get_project_id() {
  local project_number="$1"
  gh api graphql -f query="
    query {
      organization(login: \"${ORG}\") {
        projectV2(number: ${project_number}) { id }
      }
    }
  " --jq '.data.organization.projectV2.id' 2>/dev/null || echo ""
}

setup_labels() {
  local repo="$1"
  echo -e "  Criando labels em ${repo}..."
  gh label create "prioridade-alta"  --color "ee0701" --description "Prioridade Alta"               --repo "$repo" --force 2>/dev/null
  gh label create "prioridade-media" --color "fbca04" --description "Prioridade Media"               --repo "$repo" --force 2>/dev/null
  gh label create "prioridade-baixa" --color "0075ca" --description "Prioridade Baixa"               --repo "$repo" --force 2>/dev/null
  gh label create "backend"          --color "0e8a16" --description "Backend Java/Spring Boot"        --repo "$repo" --force 2>/dev/null
  gh label create "frontend"         --color "c5def5" --description "Frontend React/TypeScript"       --repo "$repo" --force 2>/dev/null
  gh label create "infra"            --color "f9d0c4" --description "Infraestrutura / Docker"         --repo "$repo" --force 2>/dev/null
  gh label create "conformidade"     --color "b60205" --description "Conformidade SPA/MF 1.207/2024"  --repo "$repo" --force 2>/dev/null
  gh label create "sprint-1"         --color "ededed" --description "Sprint 1"                        --repo "$repo" --force 2>/dev/null
  gh label create "cross-team"       --color "7057ff" --description "Depende de outra dupla"          --repo "$repo" --force 2>/dev/null
}

setup_milestones() {
  local repo="$1"
  gh api "repos/${repo}/milestones" -f title="Sprint 1 - Dia 1" -f state="open" > /dev/null 2>&1 || true
  gh api "repos/${repo}/milestones" -f title="Sprint 1 - Dia 2" -f state="open" > /dev/null 2>&1 || true
  gh api "repos/${repo}/milestones" -f title="Sprint 1 - Dia 3" -f state="open" > /dev/null 2>&1 || true
}

# Cria a issue e vincula ao Project específico do repositório
create_issue() {
  local repo="$1"
  local project_id="$2"
  local title="$3"
  local body="$4"
  local labels="$5"
  local milestone="$6"

  echo -e "  ${CYAN}→${NC} ${title}"

  ISSUE_URL=$(gh issue create \
    --repo "$repo" \
    --title "$title" \
    --body "$body" \
    --label "$labels" \
    --milestone "$milestone" 2>/dev/null)

  ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -o '[0-9]*$')
  REPO_NAME=$(echo "$repo" | cut -d'/' -f2)

  if [[ -n "$project_id" && -n "$ISSUE_NUMBER" ]]; then
    ISSUE_NODE_ID=$(gh api graphql -f query="
      query {
        repository(owner: \"${ORG}\", name: \"${REPO_NAME}\") {
          issue(number: ${ISSUE_NUMBER}) { id }
        }
      }
    " --jq '.data.repository.issue.id' 2>/dev/null || echo "")

    if [[ -n "$ISSUE_NODE_ID" ]]; then
      gh api graphql -f query="
        mutation {
          addProjectV2ItemById(input: {projectId: \"${project_id}\", contentId: \"${ISSUE_NODE_ID}\"}) {
            item { id }
          }
        }
      " > /dev/null 2>&1 \
        && echo -e "    ${GREEN}✓ Vinculada ao Project${NC}" \
        || echo -e "    ${YELLOW}⚠ Criada, mas não vinculada ao Project${NC}"
    fi
  fi
}

# =============================================================================
# Busca os IDs internos dos 3 Projects
# =============================================================================
echo -e "\n${CYAN}Buscando IDs dos Projects...${NC}"

PID_D1=$(get_project_id "$PROJECT_D1")
PID_D2=$(get_project_id "$PROJECT_D2")
PID_D3=$(get_project_id "$PROJECT_D3")

[[ -z "$PID_D1" ]] && echo -e "${YELLOW}⚠ Project #${PROJECT_D1} (Melchior) não encontrado — issues serão criadas sem vínculo.${NC}"
[[ -z "$PID_D2" ]] && echo -e "${YELLOW}⚠ Project #${PROJECT_D2} (Gaspar) não encontrado — issues serão criadas sem vínculo.${NC}"
[[ -z "$PID_D3" ]] && echo -e "${YELLOW}⚠ Project #${PROJECT_D3} (Baltasar) não encontrado — issues serão criadas sem vínculo.${NC}"

# =============================================================================
# DUPLA 1 — Melchior (Motor Preditivo)
# =============================================================================
echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  [1/3] ${REPO_D1}  →  Project #${PROJECT_D1}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
setup_labels "$REPO_D1"
setup_milestones "$REPO_D1"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.1] Setup do Microsserviço Preditivo" \
"## 📖 História de Usuário
**Como** desenvolvedor da Dupla 1,
**quero** um projeto Spring Boot completamente configurado,
**para que** toda a equipe suba o ambiente em menos de 5 minutos.

---
## ✅ Critérios de Aceite
- [ ] CA-1.1.1 \`./setup.sh\` inicializa sem erros e sem intervenção manual
- [ ] CA-1.1.2 \`docker compose up\` → \`/actuator/health\` responde \`UP\` em até 60s
- [ ] CA-1.1.3 \`/swagger-ui.html\` retorna HTTP 200 sem autenticação no perfil \`dev\`
- [ ] CA-1.1.4 \`/v3/api-docs\` retorna OpenAPI 3.0 em JSON válido
- [ ] CA-1.1.5 Rotas não públicas retornam HTTP 401/403 sem credenciais
- [ ] CA-1.1.6 Nenhum \`@Setter\` genérico nas classes de domínio
- [ ] CA-1.1.7 Todos os DTOs são Java Records ou \`@Value\` com anotações de validação

---
## 🛠️ Tarefas Técnicas
- [ ] Spring Initializr (Web, Actuator, Lombok, Security, Validation, Springdoc OpenAPI)
- [ ] Criar \`setup.sh\` / \`Makefile\` com targets: \`setup\`, \`run\`, \`test\`, \`clean\`
- [ ] Criar \`docker-compose.yml\` local com healthcheck
- [ ] Configurar \`SecurityConfig.java\`
- [ ] Estrutura de pacotes DDD
- [ ] Documentar variáveis de ambiente no README

---
**Story Points:** 5 | **Prioridade:** 🔴 Alta | **Dia:** 1" \
"backend,prioridade-alta,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.2] Contratos REST — 6 Endpoints de Predição" \
"## 📖 História de Usuário
**Como** desenvolvedor frontend,
**quero** 6 endpoints GET documentados para cada categoria de aposta,
**para que** possa desenvolver hooks de consumo sem aguardar a lógica de ML.

---
## ✅ Critérios de Aceite
- [ ] CA-1.2.1 6 endpoints retornam HTTP 200: \`/match-outcome\`, \`/team-sog\`, \`/total-goals\`, \`/btts\`, \`/corner-count\`, \`/player-performance\`
- [ ] CA-1.2.2 Cada endpoint documentado com \`@Operation\` e \`@Schema\` no Swagger
- [ ] CA-1.2.3 Response com envelope padrão: \`predictionType\`, \`confidenceScore\`, \`modelVersion\`, \`generatedAt\`
- [ ] CA-1.2.4 Parâmetros inválidos → HTTP 400 estruturado
- [ ] CA-1.2.5 Controller delega 100% para a camada de Service

---
## 🛠️ Tarefas Técnicas
- [ ] Criar \`PredictionController.java\`
- [ ] Criar \`PredictionRequestDTO\` e \`PredictionResponseDTO\` (Java Records)
- [ ] Criar enum \`PredictionType\` com os 6 tipos
- [ ] Criar \`GlobalExceptionHandler.java\` com \`@RestControllerAdvice\`

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Depende de:** US-1.1" \
"backend,prioridade-alta,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.3] Stubs e Mocking de Dados Preditivos" \
"## 📖 História de Usuário
**Como** membro da equipe,
**quero** endpoints retornando dados realistas hardcoded,
**para que** possa validar fluxos end-to-end sem o modelo de ML real.

---
## ✅ Critérios de Aceite
- [ ] CA-1.3.1 \`StubPredictionService\` implementa \`IPredictionService\` com dados hardcoded
- [ ] CA-1.3.2 Campo \`confidenceScore\` do stub \`match-outcome\` = \`0.75\` (baseline RandomForest)
- [ ] CA-1.3.3 Nenhum campo do DTO retorna \`null\`
- [ ] CA-1.3.4 \`StubPredictionService\` anotado com \`@Profile(\"dev\")\`
- [ ] CA-1.3.5 1 teste unitário JUnit 5 por tipo de aposta (mínimo 6 testes)

---
**Story Points:** 2 | **Prioridade:** 🟡 Média | **Depende de:** US-1.2" \
"backend,prioridade-media,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.4] Containerização — Dockerfile Multi-Stage" \
"## 📖 História de Usuário
**Como** membro da Dupla 3 (Baltasar),
**quero** o microsserviço preditivo empacotado como imagem Docker,
**para que** possa integrá-lo ao \`docker-compose.yml\` central.

---
## ✅ Critérios de Aceite
- [ ] CA-1.4.1 \`Dockerfile\` multi-stage: build JDK 21 Alpine → runtime JRE 21 Alpine
- [ ] CA-1.4.2 Imagem final < 300MB
- [ ] CA-1.4.3 Container expõe porta \`8080\` e responde \`/actuator/health\`
- [ ] CA-1.4.4 Sem credenciais hardcoded na imagem
- [ ] CA-1.4.5 \`docker build\` sem warnings

---
## 🔗 Ação Cross-Team
Após concluir, notificar **Baltasar** com nome e tag da imagem para integração no compose central.

---
**Story Points:** 3 | **Prioridade:** 🟡 Média | **Notifica:** Baltasar" \
"infra,prioridade-media,sprint-1,cross-team" "Sprint 1 - Dia 1"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.5] Custom Hooks de Fetch React (usePrediction)" \
"## 📖 História de Usuário
**Como** desenvolvedor frontend,
**quero** hooks React tipados para consumir cada endpoint de predição,
**para que** qualquer componente solicite dados com uma única linha de código.

---
## ✅ Critérios de Aceite
- [ ] CA-1.5.1 \`usePrediction(type)\` retorna \`{ data, isLoading, error }\`
- [ ] CA-1.5.2 Hooks especializados (\`useMatchOutcome\` etc.) são wrappers tipados
- [ ] CA-1.5.3 Tipo de \`data\` corresponde à interface TypeScript do \`PredictionResponseDTO\`
- [ ] CA-1.5.4 \`AbortController\` cancela requisições na desmontagem do componente
- [ ] CA-1.5.5 URL base lida de \`import.meta.env.VITE_API_BASE_URL\`
- [ ] CA-1.5.6 Erros de rede logados com prefixo \`[JackBot/Prediction]\`

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Depende de:** US-1.2" \
"frontend,prioridade-alta,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.6] Formatter — Probabilidades em Texto Educacional" \
"## 📖 História de Usuário
**Como** usuário sem conhecimento técnico,
**quero** ver predições em linguagem natural clara,
**para que** entenda o que o modelo indica sem interpretar números brutos.

---
## ✅ Critérios de Aceite
- [ ] CA-1.6.1 Função \`formatProbabilityToText(value, context)\` exportada de \`predictionFormatter.ts\`
- [ ] CA-1.6.2 \`value >= 0.70\` → \"Alta probabilidade de…\"
- [ ] CA-1.6.3 \`0.50 <= value < 0.70\` → \"Tendência para…\"
- [ ] CA-1.6.4 \`value < 0.50\` → \"Cenário incerto —…\"
- [ ] CA-1.6.5 Output nunca expõe floats brutos ao usuário
- [ ] CA-1.6.6 Sem importações de Chart.js, Recharts ou D3
- [ ] CA-1.6.7 18 casos de teste (3 faixas × 6 tipos de aposta)

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Depende de:** US-1.5" \
"frontend,prioridade-alta,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.7] Fallbacks e Error Boundaries (Frontend)" \
"## 📖 História de Usuário
**Como** usuário quando o backend está instável,
**quero** mensagem de fallback clara em vez de tela quebrada,
**para que** saiba que o sistema identificou o problema.

---
## ✅ Critérios de Aceite
- [ ] CA-1.7.1 Todos os hooks têm \`try/catch\` e populam o campo \`error\`
- [ ] CA-1.7.2 \`PredictionCard\` renderiza \`<PredictionError />\` quando \`error !== null\`
- [ ] CA-1.7.3 \`ErrorBoundary\` de classe envolve a árvore de predições
- [ ] CA-1.7.4 HTTP 5xx e timeouts (> 10s) tratados igualmente
- [ ] CA-1.7.5 Nenhum stack trace exibido ao usuário final
- [ ] CA-1.7.6 \`isLoading\` é \`false\` após qualquer desfecho

---
**Story Points:** 3 | **Prioridade:** 🟡 Média | **Depende de:** US-1.5" \
"frontend,prioridade-media,sprint-1" "Sprint 1 - Dia 3"

create_issue "$REPO_D1" "$PID_D1" \
"[US-1.8] Instrumentação de Rastreamento de Cliques" \
"## 📖 História de Usuário
**Como** product manager,
**quero** rastrear quais predições os usuários mais clicam,
**para que** a equipe priorize modelos de ML com base em demanda real na Sprint 2.

---
## ✅ Critérios de Aceite
- [ ] CA-1.8.1 \`onClick\` em \`PredictionCard\` dispara \`trackPredictionClick(type)\`
- [ ] CA-1.8.2 Persiste \`{ type, timestamp, sessionId }\` em \`localStorage\` (chave: \`jackbot:prediction:events\`)
- [ ] CA-1.8.3 Eventos em array — sem sobrescrever registros anteriores
- [ ] CA-1.8.4 \`getTrackingReport()\` agrega eventos por tipo e retorna contagens
- [ ] CA-1.8.5 Sem PII nos dados de tracking
- [ ] CA-1.8.6 Módulo isolado em \`src/services/tracking.ts\`

---
**Story Points:** 2 | **Prioridade:** 🟢 Baixa | **Depende de:** US-1.6" \
"frontend,prioridade-baixa,sprint-1" "Sprint 1 - Dia 3"

# =============================================================================
# DUPLA 2 — Gaspar (LLM e Interface Conversacional)
# =============================================================================
echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  [2/3] ${REPO_D2}  →  Project #${PROJECT_D2}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
setup_labels "$REPO_D2"
setup_milestones "$REPO_D2"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.1] Provisionamento do LM Studio" \
"## 📖 História de Usuário
**Como** desenvolvedor da Dupla 2,
**quero** o LM Studio configurado com servidor HTTP local ativo,
**para que** o microsserviço Java tenha endpoint confiável para inferência.

---
## ✅ Critérios de Aceite
- [ ] CA-2.1.1 LM Studio instalado com modelo >= 7B parâmetros (Q4) carregado
- [ ] CA-2.1.2 Servidor HTTP ativo na porta \`1234\`
- [ ] CA-2.1.3 \`curl POST http://localhost:1234/v1/chat/completions\` retorna HTTP 200
- [ ] CA-2.1.4 Latência baseline (TTFT) documentada no README
- [ ] CA-2.1.5 \`LLM_BASE_URL\` e \`LLM_MODEL_NAME\` no \`.env.example\`

---
## ⚠️ Atenção — Rede Docker
LM Studio roda no **host** (fora do Docker):
- **Windows/Mac:** \`host.docker.internal:1234\`
- **Linux:** IP da bridge \`docker0\` ou \`extra_hosts: host-gateway\`

---
**Story Points:** 2 | **Prioridade:** 🔴 Alta | **Dia:** 1" \
"infra,prioridade-alta,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.2] Microsserviço LLM — ChatController e API Gateway" \
"## 📖 História de Usuário
**Como** usuário do JackBot,
**quero** enviar mensagens para um endpoint centralizado,
**para que** o frontend não acesse o modelo diretamente.

---
## ✅ Critérios de Aceite
- [ ] CA-2.2.1 Spring Boot sobe e \`/actuator/health\` responde \`UP\`
- [ ] CA-2.2.2 \`POST /api/v1/chat\` aceita \`{ message, sessionId }\`
- [ ] CA-2.2.3 Response retorna \`{ reply, sessionId, tokensUsed, latencyMs }\`
- [ ] CA-2.2.4 \`message\` vazia → HTTP 400 estruturado
- [ ] CA-2.2.5 Swagger documenta o endpoint com exemplos

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Dia:** 1" \
"backend,prioridade-alta,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.3] LmStudioClient — Client HTTP Interno para o Modelo" \
"## 📖 História de Usuário
**Como** desenvolvedor do microsserviço LLM,
**quero** um client HTTP Java tipado para o LM Studio,
**para que** as chamadas sejam resilientes e substituíveis por outra API futuramente.

---
## ✅ Critérios de Aceite
- [ ] CA-2.3.1 \`LmStudioClient.java\` encapsula toda comunicação com o modelo
- [ ] CA-2.3.2 Usa \`RestClient\` (Spring 6.1+) ou \`WebClient\`
- [ ] CA-2.3.3 URL base e timeout via \`@ConfigurationProperties\`, sem hardcode
- [ ] CA-2.3.4 Payload no formato OpenAI Chat Completions
- [ ] CA-2.3.5 Lança \`LlmCommunicationException\` em timeout ou resposta não-2xx
- [ ] CA-2.3.6 Teste de integração com WireMock simulando o LM Studio

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Depende de:** US-2.1" \
"backend,prioridade-alta,sprint-1" "Sprint 1 - Dia 1"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.4] Containerização do Middleware LLM" \
"## 📖 História de Usuário
**Como** membro da Dupla 3 (Baltasar),
**quero** o microsserviço LLM como imagem Docker,
**para que** possa adicioná-lo ao compose central.

---
## ✅ Critérios de Aceite
- [ ] CA-2.4.1 \`Dockerfile\` multi-stage (JDK 21 → JRE 21 Alpine)
- [ ] CA-2.4.2 Imagem final < 300MB
- [ ] CA-2.4.3 \`LLM_BASE_URL\` injetada via variável de ambiente
- [ ] CA-2.4.4 Container responde \`/actuator/health\`
- [ ] CA-2.4.5 Configuração de rede (host LM Studio) documentada para Linux e Windows/Mac

---
## 🔗 Ação Cross-Team
Notificar **Baltasar** com nome e tag da imagem após conclusão.

---
**Story Points:** 2 | **Prioridade:** 🟡 Média | **Notifica:** Baltasar" \
"infra,prioridade-media,sprint-1,cross-team" "Sprint 1 - Dia 1"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.5] LlmOrchestrationService — Guardrails e Prompt Engineering" \
"## 📖 História de Usuário
**Como** gestor de conformidade,
**quero** que interações com o LLM passem por camada com restrições de contexto esportivo,
**para que** o modelo não seja manipulado via prompt injection.

---
## ✅ Critérios de Aceite
- [ ] CA-2.5.1 \`LlmOrchestrationService\` é o único ponto de entrada para o \`LmStudioClient\`
- [ ] CA-2.5.2 System Prompt injetado com: restrição de escopo, idioma PT-BR, formato conciso
- [ ] CA-2.5.3 5+ prompts adversariais retornam recusa padronizada sem processar o conteúdo
- [ ] CA-2.5.4 Mensagem do usuário sanitizada antes de ser concatenada
- [ ] CA-2.5.5 System Prompt carregado de \`classpath:prompts/system-prompt.txt\`
- [ ] CA-2.5.6 Controller delega 100% para o Service

---
## 🚨 Conformidade — Portaria SPA/MF 1.207/2024
System Prompt não deve conter referências a odds ou valores monetários. **Revisão obrigatória** pelo responsável de produto antes do merge.

---
**Story Points:** 5 | **Prioridade:** 🔴 Alta | **Depende de:** US-2.3" \
"backend,prioridade-alta,conformidade,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.6] Componente de Chat — ChatContainer, MessageList, ChatInput" \
"## 📖 História de Usuário
**Como** usuário do JackBot,
**quero** interface de chat para perguntas e respostas conversacionais,
**para que** obtenha análises esportivas sem navegar por menus.

---
## ✅ Critérios de Aceite
- [ ] CA-2.6.1 Árvore: \`ChatContainer → MessageList → MessageBubble\` e \`ChatContainer → ChatInput\`
- [ ] CA-2.6.2 \`MessageBubble\` distingue usuário (direita) e assistente (esquerda) visualmente
- [ ] CA-2.6.3 \`ChatInput\` desabilitado durante \`isLoading\`
- [ ] CA-2.6.4 Estado com \`useReducer\` (actions: ADD_USER_MESSAGE, ADD_ASSISTANT_MESSAGE, SET_LOADING, SET_ERROR)
- [ ] CA-2.6.5 Interface \`Message\` tipada: \`id\`, \`role\`, \`content\`, \`timestamp\`
- [ ] CA-2.6.6 Testes: renderização vazia, adição de mensagem, loading state

---
**Story Points:** 5 | **Prioridade:** 🔴 Alta | **Dia:** 2" \
"frontend,prioridade-alta,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.7] Integração Assíncrona — useChatSubmit e TypingIndicator" \
"## 📖 História de Usuário
**Como** usuário,
**quero** indicador claro de que minha pergunta está sendo processada,
**para que** saiba que o sistema está funcionando.

---
## ✅ Critérios de Aceite
- [ ] CA-2.7.1 Mensagem do usuário adicionada ao \`MessageList\` imediatamente ao submeter
- [ ] CA-2.7.2 \`<TypingIndicator />\` com animação \"A analisar…\" durante o aguardo
- [ ] CA-2.7.3 \`TypingIndicator\` removido ao receber resposta (sucesso ou erro)
- [ ] CA-2.7.4 Erro HTTP 5xx ou timeout adiciona mensagem de sistema ao chat
- [ ] CA-2.7.5 Hook \`useChatSubmit\` retorna \`{ submit, isLoading, error }\`

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Depende de:** US-2.6" \
"frontend,prioridade-alta,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.8] Scroll Automático e Foco no Campo de Chat" \
"## 📖 História de Usuário
**Como** usuário em conversa longa,
**quero** que a janela role automaticamente para a mensagem mais recente,
**para que** não precise fazer scroll manual.

---
## ✅ Critérios de Aceite
- [ ] CA-2.8.1 \`useRef\` no elemento sentinela ao final de \`MessageList\`
- [ ] CA-2.8.2 \`useEffect\` chama \`scrollIntoView({ behavior: 'smooth' })\` a cada nova mensagem
- [ ] CA-2.8.3 Carregamento inicial posiciona na última mensagem (\`behavior: 'instant'\`)
- [ ] CA-2.8.4 \`ChatInput\` recebe \`autoFocus\` após envio
- [ ] CA-2.8.5 Scroll automático pausado quando usuário rola para cima manualmente

---
**Story Points:** 2 | **Prioridade:** 🟡 Média | **Depende de:** US-2.6" \
"frontend,prioridade-media,sprint-1" "Sprint 1 - Dia 3"

create_issue "$REPO_D2" "$PID_D2" \
"[US-2.9] Logging de Latência e Observabilidade do LLM" \
"## 📖 História de Usuário
**Como** engenheiro de desempenho,
**quero** que o microsserviço registre latência de cada chamada ao modelo,
**para que** avalie viabilidade técnica antes da Sprint 2.

---
## ✅ Critérios de Aceite
- [ ] CA-2.9.1 \`@Around\` AOP intercepta chamadas ao \`LlmOrchestrationService\`
- [ ] CA-2.9.2 Log inclui: \`sessionId\`, \`latencyMs\`, \`tokensUsed\`, \`modelName\`
- [ ] CA-2.9.3 Logs estruturados em JSON (\`logstash-logback-encoder\`)
- [ ] CA-2.9.4 Latência > 5.000ms → \`WARN\`; > 15.000ms → \`ERROR\`
- [ ] CA-2.9.5 \`/actuator/llm-stats\` expõe \`totalRequests\`, \`averageLatencyMs\`, \`p95LatencyMs\`
- [ ] CA-2.9.6 Conteúdo das mensagens NÃO é registrado em log (privacidade)

---
**Story Points:** 3 | **Prioridade:** 🟢 Baixa | **Depende de:** US-2.5" \
"backend,prioridade-baixa,sprint-1" "Sprint 1 - Dia 3"

# =============================================================================
# DUPLA 3 — Baltasar (Infraestrutura, UX e Gamificação)
# =============================================================================
echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  [3/3] ${REPO_D3}  →  Project #${PROJECT_D3}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
setup_labels "$REPO_D3"
setup_milestones "$REPO_D3"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.1] Docker Compose Central — Orquestração dos 3 Serviços" \
"## 📖 História de Usuário
**Como** qualquer membro da equipe,
**quero** levantar todos os serviços com \`docker compose up\`,
**para que** tenha ambiente completo sem configurar cada serviço manualmente.

---
## ✅ Critérios de Aceite
- [ ] CA-3.1.1 \`docker-compose.yml\` define: \`predictive-service\`, \`llm-service\`, \`frontend\`
- [ ] CA-3.1.2 Rede bridge \`jackbot-network\` declarada; todos os serviços conectados
- [ ] CA-3.1.3 Serviços Java comunicam-se via DNS interno (sem IPs hardcoded)
- [ ] CA-3.1.4 Variáveis em \`.env\` (nunca commitado); \`.env.example\` no repo
- [ ] CA-3.1.5 Cada serviço tem \`healthcheck\`; \`depends_on\` com \`condition: service_healthy\`
- [ ] CA-3.1.6 Todos os serviços com status \`healthy\` em até 90s

---
## 🔗 Dependências Cross-Team
Aguardar imagens Docker de:
- **Melchior** → US-1.4 (nome/tag da imagem preditiva)
- **Gaspar** → US-2.4 (nome/tag da imagem LLM)

---
**Story Points:** 5 | **Prioridade:** 🔴 Alta | **Depende de:** Melchior/US-1.4, Gaspar/US-2.4" \
"infra,prioridade-alta,sprint-1,cross-team" "Sprint 1 - Dia 1"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.2] Políticas CORS nos Microsserviços Java" \
"## 📖 História de Usuário
**Como** desenvolvedor frontend,
**quero** que o Vite dev server (porta 5173) seja aceito pelos microsserviços,
**para que** possa desenvolver localmente sem erros de CORS.

---
## ✅ Critérios de Aceite
- [ ] CA-3.2.1 Ambos os microsserviços têm \`WebMvcConfig.java\` com CORS configurado
- [ ] CA-3.2.2 Origin \`http://localhost:5173\` permitida explicitamente (sem wildcard \`*\`)
- [ ] CA-3.2.3 Métodos permitidos: \`GET\`, \`POST\`, \`OPTIONS\`
- [ ] CA-3.2.4 Header \`Content-Type\` em \`allowedHeaders\`
- [ ] CA-3.2.5 Preflight \`OPTIONS\` retorna HTTP 200 com headers corretos
- [ ] CA-3.2.6 URL de origin em \`application.yml\`, não hardcoded

---
## 🔗 Ação Cross-Team
Esta task exige atuação direta nos repos **Melchior** e **Gaspar**.

---
**Story Points:** 2 | **Prioridade:** 🔴 Alta | **Apoia:** Melchior e Gaspar" \
"backend,prioridade-alta,sprint-1,cross-team" "Sprint 1 - Dia 1"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.3] Scaffold do Cliente Web — Vite + React + TailwindCSS" \
"## 📖 História de Usuário
**Como** desenvolvedor frontend das três duplas,
**quero** projeto React com Vite, TypeScript e Tailwind já configurado,
**para que** todos comecem sobre base consistente.

---
## ✅ Critérios de Aceite
- [ ] CA-3.3.1 Projeto via \`npm create vite@latest -- --template react-swc-ts\`
- [ ] CA-3.3.2 TailwindCSS configurado e funcional
- [ ] CA-3.3.3 Estrutura de pastas: \`components/{chat,prediction,gamification,shared}\`, \`hooks/\`, \`reducers/\`, \`services/\`, \`types/\`, \`utils/\`
- [ ] CA-3.3.4 Layout principal: CSS Grid 2 colunas em viewport >= 768px
- [ ] CA-3.3.5 \`src/styles/tokens.css\` com variáveis CSS de design tokens
- [ ] CA-3.3.6 \`npm run dev\` na porta 5173 sem warnings; \`npm run build\` sem erros TypeScript

---
## 🔗 Ação Cross-Team
Compartilhar estrutura de pastas e tokens CSS com **Melchior** e **Gaspar** antes do Dia 2.

---
**Story Points:** 3 | **Prioridade:** 🔴 Alta | **Desbloqueia:** todo o desenvolvimento React" \
"frontend,prioridade-alta,sprint-1,cross-team" "Sprint 1 - Dia 1"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.4] GamificationContext — Sistema de XP e Nível" \
"## 📖 História de Usuário
**Como** usuário recorrente,
**quero** ver meu XP e Nível acumulados ao longo das sessões,
**para que** me sinta recompensado e motivado a voltar.

---
## ✅ Critérios de Aceite
- [ ] CA-3.4.1 \`GamificationContext\` criado e exposto via \`GamificationProvider\`
- [ ] CA-3.4.2 Estado: \`xp\`, \`level\`, \`xpToNextLevel\`
- [ ] CA-3.4.3 Persistido em \`localStorage\` (chave: \`jackbot:gamification:state\`)
- [ ] CA-3.4.4 \`xpReducer\` com actions: \`EARN_XP\`, \`RESET_PROGRESS\`
- [ ] CA-3.4.5 Cálculo de nível isolado em \`src/utils/levelCalculator.ts\`
- [ ] CA-3.4.6 🚨 \`xpReducer\` NÃO processa variáveis financeiras — anotado com \`// COMPLIANCE: SPA/MF 1.207/2024\`
- [ ] CA-3.4.7 Teste específico verifica que o reducer não muta campos financeiros
- [ ] CA-3.4.8 \`useGamification()\` expõe \`{ xp, level, xpToNextLevel, earnXp }\`

---
## 🚨 Conformidade — Portaria SPA/MF 1.207/2024
XP não pode ser relacionado a valores monetários, odds ou saldo. PR que viole esta regra deve ser **rejeitado** em code review.

---
**Story Points:** 5 | **Prioridade:** 🔴 Alta | **Dia:** 2" \
"frontend,prioridade-alta,conformidade,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.5] Notificações Assíncronas com react-toastify" \
"## 📖 História de Usuário
**Como** usuário,
**quero** notificações não intrusivas sobre eventos relevantes,
**para que** seja informado sem interromper minha leitura.

---
## ✅ Critérios de Aceite
- [ ] CA-3.5.1 \`react-toastify\` instalado com \`<ToastContainer />\` no layout raiz
- [ ] CA-3.5.2 \`notificationService.ts\` com: \`notifySuccess\`, \`notifyInfo\`, \`notifyWarning\`, \`notifyError\`
- [ ] CA-3.5.3 Ganho de XP dispara \`notifySuccess\` após action \`EARN_XP\`
- [ ] CA-3.5.4 Padrão: \`autoClose: 3000\`, \`position: \"bottom-right\"\`
- [ ] CA-3.5.5 \`setInterval\` de demo controlado por feature flag (\`VITE_ENABLE_DEMO_NOTIFICATIONS\`)
- [ ] CA-3.5.6 \`setInterval\` limpo no cleanup do \`useEffect\`

---
**Story Points:** 3 | **Prioridade:** 🟡 Média | **Depende de:** US-3.4" \
"frontend,prioridade-media,sprint-1" "Sprint 1 - Dia 2"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.6] Responsividade Mobile — Layouts Fluidos com CSS Grid" \
"## 📖 História de Usuário
**Como** usuário no smartphone,
**quero** interface adaptada com painéis empilhados,
**para que** consuma análises sem zoom ou scroll horizontal.

---
## ✅ Critérios de Aceite
- [ ] CA-3.6.1 Viewport >= 768px: 2 colunas (\`grid-cols-2\`)
- [ ] CA-3.6.2 Viewport < 768px: coluna única (\`md:grid-cols-2\`) — sem JavaScript
- [ ] CA-3.6.3 Barra XP com \`transition-all duration-300 ease-in-out\`
- [ ] CA-3.6.4 Sem overflow horizontal em 320px (iPhone SE)
- [ ] CA-3.6.5 Legível em fonte base 16px no mobile
- [ ] CA-3.6.6 Validado no DevTools em: 320px, 375px, 768px, 1280px

---
**Story Points:** 3 | **Prioridade:** 🟡 Média | **Dia:** 3" \
"frontend,prioridade-media,sprint-1" "Sprint 1 - Dia 3"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.7] Auditoria de Desempenho e Memória dos Containers" \
"## 📖 História de Usuário
**Como** engenheiro de infraestrutura,
**quero** relatório documentado do consumo de cada container,
**para que** a equipe identifique gargalos antes da Sprint 2.

---
## ✅ Critérios de Aceite
- [ ] CA-3.7.1 Ambiente completo via \`docker compose up -d\` sem erros
- [ ] CA-3.7.2 Snapshot de \`docker stats\` salvo em \`docs/performance/sprint1-baseline.txt\`
- [ ] CA-3.7.3 Heap space JVM de cada container Java inspecionado e documentado
- [ ] CA-3.7.4 Consumo I/O do \`llm-service\` registrado durante 5 chamadas consecutivas
- [ ] CA-3.7.5 \`docs/performance/sprint1-analysis.md\` com tabela, gargalos e recomendações
- [ ] CA-3.7.6 Container com memória > 80% do limite gera action item formal na Sprint 2

---
**Story Points:** 3 | **Prioridade:** 🟡 Média | **Depende de:** US-3.1 funcional" \
"infra,prioridade-media,sprint-1" "Sprint 1 - Dia 3"

create_issue "$REPO_D3" "$PID_D3" \
"[US-3.8] Sanitização de Console e Correção de Race Conditions" \
"## 📖 História de Usuário
**Como** desenvolvedor da equipe,
**quero** console do browser limpo após integração de todos os componentes,
**para que** problemas reais sejam identificados sem ruído na demo.

---
## ✅ Critérios de Aceite
- [ ] CA-3.8.1 Sem warnings \`Each child in a list should have a unique key prop\`
- [ ] CA-3.8.2 Todos os itens de lista com \`key\` único e estável
- [ ] CA-3.8.3 \`useEffect\` com chamadas assíncronas têm cleanup (\`AbortController\` ou flag \`isMounted\`)
- [ ] CA-3.8.4 Sem warnings \`Can't perform state update on unmounted component\`
- [ ] CA-3.8.5 Console limpo no carregamento inicial (fluxo feliz)
- [ ] CA-3.8.6 \`docs/quality/console-review-checklist.md\` documentado para Sprints futuras

---
## 🔗 Ação Cross-Team
Pair review com **Melchior** (US-1.7) e **Gaspar** (US-2.7) para auditar os \`useEffect\` de cada dupla.

---
**Story Points:** 3 | **Prioridade:** 🟢 Baixa | **Última tarefa — depende de tudo integrado**" \
"frontend,prioridade-baixa,sprint-1,cross-team" "Sprint 1 - Dia 3"

# =============================================================================
# RESUMO FINAL
# =============================================================================
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ Concluído! 25 issues criadas em 3 repositórios.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
echo -e "  ${CYAN}Melchior  issues:${NC}  https://github.com/${REPO_D1}/issues"
echo -e "  ${CYAN}Melchior  project:${NC}  https://github.com/orgs/${ORG}/projects/${PROJECT_D1}"
echo ""
echo -e "  ${CYAN}Gaspar    issues:${NC}  https://github.com/${REPO_D2}/issues"
echo -e "  ${CYAN}Gaspar    project:${NC}  https://github.com/orgs/${ORG}/projects/${PROJECT_D2}"
echo ""
echo -e "  ${CYAN}Baltasar  issues:${NC}  https://github.com/${REPO_D3}/issues"
echo -e "  ${CYAN}Baltasar  project:${NC}  https://github.com/orgs/${ORG}/projects/${PROJECT_D3}\n"
