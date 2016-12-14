/*  Secret Door Script for CustomNPCs  Tags: customnpcscript, Secret Door  usage:  var thisSecretDoor;  function init(event){    //the first item in the array is the block used for the scripted block, the rest of the array, defines the door blocks    thisSecretDoor = new SecretDoor(event, ["minecraft:stonebrick", "minecraft:stonebrick", "minecraft:stonebrick"]);  }  function interact(event){    thisSecretDoor.interact(event);  } */
function SecretDoor(initEvent, blockList){  var block = this.block = initEvent.block;  this.blockList = blockList;
  this.block.setModel(this.block.getWorld().createItem(blockList[0], 0, 1));
  this.x = Math.floor(block.getX());  this.y = Math.floor(block.getY());  this.z = Math.floor(block.getZ());
  this.isOpen = false;
  this.close();}
  SecretDoor.prototype.open = function(){
    var world = this.block.getWorld();    this.block.executeCommand("/playsound tile.piston.in @a[r=10] "+this.x+" "+this.y+" "+this.z);    for(var i=1;i<this.blockList.length;i++){      var blockY = this.y - i;      world.setBlock(this.x, blockY, this.z, "minecraft:air", 0);    }    this.isOpen = true;  };
  SecretDoor.prototype.close = function() {    var world = this.block.getWorld();    this.block.executeCommand("/playsound tile.piston.out @a[r=10] "+this.x+" "+this.y+" "+this.z);
    for(var i=1;i<this.blockList.length;i++){      var blockY = this.y - i;      world.setBlock(this.x, blockY, this.z, this.blockList[i], 0);    }    this.isOpen = false;  };
  SecretDoor.prototype.interact = function(event) {    if(this.isOpen===true){      this.close();    }else{      this.open();    }  };
