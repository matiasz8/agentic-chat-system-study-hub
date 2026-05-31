# Ejercicio 02 — DBCheckpoint con SQLite

Crea un backend de checkpoints basado en SQLite que almacene versiones por `thread_id`.

## Requisitos
- Usa `sqlite3` y `json`.
- Implementa `save` y `load_latest`.
- Debe existir una clave primaria compuesta por `thread_id` y `version`.

## Referencia
Ver `../solutions/02_intermedio.py`.
