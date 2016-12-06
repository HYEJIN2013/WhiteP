from random import randint
class Monster():
    monsterHealth = 1000
    monsterStrength = 60
    
    def breathFire(self):
        fire = (randint(1,3))
        burn = 100
        if fire == 3:
            fire = (fire*(self.monsterStrength*2))
            fire = (fire+burn)
            print(fire)
            print("Wow that attack did 100 burn damage too!")
        else:
            fire = (fire*(self.monsterStrength*2))
            print(fire)
        #attack 1
    def claw(self):    
        clawAttack = (randint(4,8)*self.monsterStrength/randint(1,4))
        print(clawAttack)
        #attack 2
    def tackle(self):
        if self.monsterHealth > 100:
            tackleAttack = (randint(1,2)*self.monsterStrength)
            print(tackleAttack)
        else:
            tackleAttack = (randint (1,3)*self.monsterHealth)
            print(tackleAttack)

    def humanAttack(self):
        print("What attack do you wanna do?")
        player = int (input("Press 1 for Breathing Fire, 2 to Claw, and 3 to Tackle"))
        if player==1:
            self.breathFire()
        elif player==2:
            self.claw()
        elif player==3:
            self.tackle()
        else:
            self.humanAttack()

    def robotAttack(self):
        robot = str((randint(1,3)))
        if robot == str(1):
            self.breathFire()
        elif robot == str(2):
            self.claw()
        else:
            self.tackle()

    def alive(self):
        if self.monsterHealth > 0:
            return True
        else:
            return False
