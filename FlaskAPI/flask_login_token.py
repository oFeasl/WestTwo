from flask import Flask,request
from flask.globals import current_app
from flask.json import jsonify
from werkzeug.exceptions import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



app = Flask(__name__)

app.config["SECRET_KEY"] = "dasxrgdsdosainfsakjdasdsahdsaoi78"



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


@app.route("/have_login",methods=["POST"])
def have_login():
    respond = judge_token(request.headers)
    if respond == False:
        return "Error"
    return "ID="+(str)(respond)



@app.route("/regist",methods=["POST"])
def regist():
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
    

@app.route("/login",methods=["POST"])
def login():
    print(request.json)
    if not request.json or not "username" in request.json or not "password" in request.json:
        return "form error"
    for i in users:
        if i["username"] == request.json["username"] and i["password"]==request.json["password"]:
            return {"user":request.json,"token":create_token(user_id=i["id"])}
    return "Error 2"
    
def create_token(user_id):
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=1800)
    token = s.dumps({"id":user_id}).decode("ascii")
    return token


def judge_token(headers):
    try:
        token = headers["token"]
        s = Serializer(app.config["SECRET_KEY"],1800)
        datas = s.loads(token)
        return datas["id"] 
    except:
        return False


if __name__ == "__main__":
    app.run(debug=1)