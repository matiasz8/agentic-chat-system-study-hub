# Ejercicio 02 — ErrorHandlingNode async

Implementa un nodo async que llame una función externa simulada y capture errores.

## Requisitos
- Usa `TypedDict`, `Annotated` y `operator.add`.
- Si el payload viene vacío, suma un error al state y aumenta `retries`.
- Si todo sale bien, guarda el resultado transformado.

## Criterios de aceptación
- El script debe mostrar un caso exitoso y uno fallido.
- No debe romper la ejecución cuando ocurre un error.

## Referencia
Ver `../solutions/02_intermedio.py`.
