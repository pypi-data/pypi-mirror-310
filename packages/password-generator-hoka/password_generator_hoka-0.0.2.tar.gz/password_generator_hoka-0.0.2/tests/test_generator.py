import unittest
from password_generator.generate_password import generate_password

class TestPasswordGenerator(unittest.TestCase):
    def test_default_length(self):
        password = generate_password()
        self.assertEqual(len(password), 12)

    def test_custom_length(self):
        password = generate_password(length=8)
        self.assertEqual(len(password), 8)

    def test_no_special_chars(self):
        password = generate_password(use_special_chars=False)
        self.assertTrue(all(c.isalnum() for c in password))

    def test_error_on_too_short_length(self):
        with self.assertRaises(ValueError):
            generate_password(length=3)

if __name__ == "__main__":
    unittest.main()
