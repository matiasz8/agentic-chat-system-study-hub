# Ask Sage Enterprise - Nivel Basico
# FastAPI server simple

class SimpleServer:
    def __init__(self):
        self.responses = {
            "aspirina": "AINE para dolor",
            "paracetamol": "Analgesico"
        }
    
    def ask(self, question):
        for key, value in self.responses.items():
            if key in question.lower():
                return {"answer": value, "confidence": 0.9}
        return {"answer": "No encontre", "confidence": 0.0}

if __name__ == "__main__":
    server = SimpleServer()
    print(server.ask("Que es aspirina?"))
