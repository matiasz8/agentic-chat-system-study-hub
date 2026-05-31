# Ask Sage MVP - Nivel Basico
# Busqueda simple por palabras clave

class SimpleRAG:
    def __init__(self):
        self.docs = [
            "La aspirina es un antiinflamatorio",
            "Paracetamol es un analgesico",
            "Ibuprofeno reduce la inflamacion"
        ]
    
    def search(self, query):
        query_words = set(query.lower().split())
        results = []
        for doc in self.docs:
            if any(w in doc.lower() for w in query_words):
                results.append(doc)
        return results

if __name__ == "__main__":
    rag = SimpleRAG()
    print(rag.search("aspirina"))
