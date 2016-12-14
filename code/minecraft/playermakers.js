.....
var INTERVAL = 60 * 1000;var ANIMATED = true;
var JSON_PATH = "players.json";var IMG_PATH = "static/markers/{icon}.png";var IMG_SIZE_FACTOR = 1.5;
function PlayerMarker(ui, username, icon, world, pos) {	this.ui = ui;
	this.username = username;	this.world = world;	this.active = true;
	this.marker = L.marker(this.ui.mcToLatLng(pos.x, pos.z, pos.y), {		title: this.username,		icon: L.icon({			iconUrl: IMG_PATH.replace("{icon}", icon),			iconSize: [16 * IMG_SIZE_FACTOR, 32 * IMG_SIZE_FACTOR],		}),	});	this.marker.addTo(this.ui.lmap);
	this.moveCounter = 0;	this.start = null;	this.destination = pos;}
......
MapPlayerMarkerHandler.prototype.create = function() {	ui = this.ui;
	var handler = function(self) {		return function() {			$.ajax({				dataType: "json",				url: JSON_PATH,				success: function(data) {					self.updatePlayers(data);				},				error: function(xhr,err,txt) {					console.log('player error: '+err+' -> '+txt);				}			});			// I was getting errors, but they were never reported, so black hole of doom			//$.getJSON(JSON_PATH, function(data) { console.log('wtf...');self.updatePlayers(data); });		};	}(this);
	window.setTimeout(handler, 500);	window.setInterval(handler, INTERVAL);};
....
MapPlayerMarkerHandler.prototype.updatePlayers = function(data) {	if(!data)		return;
	var globalPlayersOnline = [];	var worldPlayersOnline = 0;	for(var i = 0; i < data["players"].length; i++) {		var user = data["players"][i];		var username = user.username;		var pos = {x: user.x, z: user.z, y: user.y};
		var player;
		if(user.username in this.players) {			player = this.players[username];		} else {			player = new PlayerMarker(ui, username, user.icon, user.world, pos);			this.players[username] = player;		}
		player.setActive(user.world == this.currentWorld);
		if(player.active) {			worldPlayersOnline++;			player.move(pos);		}		globalPlayersOnline.push(username);	}
	for(var name in this.players) {		if(globalPlayersOnline.indexOf(name) == -1) {			this.players[name].setActive(false);			delete this.players[name];		}	}
	document.title = "(" + worldPlayersOnline + "/" + globalPlayersOnline.length + ") " + this.documentTitle;};
....
