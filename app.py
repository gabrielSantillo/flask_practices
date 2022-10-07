from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
import json
from apihelpers import check_endpoint_info

app = Flask(__name__)

@app.post('/api/client')
def add_client():
    invalid = check_endpoint_info(request.json, ['username', 'password', 'is_premium'])
    if(invalid != None):
        return invalid

    results = run_statement('CALL insert_client(?,?,?)',
    [request.json.get('username'), request.json.get('password'), request.json.get('is_premium')])

    if(type(results) == list):
        return make_response(jsonify(results), 201)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(jsonify(results), 400)

@app.patch('/api/client')
def change_password():
    invalid = check_endpoint_info(request.json, ['username', 'old_password', 'new_password'])
    if(invalid != None):
        return invalid

    results = run_statement('CALL change_password(?,?,?)',
    [request.json.get('username'), request.json.get('old_password'), request.json.get('new_password')])

    if(type(results) == list):
        if(len(results) == 1):
            return make_response(jsonify(results), 200)
        else:
            return make_response(jsonify("Invalid password"), 401)
    else:
        return make_response(jsonify(results), 400)


app.run(debug=True)