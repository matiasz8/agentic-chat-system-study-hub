# 🧰 Gestión de Herramientas para Agentes

## 📚 Descripción

En un sistema de agentes, una **tool** es una capacidad invocable desde el flujo del agente: buscar documentos, calcular algo, llamar una API o ejecutar una acción de negocio. La gestión de herramientas cubre todo su ciclo de vida: registro, descubrimiento, validación de entradas, ejecución segura, manejo de errores, versionado y observabilidad.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Explicar qué es una tool en ecosistemas como OpenAI function calling o LangChain.
- [ ] Implementar el patrón `Tool Registry` para registrar y descubrir herramientas.
- [ ] Describir esquemas de entrada y salida con estructuras estilo JSON Schema.
- [ ] Validar inputs antes de ejecutar una tool.
- [ ] Manejar errores, timeouts y reintentos de forma controlada.
- [ ] Entender estrategias de versionado y hot-reload en catálogos de tools.

## 📋 Estructura del Módulo

```text
24_tools_management/
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

## 🧠 Concepto Central

Una tool bien administrada no es “una función cualquiera”: es un contrato operativo entre el agente y el mundo exterior.

```text
+--------------------+
| Tool Registry      | -> descubre qué tools existen
+--------------------+
          |
          v
+--------------------+
| Schema Validation  | -> valida inputs esperados
+--------------------+
          |
          v
+--------------------+
| Executor           | -> aplica timeout / retries
+--------------------+
          |
          v
+--------------------+
| Result / Error     | -> tipado y manejo consistente
+--------------------+
          |
          v
+--------------------+
| Audit Log          | -> qué se llamó y qué pasó
+--------------------+
```

## 🕰️ Historia y Contexto

En los primeros agentes basados en prompts, las tools solían ser funciones “inyectadas” manualmente. Con el auge de **function calling**, **LangChain tools** y motores multiagente, apareció la necesidad de tratarlas como un catálogo explícito: con metadatos, contratos de entrada y reglas de ejecución.

Hoy el problema ya no es solo “cómo llamo una función”, sino “cómo evito que una tool falle silenciosamente, tarde demasiado, reciba parámetros inválidos o cambie de versión sin romper al agente”.

## 🟢 Nivel Básico: Tool Registry

Empieza registrando funciones con nombre, descripción y esquema.

```python
@registry.register(
    name="search_docs",
    description="Busca documentos internos",
    schema={"type": "object", "required": ["query"]},
)
def search_docs(query: str) -> list[str]:
    ...
```

El objetivo aquí es poder **descubrir** e **invocar** herramientas por nombre.

## 🟡 Nivel Intermedio: Validación y Tipos

Luego agregas validación de entradas y chequeo básico de salida.

```python
executor.invoke("word_count", {"text": "hola mundo"})
```

Si faltan campos o el tipo no coincide, el error debe ser claro y consistente.

## 🔴 Nivel Avanzado: Lifecycle Completo

En producción, una tool necesita más contexto operativo.

```python
result = manager.invoke(
    "summarize",
    payload={"text": "..."},
    version="2.0.0",
)
```

El manager puede decidir versión, timeout, categoría, reintentos y aislamiento lógico de la ejecución.

## 💼 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: registro simple con decorador y descubrimiento.
- **`examples/02_intermedio.py`**: validación de inputs y chequeo de outputs.
- **`examples/03_avanzado.py`**: versionado, hot-reload simulado y timeout.

## 🧪 Panorama de Ejercicios

- **Ejercicio 1**: construir un `ToolRegistry` con metadata y búsqueda.
- **Ejercicio 2**: añadir validación de esquema propia.
- **Ejercicio 3**: crear un `ToolExecutor` con timeout, retries y logging.

## 🔀 Alternativas y Comparación

| Enfoque | Fortalezas | Debilidades | Cuándo usarlo |
|---|---|---|---|
| **Registry custom en stdlib** | Muy didáctico, control total | Más trabajo manual | Aprendizaje, prototipos, runtime simple |
| **OpenAI function calling** | Contrato claro de tools para modelos | No resuelve toda la ejecución operativa | Integración directa con modelos compatibles |
| **LangChain Tools** | Ecosistema amplio y abstractions listas | Puede ocultar detalles internos | Apps agentic rápidas sobre LangChain |
| **Pydantic-based registries** | Validación fuerte y DX alta | Dependencia externa | Backends Python con tipado estricto |
| **Pluggy / plugin systems** | Excelente para extensibilidad | Más complejo de arrancar | Plataformas con marketplace o plugins |

## 📚 Recursos

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- JSON Schema: https://json-schema.org/learn/getting-started-step-by-step
- LangChain Tools: https://python.langchain.com/docs/concepts/tools/
- Python `concurrent.futures`: https://docs.python.org/3/library/concurrent.futures.html
- Python `typing.TypedDict`: https://docs.python.org/3/library/typing.html#typing.TypedDict

## ⏭️ Próximos Pasos

1. Ejecuta el registry básico y luego rompe a propósito un input en el ejemplo intermedio.
2. Piensa cómo conectar este módulo con **22_agentcore_governance**: las tools también deben estar gobernadas.
3. Relaciónalo con **23_cedar_policies** si quieres autorización fina antes de la ejecución.
4. Como práctica extra, diseña una tool con dos versiones y una política distinta para cada una.
