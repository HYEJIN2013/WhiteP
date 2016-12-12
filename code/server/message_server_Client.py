import socket
from time import strftime

IP = "192.168.1.67"
PORT = 8000
MESSAGE = "Hi there!"

def sendMessage(message, ip_address=IP, port=PORT):
    message = strftime("%Y-%m-%d %H:%M:%S") + message
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_address, port))
    client.send(message)

if __name__ == '__main__':
    sendMessage(MESSAGE)
