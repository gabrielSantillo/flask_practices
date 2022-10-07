from flask import Flask, request
from dbhelpers import run_statement
import json

app = Flask(__name__)



app.run(debug=True)