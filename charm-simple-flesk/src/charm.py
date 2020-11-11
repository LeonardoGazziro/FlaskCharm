#! /usr/bin/env python3
# src/charm.py

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Welcome to flask API"


@app.route('/factorial', methods=['GET'])
def factorial():
    if 'number' in flask.request.args:
        number = int(flask.request.args['number'])
        fat = 1
        while number > 0:
            fat *= number
            number -= 1
        return str(fat)
    else:
        return "Error: No number field provided. Please specify an id."


if __name__ == "__main__":
    app.run()