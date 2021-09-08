import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# initialize Flask app
app = Flask(__name__)
setup_db(app)
CORS(app)

# reinitialize the database for testing
db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_all_drinks():
    '''
    returns all drinks in database in short format
    '''
    # find all drinks in database
    drinks = list(map(lambda drink: drink.short(), Drink.query.all()))
    return jsonify(
        {
            'success': True,
            'drinks': drinks
        }
    )


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_all_drink_details(current_user):
    '''
    requires at least barista role
    returns all drinks in database in long format
    '''
    # find all drinks in database
    drinks = list(map(lambda drink: drink.long(), Drink.query.all()))
    return jsonify(
        {
            'success': True,
            'drinks': drinks
        }
    )


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(current_user):
    '''
    posts a new drink to the database
    requires manager role
    returns the inserted drink
    '''
    try:
        data = request.json
        # initiate new drink from Drink class
        drink = Drink(title=data['title'], recipe="""{}""".format(
            json.dumps(data['recipe'])))
        # do a commit to insert it to db
        drink.insert()
    except Exception:
        abort(422)
    return jsonify(
        {
            'success': True,
            'drinks': [drink.long()]
        }
    )


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(current_user, id):
    '''
    updates the required drink
    requires manager role
    returns the updated drink or 404
    '''
    data = request.json
    # find the required drink or abort(404)
    drink = Drink.query.get_or_404(id)
    # update the drink
    try:
        if 'title' in data:
            drink.title = data['title']
        if 'recipe' in data:
            drink.recipe = """{}""".format(json.dumps(data['recipe']))
        # commit changes
        drink.update()
    except Exception:
        abort(422)
    return jsonify(
        {
            'success': True,
            'drinks': [drink.long()]
        }
    )


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(current_user, id):
    '''
    deletes the required drink with the given id
    requires manager role
    returns the id of the deleted entry
    '''
    # find the drink with given id or abort(404)
    drink = Drink.query.get_or_404(id)
    # delete the drink from the database
    drink.delete()
    return jsonify(
        {
            'success': True,
            'delete': id
        }
    )


# Error Handling
'''
unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
server error
'''


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


'''
Authentication and Authorization errors
'''


@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.message
    }), error.status_code


'''
not found
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
