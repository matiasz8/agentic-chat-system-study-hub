# 🔌 Módulo 30: Model Context Protocol (MCP)

El **Model Context Protocol (MCP)** es un estándar abierto presentado por **Anthropic en noviembre de 2023** para conectar modelos de IA con herramientas, archivos, APIs y fuentes de datos usando una interfaz común. En vez de implementar una integración distinta para cada host y cada servicio, MCP define un contrato uniforme basado en **JSON-RPC 2.0** para descubrir capacidades y ejecutarlas de forma consistente.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Explicar qué problema resuelve MCP y por qué reduce el problema **N×M**.
- [ ] Identificar la arquitectura **Host → Client → Server**.
- [ ] Diferenciar las primitivas **Resources**, **Tools** y **Prompts**.
- [ ] Reconocer los transportes más usados: **stdio** y **HTTP+SSE**.
- [ ] Interpretar mensajes MCP como `initialize`, `tools/list`, `tools/call`, `resources/list` y `resources/read`.
- [ ] Diseñar servidores MCP simples en Python usando solo la librería estándar.
- [ ] Entender patrones avanzados como agregación de servidores, namespaces y health checks.

## 📁 Estructura del Módulo

```
30_mcp_protocol/
├── README.md
├── examples/
│   ├── 01_basico.py
│   ├── 02_intermedio.py
│   └── 03_avanzado.py
├── exercises/
│   ├── 01.md
│   ├── 02.md
│   └── 03.md
└── solutions/
    ├── 01.py
    ├── 02.py
    └── 03.py
```

## 🧠 Idea Central: MCP como “adaptador universal” para IA

```
┌──────────────────────────────┐
│ Host (Claude Desktop / IDE) │
└──────────────┬───────────────┘
               │
               ▼
      Cliente MCP embebido
               │
      stdio / HTTP+SSE
               │
               ▼
        Servidor MCP
      ┌──────┼───────┐
      ▼      ▼       ▼
 Resources  Tools  Prompts
```

### Problema N×M

```
Sin MCP:
Modelos M1..Mn × Herramientas T1..Tm
=> cada combinación necesita integración propia
=> N × M conectores

Con MCP:
Modelos hablan MCP y herramientas exponen MCP
=> N hosts + M servidores
=> N + M integraciones
```

## 🏗️ Arquitectura MCP

1. **Host**: aplicación principal donde vive la experiencia del usuario (Claude Desktop, un IDE, un agente embebido).
2. **Client**: componente dentro del host que habla MCP, envía requests y consume respuestas.
3. **Server**: proceso o servicio remoto que expone capacidades.

### Las 3 primitivas

- **Resources**: datos legibles, como documentos, archivos, registros o resultados cacheados.
- **Tools**: funciones invocables con parámetros, por ejemplo `search`, `create_ticket` o `get_weather`.
- **Prompts**: plantillas reutilizables para guiar la interacción entre host, modelo y herramientas.

### Transportes frecuentes

- **stdio**: ideal para integración local. Un host lanza un proceso hijo y conversa por entrada/salida estándar.
- **HTTP+SSE**: útil cuando el servidor MCP vive remoto y el cliente necesita eventos en streaming.

## 📜 Contexto e Historia

Antes de MCP, cada framework o proveedor resolvía el acceso a herramientas con APIs incompatibles entre sí. Eso complicaba portar agentes entre hosts, IDEs y backends. Con el anuncio de MCP en 2023, Anthropic propuso un estándar abierto para desacoplar el **modelo** del **sistema externo**. El ecosistema adoptó rápidamente la idea porque permite reutilizar el mismo servidor con distintos hosts y favorece la interoperabilidad entre herramientas locales y remotas.

MCP no reemplaza a REST, gRPC o bases de datos; los **organiza** detrás de una interfaz orientada a agentes. El resultado es una capa de integración más predecible para discovery, ejecución y lectura de contexto.

## 💻 Niveles de Aprendizaje

### 🟢 Básico: listar e invocar tools

