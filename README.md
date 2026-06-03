# 📚 Agentic Chat System Study Hub

> Guía de estudio interactiva: Arquitectura de sistemas agentic para Ask Sage

## 🎯 ¿Qué es esto?

Una **referencia técnica educativa** de 67 páginas con documentación completa sobre cómo construir un chatbot agentic como Ask Sage, siguiendo la arquitectura recomendada de **4 capas**:

1. **Frontend**: Vercel AI SDK + Next.js (streaming, generative UI)
2. **Orchestration**: LangGraph (state, nodos, decisiones, checkpoints)
3. **Runtime**: AWS AgentCore (serverless, identity forwarding, governance con Cedar)
4. **Data**: MCP + Embeddings (conexión a datos, procesamiento multimodal)

Plus: **Testing & Validation** (prompts, workflows, E2E, CI/CD)

---

## ✅ ¿Qué funciona?

- ✅ **67 páginas de documentación** - Completamente funcionales
- ✅ **4 rutas de aprendizaje** - Rápida (8h), Completa (20h), Ask Sage (8h), Proyectos (12h)
- ✅ **Testing framework** - `test_prompts.py` + `test_workflows.py` incluidos
- ✅ **CI/CD pipeline** - GitHub Actions automatizado
- ✅ **Depersonalizado** - Lenguaje neutral, sin referencias personales

---

## ❌ ¿Qué NO es?

Este **NO es** un POC ejecutable. Es educación.

- ❌ No tiene chat demo funcional
- ❌ No tiene `/api/chat` implementada
- ❌ No tiene AWS AgentCore desplegado
- ❌ No tiene MCP server integrado
- ❌ No procesa PDF/video en vivo

**→ Para POC, ver [ask-sage-poc](https://github.com/matiasz8/ask-sage-poc) (repo separado)**

---

## 🚀 Quick Start (2 min)

```bash
# 1. Clonar
git clone https://github.com/matiasz8/agentic-chat-system-study-hub.git
cd agentic-chat-system-study-hub

# 2. Instalar
npm install

# 3. Ejecutar
npm run dev

# 4. Abrir
# → http://localhost:3000
```

Eso es. No hay `npm run backend`. Es Nextra (documentación estática).

---

## 📖 Rutas de Aprendizaje

### 🟢 Ruta Rápida (8 horas)
Para entender conceptos en paralelo:
- Orchestration: Fundamentos + State (3h)
- Frontend: Streaming + Gen UI (2h)
- Validation: Testing básico (1.5h)
- Proyecto simple (1.5h)

**→ [Empezar ruta rápida](/ask-sage/path)**

### 🟡 Ruta Completa (20 horas)
Todo en detalle:
- Orchestration (5h) → Runtime (3h) → Frontend (3h) → Data (3h) → Testing (2h) → Proyectos (4h)

**→ [Empezar ruta completa](/rutas/learning-paths)**

### 🔵 Ask Sage Específicamente (8 horas)
Foco en arquitectura para Ask Sage:
- Context: Qué es Ask Sage, timeline, scope
- Validación: Prompts farmacéuticos, workflows de aprobación
- Deployment: AWS AgentCore en producción

**→ [Empezar Ask Sage path](/ask-sage/path)**

---

## 📊 Cobertura de Contenido

| Capa | Tema | Páginas | Status |
|------|------|---------|--------|
| **Frontend** | Vercel AI SDK | 4 | ✅ Completo |
| | Streaming | 1 | ✅ |
| | Gen UI | 1 | ✅ |
| | Full Stack | 1 | ✅ |
| **Orchestration** | Fundamentos | 5 | ✅ Completo |
| | State Pattern | 1 | ✅ |
| | Nodos | 1 | ✅ |
| | Aristas | 1 | ✅ |
| | Checkpoints | 1 | ✅ |
| **Runtime** | Serverless | 5 | ✅ Completo |
| | Identity Forwarding | 1 | ✅ |
| | AgentCore | 1 | ✅ |
| | Cedar Policies | 1 | ✅ |
| | Tools | 1 | ✅ |
| **Data** | MCP Protocol | 2 | ✅ Completo |
| | Embeddings | 1 | ✅ |
| **Validation** | Testing | 5 | ✅ Completo |
| | Prompts | 1 | ✅ |
| | Workflows | 1 | ✅ |
| | E2E | 1 | ✅ |
| | CI/CD | 1 | ✅ |
| **Proyectos** | MVP | 3 | ✅ Completo |
| | Enterprise | 1 | ✅ |
| | AWS Deploy | 1 | ✅ |

**Total: 67 páginas ✅**

---

## 🛠️ Stack Técnico

- **Frontend**: Next.js 14 + Nextra (documentación)
- **Testing**: Python 3.9+ (pytest, mock)
- **CI/CD**: GitHub Actions
- **Linting**: ESLint, Black (Python)
- **Version Control**: Git + pre-commit hooks

---

## 📝 Casos de Uso

Este hub es perfecto para **entender arquitectura agentic** antes de:
- Evaluar plataformas de chatbot agentic
- Empezar implementación de Ask Sage
- Asignar recursos para arquitectura + desarrollo

**Tiempo recomendado**: 1 semana (ruta completa) o 2 días (ruta rápida)

---

## 🔗 Recursos Externos

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Vercel AI SDK](https://vercel.com/ai/sdk)
- [AWS Bedrock](https://aws.amazon.com/es/bedrock/)
- [Cedar Language](https://www.cedarpolicy.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🤝 Contribuciones

Este repo es **read-only de referencia**. Para Ask Sage POC real, ver [ask-sage-poc](https://github.com/matiasz8/ask-sage-poc).

---

## 📄 License

MIT

---

## 📞 Contacto

Preguntas sobre contenido educativo: [Issues](https://github.com/matiasz8/agentic-chat-system-study-hub/issues)

Preguntas sobre Ask Sage POC: Revisar ask-sage-poc repo
