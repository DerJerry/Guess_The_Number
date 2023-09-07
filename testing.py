import unittest
from app import app

class RandomNumberGameTest(unittest.Testcase):
    def selfUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code,200)

    def test_game(self):
        response = self.app.get('/game')
        self.assertEqual(response.status_code, 200)

    def test_scoreboard(self):
        response = self.app.get('/scoreboard')
        self.assertEqual(response.status_code,200)

    session = self.app.application.session
    target_number = session["target_number"]
    self.assertTrue(1<=target_number <= 100)

if __name__ == '__main__':
    unittest.main()