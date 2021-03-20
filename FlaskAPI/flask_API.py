from flask import Flask,redirect,url_for
from flask import json
from flask.globals import request
from flask.json import jsonify
from werkzeug.exceptions import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
app.config["SECRET_KEY"] = "dsaiwe982nzcxsa79e812dsa"


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'state': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False,
        'owner':1
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'state': u'Need to find a good Python tutorial on the web',
        'done': False,
        'owner':1
    },
    {
        'id': 3,
        'title': u'Test_title_3',
        'state': u'Test_state_3',
        'done': False,
        'owner':2
    }
]


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

@app.route("/")
def index():
    token_result = judge_token(request.headers)
    
    abort(404)
    

@app.route("/display_tasks",methods=["GET"])
def display_tasks():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']


    
    my_tasks=[]
    for i in tasks:
        if i['owner'] == user_id:
            my_tasks.append(i)
    return jsonify(my_tasks)

#####################删除###########################

# 删除接口，返回data中带有删除的task
@app.route("/del_task/<int:id>",methods=["DELETE"])
def del_task(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']


    for i in tasks :
        if i["id"]==id and i["owner"]==user_id:
            del_task = i
            tasks.remove(i)
            return jsonify(return_Feedback(status=0,message="删除成功",data=del_task))
    return jsonify(status[1])


# 删除所有已完成事项
@app.route("/del_all_done",methods=["DELETE"])
def del_all_done():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']

    temp_task1 = []
    for i in tasks:
        if i["done"] == True and i["owner"]==user_id:
            temp_task1.append(i)
    for j in temp_task1:
        tasks.remove(j)
    return jsonify(return_Feedback(status=0,message="删除成功",data=temp_task1))


# 删除所有已代办事项
@app.route("/del_all_undone",methods=["DELETE"])
def del_all_undone():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']


    temp_task2 = []
    for i in tasks:
        if i["done"] == False and i["owner"]==user_id:
            temp_task2.append(i)
    for j in temp_task2:
        tasks.remove(j)
    return jsonify(return_Feedback(status=0,message="删除成功",data=temp_task2))


#######################删除#########################



@app.route("/get")
def get():
    print(request.method)
    print(request.json)
    print(request.headers)
    print(request.host)
    print(request.url)

#######################新增#########################


# 新增task接口，返回data中带有新增的task
@app.route("/add_task",methods=["POST"])
def add_task():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']


    if not request.json or not 'title' in request.json:
        return jsonify(status[2])
    task={
        "id":tasks[-1]["id"]+1,
        "title":request.json["title"],
        'state': request.json.get("state", ""),
        "done":False,
        "owner":user_id
    }
    tasks.append(task)
    return jsonify(return_Feedback(status=0,message="",data=task))


#######################新增#########################








#######################更改#########################

# 将1条task设为已办
@app.route("/set_a_done/<int:id>",methods=["PUT"])
def set_a_done_(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["id"] == id and i["owner"]==user_id:
            i["done"] = True
            return jsonify(return_Feedback(status=0,message="",data=i))
    return jsonify(return_Feedback(status=1,message="Id Not Found",data={}))

# 将1条task设为待办
@app.route("/set_a_undone/<int:id>",methods=["PUT"])
def set_a_undone_(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["id"] == id and i["owner"]==user_id:
            i["done"] = False
            return jsonify(return_Feedback(status=0,message="",data=i))
    return jsonify(return_Feedback(status=1,message="Id Not Found",data={}))

# 将所有task设为已办
@app.route("/set_all_done",methods=["PUT"])
def set_all_done_():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["owner"]==user_id:
            i["done"]=True
    return jsonify(return_Feedback(status=0,message="All Tasks Are Done",data={}))

# 将所有task设为待办
@app.route("/set_all_undone",methods=["PUT"])
def set_all_undone_():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=1,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["owner"]==user_id:
            i["done"]=False
    return jsonify(return_Feedback(status=0,message="All Tasks Are Undone",data={}))

#######################更改#########################





#######################查找#########################






#######################查找#########################




#######################注册#########################
@app.route("/regist",methods=["POST"])
def regist():
    if not request.json or not "username" in request.json or not "password" in request.json:
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
#######################注册#########################





#######################登录#########################
@app.route("/login",methods=["POST"])
def login():
    print(request.json)
    if not request.json or not "username" in request.json or not "password" in request.json:# 格式错误
        return jsonify(return_Feedback(status=1,message="Form Error",data=""))
    for i in users:# 遍历用户列表
        if i["username"] == request.json["username"] and i["password"]==request.json["password"]:
            return {"user":request.json,"token":get_token(user_id=i["id"],user_name=i["username"],user_pwd=i["password"])} # 认证成功
    return jsonify(return_Feedback(status=1,message="Login Error",data=""))# 没有这个用户
    

def get_token(user_id,user_name,user_pwd):
    s = Serializer(secret_key=app.config["SECRET_KEY"],expires_in=3600)
    token = s.dumps({"id":user_id,"username":user_name,"password":user_pwd}).decode("ascii")
    return token


def judge_token(headers):
    try:
        token = headers["token"]
        s = Serializer(app.config["SECRET_KEY"],1800)
        token_result = s.loads(token)
        return token_result
    except:
        return False

#######################登录#########################

@app.errorhandler(404)
def nofound(error):
    return jsonify(errors[0])

def return_Feedback(status,message,data):
    Feedback = {
        "status"  : 0,
        "message" :" ",
        "data"    : " "
    }
    Feedback["status"]=status
    Feedback["message"]=message
    Feedback["data"]=data
    return Feedback

if __name__=="__main__":
    app.run(debug=1)