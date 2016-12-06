import random

def diceRoll(numOfDice, maxNum):
    summ = 0
    for i in xrange(numOfDice):
        summ += random.randrange(1,maxNum+1)

    return summ

#inherit from lambardo class
class ForceUser(object):
    def __init__(self, hit, dmg, df, mhp, mfp, chp, cfp, numOfDice=1, maxNum=3, rank=1, side='neutral'):
        self.hitBonus = hit
        self.dmg = dmg
        self.defense = df
        self.maxHP = mhp
        self.currHP = chp
        self.maxFP = mfp
        self.currFP = cfp
        self.numOfDice = numOfDice
        self.maxNum = maxNum
        self.rank = rank
        self.side = side

    def takeDmg(self, dmg):
        self.currHP -= dmg
        if self.currHP <= 0:
            self.currHP = 0

    def loseFP(self,fp):
        self.currFP -= fp
        if self.currFP <= 0:
            self.currFP = 0

    def restoreHealth(self, hp):
        self.currHP += hp
        if self.currHP > self.maxHP:
            self.currHP = self.maxHP

    def regenForcePoints(self,fp = 1):
        self.currFP += fp
        if self.currFP > self.maxFP:
            self.currFP = self.maxFP

    def reset(self):
        self.currHP = self.maxHP
        self.currFP = self.maxFP

    def isAlive(self):
        if self.currHP == 0:
            return False
        return True

    def displayOptions(self):
        return 'Attack'

    def validOptions(self, num):
        options = self.displayOptions()
        if len(options) >= num:
            tmphp, tmpfp = self.currHP, self.currFP
            if self.performAction(options[num-1],0) > 0:
                self.currHP, self.currFP = tmphp, tmpfp
                return options[num-1]
        return False

    def Attack(self, enemyDef):
        if diceRoll(1, 20) + self.hitBonus >= enemyDef:
            return diceRoll(self.numOfDice, self.maxNum)
        return 0

    def performAction(self, actionStr, enemyDef):
        if actionStr == 'Attack':
            return self.Attack(enemyDef)
        else:
            return eval('self.'+actionStr+'()')

    def displayStats(self):
        print self
        print self.currHP
        print self.currFP
    '''
    Light Side
    '''
class Youngling(ForceUser):
    def __init__(self, hit = 1, dmg = 0, df = 0, mhp = 20, mfp = 2, chp = 20, cfp = 2, numdice = 1, maxnum = 3, rank=1, side='light'):
        super(Youngling,self).__init__(hit,dmg,df,mhp,mfp,chp,cfp,numdice, maxnum, rank, side)

    def ForcePush(self):
        if self.currFP < 2:
            print 'not enough Force Points'
            return False
        self.loseFP(2)
        return diceRoll(1,6)

    def displayOptions(self):
        options = []
        options.append(super(Youngling,self).displayOptions())
        options.append('ForcePush')
        return options


class Padawan(Youngling):
    def __init__(self):
        super(Padawan, self).__init__(3,1,12,30,4,30,4,1,6,2)

    def Heal(self):
        if self.currFP < 3:
            print 'not enough force points'
            return False
        self.loseFP(3)
        self.restoreHealth(diceRoll(2,6) + 6)
        return 1

    def displayOptions(self):
        options = []
        options.append(super(Padawan, self).displayOptions())
        options.append('Heal')
        return options

class JediKnight(Padawan):
    def __init__(self):
        super(Padawan,self).__init__(6,2,18,50,6,50,6,2,6,3)

    def LightsaberFlurry(self):
        if self.currFP < 5:
            print 'not enough force points'
            return False
        self.loseFP(5)
        return diceRoll(3,6) + 6

    def displayOptions(self):
        options = []
        options.append(super(JediKnight, self).displayOptions())
        options.append('LightsaberFlurry')
        return options

class JediMaster(JediKnight):
    def __init__(self):
        super(Padawan, self).__init__(12, 3, 22, 75, 8, 75, 8,3,6,4)

    def ForceDrain(self):
        if self.currFP < 7:
            print 'not enough force points'
            return False
        self.loseFP(7)
        return 7

    def displayOptions(self):
        options = []
        options.append(super(JediMaster, self).displayOptions())
        options.append('ForceDrain')
        return options

    '''
    Dark Side
    '''
class Acolyte(ForceUser):
    def __init__(self, hit = 1, dmg = 0, df = 0, mhp = 20, mfp = 2, chp = 20, cfp = 2, numdice = 1, maxnum = 3, rank=1, side='dark'):
        super(Acolyte,self).__init__(hit,dmg,df,mhp,mfp,chp,cfp,numdice,maxnum,rank,side)

    def ForcePush(self):
        if self.currFP < 2:
            print 'not enough Force Points'
            return False
        self.loseFP(2)
        return diceRoll(1, 6)

    def displayOptions(self):
        options = []
        options.append(super(Acolyte, self).displayOptions())
        options.append('ForcePush')
        return options

class Apprentice(Acolyte):
    def __init__(self):
        super(Apprentice, self).__init__(3, 3, 12, 25, 4, 25, 4,1,6,2)

    def DrainLife(self):
        if self.currFP < 3:
            print 'not enough force points'
            return False
        self.loseFP(3)
        tmp = diceRoll(1,6) + 3
        self.restoreHealth(tmp)
        return tmp

    def displayOptions(self):
        options = []
        options.append(super(Acolyte, self).displayOptions())
        options.append('DrainLife')
        return options

class SithMaster(Apprentice):
    def __init__(self):
        super(Apprentice, self).__init__(6, 6, 15, 40, 6, 40, 6,2,6,3)

    def ForceChoke(self):
        if self.currFP < 5:
            print 'not enough force points'
            return False
        self.loseFP(5)
        return diceRoll(3,6) + 6

    def displayOptions(self):
        options = []
        options.append(super(Acolyte, self).displayOptions())
        options.append('ForceChoke')
        return options

class SithLord(SithMaster):
    def __init__(self):
        super(Apprentice, self).__init__(12, 8, 18, 60, 8, 60, 8,3,6,4)

    def ForceLightning(self):
        if self.currFP < 7:
            print 'not enough force points'
            return False
        self.loseFP(7)
        return diceRoll(5,6) + 5

    def displayOptions(self):
        options = []
        options.append(super(Acolyte, self).displayOptions())
        options.append('ForceLightning')
        return options


class Player(object):
    expDic = {1 : 199, 2 : 399, 3 : 799, 4 : 800}
    def __init__(self, forceuser, name, exp):
        self.FU = forceuser
        self.playerName = name
        self.exp = exp

    def gainExp(self, exp):
        self.exp += exp
        if self.exp > self.expDic[self.FU.rank] and self.FU.rank != 4:
            self.levelUp()

    def levelUp(self):
        if self.FU.rank >= 4:
            return
        if self.FU.side == 'light':
            if self.FU.rank == 1:
                self.FU = Padawan()
            elif self.FU.rank == 2:
                self.FU = JediKnight()
            else:
                self.FU = JediMaster()
        else:
            if self.FU.rank == 1:
                self.FU = Apprentice()
            elif self.FU.rank == 2:
                self.FU = SithMaster()
            else:
                self.FU = SithLord()
