import BaseHTTPServer
from subprocess import Popen, PIPE

# What interface to listen on
# Don't change this unless you want to leak your passwords.
HOST = '127.0.0.1'

# What port to listen on. Change this if you'd like,
# you'll need to update the chrome extension's port too.
PORT = 9573


# This will prompt the user for permission to lookup 'site's password. 
# If you don't like/want zenity, replace this with your own. 
# Returns 'True' if we should get the password. Otherwise we wont.
def prompt(site):
    exit_code = Popen([
        'zenity', 
        '--question', 
        '--text=A request for the password of [%s] has come in. Allow?' 
            % site
    ]).wait()

    return exit_code == 0 # User pushed OK
    # Zenity doc: https://help.gnome.org/users/zenity/stable/usage.html.en

# Actually make the request to pass to get the password.
def get_pass(site):
    pass_proc = Popen([
        'pass',
        'show',
        site
    ], stdout=PIPE)

    stdout, stderr = pass_proc.communicate()

    # if pass didn't exit correctly, give no password.
    if pass_proc.returncode != 0:
        return ""

    # Get the first line from pass's output
    password = stdout.split("\n")[0]

    return password

class PassRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        # No matter what happens, we're giving a valid text response.
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

        # request string
        # e.g: "/foo.html?123"
        request = s.path
        if not request:
            return
        if request[0] != '/':
            return

        # If you actually have a password for 'favicon.ico' remove this
	# but this is usually a browser wanting an icon.
	if request == '/favicon.ico':
	    return
    
        pass_name = s.path[1:] # remove the leading '/'

	# Get user authorization to get the password.
        if prompt(pass_name) != True:
            return
	
	# Get the password and tell the user!
        s.wfile.write(get_pass(pass_name))


if __name__ == '__main__':
    # Setup a server using our handler
    server = BaseHTTPServer.HTTPServer(
        (HOST, PORT), 
        PassRequestHandler)

    # Server forever, or until we break
    try:
        server.serve_forever()
    except:
        pass

    # Be nice and close the port/clean up/etc..
    server.server_close()
