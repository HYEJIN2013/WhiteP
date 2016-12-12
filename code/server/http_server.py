#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: http_ser.py
#         Desc: http server
#       Author: Sungis
#        Email: mr.sungis@gmail.com
#     HomePage: http://sungis.github.com
#      Version: 0.0.1
#   LastChange: 2014-01-10 20:01:30
#      History:
#=============================================================================
'''

import socket
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "==> python http_ser.py 8080"
    else:
        port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('localhost', port))
        sock.listen(5)
        print("server start@%d" %port)
        
        while True:
            connection,address = sock.accept()
            connection.settimeout(5)
            buf = connection.recv(1024)
            req = buf.split('\n')
            strs = req[0].split(' ')
            url = strs[1]
            rep = list()
            rep.append('HTTP/1.1 200 OK')
            if '/stop' == url:
                rep.append("<html><body>stop server</body></html>")
                connection.send('\n\n'.join(rep))
                connection.close()
                break
            if "/index" == url:
                f = open("index.html")
                s = f.read()
                f.close()
                rep.append(s)
                connection.send("\n\n".join(rep))
                connection.close()
            else:
                html = "<html><body>%s</body></html>" %("<br>".join(req))
                rep.append(html)
                connection.send('\n\n'.join(rep))
                connection.close()
        sock.close()
