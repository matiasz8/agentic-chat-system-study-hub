# Ejercicio 03 — DistributedCheckpoint

Modela un checkpoint distribuido que guarde también el `owner` y el `trace_id` de la ejecución.

## Requisitos
- Usa `TypedDict`, `Annotated` y `operator.add` para `spans`.
- Debe existir un método `resume()` que retorne owner y state.
- Agrega al menos dos spans antes y después de reanudar.

## Referencia
Ver `../solutions/03_avanzado.py`.
