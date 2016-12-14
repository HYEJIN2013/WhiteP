/*   ■======================■       ¤Script by nentox¤ ■==============================■  Bug und/oder Fehler Meldungen            bitte per         Email oder Skype              an mich          ■===========■             ●Skype●         germanfroggy89             ●Email●        nentox125@gmail.com           ■=========■            {×[====]×}            v. 1.1.2 Beta                                                    ChangeLog:---------1.0.0•First Release!---------1.1.0 Beta•diverse Bug Fixes •Code Optimierung---------1.1.1 Beta•Fehler der alten Version behoben---------1.1.2•Fehler aus 1.1.1 Beta wurden behoben!---------*/
var mod = false ;
function modTick () {
if(mod == true) {Player.setCanFly(1);
}
if(mod == false){Player.setCanFly(0);
}} 
function procCmd (cmd) {
if (cmd == "fliegenOff" ){mod = falseclientMessage("Deaktiviert");
}

if (cmd == "fliegenOn" ){mod = trueclientMessage("Aktiviert");
}
}
function newLevel() {clientMessage ("§4Mach §7/fliegenOn §4oder §7/fliegenOff");}
