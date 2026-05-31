class AuthAPI:
    def __init__(self):
        self.valid_keys = {"sk-key-1"}
    
    def validate_key(self, api_key):
        return api_key in self.valid_keys
    
    def ask(self, api_key, question):
        if not self.validate_key(api_key):
            return {"error": "Invalid key"}
        return {"answer": "Response", "confidence": 0.9}

if __name__ == "__main__":
    api = AuthAPI()
    print(api.ask("sk-key-1", "test"))
