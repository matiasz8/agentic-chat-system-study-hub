import unittest

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.data = {"status": "ok"}
    
    def test_status(self):
        self.assertEqual(self.data["status"], "ok")
    
    def test_structure(self):
        self.assertIn("status", self.data)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
