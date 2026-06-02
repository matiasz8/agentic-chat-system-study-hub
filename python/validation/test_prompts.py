"""
Testing Prompts - Ejemplos de cómo testear prompts y outputs de LLM

FASE 3: Validation & Testing - Módulo 01
"""

import pytest
import json
from typing import Dict, Any

# Imports para testing
from .mock_llm import MockAnthropic, get_test_response


class TestPromptValidation:
    """Tests para validación de prompts"""

    def test_prompt_returns_valid_json(self):
        """
        Test 1: Verificar que el prompt devuelve JSON válido.
        Escenario: Preguntamos por stock y esperamos JSON.
        """
        mock_llm = MockAnthropic()
        response = mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            messages=[{"role": "user", "content": "¿stock del medicamento?"}],
        )

        response_text = response.content[0].text
        try:
            data = json.loads(response_text)
            assert isinstance(data, dict), "Response should be a dict"
            assert "stock" in data, "Response should contain 'stock'"
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response_text}")

    def test_prompt_respects_format_constraint(self):
        """
        Test 2: Verificar que el output respeta constraints.
        Escenario: Prompt pide que la respuesta sea JSON.
        """
        mock_llm = MockAnthropic()
        response = mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            system="Siempre responde en formato JSON válido",
            messages=[{"role": "user", "content": "¿Qué medicamentos tenemos?"}],
        )

        response_text = response.content[0].text
        # Validar que es JSON
        assert response_text.startswith("{"), "Should start with {"
        # Validar que se puede parsear
        try:
            json.loads(response_text)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON format")

    def test_prompt_error_handling(self):
        """
        Test 3: Verificar que errores se manejan correctamente.
        Escenario: Usuario intenta acción no permitida.
        """
        mock_llm = MockAnthropic()
        response = mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            messages=[{"role": "user", "content": "error en transacción"}],
        )

        response_text = response.content[0].text
        assert "Error" in response_text or "error" in response_text.lower(), \
            "Should contain error message"

    def test_mock_llm_call_tracking(self):
        """
        Test 4: Verificar que el mock LLM rastrea llamadas.
        Útil para saber cuántas veces se llamó.
        """
        mock_llm = MockAnthropic()
        assert mock_llm.call_count == 0

        # Hacer 3 llamadas
        for i in range(3):
            mock_llm.create_message(
                model="claude-3",
                max_tokens=100,
                messages=[{"role": "user", "content": f"Pregunta {i}"}],
            )

        assert mock_llm.call_count == 3, "Should track 3 calls"

    def test_get_test_response_helper(self):
        """
        Test 5: Usar helper function para tests rápidos.
        """
        response_stock = get_test_response("¿stock?")
        assert "stock" in response_stock.lower() or "150" in response_stock

        response_error = get_test_response("error")
        assert "error" in response_error.lower() or "permission" in response_error.lower()

        response_translate = get_test_response("translate to spanish")
        assert "traducción" in response_translate.lower() or "spanish" in response_translate.lower()


class TestPromptFormats:
    """Tests para diferentes formatos de output"""

    @pytest.mark.parametrize(
        "input_text,expected_in_output",
        [
            ("stock", "stock"),
            ("paracetamol", "Paracetamol"),
            ("cantidad", "150"),
        ],
    )
    def test_parametrized_responses(self, input_text, expected_in_output):
        """
        Test parametrizado: prueba múltiples inputs con expected outputs.
        """
        response = get_test_response(input_text)
        assert expected_in_output in response or expected_in_output.lower() in response.lower(), \
            f"Expected '{expected_in_output}' in response: {response}"

    def test_response_type_is_string(self):
        """Verificar que la respuesta siempre es string"""
        response = get_test_response("cualquier cosa")
        assert isinstance(response, str), "Response should be a string"


class TestPromptInjectionSafety:
    """Tests para seguridad contra prompt injection"""

    def test_prompt_with_malicious_input(self):
        """
        Test 6: Verificar que inputs maliciosos no rompan el sistema.
        """
        mock_llm = MockAnthropic()

        # Input maligno que intenta romper el sistema
        malicious_input = "'; DROP TABLE medications; --"

        response = mock_llm.create_message(
            model="claude-3",
            max_tokens=100,
            messages=[{"role": "user", "content": malicious_input}],
        )

        # Debería devolver una respuesta válida sin errores
        assert response.content[0].text is not None
        assert len(response.content[0].text) > 0

    def test_prompt_with_special_characters(self):
        """
        Test 7: Inputs con caracteres especiales.
        """
        special_inputs = [
            "¿Cuál es el stock del paracetamol? \n\n\n",
            "{\"hack\": true}",
            "SELECT * FROM ...",
        ]

        for input_text in special_inputs:
            response = get_test_response(input_text)
            assert isinstance(response, str), f"Failed for input: {input_text}"


# Fixtures de ejemplo para tests más complejos
@pytest.fixture
def sample_medication_database():
    """Fixture: Base de datos de medicamentos de ejemplo"""
    return {
        "paracetamol": {"stock": 150, "price": 2.50},
        "ibuprofeno": {"stock": 200, "price": 3.00},
        "aspirina": {"stock": 100, "price": 1.50},
    }


def test_with_database_fixture(sample_medication_database):
    """
    Test que usa fixture de base de datos.
    """
    assert "paracetamol" in sample_medication_database
    assert sample_medication_database["paracetamol"]["stock"] == 150


if __name__ == "__main__":
    # Ejecutar tests: pytest python/validation/test_prompts.py -v
    print("Tests de prompts. Ejecuta con: pytest test_prompts.py -v")
