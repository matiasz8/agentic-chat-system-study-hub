class TestRunner:
    def __init__(self):
        self.tests = []
    
    def add_test(self, name, func):
        self.tests.append((name, func))
    
    def run(self):
        for name, func in self.tests:
            try:
                func()
                print(f"✅ {name}")
            except AssertionError as e:
                print(f"❌ {name}: {e}")

runner = TestRunner()
runner.add_test("addition", lambda: 1+1 == 2 or (_ for _ in ()).throw(AssertionError()))
runner.run()