```python
request = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
    "name": "calculate",
    "arguments": {"expression": "2 + 2 * 5"}
}}
response = server.handle(request)
print(response["result"]["content"][0]["text"])
```

Aprende a responder `tools/list` y `tools/call` con formato JSON-RPC válido.

### 🟡 Intermedio: resources, tools y prompts en un mismo servidor

```python
dispatcher = {
    "resources/list": server.list_resources,
    "resources/read": server.read_resource,
    "tools/call": server.call_tool,
    "prompts/get": server.get_prompt,
}
result = dispatcher[message["method"]](message["params"])
```

Aquí ves a MCP como una capa uniforme para datos, acciones y plantillas.

### 🔴 Avanzado: hub multi-servidor

```python
routed_name = "weather.search"
server_name, tool_name = routed_name.split(".", 1)
response = hub.route_tool(server_name, tool_name, {"query": "Madrid"})
```

El objetivo es resolver colisiones de nombres, monitorear salud y enrutar llamadas.

## 🔄 Mensajes JSON-RPC 2.0 más comunes

| Método | Propósito | Resultado típico |
|---|---|---|
| `initialize` | Negociar versión/protocolo y capacidades | metadata del servidor |
| `tools/list` | Descubrir herramientas | catálogo de tools |
| `tools/call` | Ejecutar una tool | `content` con texto o estructura |
| `resources/list` | Descubrir recursos disponibles | lista de URIs |
| `resources/read` | Leer un recurso puntual | contenido del recurso |

## 🧪 Ejemplos Prácticos del módulo

| Archivo | Qué enseña | Enfoque |
|---|---|---|
| `examples/01_basico.py` | Servidor MCP en memoria con `get_weather` y `calculate` | Discovery + tool call |
| `examples/02_intermedio.py` | Servidor con resources, tools y prompts | Dispatch loop simulado |
| `examples/03_avanzado.py` | Hub que agrega varios servidores | Routing, namespaces y salud |

## 📝 Ejercicios del módulo

| Ejercicio | Objetivo | Solución |
|---|---|---|
| `exercises/01.md` | Responder `initialize` y `tools/list` | `solutions/01.py` |
| `exercises/02.md` | Implementar `tools/call` con 3 tools reales | `solutions/02.py` |
| `exercises/03.md` | Crear cliente MCP que descubra e invoque tools | `solutions/03.py` |

## ⚖️ Alternativas y Comparación

| Opción | Tipo de integración | Fortalezas | Limitaciones |
|---|---|---|---|
| **MCP** | Estándar abierto orientado a agentes | Interoperabilidad, discovery, transportes definidos | Ecosistema todavía joven |
| OpenAI Function Calling | API propietaria | Muy simple dentro del stack OpenAI | No es portable entre hosts/proveedores |
| LangChain Tools | Abstracción de framework | Conveniente si ya usas LangChain | No define un protocolo universal externo |
| REST ad-hoc | Integración manual | Flexible y ampliamente conocida | Sin semántica estándar para discovery |
| gRPC interno | RPC tipado | Muy bueno entre servicios backend | Menos natural para hosts/agentes de escritorio |

## 📚 Recursos Recomendados

- Especificación oficial: https://spec.modelcontextprotocol.io/
- Sitio del protocolo: https://modelcontextprotocol.io/introduction
- Repositorio oficial: https://github.com/modelcontextprotocol
- Anuncio de Anthropic: https://www.anthropic.com/news/model-context-protocol
- JSON-RPC 2.0: https://www.jsonrpc.org/specification

## 🔗 Próximos Pasos

1. Ejecuta `examples/01_basico.py` y observa el ida y vuelta JSON-RPC.
2. Completa `exercises/01.md` antes de pasar a tools más complejas.
3. Extiende el ejemplo intermedio para agregar autenticación o logging.
4. Relaciona este módulo con RAG, agentes y conectores externos del resto del hub.
5. Cuando te sientas cómodo, implementa un servidor MCP real sobre `stdio`.
