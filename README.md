## Trivia Torrent

This full stack application is a trivia game where users can go through a game of questions trying to get the highest score possible! Users can add, delete and search for questions through various categories including but not limited to Science, Art and Geography. 
This application consists of 2 parts: the frontend run by react and javascript, and the backend run mainly by flask and python and also including sqlalchemy for database manipulation.

## Getting Started
# Prerequisites

This project was run on Python 3.7 so developers should have that installed on their computers in addition to Node for the backend.

# Backend #

From the backend folder run 

//pip install requirements.txt 

All required packages are included in the requirements file.

To run the application run the following commands:

//export FLASK_APP=flaskr
//export FLASK_ENV=development
//flask run

This runs the application in development mode and this ouputs a debugger in the console and the server refreshes itself whenever changes are made.
*The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration. 

# Frontend #

From the frontend folder, run the following commands to start the client:

//npm install // only once to install dependencies
//npm start 

By default, the frontend will run on localhost:3000

## API Reference
# Error Handling

Errors are returned in a JSON object format as follows:

{
    'success' : False,
    'error' : 400,
    'message' : 'bad request'
}

This API supports 2 different error types:
1. 404: resource not found
2. 422: not processable

# Endpoints #

GET /categories
-returns a list of all available categories and their number

//curl http://127.0.0.1:5000/categories

--Response--
{'categories' : [{
    'id' : 0,
    'type' : 'Science'
},{
    'id' : 1,
    'type' : 'History'
}]
, 'total_categories' : 2}

GET /questions
-returns a list of questions paginated by sets of 10, number of total questions, and also a list of all categories.
-used to populate the main list page

//curl http://127.0.0.1:5000/questions

--Response--
{'questions' : [{
      'id': 0,
      'question': '??',
      'answer': 'A',
      'category': 1,
      'difficulty': 4
    },
    {
      'id': 1,
      'question': '??',
      'answer': 'A',
      'category': 2,
      'difficulty': 5
}]
'categories' : [{
    'id' : 0,
    'type' : 'Science'
},{
    'id' : 1,
    'type' : 'History'
}]
, 'total_questions' : 2}

DELETE /questions/<int:question_id>
-deletes question of inputted id
-returns id of deleted question

//curl -X DELETE http://127.0.0.1:5000/questions/3

--Response--
{
    'deleted' : 1
}

POST /questions/add
-adds new question with data accompanied with request
-request body should include 'question', 'answer', 'category' (category_id) and 'difficulty'
-returns id of created question

//curl http://127.0.0.1:5000/questions/add -X POST -H "Content-Type: application/json" -d '{"question":"??", "answer":"A", "category":"2", "difficulty":"4"}'

--Response--
{
    'created' : 1
}

POST /questions/search
-returns a list of questions that include search term which is included with the request under key 'searchTerm'

//curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"search"}'

--Response--
{'questions' : [{
      'id': 0,
      'question': '??',
      'answer': 'A',
      'category': 1,
      'difficulty': 4
    },
    {
      'id': 1,
      'question': '??',
      'answer': 'A',
      'category': 2,
      'difficulty': 5
}]
, 'total_questions' : 2}

GET /categories/<int:category_id>/questions
-returns list of questions under selected category paginated by sets of 10 and also the current selected category

//curl http://127.0.0.1:5000/categories/2/questions

--Response--
{'questions' : [{
      'id': 0,
      'question': '??',
      'answer': 'A',
      'category': 1,
      'difficulty': 4
    },
    {
      'id': 1,
      'question': '??',
      'answer': 'A',
      'category': 2,
      'difficulty': 5
}]
, 'total_questions' : 2,
'currentCategory' : 'Science'}

POST /quizzes
-returns a new question that hasn't been asked previously
-request body should include 'previous_questions' which is a list of already asked question ids, and 'quiz_category' which includes the selected category

//curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[2,1], "quiz_category":"Science"}'

--Response--
{
    'question' : '??'
}

## Authors

Yousef Ahmed Radwan

## Acknowledgements

Big thanks to udacity for their incredibly insightful course