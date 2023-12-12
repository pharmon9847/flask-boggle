from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    
    def setUp(self):
        """What to do before every test is run"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_homepage(self):
        """Test if information is in session and proper HTML is being displayed"""
        
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>HighScore:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Remaining:', response.data)
            
    def test_valid_word(self):
        """Test if chosen word is valid by modifying board in session"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "E", "E", "R", "Z"],
                                 ["B", "E", "E", "R", "T"],
                                 ["B", "E", "E", "R", "P"],
                                 ["B", "E", "E", "R", "W"],
                                 ["B", "E", "E", "R", "M"],]
        response = self.client.get('/check-word?word=beer')
        self.assertEqual(response.json['result'], 'ok')
        
    def test_invalid_word(self):
        """Test to see if word is on board"""
        
        self.client.get('/')
        response = self.client.get('/check-word?word=salad')
        self.assertEqual(response.json['result'], 'not-on-board')
        
    def test_non_english_word(self):
        """Test to see if word is in dictionary"""
        
        self.client.get('/')
        response = self.client.get('/check-word?word=nanoonanoo')
        self.assertEqual(response.json['result'], 'not-word')

