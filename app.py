from flask import Flask, request
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
        results_json = json.dumps(results, default=str)
        return results_json
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return "Sorry."

@app.patch('/api/client')
def change_password():
    invalid = check_endpoint_info(request.json, ['username', 'old_password', 'new_password'])
    if(invalid != None):
        return invalid

    results = run_statement('CALL change_password(?,?,?)',
    [request.json.get('username'), request.json.get('old_password'), request.json.get('new_password')])

    if(type(results) == list):
        results_json = json.dumps(results, default=str)
        return results_json
    else:
        return "Sorry."


app.run(debug=True)