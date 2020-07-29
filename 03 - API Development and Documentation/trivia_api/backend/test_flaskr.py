import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["categories"])
    

    def test_fail_get_categories(self):
        response = self.client().post('/categories')
        self.assertNotEqual(response.status_code, 200)
    

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["questions"]), QUESTIONS_PER_PAGE)
        self.assertGreaterEqual(data["total_questions"], QUESTIONS_PER_PAGE)
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])
    

    def test_404_for_paginated_questions(self):
        response = self.client().get('/questions?page=10')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")
    

    def test_delete_question(self):
        response = self.client().delete('/questions/10')
        data = json.loads(response.data)
        self.assertTrue(data["success"])

    
    def test_fail_delete_question(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")
    

    def test_add_questions(self):
        # random question
        question = {
            "question": "What is the longest river in the world?",
            "answer": "Nile River",
            "category": "3",
            "difficulty": "2"
        }
        response = self.client().post('/questions',
                        data=json.dumps(question),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
    

    def test_fail_add_questions_with_empty_string(self):
        # equestion with empty content
        question = {
            "question": "",
            "answer": "Nile River",
            "category": "3",
            "difficulty": "2"
        }
        response = self.client().post('/questions',
                        data=json.dumps(question),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable")
    

    def test_fail_add_questions_with_empty_answer(self):
        # equestion with empty content
        question = {
            "question": "What is the longest river in the world?",
            "answer": "",
            "category": "3",
            "difficulty": "2"
        }
        response = self.client().post('/questions',
                        data=json.dumps(question),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable")
    

    def test_search(self):
        response = self.client().post('/search',
                        data=json.dumps({"search_term": "movie"}),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(type(data["questions"]), list)
        self.assertEqual(data["total_questions"], len(data["questions"]))
        self.assertTrue(data["current_category"])
    
    
    def test_fail_search(self):
        response = self.client().post('/search',
                        data=json.dumps({"searchterm": "movie"}),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable")
    

    def test_question_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(type(data["questions"]), list)
        self.assertEqual(data["total_questions"], len(data["questions"]))
        self.assertEqual(data["current_category"], "science")
    
    
    def test_fail_question_by_category(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")
    

    def test_quiz(self):
        body = {
            "previous_questions": [],
            "quiz_category": {
                "id": 6,
                "type": "sports" 
            }
        }
        response = self.client().post('/quizzes',
                        data=json.dumps(body),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])
    
    
    def test_fail_quiz(self):
        body = {
            "previous_questions": [],
            "quiz_category": 6
        }
        response = self.client().post('/quizzes',
                        data=json.dumps(body),
                        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable")



        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()