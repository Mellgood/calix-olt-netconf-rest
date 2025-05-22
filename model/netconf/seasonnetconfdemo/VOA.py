import socket
import sys
from time import sleep, time


def set_attenuation(att_val):
    # Use a breakpoint in the code line below to debug your script.

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('10.13.17.73', 1234)
    #print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:

        # Send test message
        message = '{"cmd1":1,"cmd2":1}'
        sock.send(message.encode('utf-8'))
        message="\r\n";
        sleep(1)
        sock.send(message.encode('utf-8'));
        while True:
            data = sock.recv(1000)
            print('received "{data}"'.format(data=data))
            break

        # obtain control
        # put in the string the data you received
        message='{"cmd1":2,"cmd2":1,"userdata":{"idProduct":22354,"idVendor":5251,"sn":"POACCH0020"}}'
        sock.send(message.encode('utf-8'))
        message="\r\n";
        sleep(1)
        sock.send(message.encode('utf-8'));
        while True:
            data = sock.recv(1000)
            print('received "{data}"'.format(data=data))
            break

        # set attenuation ch1
        message='{"cmd1":102,"cmd2":2,"userdata":{"attenuation":%d,"channel":1,"idProduct":22354,"idVendor":5251,"sn":"POACCH0020"}}'%(att_val)
        #print(message);
        sock.send(message.encode('utf-8'))
        message="\r\n";
        sleep(1)
        sock.send(message.encode('utf-8'));
        while True:
            data = sock.recv(1000)
            print('received "{data}"'.format(data=data))
            break

        # set attenuation ch1
        message='{"cmd1":102,"cmd2":2,"userdata":{"attenuation":%d,"channel":2,"idProduct":22354,"idVendor":5251,"sn":"POACCH0020"}}'%(att_val)
        #print(message);
        sock.send(message.encode('utf-8'))
        message="\r\n";
        sleep(1)
        sock.send(message.encode('utf-8'));
        while True:
            data = sock.recv(1000)
            print('received "{data}"'.format(data=data))
            break

    finally:
        #print >> sys.stderr, 'closing socket'
        sock.close()

def insert_failure():
    set_attenuation(1600)

def remove_failure():
    set_attenuation(53)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #insert_failure()
    #remove_failure()

    set_attenuation(600)
    #t = time()
    # do stuff
    #for i in range(1000000):
    #    print(i)
    #elapsed = time() - t
    #print(elapsed)

