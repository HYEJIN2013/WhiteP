import socket
import json
import os

''' Database server.
A program that runs a server that is accessible on http://localhost:4000/. When your server receives a request on 
http://localhost:4000/set?somekey=somevalue it should store the passed key and value in memory. When it receives a request 
on http://localhost:4000/get?key=somekey it should return the value stored at somekey.
Author: Joe Jean
Date: Feb 7, 2015 '''

def fileIsEmpty(filePath):
	return os.stat(filePath).st_size == 0


def saveToFile(filename, keyValueDict):
	content = {}
	if fileIsEmpty(filename):
		with open(filename, "w") as dbFile:
			json.dump(keyValueDict, dbFile)
	else:
		with open(filename, "r") as dbFile:
			content = json.load(dbFile)
			content.update(keyValueDict)
		with open(filename, "w") as dbFile:
			json.dump(content, dbFile)


def readFromFile(filename, key):
	with open(filename, "r") as dbFile:
		response = json.load(dbFile)
		return response.get(key)




def getVerbKeyValue(text):
	'''Take a string returned by a connection via recvfrom(),
	extract and return three key pieces of information from the URL
	parameters in the input string. The format of the first line of "text" is as follows "GET /verb?somekey=somevalue HTTP/1.1"
	Those values are the verb--set or get--,a key and a value.'''

	k = 5
	url = ""
	while text[k]!= " ":
		url += text[k]
		k += 1
	verb = url[:3]
	print url
	keyValueList = url[4:].split("=")
	key = keyValueList[0]
	value = keyValueList[1]

	return verb, key, value
	

def initializeSocket(host, port, backlog=5):
	'''Initilizes the socket, bind it to the host and port, make it listen to a number of connections specified by backlog.
	backlog is an argument to listen() it specifies the maximum number of connections that can be queued
	This returns the socket object after initialization.'''
	s = socket.socket()
	s.bind((host, port))
	s.listen(backlog)
	return s




def listenForConnections(host, port):
	#Temporary storage for the key value pairs
	keyValueDict = {} 
	dbFile = "database.txt"
	#It is important to create the db when the program launches because we check if the file is empty or not later on
	with open(dbFile,"w") as _:
		pass
	mySocket = initializeSocket(host, port)

	#The server's main loop. It waits for, accepts and processes requests
	while True:
		print "Database Server Listening on Port {}".format(port)
		connection, address = mySocket.accept()
		print "connection received from address {}".format(address)
		#Get response data from the client including the url with parameters
		responseText, _ = connection.recvfrom(4096)

		#If the request is sent to the root url --http://localhost:4000/--
		if responseText[4:10] == "/ HTTP":
			connection.send("Welcome to the DB server.\n Please use 'http://localhost:4000/set?somekey=somevalue'\
				or 'http://localhost:4000/get?key=somekey' to save and retrieve data respectively")
			connection.close()
		#Otherwise we assume the request is sent using one of the accepted url formats mentioned above.
		else:
			verb, key, value = getVerbKeyValue(responseText)
		
			if verb == "set":
				keyValueDict[key] = value
				saveToFile(dbFile, keyValueDict)
				connection.send("The key/value {} = {} was saved!".format(key, value))
				keyValueDict = {}
				connection.close()
			elif verb == "get":
				response = readFromFile(dbFile, value)
				if response!=None:
					connection.send(response)
					connection.close()
				else:
					connection.send("Sorry no saved value for key {}".format(value))
					connection.close()
			else:
				connection.send("Sorry your url must be either of the form 'http://localhost:4000/set?somekey=somevalue'\
				or of the form 'http://localhost:4000/get?key=somekey'")
				connection.close()



listenForConnections('localhost', 4000)
