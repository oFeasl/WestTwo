from flask import Flask,redirect,url_for
from flask import json
from flask.globals import request
from flask.json import jsonify
from werkzeug.exceptions import abort

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'state': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'state': u'Need to find a good Python tutorial on the web',
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
    },
    {
        "code":3,
        "state":"Add Failed!"
    }
]

@app.route("/")
def index():
    abort(404)
    

@app.route("/display_tasks")
def display_tasks():
    return jsonify(tasks)


# 删除接口，返回data中带有删除的task
@app.route("/del_task/<int:id>",methods=["DELETE"])
def del_task(id):
    for i in tasks :
        if i["id"]==id:
            del_task = i
            tasks.remove(i)
            return jsonify({"status":0,"message":"删除成功","data":del_task})
    return jsonify(status[1])


# 新增task接口，返回data中带有新增的task
@app.route("/add_task",methods=["POST"])
def add_task():
    if not request.json or not 'title' in request.json:
        return jsonify(status[2])
    task={
        "id":tasks[-1]["id"]+1,
        "title":request.json["title"],
        'state': request.json.get("state", ""),
        "done":False
    }
    tasks.append(task)
    return jsonify({"status":0,"message":"添加成功","data":task})



@app.errorhandler(404)
def nofound(error):
    return jsonify(errors[0])

if __name__=="__main__":
    app.run(debug=1)