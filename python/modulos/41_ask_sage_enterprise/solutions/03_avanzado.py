from collections import defaultdict

class RateLimitedAPI:
    def __init__(self):
        self.valid_keys = {"sk-key-1"}
        self.counts = defaultdict(int)
        self.limit = 100
    
    def validate_key(self, api_key):
        return api_key in self.valid_keys
    
    def check_limit(self, api_key):
        self.counts[api_key] += 1
        return self.counts[api_key] <= self.limit
    
    def ask(self, api_key, question):
        if not self.validate_key(api_key):
            return {"error": "Invalid key"}
        if not self.check_limit(api_key):
            return {"error": "Rate limit exceeded"}
        return {"answer": "Response", "confidence": 0.9}

if __name__ == "__main__":
    api = RateLimitedAPI()
    print(api.ask("sk-key-1", "test"))
