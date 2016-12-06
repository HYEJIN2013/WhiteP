import random, ForceUsers, time
import jedigame

def diceRoll(numOfDice, maxNum):
    summ = 0
    for i in xrange(numOfDice):
        summ += random.randrange(1,maxNum+1)

    return summ

def endTurn(jedi, sith):
    # end turn (regen fp)
    jedi.regenForcePoints()
    sith.regenForcePoints()

def Battle(game):
    global player1
    global player2
    # make two classes for combat


    jedi = player1.FU
    sith = player2.FU
    print 'Combat Begin'
    game.enter_combat(game.characters['jedi'], 'up')
    game.enter_combat(game.characters['sith'], 'down')

    while jedi.isAlive() and sith.isAlive():
        assert isinstance(jedi, ForceUsers.ForceUser)
        game.jedigame.actions = []
        jediStatus = [player1.playerName , "     Health:" + str(jedi.currHP) ,
            "     Force:" + str(jedi.currFP)]
        sithStatus = [player2.playerName , "     Health:" + str(sith.currHP) ,
            "     Force:" + str(sith.currFP)]
        for i, status in enumerate(jediStatus):
            game.jedigame.actions.append(jedigame.JediAction(status, 20,400 + (i*35),0,0))

        for i, status in enumerate(sithStatus):
            game.jedigame.actions.append(jedigame.JediAction(status, 200, 400 + (i*35), 0, 0))

        jedi.displayStats()
        sith.displayStats()

        for i,s in enumerate(jedi.displayOptions()):
            print str(i+1) + ': ' + s
        jediInput = False
        while jediInput == False:
            jediInput = raw_input('Select option: ')
            if len(jediInput) == 0:
                jediInput = False
                continue
            jediInput = jedi.validOptions(int(jediInput))


        for i, s in enumerate(sith.displayOptions()):
            print str(i + 1) + ': ' + s
        sithInput = False
        while sithInput == False:
            sithInput = raw_input('Select option: ')
            if len(sithInput) == 0:
                sithInput = False
                continue
            sithInput = sith.validOptions(int(sithInput))

        # perform attacks
        jediAction = False
        sithAction = False
        # Force Drain cancel other force moves
        if jediInput == 'ForceDrain':
            game.jedigame.actions.append(jedigame.JediAction(player1.playerName + " - Force Drain", 30, 50 + (i * 35), 0, 0))
            game.characters['jedi'].weapon = game.attacks['DrainFP']
            time.sleep(2)
            game.characters['jedi'].weapon = None
            game.jedigame.actions.pop()
            pointsToDrain = jedi.ForceDrain()
            sith.loseFP(pointsToDrain)
            if sithInput == 'Attack':
                sdmg = sith.performAction(sithInput, jedi.defense, game)
                jedi.takeDmg(sdmg)
            endTurn(jedi, sith)
            continue

        # healing occurs first
        if jediInput == 'Heal':
            game.jedigame.actions.append(jedigame.JediAction(player1.playerName + " -- Healing", 30, 50 + (i * 35), 0, 0))
            game.characters['jedi'].weapon = game.attacks['Heal']
            time.sleep(2)
            game.characters['jedi'].weapon = None
            game.jedigame.actions.pop()
            jedi.Heal()
            jediAction = True

        if sithInput == 'Drain Life':
            sith.DrainLife()
            sithAction = True

        # other attacks
        if jediAction == False:
            game.jedigame.actions.append(jedigame.JediAction(
                player1.playerName + " -- " + jediInput, 30, 50 + (i * 35), 0, 0))
            game.characters['jedi'].weapon = game.attacks[jediInput]
            time.sleep(2)
            game.characters['jedi'].weapon = None
            game.jedigame.actions.pop()

            jdmg = jedi.performAction(jediInput, sith.defense)
            sith.takeDmg(jdmg)

        if sithAction == False:
            game.jedigame.actions.append(jedigame.JediAction(
                player2.playerName + " -- " + sithInput, 30, 50 + (i * 35), 0, 0))
            game.characters['sith'].weapon = game.attacks[sithInput]
            time.sleep(2)
            game.characters['sith'].weapon = None
            game.jedigame.actions.pop()

            sdmg = sith.performAction(sithInput, jedi.defense)
            jedi.takeDmg(sdmg)

        endTurn(jedi, sith)


    EndCombat(player1,player2)



def EndCombat(player1, player2):
    dicExp = {'win': lambda x,y: 1.00 + (.20/ (x-y+1)),\
              'loss' : lambda x,y: 0.50 + (.05 / (x-y+1)),\
              'tie' : lambda x,y: (.1 / (x-y+1))}

    if player1.FU.isAlive() and player2.FU.isAlive() == False:
        print player1.playerName + ' Wins!'
        player1.gainExp(100 * dicExp['win'](player2.FU.rank, player1.FU.rank))
        player2.gainExp(100 * dicExp['loss'](player2.FU.rank, player1.FU.rank))
    elif player1.FU.isAlive() == False and player2.FU.isAlive():
        print player2.playerName + ' Wins!'
        player2.gainExp(100 * dicExp['win'](player1.FU.rank,player2.FU.rank))
        player1.gainExp(100 * dicExp['loss'](player1.FU.rank, player2.FU.rank))
    else:
        print player1.playerName + ' and ' + player2.playerName + ' have both been slain!'
        player1.gainExp(100 * dicExp['tie'](player2.FU.rank, player1.FU.rank))
        player2.gainExp(100 * dicExp['tie'](player1.FU.rank, player2.FU.rank))

    player1.FU.reset()
    player2.FU.reset()


if __name__ == "__main__":
    player1 = ForceUsers.Player(ForceUsers.Youngling(),'Steve',0)
    player2 = ForceUsers.Player(ForceUsers.Acolyte(), 'Toby', 0)
    game = jedigame.GamePlay()
    while True:
        Battle(game)
