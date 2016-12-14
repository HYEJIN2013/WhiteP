Object.prototype.typeId = function (){alert(this.type);}function MinecraftAnimal(type){this.type=type;}var cow = new MinecraftAnimal("11");var pig = new MinecraftAnimal("12");
cow.typeId();pig.typeId();
