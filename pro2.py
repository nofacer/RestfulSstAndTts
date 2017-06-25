import argparse
import zmq

parser = argparse.ArgumentParser(description='zeromq server/client')
parser.add_argument('--bar')
args = parser.parse_args()

if args.bar:
    print(args.bar)
    # client
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    socket.send_string(args.bar)
    msg = socket.recv()
    print (msg)
else:
    # server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5555')
    while True:
        msg = socket.recv().decode('utf-8')
        print(msg)
        if msg == 'zeromq':
            socket.send_string('ah ha!')
        else:
            socket.send_string('...nah')