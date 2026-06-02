"""
Testing Workflows - Ejemplos de cómo testear LangGraph workflows

FASE 3: Validation & Testing - Módulo 02
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class MockState:
    """Mock State para testing de LangGraph sin dependencias reales"""

    def __init__(self):
        self.data = {}
        self.history = []

    def set(self, key: str, value):
        """Simula set de state"""
        self.data[key] = value
        self.history.append(f"SET {key}={value}")

    def get(self, key: str, default=None):
        """Simula get de state"""
        return self.data.get(key, default)

    def update(self, updates: dict):
        """Simula update de state"""
        self.data.update(updates)
        self.history.append(f"UPDATE {updates}")


class MockNode:
    """Mock Node para simular nodos de LangGraph"""

    def __init__(self, name: str, output: dict = None):
        self.name = name
        self.output = output or {}
        self.call_count = 0
        self.last_input = None

    def execute(self, state: MockState) -> dict:
        """Simula ejecución de nodo"""
        self.call_count += 1
        self.last_input = state.data.copy()
        return self.output

    def __call__(self, state: MockState) -> dict:
        """Hacer el nodo callable"""
        return self.execute(state)


class TestWorkflowExecution:
    """Tests para ejecución de workflows"""

    def test_node_executes(self):
        """
        Test 1: Verificar que un nodo se ejecuta.
        """
        node = MockNode("test_node", output={"result": "success"})
        state = MockState()

        output = node.execute(state)

        assert node.call_count == 1, "Node should execute once"
        assert output["result"] == "success"

    def test_state_mutations(self):
        """
        Test 2: Verificar que el state se muta correctamente.
        """
        state = MockState()
        state.set("user", "john")
        state.set("action", "query_db")

        assert state.get("user") == "john"
        assert state.get("action") == "query_db"

    def test_node_chain_execution(self):
        """
        Test 3: Verificar que múltiples nodos se ejecutan en cadena.
        """
        # Crear nodos
        node1 = MockNode("node1", output={"step": 1})
        node2 = MockNode("node2", output={"step": 2})
        node3 = MockNode("node3", output={"step": 3})

        state = MockState()

        # Ejecutar en secuencia
        node1.execute(state)
        state.update(node1.output)

        node2.execute(state)
        state.update(node2.output)

        node3.execute(state)
        state.update(node3.output)

        # Verificar que todos se ejecutaron
        assert node1.call_count == 1
        assert node2.call_count == 1
        assert node3.call_count == 1
        assert state.get("step") == 3

    def test_conditional_edge_logic(self):
        """
        Test 4: Verificar que aristas condicionales funcionan.
        """

        def router(state: MockState) -> str:
            """Función que decide a qué nodo ir"""
            action = state.get("action", "default")
            if action == "query":
                return "query_node"
            elif action == "update":
                return "update_node"
            else:
                return "default_node"

        state = MockState()
        state.set("action", "query")

        next_node = router(state)
        assert next_node == "query_node"

        state.set("action", "update")
        next_node = router(state)
        assert next_node == "update_node"

    def test_state_history_tracking(self):
        """
        Test 5: Verificar que se rastrea el historial del state.
        """
        state = MockState()
        state.set("step", 1)
        state.set("action", "query")
        state.update({"result": "ok"})

        assert len(state.history) == 3
        assert "SET step=1" in state.history
        assert "SET action=query" in state.history
        assert "UPDATE" in state.history[2]


class TestWorkflowErrorHandling:
    """Tests para manejo de errores en workflows"""

    def test_node_error_handling(self):
        """
        Test 6: Verificar que errores de nodo se manejan.
        """

        class ErrorNode:
            def __init__(self, error_msg):
                self.error_msg = error_msg

            def execute(self, state):
                raise ValueError(self.error_msg)

        node = ErrorNode("Simulated error")
        state = MockState()

        with pytest.raises(ValueError) as exc_info:
            node.execute(state)

        assert "Simulated error" in str(exc_info.value)

    def test_node_timeout_handling(self):
        """
        Test 7: Verificar que timeouts se manejan.
        """

        class TimeoutNode:
            def __init__(self, timeout_seconds=0):
                self.timeout = timeout_seconds

            def execute(self, state):
                if self.timeout > 0:
                    raise TimeoutError(f"Node timed out after {self.timeout}s")
                return {"status": "ok"}

        node = TimeoutNode(timeout_seconds=5)

        with pytest.raises(TimeoutError):
            node.execute(MockState())

    def test_validation_error_in_state(self):
        """
        Test 8: Verificar que errores de validación se detectan.
        """

        def validate_state(state: MockState) -> bool:
            """Valida que state tenga campos requeridos"""
            required_fields = ["user_id", "action"]
            for field in required_fields:
                if field not in state.data:
                    return False
            return True

        state = MockState()
        assert not validate_state(state), "Should fail validation"

        state.set("user_id", "123")
        state.set("action", "query")
        assert validate_state(state), "Should pass validation"


class TestWorkflowIntegration:
    """Tests de integración de workflows completos"""

    def test_simple_workflow(self):
        """
        Test 9: Workflow simple: Init → Process → Complete
        """

        class SimpleWorkflow:
            def __init__(self):
                self.state = MockState()

            def run(self, input_data: dict) -> dict:
                # Init
                self.state.set("user", input_data["user"])
                self.state.set("action", input_data["action"])

                # Process
                if self.state.get("action") == "query":
                    result = {"data": [1, 2, 3]}
                else:
                    result = {"data": []}

                # Complete
                self.state.set("result", result)
                return result

        workflow = SimpleWorkflow()
        result = workflow.run({"user": "john", "action": "query"})

        assert result["data"] == [1, 2, 3]

    @pytest.mark.parametrize(
        "action,expected",
        [
            ("query", {"data": [1, 2, 3]}),
            ("insert", {"status": "inserted"}),
            ("delete", {"status": "deleted"}),
        ],
    )
    def test_workflow_actions(self, action, expected):
        """
        Test 10: Workflow con múltiples acciones (parametrizado).
        """

        def execute_action(action: str) -> dict:
            if action == "query":
                return {"data": [1, 2, 3]}
            elif action == "insert":
                return {"status": "inserted"}
            elif action == "delete":
                return {"status": "deleted"}
            return {}

        result = execute_action(action)
        assert result == expected


class TestWorkflowMocking:
    """Tests que mockean componentes externos"""

    def test_workflow_with_mocked_database(self):
        """
        Test 11: Workflow que usa database mockeada.
        """
        from unittest.mock import MagicMock
        
        # Crear un mock directo sin patch
        mock_db = MagicMock()
        mock_db.return_value = [{"id": 1, "name": "Paracetamol"}]

        result = mock_db("SELECT * FROM medications")

        assert result[0]["name"] == "Paracetamol"
        mock_db.assert_called_once()

    def test_workflow_with_mocked_api(self):
        """
        Test 12: Workflow que llama API mockeada.
        """
        from unittest.mock import MagicMock
        
        # Crear un mock directo sin patch
        mock_api = MagicMock()
        mock_api.return_value = {"status": 200, "data": "ok"}

        result = mock_api("/api/medications")

        assert result["status"] == 200
        mock_api.assert_called_once_with("/api/medications")


@pytest.fixture
def workflow_state():
    """Fixture: Estado inicial para workflow tests"""
    state = MockState()
    state.set("user_id", "test-user")
    state.set("timestamp", "2024-01-01T00:00:00")
    return state


def test_with_workflow_fixture(workflow_state):
    """Test que usa fixture de workflow"""
    assert workflow_state.get("user_id") == "test-user"
    assert workflow_state.get("timestamp") is not None


if __name__ == "__main__":
    # Ejecutar tests: pytest python/validation/test_workflows.py -v
    print("Tests de workflows. Ejecuta con: pytest test_workflows.py -v")
