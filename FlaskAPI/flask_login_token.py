from flask import Flask,request
from flask.json import jsonify
from werkzeug.exceptions import abort
app = Flask(__name__)


users = [
    {
        'id':1,
        'username':'1',
        'password':'1'
    },
    {
        'id':2,
        'username':'2',
        'password':'2'
    }
]

@app.route("/",methods=["GET"])
def wel_page():
    return "Welcome_page"


@app.route("/have_login",methods=["GET"])
def have_login():
    return "You have login"

@app.route("/regist",methods=["POST"])
def login():
    if not request.json or request.json["username"] == None or request.json["password"] == None:
        abort(400)
    user_id = users[-1]['id']+1
    user_username = request.json['username']
    user_password = request.json['password']

    user = {
        'id' : user_id,
        'username' : user_username,
        'password' : user_password
    }

    users.append(user)
    return jsonify(user)


@app.route("/all_users",methods=["GET"])
def all_users():
    return jsonify(users)
    


if __name__ == "__main__":
    app.run(debug=1)