# 🏗️ ARQUITECTURA: Las 3 Capas del Sistema

> **Cómo está diseñado internamente el Chat IA Agentic**

---

## 📊 Diagrama de Capas (La Estructura Completa)

```
                        ┌─────────────────────┐
                        │   USUARIO FINAL     │
                        │  (Celular/Web)      │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  🎨 CAPA 1: FRONTEND        │
                    │    Vercel AI SDK            │
                    │    React + Next.js          │
                    ├─────────────────────────────┤
                    │ • useChat hook              │
                    │ • Streaming tokens          │
                    │ • Generative UI (gráficos)  │
                    │ • Interactividad            │
                    │                             │
                    │ MÓDULOS: 00, 01, 02, 03     │
                    └──────────────┬──────────────┘
                                   │
                         API REST   │  POST /api/chat
                         ┌─────────▼────────┐
                         │ Headers          │
                         │ x-user-token     │
                         │ Content-Type     │
                         └──────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  🧠 CAPA 2: ORCHESTRATION   │
                    │    LangGraph                │
                    │    (Agent Logic)            │
                    ├─────────────────────────────┤
                    │ • State (Memoria)           │
                    │ • Nodes (Funciones)         │
                    │ • Edges (Decisiones)        │
                    │ • Checkpoints (Persistencia)│
                    │                             │
                    │ MÓDULOS: 10, 11, 12, 13, 14 │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  ☁️  CAPA 3: RUNTIME        │
                    │    AWS Bedrock AgentCore    │
                    │    (Infrastructure)         │
                    ├─────────────────────────────┤
                    │ • Serverless                │
                    │ • Identity Forwarding ⭐     │
                    │ • Governance (Cedar) ⭐      │
                    │ • Tool Management           │
                    │ • Memory/Persistence        │
                    │                             │
                    │ MÓDULOS: 20, 21, 22, 23, 24 │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  🔌 CAPA 4: DATOS           │
                    │    MCP + Embeddings         │
                    │    (Data Connection)        │
                    ├─────────────────────────────┤
                    │ • MCP Servers               │
                    │ • Multimodal Embeddings     │
                    │ • Vector Search             │
                    │                             │
                    │ MÓDULOS: 30, 31             │
                    └─────────────────────────────┘
```

---

## 🔄 Flujo de Datos: Un Chat Completo

```
1. USUARIO ESCRIBE
   ┌────────────────────────┐
   │ "¿Stock medicamento X?"│
   └────────────┬───────────┘
                │
2. FRONTEND (Capa 1: Vercel)
   ┌──────────────────────────────┐
   │ • useChat maneja el input    │
   │ • POST /api/chat             │
   │ • Envía token en headers     │
   └────────────┬─────────────────┘
                │
3. BACKEND RECIBE (En AWS AgentCore)
   ┌────────────────────────────────┐
   │ • Valida user-token            │
   │ • Extrae identidad del usuario │
   │ • Inyecta en contexto          │
   └────────────┬───────────────────┘
                │
4. ORCHESTRATION (Capa 2: LangGraph)
   ┌────────────────────────────────┐
   │ • Carga State anterior         │
   │ • LLM lee: "¿Qué hago?"        │
   │ • Decide: "Consultar BD"       │
   │ • Ejecuta nodo correspondiente │
   └────────────┬───────────────────┘
                │
5. TOOLING (Capa 3: AgentCore)
   ┌──────────────────────────────┐
   │ • AgentCore valida permisos  │
   │ • Cedar policies revisan     │
   │ • Permite o bloquea          │
   └────────────┬─────────────────┘
                │
6. DATOS (Capa 4: Acceso)
   ┌───────────────────────────────┐
   │ • MCP consulta BD privada     │
   │ • Con user-token del usuario  │
   │ • Retorna solo datos visibles │
   └────────────┬──────────────────┘
                │
7. RESPUESTA (Streaming)
   ┌──────────────────────────────┐
   │ • Backend: streamText()      │
   │ • Envía tokens: "El stock..."│
   │ • Frontend: actualiza render │
   │ • Usuario ve en tiempo real  │
   └──────────────────────────────┘
```

