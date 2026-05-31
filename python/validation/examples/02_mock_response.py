"""
Ejemplo 2: Mock LLM - Test sin gastar dinero

Cómo mockear respuestas de Claude para testing sin llamar a API real.
"""

from validation.mock_llm import MockAnthropic, get_test_response
import json


def test_with_mock_llm():
    """
    Test usando MockAnthropic.
    No gasta dinero en API calls.
    """
    print("=" * 60)
    print("Test 1: Usar MockAnthropic")
    print("=" * 60)

    # Crear instancia mock
    mock_llm = MockAnthropic(api_key="test-key")

    # Simular llamada a API
    response = mock_llm.create_message(
        model="claude-3-opus",
        max_tokens=100,
        system="Eres un agente farmacéutico. Responde siempre en JSON.",
        messages=[
            {
                "role": "user",
                "content": "¿Cuál es el stock del Paracetamol?"
            }
        ]
    )

    # Procesar respuesta
    response_text = response.content[0].text
    print(f"Response: {response_text}")

    # Validar
    data = json.loads(response_text)
    print(f"Parsed: {data}")
    assert "medication" in data
    assert "stock" in data
    print(f"✅ Test 1 pasó!\n")


def test_with_helper_function():
    """
    Test usando helper function.
    Aún más rápido para casos simples.
    """
    print("=" * 60)
    print("Test 2: Usar helper function")
    print("=" * 60)

    # Obtener respuesta mock
    response = get_test_response("¿stock del ibuprofen?")
    print(f"Response: {response}")

    # Validar
    assert "stock" in response or "150" in response
    print(f"✅ Test 2 pasó!\n")


def test_call_tracking():
    """
    Test que rastrea número de llamadas.
    Útil para verificar que el mock se llama correctamente.
    """
    print("=" * 60)
    print("Test 3: Rastrear llamadas al mock")
    print("=" * 60)

    mock_llm = MockAnthropic()
    print(f"Call count inicial: {mock_llm.call_count}")

    # Hacer 3 llamadas
    for i in range(3):
        mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            messages=[{"role": "user", "content": f"Pregunta {i}"}]
        )
        print(f"  Llamada {i+1}...")

    print(f"Call count final: {mock_llm.call_count}")
    assert mock_llm.call_count == 3
    print(f"✅ Test 3 pasó!\n")


def test_no_cost():
    """
    Test que demuestra que usando mock no gastamos dinero.
    """
    print("=" * 60)
    print("Test 4: Sin costo - Mock vs Real API")
    print("=" * 60)

    print("Método Real (costo = $$$):")
    print("  from anthropic import Anthropic")
    print("  client = Anthropic()")
    print("  # Cada llamada cuesta dinero")
    print()

    print("Método Mock (costo = gratis):")
    print("  from validation.mock_llm import MockAnthropic")
    print("  mock_client = MockAnthropic()")
    print("  # Llamadas sin costo para testing")
    print()

    # Usar mock
    mock_llm = MockAnthropic()
    for _ in range(100):  # 100 llamadas sin costo
        mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            messages=[{"role": "user", "content": "test"}]
        )

    print(f"✅ Hicimos 100 llamadas sin gastar dinero!")
    print(f"   Call count: {mock_llm.call_count}\n")


if __name__ == "__main__":
    test_with_mock_llm()
    test_with_helper_function()
    test_call_tracking()
    test_no_cost()

    print("=" * 60)
    print("✅ TODOS LOS TESTS PASARON!")
    print("=" * 60)
    print()
    print("Ejecutar con: python 02_mock_response.py")
