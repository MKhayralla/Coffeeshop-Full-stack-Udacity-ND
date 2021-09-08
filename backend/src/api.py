import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_all_drinks():
    drinks = list(map(lambda drink:drink.short(), Drink.query.all()))
    return jsonify(
        {
            'success' : True,
            'drinks' : drinks
        }
    )



@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_all_drink_details(current_user):
    drinks = list(map(lambda drink:drink.long(), Drink.query.all()))
    return jsonify(
        {
            'success' : True,
            'drinks' : drinks
        }
    )


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(current_user):
    try:
        data = request.json
        drink = Drink(title = data['title'], recipe ="""{}""".format(json.dumps(data['recipe'])))
        drink.insert()
    except:
        abort(422)
    return jsonify(
        {
            'success' : True,
            'drinks' : [drink.long()]
        }
    )


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(current_user, id):
    data = request.json
    drink = Drink.query.get_or_404(id)
    try:
        if 'title' in data:
            drink.title = data['title']
        if 'recipe' in data:
            drink.recipe = """{}""".format(json.dumps(data['recipe']))
        drink.update()
    except :
        abort(422)
    return jsonify(
        {
            'success' : True,
            'drinks' : [drink.long()]
        }
    )


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(current_user, id):
    drink = Drink.query.get_or_404(id)
    drink.delete()
    return jsonify(
        {
            'success' : True,
            'delete' : id
        }
    )

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.message
    }), error.status_code

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


