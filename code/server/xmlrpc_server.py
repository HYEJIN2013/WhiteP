from SimpleXMLRPCServer import SimpleXMLRPCServer

def file_reader(file_name):

    with open(file_name, 'r') as f:
        return f.read()

server = SimpleXMLRPCServer(('localhost', 5800))
server.register_introspection_functions()

server.register_function(file_reader)

server.serve_forever()
