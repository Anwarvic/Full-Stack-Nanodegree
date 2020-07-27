# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Documentation

### Endpoints

In this project, you can find six endpoints, in the following list, that will be disucessed with more details in a bit:

- `GET '/categories`
- `GET '/questions?page=xx'`
- `GET '/categories/<id>/questions'`
- `POST '/questions'`
- `POST '/quizzes'`
- `POST '/search'`
- `DELETE /questions/<id>`

#### GET '/categories'
This endpoint fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: (SUCCESS) A JSON object with two keys:
    - `success` which equals `True`
    - `categories` a dictionary of the categories found in the database where the key is the category id and the value is the category name.
    ```
    {
        "success": True,
        "categories":{
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports"
        }
    }
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Not Found"
    }
    ```


#### GET '/questions?page=xx`
This endpoint fetches a paginated list of questions where each page has 10 questions at most.
- Request Argument: It takes an optional `page` argument that represents the questions in this page. The default value for this argument is `1`.
- Returns: (SUCCESS) A JSON object with multiple keys:
    - `success`: which equals `True`
    - `questions`: a list of questions where each question is a dictionary.
    - `total_questions`: the total number of questions in the database.
    - `categories`: a dictionary of the categories found in the database where the key is the category id and the value is the category name.
    - `current_category`: the most common category in the returned list of questions.
    ```
    {
    "categories": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "current_category": "entertainment",
    "questions": [
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        ...
    ],
    "success": true,
    "total_questions": 100
    }
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Not Found"
    }
    ```

#### GET '/categories/<id>/questions'
This endpoint fetches a list of questions associated with the given category's id.
- Request Argument: None.
- Returns: (SUCCESS) A JSON object with multiple keys:
    - `success`: which equals `True`
    - `questions`: a list of questions associated with the given category's id where each question is a dictionary.
    - `total_questions`: the total number of questions found under this category in the database.
    - `categories`: a dictionary of the categories found in the database where the key is the category id and the value is the category name.
    - `current_category`: the name of the given category's id.
    ```
    {
    "current_category": "art",
    "questions": [
        {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        ...
        ...
    ],
    "success": true,
    "total_questions": 4
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Not Found"
    }
    ```

#### POST '/questions'
This endpoint inserts a question object into our database. The question is sent as a JSON object where it has four different keys not of them can be empty:
- `question`: The question body.
- `answer`: The answer to the question.
- `category`: The category under to this question is referring.
- `difficulty`: An integer representing difficulty of the question on a scale from 1 to 5 where 5 is very difficult.

Here is an example of how the sent data should look like
```
{
    "question": "What is the longest river in the world?",
    "answer": "Nile River",
    "category": "3",
    "difficulty": "2"
}
```
- Requst Argument: None.
- Returns: (SUCCESS) A JSON object with one key:
    ```
    {
        "success": True
    }
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Unprocessable"
    }
    ```

#### POST '/quizzes'
This endpoint gets random questions to play a quiz where the user can choose a certain category to get questions about and a question isn't repeated unless the page is refreshed. This endpoint is sent a JSON object where it has just two keys:
- `previous_questions`: A list of all previous questions which will be an empty list initially .
- `quiz_category`: A dictionary representing the category the user chose.
```
{
    "previous_questions": [],
    "quiz_category": {
        "id": 2,
        "type": "art"
    }
}
```
- Requst Argument: None.
- Returns: (SUCCESS) A JSON object with one key:
    ```
    {
        "success": True
    }
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Not Found"
    }
    ```

#### POST /search
This endpoints gets questions based on a search term. It returns any questions for whom the search term is a substring of the question independently on the letter-case. It's send a JSON object with one key called `search_term`:
```
{
    "search_term": ""
}
```
- Requst Argument: None.
- Returns: (SUCCESS) A JSON object with four key:
    - `success`: which equals `True`
    - `questions`: a list of questions where each question is a dictionary.
    - `total_questions`: the total number of questions in the database matched the search term.
    - `current_category`: the most common category in the returned list of questions.
    ```
    {
    "current_category": "art",
    "questions": [
        {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        ...
        ...
    ],
    "success": true,
    "total_questions": 4
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Unprocessable"
    }
    ```


#### DELETE /questions/<id>
This endpoint deletes question from database using a question ID. 
- Requst Argument: None.
- Returns: (SUCCESS) A JSON object with one key:
    ```
    {
        "success": True
    }
    ```
- Returns: (FAIL) A JSON object with two keys:
    - `success`: which equals `False`
    - `message`: A message that explains the error
    ```
    {
        "success": False,
        "message": "Not Found"
    }
    ```
