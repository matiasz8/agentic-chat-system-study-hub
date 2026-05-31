"""
Pytest configuration y fixtures para testing en todo el hub.
Usado por FASE 3: Validation & Testing
"""

import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture
def mock_anthropic_api():
    """Mock para Anthropic API (no gastar dinero en tests)"""
    with patch('anthropic.Anthropic') as mock:
        mock_response = Mock()
        mock_response.messages.create.return_value = Mock(
            content=[Mock(text="Mock response from Claude")]
        )
        yield mock


@pytest.fixture
def env_setup(tmp_path):
    """Setup de variables de entorno para tests"""
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    os.environ['MOCK_LLM'] = 'true'
    yield
    # Cleanup
    if 'MOCK_LLM' in os.environ:
        del os.environ['MOCK_LLM']


@pytest.fixture
def sample_prompt():
    """Prompt de ejemplo para testing"""
    return {
        "system": "Eres un agente farmacéutico útil.",
        "user": "¿Cuál es el stock del medicamento X?",
        "expected_format": "json"  # Esperamos respuesta JSON
    }


@pytest.fixture
def sample_state():
    """Estado de ejemplo para testing de LangGraph"""
    return {
        "messages": [],
        "context": {},
        "user_id": "test-user-123",
        "step": 0
    }


# Configuración de pytest
def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Agregar markers personalizados
    config.addinivalue_line(
        "markers", "unit: marca test como test unitario (rápido)"
    )
    config.addinivalue_line(
        "markers", "integration: marca test como integración (más lento)"
    )
    config.addinivalue_line(
        "markers", "llm: marca test que usa LLM real (requiere API key)"
    )
