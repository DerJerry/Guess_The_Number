import unittest
from app import app

class RandomNumberGameTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_game(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['target_number'] = 42

        response = self.app.get('/game')
        self.assertEqual(response.status_code, 200)    
        
        with self.app.session_transaction() as session:
            target_number = session["target_number"]
            self.assertTrue(1<=target_number <= 100)

    def test_scoreboard(self):
        response = self.app.get('/scoreboard')
        self.assertEqual(response.status_code, 200)


    #! Nicht funktionierender Test
    def test_GuessBtn(self):
        response = self.app.post('/game', data={'guess': 50, 'target_number': 40, 'attempts': 1})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()