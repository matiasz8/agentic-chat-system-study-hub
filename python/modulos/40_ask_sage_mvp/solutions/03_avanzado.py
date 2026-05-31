class Agent:
    def retrieve(self, q):
        return [f"Doc for {q}"]
    def generate(self, docs):
        return "Answer: " + str(docs)
    def validate(self, answer):
        return len(answer) > 0
    def process(self, q):
        docs = self.retrieve(q)
        ans = self.generate(docs)
        return {"answer": ans, "valid": self.validate(ans)}

if __name__ == "__main__":
    agent = Agent()
    print(agent.process("test"))
