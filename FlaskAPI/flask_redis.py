# from flask import Flask
import redis
# app=Flask(__name__)



# @app.route("/")
# def index1():
#     return "Hello?"



if __name__=="__main__":
    conn=redis.Redis(host='127.0.0.1',port=6379,db=1)
    conn.set(1,"a")
    conn.set(2,"b")
    conn.set(3,"c")
    for i in range(1,4):
        print(conn.get(name=i).decode())
    print(type(conn.info().get("db1")['keys']))
    # app.run()