---

## 📋 Responsabilidades de Cada Capa

### 🎨 CAPA 1: Frontend (Vercel AI SDK)
**Pregunta:** "¿Qué ve el usuario?"

| Responsabilidad | Cómo |
|-----------------|-----|
| **UX** | React + Tailwind |
| **Streaming** | Server-Sent Events |
| **Generative UI** | Componentes dinámicos |
| **State** | useChat hook |
| **Contratos** | API REST /api/chat |

**Herramientas:**
- Next.js (servidor + cliente)
- Vercel AI SDK (streaming)
- Recharts (gráficos)
- TailwindCSS (estilos)

---

### 🧠 CAPA 2: Orchestration (LangGraph)
**Pregunta:** "¿Cómo el agente decide?"

| Responsabilidad | Cómo |
|-----------------|-----|
| **Lógica** | State + Nodes |
| **Decisiones** | Aristas condicionales |
| **Memoria** | Checkpoints en BD |
| **Iteración** | Ciclos hasta respuesta |
| **Testing** | Unidades independientes |

**Herramientas:**
- LangGraph (framework)
- Pydantic (tipado)
- Python asyncio

---

### ☁️ CAPA 3: Runtime (AWS AgentCore) ⭐
**Pregunta:** "¿Dónde y cómo corre?"

| Responsabilidad | Cómo |
|-----------------|-----|
| **Seguridad** | Identity Forwarding |
| **Governanza** | Cedar Policies |
| **Tools** | Control de ejecución |
| **Persistencia** | Memory service |
| **Escalabilidad** | Serverless |

**Herramientas:**
- AWS AgentCore (runtime)
- AWS Bedrock (LLM)
- DynamoDB (persistencia)
- Cedar (políticas)

---

### 🔌 CAPA 4: Datos (MCP)
**Pregunta:** "¿De dónde saca información?"

| Responsabilidad | Cómo |
|-----------------|-----|
| **Conexión** | MCP Servers |
| **Búsqueda** | Embeddings |
| **Vectores** | Modelos multimodales |
| **Privacidad** | Token del usuario |

**Herramientas:**
- MCP Protocol (estándar)
- Vector databases (Weaviate, Pinecone)
- Bedrock embeddings

---

## 🔐 Seguridad en Capas

```
┌─────────────────────────────────┐
│ Frontend (Vercel)               │
│ • Envía user-token en headers   │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│ API Gateway (AWS)               │
│ • Valida token contra Okta/AD   │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│ AgentCore Layer (AWS)           │
│ • Inyecta credenciales en env   │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│ Cedar Policy Engine             │
│ • ¿Puede ejecutar esta tool? ⭐  │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│ LangGraph Layer                 │
│ • Recibe token en context       │
└────────┬────────────────────────┘
         │
┌────────▼──────────────────────────┐
│ Database Layer                    │
│ • Valida usuario en BD privada    │
│ • Devuelve solo datos autorizados │
└───────────────────────────────────┘
```

---

## 📊 Componentes Clave por Capa

### Capa 1: Frontend

```typescript
// Componente principal del chat
<ChatComponent>
  useChat({
    api: '/api/chat',
    body: { conversation_id: ... }
  })

  // Renderiza mensajes con streaming
  {messages.map(msg => {
    if (msg.type === 'text') {
      return <TextMessage>{msg.content}</TextMessage>
    }
    if (msg.type === 'component') {
      return <DynamicComponent>{msg.content}</DynamicComponent>
    }
  })}
</ChatComponent>
```

### Capa 2: Orchestration

