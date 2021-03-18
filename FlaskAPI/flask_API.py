from flask import Flask,redirect,url_for
from flask import json
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

errors = [
    {
        "code":404,
        "state":"Page Not Found!"
    },
    {
        "code":401,
        "state":"401"
    },
    {
        "code":402,
        "state":"402"
    },
]

status = [
    {
        "code":1,
        "state":"Delete Successfully!"
    },
    {
        "code":2,
        "state":"Id No Found!"
    }
]

@app.route("/")
def index():
    abort(404)
    

@app.route("/display_tasks")
def display_tasks():
    return jsonify(tasks)


@app.route("/del_task/<int:id>")
def del_task(id):
    for i in tasks :
        if i["id"]==id:
            tasks.remove(i)
            return redirect(url_for("display_tasks"))
    return jsonify(status[1])



@app.errorhandler(404)
def nofound(error):
    return jsonify(errors[0])

if __name__=="__main__":
    app.run(debug=1)