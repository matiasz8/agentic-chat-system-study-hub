# Ejercicio 03 — StreamingNode con callbacks

Diseña un nodo avanzado que procese un texto palabra por palabra y emita eventos a través de callbacks.

## Requisitos
- Debe existir una clase `StreamingNode`.
- Necesitas callbacks de inicio, chunk y fin.
- El resultado final debe reconstruirse a partir de los chunks emitidos.

## Criterios de aceptación
- El state final contiene `chunks`, `events` y `result`.
- Los callbacks se ejecutan en orden.

## Referencia
Ver `../solutions/03_avanzado.py`.
