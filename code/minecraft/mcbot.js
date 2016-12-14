var spawn = require('child_process').spawn,
	minecraftProcess = spawn('java', ['-jar', 'minecraft_server.1.7.2.jar'], {
		cwd: 'Absolute path to minecraft server jar here!'
	});

var util = require("util");
var irc = require('irc'); // Remember to run "npm install irc!"

var channel = "channel name here, remember '#' before the name!";
var bot = new irc.Client("irc server here", "bot name here", {
    channels: [channel],
    realName: 'Name shown on /whois here'
});

bot.addListener('message#', function(nick, channel, text, message) {
	console.log("channel speak");
	minecraftProcess.stdin.write("/say <" + nick + "> " + text + "\n");
});

function death(chunk, matches) {
	var string = matches[1] + " died!";
	if(matches.length >= 3)
		string += " Killed by " + matches[2];
	if(matches.length >= 4)
		string += " with " + matches[3] + "!";
	string += " :D";
	bot.say(channel, string);
	console.log(string);
}


function join(chunk, player) {
	bot.say(channel, player + " is a champ and joined Sandberg.");
	console.log('join');
}

function quit(chunk, player) {
	bot.say(channel, player + " must have experienced a terrible catastrophe, he just quit Sandberg!");
	console.log('quit');
}

function achievement(chunk, player, achievement) {
	bot.say(channel, player + " jsut achieved " + achievement + "!");
	console.log('achievement');
}

function error(data) {
	console.log('error');
}

function chat(chunk, player, msg) {
	if(player.indexOf('server') > -1) return;
	bot.say(channel, '<' + player + '> ' + msg);
}

// Listen on standard input
process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(chunk) {
  if(chunk.indexOf('quit') > -1) {
  	bot.disconnect("Good bye cruel world!");
  	minecraftProcess.kill();
  	console.log('quit');
  	process.stdin.pause();
  }
});

/**
 * Fetch regular standard output from minecraft server.
 * 
 *************/
minecraftProcess.stdout.on('data', function(data) {
	var chunk = data.toString();
	// Deaths
	var match =
		// Anvil
		chunk.match(/([a-z0-9_]*) was squashed by a falling anvil/i) ||
		// Cactus
		chunk.match(/([a-z0-9_]*) was pricked to death/i) ||
		chunk.match(/([a-z0-9_]*) walked into a cactus whilst trying to escape ([a-z0-9_]*)/i) ||
		// Dispenser arrow
		chunk.match(/([a-z0-9_]*) was shot by arrow/i) ||
		// Drowning
		chunk.match(/([a-z0-9_]*) drowned/i) ||
		chunk.match(/([a-z0-9_]*) drowned whilst trying to escape ([a-z0-9_]*)/i) ||
		// Explosion
		chunk.match(/([a-z0-9_]*) blew up/i) ||
		chunk.match(/([a-z0-9_]*) was blown up by ([a-z0-9_]*)/i) ||
		// Falling
		chunk.match(/([a-z0-9_]*) hit the ground too hard/i) ||
		chunk.match(/([a-z0-9_]*) fell from a high place/i) ||
		chunk.match(/([a-z0-9_]*) fell off a ladder/i) ||
		chunk.match(/([a-z0-9_]*) fell off some vines/i) ||
		chunk.match(/([a-z0-9_]*) fell out of the water/i) ||
		chunk.match(/([a-z0-9_]*) fell into a patch of fire/i) ||
		chunk.match(/([a-z0-9_]*) fell into a patch of cacti/i) ||
		chunk.match(/([a-z0-9_]*) was doomed to fall (by ([a-z0-9_]*))/i) ||
		chunk.match(/([a-z0-9_]*) was shot off some vines by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was shot off a ladder by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was blown from a high place by ([a-z0-9_]*)/i) ||
		// Fire
		chunk.match(/([a-z0-9_]*) went up in flames/i) ||
		chunk.match(/([a-z0-9_]*) burned to death/i) ||
		chunk.match(/([a-z0-9_]*) was burnt to a crisp whilst fighting ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) walked into a fire whilst fighting ([a-z0-9_]*)/i) ||
		// Mob
		chunk.match(/([a-z0-9_]*) was slain by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was shot by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was fireballed by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was killed by ([a-z0-9_]*) using (magic)/i) ||
		chunk.match(/([a-z0-9_]*) got finished off by ([a-z0-9_]*) using ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was slain by ([a-z0-9_]*) using ([a-z0-9_]*)/i) ||
		// Lava
		chunk.match(/([a-z0-9_]*) tried to swim in lava/i) ||
		chunk.match(/([a-z0-9_]*) tried to swim in lava while trying to escape ([a-z0-9_]*)/i) ||
		// Lightning
		chunk.match(/([a-z0-9_]*) died/i) ||
		// PvP
		chunk.match(/([a-z0-9_]*) got finished off by ([a-z0-9_]*) using ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was slain by ([a-z0-9_]*) using ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) got finished off by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was shot by ([a-z0-9_]*) using ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was slain by ([a-z0-9_]*)/i) ||
		chunk.match(/([a-z0-9_]*) was killed by ([a-z0-9_]*) using (magic)/i) ||
		// Potion of harming
		chunk.match(/([a-z0-9_]*) was killed by magic/i) ||
		// Starvation
		chunk.match(/([a-z0-9_]*) starved to death/i) ||
		// Suffocation
		chunk.match(/([a-z0-9_]*) suffocated in a wall/i) ||
		// Thorns enchantment
		chunk.match(/([a-z0-9_]*) was killed while trying to hurt ([a-z0-9_]*)/i) ||
		// Void and /kill
		chunk.match(/([a-z0-9_]*) fell out of the world/i) ||
		chunk.match(/([a-z0-9_]*) fell from a high place and fell out of the world/i) ||
		chunk.match(/([a-z0-9_]*) was knocked into the void by ([a-z0-9_]*)/i) ||
		// Wither effect
		chunk.match(/([a-z0-9_]*) withered away/i);

	if(match && match.length) {
		death(chunk, match);
		return;
	}

	match = chunk.match(/([a-z0-9_]*) joined the game/i);
	if(match && match.length) {
		join(chunk, match[1]);
	}

	match = chunk.match(/([a-z0-9_]*) left the game/i);
	if(match && match.length) {
		quit(chunk, match[1]);
	}

	match = chunk.match(/([a-z0-9_]*) has just earned the achievement \[([a-z0-9 !]+)\]/i);
	if(match && match.length) {
		achievement(chunk, match[1], match[2]);
	}

	match = chunk.match(/: <([a-z0-9_]*)> (.*)/i);
	if(match && match.length) {
		chat(chunk, match[1], match[2]);
	}
});

minecraftProcess.on('stderr', function (data) {
    error(chunk, match[1], match[2]);
    console.log('error with minecraft server: ', message);
});

bot.addListener('error', function(message) {
    console.log('error with irc bot: ', message);
});


