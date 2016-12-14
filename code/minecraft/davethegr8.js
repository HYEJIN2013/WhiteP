exports.greet = function( player ) {
    echo( player, 'Hi ' + player.name);
}

var mine = {
	house: function () {
		var drone = box(blocks.brick.mossy,7,5,7);
		drone.up().fwd(1).right(1);
		drone.box(blocks.air,5,4,5);
	},
	hole: function(l, w) {
		l = l || 8;
		w = w || l;

		var utils = require('utils'),
			pointer = utils.locationToJSON(utils.getMousePos());

		down(pointer.y - 4).box(blocks.air, w, pointer.y - 4 + 1, l);
	},
	mine: function () {
		var utils = require('utils'),
			pointer = utils.getMousePos(),
			block = utils.blockAt(pointer);

		echo(block);
	}
};

exports.davethegr8 = mine;