```python
# Definición del grafo
graph = StateGraph(AgentState)

graph.add_node("agent", agent_fn)        # LLM decide
graph.add_node("query_db", query_db_fn)  # Consulta BD
graph.add_conditional_edges("agent", router)  # Decisión

# Router: ¿Qué hacer?
def router(state):
    if "query_db" in state["decision"]:
        return "query_db"
    return "agent"

# Ejecución
output = graph.invoke(initial_state, config)
```

### Capa 3: Runtime

```python
# AWS AgentCore maneja:
# 1. user_token inyectado en contexto
user_token = os.getenv("AWS_USER_TOKEN")

# 2. Cedar valida ANTES de ejecutar
# No necesitas código: es externo

# 3. Tu código recibe credenciales limpias
with database.connect(token=user_token) as conn:
    result = conn.query(...)  # Solo datos del usuario
```

### Capa 4: Datos

```python
# MCP Server expone herramientas
@mcp_server.tool("search_database")
async def search_database(query: str) -> List[dict]:
    # Acceso con credenciales del usuario
    results = db.search(query, user=context.user_id)
    return results

# Cliente (LangGraph) usa sin reinventar
mcp_client.call_tool("search_database", query="stock")
```

---

## 🔄 Interacciones Entre Capas

### Frontend ↔ Backend

```
Frontend:  POST /api/chat
           Header: x-user-token
           Body: { messages: [...] }
             ↓
Backend:   Streaming response
           Event: { type: "text", content: "El stock..." }
           Event: { type: "component", content: <Chart /> }
             ↓
Frontend:  useChat maneja eventos
           Renderiza texto + componentes
```

### Orchestration ↔ Runtime

```
LangGraph: Intenta ejecutar tool
           LLM decide: "cancelar_orden"
             ↓
AgentCore: Cedar policy engine evalúa
           ¿Puede Javier cancelar órdenes?
           ¿De qué antigüedad?
             ↓
LangGraph: Obtiene permiso ✅
           Ejecuta función
           O error ❌ (maneja gracefully)
```

### Runtime ↔ Datos

```
AgentCore: Ejecuta tool
           user_token = token_javier
             ↓
MCP/DB:    Conecta con token
           SELECT * WHERE owner = javier
             ↓
AgentCore: Retorna datos filtra dos
           Solo lo que Javier puede ver
```

---

## 🎯 Cuándo Cada Capa Importa

| Situación | Capa Crítica |
|-----------|-------------|
| "La app se ve lenta" | Frontend (Capa 1) |
| "El agente no decide bien" | Orchestration (Capa 2) |
| "Usuario X ve datos de Y" | Runtime (Capa 3) - Identity |
| "Agente ejecuta herramientas incorrectas" | Runtime (Capa 3) - Governance |
| "No encuentra información" | Datos (Capa 4) |

---

## ✅ Checklist: ¿Tu Sistema Está Bien Diseñado?

- [ ] ¿Frontend streams tokens? (Capa 1)
- [ ] ¿LangGraph tiene State centralizado? (Capa 2)
- [ ] ¿AgentCore inyecta user_token? (Capa 3)
- [ ] ¿Cedar policies controlan tools? (Capa 3)
- [ ] ¿MCP accede con credenciales? (Capa 4)
- [ ] ¿Todo está en capas separadas?
- [ ] ¿Puedes testear cada capa por separado?
- [ ] ¿Documentación clara entre capas?

---

## 📚 Referencia Rápida

```
Pregunta                    Respuesta                  Módulo
─────────────────────────────────────────────────────────────
¿Cómo ve el usuario?        Vercel AI SDK              00-03
¿Cómo decide el agente?     LangGraph State            11-14
¿Cómo corre en AWS?         AgentCore                  20-24
¿Cómo accede a datos?       MCP                        30-31
¿Todo junto cómo?           Proyectos finales          40-42
```

---

**Versión:** 1.0
**Fecha:** Mayo 2026
**Enfoque:** 4 Capas Integradas para Chat IA Empresarial
