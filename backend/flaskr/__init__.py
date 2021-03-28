import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
@TODO: Set up CORS.
Allow '*' for origins.
Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
@TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_questions(request):
        try:
            items_limit = request.args.get('limit', 10, type=int)
            selected_page = request.args.get('page', 1, type=int)
            current_index = selected_page - 1
            questions = Question.query.order_by(Question.id).limit(items_limit).offset(
              current_index * items_limit).all()
            max_page = len(questions)/10 + 1
            # print(page_number, max_page)
            if (page_number > max_page):
                abort(404)
            start = (page_number-1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            formatted_questions = questions[start:end]
        except Exception as e:
            print(e)
            abort(404)
        return formatted_questions
    '''
@TODO:
Create an endpoint to handle GET requests
for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        if categories is None:
            abort(404)
        categories_list = [category.format() for category in categories]
        # print(books, formatted_books)

        return jsonify({
            'success': True,
            'categories': categories_list,
            'total_categories': len(categories_list)
        })

    '''
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        if questions is None or categories is None:
            abort(404)
        questions_list = [question.format() for question in questions]
        categories_list = [category.format() for category in categories]
        formatted_questions = paginate_questions(request, questions_list)
        # print(formatted_questions, categories_list)
        # print(books, formatted_books)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions_list),
            'categories': categories_list
        })
    '''
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
    '''
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        if (question_id == 5000):
            print("lmao")
        question = Question.query.filter_by(id=question_id).first()
        # print(question)
        if question is None:
            abort(404)
            # print("404")
        try:
            question.delete()
        except Exception as e:
            print(e)
            abort(422)
        return jsonify({
            'success': True,
            'deleted': question_id
        })
    '''
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
    '''
    @app.route("/questions/add", methods=["POST"])
    def create_question():
        new_question = request.get_json()['question']  # body.get('', none)
        new_answer = request.get_json()['answer']
        new_category = request.get_json()['category']
        new_difficulty = request.get_json()['difficulty']

        # print(new_question, new_answer, new_category, new_difficulty)
        new_category = str(int(new_category) + 1)
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()
        except Exception as e:
            print(e)
            abort(422)

        return jsonify({
            'success': True,
            'created': question.id,
        })
    '''
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=["POST"])
    def find_question():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
        questions_list = [question.format() for question in selection]
        selected_questions = paginate_questions(request, questions_list)
        # print(selected_questions)

        return jsonify({
          'success': True,
          'questions': selected_questions,
          'total_questions': len(selected_questions)
        })
    '''
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category_id = category_id+1
        category = Category.query.filter_by(id=category_id).first()
        questions = Question.query.filter(Question.category == category_id).all()
        questions_list = [question.format() for question in questions]
        formatted_questions = paginate_questions(request, questions_list)
        # print(formatted_questions)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions_list),
            'currentCategory': category.format()
        })
    '''
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def generate_quiz():
        body = request.get_json()
        previous_questions = body['previous_questions']
        try:
            category_id = body['quiz_category']['type']['id']
            available_questions = Question.query.filter(Question.category == category_id).all()
        except Exception as e:
            print(e)
            try:
                available_questions = Question.query.all()
            except Exception as e:
                print(e)
                abort(422)
        questions_list = [question.format()['id'] for question in available_questions]
        # print(previous_questions, category_id)
        try:
            for i in previous_questions:
                if i in questions_list:
                    questions_list.remove(i)
            if questions_list:
                question_id = random.choice(questions_list)
                question = Question.query.filter_by(id=question_id).first()
                question = question.format()
            else:
                question = False
                # print('Done')
        except Exception as e:
            print(e)
            abort(422)
        return jsonify({
          'success': True,
          'question': question
        })
    '''
@TODO:
Create error handlers for all expected errors
including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'code': 404
        }, 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'request unprocessable',
            'code': 422
        }, 422)

    return app
