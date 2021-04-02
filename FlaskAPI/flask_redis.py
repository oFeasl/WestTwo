import redis


if __name__=="__main__":
    conn=redis.Redis(host='127.0.0.1',port=6379,db=1)

    keys = conn.keys()
    for i in keys:
        conn.delete(i)