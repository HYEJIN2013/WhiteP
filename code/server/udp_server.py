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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((addr, PORT))
    print("Server's address: {0}:{1}".format(socket.gethostbyname(addr),PORT ))
    
    while True:
        sock.settimeout(None)
        print("Standing by")
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        print("Data: ",data.decode("UTF-8"), " from ", addr)
    

if __name__ == "__main__":
    main()
