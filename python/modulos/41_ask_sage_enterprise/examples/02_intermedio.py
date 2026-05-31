# Ask Sage Enterprise - Nivel Intermedio
# Autenticacion multi-tenant

class MultiTenantServer:
    def __init__(self):
        self.tenants = {
            "sk-key-1": "Hospital A",
            "sk-key-2": "Clinica B"
        }
        self.responses = {"aspirina": "AINE"}
    
    def validate_key(self, api_key):
        return api_key in self.tenants
    
    def ask(self, api_key, question):
        if not self.validate_key(api_key):
            return {"error": "Invalid API key", "status": 401}
        
        tenant = self.tenants[api_key]
        for key, value in self.responses.items():
            if key in question.lower():
                return {"answer": value, "tenant": tenant, "confidence": 0.9}
        return {"answer": "No encontre", "tenant": tenant, "confidence": 0.0}

if __name__ == "__main__":
    server = MultiTenantServer()
    print(server.ask("sk-key-1", "Que es aspirina?"))
