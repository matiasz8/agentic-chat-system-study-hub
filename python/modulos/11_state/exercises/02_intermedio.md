# Ejercicio 02 — Reducer custom para documentos únicos

## Problema
Modela un `SearchState` que acumule:

- consultas del usuario
- documentos recuperados
- paso actual del workflow

Debes crear un reducer custom que elimine documentos duplicados por `id`.

## Requisitos
- Usa `TypedDict` y `Annotated`.
- Define al menos tres nodos: `collect_query`, `retrieve_docs`, `rerank_docs`.
- El resultado final debe contener documentos únicos y ordenados por llegada.

## Criterios de aceptación
- No aparecen IDs repetidos.
- El state final conserva todas las queries.
- `current_step` termina en `reranked`.

## Referencia
Ver `../solutions/02_intermedio.py`.
