class SimpleAPI:
    def ask(self, question):
        return {"answer": "Response for " + question, "confidence": 0.9}

if __name__ == "__main__":
    api = SimpleAPI()
    print(api.ask("test"))
