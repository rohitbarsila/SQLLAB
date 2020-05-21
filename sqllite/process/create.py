from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import sqlite3
from sqlite3 import Error
import os


def create_connection(user):

    os.makedirs('Database', exist_ok=True)
    db=olddb=sqlite3.connect('Database/testDB.db')
    conn=newdb=sqlite3.connect('Database/'+str(user)+'.db')
    x=db.execute("SELECT * FROM AGENTS")
    header=x.description
    head=[]
    for l in header:

        head.append(l[0])
    data = x.fetchall()

    print(data)
    try:
        conn.execute("CREATE TABLE AGENTS "+str(tuple(head)) +";")
    except:
        pass
    for d in data:
        update_task(newdb,d)
    db.close()
    return conn

def update_task(conn, task):

    x=[]
    for val in range(len(task)):
        x.append("?")
    sql = "insert into AGENTS values "+str(tuple(x)).replace("'","")
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def input_command(user,command):

    conn = sqlite3.connect('Database/'+str(user)+'.db')
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows

def reset(user):
    if os.path.exists('Database/' + str(user) + '.db'):
        conn = sqlite3.connect('Database/' + str(user) + '.db')
        cur = conn.cursor()
        cur.execute("drop table AGENTS")
        conn.commit()
        create_connection(user)
    else:
        print("The file does not exist Creating ")
        create_connection(user)
    return True

class DataP(APIView):
    def post(self, request, format=None):
            user=request.user
            data=request.data
            reset(user)
            if "reset" in request.data and request.data["reset"]=="True":
                    x=reset(user)
                    if x:
                        return Response({"Status": "Sucess", "Message": "Data Reset Done"})
                    else:
                        return Response({"Status": "Error", "Message": "Something Occured"})
            elif "command" in request.data:
                command=data["command"]
                output=input_command(request.user,command)
                return Response({"Status":"Sucess","Output":output})
            else:
                return Response({"Status": "Error", "Message": "Command Not Found" })
