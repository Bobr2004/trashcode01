from .Weapons import Weapon
from json import load
from random import randint

with open("data/data.json", "r") as jin:
    battle_data = load(jin)


class Hero:
    def __init__(self, name: str, max_hp: int, souls: float, agility: int, strength: int, weapon: Weapon):
        self.name = name
        self.lvl = None
        self.max_hp = max_hp
        self.health = max_hp
        self.damage_block = 0
        self.agility = agility
        self.strength = strength
        self.weapon = weapon
        self.__damage = None
        self.lvl = (agility + strength + (max_hp - 380) / 40) - 3
        self.souls = souls
        self.bag: list = [self.weapon]
        self.__lvl_price = None

    @property
    def lvl_price(self):
        if self.__lvl_price is None:
            self.__lvl_price = round(150 * 1.1 ** self.lvl)
        return self.__lvl_price

    @property
    def damage(self):
        if self.__damage is None:
            self.__damage = self.weapon.base_damage + (
                    self.damage_from_scale("strength", "strength_scale") +
                    self.damage_from_scale("agility", "agility_scale")
            )
            self.__damage = self.__damage + 0.05 * self.__damage * int(
                self.weapon.weapon_type == "sword" and self.agility == self.strength)
        return self.__damage

    def reset_damage(self):
        self.__damage = None

    def damage_from_scale(self, stat, scale):
        x = getattr(self, stat)
        y = getattr(self.weapon, scale)
        if x > 20:
            return 20 * battle_data["dmg_scales"][y] + (x - 20) * battle_data["dmg_scales"][y] * 0.5
        else:
            return x * battle_data["dmg_scales"][y]

    def lvl_up(self, stat):
        match stat:
            case 1:
                self.max_hp += 40
                self.damage_block += 2.5
            case 2:
                self.agility += 1
                self.__damage = None
            case 3:
                self.strength += 1
                self.__damage = None
        self.spend_souls(self.lvl_price)
        self.lvl += 1
        self.__lvl_price = None

    def spend_souls(self, value):
        self.souls -= value

    def obtain_weapon(self, weapon):
        self.weapon = weapon
        self.__damage = None

    def get_item(self, item):
        self.bag.append(item)

    # show
    def show_stats(self):
        for attr, value in self.__dict__.items():
            if attr == "name":
                print(f"{value}")
                continue
            elif attr == "damage_block":
                attr = "health_regen"
            elif attr == "max_hp":
                attr = "health"
            elif attr == "health":
                continue
            elif attr == "weapon":
                value = value.name
            elif attr == "_Hero__damage":
                attr = "damage"
                value = self.damage
            elif attr == "bag":
                continue
            elif attr == "_Hero__lvl_price":
                continue
            print(f"{attr.title()} : {value}")
        print("---" * 5)

    # show main stats
    def show_main(self, other=None):
        stats = ["name", "souls"]
        if not (other is None):
            stats.extend(other)
        for attr in stats:
            if attr == "name":
                print(f"{getattr(self, attr)}")
                continue
            elif attr == "max_hp":
                attr = "health"
                self.health = self.max_hp
            elif attr == "damage_block":
                print(f"{'health_regen'.title()} : {getattr(self, attr)}")
                continue
            elif attr == "_Hero__damage":
                print(f"{'damage'.title()} : {round(self.damage)}")
                continue
            elif attr == "weapon":
                print(f"{attr.title()} : {getattr(self, attr).name}")
                continue
            print(f"{attr.title()} : {getattr(self, attr)}")
        print("---" * 5)

    def show_bag(self):
        for index, item in enumerate(self.bag, 1):
            print(f"{index} - {item.name}")

    # fight

    # swords
    def swords_skills(self):
        isSword = int(self.weapon.weapon_type == "sword")
        isHummer = int(self.weapon.weapon_type == "hummer")
        isDagger = int(self.weapon.weapon_type == "dagger")
        tab = ' ' * (len(str(round(self.health, 1)) + str(self.max_hp)) - 1)
        actions = {
            "slash": (self.damage, "slash"),
            "prick": (((self.damage + (self.agility * 2)) * (1.1 + + (0.05 * isDagger) + (0.1 * isSword))), "thrust"),
            "swing": (((self.damage + (self.strength * 6)) * (1.5 + (0.3 * isSword))), "slash")
        }
        print("\n"
              f"{tab} 1 - attack            ({round(actions['slash'][0])} damage)\n"
              f"{tab} 2 - rage prick {75 + (5 * isDagger) + (0.3 * self.agility)}%  ({round(actions['prick'][0])} damage)\n"
              f"{tab} 3 - heavy attack      ({round(actions['swing'][0])} damage)\n\n"
              f"{tab} 4 - block      ({(60 + (self.strength * 0.5) + (10 * isHummer)):.1f}% reduction)\n"
              f"{tab} 5 - dodge      ({60 + (self.agility * 0.5) + (10 * isDagger):.1f}% chance)\n")

        while True:
            action = input()
            match action:
                case "1":
                    attack = (actions['slash'][0], 1, 2 + 5 * isDagger, 0)
                case "2":
                    attack = (
                        int(randint(1, 100) <= (75 + 5 * isDagger + (0.3 * self.agility))) * actions['prick'][0], 1,
                        2 + 5 * isDagger, 0)
                case "3":
                    attack = (actions['swing'][0], 2, 2 + 5 * isDagger, 0)
                case "4":
                    attack = (0, 1, 2 + (5 * isDagger), 60 + (10 * isHummer) + (0.5 * self.strength))
                case "5":
                    attack = (0, 1, 60 + (10 * isDagger) + (self.agility * 0.5), 0)
                case _:
                    print("Try again")
                    continue
            return attack
