# El State (Estado Centralizado) en LangGraph

## 📚 Descripción

El **State** es el corazón de cualquier grafo en LangGraph. Actúa como memoria compartida entre todos los nodos, permitiendo que el flujo del agente sea coordinado, persistente y rastreable.

En términos simples: El State es un diccionario que viaja entre nodos, donde cada nodo puede leer su contenido y actualizarlo.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender qué es el State y por qué es crítico
- ✅ Definir un StateSchema personalizado con tipos
- ✅ Implementar reducers para actualizar el State
- ✅ Manejar estado inmutable vs mutable
- ✅ Crear patrones de State avanzados para agentes complejos

## 📋 Estructura del Módulo

```
11_state/
├── README.md                    ← Estás aquí
├── examples/
│   ├── 01_basico.py            ← State simple y estático
│   ├── 02_intermedio.py        ← State con tipos y reducers
│   └── 03_avanzado.py          ← State con callbacks y logging
├── exercises/
│   ├── 01_basico.md            ← Ejercicio: definir StateSchema
│   ├── 02_intermedio.md        ← Ejercicio: implementar reducers
│   └── 03_avanzado.md          ← Ejercicio: state con persistencia
└── solutions/
    ├── 01_basico.py
    ├── 02_intermedio.py
    └── 03_avanzado.py
```

## 🔄 ¿Qué es el State?

### Concepto Visual

```
┌─────────────────────────────────────────────┐
│           STATE (Memoria Compartida)        │
├─────────────────────────────────────────────┤
│ {                                           │
│   "messages": [...],                        │
│   "current_step": "validation",             │
│   "context": {"user_id": 123, ...},        │
│   "results": [...],                         │
│   "errors": []                              │
│ }                                           │
└──────────┬────────────────────┬─────────────┘
           │                    │
        ┌──▼──┐            ┌────▼──┐
        │Node1│            │Node2  │
        │(lee)│            │(lee)  │
        └─────┘            └───────┘
           │ (actualiza)      │ (actualiza)
           └──────────┬───────┘
                      │
              ┌───────▼────────┐
              │  State Updated  │
              │  (persistencia) │
              └─────────────────┘
```

### 3 Principios Clave

1. **Centralizado**: Un único punto de verdad
2. **Inmutable**: Cada actualización crea nuevo estado
3. **Tipado**: Define explícitamente qué datos contiene

---

## 💻 Contenido Educativo

### 1️⃣ State Básico: Dict Simple

El form más simple es un diccionario Python normal:

```python
from langgraph.graph import StateGraph

# ❌ Así NO (sin tipos, error-prone)
graph = StateGraph(dict)

# ✅ Así SÍ (con TypedDict)
from typing import TypedDict, Literal

class SimpleState(TypedDict):
    """State mínimo para un agente"""
    messages: list[str]      # Historial de mensajes
    current_step: str        # Paso actual (validation, processing, etc)
```

**Cuándo usar**: Prototipos rápidos, demos, desarrollo local

---

### 2️⃣ State Intermedio: Con Reducer

Cuando el estado es complejo, usa **reducers** para controlar cómo se actualiza:

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    """State con múltiples campos y reducers"""
    messages: Annotated[list, add]           # Acumula mensajes
    current_step: str                        # Reemplaza valor
    context: dict                            # Reemplaza diccionario
    results: Annotated[list, add]            # Acumula resultados
    conversation_id: str                     # Identificador

# El reducer 'add' = concatena/acumula
# Sin reducer = reemplaza valor
```

**Ventaja**: Control granular de cómo se actualizan los datos

**Cuándo usar**: Agentes con múltiples nodos, conversaciones, históricos

---

### 3️⃣ State Avanzado: Custom Reducers

Para lógica compleja, define reducers personalizados:

```python
def merge_context(existing: dict, update: dict) -> dict:
    """Merge de contextos (combina sin perder datos)"""
    merged = existing.copy()
    merged.update(update)
    return merged

def filter_sensitive_logs(logs: list, new_logs: list) -> list:
    """Acumula logs pero sin datos sensibles"""
    return logs + [
        log for log in new_logs 
        if "password" not in str(log).lower()
    ]

class AdvancedState(TypedDict):
    messages: Annotated[list, add]
    context: Annotated[dict, merge_context]
    logs: Annotated[list, filter_sensitive_logs]
    step_history: Annotated[list, add]
