console.log("start");
var fs = require('fs');
const MINECRAFT_PATH = "<need specified your minecraft dir path>/minecraft/";const SPATH = MINECRAFT_PATH + "assets/objects/";const DPATH = "<need specified your destination dir path>/";
var json = require(MINECRAFT_PATH + 'assets/indexes/1.8.json');var o = json.objects;
for( var key in o ){  if( /.*\.ogg$/.test(key)){    var swap_key = key.replace(/\//g, "_");
    var hash = o[key].hash;    var dir = hash.substr(0, 2);    console.log(key, dir + "/" + hash);
    var stat = fs.statSync( SPATH + dir + "/" + hash );
    var ws = fs.createWriteStream( DPATH + swap_key );    fs.createReadStream( SPATH + dir + "/" + hash).pipe( ws );  }}
