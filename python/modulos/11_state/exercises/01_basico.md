# Ejercicio 01 — State básico acumulable

## Problema
Crea un `TypedDict` llamado `TicketState` con estos campos:

- `messages: Annotated[list[str], operator.add]`
- `status: str`
- `priority: str`

Implementa dos funciones:

1. `receive_ticket(state)` debe agregar un mensaje inicial del usuario.
2. `classify_ticket(state)` debe definir la prioridad como `high` si aparece la palabra `urgente`.

## Requisitos
- Debe existir una función `merge_state` que combine listas usando `Annotated`.
- El script debe imprimir el state final.
- No se permite mutar listas globales.

## Criterios de aceptación
- Se conservan ambos mensajes.
- `status` termina en `classified`.
- `priority` refleja el contenido del ticket.

## Referencia
Ver `../solutions/01_basico.py`.
