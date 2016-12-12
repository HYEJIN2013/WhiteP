import web
import subprocess

urls = (
    '/ping/(.*)/', 'ping'
)

app = web.application(urls, globals())

class ping:        
    def GET(self, ip):
        result = subprocess.call(["ping", "-c", "1", ip])

        # return code zero means that ping worked
        if result == 0:
            return "ok"
        else:
            return "not ok"

if __name__ == "__main__":
    app.run()
