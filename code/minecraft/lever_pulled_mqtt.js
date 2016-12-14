var mqtt = require('sc-mqtt');  var client = mqtt.client(); // local host is default. Otherwise use host, user/pwdclient.connect();
//Subscribe to changes in the state of the Arduinoclient.subscribe('/arduino/1/status');var player; // To remember who pulled the switch
// Here we tell Minecraft to give us control after certain eventsevents.on('player.PlayerInteractEvent', function (listener, event) { 	var block = event.getClickedBlock(); // Which block?	var type = block.getType();			 // What type is it? 	player = event.player; 				 // Note who shall be alerted
	if(type==org.bukkit.Material.LEVER) {		var loc = block.location;	//We need to find the location				// Compose a MQTT Topic which contains the world name and location of the block		var mqttTopic='minecraft/'+loc.world.name+'/lever/'+loc.x+','+loc.y+','+loc.z+'/status';
		// Is the lever up or down?		var state='';		if (block.data==3){			state='DOWN'		}		else		{			state='UP'		} 	    
		// Now publish it  		client.publish(mqttTopic, 	// which topic  		state,				// the status  		1,				// QoS 1 ( deliver at least once )  		true); 				// broker should retain message
	}})
//Give the player a notification if a message arrivesclient.onMessageArrived(function(topic, message){	var bytes = message.payload;		var javaString = new java.lang.String(bytes);	// Using the Java libraries, we can convert from binary	player.sendMessage(javaString.slice(0, - 1));	});
