"""
Mock LLM para testing. Simula respuestas de Claude sin gastar dinero.

FASE 3: Validation & Testing
"""

from dataclasses import dataclass


@dataclass
class MockMessage:
    """Simula un mensaje de respuesta de Anthropic"""

    text: str


@dataclass
class MockResponse:
    """Simula una respuesta de Anthropic API"""

    content: list


class MockAnthropic:
    """
    Mock de cliente Anthropic.
    Úsalo en tests para evitar llamadas a la API real.
    """

    def __init__(self, api_key: str = "mock-key"):
        self.api_key = api_key
        self.call_count = 0
        self.last_message: dict | None = None

    def create_message(
        self,
        model: str,
        max_tokens: int,
        system: str | None = None,
        messages: list | None = None,
        **kwargs,
    ) -> MockResponse:
        """
        Simula una llamada a API.

        Args:
            model: Modelo (ignorado)
            max_tokens: Max tokens (ignorado)
            system: System prompt (almacenado)
            messages: Lista de mensajes (almacenado)

        Returns:
            MockResponse con texto predefinido
        """
        self.call_count += 1
        self.last_message = {"system": system, "messages": messages}

        # Respuestas por defecto según el prompt
        if messages and len(messages) > 0:
            user_content = messages[-1].get("content", "").lower()

            if "stock" in user_content:
                return MockResponse(
                    content=[
                        MockMessage(
                            text='{"medication": "Paracetamol", "stock": 150, "status": "ok"}'
                        )
                    ]
                )

            elif "json" in user_content:
                return MockResponse(content=[MockMessage(text='{"response": "valid json"}')])

            elif "error" in user_content:
                return MockResponse(
                    content=[
                        MockMessage(text="Error: No tienes permiso para realizar esta acción.")
                    ]
                )

        # Respuesta por defecto
        return MockResponse(content=[MockMessage(text="Respuesta mock por defecto")])

    # Alias para compatibilidad con cliente real
    def messages_create(self, **kwargs) -> MockResponse:
        """Alias para create_message (compatibilidad con API real)"""
        return self.create_message(**kwargs)


def get_test_response(prompt: str) -> str:
    """
    Obtiene una respuesta mock basada en el prompt.
    Útil para tests simples sin instanciar MockAnthropic.

    Args:
        prompt: Prompto de usuario

    Returns:
        Respuesta mock como string
    """
    prompt_lower = prompt.lower()

    if "stock" in prompt_lower:
        return '{"medication": "Paracetamol", "stock": 150}'

    elif "error" in prompt_lower:
        return "Error: Permission denied"

    elif "translate" in prompt_lower:
        return "Traducción: Este es un texto de ejemplo"

    return "Respuesta mock por defecto"


# Ejemplo de uso
if __name__ == "__main__":
    # Test 1: Usar MockAnthropic
    mock_llm = MockAnthropic()
    response = mock_llm.create_message(
        model="claude-3-opus",
        max_tokens=100,
        system="Eres un asistente útil",
        messages=[{"role": "user", "content": "¿Cuál es el stock del paracetamol?"}],
    )
    print(f"Mock Response 1: {response.content[0].text}")
    print(f"Call count: {mock_llm.call_count}")

    # Test 2: Usar helper function
    response2 = get_test_response("Translate this to Spanish")
    print(f"Mock Response 2: {response2}")
