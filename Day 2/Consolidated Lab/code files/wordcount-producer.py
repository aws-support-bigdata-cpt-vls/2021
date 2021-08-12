# Producer
import socket
import time
import json
import random
import datetime



def getReferrer():
    data = {}
    now = datetime.datetime.now()
    str_now = now.isoformat()
    f1=random.choice(['Madrid', 'CapeTown', 'Denver', 'Texas', 'Yaounde','Paris', 'Mumbai', 'Sydney'])
    temp = random.random() * 100
    f2=int(round(temp, 2))
    f3=random.choice(['OK', 'FAIL', 'WARN'])
    #myrecord= str(f1)+" "+str(f2)+" "+str(f3)+"\n"
    myrecord = f'{f1}\n'
    return myrecord



HOST = '172.31.53.10' #ec2  server producer
PORT = 9999 #port number


#create to socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = getReferrer()
            print(data)
            conn.send(data.encode('utf-8'))

s.close()
