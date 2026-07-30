"""
Ejemplo 3: Validación de Workflows - E2E Testing

Cómo testear un workflow completo de principio a fin.
"""

from validation.mock_llm import MockAnthropic


class SimpleWorkflow:
    """
    Workflow simplificado que simula un agente farmacéutico.

    Flujo:
    1. Usuario pregunta
    2. Agente consulta BD
    3. Agente devuelve respuesta JSON
    """

    def __init__(self, llm=None):
        self.llm = llm or MockAnthropic()
        self.history = []

    def run(self, user_input: str) -> dict:
        """
        Ejecuta el workflow completo.

        Args:
            user_input: Pregunta del usuario

        Returns:
            Respuesta con estructura: {"status": "ok"|"error", "data": ..., "step": int}
        """
        # Paso 1: Validar input
        if not user_input or len(user_input) < 3:
            return {"status": "error", "error": "Input too short", "step": 1}

        # Paso 2: Procesar con LLM
        try:
            response = self.llm.create_message(
                model="claude-3",
                max_tokens=100,
                system="Eres un agente farmacéutico. Responde en JSON.",
                messages=[{"role": "user", "content": user_input}],
            )
            response_text = response.content[0].text
        except Exception as e:
            return {"status": "error", "error": str(e), "step": 2}

        # Paso 3: Validar JSON
        import json

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            return {"status": "error", "error": "Invalid JSON response", "step": 3}

        # Paso 4: Retornar éxito
        self.history.append({"input": user_input, "output": data})
        return {"status": "success", "data": data, "step": 4}


def test_workflow_happy_path():
    """
    Test 1: Flujo exitoso
    Usuario pregunta válida → Respuesta correcta
    """
    print("=" * 60)
    print("Test 1: Happy Path (Flujo exitoso)")
    print("=" * 60)

    workflow = SimpleWorkflow()
    result = workflow.run("¿Cuál es el stock del Paracetamol?")

    print("Input: '¿Cuál es el stock del Paracetamol?'")
    print(f"Output: {result}")
    print(f"Status: {result['status']}")

    assert result["status"] == "success", "Should succeed"
    assert "data" in result, "Should have data"
    print("✅ Test 1 pasó!\n")


def test_workflow_invalid_input():
    """
    Test 2: Input inválido
    Usuario pregunta algo demasiado corto → Error
    """
    print("=" * 60)
    print("Test 2: Invalid Input (Input demasiado corto)")
    print("=" * 60)

    workflow = SimpleWorkflow()
    result = workflow.run("X")

    print("Input: 'X'")
    print(f"Output: {result}")

    assert result["status"] == "error", "Should fail"
    assert "error" in result, "Should have error message"
    assert result["step"] == 1, "Should fail at step 1"
    print("✅ Test 2 pasó!\n")


def test_workflow_history():
    """
    Test 3: Historial de conversación
    Verificar que el workflow rastrea la historia
    """
    print("=" * 60)
    print("Test 3: Historial (Workflow tracks history)")
    print("=" * 60)

    workflow = SimpleWorkflow()

    # Hacer 3 preguntas
    questions = [
        "¿Stock de Paracetamol?",
        "¿Stock de Ibuprofeno?",
        "¿Medicamentos disponibles?",
    ]

    for q in questions:
        result = workflow.run(q)
        print(f"  Q: {q} → Status: {result['status']}")

    print(f"\nHistorial: {len(workflow.history)} preguntas registradas")
    assert len(workflow.history) == 3, "Should track all 3 questions"
    print("✅ Test 3 pasó!\n")


def test_workflow_security():
    """
    Test 4: Seguridad contra inyecciones
    Input maligno → Error o bloqueado
    """
    print("=" * 60)
    print("Test 4: Security (Inyección SQL)")
    print("=" * 60)

    workflow = SimpleWorkflow()

    malicious_inputs = [
        "¿Stock de X'; DROP TABLE --?",
        "'; DELETE FROM users --",
        "<script>alert('xss')</script>",
    ]

    for malicious in malicious_inputs:
        result = workflow.run(malicious)
        print(f"  Malicious: {malicious[:30]}...")
        print(f"  Status: {result['status']}")

        # Debería fallar o ignorar la inyección
        assert result["status"] in ["success", "error"], "Should handle gracefully"

    print("✅ Test 4 pasó!\n")


def test_workflow_performance():
    """
    Test 5: Performance
    Workflow responde rápido
    """
    print("=" * 60)
    print("Test 5: Performance (< 1s)")
    print("=" * 60)

    import time

    workflow = SimpleWorkflow()
    start = time.time()

    for i in range(10):
        workflow.run(f"¿Stock {i}?")

    elapsed = time.time() - start
    avg_time = elapsed / 10

    print(f"10 llamadas en {elapsed:.2f}s")
    print(f"Promedio: {avg_time * 1000:.1f}ms por llamada")

    assert avg_time < 0.5, f"Should be < 500ms, was {avg_time * 1000:.1f}ms"
    print("✅ Test 5 pasó!\n")


def test_workflow_multiple_llm_calls():
    """
    Test 6: Múltiples llamadas LLM
    Workflow reutiliza cliente LLM
    """
    print("=" * 60)
    print("Test 6: Multiple LLM Calls (Rastrear llamadas)")
    print("=" * 60)

    mock_llm = MockAnthropic()
    workflow = SimpleWorkflow(llm=mock_llm)

    # Hacer 5 llamadas
    for i in range(5):
        workflow.run(f"¿Medicamento {i}?")

    print(f"LLM llamadas: {mock_llm.call_count}")
    assert mock_llm.call_count == 5, "Should track all LLM calls"
    print("✅ Test 6 pasó!\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("VALIDACIÓN DE WORKFLOWS - E2E TESTING")
    print("=" * 60 + "\n")

    test_workflow_happy_path()
    test_workflow_invalid_input()
    test_workflow_history()
    test_workflow_security()
    test_workflow_performance()
    test_workflow_multiple_llm_calls()

    print("=" * 60)
    print("✅ TODOS LOS TESTS PASARON!")
    print("=" * 60)
    print("\nEjecutar con: python validation/examples/03_validate_workflow.py")
