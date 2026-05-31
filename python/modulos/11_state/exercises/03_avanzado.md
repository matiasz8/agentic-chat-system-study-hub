# Ejercicio 03 — State con callbacks de auditoría

## Problema
Diseña un `AuditState` para un flujo de aprobación humana. Cada cambio del state debe:

- guardar quién actualizó el state
- registrar el timestamp
- conservar un snapshot del valor anterior

## Requisitos
- Usa `TypedDict`, `Annotated` y callbacks.
- Implementa una clase `StateObserver` o equivalente.
- Debe imprimirse el state final y el historial de eventos.

## Criterios de aceptación
- El observer recibe al menos un evento.
- El audit log crece en cada actualización.
- El script sigue siendo ejecutable con `python` sin dependencias externas.

## Referencia
Ver `../solutions/03_avanzado.py`.
