# from flask import Flask
from types import coroutine
import redis
# app=Flask(__name__)



# @app.route("/")
# def index1():
#     return "Hello?"



if __name__=="__main__":
    conn=redis.Redis(host='127.0.0.1',port=6379,db=1)
    # conn.append(1,'a/')
    # conn.append(2,'b/')
    # conn.append(3,'c/')
    # for i in range(1,4):
    # conn.delete(1)
    # conn.delete(2)
    # conn.delete(3)
    
    

    keys = conn.keys()
    # print(keys)
    # # print(conn.get(name=10).decode())
    for i in keys:
        conn.delete(i)
    # temp_list = conn.get(name=1).decode()
    # # print(temp_list)
    # list1 = temp_list.split('/')
    # print(list1)
    
    # print(type(conn.info().get("db1")['keys']))
    # app.run()