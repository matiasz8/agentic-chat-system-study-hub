# Ask Sage Enterprise - Nivel Avanzado
# Rate limiting y monitoring

from collections import defaultdict
import time

class EnterpriseServer:
    def __init__(self):
        self.tenants = {"sk-key-1": "Hospital A"}
        self.responses = {"aspirina": "AINE"}
        self.request_counts = defaultdict(int)
        self.request_limit = 100
    
    def validate_key(self, api_key):
        return api_key in self.tenants
    
    def check_rate_limit(self, api_key):
        self.request_counts[api_key] += 1
        return self.request_counts[api_key] <= self.request_limit
    
    def ask(self, api_key, question):
        if not self.validate_key(api_key):
            return {"error": "Invalid API key", "status": 401}
        
        if not self.check_rate_limit(api_key):
            return {"error": "Rate limit exceeded", "status": 429}
        
        start = time.time()
        tenant = self.tenants[api_key]
        
        for key, value in self.responses.items():
            if key in question.lower():
                duration = time.time() - start
                return {"answer": value, "tenant": tenant, "duration_ms": int(duration * 1000)}
        
        return {"answer": "No encontre", "tenant": tenant}

if __name__ == "__main__":
    server = EnterpriseServer()
    print(server.ask("sk-key-1", "Que es aspirina?"))
