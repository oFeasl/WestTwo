from flask import Flask
from flask.json import jsonify
from werkzeug.exceptions import abort

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route("/")
def index():
    abort(404)
    return jsonify(tasks)

@app.errorhandler(404)
def nofound():
    return "NoFound"

if __name__=="__main__":
    app.run(debug=1)