var connect = require('connect')
var http = require('http')

var app = connect()

// gzip/deflate outgoing responses
var compression = require('compression')
app.use(compression())

// list of banned IPs
var banned = [
'127.0.0.1',
'192.168.2.12'
];

// the middleware function
blacklist = function() {
    
    return function(req, res, next) {
        if (banned.indexOf(req.connection.remoteAddress) > -1) {
            res.end('Banned');
        }
        else { next(); }
    }
    
};
app.use(blacklist());

// respond to all requests
app.use(function(req, res){
  res.end('Hello from Connect!\n');
})

//create node.js http server and listen on port
http.createServer(app).listen(3000)
