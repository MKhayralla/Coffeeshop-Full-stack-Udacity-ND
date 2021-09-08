#  Coffeshop Full Stack 

The project is an educational project and one of udacity full-stack nanodegree projects .
it is a demonstration of API development techniques using flask micro-framework and user authentication and authorization using OIDC and jwt .
most remarakable modules used are SQLAlchemy, flask-cors and jose .
TDD approach is used through the development life-cycle .
code style in the backend is [PEP8](https://www.python.org/dev/peps/pep-0008/)


## Getting Started

### Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)





2. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


3. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Running the server

in the backend folder, execute:

```bash
export FLASK_APP=src/api.py
export FLASK_ENV=development
flask run
```



### Frontend

1. **Ionic** - Follow instructions to install ionic in this [article](https://tecadmin.net/install-ionic-framework-on-ubuntu/)

##### Follow the same order in windows or Mac




2. **NPM Packages** once you installed node and npm install dependencies by naviging to the `/frontend` directory and running:
```bash
npm install
```
This will install all of the required packages .

#### Running the server

in the frontend folder, execute:

```bash
ionic serve --port=3000
```
this will start the frontend app on `http://localhost:3000/` which is important since this is
the callback url for authentication service

## Testing The Backend
To run the tests, import the `udacity-fsnd-udaspicelatte.postman_collection.json` collection into Postman

## API Reference
### Error Handling
The API will respond with a json response that contains error code and failure message

#### Sample error response
```
{
    "success" : false,
    "error" : 404,
    "message" : "Resource Not Found"
}
```

Expected errors are 422,404,401,403,500

### Endpoints

#### GET /drinks
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks 

```bash
curl -X GET http://localhost:5000/drinks/
```

```json

{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}

```


#### GET /drinks-detail
- Request Arguments: None
- requires autherization header using bearer token for a user who have `get:drinks-detail` permission
- Returns: An object with a single key, drinks, that contains an array of drinks in long format

```bash
curl -X GET http://localhost:5000/drinks-detail/
```

```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}

```


#### POST /drinks
- Request Arguments: None
- requires autherization header using bearer token for a user who have `post:drinks` permission
- posts new drink recipes to the database
- Returns: An object with a single key, drinks, that contains the posted drink

- check the postman collection for a complete sample
- sample response :

```json

{
    "drinks": [
        {
            "id": 2,
            "recipe": {
                "color": "blue",
                "name": "Water",
                "parts": 1
            },
            "title": "Water3"
        }
    ],
    "success": true
}

```

#### PATCH /drinks/<int:drink_id>
- Request Arguments: None
- requires autherization header using bearer token for a user who have `patch:drinks` permission
- edits drink with id drink_id and returns 404 if not found
- Returns: An object with a single key, drinks, that contains the edited drink

- check the postman collection for a complete sample
- sample response :

```json

{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}

```


#### DELETE /drinks/<int:drink_id>
- requires autherization header using bearer token for a user who have `post:drinks` permission
- Deletes the drink with the given drink_id

```bash
curl -X DELETE  http://localhost:5000/drinks/1

```

```json

{
    "delete": 1,
    "success": true
}

```


## Authors
- Mahmoud Khayralla (Me)
- Udacity team who made the starter code of this project which you can find [here](https://github.com/udacity/FSND/tree/master/projects/03_coffee_shop_full_stack/starter_code)

## Acknowledgements
- I would like to thank the instructor  for making things very simple to make and giving me very deep knowledge of scurity issues in developing microservices
- I'd like to thank [Udacity](http://udacity.com/) for their great contribution to the IT learning community
- I'd like to thank the [NTL_initiative](http://techleaders.eg/learning-tracks/) for giving me this chance