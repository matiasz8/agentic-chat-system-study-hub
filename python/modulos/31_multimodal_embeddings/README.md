# 🧠🖼️ Módulo 31: Embeddings Multimodales

Los **embeddings** son representaciones vectoriales densas que capturan significado. Cuando hablamos de **embeddings multimodales**, texto, imágenes e incluso audio comparten un mismo espacio vectorial para que un sistema pueda comparar elementos distintos con una métrica común, normalmente **cosine similarity**. Esa idea es la base de búsqueda semántica, recuperación cruzada, recomendación, deduplicación y RAG moderno.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Explicar qué es un embedding y por qué representa significado en forma numérica.
- [ ] Implementar **cosine similarity** desde cero con Python estándar.
- [ ] Construir embeddings de texto tipo bag-of-words / TF-IDF simplificado.
- [ ] Modelar un **vector store** en memoria con operaciones de alta y búsqueda.
- [ ] Entender cómo funciona la recuperación **cross-modal** (texto → imagen, imagen → texto).
- [ ] Comparar embeddings densos, embeddings dispersos y búsqueda por keywords.
- [ ] Relacionar embeddings con casos reales como semantic search, recomendación y RAG.

## 📁 Estructura del Módulo

```
31_multimodal_embeddings/
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

## 🔎 Concepto Central

```
Texto / Imagen / Audio
        │
        ▼
  Encoder multimodal
        │
        ▼
[0.12, -0.44, 0.91, ...]
        │
 cosine similarity
        │
        ▼
búsqueda, ranking y recuperación
```

En modelos como **CLIP** o **ImageBind**, una consulta textual y una imagen terminan cerca en el mismo espacio si “significan” algo parecido. Por eso puedes buscar “perro en la playa” y recuperar imágenes aunque ninguna tenga ese texto literal guardado.

## 🕰️ Historia y Contexto

La idea de mapear palabras a vectores viene de familias como **word2vec** y **GloVe**. Más adelante, los transformers permitieron embeddings contextuales. El salto multimodal se aceleró con modelos como **CLIP** (OpenAI, 2021), que alineó texto e imagen en un espacio compartido, y **ImageBind** (Meta, 2023), que extendió el enfoque a más modalidades. En paralelo surgieron bases de datos vectoriales especializadas como Pinecone, Weaviate y extensiones como pgvector.

Este módulo no implementa redes neuronales reales; usa simulaciones educativas con stdlib para que entiendas los principios: tokenización, pesos simples, similitud y ranking.

## 💻 Niveles de Aprendizaje

### 🟢 Básico: similitud entre documentos

```python
query = vectorizer.embed_text("python para agentes")
score = cosine_similarity(query, vectorizer.embed_text("python para automatizar tareas"))
print(round(score, 3))
```

Primer paso: convertir texto en vectores comparables y medir cercanía semántica aproximada.

### 🟡 Intermedio: vector store en memoria

```python
store.add_document("doc-1", "RAG usa embeddings para recuperar contexto")
results = store.search("buscar contexto semántico", top_k=2)
```

Aquí aparece la mecánica de indexación, top-k y ranking por similitud.

### 🔴 Avanzado: recuperación cross-modal

```python
retriever.add_image("img-playa", "perro corriendo en arena y mar")
hits = retriever.search_text("perro en la playa")
```

La clave es compartir un espacio vectorial para texto e imágenes representadas por metadatos.

## 📐 Cosine Similarity

La similitud coseno compara el ángulo entre dos vectores. Si apuntan en direcciones parecidas, el score se acerca a **1**; si no comparten orientación, se acerca a **0**; y si son opuestos, puede ser negativo.

```
            A
           /
          /
         /  θ
        /
       /______ B
```

Fórmula:

```
cos(A, B) = (A · B) / (||A|| * ||B||)
```

## 🧪 Ejemplos Prácticos del módulo

| Archivo | Qué enseña | Enfoque |
|---|---|---|
| `examples/01_basico.py` | Cosine similarity y embeddings de texto simples | TF-IDF-like con stdlib |
| `examples/02_intermedio.py` | Búsqueda semántica sobre un corpus chico | Vector store en memoria |
| `examples/03_avanzado.py` | Shared space texto + metadatos de imagen | Cross-modal retrieval |

## 📝 Ejercicios del módulo

| Ejercicio | Objetivo | Solución |
|---|---|---|
| `exercises/01.md` | Implementar `SimilaritySearch` con cosine similarity | `solutions/01.py` |
| `exercises/02.md` | Crear `VectorStore` con alta, búsqueda y delete | `solutions/02.py` |
| `exercises/03.md` | Construir retriever multimodal | `solutions/03.py` |

## 🧰 Vector Databases: idea general

Una base vectorial no solo guarda texto; almacena vectores y permite recuperar vecinos cercanos rápidamente. En este módulo simulamos esa idea con listas y ranking lineal. En producción, motores como **Pinecone**, **Weaviate** o **pgvector** optimizan indexación, filtrado y escalabilidad.

## ⚖️ Alternativas y Comparación

| Enfoque | Tipo | Ventajas | Limitaciones |
|---|---|---|---|
| TF-IDF / BM25 | Léxico / sparse | Simple, interpretable, barato | No captura bien sinonimia o contexto |
| Embeddings de texto | Semántico unimodal | Excelente para búsqueda semántica textual | No cruza modalidades por sí solo |
| Embeddings multimodales tipo CLIP | Semántico cross-modal | Permite texto ↔ imagen | Requiere entrenamiento/modelos especializados |
| Vector DB + embeddings | Infraestructura de retrieval | Escalable, filtros y top-k eficientes | Más complejidad operativa |
| Reglas por metadata | Heurístico | Muy controlable y barato | Difícil de mantener y poco flexible |

## 📚 Recursos Recomendados

- CLIP (OpenAI): https://openai.com/index/clip/
- ImageBind (Meta): https://imagebind.metademolab.com/
- pgvector: https://github.com/pgvector/pgvector
- Pinecone learning center: https://www.pinecone.io/learn/vector-embeddings/
- Explicación de similitud coseno: https://developers.google.com/machine-learning/clustering/dnn-clustering/supervised-similarity
- Weaviate concepts: https://weaviate.io/developers/weaviate/concepts/search/vector-search

## 🔗 Próximos Pasos

1. Corre `examples/01_basico.py` y verifica cómo cambia el ranking según la consulta.
2. Completa el `VectorStore` del ejercicio 2 para afianzar el patrón add/search/delete.
3. Extiende el ejemplo avanzado con más metadatos: color, escena, objetos, acción.
4. Conecta este tema con módulos de RAG, búsqueda semántica y agentes con memoria.
5. Si luego usas librerías reales, compara tus resultados manuales con un modelo preentrenado.
