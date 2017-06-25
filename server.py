import os
import zmq


print ('Process id:',str(os.getpid()) )
# server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:5555')
while True:
    msg = socket.recv().decode('utf-8')
    print(msg)
    socket.send_string('ah ha!')
