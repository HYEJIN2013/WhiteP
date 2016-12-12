print("-----")
print("Merhaba! Bu basit program ile basitçe server.properties dosyalarını oluşturabilirsin.")
print("Şimdi sana basit sorular soracağız. Bu soruları yanıtladıktan sonra dosyan hazır olacak.")
print("Sana sorulan sorulara 'Evet' 'Hayır' şeklinde cevap verebileceğin gibi evet yerine 'E' hayır yerine 'H' kullanabilirsin..")
print("Biz büyük küçük harfe dikkat ediyoruz. Sadece yukarıdaki 4 şekilde cevap verebilirsiniz.")
print("-----")
devamEdelim = input("Sorulara geçelim mi? :")

if devamEdelim == "Evet" or devamEdelim == "E":
	print("-----")
	sunucuAdi = input("Sunucunuzun adı nedir? :")
	spawnKorumasi = input("Spawnın kaç block uzağı kırılamasın? :")
	netherSorusu = input("Sunucunuzda nether açık olsun mu? :")
	gameMode = input("Gamemode kaç olsun? (0=survival,1=gamemode) :")
	zorluk = input("Zorluk kaç olsun? (0,1,2 kullanılabilir) :")
	yaratiklar = input("Yaratıklar açık olsun mu? :")
	pvpSorusu = input("PVP açık olsun mu? (oyuncular arası savaş) :")
	hardCore = input("Hardcore açık olsun mu? (Tek ölüm hakkı.) :")
	commandBlock = input("Komut  bloğu açık olsun mu? :")
	maxPlayers = input("Maximum oyuncu sayısı kaç olsun? :")
	serverIP = input("Sunucu IP'nizi yazın :")
	koyluler = input("Köylüler doğsun mu? : ")
	hayvanlar = input("Hayvanlar doğsun mu? :")
	whiteList = input("Whitelist açık olsun mu? : ")
	onlineMod = input("Online mod açık olsun mu? (Açık olursa cracklar giremez!) :")
	aciklama = input("Sunucunuzun açıklaması ne olsun? : ")
	print("-----")

	if netherSorusu == "Evet" or netherSorusu == "E":
		netherSorusu = "true"
	else:
		netherSorusu = "false"

	if yaratiklar == "Evet" or yaratiklar == "E":
		yaratiklar = "true"
	else:
		yaratiklar = "false"

	if pvpSorusu == "Evet" or pvpSorusu == "E":
		pvpSorusu= "true"
	else:
		pvpSorusu= "false"

	if hardCore == "Evet" or hardCore == "E":
		hardCore= "true"
	else:
		hardCore= "false"

	if commandBlock == "Evet" or commandBlock == "E":
		commandBlock= "true"
	else:
		commandBlock= "false"

	if koyluler == "Evet" or koyluler == "E":
		koyluler= "true"
	else:
		koyluler= "false"

	if hayvanlar == "Evet" or hayvanlar == "E":
		hayvanlar= "true"
	else:
		hayvanlar= "false"

	if whiteList == "Evet" or whiteList == "E":
		whiteList= "true"
	else:
		whiteList= "false"

	if onlineMod == "Evet" or onlineMod == "E":
		onlineMod= "true"
	else:
		onlineMod= "false"

	metin = """#Minecraft Server Ayar Dosyası
#Sunucu Adı {}
spawn-protection= {}
max-tick-time=60000
generator-settings=
force-gamemode=false
allow-nether= {}
gamemode= {}
enable-query=false
player-idle-timeout=0
difficulty={}
spawn-monsters={}
op-permission-level=4
resource-pack-hash=
announce-player-achievements=true
pvp={}
snooper-enabled=true
level-type=DEFAULT
hardcore={}
enable-command-block={}
max-players={}
network-compression-threshold=256
max-world-size=29999984
server-port=25565
server-ip={}
spawn-npcs={}
allow-flight=false
level-name=world
view-distance=10
resource-pack=
spawn-animals={}
white-list={}
generate-structures=true
online-mode={}
max-build-height=256
level-seed=
use-native-transport=true
motd={}
enable-rcon=false"""

	dosya = open("server.properties", "w")
	dosya.write(metin.format(
							sunucuAdi,
							spawnKorumasi,
							netherSorusu,
							gameMode,
							zorluk,
							yaratiklar,
							pvpSorusu,
							hardCore,
							commandBlock,
							maxPlayers,
							serverIP,
							koyluler,
							hayvanlar,
							whiteList,
							onlineMod,
							aciklama
							))
	print("Dosyanız hazırlandı. Programla aynı dizinde dosyanızı görebilirsiniz.")
	print("Eğer masaüstünde çalıştırdıysanız dosyanız masaüstündedir.")
