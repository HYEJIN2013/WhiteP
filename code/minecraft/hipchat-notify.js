Tail = require('tail').Tail;tail = new Tail("latest.log");
HipChatClient = require('node-hipchat')hipchat = new HipChatClient("*************************");
var loginPattern = /.*\[Server thread\/INFO\]: (.*) joined the game/;
tail.on("line", function(data) {	var loginMatch = data.match(loginPattern);	if (loginMatch) {		console.log(loginMatch[1]);		hipchat.postMessage({			'room': '297355', 			'from': 'MineCraft', 			'message': 'Looks like '+loginMatch[1]+' just logged in.', 			'notify': 0		});	}});
