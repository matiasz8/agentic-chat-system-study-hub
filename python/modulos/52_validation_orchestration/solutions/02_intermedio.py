class Validator:
    def check(self, val):
        return val is not None and len(str(val)) > 0
v = Validator()
print(v.check("test"))
