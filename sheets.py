from combat import *

Baldur = Sheet("Baldur", [15, 8, 11, 12, 7, 10], True, True)
Baldur.SetShield("steel-medium")
Baldur.SetWeaponDice("d8", True)
Baldur.armor = 3

Goblin = Sheet("Goblin", [11, 13, 12, 10, 9, 6], True, True)
Goblin.life = 6
Goblin.fightBonus = 1
Goblin.SetWeaponDice("d6", True)
Goblin.SetShield("wood-medium")
Goblin.armor = 1

sheets = []
for i in range(3):
    sheets.append(copy(Goblin))

results = Baldur.CombatSolo(sheets)


if (results[0].Alive()):
    print("Baldur wins!!!")
else:
    print("Baldur defeated by ", len(sheets), " goblins.")

for i in results:
    print(i.name, i.life)

