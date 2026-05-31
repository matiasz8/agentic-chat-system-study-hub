# Ask Sage MVP - Nivel Avanzado
# LangGraph agent con validacion

class AskSageAgent:
    def __init__(self):
        self.docs = {
            "aspirina": "AINE para dolor",
            "paracetamol": "Analgesico simple"
        }
    
    def process(self, question):
        query = question.lower()
        retrieved = [v for k, v in self.docs.items() if k in query]
        answer = " | ".join(retrieved) if retrieved else "No encontre info"
        confidence = len(retrieved) / len(self.docs)
        return {"answer": answer, "confidence": confidence}

if __name__ == "__main__":
    agent = AskSageAgent()
    result = agent.process("Que es aspirina?")
    print(result)
