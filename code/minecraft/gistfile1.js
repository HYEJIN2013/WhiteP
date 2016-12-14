var net = require('net'),
    events = require('events'),
    util = require('util');

function Connection(settings) {
  events.EventEmitter.call(this);
  var self = this;

  this.socket = net.createConnection(settings.port, settings.host);
  this.socket.setNoDelay(true);
  this.status = 'connecting';

  this.socket.on('connect', function() {
    console.log('connected');
    console.log('writing');
    self.socket.write(new Buffer('02', 'hex'), function() {
      console.log('flushed');
    });
    self.status = 'send-2';
  });

  function handleByte(b) {
    switch(self.status) {
      case 'send-2':
        if(b !== 0x2)
          return false;

        self.socket.write(new Buffer('01', 'hex'), function() {
          console.log('flushed');
        });
        self.status = 'send-1';

        return true;

      case 'send-1':
        if(b !== 0x1)
          return false;

        self.status = 'recv-0d';

        return true;

      case 'recv-0d':
        if(b !== 0x1)
          return false;

        self.emit('authenticated');

        return true;

      default:
        return false;
    }
  }

  this.socket.on('data', function(chunk) {
    console.log('got data: ' + chunk);
    while(chunk.length > 0) {
      if(handleByte(chunk[0])) {
        console.error('error in ' + self.status);
        process.exit(1);
      }

      chunk = chunk.slice(1);
    }
  });
}

util.inherits(events.EventEmitter, Connection);

exports.Connection = Connection;

var server = new Connection({ port: 25565, host: "localhost"});