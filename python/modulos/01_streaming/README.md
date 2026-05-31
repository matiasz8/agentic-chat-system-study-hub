# 🌊 Módulo 01: Streaming de Tokens con Vercel AI SDK y SSE

Este módulo explica cómo una respuesta de IA puede empezar a aparecer antes de estar completa. Vas a estudiar **token streaming**, el protocolo **Server-Sent Events (SSE)** y los conceptos operativos que hacen que una interfaz se sienta rápida: **time-to-first-token**, transferencia por chunks, buffers, backpressure y cancelación. Aunque el stack real suele ser React + Vercel AI SDK, aquí lo modelamos con **Python stdlib** para entender la mecánica sin magia.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [x] Explicar qué es el streaming de tokens y por qué mejora la UX
- [x] Describir cómo funciona SSE sobre HTTP chunked transfer
- [x] Implementar un stream simple usando generadores en Python
- [x] Formatear eventos compatibles con SSE (`data: ...\n\n`)
- [x] Identificar problemas de buffering, backpressure y cancelación
- [x] Diseñar un pipeline con productor, proxy y múltiples consumidores
- [x] Relacionar estos patrones con Vercel AI SDK y frontends modernos

## 📂 Estructura del Módulo

```
01_streaming/
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

**Streaming** significa enviar partes pequeñas de la respuesta apenas están listas, en lugar de esperar al texto completo. En un chat con IA, cada token o fragmento puede viajar al cliente en cuanto el modelo lo produce.

```
Usuario pregunta
      │
      ▼
┌──────────────┐
│  LLM/Agente  │  genera tokens: "Hola" → "," → " mundo"
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Servidor API │  empaqueta cada token en chunks o eventos SSE
└──────┬───────┘
       │  HTTP response abierta
       ▼
┌──────────────┐
│ Frontend/UI  │  pinta texto apenas llega
└──────────────┘

Resultado: menor espera percibida y feedback inmediato.
```

### Flujo SSE simplificado

```
event: token
id: 7
retry: 1500
data: Hola

event: token
id: 8
data: mundo

event: done
data: [DONE]
```

## 🕰️ Historia y Contexto

Antes de los LLMs conversacionales, muchas aplicaciones web devolvían respuestas completas al final del request. Eso funcionaba para CRUD clásico, pero se sentía lento en operaciones largas.

- **HTTP chunked transfer** apareció para permitir respuestas en partes sin conocer de antemano el tamaño final.
- **SSE** se estandarizó dentro del ecosistema HTML5 para empujar eventos unidireccionales del servidor al navegador usando una conexión HTTP normal.
- Con la explosión de chatbots en **2022-2024**, el streaming se volvió clave porque los modelos generativos producen texto de forma incremental.
- Herramientas como **Vercel AI SDK** popularizaron una API de alto nivel para esconder la complejidad de chunks, protocolos y sincronización.

En otras palabras: el streaming no nació por los LLMs, pero los LLMs lo convirtieron en una necesidad de producto.

## 🟢 Nivel Básico: Generador que emite tokens

La forma más simple de entender streaming es un generador de Python que entrega una palabra a la vez.

```python
import time

def stream_tokens(texto: str):
    for token in texto.split():
        time.sleep(0.1)
        yield token

for token in stream_tokens("hola mundo desde python"):
    print(token, end=" ", flush=True)
```

**Qué enseña:** el productor no devuelve todo junto; entrega unidades pequeñas que el consumidor procesa inmediatamente.

## 🟡 Nivel Intermedio: Formato SSE

Cuando queremos interoperar con el navegador o con un SDK frontend, hay que serializar cada pieza con el formato correcto.

```python
def sse_event(event_id: int, data: str, retry: int = 1500) -> str:
    return (
        f"id: {event_id}\n"
        f"event: token\n"
        f"retry: {retry}\n"
        f"data: {data}\n\n"
    )

print(sse_event(1, "hola"))
```

**Qué enseña:** SSE no es solo “mandar texto”; tiene un framing específico para reconexión, IDs y eventos.

## �� Nivel Avanzado: Backpressure y cancelación

En producción, el reto no es solo emitir tokens sino coordinar velocidades distintas entre productor y consumidores.

```python
from queue import Queue

cola = Queue(maxsize=3)  # buffer chico = presión visible

def producir(tokens):
    for token in tokens:
        cola.put(token)  # se bloquea si el consumidor va lento

def consumir():
    while True:
        token = cola.get()
        print(token)
        cola.task_done()
```

**Qué enseña:** si el frontend, proxy o red se atrasan, el sistema necesita buffers, límites y estrategias de cancelación.

## 🧪 Ejemplos Prácticos Incluidos

| Archivo | Nivel | Qué demuestra |
|---|---|---|
| `examples/01_basico.py` | Básico | Generador con delay y salida inmediata por stdout |
| `examples/02_intermedio.py` | Intermedio | Simulación de servidor SSE con `queue` + `threading` |
| `examples/03_avanzado.py` | Avanzado | Pipeline completo con backpressure, fan-out y cancelación |

## 📝 Ejercicios del Módulo

| Archivo | Desafío | Resultado esperado |
|---|---|---|
| `exercises/01.md` | Construir un stream token por token | Comprender `yield`, delays y flush inmediato |
| `exercises/02.md` | Formatear eventos SSE con `id` y `retry` | Generar salida interoperable con EventSource |
| `exercises/03.md` | Diseñar un proxy de streaming multi-consumidor | Manejar cancelación y presión entre etapas |

## 🔀 Alternativas y Comparación

| Opción | Dirección | Ventaja principal | Desventaja principal | Cuándo usarla |
|---|---|---|---|---|
| **SSE** | Servidor → cliente | Simple, HTTP nativo, ideal para texto incremental | Unidireccional | Chats, progreso, notificaciones ligeras |
| **WebSocket** | Bidireccional | Canal full-duplex y menor overhead por mensaje | Más complejidad operacional | Juegos, colaboración en tiempo real, apps muy interactivas |
| **Long polling** | Cliente ↔ servidor | Compatible con infra vieja | Más requests y mayor latencia | Sistemas heredados |
| **Polling periódico** | Cliente ↔ servidor | Fácil de implementar | Mala UX y consumo innecesario | Estados que cambian poco |
| **Respuesta completa** | Servidor → cliente | Implementación trivial | Peor time-to-first-token | Operaciones muy cortas o batch |

## 📚 Recursos

- Python docs: `time`, `queue`, `threading`, `itertools`
- MDN: **Server-Sent Events** y `EventSource`
- WHATWG HTML Living Standard: especificación de SSE
- Vercel AI SDK docs: streaming UI y text streams
- Artículos sobre **time-to-first-byte** y **time-to-first-token** en UX conversacional

## 🚀 Próximos Pasos

1. Ejecuta `examples/01_basico.py` y observa la diferencia entre imprimir con y sin `flush=True`.
2. Ejecuta `examples/02_intermedio.py` para ver cómo luce un stream SSE real.
3. Estudia `examples/03_avanzado.py` y sigue el viaje del token por todo el pipeline.
4. Resuelve los tres ejercicios antes de pasar al módulo `03_frontend_completo`.
5. Cuando domines la mecánica, relaciona cada pieza con `useChat`, `streamText` o `toDataStreamResponse` en tu stack real.

---

**Última actualización:** 2026-05-31  
**Dificultad:** ⭐⭐ Intermedia  
**Duración estimada:** 90 minutos
