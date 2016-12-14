var proto=require("./../../enums/protocol");var fs=require("fs");
function transformProtocol(protocol){  var transformedProtocol = Object    .keys(protocol)    .reduce(function(transformedProtocol, state) {      transformedProtocol[state] = Object        .keys(protocol[state])        .reduce(function(stateO, direction) {          stateO[direction] = Object            .keys(protocol[state][direction])            .reduce(function(packetsO, packetName) {              packetsO[packetName] = transformPacket(protocol[state][direction][packetName]);              return packetsO;            }, {});          return stateO;        }, {});      return transformedProtocol;    }, {});  transformedProtocol=reorder(["handshaking","status","login","play"],transformedProtocol);  return transformedProtocol;}
function reorder (order, obj) {  return order.reduce (function (rslt, prop) {    rslt[prop] = obj[prop];    return rslt;  }, {});}
function write(protocol){  fs.writeFile("../../enums/protocol.json", JSON.stringify(protocol,null,2));}

function transformPacket(packet){  return {    "id":packet.id,    "fields":transformFields(packet["fields"])  };}
function transformFields(fields){  return fields.map(function(field){return transformField(field);});}
function transformField(field){  return {    "name":field["name"],    "type":transformType(field)  }}
function transformType(field) {  if(field.type == "container")    return ["container", transformFields(field.typeArgs["fields"])];  if(field.type == "buffer")    return ["buffer", {"countType": field.typeArgs["countType"]}];  if(field.type == "condition") {   return ["condition", {     "type":transformType(field.typeArgs),     "field":field.typeArgs["field"],     "values":field.typeArgs["values"],     "this":field.typeArgs["this"],     "different":field.typeArgs["different"]   }];  }  if(field.type=="array")    return ["array", field.typeArgs["count"] ? field.typeArgs : {      "type":transformType(field.typeArgs),      "countType":field.typeArgs["countType"]    }];
  return field["type"];}
write(transformProtocol(proto));
