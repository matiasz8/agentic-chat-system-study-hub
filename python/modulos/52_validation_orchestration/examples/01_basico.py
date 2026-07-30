def validate(result, expected):
    assert result == expected, f"Expected {expected}, got {result}"
    return True


result = validate(1 + 1, 2)
print("✅ Test passed")
