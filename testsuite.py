import unittest
from main import app

class TestAuthEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.username = "userABC"
        self.password = "password123"

    def test_successful_authentication(self):
        """Test successful authentication."""
        data = {"username": self.username, "password": self.password}
        response = self.app.post('/auth', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_authentication_failure(self):
        """Test authentication failure with incorrect credentials."""
        data = {"username": "invalid_user", "password": "invalid_password"}
        response = self.app.post('/auth', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Authentication failed', response.data)

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthEndpoint)
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    passed_percentage = (result.testsRun - len(result.errors) - len(result.failures)) / result.testsRun * 100
    print(f"Passed {round(passed_percentage, 2)}% of test cases.")
