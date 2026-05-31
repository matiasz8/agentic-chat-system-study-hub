def search(docs, query):
    query_words = set(query.lower().split())
    return [d for d in docs if any(w in d.lower() for w in query_words)]

if __name__ == "__main__":
    docs = ["Aspirina reduce dolor", "Paracetamol para fiebre"]
    assert len(search(docs, "dolor")) > 0
