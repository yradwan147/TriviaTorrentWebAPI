import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginated_books(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue((data['categories']))
    
    """ def test_404_page_overflow(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['code'], 404) """

    def test_delete_element(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
    
    """ def test_delete_element_nonexistent(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['code'], 404) """
    
    def test_add_element(self):
        res = self.client().post('/questions/add', json={"question":"??", "answer":"A", "category":"4", "difficulty":"4"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    def test_search_element(self):
        res = self.client().post('/questions/search', json={'searchTerm':'boxer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertTrue(data['questions'])
    
    def test_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])
        self.assertEqual(data['total_questions'], 3)
        self.assertTrue(data['questions'])

    def test_question_generation(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category' : {'type':{'id':1}}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_question_generation_noduplicates(self):
        res = self.client().post('/quizzes', json={'previous_questions':[21,20], 'quiz_category' : {'type':{'id':1}}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['id'], 22)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()