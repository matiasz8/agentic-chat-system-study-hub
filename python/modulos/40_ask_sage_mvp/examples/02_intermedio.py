# Ask Sage MVP - Nivel Intermedio
# Ranking por relevancia con TF

class RankedRAG:
    def __init__(self):
        self.docs = [
            "La aspirina es un antiinflamatorio",
            "Paracetamol es un analgesico para fiebre",
            "Ibuprofeno reduce dolor"
        ]
    
    def score(self, query, doc):
        query_words = set(query.lower().split())
        doc_words = set(doc.lower().split())
        common = query_words & doc_words
        return len(common) / len(doc_words) if doc_words else 0
    
    def search(self, query):
        scores = [(self.score(query, d), d) for d in self.docs]
        scores.sort(reverse=True)
        return [d for _, d in scores if _ > 0]

if __name__ == "__main__":
    rag = RankedRAG()
    print(rag.search("dolor inflamacion"))
