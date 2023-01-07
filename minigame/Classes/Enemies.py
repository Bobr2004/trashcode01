from .HeroClass import Hero
from random import randint


class Enemy:
    def __init__(self, name: str, max_hp: int, damage: float, souls: int,
                 giant=False, boss=False, end=True, ):
        self.name = name
        self.max_health = max_hp
        self.health = max_hp
        self.damage = damage
        self.souls = souls
        self.end = end
        self.heavy_attck = False
        self.restore = False
        self.name_s = name
        self.isGiant = int(giant)
        self.isBoss = int(boss)

    def fight_back(self, hero, chance=2, coefc=0):
        coefc = (100 - coefc)
        coefc = coefc / 100
        heavy_multiply = 2.5 + (1 * self.isBoss)
        if self.heavy_attck:
            hero.health -= self.damage * coefc * int(randint(1, 100) > (chance + (5 * self.isGiant)))
            self.damage /= heavy_multiply
            self.name_s = self.name
            self.heavy_attck = False
        elif self.restore:
            self.health += 0.15 * self.max_health
            self.name_s = self.name
            self.restore = False

        else:
            self.heavy_attck = randint(1, 100) > 55 - (10 * self.isGiant)
            self.restore = randint(1, 100) <= -5 + (55 * self.isBoss) and (self.health < 0.6 * self.max_health)
            if self.heavy_attck:
                self.damage *= heavy_multiply
                self.name_s = "!!! " + self.name
                self.restore = False
            elif self.restore:
                self.name_s = "+♡+ " + self.name
                self.heavy_attck = False
            else:
                hero.health -= self.damage * coefc * (int(randint(1, 100) > (chance + (5 * self.isGiant))))
        hero.health += hero.damage_block
        if hero.health >= hero.max_hp:
            hero.health = hero.max_hp
        if self.health >= self.max_health:
            self.health = self.max_health


enemies_data = {
    "village": [
        Enemy("Stray dog", 450, 95, 220),
        Enemy("Zombie", 540, 80, 240),
        Enemy("Giant living flesh", 780, 70, 320, giant=True),

        Enemy("Armored Zombie", 720, 100, 330, giant=True),
        Enemy("Ghost", 650, 90, 290),
        Enemy("Limbless demon", 890, 80, 420, giant=True),

        Enemy("Bibus (zombie lord)", 1400, 105, 3600, boss=True)
    ],
    "dungeon": [
        Enemy("Skeleton", 900, 95, 640),
        Enemy("Giant skeleton", 1130, 110, 820, giant=True),
        Enemy("Armless demon", 1040, 100, 770, giant=True),

        Enemy("Troll", 1060, 120, 815),
        Enemy("Giant Troll", 1230, 125, 935, giant=True),
        Enemy("Goblin", 720, 90, 595),
        Enemy("Demon's arm", 900, 80, 1050),

        Enemy("Gleb (troll king)", 1980, 145, 10_840, boss=True)
    ],
    "swamp": [
        Enemy("Fire frog", 1620, 158, 1350),
        Enemy("Giant spider", 1530, 165, 1450, giant=True),
        Enemy("Living moss", 2700, 70, 1650),

        Enemy("Giant rat", 1350, 150, 1350, giant=True),
        Enemy("Giant worm", 1430, 120, 1430, giant=True),
        Enemy("Headless demon", 1515, 135, 1510, giant=True),

        Enemy("Liquid Biliboba", 2340, 180, 20_160, boss=True)
    ],
    "kingdom": [
        Enemy("Soldier", 2800, 215, 2420),
        Enemy("Champion", 3200, 225, 3030),
        Enemy("Knight", 3100, 220, 2810),

        Enemy("Royal executor", 2600, 235, 2520, giant=True),
        Enemy("Hornless demon", 3320, 205, 2950, giant=True),

        Enemy("Ignat (fire dragon)", 5700, 250, 38_800, boss=True)
    ],
    "boss": [
        "biba",
        Enemy("Bili‘bobus (the whole demon)", 7250, 305, 0, boss=True, end=False)]
}
