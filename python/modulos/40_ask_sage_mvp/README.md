# 🚀 Ask Sage MVP (Minimum Viable Product)

## 📚 Descripción

**Ask Sage** es un sistema interno de chat empresarial que conecta a los empleados con el conocimiento de la compañía. En su versión **MVP**, el foco está en validar valor: cargar documentos, dividirlos en chunks, recuperar contexto útil y responder preguntas con un flujo simple de **FastAPI + React + RAG**.

Este módulo explica cómo construir esa primera versión funcional sin distraerse con complejidades enterprise. Aprenderás ingestión documental, búsqueda, contexto, sesiones y autenticación básica usando únicamente Python estándar para modelar los patrones principales.

## 🎯 Objetivos de Aprendizaje

- [x] Entender la arquitectura mínima de Ask Sage MVP
- [x] Implementar una ingesta de documentos con metadatos
- [x] Dividir texto en chunks reutilizables para búsqueda
- [x] Construir una recuperación simple basada en keywords
- [x] Generar respuestas simuladas usando contexto recuperado
- [x] Gestionar sesiones e historial conversacional
- [x] Modelar autenticación básica por API key

## 📁 Estructura del Módulo

```
40_ask_sage_mvp/
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

## 🧠 Concepto: flujo de un Ask Sage MVP

El MVP une cuatro piezas: documentos, índice, sesiones y respuesta guiada por contexto.

```
Usuario
  |
  v
[Pregunta]
  |
  v
+------------------+
| Session Manager  |--> historial por chat
+------------------+
  |
  v
+------------------+
| RAG Pipeline     |
| buscar chunks    |
| crear prompt     |
| responder        |
+------------------+
  |
  v
+------------------+
| Mock LLM         |
+------------------+
  ^
  |
+------------------+
| Índice de chunks |
+------------------+
  ^
  |
+------------------+
| Ingesta          |
| leer -> dividir  |
+------------------+
```

## 🕰️ Historia y contexto

Muchos asistentes internos nacen como buscadores documentales pobres o FAQs rígidas. El patrón RAG cambió esa experiencia al permitir recuperar conocimiento y redactar respuestas más naturales. El MVP de Ask Sage aparece precisamente para validar adopción: ¿los empleados encuentran valor?, ¿los documentos sirven?, ¿conviene escalar a una versión enterprise?

## 🟢 Básico: documentos en memoria + Q&A simple

```python
documents = {
    "hr": "La política de vacaciones permite 15 días hábiles.",
    "it": "La VPN corporativa usa autenticación multifactor.",
}
question = "¿Cuántos días de vacaciones tengo?"
hits = [text for text in documents.values() if "vacaciones" in text.lower()]
print(hits[0] if hits else "Sin contexto")
```

## 🟡 Intermedio: ingestión con chunks

```python
def chunk_words(text: str, size: int = 8) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

print(chunk_words("Ask Sage indexa políticas internas y manuales críticos."))
```

## 🔴 Avanzado: MVP completo con sesiones y streaming

```python
for token in ["Analizando", " contexto", " recuperado", "... listo"]:
    print(token, end="", flush=True)
print()
```

## 🧪 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: chat CLI simulado con documentos en memoria.
- **`examples/02_intermedio.py`**: pipeline de ingesta, chunking, índice y respuesta contextual.
- **`examples/03_avanzado.py`**: simulación integral con auth, sesiones y streaming.

## 🏋️ Panorama de Ejercicios

- **Ejercicio 1**: construir la ingesta de documentos con metadatos.
- **Ejercicio 2**: montar una tubería RAG simple con prompt y respuesta simulada.
- **Ejercicio 3**: integrar ingesta, recuperación y sesiones en un CLI completo.

## ⚖️ Alternativas y comparaciones

| Enfoque | Ventajas | Desventajas | Cuándo usarlo |
|---|---|---|---|
| Keyword search en memoria | Muy simple y barato | Baja precisión semántica | MVPs y demos |
| Full-text search | Mejor ranking textual | Requiere motor dedicado | Catálogos medianos |
| Vector search | Recall semántico alto | Más infraestructura | RAG productivo |
| Hybrid search | Buen balance léxico-semántico | Más complejidad | Sistemas enterprise |
| FAQ manual | Control total | Escala mal | Dominios muy pequeños |

## 📚 Recursos

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Python `dataclasses`: https://docs.python.org/3/library/dataclasses.html
- AWS Knowledge Bases for Bedrock: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- Martin Fowler sobre Information Retrieval: https://martinfowler.com/articles/information-retrieval.html

## 🔗 Próximos pasos

1. Ejecuta los ejemplos en orden.
2. Resuelve los ejercicios antes de abrir `solutions/`.
3. Continúa con **41_ask_sage_enterprise** para sumar aislamiento, permisos y auditoría.
4. Luego pasa a **42_deployment_aws** para pensar en operación real.
