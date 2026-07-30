"""
Ejemplo 1: Testing Básico - Test Prompt JSON

Cómo validar que un prompt devuelve JSON válido.
"""

import json


def format_stock_response(medication: str, quantity: int) -> str:
    """
    Simula respuesta de LLM para query de stock.
    En producción, esto vendría de Claude.
    """
    return json.dumps(
        {
            "medication": medication,
            "stock": quantity,
            "status": "available" if quantity > 0 else "out_of_stock",
            "timestamp": "2024-01-01T00:00:00Z",
        }
    )


def validate_json_response(response: str) -> tuple[bool, dict | None, str]:
    """
    Valida que la respuesta es JSON válido.

    Returns:
        (is_valid, parsed_data, error_message)
    """
    try:
        data = json.loads(response)
        return (True, data, "")
    except json.JSONDecodeError as e:
        return (False, None, f"Invalid JSON: {e}")


def test_prompt_returns_valid_json():
    """Test: Prompt devuelve JSON válido"""
    # Simular respuesta de LLM
    response = format_stock_response("Paracetamol", 150)

    # Validar
    is_valid, data, error = validate_json_response(response)

    print(f"✅ Response: {response}")
    print(f"✅ Valid JSON: {is_valid}")
    print(f"✅ Parsed data: {data}")

    assert is_valid, f"Should return valid JSON: {error}"
    assert data["medication"] == "Paracetamol"
    assert data["stock"] == 150


def test_prompt_validates_fields():
    """Test: JSON contiene campos requeridos"""
    response = format_stock_response("Ibuprofeno", 200)
    is_valid, data, _ = validate_json_response(response)

    required_fields = ["medication", "stock", "status", "timestamp"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    print("✅ All required fields present")


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo 1: Testing Básico - Test Prompt JSON")
    print("=" * 60)
    print()

    test_prompt_returns_valid_json()
    print()
    test_prompt_validates_fields()

    print()
    print("✅ Todos los tests pasaron!")
    print()
    print("Ejecutar con: python 01_test_basico.py")
