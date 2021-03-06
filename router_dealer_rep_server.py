import time
import threading
from multiprocessing import Process
import zmq

context = zmq.Context()

def worker():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.connect('tcp://127.0.0.1:10103')
    while True:
        msg = socket.recv_string()
        print(f'Received request: [{msg}]')
        time.sleep(1)
        socket.send_string(msg)

url_client = 'tcp://*:5556'
clients = context.socket(zmq.ROUTER)
clients.bind(url_client)
workers = context.socket(zmq.DEALER)
workers.bind('tcp://127.0.0.1:10103')

for _ in range(4):
    #thread = threading.Thread(target=worker)
    #thread.start()
    p = Process(target=worker)
    p.start()
    

zmq.device(zmq.QUEUE, clients, workers)
