import socket
import sys

def main():
    argc = len(sys.argv)
    addr = "127.0.0.1"
    PORT = 801
    if(argc > 1):
        addr = sys.argv[1]
    if(argc > 2): 
        PORT = sys.argv[2]
    sock = socket.socket()
    sock.bind((addr, PORT))
    sock.listen(10)
    print("Server's address: {0}:{1}".format(socket.gethostbyname(addr),PORT ))
    
    while True:
        sock.settimeout(None)
        print("Awaiting connection")
        conn, addr = sock.accept()
        print("Got connection: ", addr)
        while True:
            sock.settimeout(15)
            data = conn.recv(1024)
            if not data:
                break
            print("Data: ",data.decode("UTF-8"))
    

if __name__ == "__main__":
    main()