```

**Cuándo usar**: Producción, agentes con requisitos de seguridad/compliance

---

## 🏗️ Alternativas en la Industria

| Herramienta | Enfoque | Casos de Uso |
|-----------|---------|-------------|
| **LangGraph** (recomendado) | Graph + State explícito | Agentes complejos, control total |
| **LangChain** | Chain de componentes | Pipelines simples, RAG básico |
| **Prefect** | Task + State implícito | Workflows de datos, ETL |
| **Airflow** | DAG + metadata | Orquestación de datos a escala |
| **Custom** | Manual con DB | Requisitos muy específicos |

---

## 🚀 Quick Start: Tus Primeros Pasos

### Paso 1: Instala LangGraph
```bash
pip install langgraph langchain
```

### Paso 2: Define tu State
```python
from typing import TypedDict, Annotated
from operator import add

class MyState(TypedDict):
    user_input: str
    messages: Annotated[list, add]
    result: str
```

### Paso 3: Crea un nodo simple
```python
def process_input(state: MyState):
    return {"messages": [f"Processing: {state['user_input']}"]}
```

### Paso 4: Construye el grafo
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(MyState)
graph.add_node("process", process_input)
graph.add_edge(START, "process")
graph.add_edge("process", END)

compiled = graph.compile()
result = compiled.invoke({"user_input": "Hola", "messages": []})
print(result)
```

---

## 📖 Ejemplos Prácticos

### Ejemplo 1: Chatbot con Histórico
```python
class ChatState(TypedDict):
    user_message: str
    messages: Annotated[list, add]      # Acumula todo el chat
    mode: Literal["chat", "search"]      # Modo actual

# messages acumula automáticamente cada interacción
```

### Ejemplo 2: Workflow de Validación
```python
class ValidationState(TypedDict):
    input_data: dict
    validation_errors: Annotated[list, add]  # Errores acumulados
    step: str  # "receive" → "validate" → "process" → "done"
    
# Si hay 3 errores en paso 1 y 2 en paso 2:
# validation_errors = [error1, error2, error3, error4, error5]
```

---

## 🏋️ Ejercicios

### ✏️ Ejercicio 1: StateSchema Básico
**Objetivo**: Define un State para un agente Q&A

```python
# Tu respuesta aquí:
class QAState(TypedDict):
    # TODO: Define los campos necesarios
    pass

# Debería tener:
# - Campo para almacenar la pregunta
# - Campo para el histórico de Q&A
# - Campo para el score de confianza
# - Campo para el paso actual
```

**Solución esperada**: Ver `solutions/01_basico.py`

### ✏️ Ejercicio 2: Implementa un Reducer Custom
**Objetivo**: Crea un reducer que acumule solo errores únicos

```python
def deduplicate_errors(existing: list, new_errors: list) -> list:
    # TODO: Implementa
    pass

# Debería:
# - Combinar listas
# - Eliminar duplicados
# - Mantener orden
```

**Solución esperada**: Ver `solutions/02_intermedio.py`

### ✏️ Ejercicio 3: State con Callbacks
**Objetivo**: Crea un State que loguee cada cambio

```python
class LoggingState(TypedDict):
    data: dict
    # TODO: Agrega campos de logging
    
# Cuando el state se actualice, debe:
# - Registrar timestamp
# - Registrar quién cambió qué
# - Guardar versión anterior
```

**Solución esperada**: Ver `solutions/03_avanzado.py`

---

## 📚 Recursos

| Recurso | Enlace | Tipo |
|---------|--------|------|
| LangGraph Docs | [docs.langchain.com](https://docs.langchain.com/docs/langgraph/intro) | Oficial |
| State Management | [Guide](https://docs.langchain.com/docs/langgraph/working-with-state) | Guía |
| TypedDict | [Python docs](https://docs.python.org/3/library/typing.html#typing.TypedDict) | Referencia |

---

## 🔗 Próximos Pasos

1. ✅ Completa los 3 ejercicios de este módulo
2. 📖 Lee `examples/01_basico.py` para ver un State mínimo funcional
3. 🚀 Avanza a **Módulo 12: Nodos** - Cómo crear las funciones que usan el State
4. 🔀 Luego: **Módulo 13: Aristas** - Cómo conectar nodos según el State

---

**Última actualización:** 2026-05-31  
**Dificultad:** ⭐⭐ Intermedia  
**Duración estimada:** 90 minutos  
**Prerequisitos:** Módulos 00-02 (Frontend) completados
