# Combat simulator
#

from math import floor
from random import randrange
from copy import copy
import numpy as np

def parseDiceRoll(dice):
    dice = dice.strip()
    if 'd' not in dice:
        raise RuntimeError("dice invalid.")
    s = dice.split("d")
    num = int(s[0]) if s[0] != "" else 1
    if '+' in s[1]:
        s = s[1].split("+")
        tdice = int(s[0])
        bonus = int(s[1])
    elif '-' in s[1]:
        s = s[1].split("-")
        tdice = int(s[0])
        bonus = -int(s[1])
    else:
        tdice = int(s[1])
        bonus = 0

    results = []

    for i in range(num):
        results.append(randrange(1, tdice+1))

    return sum(results) + bonus


def log(*argv):
    s=""
    for arg in argv:
        s += " "+str(arg)
    print(s)


def d20():
    return randrange(1, 21)


def d20le(num):
    return d20() <= num


class Sheet(object):

    def __init__(self, name, attrs, hasFight=False, hasShot=False):
        self.name = name
        self.str = attrs[0]
        self.dex = attrs[1]
        self.con = attrs[2]
        self.Int = attrs[3]
        self.wis = attrs[4]
        self.cha = attrs[5]
        self.hasFight = hasFight
        self.hasShot = hasShot
        self.fightBonus = 0
        self.shotBonus = 0
        self.blocks = 0
        self.shield = "none"
        self.luck = 0
        self.wdice = "d4"
        self.fight = True
        self.armor = 0
        self.life = self.con + 1

    def Fight(self):
        return (self.str if self.hasFight else self.str-2) + self.fightBonus

    def Dodge(self):
        return floor((self.dex-10)/2)

    def Shot(self):
        return (self.dex if self.hasShot else self.dex-2) + self.shotBonus

    def SetShield(self, shield):
        self.blocks = {
            "wood-small": 1,
            "wood-medium": 2,
            "wood-large": 3,
            "steel-small": 3,
            "steel-medium": 4,
            "steel-large": 5,
            "none": 0
        }[shield]
        self.shield = shield

    def RepairShield(self):
        self.SetShield(self.shield)

    def Block(self):
        if self.blocks > 0:
            self.blocks -= 1
            return True
        return False

    def SetWeaponDice(self, dice, fight=True):
        self.fight = fight
        if fight:
            mod = floor(self.str/2 - 5)
            bonus = "+"+str(mod) if mod > 0 else ""
            bonus += str(mod) if mod < 0 else ""
            self.wdice = dice + bonus
        else:
            self.wdice = dice

    def TakeDmg(self, num):
        dmg = num - self.armor
        dmg = dmg if dmg > 0 else 1
        self.life -= dmg
        return dmg

    def DealsDmg(self):
        return parseDiceRoll(self.wdice)

    def __attack(self, sheet, num):
        if d20le(num + sheet.Dodge()):
            if sheet.Block():
                log(sheet.name + " blocks the Attack of " + self.name)
                return False
            log(sheet.name + " was attacked by " + self.name + " and take "
                + str(sheet.TakeDmg(self.DealsDmg())) + " of damage.")
            return True
        log(self.name + " missed the attack.")
        return False

    def Attack(self, sheet):
        if self.fight:
            self.__attack(sheet, self.Fight())
        else:
            self.__attack(sheet, self.Shot())

    def CombatX1(self, sheet):
        i1 = d20()+self.dex
        i2 = d20()+sheet.dex
        p1 = copy(self) if i1 > i2 else copy(sheet)
        p2 = copy(sheet) if i1 > i2 else copy(self)
        rounds = 0

        log(p1.name, p1.life, p2.name, p2.life)

        while (p1.life > 0 and p2.life > 0):
            rounds += 1
            p1.Attack(p2)
            if p2.life > 0:
                p2.Attack(p1)

        res = {}
        res[p1.name] = p1.life
        res[p2.name] = p2.life
        res["turns"] = rounds
        res["winner"] = p1.name if (p1.life > 0) else p2.name
        return res

    def _anyAlive(self, sheets):
        a = map(lambda x: x.Alive(), sheets)
        return any(a)

    def Alive(self):
        return self.life > 0

    def CombatSolo(self, sheets):
        if len(sheets) == 1:
            self.CombatX1(sheets)

        vinit = []
        p = np.array([copy(self)])
        vinit.append(d20()+self.dex)

        for s in sheets:
            vinit.append(d20()+s.dex)
            p = np.append(p, copy(s))

        init = np.array(vinit).argsort()[::-1]

        while (self._anyAlive(p[1:]) and p[0].Alive()):
            for i in range(len(init)):
                attacker = p[init[i]]
                if attacker.Alive():
                    if init[i] != 0:
                        attacker.Attack(p[0])
                    else:
                        next_alive = 0
                        for char in p[1:]:
                            if char.Alive(): break
                            next_alive += 1
                        p[0].Attack(p[next_alive+1])

        return p



