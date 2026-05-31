def score(query, doc):
    query_words = set(query.lower().split())
    doc_words = set(doc.lower().split())
    return len(query_words & doc_words) / len(doc_words) if doc_words else 0

def search_ranked(docs, query):
    scored = [(score(query, d), d) for d in docs]
    return sorted(scored, reverse=True)

if __name__ == "__main__":
    docs = ["Aspirina", "Paracetamol"]
    print(search_ranked(docs, "aspirina"))
