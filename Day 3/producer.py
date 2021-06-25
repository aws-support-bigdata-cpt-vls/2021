import socket
import time
import json
import random
import datetime
def ProductInfoProducer():
    item=random.choice(['Apple', 'Orange', 'Mango', 'Guava', 'Pear','Grape', 'Lemon', 'Banana'])
    return f'{item}\n'
HOST = '10.10.20.158'  #ec2  server producer
PORT = 8000 #port number
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = ProductInfoProducer()
            print(data)
            conn.send(data.encode('utf-8'))
s.close()