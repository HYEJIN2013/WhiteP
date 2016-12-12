import socket #import librery for sockets
import random #import librery for random numers



s = socket.socket()
s.bind(("localhost",9999))


s.listen(10) ##accept maxim conexion
n = 0
x = random.randint(1, 50)
y = 0
res= 0
a = 0
d = 0

print "Esperamos que alguien se conecte"
sc, addr = s.accept() ##host y direccion and waiting conexion
print "Se trata de conectar alguien"

#def funcion:
base = open("usuario.dat","r")##base data user
llave = open("llaves.dat","r")##base data private 


#funcion for verific user#
def verificar(recivido):
    for i in base.xreadlines():
        dato = i
        x = 0
        print "dato = ",dato
        tam = len(dato)
        print "recivido = ",recivido
        if str(recivido) == str(dato):
            print "si eres tu xD"
            break
        else:
            "no eres tu xD"


##funcion for read keys
def llaves():
    global d
    global n
    for i in llave.xreadlines():
        tam = len(i)
        d = int(i[0])
        n = 14



##funcion for send messege to client
def enviar():
    print "numero que ando enviando: ",x
    sc.send(str(x))


##funcion for recive messege of client
def recivir():
    global res
    llaves()
    print "e = ",d
    print "n = ",n
    recibido = int(sc.recv(1024))
    print "recibodo r= ", recibido
    res = recibido
    ##calculate "y" of client with the private keys
    a = pow(res,d) % n
    #messege desencript#
    print "Y=",a


#funcion of y#
def funcion():
    global y
    y = x
    print "yyyy",y


#process of comunication#
while True:
    if n == 0:
        enviar()
        n = 1
    if n == 1:
        print "esperando respuesta"
        funcion()
        recivir()
        
        n = 2
    if n == 2:
        print "espero respuesta:"
        recibido = sc.recv(1024)
        print "tu nombre es: ",recibido
        verificar(recibido)
        n = 3
print "adios"



sc.close()##close client
s.close() ##close server
