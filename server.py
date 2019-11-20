# -*- coding: utf-8 -*-
#
# Bluetooth server for Raspberry Configurator
# 
# Dependencies:
#     sudo apt-get install pi-bluetooth
#     sudo apt-get install bluetooth bluez
#     sudo apt-get install bluez python-bluez
#
# Run the server:
#     sudo python server.py
#
#
# For more details about setting up bluetooth see:
#   https://github.com/EnableTech/raspberry-bluetooth-demo/blob/master/README.md
# 

from bluetooth import * # to communicate with the mobile app
import os # to run system commands to setup bluetooth
import signal # to time out wairing for incomming connection

server_sock=BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

UUID = "f01deff7-042f-43bc-9a70-13f3de185046"

advertise_service(server_sock, "CubeWorks Pi Configurator", service_id = UUID, service_classes = [ UUID, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])

# Handle incomming request
# TODO: implement your read/write commands her
def handle_cmd(data, client_sock):
    s = data.strip().split(" ", 1)
    if len(s) == 0:
        send("error no command")
    if len(s) == 1:
        cmd = s[0]
        if cmd == "hello":
            send("hi", client_sock)
        elif cmd == "get":
            # TODO: return your actual values here
            f1 = '{"label": "Value 1", "value": "42", "unit": "x"}'
            f2 = '{"label": "Value 2", "value": "23", "unit": "y"}'
            send('values  [%s,%s]' % (f1, f2), client_sock)
        else:
            send("error invalid command", client_sock)
    else:
        cmd = s[0]
        data = s[1]
        if cmd == "save":
            # TODO: implement save and return updated values, status messaged, etc.
            f1 = '{"label": "Save: Not implemented!", "type": "label"}'
            f2 = '{"label": "Value 1", "value": "42", "unit": "x"}'
            f3 = '{"label": "Value 2", "value": "23", "unit": "y"}'
            send("values  [%s,%s,%s]" % (f1, f2, f3), client_sock)
        elif cmd == "print":
            print data
        else:
            send("error invalid command", client_sock)


def set_discoverable(enable=True):
    if enable:
        print("Set bluetooth device name")
        os.system('hciconfig hci0 name f01deff7conf')
        os.system('hciconfig hci0 reset')
        print("Enable discoverability")
        os.system('hciconfig hci0 piscan')
    else:
        print("disable discoverability")
        os.system('hciconfig hci0 noscan')


def send(cmd, client_sock):
    print "Sending: ", cmd
    client_sock.send(cmd)
    client_sock.send("\n")


def timeout_handler(signum, frame):
    raise Exception("timeout")


def wait_for_connection(timeout = 20):
    print("Waiting for connection on RFCOMM channel %d" % port)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        sock, client_info = server_sock.accept()
        signal.alarm(0)
        print "Accepted connection from", client_info
        return sock
    except Exception, msg:
        print "couldn't connect:", msg 
        return None
    

def listen_once(timeout = 20):
    set_discoverable()

    client_sock = wait_for_connection(timeout)

    if client_sock is not None:
        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                print "Received:", data.strip()
                handle_cmd(data, client_sock)
        except IOError as e:
            print "IOError", e
        except Exception as e:
            print "Exception", e

        print "disconnected"
        client_sock.close()

    server_sock.close()
    set_discoverable(False)
    print("all done")


if __name__ == '__main__':
    listen_once(20)

